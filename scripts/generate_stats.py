#!/usr/bin/env python3
import json, os, urllib.request
from pathlib import Path
from xml.sax.saxutils import escape

USER = "SlimanKhan"
OUT = Path("assets")
headers = {"Accept": "application/vnd.github+json", "User-Agent": "SlimanKhan-profile-generator"}
token = os.environ.get("GITHUB_TOKEN")
if token:
    headers["Authorization"] = f"Bearer {token}"

def fetch(url):
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.load(response)

profile = fetch(f"https://api.github.com/users/{USER}")
repositories = fetch(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner")
stats = [
    ("Public repositories", profile.get("public_repos", 0)),
    ("Followers", profile.get("followers", 0)),
    ("Stars received", sum(r.get("stargazers_count", 0) for r in repositories)),
    ("Forks", sum(r.get("forks_count", 0) for r in repositories)),
]

for theme in ("dark", "light"):
    if theme == "dark":
        bg, panel, heading, muted, accent, border = "#0D1117", "#161B22", "#F0F6FC", "#9BA7B4", "#60A5FA", "#30363D"
    else:
        bg, panel, heading, muted, accent, border = "#FFFFFF", "#F8FAFC", "#0F172A", "#475569", "#2563EB", "#E2E8F0"
    pieces = []
    for index, (label, value) in enumerate(stats):
        x, y = 36 + (index % 2) * 350, 100 + (index // 2) * 100
        pieces.append(f'<rect x="{x}" y="{y}" width="320" height="76" rx="12" fill="{panel}" stroke="{border}"/>')
        pieces.append(f'<text x="{x+18}" y="{y+29}" fill="{muted}" font-family="Arial,sans-serif" font-size="13">{escape(label)}</text>')
        pieces.append(f'<text x="{x+18}" y="{y+59}" fill="{accent}" font-family="Arial,sans-serif" font-size="25" font-weight="700">{value}</text>')
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="720" height="310" viewBox="0 0 720 310"><rect width="720" height="310" rx="18" fill="{bg}" stroke="{border}"/><text x="36" y="48" fill="{heading}" font-family="Arial,sans-serif" font-size="20" font-weight="700">GitHub profile snapshot</text><text x="36" y="72" fill="{muted}" font-family="Arial,sans-serif" font-size="12">@{USER} · live public profile data</text>{''.join(pieces)}</svg>'
    (OUT / f"stats-{theme}.svg").write_text(svg, encoding="utf-8")
