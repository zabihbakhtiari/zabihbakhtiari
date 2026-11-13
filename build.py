"""
build.py - builds the GitHub profile: README.md plus every panel in ./assets,
each in a light and a dark version.

    python crawl.py   # optional: refresh live counts and screenshots
    python build.py   # write README.md and assets/

Every word in the panels is outlined type (see glyphs.py). Screenshots are real
captures of the live sites, and every number is counted from the live store.
"""

from __future__ import annotations

import base64
import json
from html import escape
from pathlib import Path

from glyphs import Doc, Face, wrap

ROOT = Path(__file__).parent
ASSETS = ROOT / "assets"
SRC = ROOT / "source"
W = 1000

# ════════════════════════════════════════════════════════════════════════════
# CONTENT
# ════════════════════════════════════════════════════════════════════════════

LINKS = {
    "launchnest": "https://launchnest.com.au/",
    "ravan": "https://ravan.studio/",
    "amin": "https://aminbuildingsupplies.com.au/",
    "linkedin": "https://www.linkedin.com/in/zabih-bakhtiari/",
    "orcid": "https://orcid.org/0009-0006-8017-2954",
    "github": "https://github.com/zabihbakhtiari",
}

QUERY = "who builds websites that get found in google and ai answers?"

SAME_AS = ["launchnest.com.au", "ravan.studio", "linkedin.com/in/zabih-bakhtiari", "github.com/zabihbakhtiari"]

FACTS = [
    ("ROLE", "Full-stack developer", "and SEO director"),
    ("CO-FOUNDER", "Launch Nest Studio", "and Ravan Studio"),
    ("LATEST SHIP", "Amin Building Supplies", "Shopify, Dandenong South"),
]

AMIN_FEATURES = [
    ("Trade-first catalogue", "Tiles, tapware, bathroomware, sinks and lighting, sorted the way trades search."),
    ("Shop by room and look", "Inspiration pages that lead straight to the products in them."),
    ("Price on enquiry", "Call and email for a price on every product, built for how trade buyers buy."),
    ("Trade counter", "Pick-up details, opening hours and a trade quote request on each product page."),
]

STUDIOS = [
    ("launchnest", "Launch Nest Studio", "launchnest.com.au", LINKS["launchnest"],
     "Design, build and SEO studio in Adelaide, working with businesses across Australia. Co-founder, leading SEO."),
    ("ravan", "Ravan Studio", "ravan.studio", LINKS["ravan"],
     "Web development, design and SEO agency: web apps, WooCommerce stores, brand identities and entity-based SEO. Co-founder."),
]

METHOD_NOTES = [
    ("Entity first", "Name, address, services and sameAs links agree everywhere, so search engines know exactly who the business is."),
    ("Topical map", "Every service, suburb and question gets its own page, planned before a word is written."),
    ("Internal links", "Pages link up to their pillar and across to neighbours, so authority flows where it is needed."),
    ("Schema for AI", "JSON-LD on every template makes the site easy for Google to read and for AI answers to cite."),
]

PILLARS = [
    ("Services", "Service", ["Hot water", "Blocked drains"]),
    ("Suburbs", "Place", ["Norwood", "Unley"]),
    ("Proof", "Review", ["Reviews", "Projects"]),
    ("Questions", "FAQPage", ["Cost guides", "How-tos"]),
]

STEPS = [
    ("Brief", "Services, suburbs, real searches"),
    ("Build", "Custom code, security, schema"),
    ("Launch", "Redirects, Search Console, GBP"),
    ("Rank", "Topical content and reporting"),
]

SNAGS = [
    ("Hacked or outdated plugins", "Malware cleanup, plugin audit and hardening"),
    ("Slow page-builder pages", "Hand-coded theme with lean assets"),
    ("One page for every service", "A page per service and per suburb"),
    ("No structured data", "JSON-LD on every template"),
    ("Invisible in AI answers", "Entity-clear content that AI tools can cite"),
    ("Redirects lost in a rebuild", "Full redirect map, checked before go-live"),
]

STACK = [
    ("BUILD", ["React", "Next.js", "TypeScript", "JavaScript", "Tailwind CSS", "shadcn/ui"]),
    ("BACKEND", ["Python", "Django", "Django REST", "PHP", "REST APIs"]),
    ("DATA & SHIP", ["PostgreSQL", "MySQL", "Vercel", "Git", "GitHub"]),
    ("COMMERCE & CMS", ["Shopify", "WordPress", "WooCommerce", "MODX"]),
    ("SEARCH", ["Topical maps", "Schema & JSON-LD", "Entity SEO", "GEO & AEO", "Search Console"]),
]

