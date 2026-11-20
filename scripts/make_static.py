"""Draw assets/header.svg and assets/stack.svg.

Edit STACK below and run:  python3 scripts/make_static.py
"""

import random
from pathlib import Path

from pixelfont import (BALL, BG, COURT, DIM, INK, MONO, MUTED, PANEL, TRAM,
                       esc, grid_art, pixel_text)

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

# --------------------------------------------------------------------------- header

W, H = 1200, 400
TRACK_Y = 352


def skyline(rng):
    """Blocky Melbourne skyline: low on the left (under the text), tall on the right."""
    u = 6
    shapes, lit = [], []
    x = 0
    while x < W:
        bw = rng.choice([4, 5, 6, 7, 8]) * u
        if x < 600:
            bh = rng.randint(5, 11) * u
        elif x < 860:
            bh = rng.randint(8, 15) * u
        else:
            bh = rng.randint(12, 26) * u
        top = TRACK_Y - bh
        shapes.append(f"M{x} {TRACK_Y}V{top}h{bw}V{TRACK_Y}z")
        for wy in range(top + u, TRACK_Y - u, u * 2):
            for wx in range(x + u, x + bw - u + 1, u * 2):
                if rng.random() < 0.22:
                    lit.append(f"M{wx} {wy}h3v4h-3z")
        x += bw + rng.choice([0, 0, u])

    # Eureka Tower: tall, narrow, gold crown.
    ex, etop = 930, 150
    tower = f"M{ex} {TRACK_Y}V{etop}h48V{TRACK_Y}z"
    crown = f"M{ex} {etop}h48v30h-48z"
    for wy in range(etop + 40, TRACK_Y - 12, 12):
        for wx in range(ex + 6, ex + 42, 12):
            if rng.random() < 0.35:
                lit.append(f"M{wx} {wy}h3v4h-3z")

    # Arts Centre spire: a lattice cone on a low base, with a mast.
    sx, base_top = 1060, 286
    spire = [f"M{sx - 30} {TRACK_Y}V{base_top}h60V{TRACK_Y}z"]
    for i, half in enumerate(range(24, 0, -3)):
        y = base_top - (i + 1) * 12
        spire.append(f"M{sx - half} {y}h{half * 2}v12h-{half * 2}z")
    mast_top = base_top - 9 * 12 - 40
    spire.append(f"M{sx - 1} {mast_top}h3v{40 + 12}h-3z")

    return "".join(shapes), "".join(lit), tower, crown, "".join(spire)


TRAM_ROWS = [
    "................pppppppp................",
    ".................p....p.................",
    "..................pppp..................",
    ".rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr.",
    "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwf",
    "wwyyyywyyyywyyyywddwyyyywyyyywyyyywfffff",
    "wwyyyywyyyywyyyywddwyyyywyyyywyyyywfffff",
    "wwyyyywyyyywyyyywddwyyyywyyyywyyyywwwwww",
    "ggggggggggggggggggddgggggggggggggggggggh",
    "GGGGGGGGGGGGGGGGGGddGGGGGGGGGGGGGGGGGGGG",
    "gggggggggggggggggggggggggggggggggggggggg",
    "....kkkkkk....................kkkkkk....",
]
TRAM_PALETTE = {
    "p": "#8A94B0", "r": "#C9D1E6", "w": "#E8EEF9", "y": "#F6D57A",
    "d": "#2B3A63", "f": "#9FC3FF", "g": TRAM, "G": "#5E9A16",
    "h": "#FFF3B0", "k": "#05070F",
}

BALL_ROWS = [
    "..####..",
    ".#s####.",
    "#s#####s",
    "#s####s#",
    "#s####s#",
    "#s#####s",
    ".#s####.",
    "..####..",
]


