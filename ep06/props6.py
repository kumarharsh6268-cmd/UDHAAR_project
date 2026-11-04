# Ep6 props & set pieces (SVG strings). Shared art library conventions (art.py).
import sys, math, random
sys.path.insert(0, '/home/claude/udhaar/scripts')
from art import *
from shapes import cr_path

INK = '#26284a'
PROPS_DEF = (BRASS_DEF + RED_DEF + PAGE_DEF +
    '<linearGradient id="blk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a3a3e"/><stop offset="0.45" stop-color="#18181b"/><stop offset="1" stop-color="#0c0c0e"/></linearGradient>'
    '<linearGradient id="chrome" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f2f2ee"/><stop offset="0.5" stop-color="#9a9c9e"/><stop offset="1" stop-color="#4a4c50"/></linearGradient>'
    '<linearGradient id="woodt" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7a5636"/><stop offset="1" stop-color="#4a3220"/></linearGradient>'
    '<linearGradient id="paperw" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f4efe2"/><stop offset="1" stop-color="#ddd5c2"/></linearGradient>'
    '<linearGradient id="env" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e9dcc0"/><stop offset="1" stop-color="#c9b896"/></linearGradient>'
    '<linearGradient id="khaki" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#a08a62"/><stop offset="1" stop-color="#6a5838"/></linearGradient>')

# ------------------------------------------------------------------ sewing machine (side view, needle at LEFT)
def sewing_machine(x, y, s=1.0, cover=None, flip=False, decal=0.55, thread='#6d7f8a', glint=1.0):
    """classic black treadle-head machine; (x,y)=bottom centre of bed; ~430*s wide, ~260*s tall"""
    o = []
    o.append('<path d="M-215,-34 L215,-34 C224,-34 228,-28 228,-20 L228,0 L-215,0 C-224,0 -228,-6 -228,-14 L-228,-22 C-228,-30 -222,-34 -215,-34 Z" fill="url(#blk)"/>')
    o.append(f'<path d="M-222,-32 L222,-32" stroke="#8a8a90" stroke-width="3" stroke-opacity="{0.6*glint}"/>')
    o.append('<rect x="-150" y="-30" width="70" height="22" rx="3" fill="#5a5a60" fill-opacity="0.8"/>')  # needle plate
    # pillar + arm
    o.append('<path d="M110,-34 C108,-90 112,-150 122,-196 C130,-232 160,-248 196,-246 C216,-244 226,-232 226,-212 L222,-34 Z" fill="url(#blk)"/>')
    o.append('<path d="M-196,-246 C-120,-262 60,-262 200,-246 C214,-244 222,-236 222,-222 L216,-196 C120,-206 -60,-206 -196,-200 Z" fill="url(#blk)"/>')
    o.append(f'<path d="M-190,-250 C-110,-264 60,-264 196,-250" stroke="#9a9aa2" stroke-width="5" fill="none" stroke-opacity="{0.55*glint}"/>')
    # head (left)
    o.append('<path d="M-214,-252 C-224,-252 -230,-244 -230,-232 L-226,-70 C-226,-60 -220,-54 -210,-54 L-146,-54 C-136,-54 -132,-60 -132,-70 L-130,-204 C-130,-236 -160,-254 -214,-252 Z" fill="url(#blk)"/>')
    o.append('<rect x="-222" y="-232" width="64" height="150" rx="10" fill="url(#chrome)" fill-opacity="0.22"/>')
    # needle bar, foot, needle
    o.append('<rect x="-190" y="-60" width="9" height="34" fill="url(#chrome)"/><path d="M-186,-26 L-186,-12" stroke="#d9d9d4" stroke-width="2.4"/>')
    o.append('<path d="M-206,-30 L-166,-30 L-160,-24 L-208,-24 Z" fill="url(#chrome)"/>')
    # spool pin & thread
    o.append(f'<rect x="-24" y="-296" width="5" height="44" fill="#9a9a9e"/><rect x="-40" y="-292" width="36" height="22" rx="4" fill="{thread}"/>')
    o.append(f'<path d="M-24,-292 C-80,-300 -150,-280 -186,-200" stroke="#e8e2d0" stroke-width="1.4" fill="none" stroke-opacity="0.7"/>')
    # handwheel
    o.append('<ellipse cx="232" cy="-176" rx="22" ry="56" fill="#121214"/><ellipse cx="236" cy="-176" rx="16" ry="48" fill="url(#chrome)" fill-opacity="0.75"/><ellipse cx="238" cy="-176" rx="7" ry="20" fill="#2a2a2e"/>')
    # gold decal scrolls (muted)
    o.append(f'<g stroke="#b9994e" stroke-opacity="{decal}" fill="none" stroke-width="3">'
             '<path d="M-110,-232 C-80,-246 -40,-246 -10,-234 C10,-226 30,-226 50,-234"/>'
             '<path d="M-100,-220 C-70,-230 -40,-228 -20,-220 M60,-236 C90,-246 130,-244 160,-232"/>'
             '<path d="M130,-170 C140,-140 140,-110 132,-80 M150,-160 C158,-130 158,-100 150,-70"/>'
             '<circle cx="-60" cy="-226" r="5"/><circle cx="100" cy="-228" r="5"/></g>')
    if cover == 'half':
        cv = '#7a6e5e'
        o.append(f'<path d="M-40,-282 C60,-292 200,-270 246,-200 C262,-140 258,-60 262,-6 L210,8 C170,-8 140,8 100,-2 C60,10 20,-4 -10,4 C-40,-60 -30,-140 -60,-200 C-70,-240 -60,-270 -40,-282 Z" fill="{cv}"/>')
        o.append('<path d="M40,-284 C70,-180 50,-90 70,0 M170,-260 C180,-160 200,-80 220,4" stroke="#000" stroke-opacity="0.2" stroke-width="10" fill="none" filter="url(#b4)"/>')
        o.append('<path d="M-40,-282 C60,-292 200,-270 240,-205" stroke="#fff3da" stroke-opacity="0.35" stroke-width="5" fill="none"/>')
    elif cover:
        o.append(f'<path d="M-250,-150 C-230,-250 -120,-290 0,-290 C140,-292 236,-262 252,-160 C262,-100 258,-50 262,-6 L210,10 C170,-10 140,8 100,-2 C60,12 20,-4 -20,6 C-60,-8 -100,10 -140,-2 C-180,12 -220,0 -262,8 C-262,-40 -258,-100 -250,-150 Z" fill="{cover}"/>')
        o.append('<path d="M-200,-220 C-180,-150 -190,-70 -210,0 M-60,-280 C-40,-180 -60,-80 -50,4 M80,-284 C110,-180 90,-90 110,0 M200,-250 C200,-160 220,-80 236,4" stroke="#000" stroke-opacity="0.18" stroke-width="10" fill="none" filter="url(#b4)"/>')
        o.append('<path d="M-240,-190 C-200,-262 -80,-286 20,-286 C130,-284 220,-256 240,-200" stroke="#fff3da" stroke-opacity="0.35" stroke-width="5" fill="none"/>')
    sx = -s if flip else s
    return f'<g transform="translate({x},{y}) scale({sx},{s})">{"".join(o)}</g>'

