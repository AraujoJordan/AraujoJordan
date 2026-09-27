"""Generate light and dark GitHub profile SVGs from the portrait and stats."""

from pathlib import Path
import base64
import html
import json


ROOT = Path(__file__).parent
ASSETS = ROOT / 'assets'
STATS = json.loads((ROOT / 'stats.json').read_text())
PORTRAIT = 'data:image/jpeg;base64,' + base64.b64encode((ASSETS / 'portrait.jpg').read_bytes()).decode('ascii')


def render(theme):
    dark = theme == 'dark'
    colors = {
        'bg': '#161b22' if dark else '#ffffff',
        'stroke': '#30363d' if dark else '#d0d7de',
        'text': '#c9d1d9' if dark else '#24292f',
        'key': '#ffa657' if dark else '#953800',
        'value': '#a5d6ff' if dark else '#0a3069',
        'muted': '#8b949e' if dark else '#57606a',
    }
    font = 'Menlo,Consolas,monospace'
    svg = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="985" height="580" viewBox="0 0 985 580" role="img" aria-labelledby="title desc">',
        f'<title id="title">Jordan Araujo profile, {theme} mode</title>',
        '<desc id="desc">Jordan’s portrait beside his mobile engineering profile, interests, and GitHub stats.</desc>',
        f'<rect x="1" y="1" width="983" height="578" rx="20" fill="{colors["bg"]}" stroke="{colors["stroke"]}" stroke-width="1.5"/>',
        '<defs><clipPath id="portrait"><rect x="20" y="20" width="360" height="540" rx="12"/></clipPath></defs>',
        f'<image x="20" y="20" width="360" height="540" clip-path="url(#portrait)" href="{PORTRAIT}"/>',
    ]

    def txt(x, y, value, color='text', size=16, weight='normal'):
        svg.append(f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" fill="{colors[color]}">{html.escape(str(value))}</text>')

    def row(y, key, value):
        txt(429, y, key, 'key')
        txt(551, y, ':')
        txt(572, y, value, 'value')

    def section(y, title):
        txt(410, y, f'─ {title} ' + '─' * max(0, 42 - len(title)), 'muted')

    svg.append(f'<text x="410" y="45" font-family="{font}" font-size="17" font-weight="bold"><tspan fill="{colors["key"]}">jordan</tspan><tspan fill="{colors["text"]}">@</tspan><tspan fill="{colors["value"]}">github</tspan></text>')
    txt(410, 62, '─────────────', 'muted')
    row(91, 'Name', 'Jordan L. Araujo Jr.')
    row(112, 'Role', 'Senior Android Engineer')
    row(133, 'Work', 'ServiceTitan')
    row(154, 'Location', 'Calgary, Canada')
    row(175, 'Experience', '10+ years in mobile')
    row(196, 'Website', 'araujojordan.com')
    section(225, 'Tech Stack')
    row(251, 'Mobile', 'Kotlin, Compose, KMP')
    row(272, 'Languages', 'Kotlin, Java, TypeScript, Python')
    row(293, 'Web', 'React, Next.js, CSS')
    row(314, 'Testing', 'Paparazzi, UIAutomator')
    section(342, 'Outside the IDE')
    row(368, 'Game Dev', 'Godot projects')
    row(389, 'Creative', 'Pixel art, 3D worlds')
    row(410, 'Audio', 'Game sound experiments')
    section(438, 'Open Source + GitHub')
    row(464, 'Projects', 'Reflow, ExcuseMe, Kobaia')
    row(485, 'Public Repos', STATS['public_repos'])
    txt(706, 485, 'Stars:', 'key')
    txt(785, 485, STATS['earned_stars'], 'value')
    row(506, 'Followers', STATS['followers'])
    txt(706, 506, 'Contribs:', 'key')
    txt(805, 506, STATS['year_contributions'], 'value')
    txt(410, 548, f'GitHub snapshot: {STATS["as_of"]}', 'muted', 13)
    svg.append('</svg>')
    (ASSETS / f'{theme}_mode.svg').write_text('\n'.join(svg) + '\n')


for theme in ('light', 'dark'):
    render(theme)
