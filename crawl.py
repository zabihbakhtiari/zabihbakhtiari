"""
crawl.py - refreshes the real data and screenshots used by build.py.

    python crawl.py            # counts + screenshots
    python crawl.py --no-shots # counts only

Counts come from the live store's public Shopify catalogue and its sitemap.
Screenshots are taken with headless Microsoft Edge or Google Chrome, with real
phone emulation for the mobile captures (needs: pip install websocket-client).
Everything lands in ./source, which build.py reads.
"""

from __future__ import annotations

import base64
import datetime as dt
import io
import json
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).parent
SRC = ROOT / "source"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"
MOBILE_UA = ("Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 "
             "(KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1")

STORE = "https://aminbuildingsupplies.com.au"

# name, url, mobile?, wait (ms), width px to keep
SHOTS = [
    ("amin-home", f"{STORE}/", False, 1500, 1020),
    ("amin-tiles", f"{STORE}/collections/tiles", False, 6000, 1020),
    ("amin-product", f"{STORE}/products/riviere-freestanding-acrylic-bathtub", False, 6000, 1020),
    ("amin-mobile", f"{STORE}/", True, 1500, 440),
    ("launchnest", "https://launchnest.com.au/", False, 8000, 900),
    ("ravan", "https://ravan.studio/", False, 8000, 900),
]


def get(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=40).read().decode("utf-8", "replace")


def count_store() -> dict:
    products, page = [], 1
    while True:
        batch = json.loads(get(f"{STORE}/products.json?limit=250&page={page}"))["products"]
        if not batch:
            break
        products += batch
        page += 1
    collections = json.loads(get(f"{STORE}/collections.json?limit=250"))["collections"]
    sitemap_urls = 0
    for loc in re.findall(r"<loc>(.*?)</loc>", get(f"{STORE}/sitemap.xml")):
        sitemap_urls += get(loc.replace("&amp;", "&")).count("<url>")
    return {
        "products": len(products),
        "variants": sum(len(p["variants"]) for p in products),
        "collections": len([c for c in collections if c["handle"] != "frontpage"]),
        "product_types": len({p["product_type"] for p in products if p["product_type"]}),
        "brands": len({p["vendor"] for p in products if p["vendor"]}),
        "sitemap_urls": sitemap_urls,
        "counted_on": dt.date.today().isoformat(),
    }


def find_browser() -> str | None:
    for c in [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    ]:
        if Path(c).exists():
            return c
    return shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("msedge")


def _free_port() -> int:
    with socket.socket() as sk:
        sk.bind(("127.0.0.1", 0))
        return sk.getsockname()[1]


def capture(browser: str, url: str, mobile: bool, wait_ms: int) -> bytes | None:
    """Real device emulation over the DevTools protocol (a phone is a true 390px screen)."""
    import websocket  # websocket-client

    port = _free_port()
    with tempfile.TemporaryDirectory() as tmp:
        proc = subprocess.Popen([browser, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
                                 f"--remote-debugging-port={port}", "--remote-allow-origins=*", f"--user-data-dir={tmp}",
                                 "about:blank"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            ws_url = None
            for _ in range(60):
                try:
                    targets = json.loads(urllib.request.urlopen(f"http://127.0.0.1:{port}/json/list", timeout=2).read())
                    ws_url = next(t["webSocketDebuggerUrl"] for t in targets if t["type"] == "page")
                    break
                except Exception:
                    time.sleep(0.25)
            if not ws_url:
                return None
            ws = websocket.create_connection(ws_url, timeout=90, suppress_origin=True)
            ids = iter(range(1, 10_000))

            def call(method, **params):
                i = next(ids)
                ws.send(json.dumps({"id": i, "method": method, "params": params}))
                while True:
                    msg = json.loads(ws.recv())
                    if msg.get("id") == i:
                        return msg.get("result", {})

            w, h, scale = (390, 844, 2) if mobile else (1440, 900, 1)
            call("Emulation.setDeviceMetricsOverride", width=w, height=h, deviceScaleFactor=scale, mobile=mobile)
            if mobile:
                call("Emulation.setUserAgentOverride", userAgent=MOBILE_UA)
                call("Emulation.setTouchEmulationEnabled", enabled=True)
            call("Page.enable")
            call("Page.navigate", url=url)
            deadline = time.time() + 45
            while time.time() < deadline:
                if json.loads(ws.recv()).get("method") == "Page.loadEventFired":
                    break
            time.sleep(wait_ms / 1000)
            clip = {"x": 0, "y": 0, "width": w, "height": 1688 if mobile else h, "scale": 1}
            shot = call("Page.captureScreenshot", format="png", clip=clip, captureBeyondViewport=mobile)
            ws.close()
            return base64.b64decode(shot["data"])
        finally:
            proc.terminate()
            try:
                proc.wait(10)
            except subprocess.TimeoutExpired:
                proc.kill()


def screenshot(browser: str, name: str, url: str, mobile: bool, wait: int, keep_w: int) -> None:
    png = capture(browser, url, mobile, wait)
    if not png:
        print(f"  ! {name}: no screenshot")
        return
    im = Image.open(io.BytesIO(png)).convert("RGB")
    im = im.resize((keep_w, round(im.height * keep_w / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=80, optimize=True, progressive=True)
    (SRC / f"{name}.jpg").write_bytes(buf.getvalue())
    print(f"  {name}.jpg  {im.width}x{im.height}  {len(buf.getvalue()) // 1024} KB")


def main() -> None:
    SRC.mkdir(exist_ok=True)
    print("Counting the live store...")
    data = {"amin": count_store()}
    (SRC / "data.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(" ", data["amin"])
    if "--no-shots" in sys.argv:
        return
    browser = find_browser()
    if not browser:
        print("No Edge or Chrome found, keeping existing screenshots.")
        return
    print("Taking screenshots...")
    for job in SHOTS:
        screenshot(browser, *job)


if __name__ == "__main__":
    main()