def header():
    rng = random.Random(96)  # route 96, the tram that never comes when you need it
    stars, twinkle = [], []
    for i in range(70):
        sx, sy = rng.randint(10, W - 10), rng.randint(12, 250)
        size = rng.choice([2, 2, 3])
        (twinkle if i % 6 == 0 else stars).append(f"M{sx} {sy}h{size}v{size}h-{size}z")

    shapes, lit, tower, crown, spire = skyline(rng)

    title_d, title_w = pixel_text("SHAWN LEE", 60, 74, 10)
    shadow_d, _ = pixel_text("SHAWN LEE", 66, 80, 10)

    ball_x = 60 + title_w + 34
    ball_ground = 74 + 70 - 24
    ball = grid_art(BALL_ROWS, {"#": BALL, "s": "#F7FFD6"}, 0, 0, 3)
    ball_svg = "".join(f'<path fill="{c}" d="{d}"/>' for c, d in ball.items())

    tram = grid_art(TRAM_ROWS, TRAM_PALETTE, 0, 0, 4)
    tram_svg = "".join(f'<path fill="{c}" d="{d}"/>' for c, d in tram.items())
    tram_h = len(TRAM_ROWS) * 4
    tram_w = len(TRAM_ROWS[0]) * 4

    sleepers = "".join(f"M{x} {TRACK_Y + 4}h8v4h-8z" for x in range(0, W, 22))

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<title>SHAWN LEE in pixel letters, with a bouncing tennis ball, over a night Melbourne skyline with a tram going past. Games, web apps and AI tools you can open in a browser.</title>
<style>
.tw{{animation:tw 3.2s steps(2,end) infinite}}
@keyframes tw{{50%{{opacity:.15}}}}
.ball{{animation:bounce 1.15s infinite}}
@keyframes bounce{{
 0%,100%{{transform:translateY(-64px);animation-timing-function:cubic-bezier(.5,0,1,.5)}}
 50%{{transform:translateY(0);animation-timing-function:cubic-bezier(0,.5,.5,1)}}
}}
.shadow{{transform-box:fill-box;transform-origin:center;animation:shadow 1.15s infinite}}
@keyframes shadow{{
 0%,100%{{transform:scaleX(.45);opacity:.25;animation-timing-function:cubic-bezier(.5,0,1,.5)}}
 50%{{transform:scaleX(1);opacity:.7;animation-timing-function:cubic-bezier(0,.5,.5,1)}}
}}
.tram{{animation:drive 17s linear infinite}}
@keyframes drive{{from{{transform:translateX(-{tram_w + 120}px)}}to{{transform:translateX({W + 40}px)}}}}
@media (prefers-reduced-motion: reduce){{.tw,.ball,.shadow,.tram{{animation:none}}}}
</style>
<defs>
<clipPath id="frame"><rect width="{W}" height="{H}" rx="18"/></clipPath>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="{BG}"/><stop offset="1" stop-color="#131B36"/>
</linearGradient>
<linearGradient id="beam" x1="0" y1="0" x2="1" y2="0">
<stop offset="0" stop-color="#FFF3B0" stop-opacity=".35"/><stop offset="1" stop-color="#FFF3B0" stop-opacity="0"/>
</linearGradient>
</defs>
<g clip-path="url(#frame)">
<rect width="{W}" height="{H}" fill="url(#sky)"/>
<path fill="#2A3557" d="{''.join(stars)}"/>
<path class="tw" fill="#C9D6FF" d="{''.join(twinkle)}"/>


<path fill="{COURT}" d="{shadow_d}"/>
<path fill="#F4F7FF" d="{title_d}"/>

<ellipse class="shadow" cx="{ball_x + 12}" cy="{ball_ground + 26}" rx="14" ry="3" fill="#000"/>
<g transform="translate({ball_x} {ball_ground})"><g class="ball">{ball_svg}</g></g>

<text x="60" y="206" font-family="{MONO}" font-size="25" fill="#DCE4FF">Games, web apps and AI tools you can open in a browser.</text>
<text x="60" y="242" font-family="{MONO}" font-size="19" fill="{MUTED}">University of Melbourne</text>

<path fill="#141C33" d="{shapes}"/>
<path fill="#151F3B" d="{tower}"/>
<path fill="#E3B341" d="{crown}"/>
<path fill="#1A2443" d="{spire}"/>
<path fill="#F2C94C" fill-opacity=".8" d="{lit}"/>

<rect y="{TRACK_Y}" width="{W}" height="{H - TRACK_Y}" fill="#080C18"/>
<path fill="#1C2440" d="{sleepers}"/>
<rect y="{TRACK_Y}" width="{W}" height="3" fill="#3A4670"/>

<g class="tram"><g transform="translate(0 {TRACK_Y - tram_h})">
<path fill="url(#beam)" d="M{tram_w} {tram_h - 16}l120 -14v34z"/>
{tram_svg}
</g></g>

