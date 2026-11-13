"""
build.py - generates the GitHub profile README and every SVG graphic in ./assets.

All profile content lives in the DATA section below. Edit it, then run:

    python build.py

and commit README.md plus the assets folder. No HTML to hand-edit.
"""

from __future__ import annotations

from html import escape
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).parent
ASSETS = ROOT / "assets"

# ════════════════════════════════════════════════════════════════════════════
# DATA - edit this section
# ════════════════════════════════════════════════════════════════════════════

PROFILE = {
    "name": "Zabih Bakhtiari",
    "handle": "zabihbakhtiari",
    "role": "Full-stack developer & SEO director",
    "tagline": [
        "Websites, web apps and search visibility",
        "for Australian trades and local businesses.",
    ],
    "badge": "Launch Nest Studio  ·  Ravan Studio",
    "chips": ["Full-stack", "Holistic SEO", "GEO & AEO", "Shopify"],
}

LINKS = {
    "launchnest": "https://launchnest.com.au/",
    "ravan": "https://ravan.studio",
    "linkedin": "https://www.linkedin.com/in/zabih-bakhtiari/",
    "orcid": "https://orcid.org/0009-0006-8017-2954",
    "repos": "https://github.com/zabihbakhtiari?tab=repositories",
    "amin": "https://aminbuildingsupplies.com.au/",
}

# Newest finished build - shown as the large featured card.
FEATURED = {
    "slug": "amin",
    "title": "Amin Building Supplies",
    "kind": "CLIENT BUILD  ·  SHOPIFY  ·  DANDENONG SOUTH, VIC",
    "url": LINKS["amin"],
    "display_url": "aminbuildingsupplies.com.au",
    "desc": [
        "Shopify store for a building-supplies retailer serving",
        "trades and homeowners: tiles, tapware, bathroomware,",
        "sinks and outdoor lighting, with enquiry-led pricing.",
    ],
    "pills": ["Shopify", "Shop by room", "Shop the look", "Trade enquiries"],
    "summary": (
        "Shopify store for a Dandenong South building-supplies retailer. "
        "A catalogue of tiles, tapware, bathroomware, kitchen and laundry sinks "
        "and outdoor lighting, with shop-by-room and shop-the-look pages, an "
        "\"ask for a price\" enquiry flow and a dedicated trade enquiries page."
    ),
}

# Project grid (2 per row).
PROJECTS = [
    {
        "slug": "ravan",
        "title": "Ravan Studio",
        "kind": "PRODUCT",
        "accent": "#8B5CF6",
        "url": LINKS["ravan"],
        "display_url": "ravan.studio",
        "desc": ["AI visibility scoring for Shopify stores: see how",
                 "ChatGPT, Perplexity and AI Overviews see a brand."],
        "pills": ["GEO", "AEO", "Shopify", "AI search"],
        "summary": "AI visibility scoring for Shopify stores, for GEO and AEO.",
    },
    {
        "slug": "launchnest",
        "title": "Launch Nest Studio",
        "kind": "AGENCY  ·  CO-FOUNDER",
        "accent": "#22D3EE",
        "url": LINKS["launchnest"],
        "display_url": "launchnest.com.au",
        "desc": ["Websites, local SEO and topical maps for",
                 "Australian trades and local businesses."],
        "pills": ["Custom WordPress", "Local SEO", "Schema"],
        "summary": "Websites, local SEO and topical maps for Australian trades.",
    },
    {
        "slug": "admin",
        "title": "admin-dashboard",
        "kind": "OPEN SOURCE",
        "accent": "#F59E0B",
        "url": "https://github.com/zabihbakhtiari/admin-dashboard",
        "display_url": "github.com/zabihbakhtiari/admin-dashboard",
        "desc": ["Admin dashboard UI for business platforms,",
                 "built in TypeScript."],
        "pills": ["TypeScript", "Dashboard UI"],
        "summary": "Admin dashboard UI for business platforms, in TypeScript.",
    },
    {
        "slug": "commerce",
        "title": "commerce",
        "kind": "OPEN SOURCE  ·  FORK",
        "accent": "#F472B6",
        "url": "https://github.com/zabihbakhtiari/commerce",
        "display_url": "github.com/zabihbakhtiari/commerce",
        "desc": ["Next.js storefront forked from vercel/commerce:",
                 "headless commerce on React Server Components."],
        "pills": ["Next.js", "TypeScript", "Headless"],
        "summary": "Next.js storefront, forked from vercel/commerce.",
    },
]