def treadle_table(x, y, w, h=40, s=1.0, legs=True, depth=0):
    """wooden table top (x,y)=top-left; iron treadle legs below"""
    o = [R(x, y, w, h, 'url(#woodt)'), R(x, y, w, 6, '#9a7450', 0.7), R(x + w * 0.62, y + h, w * 0.3, 70 * s, '#5a3e28')]
    o.append(R(x + w * 0.66, y + h + 22 * s, w * 0.22, 8 * s, '#a88a62', 0.5))
    if legs:
        lx = [x + 30 * s, x + w - 50 * s]
        for xx in lx:
            o.append(f'<path d="M{xx},{y+h} L{xx+8*s},{y+h+330*s} L{xx+28*s},{y+h+330*s} L{xx+24*s},{y+h} Z" fill="#1a1a1c"/>')
            o.append(f'<path d="M{xx+12*s},{y+h+80*s} C{xx-20*s},{y+h+140*s} {xx+50*s},{y+h+190*s} {xx+14*s},{y+h+250*s}" stroke="#1a1a1c" stroke-width="{7*s}" fill="none"/>')
        o.append(f'<path d="M{lx[0]},{y+h+300*s} L{lx[1]+28*s},{y+h+300*s}" stroke="#1a1a1c" stroke-width="{9*s}"/>')
        o.append(f'<path d="M{lx[0]+40*s},{y+h+320*s} L{lx[1]-10*s},{y+h+290*s} L{lx[1]-10*s},{y+h+312*s} L{lx[0]+40*s},{y+h+338*s} Z" fill="#26262a"/>')
    return ''.join(o)

def stool(x, y, s=1.0, col='#5a3e28'):
    return (f'<g transform="translate({x},{y}) scale({s})"><rect x="-70" y="-14" width="140" height="22" rx="6" fill="{col}"/>'
            '<rect x="-70" y="-14" width="140" height="6" fill="#9a7450" fill-opacity="0.6"/>'
            f'<path d="M-60,8 L-74,160 L-60,160 L-44,8 Z M60,8 L74,160 L60,160 L44,8 Z M-20,8 L-26,150 L-14,150 L-8,8 Z" fill="{col}"/>'
            f'<path d="M-66,96 L66,96" stroke="{col}" stroke-width="8"/></g>')

def bulb(x, y, cord_top=0, glow=1.0, r=26):
    return (S(f'M{x},{cord_top} L{x},{y-r}', '#1a1714', 3) +
            g(E(x, y + 10, 260 * glow, 260 * glow, '#ffd590', 0.28), filt='b60') +
            g(E(x, y, 90, 90, '#ffe7b0', 0.45), filt='b24') +
            R(x - 9, y - r - 16, 18, 20, '#3a332a') + E(x, y, r * 0.8, r, '#fff3cf'))

def cloth_shelves(x, y, w, h, rows=5, seed=3, cols=None, sat=1.0):
    rnd = random.Random(seed)
    cols = cols or ['#8a5a4a', '#5a6f7a', '#a08850', '#6a7a5a', '#7a5a6e', '#c0b49a', '#4f5f6e', '#9a6a3e', '#6e4a3a', '#b0a080', '#4a6a5e', '#8e7a96']
    o = [R(x, y, w, h, '#2e241c')]
    rh = h / rows
    for r_ in range(rows):
        yy = y + r_ * rh
        o.append(R(x, yy + rh - 10, w, 10, '#5a4030'))
        xx = x + 8
        while xx < x + w - 30:
            bw = rnd.uniform(56, 110); stack = rnd.randint(3, 6); sh = (rh - 18) / stack
            for k in range(stack):
                c = rnd.choice(cols)
                o.append(f'<rect x="{xx:.1f}" y="{yy + rh - 10 - (k+1)*sh:.1f}" width="{bw:.1f}" height="{sh-2:.1f}" rx="5" fill="{c}"/>')
                o.append(f'<rect x="{xx:.1f}" y="{yy + rh - 10 - (k+1)*sh:.1f}" width="{bw:.1f}" height="{(sh-2)*0.3:.1f}" rx="4" fill="#fff" fill-opacity="0.10"/>')
            xx += bw + rnd.uniform(4, 10)
    return ''.join(o)

def bolts_tall(x, y, w, h, seed=7, cols=None):
    """bolts of cloth rolled & stacked to the ceiling (front view: circles/rolls)"""
    rnd = random.Random(seed)
    cols = cols or ['#7e5848', '#566a76', '#9c8450', '#647458', '#76586a', '#bdb196', '#4e5d6c', '#94683e', '#a8987c', '#4a665a']
    o = []
    rr = 44
    yy = y + h - rr
    row = 0
    while yy > y - rr:
        xx = x + rr + (rr if row % 2 else 0)
        while xx < x + w:
            c = rnd.choice(cols)
            o.append(E(xx, yy, rr, rr * 0.98, c))
            o.append(E(xx - 8, yy - 8, rr * 0.75, rr * 0.72, '#fff', 0.07))
            o.append(f'<circle cx="{xx}" cy="{yy}" r="{rr*0.62}" fill="none" stroke="#000" stroke-opacity="0.16" stroke-width="3"/>')
            o.append(f'<circle cx="{xx}" cy="{yy}" r="{rr*0.3}" fill="none" stroke="#000" stroke-opacity="0.16" stroke-width="3"/>')
            o.append(E(xx, yy, 8, 8, '#2a2018', 0.8))
            xx += rr * 2 + 2
        yy -= rr * 1.74; row += 1
    return ''.join(o)

# ------------------------------------------------------------------ paper props
def envelope(x, y, w=180, h=110, rot=0, fill='url(#env)', flap=True, shade=0.0):
    o = f'<g transform="translate({x},{y}) rotate({rot})">'
    o += f'<rect x="{-w/2+6}" y="{-h/2+8}" width="{w}" height="{h}" rx="4" fill="#000" fill-opacity="0.35" filter="url(#b6)"/>'
    o += f'<rect x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" rx="3" fill="{fill}"/>'
    if flap:
        o += f'<path d="M{-w/2},{-h/2} L0,{h*0.12} L{w/2},{-h/2}" fill="none" stroke="#8a7a5a" stroke-width="2.4" stroke-opacity="0.7"/>'
        o += f'<path d="M{-w/2},{h/2} L{-w*0.12},{0} M{w/2},{h/2} L{w*0.12},0" stroke="#8a7a5a" stroke-width="1.6" stroke-opacity="0.4"/>'
    if shade: o += f'<rect x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" fill="#000" fill-opacity="{shade}"/>'
    return o + '</g>'

def ruled_paper(x, y, w, h, rot=0, fill='url(#pagec)', rule='#9fb2b6', margin='#d08a8a', step=56, first=120, content='', shadow=True):
    o = f'<g transform="translate({x},{y}) rotate({rot})">'
    if shadow: o += f'<rect x="10" y="14" width="{w}" height="{h}" fill="#120c08" fill-opacity="0.45" filter="url(#b12)"/>'
    o += f'<rect width="{w}" height="{h}" fill="{fill}"/>'
    o += ''.join(f'<path d="M24,{yy} L{w-18},{yy}" stroke="{rule}" stroke-width="2" stroke-opacity="0.7"/>' for yy in range(first, int(h) - 20, step))
    if margin: o += f'<path d="M96,16 L96,{h-16}" stroke="{margin}" stroke-width="2.4" stroke-opacity="0.6"/>'
    return o + content + '</g>'