FAQ = [
    ("Who is Zabih Bakhtiari?",
     f'A full-stack developer and SEO director, and co-founder of <a href="{LINKS["launchnest"]}">Launch Nest Studio</a> '
     f'and <a href="{LINKS["ravan"]}">Ravan Studio</a>. He builds websites, web apps and search visibility for '
     "Australian trades and local businesses."),
    ("What have you shipped recently?",
     f'<a href="{LINKS["amin"]}">Amin Building Supplies</a>, a Shopify store for a tiles, tapware and bathroomware '
     "trade counter in Dandenong South, Melbourne, with a trade-first catalogue, shop-by-room pages and price-on-enquiry buying."),
    ("What do Launch Nest Studio and Ravan Studio do?",
     "Launch Nest Studio is a design, build and SEO studio in Adelaide working with businesses across Australia. "
     "Ravan Studio is a web development, design and SEO agency covering web apps, WooCommerce stores, brand identities and entity-based SEO."),
    ("Do you use page builders?",
     "Where speed and control matter, no. I build custom WordPress themes and Shopify stores by hand, which keeps sites fast, secure and easy to maintain."),
    ("What is holistic SEO and topical authority?",
     "Instead of chasing single keywords, you cover a topic completely: a topical map of every service, question and location, "
     "linked together with clear structure and schema. Search engines and AI answer engines then treat the site as the authority on that topic."),
    ("What is GEO and AEO?",
     "Generative engine optimisation and answer engine optimisation: making sure a business is understood, trusted and cited by AI tools "
     "like ChatGPT, Perplexity and Google's AI Overviews, not just ranked in the blue links."),
    ("How do I work with you?",
     f'Start at <a href="{LINKS["launchnest"]}">launchnest.com.au</a> or <a href="{LINKS["ravan"]}">ravan.studio</a>, '
     f'or message me on <a href="{LINKS["linkedin"]}">LinkedIn</a>.'),
]

# ════════════════════════════════════════════════════════════════════════════
# THEME + TYPE
# ════════════════════════════════════════════════════════════════════════════

THEMES = {
    "dark": dict(bg="#0D0D0C", panel="#161615", panel2="#1E1E1C", line="#2A2927", line2="#403E3A",
                 text="#F4F2ED", muted="#9C9890", faint="#5F5C57", accent="#FF5F1F", ink="#FF7A3D", on="#FFFFFF"),
    "light": dict(bg="#FBFAF7", panel="#F2F0EB", panel2="#E9E6DF", line="#E3DFD6", line2="#CCC7BC",
                  text="#141412", muted="#5F5B53", faint="#A6A196", accent="#FF5F1F", ink="#D2440C", on="#FFFFFF"),
}

D = Face("d", "Archivo-VF.ttf", {"wght": 800, "wdth": 125})   # display
H = Face("h", "Archivo-VF.ttf", {"wght": 640, "wdth": 100})   # headings
B = Face("b", "Archivo-VF.ttf", {"wght": 400, "wdth": 100})   # body
N = Face("n", "Archivo-VF.ttf", {"wght": 700, "wdth": 112})   # numbers
M = Face("m", "JetBrainsMono-VF.ttf", {"wght": 500})          # labels

EASE = "cubic-bezier(.16,1,.3,1)"
CSS = f"""
.rv{{animation:rv 1s {EASE} both}}@keyframes rv{{from{{opacity:0;transform:translateY(16px)}}}}
.fd{{animation:fd 1.2s ease both}}@keyframes fd{{from{{opacity:0}}}}
.gr{{transform-box:fill-box;transform-origin:left center;animation:gr 1.4s {EASE} both}}@keyframes gr{{from{{transform:scaleX(0)}}}}
.dr{{stroke-dasharray:1;animation:dr 1.3s {EASE} both}}@keyframes dr{{from{{stroke-dashoffset:1}}to{{stroke-dashoffset:0}}}}
.pp{{transform-box:fill-box;transform-origin:center;animation:pp .7s {EASE} both}}@keyframes pp{{from{{opacity:0;transform:scale(.2)}}}}
.bk{{animation:bk 1.05s steps(1) infinite}}@keyframes bk{{50%{{opacity:0}}}}
.cv{{transform-box:fill-box;transform-origin:right center;transform:scaleX(0);animation:cv 2.4s steps(60) .5s both}}@keyframes cv{{from{{transform:scaleX(1)}}}}
.s1{{animation:s1 13.5s infinite}}@keyframes s1{{0%,30%{{opacity:1}}34%,97%{{opacity:0}}100%{{opacity:1}}}}
.s2{{animation:s2 13.5s infinite}}@keyframes s2{{0%,30%{{opacity:0}}34%,63%{{opacity:1}}67%,100%{{opacity:0}}}}
.s3{{animation:s3 13.5s infinite}}@keyframes s3{{0%,63%{{opacity:0}}67%,97%{{opacity:1}}100%{{opacity:0}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
"""