SERVICES = [
    ("WP", "Custom WordPress", ["Hand-coded themes, no page-", "builder bloat, easy to edit."]),
    ("SH", "Shopify stores", ["Catalogues, enquiry flows and", "integrations with your systems."]),
    ("FS", "Full-stack platforms", ["Finance, jobs and ops tools in", "React, TypeScript and Django."]),
    ("SEC", "Security cleanup", ["Malware removal, plugin audits,", "updates and lockdown."]),
    ("SEO", "Audits & roadmaps", ["Technical, content and local SEO", "with a month-by-month plan."]),
    ("{ }", "Topical maps & schema", ["Semantic content networks and", "JSON-LD for Google and AI."]),
]

PROCESS = [
    ("Brief", ["Map the business, services,", "suburbs and real searches."]),
    ("Build", ["Fast custom code, security", "and schema from day one."]),
    ("Launch", ["Redirects, Search Console,", "GBP and analytics checked."]),
    ("Rank", ["Topical content and reports", "for Google and AI search."]),
]

STACK = [
    ("FRONTEND", ["React", "TypeScript", "JavaScript", "Next.js", "Tailwind CSS", "shadcn/ui", "HTML5", "CSS3"]),
    ("BACKEND", ["Python", "Django", "Django REST Framework", "PHP", "REST APIs"]),
    ("DATA", ["PostgreSQL", "MySQL"]),
    ("CMS & COMMERCE", ["WordPress", "Shopify", "MODX"]),
    ("SHIP", ["Vercel", "Git", "GitHub"]),
    ("SEARCH", ["Schema & JSON-LD", "Topical maps", "GEO & AEO", "Search Console"]),
]

AUDIT = [
    ("Hacked or outdated plugins", "Malware cleanup, plugin audit, updates and hardening"),
    ("Slow page-builder pages", "Hand-coded theme, lean assets, Core Web Vitals pass"),
    ("One page trying to rank for every service", "A page per service and suburb, linked by a topical map"),
    ("No structured data", "JSON-LD for the business, services, products and FAQs"),
    ("Invisible in AI answers", "Entity-clear content built to be cited by ChatGPT, Perplexity and AI Overviews"),
    ("Broken redirects after a rebuild", "Full redirect map and Search Console checks before go-live"),
]

FAQ = [
    ("Who is Zabih Bakhtiari?",
     f'A full-stack developer and SEO director, and co-founder of <a href="{LINKS["launchnest"]}">Launch Nest Studio</a> '
     f'and <a href="{LINKS["ravan"]}">Ravan Studio</a>. He builds websites, web apps and search visibility for '
     "Australian trades and local businesses."),
    ("What have you shipped recently?",
     f'<a href="{LINKS["amin"]}">Amin Building Supplies</a>, a Shopify store for a building-supplies retailer in '
     "Dandenong South, VIC, covering tiles, tapware, bathroomware, sinks and outdoor lighting for trades and homeowners."),
    ("What does Launch Nest Studio do?",
     "Launch Nest Studio is a digital agency for Australian trades and local businesses. It builds fast, custom "
     "websites and runs SEO: audits, local SEO, topical maps, schema and ongoing content."),
    ("What is Ravan Studio?",
     "Ravan Studio scores how visible a Shopify store is in AI search, such as ChatGPT, Perplexity and Google's AI "
     f'Overviews, and shows what to fix. Visit <a href="{LINKS["ravan"]}">ravan.studio</a>.'),
    ("Do you use page builders?",
     "Where speed and control matter, no. I build custom WordPress themes by hand, which keeps sites fast, secure "
     "and easy to maintain."),
    ("What is holistic SEO and topical authority?",
     "Instead of chasing single keywords, you cover a topic completely: a topical map of every service, question "
     "and location, linked together with clear structure and schema. Search engines and AI answer engines then "
     "treat the site as the authority on that topic."),
    ("What is GEO and AEO?",
     "Generative engine optimisation and answer engine optimisation: making sure a business is understood, trusted "
     "and cited by AI tools like ChatGPT, Perplexity and AI Overviews, not just ranked in the blue links."),
    ("How do I work with you?",
     f'Start at <a href="{LINKS["launchnest"]}">launchnest.com.au</a> or message me on '
     f'<a href="{LINKS["linkedin"]}">LinkedIn</a>.'),
]

BUTTONS = [
    ("launchnest", "Launch Nest Studio", LINKS["launchnest"], "Launch Nest Studio website"),
    ("ravan", "Ravan Studio", LINKS["ravan"], "Ravan Studio website"),
    ("linkedin", "LinkedIn", LINKS["linkedin"], "Zabih Bakhtiari on LinkedIn"),
    ("orcid", "ORCID", LINKS["orcid"], "Zabih Bakhtiari on ORCID"),
    ("repos", "Repositories", LINKS["repos"], "Zabih Bakhtiari's GitHub repositories"),
]

# ════════════════════════════════════════════════════════════════════════════
# THEME
# ════════════════════════════════════════════════════════════════════════════

