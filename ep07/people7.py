# Ep7 people: Ma (Sudha) lit profile (pilot s30 construction, locked design) and Bablu "Hero" (48).
import sys, math
sys.path.insert(0, '/home/claude/udhaar/scripts'); sys.path.insert(0, '/home/claude/udhaar/ep06')
from shapes import cr_path, mirror_x, MA_L, MA_PALLU_L, KABIR_PROFILE, KABIR_HAIR

_u = [0]
def _id(p): _u[0] += 1; return f'{p}{_u[0]}'

def ma_lit(look=0, lids=0.0, flip=False, pallu_hi='#d8d0bd'):
    """Ma, facing RIGHT (as pilot s30): white widow's pallu over her head, no bindi, warm side light.
    lids 0..1 lowers the eyelid; look shifts the iris (+ = further right). flip=True faces LEFT."""
    gs, gp = _id('mskin'), _id('mpal')
    d = (f'<defs><linearGradient id="{gs}" x1="1" y1="0" x2="0" y2="0"><stop offset="0.1" stop-color="#a87554"/><stop offset="0.55" stop-color="#6a4330"/><stop offset="1" stop-color="#2a1a12"/></linearGradient>'
         f'<linearGradient id="{gp}" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="{pallu_hi}"/><stop offset="0.5" stop-color="#a49c89"/><stop offset="1" stop-color="#4f4b43"/></linearGradient></defs>')
    face = cr_path(mirror_x(MA_L)); pal = cr_path(mirror_x(MA_PALLU_L))
    ey = 371
    o = d + f'<path d="{face}" fill="url(#{gs})"/><path d="{pal}" fill="url(#{gp})"/>'
    o += f'<path d="M770,{ey-1} C756,{ey-11} 738,{ey-11} 724,{ey-1} C738,{ey+9} 756,{ey+9} 770,{ey-1} Z" fill="#e4d2ba"/>'
    o += f'<ellipse cx="{760+look}" cy="{ey+lids*2}" rx="7" ry="{7-lids*3}" fill="#1a110c"/>'
    if lids < 0.6: o += f'<circle cx="{762+look}" cy="{ey-3}" r="2" fill="#fff"/>'
    o += f'<path d="M772,{ey-2+lids*3} C756,{ey-14+lids*9} 738,{ey-14+lids*9} 722,{ey-2+lids*3} L722,{ey-12} C740,{ey-20} 758,{ey-20} 772,{ey-12} Z" fill="#7a4e36" fill-opacity="{min(1,lids*1.3)}"/>'
    o += f'<path d="M778,{ey-11+lids*6} C760,{ey-21+lids*8} 740,{ey-21+lids*8} 720,{ey-11+lids*6}" stroke="#2a1a12" stroke-width="4" fill="none"/>'
    o += ('<path d="M786,336 C764,322 738,322 714,332" stroke="#3a2a20" stroke-width="7" fill="none" stroke-linecap="round"/>'
          '<path d="M790,330 C800,322 806,312 808,300" stroke="#2a1a12" stroke-width="3" fill="none" stroke-opacity="0.6"/>'
          '<path d="M770,395 C760,402 748,404 736,400" stroke="#5a3a28" stroke-width="2.5" fill="none" stroke-opacity="0.6"/>'
          '<path d="M796,528 C786,532 776,532 766,528" stroke="#4a2a1e" stroke-width="3.5" fill="none"/>'
          '<path d="M700,230 C680,250 660,280 650,320" stroke="#7a7266" stroke-width="10" fill="none" stroke-opacity="0.5"/>'
          '<path d="M660,250 C700,236 740,232 780,238" stroke="#3a3632" stroke-width="12" fill="none" stroke-opacity="0.55"/>')
    if flip: o = f'<g transform="translate(1120,0) scale(-1,1)">{o}</g>'
    return o

