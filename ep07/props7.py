# Ep7 props: Verma room pieces, bell underside with the engraved 47 plate, calendar, notes, sweets box, door bolt.
import sys, math, random
sys.path.insert(0, '/home/claude/udhaar/scripts'); sys.path.insert(0, '/home/claude/udhaar/ep06')
from art import *
from shapes import cr_path
from props6 import kalam, INK

P7_DEF = ('<linearGradient id="note500" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#b9b49a"/><stop offset="1" stop-color="#8f8a72"/></linearGradient>'
          '<linearGradient id="doorg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#4f7d78"/><stop offset="1" stop-color="#355754"/></linearGradient>'
          '<radialGradient id="dome_in" cx="0.5" cy="0.45" r="0.6"><stop offset="0" stop-color="#5a4016"/><stop offset="0.7" stop-color="#2a1d0c"/><stop offset="1" stop-color="#120c05"/></radialGradient>'
          '<linearGradient id="plate" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e2bd66"/><stop offset="1" stop-color="#8d6624"/></linearGradient>')

def note500(x, y, rot=0, s=1.0, shade=0):
    """₹500 note, muted; no legible bank text (only the numeral)"""
    o = f'<g transform="translate({x},{y}) rotate({rot}) scale({s})">'
    o += '<rect x="0" y="0" width="300" height="134" rx="4" fill="url(#note500)"/>'
    o += '<rect x="10" y="10" width="280" height="114" rx="3" fill="none" stroke="#6f6a52" stroke-width="2" stroke-opacity="0.6"/>'
    o += '<circle cx="216" cy="67" r="38" fill="#a6a186" stroke="#6f6a52" stroke-width="2" stroke-opacity="0.5"/>'
    o += '<rect x="96" y="10" width="8" height="114" fill="#6f6a52" fill-opacity="0.45"/>'
    o += '<text x="34" y="58" font-family="Mukta" font-weight="800" font-size="34" fill="#5d5843" fill-opacity="0.9">500</text>'
    o += '<text x="250" y="118" font-family="Mukta" font-weight="800" font-size="22" fill="#5d5843" fill-opacity="0.8">500</text>'
    if shade: o += f'<rect width="300" height="134" fill="#000" fill-opacity="{shade}"/>'
    return o + '</g>'

def note_stack(x, y, n=8, rot=0, s=1.0, seed=1):
    rnd = random.Random(seed)
    return ''.join(note500(x + rnd.uniform(-8, 8), y - i * 3, rot + rnd.uniform(-3, 3), s, 0.25 * (1 - i / n)) for i in range(n))

def bell_underside(x, y, s=1.0, plate=True, dust=0.0):
    """the dome seen from below/inside: rim ellipse, dark interior, clapper, riveted brass plate engraved 47"""
    o = f'<g transform="translate({x},{y}) scale({s})">'
    o += '<ellipse cx="0" cy="0" rx="300" ry="250" fill="url(#brass)"/>'
    o += '<ellipse cx="0" cy="0" rx="270" ry="222" fill="url(#dome_in)"/>'
    o += '<ellipse cx="0" cy="0" rx="300" ry="250" fill="none" stroke="#f3d68e" stroke-width="10" stroke-opacity="0.7"/>'
    o += '<path d="M-250,-80 C-200,-190 -80,-230 40,-226" stroke="#fff1c0" stroke-width="10" fill="none" stroke-opacity="0.5" stroke-linecap="round"/>'
    # clapper stem & ball
    o += '<path d="M-6,-40 L-4,70 L4,70 L6,-40 Z" fill="#3a2c1a"/><circle cx="0" cy="84" r="22" fill="#7a5a28"/><circle cx="-6" cy="78" r="6" fill="#d9b56a" fill-opacity="0.7"/>'
    if plate:
        o += '<g transform="translate(-10,-130) rotate(-4)"><rect x="-120" y="-56" width="240" height="112" rx="10" fill="#000" fill-opacity="0.45" transform="translate(6,8)"/>'
        o += '<rect x="-120" y="-56" width="240" height="112" rx="10" fill="url(#plate)"/>'
        o += ''.join(f'<circle cx="{cx}" cy="{cy}" r="8" fill="#6a4a1a"/><circle cx="{cx-2}" cy="{cy-2}" r="3" fill="#f6dc9a"/>' for cx, cy in ((-100, -36), (100, -36), (-100, 36), (100, 36)))
        # engraved numeral: dark cut + light lower edge
        o += '<text x="2" y="38" font-family="Mukta" font-weight="800" font-size="104" text-anchor="middle" fill="#fff1c0" fill-opacity="0.6">47</text>'
        o += '<text x="0" y="34" font-family="Mukta" font-weight="800" font-size="104" text-anchor="middle" fill="#3a2608">47</text></g>'
    if dust:
        o += f'<ellipse cx="0" cy="0" rx="300" ry="250" fill="#8a8070" fill-opacity="{dust}"/>'
    return o + '</g>'