<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="18" fill="none" stroke="#1C2647" stroke-width="2"/>
</g>
</svg>
"""
    return svg


# --------------------------------------------------------------------------- stack

STACK = [
    ("LANGUAGES", [("TypeScript", "#3178C6"), ("JavaScript", "#F7DF1E"), ("Python", "#4B8BBE"),
                   ("Java", "#E76F00"), ("C", "#A8B9CC"), ("GDScript", "#478CBF"), ("SQL", "#6F8FEA")]),
    ("FRONTEND", [("React", "#61DAFB"), ("Next.js", "#FFFFFF"), ("Vite", "#8C93FF"),
                  ("Tailwind CSS", "#38BDF8"), ("Three.js", "#C9D1E6"), ("PWA", "#A78BFA")]),
    ("BACKEND & DATA", [("Supabase", "#3ECF8E"), ("PostgreSQL", "#6F8FEA"), ("FastAPI", "#05998B"),
                        ("SQLAlchemy", "#E8553E"), ("Pydantic", "#E92063"), ("Node.js", "#5FA04E")]),
    ("GAMES", [("Godot 4", "#478CBF"), ("Canvas / WebGL", "#E34F26"), ("Three.js", "#C9D1E6"),
               ("JavaFX", "#ED8B00")]),
    ("AI", [("Claude API", "#D97757"), ("Claude Code", "#D97757"), ("OpenAI API", "#10A37F")]),
    ("TESTING", [("Vitest", "#A3D84B"), ("Playwright", "#2EAD33"), ("Testing Library", "#E33332"),
                 ("Pytest", "#0A9EDC")]),
    ("SHIPPING", [("Vercel", "#FFFFFF"), ("GitHub Pages", "#9FC3FF"), ("GitHub Actions", "#2088FF"),
                  ("Git", "#F05032"), ("pnpm", "#F69220"), ("uv", "#DE5FE9")]),
]

CHAR_W = 11     # monospace advance at font-size 18, pinned with textLength
CHIP_H = 40
GAP = 10
ROW_GAP = 18


def chip(x, y, name, color):
    w = 44 + CHAR_W * len(name)
    body = (f"M{x + 3} {y}h{w - 6}v3h3v{CHIP_H - 6}h-3v3h-{w - 6}v-3h-3v-{CHIP_H - 6}h3z")
    return w, (
        f'<path fill="{PANEL}" d="{body}"/>'
        f'<rect x="{x + 14}" y="{y + 15}" width="10" height="10" fill="{color}"/>'
        f'<text x="{x + 32}" y="{y + 26}" font-family="{MONO}" font-size="18" fill="{INK}" '
        f'textLength="{CHAR_W * len(name)}" lengthAdjust="spacingAndGlyphs">{esc(name)}</text>'
    )


def stack():
    width = 1200
    pad = 48
    label_w = 210
    x0, x1 = pad + label_w, width - pad
    title_d, title_w = pixel_text("STACK", pad, 40, 6)
    body = []
    y = 124
    for label, items in STACK:
        row_top = y
        x = x0
        for name, color in items:
            w = 44 + CHAR_W * len(name)
            if x + w > x1:
                x = x0
                y += CHIP_H + 10
            _, svg = chip(x, y, name, color)
            body.append(svg)
            x += w + GAP
        body.insert(0, f'<rect x="{pad}" y="{row_top + 16}" width="8" height="8" fill="{COURT}"/>'
                       f'<text x="{pad + 20}" y="{row_top + 25}" font-family="{MONO}" font-size="15" '
                       f'letter-spacing="2" fill="{MUTED}">{esc(label)}</text>')
        y += CHIP_H + ROW_GAP
    height = y - ROW_GAP + 36
    names = ", ".join(n for _, items in STACK for n, _ in items)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
<title>Tech stack: {esc(names)}</title>
<rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="18" fill="{BG}" stroke="#1C2647" stroke-width="2"/>
<path fill="{BALL}" d="{title_d}"/>
<text x="{pad + title_w + 20}" y="80" font-family="{MONO}" font-size="18" fill="{MUTED}">what my projects are actually built with</text>
<rect x="{pad}" y="102" width="{width - pad * 2}" height="2" fill="#1A2442"/>
{''.join(body)}
</svg>
"""


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / "header.svg").write_text(header(), encoding="utf-8")
    (ASSETS / "stack.svg").write_text(stack(), encoding="utf-8")
    print("wrote", ASSETS / "header.svg", "and", ASSETS / "stack.svg")