def kalam(x, y, t, size=60, fill=INK, rot=0, weight=400, op=0.92, anchor='start', font='Kalam'):
    return f'<text x="{x}" y="{y}" font-family="{font}" font-weight="{weight}" font-size="{size}" fill="{fill}" fill-opacity="{op}" text-anchor="{anchor}" transform="rotate({rot} {x} {y})">{t}</text>'

def ledger_spread(x, y, w, h, left='', right='', rot=0, cover=True):
    """open red cloth ledger; left/right = SVG content in page-local coords (page w/2-30 wide)"""
    pw = w / 2 - 22
    o = f'<g transform="translate({x},{y}) rotate({rot})">'
    if cover:
        o += f'<rect x="-14" y="-14" width="{w+28}" height="{h+28}" rx="14" fill="#120c08" fill-opacity="0.55" filter="url(#b16)" transform="translate(12,16)"/>'
        o += f'<rect x="-14" y="-14" width="{w+28}" height="{h+28}" rx="14" fill="url(#ledger)"/><rect x="-14" y="-14" width="{w+28}" height="{h+28}" rx="14" fill="url(#weave)"/>'
    for i, cont in enumerate((left, right)):
        px = 8 + i * (pw + 28)
        o += f'<g transform="translate({px},6)"><rect width="{pw}" height="{h-12}" fill="url(#pagec)"/>'
        o += ''.join(f'<path d="M20,{yy} L{pw-14},{yy}" stroke="#9fb2b6" stroke-width="1.8" stroke-opacity="0.65"/>' for yy in range(110, int(h) - 40, 54))
        o += f'<path d="M70,14 L70,{h-26}" stroke="#d08a8a" stroke-width="2" stroke-opacity="0.55"/>{cont}</g>'
    # gutter shadow
    o += f'<rect x="{w/2-30}" y="6" width="60" height="{h-12}" fill="#3a2a1a" fill-opacity="0.35" filter="url(#b12)"/>'
    o += f'<path d="M{w/2},6 L{w/2},{h-6}" stroke="#6a5038" stroke-width="2" stroke-opacity="0.6"/>'
    return o + '</g>'

def page6_content(scale=1.0, address=True, amount=True):
    o = kalam(40, 92, '6.', 56) + kalam(100, 92, 'रुख़साना बेगम', 66, weight=700)
    if address: o += kalam(104, 200, 'दर्ज़ी गली', 54)
    if amount:
        o += kalam(104, 306, '₹ 30,000', 62, weight=700) + kalam(400, 306, '— मशीन', 52)
        o += kalam(104, 410, '2006', 50)
    return o

def pencil(x, y, L=300, rot=0, w=16, col='#c9a23a'):
    return (f'<g transform="translate({x},{y}) rotate({rot})">'
            f'<rect x="0" y="{-w/2}" width="{L}" height="{w}" fill="{col}"/><rect x="0" y="{-w/2}" width="{L}" height="{w*0.35}" fill="#fff" fill-opacity="0.25"/>'
            f'<path d="M0,{-w/2} L{-34},0 L0,{w/2} Z" fill="#e6c79c"/><path d="M-26,-2.6 L-34,0 L-26,2.6 Z" fill="#2a2a2e"/>'
            f'<rect x="{L}" y="{-w/2}" width="22" height="{w}" fill="#a8a8a8"/><rect x="{L+22}" y="{-w/2}" width="18" height="{w}" rx="4" fill="#c98a8a"/></g>')

def ticket(x, y, s=1.0, rot=0, circled=False):
    """pale bus ticket; Route 47; 9-1-2001 (fixed canon)"""
    o = f'<g transform="translate({x},{y}) rotate({rot}) scale({s})">'
    o += '<rect x="8" y="12" width="300" height="520" fill="#000" fill-opacity="0.35" filter="url(#b8)"/>'
    o += '<path d="M0,0 L300,0 L300,520 L0,520 Z" fill="#e6dfc4"/>'
    o += ''.join(f'<circle cx="{xx}" cy="0" r="7" fill="#3a3028"/>' for xx in range(20, 300, 26))
    o += '<rect x="0" y="0" width="300" height="520" fill="#c9b98a" fill-opacity="0.18"/>'
    f = 'font-family="Mukta" fill="#5a5048"'
    o += f'<text x="150" y="62" {f} font-size="26" font-weight="700" text-anchor="middle" letter-spacing="3">NAGAR BUS SEVA</text>'
    o += '<path d="M24,82 L276,82" stroke="#5a5048" stroke-width="2" stroke-opacity="0.7"/>'
    o += f'<text x="30" y="136" {f} font-size="24" font-weight="600">ROUTE</text>'
    o += f'<text x="150" y="232" {f} font-size="118" font-weight="800" text-anchor="middle" fill-opacity="0.9">47</text>'
    o += '<path d="M24,262 L276,262" stroke="#5a5048" stroke-width="2" stroke-opacity="0.6" stroke-dasharray="6 6"/>'
    o += f'<text x="30" y="312" {f} font-size="26" font-weight="600">DATE</text><text x="270" y="312" {f} font-size="30" font-weight="700" text-anchor="end">9-1-2001</text>'
    o += f'<text x="30" y="368" {f} font-size="26" font-weight="600">FARE</text><text x="270" y="368" {f} font-size="30" font-weight="700" text-anchor="end">₹ 4</text>'
    o += '<path d="M24,400 L276,400" stroke="#5a5048" stroke-width="2" stroke-opacity="0.6" stroke-dasharray="6 6"/>'
    o += ''.join(f'<rect x="{30+i*24}" y="430" width="{10 + (i*7)%9}" height="60" fill="#5a5048" fill-opacity="0.35"/>' for i in range(10))
    # wear: fold line, stain
    o += '<path d="M0,250 L300,268" stroke="#8a7e66" stroke-width="2" stroke-opacity="0.5"/><ellipse cx="220" cy="460" rx="60" ry="40" fill="#a08a5a" fill-opacity="0.15" filter="url(#b12)"/>'
    if circled:
        o += '<path d="M66,150 C30,190 52,252 140,258 C232,262 262,214 246,172 C228,126 150,124 90,140" stroke="#9a2a2a" stroke-width="5" fill="none" stroke-opacity="0.85"/>'
    return o + '</g>'