BABLU_FACE = [(x * 1.06 - 20, y) for x, y in KABIR_PROFILE]
def bablu(flip=False, mouth='smile', shirt='#8a7444', motif='#5a3e2a', brows=0, eye='open', gleam=1.0):
    """Bablu 'Hero', 48: stocky, oiled pompadour that shines, thin moustache, loud printed shirt (muted). Faces LEFT."""
    gid = _id('bsk')
    pts = list(BABLU_FACE)
    # fuller cheek/jaw & double chin
    pts = [(x - 6, y + 10) if 19 <= i <= 22 else (x, y) for i, (x, y) in enumerate(pts)]
    face = cr_path(pts)
    o = [f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0.12" stop-color="#b47e58"/><stop offset="0.55" stop-color="#7a4e34"/><stop offset="1" stop-color="#3a2418"/></linearGradient></defs>']
    o.append(f'<path d="{face}" fill="url(#{gid})"/>')
    # double chin + jowl
    o.append('<path d="M360,640 C380,690 430,712 480,708 C452,690 420,672 400,650 Z" fill="#6a4230" fill-opacity="0.22"/>')
    # printed shirt, wide collar
    sh = [(400, 790), (520, 820), (640, 830), (740, 800), (840, 850), (960, 920), (1080, 990), (1150, 1060), (1150, 1520), (300, 1520), (318, 1260), (340, 1060), (370, 900)]
    o.append(f'<path d="{cr_path(sh)}" fill="{shirt}"/>')
    o.append(''.join(f'<path d="M{x},{y} c14,-18 34,-10 30,8 c-4,18 -26,22 -36,10 z" fill="{motif}" fill-opacity="0.75"/><circle cx="{x+40}" cy="{y+40}" r="7" fill="#c9b27a" fill-opacity="0.6"/>'
                     for x in range(330, 1150, 90) for y in range(880 + (x % 180) // 3, 1520, 110)))
    o.append('<path d="M410,800 L520,900 L560,830 Z M760,806 L700,920 L650,830 Z" fill="#c9b27a" fill-opacity="0.85"/>')
    o.append('<path d="M410,800 L520,900 L560,830 M760,806 L700,920 L650,830" stroke="#3a2a18" stroke-width="4" fill="none" stroke-opacity="0.6"/>')
    # eye, brow (expressive), nose, moustache, mouth
    by = -brows * 10
    if eye == 'open':
        o.append('<path d="M344,380 C356,370 374,370 386,380 C374,390 356,390 344,380 Z" fill="#ead6bc"/><ellipse cx="354" cy="380" rx="7.5" ry="8" fill="#1d130e"/><circle cx="352" cy="377" r="2.2" fill="#fff4dc"/>')
    else:  # squeezed (mid-impression)
        o.append('<path d="M342,382 C356,376 374,376 388,382" stroke="#1d130e" stroke-width="5" fill="none" stroke-linecap="round"/>')
    o.append(f'<path d="M332,{350+by} C352,{336+by*1.4} 380,{336+by*1.4} 402,{346+by}" stroke="#140d09" stroke-width="11" fill="none" stroke-linecap="round"/>')
    o.append('<path d="M300,496 C306,488 316,488 320,496" stroke="#3a2418" stroke-width="4" fill="none"/>')
    o.append('<path d="M300,524 C316,514 338,516 352,528 C338,532 316,532 300,530 Z" fill="#1a110c"/>')
    if mouth == 'smile':
        o.append('<path d="M314,548 C326,560 342,560 354,550" stroke="#4a2a1e" stroke-width="4" fill="none"/>')
    elif mouth == 'open':
        o.append('<path d="M312,544 C320,566 344,570 356,550 Z" fill="#3a1a14"/>')
    else:
        o.append('<path d="M316,548 C326,550 340,550 350,548" stroke="#4a2a1e" stroke-width="4" fill="none"/>')
    o.append('<path d="M610,420 C645,405 668,440 656,482 C646,520 620,524 606,506 Z" fill="#6a4230"/><path d="M622,440 C640,436 648,460 640,482" stroke="#3a2418" stroke-width="4" fill="none"/>')
    # oiled pompadour: high puff at the front, combed back, shining
    hair = [(330, 300), (318, 248), (330, 196), (366, 150), (420, 118), (500, 100), (580, 104), (650, 128), (708, 170), (748, 230),
            (770, 310), (774, 400), (760, 470), (734, 520), (704, 470), (680, 400), (640, 380), (600, 386), (584, 440), (566, 440),
            (552, 360), (520, 300), (460, 268), (400, 262)]
    o.append(f'<path d="{cr_path(hair)}" fill="#0c0908"/>')
    o.append(f'<path d="M346,210 C400,150 500,128 600,142 C660,152 710,190 740,250" stroke="#f6e2b8" stroke-width="10" fill="none" stroke-opacity="{0.75*gleam}" stroke-linecap="round"/>')
    o.append(f'<path d="M380,240 C440,196 520,184 590,196" stroke="#ffffff" stroke-width="5" fill="none" stroke-opacity="{0.6*gleam}" stroke-linecap="round"/>')
    o.append(''.join(f'<path d="M{430+i*40},{150+i*4} C{470+i*40},{170+i*6} {520+i*40},{200+i*8} {560+i*40},{250+i*10}" stroke="#3a3028" stroke-width="3" fill="none" stroke-opacity="0.7"/>' for i in range(6)))
    s = ''.join(o)
    if flip: s = f'<g transform="translate(1120,0) scale(-1,1)">{s}</g>'
    return s

def joined_palms(x, y, s=1.0, skin='#8a5a3e', lo='#4a2c1d', sleeve='#8a7444'):
    """namaste seen in profile: palms pressed, fingertips up; wrists at (x,y)"""
    return (f'<g transform="translate({x},{y}) scale({s})">'
            f'<path d="M-60,40 C-50,-10 -40,-60 -30,-110 L40,-110 C50,-50 60,0 70,40 Z" fill="{sleeve}"/>'
            f'<path d="M-20,-100 C-34,-150 -36,-210 -24,-260 C-16,-296 -2,-318 8,-322 C16,-318 22,-300 24,-270 C30,-220 34,-160 30,-100 Z" fill="{skin}"/>'
            f'<path d="M4,-318 C6,-260 6,-180 4,-104" stroke="{lo}" stroke-width="3" fill="none" stroke-opacity="0.7"/>'
            f'<path d="M-28,-170 C-40,-180 -46,-200 -40,-214 C-32,-206 -26,-190 -22,-176 Z" fill="{skin}"/>'
            f'<path d="M-30,-160 C-38,-150 -40,-130 -34,-116" stroke="{lo}" stroke-width="2.5" fill="none" stroke-opacity="0.6"/>'
            + ''.join(f'<path d="M{-22+k*3},{-230+k*26} q10,4 20,0" stroke="{lo}" stroke-width="2" fill="none" stroke-opacity="0.5"/>' for k in range(3)) +
            '</g>')

def fist(x, y, s=1.0, rot=0, skin='#8a5a3e', hi='#b47e5a', lo='#4a2c1d', sleeve='#8a7444', arm=260):
    """loose fist seen from the side, knuckles up/forward; wrist at (x,y), forearm going down (+y)"""
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({s})">'
            f'<path d="M-36,0 L-44,{arm} L48,{arm} L38,0 Z" fill="{sleeve}"/>'
            f'<path d="M-34,10 C-44,-20 -46,-60 -30,-86 C-14,-108 22,-110 42,-92 C60,-74 62,-40 54,-14 C48,6 30,14 -34,10 Z" fill="{skin}"/>'
            f'<path d="M-30,-86 C-14,-108 22,-110 42,-92" stroke="{hi}" stroke-width="6" fill="none" stroke-opacity="0.6"/>'
            + ''.join(f'<path d="M{-28+k*20},{-88+abs(k-1.5)*4} C{-24+k*20},{-70} {-22+k*20},{-50} {-24+k*20},{-30}" stroke="{lo}" stroke-width="2.4" fill="none" stroke-opacity="0.55"/>' for k in range(1, 4)) +
            f'<path d="M-34,-30 C-50,-36 -56,-56 -46,-70 C-36,-64 -32,-50 -30,-40 Z" fill="{skin}"/>'
            f'<path d="M-36,4 L38,4" stroke="{lo}" stroke-width="3" stroke-opacity="0.3"/>'
            '</g>')
