"""
glyphs.py - turns text into outlined SVG glyphs.

GitHub shows README images without web fonts, so every word in the graphics is
drawn as vector outlines: shaped with HarfBuzz (kerning, ligatures) and traced
from the fonts in ./fonts. Fonts are downloaded on first run (SIL OFL).
"""

from __future__ import annotations

import io
import urllib.request
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

FONT_DIR = Path(__file__).parent / "fonts"
SOURCES = {
    "Archivo-VF.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/archivo/Archivo%5Bwdth,wght%5D.ttf",
    "JetBrainsMono-VF.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/jetbrainsmono/JetBrainsMono%5Bwght%5D.ttf",
}


def _ensure_fonts() -> None:
    FONT_DIR.mkdir(exist_ok=True)
    for name, url in SOURCES.items():
        path = FONT_DIR / name
        if not path.exists():
            print(f"Downloading {name}...")
            path.write_bytes(urllib.request.urlopen(url, timeout=60).read())


class Face:
    def __init__(self, key: str, file: str, axes: dict[str, float]):
        _ensure_fonts()
        vf = TTFont(FONT_DIR / file)
        # Variable fonts draw letters from overlapping contours. Merge them, or
        # GitHub's downscaling leaves faint seams that make the type look scratchy.
        static = instancer.instantiateVariableFont(vf, axes, overlap=instancer.OverlapMode.REMOVE)
        buf = io.BytesIO()
        static.save(buf)
        data = buf.getvalue()
        self.key = key
        self.tt = TTFont(io.BytesIO(data))
        self.upm = self.tt["head"].unitsPerEm
        self.order = self.tt.getGlyphOrder()
        self.gs = self.tt.getGlyphSet()
        self.hb = hb.Font(hb.Face(hb.Blob(data)))
        self._paths: dict[int, str] = {}

    def shape(self, s: str) -> list[tuple[int, int, int]]:
        buf = hb.Buffer()
        buf.add_str(s)
        buf.guess_segment_properties()
        hb.shape(self.hb, buf, {"kern": True, "liga": True})
        return [(i.codepoint, p.x_advance, p.x_offset) for i, p in zip(buf.glyph_infos, buf.glyph_positions)]

    def width(self, s: str, size: float, track: float = 0) -> float:
        g = self.shape(s)
        return (sum(a for _, a, _ in g) / self.upm + track * max(len(g) - 1, 0)) * size

    def path(self, gid: int) -> str:
        if gid not in self._paths:
            pen = SVGPathPen(self.gs, ntos=lambda v: f"{v:.0f}" if v == int(v) else f"{v:.1f}")
            self.gs[self.order[gid]].draw(pen)
            self._paths[gid] = pen.getCommands()
        return self._paths[gid]


class Doc:
    """Collects the glyphs one SVG uses so each is defined once."""

    def __init__(self):
        self.used: dict[str, str] = {}

    def text(self, face: Face, s: str, x: float, y: float, size: float, fill: str,
             anchor: str = "start", track: float = 0, cls: str = "", style: str = "", opacity: float | None = None) -> str:
        if not s:
            return ""
        w = face.width(s, size, track)
        if anchor == "middle":
            x -= w / 2
        elif anchor == "end":
            x -= w
        k = size / face.upm
        out, pen_x = [], 0.0
        for gid, adv, off in face.shape(s):
            d = face.path(gid)
            if d:
                gid_key = f"{face.key}{gid}"
                self.used[gid_key] = d
                gx = x + (pen_x + off) * k
                out.append(f'<use href="#{gid_key}" transform="translate({gx:.2f} {y:.2f}) scale({k:.5f} {-k:.5f})"/>')
            pen_x += adv + track * face.upm
        attrs = f' fill="{fill}"'
        if cls:
            attrs += f' class="{cls}"'
        if style:
            attrs += f' style="{style}"'
        if opacity is not None:
            attrs += f' opacity="{opacity}"'
        return f"<g{attrs}>{''.join(out)}</g>"

    def defs(self) -> str:
        return "".join(f'<path id="{k}" d="{d}"/>' for k, d in self.used.items())


def wrap(face: Face, s: str, size: float, max_w: float) -> list[str]:
    lines, cur = [], ""
    for word in s.split():
        trial = f"{cur} {word}".strip()
        if cur and face.width(trial, size) > max_w:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines
