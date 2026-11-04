# Ep6 hand system: anatomically proportioned dorsal hands (seen from above), built from bones.
# Local units: palm width at knuckles = 100. Wrist centre at (0,0); fingers point toward -y.
# side='R' right hand (thumb on viewer-left when the back of the hand faces the viewer), 'L' mirrored.
import math, sys
sys.path.insert(0, '/home/claude/udhaar/scripts')
from shapes import cr_path

_uid = [0]
def _id(p): _uid[0] += 1; return f'{p}{_uid[0]}'

# MCP knuckle base (x,y), length, base width, splay angle (deg, + toward little finger side)
FINGERS = {
    'index':  ((-33, -100), 86, 23.5, -5),
    'middle': ((-10, -105), 96, 24.5, 0),
    'ring':   ((13, -102), 90, 23.0, 5),
    'little': ((34, -93), 70, 19.5, 11),
}
SEG = (0.46, 0.30, 0.24)   # proximal, middle, distal share of length

def _rot(x, y, a):
    c, s = math.cos(a), math.sin(a); return (x * c - y * s, x * s + y * c)

def _finger(base, L, w, ang, curl, spread):
    """returns outline polygon, joint list, nail polygon (or None), tip point"""
    bx, by = base
    a = math.radians(ang + spread)
    # direction pointing up (-y) rotated by a (positive -> +x)
    d = (math.sin(a), -math.cos(a)); n = (-d[1], d[0])  # n points to +x side-ish
    cs = curl if isinstance(curl, (list, tuple)) else (curl, curl, curl)
    pts = [(bx, by)]; widths = [w]
    x, y = bx, by; ww = w
    fore = []
    for k, sh in enumerate(SEG):
        f = max(0.22, math.cos(math.radians(cs[k] * 85)))  # foreshortening seen from above
        seg = L * sh * f
        x += d[0] * seg; y += d[1] * seg
        ww = ww * (0.93 if k < 2 else 0.9)
        pts.append((x, y)); widths.append(ww); fore.append(f)
    # outline: left side up, round tip, right side down
    left = [(px - n[0] * wd / 2, py - n[1] * wd / 2) for (px, py), wd in zip(pts, widths)]
    right = [(px + n[0] * wd / 2, py + n[1] * wd / 2) for (px, py), wd in zip(pts, widths)]
    # joint bulges (slightly wider at PIP/DIP)
    for i in (1, 2):
        bul = 0.9
        left[i] = (left[i][0] - n[0] * bul, left[i][1] - n[1] * bul)
        right[i] = (right[i][0] + n[0] * bul, right[i][1] + n[1] * bul)
    tx, ty = pts[-1]; tw = widths[-1]
    tip = [(tx - n[0] * tw * 0.42 + d[0] * tw * 0.32, ty - n[1] * tw * 0.42 + d[1] * tw * 0.32),
           (tx + d[0] * tw * 0.52, ty + d[1] * tw * 0.52),
           (tx + n[0] * tw * 0.42 + d[0] * tw * 0.32, ty + n[1] * tw * 0.42 + d[1] * tw * 0.32)]
    # extend base down into palm so it merges
    bl = (left[0][0] - d[0] * 18, left[0][1] - d[1] * 18); br = (right[0][0] - d[0] * 18, right[0][1] - d[1] * 18)
    poly = [bl] + left + tip + list(reversed(right)) + [br]
    nail = None
    if fore[2] > 0.55:
        # nail on distal segment (dorsal)
        p0 = pts[2]; p1 = pts[3]; nl = math.dist(p0, p1)
        c0 = (p0[0] + (p1[0] - p0[0]) * 0.34, p0[1] + (p1[1] - p0[1]) * 0.34)
        nw = widths[3] * 0.62
        nail = [(c0[0] - n[0] * nw / 2, c0[1] - n[1] * nw / 2),
                (c0[0] + n[0] * nw / 2, c0[1] + n[1] * nw / 2),
                (p1[0] + n[0] * nw * 0.5 + d[0] * tw * 0.36, p1[1] + n[1] * nw * 0.5 + d[1] * tw * 0.36),
                (p1[0] + d[0] * tw * 0.5, p1[1] + d[1] * tw * 0.5),
                (p1[0] - n[0] * nw * 0.5 + d[0] * tw * 0.36, p1[1] - n[1] * nw * 0.5 + d[1] * tw * 0.36)]
    return poly, pts, widths, nail, d, n, fore