BG = "#0B0E14"
PANEL = "#111620"
BORDER = "#1F2633"
TEXT = "#E8ECF4"
MUTED = "#8B95A7"
DIM = "#5B6578"
VIOLET = "#8B5CF6"
CYAN = "#22D3EE"
LIME = "#A3E635"

SANS = "'Segoe UI','Inter',-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif"
MONO = "'JetBrains Mono','Cascadia Code','SFMono-Regular',Consolas,Menlo,monospace"

BASE_CSS = f"""
.s{{font-family:{SANS}}}
.m{{font-family:{MONO}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
"""

# ════════════════════════════════════════════════════════════════════════════
# SVG HELPERS
# ════════════════════════════════════════════════════════════════════════════


def tw(text: str, size: float, mono: bool = False, bold: bool = False) -> float:
    """Rough text width estimate (system fonts are not measurable here)."""
    factor = 0.6 if mono else (0.56 if bold else 0.53)
    return len(text) * size * factor


def svg(w: int, h: int, label: str, body: str, css: str = "", defs: str = "") -> str:
    lab = escape(label)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'role="img" aria-label="{lab}"><title>{lab}</title>'
        f"<defs><style>{BASE_CSS}{css}</style>{defs}</defs>{body}</svg>"
    )


def text(x, y, s, size=16, fill=TEXT, weight=400, mono=False, anchor="start", extra="") -> str:
    cls = "m" if mono else "s"
    return (
        f'<text x="{x}" y="{y}" class="{cls}" font-size="{size}" font-weight="{weight}" '
        f'fill="{fill}" text-anchor="{anchor}" {extra}>{escape(s)}</text>'
    )


def pill(x, y, label, size=13, h=28, fill="rgba(255,255,255,0.04)", stroke=BORDER, color=TEXT, mono=False):
    w = tw(label, size, mono) + 28
    out = (
        f'<rect x="{x}" y="{y}" width="{w:.1f}" height="{h}" rx="{h / 2}" fill="{fill}" stroke="{stroke}"/>'
        + text(x + w / 2, y + h / 2 + size * 0.36, label, size, color, 500, mono, "middle")
    )
    return out, w


def pill_row(x, y, labels, gap=8, **kw) -> str:
    out = []
    for lab in labels:
        p, w = pill(x, y, lab, **kw)
        out.append(p)
        x += w + gap
    return "".join(out)


def glow(id_, color, cx="85%", cy="0%", r="70%", op=0.35) -> str:
    return (
        f'<radialGradient id="{id_}" cx="{cx}" cy="{cy}" r="{r}">'
        f'<stop offset="0" stop-color="{color}" stop-opacity="{op}"/>'
        f'<stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient>'
    )


ACCENT_GRAD = (
    f'<linearGradient id="ag" x1="0" y1="0" x2="1" y2="0">'
    f'<stop offset="0" stop-color="{VIOLET}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>'
)

DOTS = (
    '<pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">'
    '<circle cx="1" cy="1" r="1" fill="#ffffff" fill-opacity="0.06"/></pattern>'
)


def frame(w, h, r=24) -> str:
    return (
        f'<rect width="{w}" height="{h}" rx="{r}" fill="{BG}"/>'
        f'<rect width="{w}" height="{h}" rx="{r}" fill="url(#dots)"/>'
    )


def border(w, h, r=24) -> str:
    return f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="{r}" fill="none" stroke="{BORDER}"/>'


# ════════════════════════════════════════════════════════════════════════════
# GRAPHICS
# ════════════════════════════════════════════════════════════════════════════

# Python syntax colours for the hero code window
K, C, S, A, P, N, D, F = "#C792EA", "#FFCB6B", "#C3E88D", "#82AAFF", "#89DDFF", "#637089", TEXT, "#F78C6C"

CODE = [
    [("from ", K), ("launchnest ", D), ("import ", K), ("Studio", C), (", ", P), ("ship", A)],
    [],
    [("class ", K), ("Zabih", C), ("(", P), ("FullStackDev", C), (", ", P), ("SEODirector", C), ("):", P)],
    [("    based_in ", D), ("= ", P), ('"Australia"', S)],
    [("    builds   ", D), ("= ", P), ("[", P), ('"websites"', S), (", ", P), ('"web apps"', S), (", ", P), ('"Shopify"', S), ("]", P)],
    [("    ranks_in ", D), ("= ", P), ("[", P), ('"Google"', S), (", ", P), ('"AI Overviews"', S), (", ", P), ('"ChatGPT"', S), ("]", P)],
    [("    stack    ", D), ("= ", P), ("[", P), ('"React"', S), (", ", P), ('"TypeScript"', S), (", ", P), ('"Django"', S), ("]", P)],
    [],
    [("    def ", K), ("latest_ship", A), ("(", P), ("self", F), (") -> ", P), ("str", C), (":", P)],
    [("        return ", K), ('"aminbuildingsupplies.com.au"', S)],
    [],
    [("ship", A), ("(", P), ("Zabih", C), ("()", P), (".", P), ("latest_ship", A), ("())  ", P), ("# live", N)],
]


def hero() -> str:
    W, H = 1200, 460
    b = [frame(W, H)]
    b.append(f'<rect width="{W}" height="{H}" rx="24" fill="url(#g1)"/>')
    b.append(f'<rect width="{W}" height="{H}" rx="24" fill="url(#g2)"/>')

    # left column
    bp, _ = pill(64, 72, "●  " + PROFILE["badge"], 13, 30, "rgba(163,230,53,0.08)", "rgba(163,230,53,0.35)", LIME)
    b.append(f'<g class="in">{bp}</g>')
    b.append(f'<g class="in" style="animation-delay:.08s">{text(62, 172, PROFILE["name"], 62, TEXT, 700)}</g>')
    b.append(f'<g class="in" style="animation-delay:.16s">{text(64, 222, PROFILE["role"], 28, "url(#ag)", 600)}</g>')
    for i, line in enumerate(PROFILE["tagline"]):
        b.append(f'<g class="in" style="animation-delay:{.24 + i * .04:.2f}s">{text(64, 272 + i * 28, line, 19, MUTED)}</g>')
    b.append(f'<g class="in" style="animation-delay:.34s">{pill_row(64, 346, PROFILE["chips"], 10, size=14, h=32)}</g>')

    # code window
    x0, y0, cw, ch = 624, 50, 520, 364
    b.append(f'<rect x="{x0}" y="{y0}" width="{cw}" height="{ch}" rx="16" fill="#0E131C" fill-opacity="0.92" stroke="{BORDER}"/>')
    b.append(f'<path d="M{x0} {y0 + 16}a16 16 0 0 1 16-16h{cw - 32}a16 16 0 0 1 16 16v24h-{cw}z" fill="#131925"/>')
    for i, c in enumerate(["#FF5F57", "#FEBC2E", "#28C840"]):
        b.append(f'<circle cx="{x0 + 22 + i * 18}" cy="{y0 + 20}" r="5.5" fill="{c}"/>')
    b.append(f'<rect x="{x0 + 84}" y="{y0 + 8}" width="92" height="32" rx="6" fill="#0E131C"/>')
    b.append(f'<rect x="{x0 + 84}" y="{y0 + 38}" width="92" height="2" fill="url(#ag)"/>')
    b.append(text(x0 + 130, y0 + 29, "zabih.py", 13, TEXT, 500, True, "middle"))
    b.append(text(x0 + cw - 18, y0 + 29, "Python 3.12", 12, DIM, 400, True, "end"))

    ly, lh = y0 + 78, 24
    for i, toks in enumerate(CODE):
        y = ly + i * lh
        num = text(x0 + 34, y, str(i + 1), 12.5, "#3B4456", 400, True, "end")
        spans = "".join(f'<tspan fill="{col}">{escape(t)}</tspan>' for t, col in toks)
        line = f'<text x="{x0 + 50}" y="{y}" class="m" font-size="14" xml:space="preserve">{spans}</text>'
        b.append(f'<g class="in" style="animation-delay:{.3 + i * .06:.2f}s">{num}{line}</g>')
    # blinking cursor after the last line
    last_w = sum(len(t) for t, _ in CODE[-1]) * 14 * 0.6
    b.append(f'<rect class="cur" x="{x0 + 52 + last_w:.0f}" y="{ly + (len(CODE) - 1) * lh - 14}" width="8" height="18" fill="{CYAN}"/>')
    b.append(border(W, H))

    css = ".cur{animation:bl 1.1s steps(1) infinite}@keyframes bl{50%{opacity:0}}"
    defs = DOTS + ACCENT_GRAD + glow("g1", VIOLET, "8%", "0%", "60%", .28) + glow("g2", CYAN, "95%", "100%", "55%", .18)
    return svg(W, H, f"{PROFILE['name']}, {PROFILE['role']}. Profile shown as a Python file, zabih.py.", "".join(b), css, defs)