def cheque(x, y, s=1.0, rot=0, torn=False, fill='#e9eee6'):
    """plain bank cheque, no legible bank name; amount line hand-filled"""
    o = f'<g transform="translate({x},{y}) rotate({rot}) scale({s})">'
    o += '<rect x="10" y="14" width="700" height="300" fill="#000" fill-opacity="0.3" filter="url(#b8)"/>'
    o += f'<rect x="0" y="0" width="700" height="300" fill="{fill}"/>'
    o += ''.join(f'<path d="M0,{yy} L700,{yy+20}" stroke="#a9c3c0" stroke-width="16" stroke-opacity="0.18"/>' for yy in range(-20, 320, 34))
    o += '<rect x="24" y="22" width="180" height="22" rx="3" fill="#7d9a9c" fill-opacity="0.55"/>'
    o += '<path d="M40,110 L560,110 M40,160 L520,160 M40,210 L380,210" stroke="#5f6f70" stroke-width="2" stroke-opacity="0.7"/>'
    o += '<rect x="520" y="182" width="160" height="46" fill="none" stroke="#5f6f70" stroke-width="2.4" stroke-opacity="0.8"/>'
    o += kalam(120, 104, 'Kabir Verma', 40, '#1f2f5a') + kalam(70, 154, 'एक लाख बीस हज़ार मात्र', 38, '#1f2f5a')
    o += kalam(532, 218, '1,20,000/-', 34, '#1f2f5a', weight=700)
    o += '<path d="M470,272 C500,250 530,286 560,262 C580,248 600,276 640,258" stroke="#1f2f5a" stroke-width="3" fill="none"/>'
    o += '<path d="M40,286 L300,286" stroke="#5f6f70" stroke-width="2" stroke-opacity="0.5" stroke-dasharray="3 5"/>'
    if torn:
        o += '<path d="M0,0 ' + ' '.join(f'L{-3 + (i%2)*4},{i*12}' for i in range(26)) + '" stroke="#bfc8c0" stroke-width="3" fill="none"/>'
    return o + '</g>'

def chequebook_stub(x, y, s=1.0, rot=0):
    o = f'<g transform="translate({x},{y}) rotate({rot}) scale({s})">'
    o += '<rect x="10" y="14" width="250" height="300" fill="#000" fill-opacity="0.35" filter="url(#b8)"/>'
    o += '<rect x="0" y="0" width="250" height="300" fill="#2f4a56"/><rect x="8" y="6" width="236" height="288" fill="#dfe6de"/>'
    o += '<path d="M24,80 L220,80 M24,130 L220,130 M24,180 L200,180" stroke="#5f6f70" stroke-width="2" stroke-opacity="0.6"/>'
    o += ''.join(f'<circle cx="246" cy="{yy}" r="2.4" fill="#8a9a96"/>' for yy in range(10, 296, 12))
    return o + '</g>'

def notice_back(x, y, w, h, rot=0, sums=True):
    """back of the bank notice: the pilot's ₹38,40,000 total faint at top, blank space for the new sum"""
    o = f'<g transform="translate({x},{y}) rotate({rot})">'
    o += f'<rect x="12" y="16" width="{w}" height="{h}" fill="#120c08" fill-opacity="0.45" filter="url(#b12)"/>'
    o += f'<rect width="{w}" height="{h}" fill="url(#paperw)"/>'
    # print-through of the front (mirrored grey lines)
    o += ''.join(f'<rect x="{w-60-(i*37)%140 - 300}" y="{90+i*44}" width="{300 + (i*53)%160}" height="12" fill="#6a6a70" fill-opacity="0.07"/>' for i in range(int(h/44) - 3))
    # tape corners
    for cx, cy in ((0, 0), (w, 0), (0, h), (w, h)):
        o += f'<rect x="{cx-36}" y="{cy-16}" width="72" height="32" fill="#efe6c8" fill-opacity="0.55" transform="rotate({35 if (cx==0)==(cy==0) else -35} {cx} {cy})"/>'
    if sums:
        o += kalam(w - 60, 120, '38,40,000', 40, '#5a5a62', anchor='end', op=0.5)
        o += f'<path d="M{w-300},140 L{w-60},140" stroke="#5a5a62" stroke-width="2" stroke-opacity="0.4"/>'
    return o + '</g>'