def bell_dusty(x, y, s=1.0, clean_side=0.0):
    """the dome bell, dull with years of dust; clean_side 0..1 = a polished streak"""
    o = bell(x, y, s, glint=clean_side > 0.3)
    o += f'<g transform="translate({x},{y}) scale({s})"><path d="M-90,70 C-90,10 -50,-12 0,-12 C50,-12 90,10 90,70 C90,82 -90,82 -90,70 Z" fill="#7d7564" fill-opacity="{0.55*(1-clean_side*0.2)}"/>'
    if clean_side:
        o += f'<path d="M-70,58 C-62,18 -36,0 -4,-4 C10,10 6,40 -10,66 Z" fill="url(#brass)" fill-opacity="{clean_side}"/>'
        o += f'<path d="M-60,40 C-50,14 -30,4 -8,2" stroke="#fff6d0" stroke-width="7" fill="none" stroke-opacity="{0.8*clean_side}" stroke-linecap="round"/>'
    return o + '</g>'

def iron_cot(x, y, w, s=1.0, sheet='#7d8a8c'):
    """iron cot side view: (x,y)=top-left of mattress"""
    return (f'<g transform="translate({x},{y}) scale({s})">'
            f'<rect x="0" y="0" width="{w}" height="46" rx="10" fill="{sheet}"/><rect x="0" y="0" width="{w}" height="12" rx="6" fill="#fff" fill-opacity="0.12"/>'
            + ''.join(f'<path d="M{20 + i*(w-40)/6:.0f},4 L{40 + i*(w-40)/6:.0f},40" stroke="#5a6668" stroke-width="5" stroke-opacity="0.5"/>' for i in range(7)) +
            f'<rect x="-20" y="46" width="{w+40}" height="18" fill="#1c1c1e"/>'
            f'<rect x="-20" y="-120" width="16" height="420" fill="#1c1c1e"/><rect x="{w+4}" y="-120" width="16" height="420" fill="#1c1c1e"/>'
            f'<path d="M-12,-100 L{w+12},-100" stroke="#1c1c1e" stroke-width="10"/>'
            + ''.join(f'<path d="M{-12 + i*(w+24)/10:.0f},64 L{-12 + i*(w+24)/10:.0f},290" stroke="#1c1c1e" stroke-width="5" stroke-opacity="0.6"/>' for i in range(1, 10)) +
            f'<path d="M-12,280 L{w+12},280" stroke="#1c1c1e" stroke-width="8"/></g>')

def sweets_box(x, y, s=1.0, rot=0, open_=False):
    o = f'<g transform="translate({x},{y}) rotate({rot}) scale({s})">'
    o += '<rect x="8" y="12" width="300" height="200" rx="6" fill="#000" fill-opacity="0.35" filter="url(#b8)"/>'
    o += '<rect x="0" y="0" width="300" height="200" rx="6" fill="#c9a06e"/>'
    o += '<rect x="0" y="0" width="300" height="56" rx="6" fill="#a8764e"/>'
    o += '<path d="M20,110 C60,80 100,140 140,110 C180,80 220,140 280,110" stroke="#8a5a3a" stroke-width="6" fill="none" stroke-opacity="0.6"/>'
    o += '<circle cx="150" cy="140" r="26" fill="#e6cc9a"/><circle cx="150" cy="140" r="14" fill="#a8764e"/>'
    o += '<path d="M150,0 L150,200 M0,96 L300,96" stroke="#e8e0cc" stroke-width="4" stroke-opacity="0.9"/>'
    return o + '</g>'