def featured() -> str:
    W, H = 1200, 372
    f = FEATURED
    b = [frame(W, H), f'<rect width="{W}" height="{H}" rx="24" fill="url(#g1)"/>']

    bp, _ = pill(48, 44, "●  JUST SHIPPED", 12, 28, "rgba(163,230,53,0.1)", "rgba(163,230,53,0.4)", LIME, True)
    b.append(bp)
    b.append(text(48, 110, f["kind"], 12, MUTED, 500, True, extra='letter-spacing="1"'))
    b.append(text(46, 160, f["title"], 42, TEXT, 700))
    for i, line in enumerate(f["desc"]):
        b.append(text(48, 202 + i * 26, line, 17, MUTED))
    b.append(pill_row(48, 278, f["pills"], 8, size=13, h=28))
    b.append(text(48, 340, f["display_url"] + "  ↗", 14, CYAN, 500, True))

    # browser mock of the storefront
    bx, by, bw, bh = 640, 36, 520, 300
    sand, bronze, char, stone = "#E9E1D4", "#A9845A", "#24221F", "#F6F2EB"
    b.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="14" fill="{stone}" stroke="{BORDER}"/>')
    b.append(f'<path d="M{bx} {by + 14}a14 14 0 0 1 14-14h{bw - 28}a14 14 0 0 1 14 14v18h-{bw}z" fill="#1A1F2A"/>')
    for i, c in enumerate(["#FF5F57", "#FEBC2E", "#28C840"]):
        b.append(f'<circle cx="{bx + 18 + i * 15}" cy="{by + 16}" r="4.5" fill="{c}"/>')
    b.append(f'<rect x="{bx + 80}" y="{by + 7}" width="{bw - 160}" height="18" rx="9" fill="#0E131C"/>')
    b.append(text(bx + bw / 2, by + 20, "aminbuildingsupplies.com.au", 11, MUTED, 400, True, "middle"))

    # nav
    ny = by + 32
    b.append(f'<rect x="{bx}" y="{ny}" width="{bw}" height="34" fill="#FFFFFF"/>')
    b.append(text(bx + 18, ny + 22, "AMIN", 15, char, 800, extra='letter-spacing="2"'))
    for i, item in enumerate(["Tiles", "Bathroom", "Kitchen", "Lighting", "Trade"]):
        b.append(text(bx + 160 + i * 62, ny + 21, item, 11.5, "#5A554E", 500))
    b.append(f'<circle cx="{bx + bw - 22}" cy="{ny + 17}" r="7" fill="none" stroke="{char}" stroke-width="1.5"/>')

    # hero banner
    hy = ny + 34
    b.append(f'<rect x="{bx}" y="{hy}" width="{bw}" height="112" fill="url(#sand)"/>')
    for i in range(9):  # tile grid texture
        b.append(f'<line x1="{bx + 300 + i * 26}" y1="{hy}" x2="{bx + 300 + i * 26}" y2="{hy + 112}" stroke="#FFFFFF" stroke-opacity=".35"/>')
    for j in range(5):
        b.append(f'<line x1="{bx + 300}" y1="{hy + j * 26}" x2="{bx + bw}" y2="{hy + j * 26}" stroke="#FFFFFF" stroke-opacity=".35"/>')
    b.append(text(bx + 22, hy + 42, "Tiles, tapware &amp; bathroomware".replace("&amp;", "&"), 17, char, 700))
    b.append(text(bx + 22, hy + 62, "for trades and homeowners", 12, "#5A554E"))
    b.append(f'<rect x="{bx + 22}" y="{hy + 76}" width="104" height="24" rx="12" fill="{char}"/>')
    b.append(text(bx + 74, hy + 92, "Shop by room", 11, "#FFFFFF", 600, anchor="middle"))

    # category tiles
    cats = [("Tiles", "#D8CCB8"), ("Tapware", "#C9CFD4"), ("Bathroom", "#E2DAD0"), ("Sinks", "#CFC6BA"), ("Lighting", "#3A3631")]
    ty, tw_ = hy + 126, (bw - 36 - 4 * 10) / 5
    for i, (lab, col) in enumerate(cats):
        tx = bx + 18 + i * (tw_ + 10)
        b.append(f'<rect x="{tx:.1f}" y="{ty}" width="{tw_:.1f}" height="50" rx="8" fill="{col}"/>')
        if lab == "Lighting":
            b.append(f'<circle cx="{tx + tw_ / 2:.1f}" cy="{ty + 25}" r="9" fill="#F5C76B" fill-opacity=".9"/>')
        b.append(text(tx + tw_ / 2, ty + 66, lab, 11, char, 600, anchor="middle"))
    # enquiry strip
    ey = ty + 78
    b.append(f'<rect x="{bx + 18}" y="{ey}" width="{bw - 36}" height="0.8" fill="#D9D1C4"/>')
    b.append(text(bx + 18, ey + 18, "Price on enquiry", 11, "#5A554E"))
    b.append(f'<rect x="{bx + bw - 130}" y="{ey + 5}" width="112" height="20" rx="10" fill="none" stroke="{bronze}"/>')
    b.append(text(bx + bw - 74, ey + 19, "Ask for a price", 10.5, bronze, 600, anchor="middle"))

    b.append(border(W, H))
    defs = DOTS + glow("g1", LIME, "0%", "0%", "55%", .14) + (
        f'<linearGradient id="sand" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{sand}"/>'
        f'<stop offset="1" stop-color="#CDBB9F"/></linearGradient>'
    )
    return svg(W, H, f"Just shipped: {f['title']}. {f['summary']}", "".join(b), defs=defs)