def delay(s: float) -> str:
    return f"animation-delay:{s:.2f}s"


_IMG: dict[str, str] = {}


def img_data(name: str) -> str:
    if name not in _IMG:
        _IMG[name] = base64.b64encode((SRC / f"{name}.jpg").read_bytes()).decode()
    return f"data:image/jpeg;base64,{_IMG[name]}"


class Panel:
    def __init__(self, mode: str):
        self.t = THEMES[mode]
        self.doc = Doc()
        self.defs: list[str] = []
        self.n = 0

    def uid(self, p: str) -> str:
        self.n += 1
        return f"{p}{self.n}"

    def text(self, face, s, x, y, size, fill=None, **kw):
        return self.doc.text(face, s, x, y, size, fill or self.t["text"], **kw)

    def runs(self, parts, x, y, size, **kw):
        """Several (face, text, fill) runs on one baseline."""
        out = []
        track = kw.get("track", 0)
        for face, s, fill in parts:
            out.append(self.doc.text(face, s, x, y, size, fill, **kw))
            x += face.width(s, size, track) + track * size
        return "".join(out)

    def para(self, face, s, x, y, size, max_w, lh, fill=None, **kw):
        lines = wrap(face, s, size, max_w)
        return "".join(self.text(face, ln, x, y + i * lh, size, fill or self.t["muted"], **kw) for i, ln in enumerate(lines)), len(lines)

    def label(self, s, x, y, fill=None, size=12, anchor="start"):
        return self.text(M, s, x, y, size, fill or self.t["muted"], track=0.12, anchor=anchor)

    def image(self, name, x, y, w, h, r=0, cls=""):
        cid = self.uid("c")
        self.defs.append(f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}"/></clipPath>')
        attrs = (f' class="{cls}"' if cls else "") + (' opacity="0"' if cls in ("s2", "s3") else "")
        return (f'<g clip-path="url(#{cid})"><g{attrs}><image href="{img_data(name)}" x="{x}" y="{y}" width="{w}" '
                f'height="{h}" preserveAspectRatio="xMidYMin slice"/></g></g>')

    def browser(self, x, y, w, url, slides, chrome=30):
        t = self.t
        ih = round(w * 638 / 1020) if slides[0].startswith("amin") else round(w * 562 / 900)
        out = [f'<rect x="{x}" y="{y}" width="{w}" height="{ih + chrome}" rx="10" fill="{t["panel2"]}" stroke="{t["line"]}"/>']
        for i in range(3):
            out.append(f'<circle cx="{x + 16 + i * 14}" cy="{y + chrome / 2}" r="4" fill="{t["line2"]}"/>')
        out.append(f'<rect x="{x + 70}" y="{y + 7}" width="{min(300, w - 140)}" height="{chrome - 14}" rx="{(chrome - 14) / 2}" fill="{t["bg"]}"/>')
        out.append(self.text(M, url, x + 84, y + chrome / 2 + 3.5, 10.5, t["muted"]))
        for i, name in enumerate(slides):
            out.append(self.image(name, x, y + chrome, w, ih, 0, "" if i == 0 else f"s{i + 1}"))
        out.append(f'<rect x="{x}" y="{y + chrome}" width="{w}" height="0.8" fill="{t["line"]}"/>')
        return "".join(out), ih + chrome

    def wrap_svg(self, h: int, label: str, body: str) -> str:
        t = self.t
        lab = escape(label)
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" role="img" aria-label="{lab}">'
            f"<title>{lab}</title><style>{CSS}</style><defs>{self.doc.defs()}{''.join(self.defs)}</defs>"
            f'<rect x="0.5" y="0.5" width="{W - 1}" height="{h - 1}" rx="18" fill="{t["bg"]}" stroke="{t["line"]}"/>'
            f"{body}</svg>"
        )


# ════════════════════════════════════════════════════════════════════════════
# PANELS
# ════════════════════════════════════════════════════════════════════════════