def hand(x, y, rot=0, sc=1.0, side='R', curl=None, spread=0.0, thumb=(1.0, 0.0),
         skin='#8a5a3e', hi='#b47e5a', lo='#4a2c1d', nail='#d9b8a0', sleeve=None, sleeve_rim=None,
         bangles=None, band=None, shadow=0.45, age=0.0, forearm=230, cuff_w=118, extra=''):
    """curl: dict finger->curl 0..1 (or (p,m,d)); thumb=(extension 0..1, angle offset deg)
    sleeve: fill colour for a shirt cuff/sleeve over the forearm; bangles: list of colours."""
    curl = curl or {}
    m = 1 if side == 'R' else -1
    gid = _id('hsk')
    o = []
    defs = (f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{hi}"/><stop offset="0.55" stop-color="{skin}"/><stop offset="1" stop-color="{lo}"/></linearGradient>')
    fill = f'url(#{gid})'
    parts = []
    # forearm (extends to +y beyond wrist)
    fa = [(-34, 6), (-40, forearm * 0.5), (-44, forearm), (44, forearm), (40, forearm * 0.5), (34, 6)]
    parts.append(f'<path d="{cr_path(fa)}" fill="{fill}"/>')
    # palm (back of hand)
    palm = [(-36, 0), (-44, -30), (-47, -62), (-45, -92), (-34, -108), (-12, -114), (12, -111), (32, -103),
            (45, -88), (47, -60), (44, -28), (36, 0)]
    parts.append(f'<path d="{cr_path(palm)}" fill="{fill}"/>')
    # thumb: CMC at (-40,-28); points up-left
    te, toff = thumb
    ta = math.radians(-32 + toff)
    td = (math.sin(ta), -math.cos(ta)); tn = (-td[1], td[0])
    tb = (-40, -30)
    L1, L2 = 52 * (0.55 + 0.45 * te), 40 * (0.5 + 0.5 * te)
    j1 = (tb[0] + td[0] * L1, tb[1] + td[1] * L1)
    ta2 = ta + math.radians(8)
    td2 = (math.sin(ta2), -math.cos(ta2)); tn2 = (-td2[1], td2[0])
    j2 = (j1[0] + td2[0] * L2, j1[1] + td2[1] * L2)
    w0, w1, w2 = 34, 26, 22
    th = [(tb[0] + tn[0] * w0 / 2 + 10, tb[1] + tn[1] * w0 / 2 + 6),
          (j1[0] + tn[0] * w1 / 2, j1[1] + tn[1] * w1 / 2),
          (j2[0] + tn2[0] * w2 / 2, j2[1] + tn2[1] * w2 / 2),
          (j2[0] + td2[0] * w2 * 0.5, j2[1] + td2[1] * w2 * 0.5),
          (j2[0] - tn2[0] * w2 / 2, j2[1] - tn2[1] * w2 / 2),
          (j1[0] - tn[0] * w1 / 2 - 2, j1[1] - tn[1] * w1 / 2),
          (tb[0] - tn[0] * w0 / 2, tb[1] - tn[1] * w0 / 2),
          (-30, 10)]
    if te > 0.05:
        parts.append(f'<path d="{cr_path(th)}" fill="{fill}"/>')
        # web between thumb and index
        web = [(j1[0] + 4, j1[1] + 2), (-36, -84), (-30, -60), (-30, -30)]
        parts.append(f'<path d="{cr_path(web)}" fill="{fill}"/>')
    det = []
    tips = {}
    order = ['little', 'ring', 'middle', 'index']
    fdata = {}
    for nm in order:
        base, L, w, ang = FINGERS[nm]
        c = curl.get(nm, 0.0)
        sp = spread * {'index': -1.0, 'middle': -0.2, 'ring': 0.6, 'little': 1.3}[nm]
        poly, pts, widths, nl, d, n, fore = _finger(base, L, w, ang, c, sp)
        fdata[nm] = (poly, pts, widths, nl, d, n, fore)
        parts.append(f'<path d="{cr_path(poly)}" fill="{fill}"/>')
        tips[nm] = pts[-1]
    # ---- details (unit coords) ----
    for nm in order:
        poly, pts, widths, nl, d, n, fore = fdata[nm]
        # knuckle (MCP) highlight
        bx, by = pts[0]
        det.append(f'<ellipse cx="{bx + d[0]*4:.1f}" cy="{by + d[1]*4:.1f}" rx="{widths[0]*0.34:.1f}" ry="{widths[0]*0.22:.1f}" fill="{hi}" fill-opacity="0.22"/>')
        # PIP & DIP creases
        for k in (1, 2):
            if fore[k - 1] < 0.3: continue
            px, py = pts[k]; wd = widths[k] * 0.38
            for j, off in enumerate((-2.2, 0.6, 3.2) if k == 1 else (-1.0, 1.4)):
                cx, cy = px + d[0] * off, py + d[1] * off
                op = 0.55 if j == 1 else 0.35
                det.append(f'<path d="M{cx - n[0]*wd:.1f},{cy - n[1]*wd:.1f} Q{cx + d[0]*1.8:.1f},{cy + d[1]*1.8:.1f} {cx + n[0]*wd:.1f},{cy + n[1]*wd:.1f}" stroke="{lo}" stroke-width="{1.1 + age*0.4:.2f}" fill="none" stroke-opacity="{op}"/>')
        # curled finger knuckle tops
        if fore[0] < 0.5:
            px, py = pts[1]
            det.append(f'<ellipse cx="{px:.1f}" cy="{py:.1f}" rx="{widths[1]*0.42:.1f}" ry="{widths[1]*0.3:.1f}" fill="{hi}" fill-opacity="0.5"/>')
        # nail
        if nl:
            det.append(f'<path d="{cr_path(nl)}" fill="{nail}" fill-opacity="0.85"/>')
            det.append(f'<path d="{cr_path(nl)}" fill="none" stroke="{lo}" stroke-width="0.8" stroke-opacity="0.35"/>')
        # light edge on thumb-side of each finger
        if fore[0] > 0.5:
            p0 = pts[0]; p1 = pts[-1]; w0_ = widths[0]
            det.append(f'<path d="M{p0[0] - n[0]*w0_*0.36:.1f},{p0[1] - n[1]*w0_*0.36:.1f} L{p1[0] - n[0]*widths[-1]*0.34:.1f},{p1[1] - n[1]*widths[-1]*0.34:.1f}" stroke="{hi}" stroke-width="2.2" stroke-opacity="0.35" stroke-linecap="round"/>')
    # separations between adjacent fingers near the base
    for a_, b_ in (('index', 'middle'), ('middle', 'ring'), ('ring', 'little')):
        pa = fdata[a_][1]; pb = fdata[b_][1]
        s0 = ((pa[0][0] + pb[0][0]) / 2, (pa[0][1] + pb[0][1]) / 2 + 2)
        s1 = ((pa[1][0] + pb[1][0]) / 2, (pa[1][1] + pb[1][1]) / 2)
        s1 = (s0[0] + (s1[0] - s0[0]) * 0.55, s0[1] + (s1[1] - s0[1]) * 0.55)
        det.append(f'<path d="M{s0[0]:.1f},{s0[1]:.1f} L{s1[0]:.1f},{s1[1]:.1f}" stroke="{lo}" stroke-width="2.2" stroke-opacity="0.55" stroke-linecap="round"/>')
    # tendons fanning from wrist to knuckles
    for nm in order:
        bx, by = fdata[nm][1][0]
        det.append(f'<path d="M{bx*0.25:.1f},-6 Q{bx*0.6:.1f},{by*0.5:.1f} {bx:.1f},{by + 10:.1f}" stroke="{hi}" stroke-width="2" fill="none" stroke-opacity="{0.10 + age*0.10:.2f}"/>')
    if age > 0.3:
        det.append(f'<path d="M-6,-20 C-2,-40 6,-56 4,-78 M14,-30 C18,-50 20,-64 18,-86" stroke="{lo}" stroke-width="2.2" fill="none" stroke-opacity="0.3"/>')
        for sx, sy in ((-14, -50), (8, -62), (22, -40)):
            det.append(f'<ellipse cx="{sx}" cy="{sy}" rx="3" ry="2.2" fill="{lo}" fill-opacity="0.18"/>')
    # thumb nail & crease
    if te > 0.4:
        det.append(f'<ellipse cx="{j2[0] + td2[0]*2:.1f}" cy="{j2[1] + td2[1]*2:.1f}" rx="7" ry="9" transform="rotate({math.degrees(ta2):.1f} {j2[0] + td2[0]*2:.1f} {j2[1] + td2[1]*2:.1f})" fill="{nail}" fill-opacity="0.8"/>')
        det.append(f'<path d="M{j1[0] - tn[0]*8:.1f},{j1[1] - tn[1]*8:.1f} Q{j1[0] + td[0]*2:.1f},{j1[1] + td[1]*2:.1f} {j1[0] + tn[0]*8:.1f},{j1[1] + tn[1]*8:.1f}" stroke="{lo}" stroke-width="1.2" fill="none" stroke-opacity="0.45"/>')
    # wrist crease shading
    det.append(f'<path d="M-36,2 Q0,10 36,2" stroke="{lo}" stroke-width="3" fill="none" stroke-opacity="0.25"/>')
    # shadow side of hand (little-finger edge)
    det.append(f'<path d="M44,-28 C48,-60 46,-88 34,-100 L40,-96 C50,-80 52,-50 46,-20 Z" fill="{lo}" fill-opacity="0.35"/>')
    # accessories on forearm
    acc = []
    if band:  # hospital id band
        acc.append(f'<rect x="-42" y="20" width="84" height="16" rx="5" fill="{band}"/><rect x="-14" y="22" width="26" height="12" rx="2" fill="#ffffff" fill-opacity="0.6"/>')
    if bangles:
        for i, bc in enumerate(bangles):
            yy = 26 + i * 9
            acc.append(f'<path d="M-46,{yy} Q0,{yy + 12} 46,{yy}" stroke="{bc}" stroke-width="6.5" fill="none" stroke-linecap="round"/>')
            acc.append(f'<path d="M-40,{yy - 1.5} Q0,{yy + 9} 40,{yy - 1.5}" stroke="#fff6dc" stroke-width="1.4" fill="none" stroke-opacity="0.45"/>')
    if sleeve:
        sr = sleeve_rim or sleeve
        sy0 = 34 if not bangles else 26 + len(bangles) * 9 + 10
        cw = cuff_w / 2
        sl = [(-cw, sy0 + 6), (-cw - 8, forearm + 40), (cw + 8, forearm + 40), (cw, sy0 + 6), (0, sy0 - 4)]
        acc.append(f'<path d="{cr_path(sl)}" fill="{sleeve}"/>')
        acc.append(f'<path d="M{-cw},{sy0 + 6} Q0,{sy0 - 6} {cw},{sy0 + 6}" stroke="{sr}" stroke-width="5" fill="none" stroke-opacity="0.8"/>')
        acc.append(f'<path d="M{-cw + 6},{sy0 + 22} Q0,{sy0 + 12} {cw - 6},{sy0 + 22}" stroke="#000" stroke-width="2" fill="none" stroke-opacity="0.18"/>')
    body = ''.join(parts)
    sh = ''
    if shadow:
        sh = f'<g transform="translate({x + 14 * sc},{y + 22 * sc}) rotate({rot}) scale({m * sc},{sc})" filter="url(#b12)" opacity="{shadow}">{body.replace(fill, "#120c08")}</g>'
    grp = f'<g transform="translate({x},{y}) rotate({rot}) scale({m * sc},{sc})">{body}{"".join(det)}{"".join(acc)}{extra}</g>'
    return f'<defs>{defs}</defs>' + sh + grp

# convenient poses
FLAT = {}
RELAXED = {'index': (0.12, 0.1, 0.05), 'middle': (0.15, 0.12, 0.08), 'ring': (0.2, 0.15, 0.1), 'little': (0.25, 0.2, 0.12)}
POINT = {'index': 0.0, 'middle': (0.86, 0.9, 0.9), 'ring': (0.88, 0.9, 0.9), 'little': (0.9, 0.9, 0.9)}
GRIP = {'index': (0.3, 0.45, 0.3), 'middle': (0.35, 0.5, 0.35), 'ring': (0.4, 0.5, 0.35), 'little': (0.45, 0.5, 0.35)}
PENCIL = {'index': (0.25, 0.35, 0.2), 'middle': (0.6, 0.7, 0.5), 'ring': (0.82, 0.88, 0.8), 'little': (0.86, 0.9, 0.85)}