def card(p: dict) -> str:
    W, H = 600, 252
    a = p["accent"]
    b = [frame(W, H, 20), f'<rect width="{W}" height="{H}" rx="20" fill="url(#g)"/>']
    b.append(f'<rect x="32" y="32" width="8" height="8" rx="2" fill="{a}"/>')
    b.append(text(50, 40, p["kind"], 11.5, a, 600, True, extra='letter-spacing="1.2"'))
    b.append(f'<circle cx="{W - 46}" cy="44" r="16" fill="rgba(255,255,255,0.04)" stroke="{BORDER}"/>')
    b.append(f'<path d="M{W - 51} 49l10-10m-7 0h7v7" fill="none" stroke="{TEXT}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>')
    b.append(text(31, 96, p["title"], 28, TEXT, 700))
    for i, line in enumerate(p["desc"]):
        b.append(text(32, 130 + i * 24, line, 15.5, MUTED))
    b.append(pill_row(32, 176, p["pills"], 8, size=12.5, h=26))
    b.append(text(32, 228, p["display_url"], 12.5, DIM, 400, True))
    b.append(border(W, H, 20))
    return svg(W, H, f"{p['title']}: {p['summary']}", "".join(b), defs=DOTS + glow("g", a, "100%", "0%", "75%", .22))


def section_icon(n: int) -> str:
    W = H = 32
    body = (
        f'<rect width="32" height="32" rx="9" fill="url(#ag)"/>'
        f'<rect x="1" y="1" width="30" height="30" rx="8" fill="{BG}" fill-opacity=".55"/>'
        + text(16, 20.5, f"{n:02d}", 12, "#FFFFFF", 700, True, "middle")
    )
    return svg(W, H, "", body, defs=ACCENT_GRAD.replace('x2="1" y2="0"', 'x2="1" y2="1"'))