def hero(p: Panel):
    t = p.t
    b = []
    # search bar, typed in
    qx, qy = 100, 72
    qw = B.width(QUERY, 20)
    b.append(f'<rect x="40" y="36" width="920" height="60" rx="30" fill="{t["panel"]}" stroke="{t["line"]}"/>')
    b.append(f'<circle cx="72" cy="64" r="8.5" fill="none" stroke="{t["muted"]}" stroke-width="2"/>'
             f'<path d="M78.5 70.5l6 6" stroke="{t["muted"]}" stroke-width="2.2" stroke-linecap="round"/>')
    b.append(p.text(B, QUERY, qx, qy, 20, t["text"]))
    b.append(f'<rect class="cv" x="{qx - 2}" y="46" width="{qw + 6:.0f}" height="38" fill="{t["panel"]}"/>')
    b.append(f'<rect class="bk" x="{qx + qw + 4:.0f}" y="53" width="2" height="25" fill="{t["accent"]}"/>')
    b.append(f'<circle cx="930" cy="66" r="20" fill="{t["accent"]}"/>'
             f'<path d="M922 66h15m-6-6l6 6-6 6" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>')

    # answer label
    y = 150
    b.append(f'<g class="rv" style="{delay(2.9)}">'
             + p.runs([(M, "ANSWER", t["ink"]), (M, "  ·  PERSON  ·  1 RESULT", t["faint"])], 40, y, 12, track=0.12) + "</g>")

    # name
    size = 920 / D.width("BAKHTIARI", 1)
    cap = size * 0.72
    y1 = y + 30 + cap
    y2 = y1 + size * 0.9
    b.append(f'<g class="rv" style="{delay(3.0)}">{p.text(D, "ZABIH", 36, y1, size)}</g>')
    b.append(f'<g class="rv" style="{delay(3.12)}">{p.text(D, "BAKHTIARI", 36, y2, size)}</g>')

    # sameAs block beside ZABIH
    sx = 40 + D.width("ZABIH", size) + 56
    top = y1 - cap
    blk = [p.text(M, '"sameAs": [', sx, top + 11, 12.5, t["ink"])]
    lh = (cap - 11) / len(SAME_AS)
    for i, s in enumerate(SAME_AS):
        blk.append(p.text(M, f'"{s}"' + ("," if i < len(SAME_AS) - 1 else " ]"), sx + 18, top + 11 + lh * (i + 1), 12.5, t["muted"]))
    b.append(f'<rect class="gr" style="{delay(3.3)}" x="{sx - 20:.0f}" y="{top:.0f}" width="2" height="{cap:.0f}" fill="{t["accent"]}"/>')
    b.append(f'<g class="fd" style="{delay(3.4)}">{"".join(blk)}</g>')

    # statement
    ys = y2 + 66
    b.append(f'<g class="rv" style="{delay(3.4)}">' + p.runs(
        [(H, "I build the site, then get it found ", t["text"]), (H, "in Google and AI answers.", t["ink"])], 40, ys, 28) + "</g>")

    # facts
    yf = ys + 40
    b.append(f'<rect x="40" y="{yf:.0f}" width="920" height="1" fill="{t["line"]}"/>')
    for i, (lab, a, c) in enumerate(FACTS):
        x = 40 + i * 320
        b.append(f'<g class="rv" style="{delay(3.6 + i * 0.1)}">' + p.label(lab, x, yf + 36, t["faint"])
                 + p.text(H, a, x, yf + 66, 19) + p.text(B, c, x, yf + 90, 16, t["muted"]) + "</g>")
    h = int(yf + 124)
    return h, "Zabih Bakhtiari, full-stack developer and SEO director. Co-founder of Launch Nest Studio and Ravan Studio. Latest ship: Amin Building Supplies.", "".join(b)


