"""Draw assets/player-card.svg from live GitHub data.

Run locally:  GH_TOKEN=$(gh auth token) python3 scripts/make_player_card.py
In CI the workflow passes the built-in GITHUB_TOKEN.
"""

import datetime as dt
import json
import os
import urllib.request
from pathlib import Path

from pixelfont import (BALL, BG, COURT, INK, MONO, MUTED, PANEL, TRAM, esc,
                       pixel_text)

ROOT = Path(__file__).resolve().parent.parent
LOGIN = os.environ.get("LOGIN", "Shawn01ee")

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      contributionCalendar {
        totalContributions
        weeks { contributionDays { weekday contributionLevel } }
      }
    }
    repositories(ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC, first: 100) {
      totalCount
      nodes {
        stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name color } }
        }
      }
    }
  }
}
"""


def fetch():
    token = os.environ.get("GH_TOKEN") or os.environ["GITHUB_TOKEN"]
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode(),
        headers={"Authorization": f"bearer {token}", "User-Agent": "profile-player-card"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.load(resp)
    if "errors" in payload:
        raise SystemExit(payload["errors"])
    return payload["data"]["user"]


LEVEL = {
    "NONE": PANEL,
    "FIRST_QUARTILE": "#1E3A8A",
    "SECOND_QUARTILE": "#2563EB",
    "THIRD_QUARTILE": COURT,
    "FOURTH_QUARTILE": "#9FC3FF",
}


def render(user):
    cc = user["contributionsCollection"]
    repos = user["repositories"]
    stars = sum(r["stargazerCount"] for r in repos["nodes"])

    langs = {}
    for repo in repos["nodes"]:
        for edge in repo["languages"]["edges"]:
            name = edge["node"]["name"]
            size, color = langs.get(name, (0, edge["node"]["color"] or "#8A94B0"))
            langs[name] = (size + edge["size"], color)
    total_bytes = sum(s for s, _ in langs.values()) or 1
    top = sorted(langs.items(), key=lambda kv: -kv[1][0])[:5]

    stats = [
        (f"{cc['contributionCalendar']['totalContributions']:,}", "CONTRIBUTIONS", "past year", COURT),
        (f"{cc['totalCommitContributions']:,}", "COMMITS", "past year", TRAM),
        (f"{cc['totalPullRequestContributions']:,}", "PULL REQUESTS", "past year", BALL),
        (f"{stars:,}", "STARS", "on my repos", "#F6D57A"),
        (f"{repos['totalCount']:,}", "PUBLIC REPOS", "my own, no forks", INK),
    ]

    width, height, pad = 1200, 440, 48
    out = []
    title_d, title_w = pixel_text("PLAYER CARD", pad, 40, 6)
    out.append(f'<path fill="{BALL}" d="{title_d}"/>')
    out.append(f'<text x="{pad + title_w + 20}" y="80" font-family="{MONO}" font-size="18" fill="{MUTED}">'
               f'live from the GitHub API</text>')
    today = dt.date.today().isoformat()
    out.append(f'<text x="{width - pad}" y="80" text-anchor="end" font-family="{MONO}" font-size="15" '
               f'letter-spacing="2" fill="{MUTED}">UPDATED {today}</text>')
    out.append(f'<rect x="{pad}" y="102" width="{width - pad * 2}" height="2" fill="{PANEL}"/>')

    col_w = (width - pad * 2) / len(stats)
    for i, (value, label, note, color) in enumerate(stats):
        x = pad + i * col_w
        d, _ = pixel_text(value, x, 130, 6)
        out.append(f'<path fill="#F4F7FF" d="{d}"/>')
        out.append(f'<rect x="{x:g}" y="193" width="8" height="8" fill="{color}"/>')
        out.append(f'<text x="{x + 16:g}" y="202" font-family="{MONO}" font-size="15" letter-spacing="2" '
                   f'fill="{INK}">{label}</text>')
        out.append(f'<text x="{x + 16:g}" y="223" font-family="{MONO}" font-size="14" fill="{MUTED}">{note}</text>')

    # contribution calendar as a pixel grid
    gx, gy, cell, step = pad, 282, 12, 15
    out.append(f'<text x="{gx}" y="{gy - 14}" font-family="{MONO}" font-size="15" letter-spacing="2" '
               f'fill="{MUTED}">LAST 12 MONTHS</text>')
    by_color = {}
    for w, week in enumerate(cc["contributionCalendar"]["weeks"]):
        for day in week["contributionDays"]:
            color = LEVEL.get(day["contributionLevel"], PANEL)
            by_color.setdefault(color, []).append(
                f"M{gx + w * step} {gy + day['weekday'] * step}h{cell}v{cell}h-{cell}z")
    for color, parts in by_color.items():
        out.append(f'<path fill="{color}" d="{"".join(parts)}"/>')

    # language split
    lx, lw = 880, width - pad - 880
    out.append(f'<text x="{lx}" y="{gy - 14}" font-family="{MONO}" font-size="15" letter-spacing="2" '
               f'fill="{MUTED}">LANGUAGES</text>')
    x = lx
    for i, (name, (size, color)) in enumerate(top):
        seg = lw * size / total_bytes if i < len(top) - 1 else lx + lw - x
        out.append(f'<rect x="{x:.1f}" y="{gy}" width="{max(seg - 2, 1):.1f}" height="12" fill="{color}"/>')
        x += seg
    for i, (name, (size, color)) in enumerate(top):
        y = gy + 38 + i * 24
        out.append(f'<rect x="{lx}" y="{y - 9}" width="8" height="8" fill="{color}"/>')
        out.append(f'<text x="{lx + 16}" y="{y}" font-family="{MONO}" font-size="15" fill="{INK}">{esc(name)}</text>')
        out.append(f'<text x="{lx + lw}" y="{y}" text-anchor="end" font-family="{MONO}" font-size="15" '
                   f'fill="{MUTED}">{100 * size / total_bytes:.1f}%</text>')

    summary = ", ".join(f"{v} {l.lower()}" for v, l, _, _ in stats)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
<title>Player card for {esc(LOGIN)}: {esc(summary)}. Top languages: {esc(", ".join(n for n, _ in top))}.</title>
<rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="18" fill="{BG}" stroke="#1C2647" stroke-width="2"/>
{chr(10).join(out)}
</svg>
"""


def without_date(svg):
    return "\n".join(line for line in svg.splitlines() if "UPDATED " not in line)


if __name__ == "__main__":
    svg = render(fetch())
    target = ROOT / "assets" / "player-card.svg"
    target.parent.mkdir(exist_ok=True)
    # Only rewrite when the numbers changed, so the daily job does not commit just to bump the date.
    if target.exists() and without_date(target.read_text(encoding="utf-8")) == without_date(svg):
        print("no change")
    else:
        target.write_text(svg, encoding="utf-8")
        print("wrote", target)