def page47(x, y, w, h, rot=0, pen=True):
    rnd = random.Random(47)
    o = f'<g transform="translate({x},{y}) rotate({rot})">'
    o += f'<rect x="12" y="16" width="{w}" height="{h}" fill="#120c08" fill-opacity="0.5" filter="url(#b12)"/>'
    o += f'<rect width="{w}" height="{h}" fill="url(#pagec)"/>'
    o += ''.join(f'<path d="M24,{yy} L{w-18},{yy}" stroke="#9fb2b6" stroke-width="2" stroke-opacity="0.65"/>' for yy in range(120, int(h) - 20, 56))
    o += f'<path d="M86,16 L86,{h-16}" stroke="#d08a8a" stroke-width="2.2" stroke-opacity="0.55"/>'
    o += kalam(30, 92, '47.', 48)
    # violent scratching over the name, paper torn in the middle
    cy = 214
    sc = ''.join(f'M{rnd.uniform(100,260):.0f},{cy + rnd.uniform(-70,70):.0f} L{rnd.uniform(w-300,w-50):.0f},{cy + rnd.uniform(-70,70):.0f} ' for _ in range(70)) + ''.join(f'M{rnd.uniform(120,w-80):.0f},{cy-80+rnd.uniform(-10,10):.0f} L{rnd.uniform(120,w-80):.0f},{cy+80+rnd.uniform(-10,10):.0f} ' for _ in range(18))
    o += f'<path d="{sc}" stroke="#1d1a2c" stroke-width="7" stroke-linecap="round" fill="none" stroke-opacity="0.9"/>'
    o += f'<path d="{sc}" stroke="#2a0e14" stroke-width="3" stroke-linecap="round" fill="none" stroke-opacity="0.5"/>'
    tear = f'M{w*0.36},{cy-10} L{w*0.42},{cy-26} L{w*0.5},{cy-8} L{w*0.58},{cy-30} L{w*0.64},{cy-6} L{w*0.6},{cy+20} L{w*0.5},{cy+12} L{w*0.42},{cy+24} Z'
    o += f'<path d="{tear}" fill="#2a1d14"/>'
    o += f'<path d="{tear}" fill="none" stroke="#f4ead2" stroke-width="3" stroke-opacity="0.8"/>'
    if pen:  # Papa's red pen, maroon (muted), lying across
        o += (f'<g transform="translate({w*0.18},{h*0.62}) rotate(-24)">'
              '<rect x="10" y="10" width="560" height="30" rx="14" fill="#000" fill-opacity="0.35" filter="url(#b6)"/>'
              '<rect x="0" y="0" width="520" height="28" rx="12" fill="#6a1e24"/><rect x="0" y="2" width="520" height="8" rx="4" fill="#fff" fill-opacity="0.2"/>'
              '<rect x="360" y="-6" width="12" height="40" rx="4" fill="#b9994e"/><path d="M520,2 L566,14 L520,26 Z" fill="#c0b8a8"/><path d="M556,11 L566,14 L556,17 Z" fill="#2a1a1a"/></g>')
    return o + '</g>'

def order_book(x, y, w, h, rot=0, name='मोहन लाल जी'):
    o = f'<g transform="translate({x},{y}) rotate({rot})">'
    o += f'<rect x="12" y="16" width="{w}" height="{h}" fill="#120c08" fill-opacity="0.45" filter="url(#b12)"/>'
    o += f'<rect x="-10" y="-10" width="{w+20}" height="{h+20}" rx="8" fill="#3d4a52"/>'
    o += f'<rect width="{w}" height="{h}" fill="url(#paperw)"/>'
    cols = [0, 0.14, 0.62, 0.8, 1.0]
    o += ''.join(f'<path d="M{w*c},{90} L{w*c},{h-10}" stroke="#7a8890" stroke-width="2.2" stroke-opacity="0.7"/>' for c in cols[1:-1])
    o += ''.join(f'<path d="M0,{yy} L{w},{yy}" stroke="#9aa8ae" stroke-width="1.8" stroke-opacity="0.7"/>' for yy in range(150, int(h) - 10, 64))
    o += f'<path d="M0,90 L{w},90" stroke="#5a6870" stroke-width="3"/>'
    o += kalam(w * 0.5, 66, name, 50, '#2a3a4a', anchor='middle', weight=700)
    return o + '</g>'