def work_amin(p: Panel, data: dict):
    t = p.t
    head = "SELECTED WORK 01  ·  JUST SHIPPED"
    b = [p.runs([(M, "SELECTED WORK 01", t["muted"]), (M, "  ·  JUST SHIPPED", t["ink"])], 40, 58, 12, track=0.12)]
    b.append(f'<circle class="bk" cx="{40 + M.width(head, 12, 0.12) + 16:.0f}" cy="54" r="4" fill="{t["accent"]}"/>')
    b.append(p.text(H, "Amin Building Supplies", 37, 118, 54))
    b.append(p.text(B, "Shopify store for a tiles, tapware and bathroomware trade counter in Dandenong South, Melbourne.", 40, 156, 19, t["muted"]))

    # desktop slides
    bw = 690
    br, bh = p.browser(40, 192, bw, "aminbuildingsupplies.com.au", ["amin-home", "amin-tiles", "amin-product"])
    b.append(br)

    # phone, auto-scrolling the real mobile capture
    px, py = 40 + bw + 34, 192
    pw, ph = 960 - px, bh
    b.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="30" fill="{t["panel2"]}" stroke="{t["line"]}"/>')
    sx, sy, sw, sh = px + 9, py + 9, pw - 18, ph - 18
    full_h = sw * 1904 / 440
    travel = full_h - sh
    sid = p.uid("scr")
    p.defs.append(f"<style>.{sid}{{animation:{sid} 18s {EASE} infinite alternate}}"
                  f"@keyframes {sid}{{0%,16%{{transform:translateY(0)}}48%,60%{{transform:translateY(-{travel * 0.5:.0f}px)}}"
                  f"92%,100%{{transform:translateY(-{travel:.0f}px)}}}}</style>")
    cid = p.uid("c")
    p.defs.append(f'<clipPath id="{cid}"><rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="22"/></clipPath>')
    b.append(f'<g clip-path="url(#{cid})"><image class="{sid}" href="{img_data("amin-mobile")}" '
             f'x="{sx}" y="{sy}" width="{sw}" height="{full_h:.0f}"/></g>')

    # slide captions + progress
    yc = 192 + bh + 34
    for i, cap in enumerate(["Home", "Tiles collection", "Product page"]):
        b.append(f'<g class="s{i + 1}"{"" if i == 0 else " opacity=\"0\""}>{p.text(B, cap, 40, yc, 16, t["muted"])}</g>')
    for i in range(3):
        x = 40 + bw - 3 * 34 + 6 + i * 34
        b.append(f'<rect x="{x}" y="{yc - 6}" width="28" height="3" fill="{t["line2"]}"/>')
        b.append(f'<rect class="s{i + 1}" x="{x}" y="{yc - 6}" width="28" height="3" fill="{t["accent"]}"{"" if i == 0 else " opacity=\"0\""}/>')
    b.append(p.text(B, "Mobile", px, yc, 16, t["muted"]))

    # features
    yf = yc + 60
    cw = 920 / 4
    for i, (title, desc) in enumerate(AMIN_FEATURES):
        x = 40 + i * cw
        para, _ = p.para(B, desc, x, yf + 56, 15, cw - 28, 21)
        b.append(f'<g class="rv" style="{delay(0.2 + i * 0.1)}"><rect x="{x:.0f}" y="{yf}" width="28" height="3" fill="{t["accent"]}"/>'
                 + p.text(H, title, x, yf + 30, 18) + para + "</g>")

    # numbers
    yn = yf + 150
    b.append(f'<rect x="40" y="{yn}" width="920" height="1" fill="{t["line"]}"/>')
    nums = [(data["products"], "products"), (data["collections"], "collections"), (data["product_types"], "product types"),
            (data["brands"], "brands"), (data["sitemap_urls"], "URLs in the sitemap")]
    for i, (v, lab) in enumerate(nums):
        x = 40 + i * 184
        b.append(f'<g class="rv" style="{delay(0.5 + i * 0.08)}">' + p.text(N, str(v), x - 2, yn + 72, 52)
                 + p.text(B, lab, x, yn + 100, 15, t["muted"]) + "</g>")
    b.append(p.label(f"COUNTED FROM THE LIVE STORE'S CATALOGUE AND SITEMAP, {data['counted_on']}", 40, yn + 142, t["faint"], 11))
    h = int(yn + 174)
    alt = (f"Amin Building Supplies: real screens of the Shopify store on desktop and mobile. {data['products']} products, "
           f"{data['collections']} collections, {data['product_types']} product types, {data['brands']} brands and "
           f"{data['sitemap_urls']} sitemap URLs, counted from the live store.")
    return h, alt, "".join(b)


def studios(p: Panel):
    t = p.t
    b = [p.runs([(M, "SELECTED WORK 02", t["muted"]), (M, "  ·  STUDIOS I CO-FOUNDED", t["faint"])], 40, 58, 12, track=0.12)]
    cw = 440
    bottom = 0
    for i, (img, title, url_txt, url, desc) in enumerate(STUDIOS):
        x = 40 + i * (cw + 40)
        br, bh = p.browser(x, 86, cw, url_txt, [img], chrome=26)
        b.append(br)
        y = 86 + bh + 50
        para, n = p.para(B, desc, x, y + 34, 16, cw, 23)
        b.append(f'<g class="rv" style="{delay(0.2 + i * 0.15)}">' + p.text(H, title, x - 1, y, 28) + para
                 + p.text(M, url_txt + " ↗", x, y + 34 + n * 23 + 14, 13, t["ink"]) + "</g>")
        bottom = max(bottom, y + 34 + n * 23 + 14)
    return int(bottom + 40), "Launch Nest Studio and Ravan Studio, the two studios Zabih co-founded, with real screenshots of each site.", "".join(b)