def wall_calendar(x, y, s=1.0, crossed=range(11, 18), today=17, pencil_swing=8):
    """Dec 2026 month grid (1 Dec = Tuesday); Ma's neat pencil crosses; pencil on a string"""
    o = f'<g transform="translate({x},{y}) scale({s})">'
    o += '<path d="M200,-40 L120,10 M200,-40 L280,10" stroke="#2a2420" stroke-width="3"/><circle cx="200" cy="-40" r="6" fill="#2a2420"/>'
    o += '<rect x="10" y="16" width="400" height="520" fill="#000" fill-opacity="0.3" filter="url(#b8)"/>'
    o += '<rect x="0" y="0" width="400" height="520" fill="#ebe3cf"/><rect x="0" y="0" width="400" height="110" fill="#b4a78a"/>'
    o += kalam(200, 80, 'दिसंबर', 54, '#3a3228', anchor='middle', font='Mukta', weight=700)
    days = 'सो मं बु गु शु श र'.split()
    o += ''.join(f'<text x="{38 + i*54}" y="150" font-family="Mukta" font-size="22" font-weight="700" fill="#5a5044" text-anchor="middle">{d}</text>' for i, d in enumerate(days))
    col0 = 1  # 1 Dec 2026 is a Tuesday (Mon-first grid -> column 1)
    for dnum in range(1, 32):
        k = dnum - 1 + col0; cx = 38 + (k % 7) * 54; cy = 196 + (k // 7) * 62
        o += f'<text x="{cx}" y="{cy}" font-family="Mukta" font-size="28" fill="#3a3228" text-anchor="middle">{dnum}</text>'
        if dnum in crossed:
            o += f'<path d="M{cx-20},{cy-30} L{cx+20},{cy+8} M{cx+20},{cy-30} L{cx-20},{cy+8}" stroke="#4a4a52" stroke-width="3.2" stroke-linecap="round" stroke-opacity="{0.95 if dnum == today else 0.75}"/>'
    o += f'<g transform="rotate({pencil_swing} 380 10)"><path d="M380,10 L380,560" stroke="#d9d0bc" stroke-width="2"/><g transform="translate(380,600) rotate(90)"><rect x="-40" y="-7" width="120" height="14" fill="#c9a23a"/><path d="M-40,-7 L-58,0 L-40,7 Z" fill="#e6c79c"/></g></g>'
    return o + '</g>'

def door_bolt(x, y, s=1.0, slid=1.0):
    """iron kundi/bolt on the blue-green door: plate, bar, staple; slid 0..1"""
    o = f'<g transform="translate({x},{y}) scale({s})">'
    o += '<rect x="-180" y="-40" width="230" height="80" rx="8" fill="#26282a"/><circle cx="-160" cy="-22" r="6" fill="#4a4c4e"/><circle cx="-160" cy="22" r="6" fill="#4a4c4e"/><circle cx="30" cy="-22" r="6" fill="#4a4c4e"/><circle cx="30" cy="22" r="6" fill="#4a4c4e"/>'
    bx = -150 + 180 * slid
    o += f'<rect x="{bx}" y="-14" width="260" height="28" rx="12" fill="#3a3c3e"/><rect x="{bx}" y="-14" width="260" height="8" rx="4" fill="#8a8c8e" fill-opacity="0.5"/>'
    o += f'<rect x="{bx+120}" y="-14" width="18" height="70" rx="6" fill="#3a3c3e"/><circle cx="{bx+129}" cy="62" r="14" fill="#3a3c3e"/>'
    o += '<rect x="210" y="-50" width="60" height="100" rx="6" fill="#26282a"/>'
    return o + '</g>'