def services() -> str:
    W, cols, tw0, th, gap = 1200, 3, 376, 150, 24
    H = 2 * th + gap
    b = []
    for i, (glyph, title, lines) in enumerate(SERVICES):
        x, y = (i % cols) * (tw0 + gap), (i // cols) * (th + gap)
        d = f' style="animation-delay:{i * .07:.2f}s"'
        g = [f'<rect x="{x + .5}" y="{y + .5}" width="{tw0 - 1}" height="{th - 1}" rx="18" fill="{PANEL}" stroke="{BORDER}"/>']
        g.append(f'<rect x="{x + 24}" y="{y + 24}" width="44" height="44" rx="12" fill="url(#ag)" fill-opacity=".9"/>')
        g.append(text(x + 46, y + 51, glyph, 12.5 if len(glyph) < 3 else 11, "#FFFFFF", 700, True, "middle"))
        g.append(text(x + 84, y + 52, title, 19, TEXT, 600))
        for j, line in enumerate(lines):
            g.append(text(x + 24, y + 100 + j * 23, line, 15, MUTED))
        b.append(f'<g class="in"{d}>{"".join(g)}</g>')
    alt = "Services: " + "; ".join(f"{t}: {' '.join(l)}" for _, t, l in SERVICES)
    return svg(W, H, alt, "".join(b), defs=ACCENT_GRAD)


def process() -> str:
    W, H = 1200, 230
    xs = [150 + i * 300 for i in range(4)]
    b = [frame(W, H), border(W, H)]
    b.append(f'<line x1="{xs[0]}" y1="66" x2="{xs[-1]}" y2="66" stroke="{BORDER}" stroke-width="2"/>')
    b.append(f'<line x1="{xs[0]}" y1="66" x2="{xs[-1]}" y2="66" stroke="url(#agl)" stroke-width="2" stroke-dasharray="6 8" class="flow"/>')
    b.append(f'<circle r="5" cy="66" fill="{CYAN}"><animate attributeName="cx" values="{xs[0]};{xs[-1]}" dur="4s" repeatCount="indefinite"/>'
             f'<animate attributeName="opacity" values="0;1;1;0" dur="4s" repeatCount="indefinite"/></circle>')
    for i, (title, lines) in enumerate(PROCESS):
        x = xs[i]
        g = [f'<circle cx="{x}" cy="66" r="24" fill="{BG}" stroke="url(#ag)" stroke-width="2"/>',
             text(x, 71, f"{i + 1:02d}", 14, TEXT, 700, True, "middle"),
             text(x, 132, title, 21, TEXT, 700, anchor="middle")]
        for j, line in enumerate(lines):
            g.append(text(x, 162 + j * 22, line, 14.5, MUTED, anchor="middle"))
        b.append(f'<g class="in" style="animation-delay:{i * .1:.1f}s">{"".join(g)}</g>')
    css = ".flow{animation:dash 1.2s linear infinite}@keyframes dash{to{stroke-dashoffset:-14}}"
    alt = "How a job runs: " + "; ".join(f"{t}: {' '.join(l)}" for t, l in PROCESS)
    line_grad = (f'<linearGradient id="agl" gradientUnits="userSpaceOnUse" x1="{xs[0]}" y1="0" x2="{xs[-1]}" y2="0">'
                 f'<stop offset="0" stop-color="{VIOLET}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>')
    return svg(W, H, alt, "".join(b), css, DOTS + ACCENT_GRAD + line_grad)


def stack() -> str:
    W, rh, top = 1200, 54, 36
    H = top * 2 + rh * len(STACK) - 14
    b = [frame(W, H), f'<rect width="{W}" height="{H}" rx="24" fill="url(#g1)"/>', border(W, H)]
    for i, (cat, items) in enumerate(STACK):
        y = top + i * rh
        g = [text(40, y + 19, cat, 12, MUTED, 600, True, extra='letter-spacing="1.2"'),
             pill_row(220, y, items, 8, size=13.5, h=30)]
        if i:
            g.insert(0, f'<line x1="40" y1="{y - 12}" x2="{W - 40}" y2="{y - 12}" stroke="{BORDER}" stroke-dasharray="2 6"/>')
        b.append(f'<g class="in" style="animation-delay:{i * .06:.2f}s">{"".join(g)}</g>')
    alt = "Tech stack: " + "; ".join(f"{c.title()}: {', '.join(it)}" for c, it in STACK)
    return svg(W, H, alt, "".join(b), defs=DOTS + glow("g1", VIOLET, "100%", "0%", "60%", .16))


def button(label: str) -> tuple[str, int]:
    h, size = 44, 15
    w = int(tw(label, size, bold=True) + 64)
    body = (
        f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="{h / 2 - 1}" fill="{PANEL}" stroke="url(#ag)" stroke-width="1.5"/>'
        + text(22, 27.5, label, size, TEXT, 600)
        + f'<path d="M{w - 30} 27l8-8m-6 0h6v6" fill="none" stroke="{CYAN}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>'
    )
    return svg(w, h, label, body, defs=ACCENT_GRAD), w


# ════════════════════════════════════════════════════════════════════════════
# README
# ════════════════════════════════════════════════════════════════════════════

SECTIONS = ["About", "Just Shipped", "Projects", "Services", "How a Job Runs", "Site Audit", "Tech Stack", "FAQ", "Connect"]


def heading(title: str) -> str:
    n = SECTIONS.index(title) + 1
    return f'## <img src="./assets/h-{n:02d}.svg" width="26" height="26" alt="" /> {title}'


def build_readme(button_widths: dict[str, int]) -> str:
    def btn(key, label, url, alt):
        return f'<a href="{url}"><img src="./assets/btn-{key}.svg" height="44" width="{button_widths[key]}" alt="{alt}" /></a>'

    rows = []
    for i in range(0, len(PROJECTS), 2):
        cells = []
        for p in PROJECTS[i:i + 2]:
            cells.append(
                f'    <td width="50%" valign="top">\n'
                f'      <a href="{p["url"]}"><img src="./assets/card-{p["slug"]}.svg" width="600" height="252" alt="{escape(p["title"])}: {escape(p["summary"])}" /></a>\n'
                f'      <p><b><a href="{p["url"]}">{escape(p["title"])}</a></b>: {escape(p["summary"])}</p>\n'
                f"    </td>"
            )
        rows.append("  <tr>\n" + "\n".join(cells) + "\n  </tr>")

    faq = "\n\n".join(
        f"<details>\n<summary><b>{q}</b></summary>\n<br />\n{a}\n</details>" for q, a in FAQ
    )
    audit = "\n".join(f"| {snag} | {fix} |" for snag, fix in AUDIT)
    stack_text = "; ".join(f"{c.title()}: {', '.join(it)}" for c, it in STACK)
    f = FEATURED
    lk = LINKS

    return dedent(f"""\
<!--
  {PROFILE['name']} ({PROFILE['handle']}): full-stack developer and SEO director.
  Co-founder of Launch Nest Studio, a digital agency building websites, web apps and SEO for Australian trades and local businesses.
  Ravan Studio: AI visibility scoring for Shopify stores. Holistic SEO, topical authority, schema, GEO and AEO.
  Latest build: {f['title']} ({f['url']}), a Shopify store for a building-supplies retailer in Dandenong South, VIC.
  Website: {lk['launchnest']}
  Ravan Studio: {lk['ravan']}
  LinkedIn: {lk['linkedin']}

  This file is generated by build.py. Edit the data there and run `python build.py`.
-->

<a href="{lk['launchnest']}"><img src="./assets/hero.svg" width="1200" height="460" alt="{PROFILE['name']}, full-stack developer and SEO director. Profile shown as a Python file, zabih.py." /></a>

<p align="center">
  <b>Hi I'm {PROFILE['name']}</b> Who builds websites, web apps and search visibility for Australian trades and local businesses.<br />
  Full-stack developer, SEO director and co-founder of <a href="{lk['launchnest']}">Launch Nest Studio</a> and <a href="{lk['ravan']}">Ravan Studio</a>.
</p>

<p align="center">
  {btn(*BUTTONS[0])}
  {btn(*BUTTONS[1])}
  {btn(*BUTTONS[2])}
</p>

{heading('About')}

I co-founded Launch Nest Studio, a digital agency that builds websites and search visibility for Australian trades and local businesses, and I lead SEO there. I write the code too: custom WordPress themes without page builders, Shopify stores, React and TypeScript front ends, Django APIs, and security cleanup when a site has been hacked.

My SEO follows the holistic, topical-authority approach: topical maps, semantic content networks and schema, built so a business shows up in Google and gets cited in AI answers from ChatGPT, Perplexity and Google's AI Overviews.

**Ravan Studio** is the product side: an AI visibility score that shows Shopify stores how AI search sees their brand.

> **Now:** just shipped <a href="{f['url']}">{f['title']}</a> · building Ravan Studio · taking on new trade and local-business builds through Launch Nest Studio.

{heading('Just Shipped')}

<a href="{f['url']}"><img src="./assets/card-{f['slug']}.svg" width="1200" height="372" alt="Just shipped: {escape(f['title'])}. {escape(f['summary'])}" /></a>

**<a href="{f['url']}">{f['title']}</a>**: {f['summary']}

- **Catalogue by category**: tiles, bathroom, kitchen and laundry, and outdoor lighting
- **Shop by room and shop the look**: inspiration pages that lead straight to products
- **Enquiry-led pricing**: "ask for a price" on products, built for how trade buyers actually purchase
- **Trade enquiries**: a dedicated page for trade accounts, alongside the Dandenong South trade counter

{heading('Projects')}

What I am building and where to find it.

<table>
{chr(10).join(rows)}
</table>

{heading('Services')}

<img src="./assets/services.svg" width="1200" height="324" alt="{escape(services_alt())}" />

{heading('How a Job Runs')}

<img src="./assets/process.svg" width="1200" height="230" alt="{escape('How a job runs: ' + '; '.join(f'{t}: {chr(32).join(l)}' for t, l in PROCESS))}" />

1. **Brief**: we map the business, its services, its suburbs and the questions customers actually search.
2. **Build**: a fast, custom site with clean code, proper security and structured data from day one.
3. **Launch**: migration, redirects, Search Console, Google Business Profile and analytics, checked before go-live.
4. **Rank**: topical content, internal links and ongoing reporting, so the site keeps climbing in Google and AI search.

{heading('Site Audit')}

The snag list: problems that turn up again and again on trade websites, and how each one gets fixed.

| Snag | Fix |
| --- | --- |
{audit}

**Want your site audited?** <a href="{lk['launchnest']}"><b>Launch Nest Studio</b></a> runs full SEO audits with a plain-English report and a month-by-month plan.

{heading('Tech Stack')}

<img src="./assets/stack.svg" width="1200" alt="{escape('Tech stack: ' + stack_text)}" />

{heading('FAQ')}

{faq}

{heading('Connect')}

<p align="center">
  {(chr(10) + '  ').join(btn(*b_) for b_ in BUTTONS)}
</p>
""")


def services_alt() -> str:
    return "Services: " + "; ".join(f"{t}: {' '.join(l)}" for _, t, l in SERVICES)


# ════════════════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════════════════


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    files: dict[str, str] = {
        "hero.svg": hero(),
        f"card-{FEATURED['slug']}.svg": featured(),
        "services.svg": services(),
        "process.svg": process(),
        "stack.svg": stack(),
    }
    for p in PROJECTS:
        files[f"card-{p['slug']}.svg"] = card(p)
    for i in range(len(SECTIONS)):
        files[f"h-{i + 1:02d}.svg"] = section_icon(i + 1)
    widths = {}
    for key, label, *_ in BUTTONS:
        files[f"btn-{key}.svg"], widths[key] = button(label)

    for name, content in files.items():
        (ASSETS / name).write_text(content, encoding="utf-8")
    (ROOT / "README.md").write_text(build_readme(widths), encoding="utf-8")
    print(f"Wrote README.md and {len(files)} SVGs to {ASSETS}")


if __name__ == "__main__":
    main()