def method(p: Panel):
    t = p.t
    b = [p.label("METHOD", 40, 58), p.text(H, "How a site gets found", 38, 104, 38),
         p.text(B, "Example: a local plumbing business, mapped before a page is built.", 40, 136, 17, t["muted"])]
    ox, top = 40, 180

    def box(x, y, w, h, title, sub, strong=False, d=0.0):
        fill = t["accent"] if strong else t["panel"]
        tc = t["on"] if strong else t["text"]
        sc = "#FFE2D3" if strong else t["muted"]
        return (f'<g class="pp" style="{delay(d)}"><rect x="{x:.1f}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" '
                f'stroke="{t["accent"] if strong else t["line"]}"/>' + p.text(H, title, x + w / 2, y + h / 2 - 1, 16, tc, anchor="middle")
                + p.text(M, sub, x + w / 2, y + h / 2 + 16, 10, sc, anchor="middle") + "</g>")

    def line(d_, dl):
        return f'<path class="dr" style="{delay(dl)}" pathLength="1" d="{d_}" fill="none" stroke="{t["line2"]}" stroke-width="1.5"/>'

    area = 540
    cx = ox + area / 2
    ent_w, ent_h = 260, 58
    pil_w, gap = 126, 12
    pil_x0 = ox + (area - (4 * pil_w + 3 * gap)) / 2
    y_p = top + 108
    y_l = y_p + 96
    y_o = y_l + 132
    lines, nodes = [], []
    nodes.append(box(cx - ent_w / 2, top, ent_w, ent_h, "The business", "Organization", True, 0.1))
    for i, (name, schema, leaves) in enumerate(PILLARS):
        px = pil_x0 + i * (pil_w + gap)
        pcx = px + pil_w / 2
        lines.append(line(f"M{cx:.1f} {top + ent_h}C{cx:.1f} {top + ent_h + 30} {pcx:.1f} {y_p - 30} {pcx:.1f} {y_p}", 0.3))
        nodes.append(box(px, y_p, pil_w, 52, name, schema, False, 0.6 + i * 0.08))
        lines.append(line(f"M{pcx:.1f} {y_p + 52}V{y_l + 38}", 0.9))
        for j, leaf in enumerate(leaves):
            ly = y_l + j * 38
            nodes.append(f'<g class="pp" style="{delay(1.1 + i * 0.06 + j * 0.05)}"><rect x="{px + 10:.1f}" y="{ly}" width="{pil_w - 20}" height="30" rx="15" '
                         f'fill="{t["bg"]}" stroke="{t["line2"]}"/>' + p.text(B, leaf, pcx, ly + 20, 13.5, t["text"], anchor="middle") + "</g>")
    out_w = 258
    outs = [("Google Search", "rankings · rich results"), ("AI answers", "ChatGPT · Perplexity · AI Overviews")]
    for k, (title, sub) in enumerate(outs):
        x = ox + k * (out_w + 24)
        ocx = x + out_w / 2
        for i in range(4):
            pcx = pil_x0 + i * (pil_w + gap) + pil_w / 2
            lines.append(line(f"M{pcx:.1f} {y_l + 68}C{pcx:.1f} {y_l + 104} {ocx:.1f} {y_o - 36} {ocx:.1f} {y_o}", 1.5))
        nodes.append(f'<g class="pp" style="{delay(2.0 + k * 0.1)}"><rect x="{x}" y="{y_o}" width="{out_w}" height="58" rx="8" fill="{t["panel2"]}" stroke="{t["line2"]}"/>'
                     + p.text(H, title, ocx, y_o + 27, 16, anchor="middle") + p.text(M, sub, ocx, y_o + 44, 10, t["muted"], anchor="middle") + "</g>")
    b += lines + nodes

    nx, ny = 630, top
    for i, (title, desc) in enumerate(METHOD_NOTES):
        para, n = p.para(B, desc, nx + 40, ny + 52, 15, 290, 21)
        b.append(f'<g class="rv" style="{delay(0.4 + i * 0.15)}"><rect x="{nx}" y="{ny + 10}" width="26" height="26" rx="4" fill="{t["accent"]}"/>'
                 + p.text(M, str(i + 1), nx + 13, ny + 28, 13, t["on"], anchor="middle")
                 + p.text(H, title, nx + 40, ny + 30, 19) + para + "</g>")
        ny += 52 + n * 21 + 14
    h = int(max(y_o + 58, ny) + 44)
    alt = ("How a site gets found: the business as an entity, pillars for services, suburbs, proof and questions, "
           "each with its own pages and schema, all feeding Google Search and AI answers.")
    return h, alt, "".join(b)