def scissors(x, y, s=1.0, rot=0):
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({s})">'
            '<path d="M0,-8 L300,-3 L300,3 L0,8 Z" fill="url(#chrome)"/><path d="M0,6 L290,22 L288,28 L0,14 Z" fill="url(#chrome)" fill-opacity="0.85"/>'
            '<circle cx="0" cy="4" r="9" fill="#5a5a60"/>'
            '<ellipse cx="-70" cy="-30" rx="60" ry="34" fill="none" stroke="#1d1d22" stroke-width="16"/><ellipse cx="-70" cy="44" rx="56" ry="32" fill="none" stroke="#1d1d22" stroke-width="16"/></g>')

def chalk(x, y, s=1.0, rot=0, col='#e8e2d4'):
    return f'<g transform="translate({x},{y}) rotate({rot}) scale({s})"><path d="M0,0 L80,-50 L110,-12 L30,38 Z" fill="{col}"/><path d="M0,0 L80,-50 L84,-44 L6,6 Z" fill="#fff" fill-opacity="0.5"/></g>'

def tape_coil(x, y, s=1.0):
    o = f'<g transform="translate({x},{y}) scale({s})">'
    for r_ in range(70, 10, -14):
        o += f'<circle r="{r_}" fill="none" stroke="#e2cf96" stroke-width="12"/><circle r="{r_}" fill="none" stroke="#3a3020" stroke-width="12" stroke-dasharray="2 10" stroke-opacity="0.5"/>'
    o += '<path d="M70,0 C140,20 220,10 320,60" stroke="#e2cf96" stroke-width="12" fill="none"/>'
    return o + '</g>'

def fabric(x, y, w, h, col, rot=0, folds=4, seed=1, op=1):
    rnd = random.Random(seed)
    pts = [(0, 0), (w * 0.3, -h * 0.04), (w * 0.7, h * 0.03), (w, 0), (w * 1.02, h * 0.4), (w, h), (w * 0.6, h * 1.03), (w * 0.2, h * 0.98), (-w * 0.02, h * 0.6)]
    o = f'<g transform="translate({x},{y}) rotate({rot})" opacity="{op}">'
    o += f'<path d="{cr_path(pts)}" fill="#000" fill-opacity="0.35" filter="url(#b12)" transform="translate(10,14)"/>'
    o += f'<path d="{cr_path(pts)}" fill="{col}"/>'
    for k in range(folds):
        xx = w * (k + 1) / (folds + 1) + rnd.uniform(-w * 0.05, w * 0.05)
        o += f'<path d="M{xx},{h*0.05} C{xx + rnd.uniform(-40,40)},{h*0.4} {xx + rnd.uniform(-40,40)},{h*0.7} {xx + rnd.uniform(-30,30)},{h*0.96}" stroke="#000" stroke-opacity="0.2" stroke-width="14" fill="none" filter="url(#b6)"/>'
        o += f'<path d="M{xx+12},{h*0.05} C{xx + rnd.uniform(-40,40)+12},{h*0.4} {xx + 12},{h*0.7} {xx + 12},{h*0.96}" stroke="#fff" stroke-opacity="0.12" stroke-width="6" fill="none" filter="url(#b4)"/>'
    return o + '</g>'

def worker(x, y, s=1.0, flip=False, fill='#231c18', rim='#f6d39c', dup=True, bun=False, seed=1):
    """young woman at a machine, seated, upper body only (table hides the rest). Faces LEFT.
    (x,y) = point where her forearms meet the table top."""
    o = []
    body = (f'M60,0 C40,-40 34,-110 40,-170 C46,-220 70,-250 104,-262 C120,-268 132,-274 134,-290 '
            f'C120,-300 112,-318 112,-338 C112,-372 136,-396 168,-396 C200,-396 222,-372 222,-340 C222,-316 210,-298 194,-290 '
            f'C198,-276 214,-266 236,-258 C276,-240 292,-200 294,-150 L300,0 Z')
    arm = 'M100,-232 C70,-190 40,-120 20,-60 L-60,-14 C-70,-8 -66,6 -54,6 L4,4 C30,-2 44,-20 56,-50 C76,-100 108,-160 132,-200 Z'
    face = 'M118,-352 C108,-344 104,-334 106,-326 L100,-318 C104,-314 108,-312 110,-310 C108,-304 110,-298 116,-296 C122,-290 130,-290 134,-292 Z'
    o.append(f'<path d="{body}" fill="{rim}" transform="translate(-4,-2)"/><path d="{arm}" fill="{rim}" transform="translate(-4,-2)"/>')
    o.append(f'<path d="{body}" fill="{fill}"/><path d="{arm}" fill="{fill}"/><path d="{face}" fill="{fill}"/>')
    if dup:
        o.append(f'<path d="M116,-360 C126,-404 196,-418 226,-372 C240,-340 246,-290 270,-250 C300,-200 310,-120 300,0 L250,0 C262,-100 250,-200 214,-262 C200,-290 196,-330 170,-356 C150,-372 130,-372 116,-360 Z" fill="{fill}"/>')
        o.append(f'<path d="M118,-362 C132,-400 196,-410 222,-372" stroke="{rim}" stroke-width="3" fill="none" stroke-opacity="0.7"/>')
    if bun:
        o.append(f'<circle cx="214" cy="-356" r="24" fill="{fill}"/>')
    sx = -s if flip else s
    return f'<g transform="translate({x},{y}) scale({sx},{s})">{"".join(o)}</g>'

def kabir_back(x, y, s=1.0, shirt='#55708a', shirt_lo='#3d5468', rim='#f3d39e', hair='#0f0c0a', skin='#5a3a28'):
    """Kabir from behind, head and shoulders (back view). (x,y)= nape; ~620*s wide"""
    o = (f'<g transform="translate({x},{y}) scale({s})">'
         f'<path d="M-300,420 C-300,240 -260,170 -150,140 C-90,124 -60,110 -56,70 L56,70 C60,110 90,124 150,140 C260,170 300,240 300,420 Z" fill="{rim}" transform="translate(0,-4)"/>'
         f'<path d="M-300,420 C-300,240 -260,170 -150,140 C-90,124 -60,110 -56,70 L56,70 C60,110 90,124 150,140 C260,170 300,240 300,420 Z" fill="{shirt}"/>'
         f'<path d="M-300,420 C-300,260 -270,190 -180,154 C-200,240 -210,320 -200,420 Z" fill="{shirt_lo}" fill-opacity="0.6"/>'
         f'<path d="M-70,96 C-40,120 40,120 70,96 L64,124 C30,140 -30,140 -64,124 Z" fill="{shirt_lo}"/>'
         f'<path d="M0,128 L0,420" stroke="{shirt_lo}" stroke-width="4" stroke-opacity="0.5"/>'
         f'<path d="M-50,100 L-48,40 L48,40 L50,100 Z" fill="{skin}"/>'
         f'<ellipse cx="-104" cy="-36" rx="20" ry="34" fill="{skin}"/><ellipse cx="104" cy="-36" rx="20" ry="34" fill="{skin}"/>'
         f'<path d="M-100,-40 C-110,-140 -60,-196 0,-198 C60,-196 110,-140 100,-40 C96,0 70,40 0,52 C-70,40 -96,0 -100,-40 Z" fill="{hair}"/>'
         f'<path d="M-100,-40 C-110,-140 -60,-196 0,-198 C40,-196 70,-180 88,-150" stroke="{rim}" stroke-width="5" fill="none" stroke-opacity="0.6"/>'
         + ''.join(f'<path d="M{-80+i*16},{-150+abs(i-5)*6} l6,-14" stroke="#2a2420" stroke-width="3"/>' for i in range(11)) +
         '</g>')
    return o

def trunk_open(x, y, s=1.0):
    """blue-green tin trunk, lid up, folded khaki uniform inside, brass bell on top of it (dome only)"""
    o = f'<g transform="translate({x},{y}) scale({s})">'
    o += '<path d="M-330,-420 L330,-420 L360,-660 L-360,-660 Z" fill="#3f6461"/><path d="M-330,-420 L330,-420 L336,-470 L-336,-470 Z" fill="#2c4a48"/>'
    o += '<path d="M-300,-440 L300,-440 L322,-630 L-322,-630 Z" fill="#2a3a36" fill-opacity="0.6"/>'
    o += '<rect x="-340" y="-420" width="680" height="380" rx="10" fill="#4a7470"/><rect x="-340" y="-420" width="680" height="40" fill="#2e4c4a"/>'
    o += '<rect x="-318" y="-400" width="636" height="70" fill="#1e2a28"/>'
    # folded khaki uniform inside (top visible)
    o += '<path d="M-300,-404 C-200,-430 200,-430 300,-404 L300,-340 L-300,-340 Z" fill="url(#khaki)"/>'
    o += '<path d="M-60,-424 L0,-380 L60,-424" stroke="#5a4a30" stroke-width="5" fill="none"/><circle cx="0" cy="-366" r="6" fill="#c9b06a"/>'
    # rust & dents
    o += ''.join(f'<ellipse cx="{-300+i*97}" cy="{-80 - (i*37)%120}" rx="{30 + (i*13)%30}" ry="{12 + (i*7)%10}" fill="#7a4a2a" fill-opacity="0.35" filter="url(#b4)"/>' for i in range(7))
    o += '<rect x="-30" y="-404" width="60" height="70" rx="6" fill="#b48a3a"/><rect x="-14" y="-380" width="28" height="30" rx="4" fill="#6a4a1a"/>'
    o += '<path d="M-340,-200 L340,-200" stroke="#2e4c4a" stroke-width="10"/>'
    o += '</g>'
    return o

def door_frame_lit(x, y, w, h, light='#f6e6c4'):
    return R(x, y, w, h, light) + R(x - 30, y - 30, 30, h + 30, '#3a2c20') + R(x + w, y - 30, 30, h + 30, '#3a2c20') + R(x - 30, y - 30, w + 60, 30, '#3a2c20')
