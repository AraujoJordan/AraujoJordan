"""Render a compact isometric contribution calendar in both README themes."""

from pathlib import Path
import json
import math


root = Path(__file__).parent
calendar = json.loads((root / 'contributions.json').read_text())
weeks = calendar['weeks']
max_count = max(day['contributionCount'] for week in weeks for day in week['contributionDays'])


def shade(color, factor):
    rgb = [int(color[i:i + 2], 16) for i in (1, 3, 5)]
    return '#' + ''.join(f'{round(channel * factor):02x}' for channel in rgb)


def render(theme):
    dark = theme == 'dark'
    bg = '#161b22' if dark else '#ffffff'
    border = '#30363d' if dark else '#d0d7de'
    text = '#c9d1d9' if dark else '#24292f'
    muted = '#8b949e' if dark else '#57606a'
    empty = '#30363d' if dark else '#eaeef2'
    colors = ['#264766', '#356da2', '#448fd2', '#79c0ff'] if dark else ['#b9d9f9', '#82b7ee', '#4c95dc', '#1769b1']
    svg = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="985" height="250" viewBox="0 0 985 250" role="img" aria-labelledby="title desc">',
        f'<title id="title">Jordan Araujo contributions, {theme} mode</title>',
        '<desc id="desc">An isometric chart of daily GitHub contributions over the past year.</desc>',
        f'<rect x="1" y="1" width="983" height="248" rx="16" fill="{bg}" stroke="{border}" stroke-width="1.5"/>',
        f'<text x="28" y="38" font-family="Menlo,Consolas,monospace" font-size="18" font-weight="bold" fill="{text}">Contribution calendar</text>',
        f'<text x="28" y="60" font-family="Menlo,Consolas,monospace" font-size="13" fill="{muted}">{calendar["totalContributions"]} contributions · updated {weeks[-1]["contributionDays"][-1]["date"]}</text>',
    ]
    for week_index, week in enumerate(weeks):
        for day_index, day in enumerate(week['contributionDays']):
            count = day['contributionCount']
            x = 33 + week_index * 16 + day_index * 5
            y = 126 + day_index * 12
            height = 0 if count == 0 else 4 + round(28 * math.log1p(count) / math.log1p(max_count))
            color = empty if count == 0 else colors[min(3, max(0, math.ceil(4 * math.log1p(count) / math.log1p(max_count)) - 1))]
            top = f'{x},{y-height} {x+11},{y-height} {x+15},{y-height-4} {x+4},{y-height-4}'
            svg.append(f'<polygon points="{top}" fill="{color}"/>')
            if height:
                front = f'{x},{y-height} {x+11},{y-height} {x+11},{y} {x},{y}'
                side = f'{x+11},{y-height} {x+15},{y-height-4} {x+15},{y-4} {x+11},{y}'
                svg.append(f'<polygon points="{front}" fill="{shade(color, 0.8)}"/>')
                svg.append(f'<polygon points="{side}" fill="{shade(color, 0.62)}"/>')
    svg.append(f'<text x="28" y="224" font-family="Menlo,Consolas,monospace" font-size="12" fill="{muted}">Less</text>')
    for index, color in enumerate([empty, *colors]):
        svg.append(f'<rect x="{66 + index * 18}" y="212" width="12" height="12" rx="2" fill="{color}"/>')
    svg.append(f'<text x="164" y="224" font-family="Menlo,Consolas,monospace" font-size="12" fill="{muted}">More</text>')
    svg.append('</svg>')
    (root / 'assets' / f'contributions-{theme}.svg').write_text('\n'.join(svg) + '\n')


for theme in ('light', 'dark'):
    render(theme)