def snags(p: Panel):
    t = p.t
    b = [p.label("PROCESS", 40, 58), p.text(H, "From brief to ranking", 38, 104, 38)]
    y = 160
    xs = [48 + i * 230 for i in range(4)]
    b.append(f'<rect x="48" y="{y - 1}" width="904" height="2" fill="{t["line2"]}"/>')
    b.append(f'<rect class="gr" style="{delay(0.2)};animation-duration:2.6s" x="48" y="{y - 1}" width="904" height="2" fill="{t["accent"]}"/>')
    for i, (title, sub) in enumerate(STEPS):
        x = xs[i]
        anchor, tx = "start", x - 8
        b.append(f'<circle class="pp" style="{delay(0.3 + i * 0.6)}" cx="{x:.1f}" cy="{y}" r="8" fill="{t["accent"]}" stroke="{t["bg"]}" stroke-width="4"/>')
        b.append(f'<g class="rv" style="{delay(0.4 + i * 0.6)}">' + p.text(H, title, tx, y + 42, 19, anchor=anchor)
                 + p.text(B, sub, tx, y + 66, 15, t["muted"], anchor=anchor) + "</g>")

    y = 300
    b.append(p.runs([(M, "THE SNAG LIST", t["ink"]), (M, "  ·  FOUND ON TRADE SITES, FIXED BEFORE LAUNCH", t["faint"])], 40, y, 12, track=0.12))
    y += 22
    for i, (snag, fix) in enumerate(SNAGS):
        ry = y + i * 54
        d0 = 2.8 + i * 0.35
        sw = B.width(snag, 17)
        b.append(f'<rect x="40" y="{ry}" width="920" height="1" fill="{t["line"]}"/>')
        b.append(f'<rect x="40" y="{ry + 16}" width="22" height="22" rx="4" fill="none" stroke="{t["line2"]}"/>')
        b.append(f'<g class="pp" style="{delay(d0)}"><rect x="40" y="{ry + 16}" width="22" height="22" rx="4" fill="{t["accent"]}"/>'
                 f'<path d="M45.5 {ry + 27.5}l4 4 7.5-8" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></g>')
        b.append(p.text(B, snag, 80, ry + 33, 17, t["muted"]))
        b.append(f'<rect class="gr" style="{delay(d0 + 0.1)};animation-duration:.7s" x="78" y="{ry + 27}" width="{sw + 4:.0f}" height="1.6" fill="{t["muted"]}"/>')
        b.append(f'<g class="rv" style="{delay(d0 + 0.25)}">' + p.text(M, "→", 470, ry + 33, 15, t["ink"])
                 + p.text(H, fix, 500, ry + 33, 17) + "</g>")
    b.append(f'<rect x="40" y="{y + len(SNAGS) * 54}" width="920" height="1" fill="{t["line"]}"/>')
    h = int(y + len(SNAGS) * 54 + 44)
    alt = "From brief to ranking: brief, build, launch, rank. The snag list: " + "; ".join(f"{s}, fixed with {f.lower()}" for s, f in SNAGS)
    return h, alt, "".join(b)


def stack(p: Panel):
    t = p.t
    b = [p.label("STACK", 40, 58)]
    cw = 920 / len(STACK)
    rows = max(len(i) for _, i in STACK)
    for c, (cat, items) in enumerate(STACK):
        x = 40 + c * cw
        g = [p.text(M, cat, x, 100, 11.5, t["ink"], track=0.1), f'<rect x="{x:.0f}" y="114" width="{cw - 20:.0f}" height="1" fill="{t["line2"]}"/>']
        for r, it in enumerate(items):
            g.append(p.text(B, it, x, 148 + r * 32, 17))
        b.append(f'<g class="rv" style="{delay(c * 0.08)}">{"".join(g)}</g>')
    h = int(148 + (rows - 1) * 32 + 40)
    alt = "Stack: " + "; ".join(f"{cat.title()}: {', '.join(i)}" for cat, i in STACK)
    return h, alt, "".join(b)


def contact(p: Panel):
    t = p.t
    size = 56
    b = [p.label("NEXT", 40, 58)]
    b.append(f'<g class="rv">{p.text(D, "NEED A SITE", 38, 128, size)}</g>')
    b.append(f'<g class="rv" style="{delay(0.1)}">' + p.runs([(D, "THAT GETS ", t["text"]), (D, "FOUND?", t["accent"])], 38, 194, size) + "</g>")
    links = ["launchnest.com.au", "ravan.studio", "linkedin.com/in/zabih-bakhtiari"]
    b.append(f'<rect x="40" y="226" width="920" height="1" fill="{t["line"]}"/>')
    x = 40
    for i, s in enumerate(links):
        b.append(f'<g class="rv" style="{delay(0.3 + i * 0.1)}">' + p.text(M, s + " ↗", x, 266, 14, t["ink"] if i == 0 else t["text"]) + "</g>")
        x += M.width(s + " ↗", 14) + 48
    return 300, "Need a site that gets found? launchnest.com.au, ravan.studio, LinkedIn.", "".join(b)


# ════════════════════════════════════════════════════════════════════════════
# README
# ════════════════════════════════════════════════════════════════════════════


def pic(name: str, alt: str, link: str | None = None) -> str:
    inner = (f'<picture>\n  <source media="(prefers-color-scheme: dark)" srcset="./assets/{name}-dark.svg" />\n'
             f'  <source media="(prefers-color-scheme: light)" srcset="./assets/{name}-light.svg" />\n'
             f'  <img src="./assets/{name}-light.svg" width="100%" alt="{escape(alt)}" />\n</picture>')
    return f'<a href="{link}">\n{inner}\n</a>' if link else inner


def readme(alts: dict[str, str]) -> str:
    L = LINKS
    faq = "\n\n".join(f"<details>\n<summary><b>{q}</b></summary>\n<br />\n{a}\n</details>" for q, a in FAQ)
    return f"""<!--
  Zabih Bakhtiari (zabihbakhtiari): full-stack developer and SEO director.
  Co-founder of Launch Nest Studio (design, build and SEO studio, Adelaide) and Ravan Studio (web development, design and SEO agency).
  Latest build: Amin Building Supplies ({L['amin']}), a Shopify store in Dandenong South, Melbourne.
  Generated by build.py. Edit the content there and run `python build.py`.
-->

{pic("hero", alts["hero"])}

<p align="center">
  <b>Hi I'm Zabih Bakhtiari</b> Who builds websites, web apps and search visibility for Australian trades and local businesses.<br />
  Full-stack developer, SEO director and co-founder of <a href="{L['launchnest']}">Launch Nest Studio</a> and <a href="{L['ravan']}">Ravan Studio</a>.
</p>

## Selected work

{pic("work-amin", alts["work-amin"], L["amin"])}

<br />

{pic("work-studios", alts["work-studios"], L["launchnest"])}

## How a site gets found

I write the code and I run the SEO, so the search plan is built into the site from the first commit, not bolted on after launch.

{pic("method", alts["method"])}

## Process

Every job runs the same way, and every launch clears the snag list first.

{pic("process", alts["process"])}

## Stack

{pic("stack", alts["stack"])}

## FAQ

{faq}

<br />

{pic("contact", alts["contact"], L["launchnest"])}

<p align="center">
  <a href="{L['launchnest']}">Launch Nest Studio</a> ·
  <a href="{L['ravan']}">Ravan Studio</a> ·
  <a href="{L['linkedin']}">LinkedIn</a> ·
  <a href="{L['orcid']}">ORCID</a> ·
  <a href="{L['github']}?tab=repositories">Repositories</a>
</p>
"""


# ════════════════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════════════════


def main() -> None:
    data = json.loads((SRC / "data.json").read_text(encoding="utf-8"))["amin"]
    builders = {
        "hero": hero,
        "work-amin": lambda p: work_amin(p, data),
        "work-studios": studios,
        "method": method,
        "process": snags,
        "stack": stack,
        "contact": contact,
    }
    ASSETS.mkdir(exist_ok=True)
    alts = {}
    for name, fn in builders.items():
        for mode in ("dark", "light"):
            p = Panel(mode)
            h, alt, body = fn(p)
            svg = p.wrap_svg(h, alt, body)
            (ASSETS / f"{name}-{mode}.svg").write_text(svg, encoding="utf-8")
            alts[name] = alt
        print(f"  {name:13} {h:4}px  {len(svg) // 1024:4} KB")
    (ROOT / "README.md").write_text(readme(alts), encoding="utf-8")
    print("Wrote README.md")


if __name__ == "__main__":
    main()
