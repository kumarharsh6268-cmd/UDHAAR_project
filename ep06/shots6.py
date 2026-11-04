# Episode 6 "Bahattar Hazaar" — every shot as an SVG generator.  usage: python3 shots6.py OUTDIR [ids...]
import sys, math, random
sys.path.insert(0, '/home/claude/udhaar/scripts'); sys.path.insert(0, '/home/claude/udhaar/ep06')
from art import *
from shapes import *
from props6 import *
from hands6 import hand, FLAT, RELAXED, POINT, GRIP, PENCIL
from people6 import rukhsana, gauri, kabir_eyes_down

BLUE, BLUE_RIM = '#55708a', '#9fb6c8'          # Kabir's faded blue shirt
COAT, COAT_RIM = '#dfe3e0', '#ffffff'          # Gauri's white coat
KAMEEZ = '#8b6a3e'                              # Rukhsana's kameez sleeve
BANG = ['#3d6b5a', '#c9a24a', '#3d6b5a', '#6a3a4a']
SKIN_K = dict(skin='#8a5a3e', hi='#b47e5a', lo='#4a2c1d')
SKIN_R = dict(skin='#865838', hi='#ad7a56', lo='#43281a', age=0.7)
SKIN_G = dict(skin='#8e6044', hi='#bb8a66', lo='#4a2e20')
SKIN_P = dict(skin='#7e5236', hi='#a87652', lo='#3e2618', age=0.5)

SH = {}
GRADE = {}
def shot(id_, grade):
    def deco(f): SH[id_] = f; GRADE[id_] = grade; return f
    return deco

def wood_grain(col1='#6a4c34', col2='#3e2a1c', seed=3, ystep=40):
    rnd = random.Random(seed)
    o = R(0, 0, W, H, col1)
    o += g(''.join(S(f"M0,{y} C300,{y + rnd.uniform(-16,16)} 700,{y + rnd.uniform(-16,16)} 1080,{y + rnd.uniform(-6,6)}", col2, rnd.uniform(3,8), 0.45) for y in range(0, 1920, ystep)), filt='rough')
    return o

def light_pool(cx, cy, rx, ry, col='#ffe6b0', op=0.35):
    return g(E(cx, cy, rx, ry, col, op), filt='b60')

def vignette_dark(op=0.5):
    return R(0, 0, W, H, 'url(#vigd)', op)
VIG = rg('vigd', [(0, '#000', 0), (0.65, '#000', 0.15), (1, '#000', 0.85)], 0.5, 0.45, 0.75)

# ======================================================================= HOSPITAL (cool daylight)
@shot('c01', 'day')
def c01():
    # Hook: a cheque being torn off the chequebook along its perforation (Gauri's coat cuff), on a steel-grey desk
    d = PROPS_DEF + VIG + lg('desk', [(0, '#7d8584'), (1, '#4c5352')])
    b = [R(0, 0, W, H, 'url(#desk)'), light_pool(700, 500, 600, 500, '#eef4f2', 0.35)]
    b.append(g(''.join(S(f'M0,{y} L1080,{y+30}', '#ffffff', 2, 0.05) for y in range(0, 1920, 60))))
    b.append(chequebook_stub(150, 600, 1.55, -6))
    b.append(cheque(400, 560, 0.98, 6, torn=True))
    # left hand pinning the chequebook flat (Gauri)
    b.append(hand(330, 470, 176, 1.5, 'L', RELAXED, 3, thumb=(0.9, 4), sleeve=COAT, sleeve_rim=COAT_RIM, cuff_w=130, **SKIN_G))
    # right hand pulling the cheque away to the right (fingers on top of the cheque)
    b.append(hand(840, 500, 196, 1.45, 'R', GRIP, 0, thumb=(0.5, 26), sleeve=COAT, sleeve_rim=COAT_RIM, cuff_w=130, **SKIN_G))
    b.append(g(S('M90,1500 C300,1480 600,1520 1000,1490', '#2f3534', 30, 0.4), filt='b16'))
    b.append(vignette_dark(0.45))
    return svg(''.join(b), d)

@shot('c02', 'day')
def c02():
    # the cheque passed across the desk: her hand (white cuff) from top, Kabir's (blue cuff) from the bottom
    d = PROPS_DEF + VIG + lg('desk', [(0, '#7d8584'), (1, '#4c5352')])
    b = [R(0, 0, W, H, 'url(#desk)'), light_pool(560, 760, 620, 520, '#eef4f2', 0.3)]
    b.append(g(''.join(S(f'M0,{y} L1080,{y+30}', '#ffffff', 2, 0.05) for y in range(0, 1920, 60))))
    b.append(cheque(200, 640, 0.98, -3))
    # Gauri's fingers on the top edge of the cheque (hand comes from top)
    b.append(hand(640, 560, 185, 1.45, 'R', GRIP, 0, thumb=(0.4, 20), sleeve=COAT, sleeve_rim=COAT_RIM, cuff_w=130, **SKIN_G))
    # Kabir's hand from the bottom, fingertips reaching the cheque's lower edge
    b.append(hand(430, 1240, 4, 1.5, 'R', RELAXED, 2, thumb=(0.9, 0), sleeve=BLUE, sleeve_rim=BLUE_RIM, **SKIN_K))
    b.append(vignette_dark(0.45))
    return svg(''.join(b), d)

@shot('c03', 'day')
def c03():
    # Dr Gauri in profile, composed, eyes on the window (not on him). Cool daylight.
    d = PROPS_DEF + VIG + lg('wall', [(0, '#c9d2cc'), (1, '#8e9a94')]) + rg('win', [(0, '#ffffff', 0.95), (1, '#dfe9ea', 0)], 0.5, 0.5, 0.6)
    b = [R(0, 0, W, H, 'url(#wall)')]
    # window on the left with frosted panes and bars
    b.append(R(-40, 180, 380, 900, '#eef4f4')); b.append(g(E(150, 600, 400, 520, '#ffffff', 0.7), filt='b60'))
    b.append(''.join(R(-40 + i * 95, 180, 10, 900, '#7f8b88') for i in range(5)))
    b.append(''.join(R(-40, 180 + i * 225, 380, 10, '#7f8b88') for i in range(5)))
    b.append(R(330, 160, 26, 940, '#6f7a77'))
    b.append(g(P('M356,180 L1080,420 L1080,1300 L356,1100 Z', '#ffffff', 0.12), filt='b40'))
    b.append(g(gauri(lids=0.25, look=-3), tf='translate(150,560) scale(0.98)', filt='roughS'))
    b.append(vignette_dark(0.4))
    return svg(''.join(b), d)

@shot('c04', 'memory')
def c04():
    # memory: Papa's hand lying on the hospital sheet, ID band, cannula tape; bed rail
    d = PROPS_DEF + VIG + lg('sheet', [(0, '#e9e4d8'), (1, '#b8b2a4')])
    b = [R(0, 0, W, H, 'url(#sheet)')]
    rnd = random.Random(4)
    b.append(g(''.join(S(f'M{rnd.uniform(-100,1100):.0f},{y} C{rnd.uniform(200,500):.0f},{y+rnd.uniform(60,160):.0f} {rnd.uniform(500,900):.0f},{y-rnd.uniform(0,100):.0f} {rnd.uniform(900,1200):.0f},{y+rnd.uniform(40,140):.0f}', '#8a8476', rnd.uniform(14,30), 0.35) for y in range(100, 1900, 150)), filt='b12'))
    b.append(R(0, 1500, W, 60, '#6c6a64')); b.append(R(0, 1500, W, 10, '#c9c6bc', 0.6))
    tape = '<rect x="-20" y="-60" width="60" height="44" rx="4" fill="#efe8d8" fill-opacity="0.9" transform="rotate(10)"/>'
    b.append(hand(640, 1000, 152, 2.1, 'R', {'index': (0.15, 0.2, 0.1), 'middle': (0.25, 0.3, 0.2), 'ring': (0.3, 0.35, 0.2), 'little': (0.35, 0.35, 0.2)}, 2,
                  thumb=(0.8, 6), band='#d9e2e6', forearm=330, extra=tape, sleeve='#9fb4b0', sleeve_rim='#d6e2de', cuff_w=150, **SKIN_P))
    b.append(light_pool(400, 500, 500, 400, '#fff3dc', 0.3))
    b.append(vignette_dark(0.55))
    return svg(''.join(b), d)

@shot('c05', 'tungsten')
def c05():
    # the brass bell in the dark, a single glint: the last words hang over it (overlay)
    d = PROPS_DEF + VIG
    b = [R(0, 0, W, H, '#14100c'), light_pool(540, 720, 420, 420, '#f3c27a', 0.35)]
    b.append(g(E(540, 1020, 280, 46, '#000', 0.6), filt='b16'))
    b.append(g(bell(540, 840, 1.9), filt='roughS'))
    b.append(vignette_dark(0.6))
    return svg(''.join(b), d)

# ======================================================================= HOME, NIGHT (tungsten)
@shot('c06', 'tungsten')
def c06():
    # the open tin trunk under the cot: folded khaki uniform, Papa's bell on it
    d = PROPS_DEF + VIG + lg('wallg', [(0, '#4e5a51'), (1, '#2c332e')])
    b = [R(0, 0, W, H, 'url(#wallg)'), R(0, 1240, W, 680, '#3a3832')]
    b.append(g(''.join(R(x, 1240, 4, 680, '#2a2924', 0.6) for x in range(0, 1080, 90)) + ''.join(R(0, y, 1080, 4, '#2a2924', 0.6) for y in range(1240, 1920, 90))))
    b.append(bulb(540, 150, -40, 1.1))
    b.append(R(0, 1060, W, 40, '#1d1c1a')); b.append(R(40, 1100, 26, 180, '#1d1c1a')); b.append(R(1014, 1100, 26, 180, '#1d1c1a'))
    b.append(g(trunk_open(540, 1740, 1.25), filt='roughS'))
    b.append(g(bell(560, 1150, 1.2), filt='roughS'))
    b.append(light_pool(540, 1200, 420, 300, '#ffd896', 0.3))
    b.append(vignette_dark(0.5))
    return svg(''.join(b), d)

@shot('c07', 'tungsten')
def c07():
    # Kabir, side-lit by the bulb at home, thinking
    d = PROPS_DEF + VIG + rg('bgk', [(0, '#c9a46a'), (0.55, '#4e5a51'), (1, '#1e2420')], 0.2, 0.25, 0.9)
    b = [R(0, 0, W, H, 'url(#bgk)')]
    b.append(bulb(130, 230, -40, 0.9))
    b.append(g(kabir_lit() + kabir_kurta(fill=BLUE, edge='#e9c58e', shirt=True), tf='translate(140,520) scale(1.06)', filt='roughS'))
    b.append(vignette_dark(0.5))
    return svg(''.join(b), d)

@shot('c08', 'tungsten')
def c08():
    # page 47: the name scratched until the paper tore; Papa's maroon pen across it
    d = PROPS_DEF + VIG
    b = [wood_grain('#4a3626', '#2a1e14', 9), light_pool(560, 700, 600, 500, '#ffd896', 0.3)]
    b.append(g(page47(150, 260, 780, 1100, -3), filt='roughS'))
    b.append(vignette_dark(0.55))
    return svg(''.join(b), d)

@shot('c09', 'tungsten')
def c09():
    # the pale Route 47 ticket (9-1-2001), held flat by Kabir's fingertips under the bulb
    d = PROPS_DEF + VIG
    b = [wood_grain('#4a3626', '#2a1e14', 11), light_pool(540, 760, 560, 520, '#ffd896', 0.32)]
    b.append(g(ticket(330, 380, 1.45, -4), filt='roughS'))
    b.append(hand(400, 1330, -6, 1.3, 'L', RELAXED, 2, thumb=(0.8, 0), sleeve=BLUE, sleeve_rim=BLUE_RIM, **SKIN_K))
    b.append(vignette_dark(0.55))
    return svg(''.join(b), d)

@shot('c10', 'tungsten')
def c10():
    # Kabir sitting on the floor, eyes lowered to what lies in front of him: bell, open diary at 47, ticket
    d = PROPS_DEF + VIG + rg('bgk', [(0, '#b89660'), (0.55, '#3c463f'), (1, '#161a17')], 0.25, 0.15, 0.95)
    b = [R(0, 0, W, H, 'url(#bgk)'), R(0, 1180, W, 740, '#33302a')]
    b.append(light_pool(540, 1500, 600, 300, '#ffd896', 0.35))
    b.append(g(kabir_eyes_down(lids=0.75) + kabir_kurta(fill=BLUE, edge='#e9c58e', shirt=True), tf='translate(290,90) scale(0.86)', filt='roughS'))
    # foreground floor: items (cropped bottom, Kabir's knee hidden by framing)
    b.append(g(page47(60, 1380, 420, 560, -8, pen=False), filt='roughS'))
    b.append(g(bell(640, 1500, 0.8), filt='roughS'))
    b.append(g(ticket(820, 1440, 0.62, 12), filt='roughS'))
    b.append(vignette_dark(0.5))
    return svg(''.join(b), d)

# ======================================================================= MORNING, LEDGER (day)
@shot('c11', 'day')
def c11():
    # morning light: Kabir's hands open the red diary, one page lifting
    d = PROPS_DEF + VIG + lg('sun', [(0, '#fff2d0', 0.5), (1, '#fff2d0', 0)], 0, 0, 1, 1)
    b = [wood_grain('#6a4c34', '#3e2a1c', 5), R(0, 0, W, H, 'url(#sun)')]
    b.append(g(ledger_spread(90, 420, 900, 760, kalam(40, 92, '5.', 50) + kalam(96, 92, 'डॉ. गौरी पाटिल', 50, weight=700) + kalam(100, 200, '₹ 1,20,000', 48) + kalam(100, 300, '2006', 42), '', -2), filt='roughS'))
    # lifting page (right page turning, curved)
    b.append(g(P('M540,430 C700,380 880,340 990,300 L990,1100 C880,1120 700,1150 540,1170 Z', 'url(#pagec)') +
               P('M540,430 C700,380 880,340 990,300 L990,1100 C880,1120 700,1150 540,1170 Z', '#7a6a50', 0.18), filt='roughS'))
    b.append(hand(240, 1420, 8, 1.35, 'L', RELAXED, 2, thumb=(0.9, 0), sleeve=BLUE, sleeve_rim=BLUE_RIM, **SKIN_K))
    b.append(hand(900, 1260, -18, 1.35, 'R', GRIP, 0, thumb=(0.6, 10), sleeve=BLUE, sleeve_rim=BLUE_RIM, **SKIN_K))
    b.append(vignette_dark(0.4))
    return svg(''.join(b), d)

@shot('c12', 'day')
def c12():
    # page 6 in daylight: name, address, amount, year. Kabir's finger under the address.
    d = PROPS_DEF + VIG + lg('sun', [(0, '#fff2d0', 0.45), (1, '#fff2d0', 0)], 0, 0, 1, 1)
    b = [wood_grain('#6a4c34', '#3e2a1c', 6), R(0, 0, W, H, 'url(#sun)')]
    cont = page6_content()
    b.append(g(ruled_paper(120, 230, 860, 1040, -2, step=104, first=130, content=cont.replace('font-size="66"', 'font-size="72"')), filt='roughS'))
    b.append(R(96, 220, 30, 1070, '#a5141e')); b.append(R(96, 220, 30, 1070, 'url(#weave)'))
    b.append(hand(470, 760, 0, 1.35, 'R', POINT, 0, thumb=(0.6, 18), sleeve=BLUE, sleeve_rim=BLUE_RIM, forearm=460, **SKIN_K))
    b.append(vignette_dark(0.4))
    return svg(''.join(b), d)

# ======================================================================= DARZI GALI (day)
@shot('c14', 'day')
def c14():
    # the tailors' lane, over Kabir's shoulder: shutters, hanging blouses, wires
    d = PROPS_DEF + VIG + lg('sky', [(0, '#e9dcc0'), (1, '#c9b89a')])
    b = [R(0, 0, W, H, 'url(#sky)')]
    vx, vy = 560, 820
    # left & right building walls in perspective
    b.append(P(f'M0,0 L{vx-120},{vy-300} L{vx-120},{vy+200} L0,1920 Z', '#8a7a64'))
    b.append(P(f'M1080,0 L{vx+120},{vy-300} L{vx+120},{vy+200} L1080,1920 Z', '#7a6a56'))
    b.append(P(f'M{vx-120},{vy+200} L{vx+120},{vy+200} L1080,1920 L0,1920 Z', '#6a6050'))
    rnd = random.Random(8)
    # shop openings / shutters receding
    for i in range(6):
        t = i / 6; t2 = (i + 0.7) / 6
        def lx(tt): return 0 + (vx - 120) * (1 - (1 - tt) ** 1.6)
        def rx(tt): return 1080 - (1080 - vx - 120) * (1 - (1 - tt) ** 1.6)
        top = lambda tt: 0 + (vy - 300) * (1 - (1 - tt) ** 1.6) + 320 * (1 - tt)
        bot = lambda tt: 1920 - (1920 - vy - 200) * (1 - (1 - tt) ** 1.6)
        for side, fx in ((-1, lx), (1, rx)):
            x0, x1 = fx(t), fx(t2)
            y0a, y0b = top(t) + (bot(t) - top(t)) * 0.3, bot(t) - 30 * (1 - t)
            y1a, y1b = top(t2) + (bot(t2) - top(t2)) * 0.3, bot(t2) - 30 * (1 - t2)
            col = rnd.choice(['#3a2e24', '#4a5a5a', '#5a4a36', '#2e3a3e'])
            b.append(P(f'M{x0},{y0a} L{x1},{y1a} L{x1},{y1b} L{x0},{y0b} Z', col, 0.95))
            # warm interior glow
            b.append(P(f'M{x0},{y0a} L{x1},{y1a} L{x1},{y1b} L{x0},{y0b} Z', '#ffcf86', 0.18 + 0.1 * rnd.random()))
            # hanging garments (simple kurta/blouse shapes) in front of each shop
            for k in range(2):
                tt = t + (t2 - t) * (0.3 + 0.4 * k)
                xx = fx(tt); yy = top(tt) + (bot(tt) - top(tt)) * 0.32; sc = (1 - tt) * 0.9 + 0.12
                gc = rnd.choice(['#8a5a5a', '#5a7a8a', '#a08850', '#6a7a5a', '#7a5a7a', '#c2b28e'])
                b.append(f'<g transform="translate({xx},{yy}) scale({sc})"><path d="M0,-20 L0,0" stroke="#2a2420" stroke-width="3"/>'
                         f'<path d="M-60,10 L-20,0 L20,0 L60,10 L80,70 L48,80 L44,200 L-44,200 L-48,80 L-80,70 Z" fill="{gc}"/>'
                         f'<path d="M-20,0 L0,30 L20,0" fill="none" stroke="#000" stroke-opacity="0.3" stroke-width="3"/></g>')
    # overhead wires
    b.append(''.join(S(f'M0,{120+i*40} C300,{220+i*30} 700,{200+i*25} 1080,{140+i*45}', '#1e1a16', 2.5, 0.8) for i in range(4)))
    # distant light at the lane's end + a couple of far silhouettes
    b.append(g(E(vx, vy, 160, 260, '#fff4dc', 0.75), filt='b40'))
    b.append(sil('woman', vx - 40, vy + 160, 120, '#3a3028', rim='#f6dcb0'))
    b.append(sil('man', vx + 50, vy + 150, 110, '#3a3028', rim='#f6dcb0'))
    # Kabir, back view, foreground right (head & shoulders only)
    b.append(g(kabir_back(760, 1420, 1.0), filt='roughS'))
    b.append(vignette_dark(0.35))
    return svg(''.join(b), d)

# ======================================================================= THE SHOP (tungsten, warm)
def shop_back(dark=0.0):
    o = R(0, 0, W, H, '#3a2e24')
    o += R(0, 0, W, 1250, '#5a4a38')
    o += cloth_shelves(0, 120, 1080, 900, rows=5, seed=5)
    o += R(0, 1020, W, 30, '#2a2018')
    o += R(0, 1250, W, 670, '#3c3228')
    o += g(''.join(S(f'M0,{y} L1080,{y}', '#2a221a', 3, 0.5) for y in range(1280, 1920, 70)))
    if dark: o += R(0, 0, W, H, '#000', dark)
    return o

@shot('c15', 'tungsten')
def c15():
    # inside: three young women at their machines under one yellow bulb, cloth stacked to the ceiling
    d = PROPS_DEF + VIG
    b = [shop_back(0.15)]
    b.append(bulb(560, 330, -40, 1.25))
    # back worker (small) right
    b.append(g(worker(760, 1010, 0.62, flip=False, seed=3) + treadle_table(530, 1010, 330, 26, 0.6) + sewing_machine(620, 1010, 0.42, decal=0.4), filt='roughS'))
    b.append(g(fabric(560, 975, 120, 40, '#8e7a96', 0, 2, 3), filt='roughS'))
    # middle worker left (faces right)
    b.append(g(worker(330, 1180, 0.82, flip=True, dup=False, bun=True) + treadle_table(250, 1180, 420, 32, 0.8) + sewing_machine(440, 1180, 0.56, decal=0.45, flip=True), filt='roughS'))
    b.append(g(fabric(470, 1135, 160, 50, '#5a6f7a', 0, 2, 4), filt='roughS'))
    # front worker right, large (faces left), cut by the frame bottom
    b.append(g(worker(700, 1600, 1.25, flip=False) + treadle_table(160, 1600, 840, 50, 1.2) + sewing_machine(430, 1600, 0.95, decal=0.5), filt='roughS'))
    b.append(g(fabric(260, 1520, 300, 90, '#a08850', 0, 3, 5), filt='roughS'))
    b.append(light_pool(560, 500, 520, 420, '#ffd896', 0.25))
    b.append(vignette_dark(0.45))
    return svg(''.join(b), d)

@shot('c16', 'tungsten')
def c16():
    # the corner: an old black machine under a faded cloth, an empty stool, dust in a shaft of light
    d = PROPS_DEF + VIG + lg('shaft', [(0, '#fff1c8', 0.45), (1, '#fff1c8', 0)], 0, 0, 0.4, 1)
    b = [R(0, 0, W, H, '#3e3328'), R(0, 0, W, 1240, '#55473a')]
    b.append(g(''.join(E(random.Random(i).uniform(0, 1080), random.Random(i + 9).uniform(0, 1200), random.Random(i + 3).uniform(40, 160), 30, '#6a5a48', 0.4) for i in range(30)), filt='b24'))
    b.append(R(0, 1240, W, 680, '#33291f'))
    b.append(P('M690,0 L860,0 L640,1500 L180,1500 Z', 'url(#shaft)'))
    b.append(R(700, 120, 150, 210, '#e8dcbc')); b.append(R(700, 120, 150, 210, '#000', 0.1)); b.append(''.join(R(700 + i * 50, 120, 6, 210, '#3a3028') for i in range(4)))
    b.append(g(treadle_table(200, 1120, 640, 48, 1.15) + sewing_machine(500, 1120, 1.0, cover='half', decal=0.55), filt='roughS'))
    b.append(g(stool(330, 1460, 1.0), filt='roughS'))
    b.append(g(''.join(E(random.Random(i).uniform(420, 760), random.Random(i * 3).uniform(300, 1300), 3, 3, '#fff3d0', 0.7) for i in range(40)), filt='b1'))
    b.append(vignette_dark(0.5))
    return svg(''.join(b), d)

def cutting_table(seed=1):
    o = wood_grain('#7a5a3c', '#4a3220', seed, 46)
    o += fabric(-80, 80, 640, 520, '#5a6f7a', -6, 4, seed)
    o += fabric(620, -60, 560, 700, '#a08850', 8, 3, seed + 1)
    o += fabric(700, 1300, 520, 700, '#7e5a68', -4, 3, seed + 2)
    o += chalk(130, 1640, 1.0, -20) + scissors(640, 1180, 0.9, -30)
    return o

@shot('c17', 'tungsten')
def c17():
    # cutting table from above: Kabir sets the open diary down; Rukhsana's hands rest on the cloth across from him
    d = PROPS_DEF + VIG
    b = [cutting_table(1), light_pool(540, 900, 640, 560, '#ffd896', 0.3)]
    b.append(g(tape_coil(170, 820, 0.9), filt='roughS'))
    b.append(g(ledger_spread(150, 720, 780, 620, page6_content().replace('font-size="66"', 'font-size="50"').replace('font-size="62"', 'font-size="50"').replace('font-size="54"', 'font-size="44"'), '', 4), filt='roughS'))
    b.append(hand(400, 320, 176, 1.25, 'L', RELAXED, 3, thumb=(0.9, 0), sleeve=KAMEEZ, sleeve_rim='#c9a874', bangles=BANG, **SKIN_R))
    b.append(hand(700, 300, 186, 1.25, 'R', RELAXED, 3, thumb=(0.9, 0), sleeve=KAMEEZ, sleeve_rim='#c9a874', bangles=BANG[:3], **SKIN_R))
    b.append(hand(560, 1600, 2, 1.4, 'R', RELAXED, 1, thumb=(0.9, 0), sleeve=BLUE, sleeve_rim=BLUE_RIM, **SKIN_K))
    b.append(vignette_dark(0.45))
    return svg(''.join(b), d)

def shop_bokeh():
    o = R(0, 0, W, H, '#2e241c')
    o += g(cloth_shelves(0, 0, 1080, 1400, rows=5, seed=9), filt='b16')
    o += g(E(860, 260, 160, 160, '#ffd896', 0.55), filt='b40') + g(E(860, 260, 40, 40, '#fff3cf', 0.9), filt='b12')
    o += R(0, 0, W, H, '#1a120c', 0.35)
    return o

@shot('c18', 'tungsten')
def c18():
    # Rukhsana's face falls (eyes lowered), side-lit by the bulb; faces RIGHT toward Kabir
    d = PROPS_DEF + VIG
    b = [shop_bokeh()]
    b.append(g(rukhsana(flip=True, lids=0.65, glasses='cord'), tf='translate(-60,420) scale(1.0)', filt='roughS'))
    b.append(vignette_dark(0.45))
    return svg(''.join(b), d)

@shot('c19', 'tungsten')
def c19():
    # closer: chin raised, eyes level: "Udhaar kis baat ka?"
    d = PROPS_DEF + VIG
    b = [shop_bokeh()]
    b.append(g(rukhsana(flip=True, lids=0.0, chin=-5, glasses='cord'), tf='translate(-260,250) scale(1.35)', filt='roughS'))
    b.append(vignette_dark(0.45))
    return svg(''.join(b), d)

@shot('c20', 'memory')
def c20():
    # memory: Papa in khaki at the shop door, backlit, holding out a small envelope; Rukhsana's hand reaches for it
    d = PROPS_DEF + VIG
    b = [R(0, 0, W, H, '#3a2e22')]
    b.append(door_frame_lit(230, 200, 680, 1600, '#f8ecd0'))
    b.append(g(E(570, 800, 420, 760, '#ffffff', 0.5), filt='b60'))
    sil_ = ('<path d="M300,1820 C300,1380 360,1240 470,1196 C514,1178 532,1150 534,1118 L626,1118 C628,1150 648,1178 700,1198 C820,1240 880,1380 880,1820 Z"/>'
            '<path d="M512,1130 C488,1076 486,1000 500,956 C516,904 562,880 604,886 C650,894 672,940 668,994 C664,1050 644,1094 622,1124 Z"/>'
            '<path d="M486,930 C492,862 556,836 620,846 C666,854 694,884 698,920 L724,926 L724,940 L484,944 Z"/>'
            '<path d="M420,1250 C380,1300 380,1380 410,1420 L470,1450 C452,1400 456,1340 500,1290 Z"/>')
    b.append(f'<g fill="#f2d39c" transform="translate(-5,-4)">{sil_}</g>')
    b.append(f'<g fill="#2a241e">{sil_}</g>')
    b.append(S('M372,1330 C410,1260 460,1226 520,1214', '#b89c66', 6, 0.7))      # khaki shoulder catching light
    b.append(S('M650,1214 C700,1228 760,1260 800,1320', '#8a7550', 5, 0.5))
    b.append(envelope(440, 1500, 240, 140, -10))
    # Papa's fingers (backlit) curled over the envelope's top edge, thumb under
    fing = ''.join(f'<path d="M{x0},{1418+k*3} C{x0-2},{1450+k*2} {x0+2},{1478+k} {x0+12},{1484+k} C{x0+22},{1486+k} {x0+26},{1470+k} {x0+24},{1440+k*2} L{x0+22},{1416+k*3} Z"/>' for k, x0 in enumerate((392, 418, 444, 468)))
    palm = '<path d="M384,1380 C380,1410 384,1430 394,1440 L494,1424 C496,1400 486,1376 470,1360 Z"/>'
    b.append(f'<g fill="#f2d39c" transform="translate(-3,-3)">{palm}{fing}</g><g fill="#2a241e">{palm}{fing}</g>')
    b.append(hand(700, 1790, -42, 1.0, 'L', RELAXED, 3, thumb=(0.9, 6), sleeve=KAMEEZ, sleeve_rim='#c9a874', bangles=BANG[:3], **SKIN_R))
    b.append(vignette_dark(0.5))
    return svg(''.join(b), d)

@shot('c21', 'tungsten')
def c21():
    # a dozen years of small, plain envelopes, kept in a tin; thread-tied bundle
    d = PROPS_DEF + VIG
    b = [cutting_table(4), light_pool(540, 900, 600, 600, '#ffd896', 0.3)]
    b.append(R(150, 420, 780, 960, '#3c4a4a')); b.append(R(170, 440, 740, 920, '#22292a'))
    rnd = random.Random(12)
    for i in range(14):
        b.append(envelope(540 + rnd.uniform(-180, 180), 560 + i * 54, 330, 170, rnd.uniform(-10, 10)))
    b.append(g(S('M380,520 C420,900 380,1200 420,1380 M700,520 C660,900 700,1200 660,1380', '#d9cfb0', 4, 0.8)))
    b.append(vignette_dark(0.5))
    return svg(''.join(b), d)

@shot('c22', 'tungsten')
def c22():
    # her order book: "Mohan Lal ji" at the top, and nothing ever written under it
    d = PROPS_DEF + VIG
    b = [cutting_table(6), light_pool(540, 800, 600, 600, '#ffd896', 0.3)]
    b.append(g(order_book(170, 300, 740, 1060, 2), filt='roughS'))
    b.append(g(pencil(820, 1250, 300, -70), filt='roughS'))
    b.append(vignette_dark(0.45))
    return svg(''.join(b), d)

@shot('c23', 'tungsten')
def c23():
    # Rukhsana upright behind the cutting table, spectacles on, chin raised
    d = PROPS_DEF + VIG
    b = [shop_bokeh()]
    b.append(g(rukhsana(flip=True, lids=0.15, chin=-7, glasses='on'), tf='translate(-110,360) scale(1.12)', filt='roughS'))
    b.append(vignette_dark(0.45))
    return svg(''.join(b), d)

@shot('c24', 'tungsten')
def c24():
    # back of the bank notice on the cutting table: Kabir's hand pencils the sum (numbers are overlays)
    d = PROPS_DEF + VIG
    b = [cutting_table(8), light_pool(540, 760, 620, 600, '#ffd896', 0.28)]
    b.append(g(notice_back(110, 240, 860, 1220, -2), filt='roughS'))
    b.append(g(pencil(640, 1250, 330, 52), filt='roughS'))
    b.append(hand(900, 1590, -32, 1.55, 'R', PENCIL, 0, thumb=(0.7, 22), sleeve=BLUE, sleeve_rim=BLUE_RIM, **SKIN_K))
    b.append(vignette_dark(0.45))
    return svg(''.join(b), d)

@shot('c25', 'tungsten')
def c25():
    # side by side: diary page 6 (₹30,000 · machine) and the notice with the new sum
    d = PROPS_DEF + VIG
    b = [cutting_table(10), light_pool(540, 760, 620, 600, '#ffd896', 0.28)]
    cont = page6_content().replace('font-size="66"', 'font-size="56"')
    b.append(g(ruled_paper(40, 300, 560, 900, -4, step=104, first=130, content=cont), filt='roughS'))
    b.append(R(20, 290, 26, 930, '#a5141e')); b.append(R(20, 290, 26, 930, 'url(#weave)'))
    b.append(g(notice_back(560, 420, 480, 760, 5, sums=False), filt='roughS'))
    b.append(vignette_dark(0.45))
    return svg(''.join(b), d)

@shot('c26', 'tungsten')
def c26():
    # Kabir's finger runs down page 6, past the machine line, over rows with nothing in them
    d = PROPS_DEF + VIG
    b = [cutting_table(12), light_pool(540, 760, 620, 600, '#ffd896', 0.28)]
    cont = page6_content()
    b.append(g(ruled_paper(110, 120, 880, 1560, -1, step=104, first=130, content=cont), filt='roughS'))
    b.append(R(86, 110, 30, 1590, '#a5141e')); b.append(R(86, 110, 30, 1590, 'url(#weave)'))
    b.append(hand(560, 1060, 0, 1.3, 'R', POINT, 0, thumb=(0.6, 18), sleeve=BLUE, sleeve_rim=BLUE_RIM, forearm=520, **SKIN_K))
    b.append(vignette_dark(0.45))
    return svg(''.join(b), d)

@shot('c27', 'tungsten')
def c27():
    # Kabir in the shop light, eyes down, unsettled
    d = PROPS_DEF + VIG
    b = [shop_bokeh()]
    b.append(g(kabir_eyes_down(lids=0.6) + kabir_kurta(fill=BLUE, edge='#e9c58e', shirt=True), tf='translate(150,470) scale(1.05)', filt='roughS'))
    b.append(vignette_dark(0.45))
    return svg(''.join(b), d)

@shot('c29', 'tungsten')
def c29():
    # the shop is doing well: new bolts to the ceiling, two machines busy below
    d = PROPS_DEF + VIG
    b = [R(0, 0, W, H, '#3a2e24'), cloth_shelves(0, 0, 1080, 1200, rows=7, seed=21, cols=['#9a5a4a','#4f7a8a','#b8984a','#6a8a5a','#8a5a7e','#d0c4a6','#4f6a8a','#b0743e','#5a8a7a','#c08a8a'])]
    b.append(R(0, 0, W, 1200, '#1a120c', 0.2))
    b.append(R(0, 1180, W, 740, '#3c3228'))
    b.append(g(worker(380, 1560, 1.0, flip=True, dup=False, bun=True) + treadle_table(60, 1560, 520, 40, 1.0) + sewing_machine(300, 1560, 0.7, flip=True, decal=0.45), filt='roughS'))
    b.append(g(worker(920, 1640, 1.1) + treadle_table(560, 1640, 600, 44, 1.1) + sewing_machine(780, 1640, 0.78, decal=0.45), filt='roughS'))
    b.append(g(fabric(140, 1500, 220, 70, '#8e7a96', 0, 2, 7) + fabric(620, 1570, 240, 80, '#5a6f7a', 0, 2, 8), filt='roughS'))
    b.append(bulb(540, 140, -40, 1.0))
    b.append(vignette_dark(0.45))
    return svg(''.join(b), d)

@shot('c30', 'tungsten')
def c30():
    # Rukhsana looks away to her machines: firm, not angry
    d = PROPS_DEF + VIG
    b = [shop_bokeh()]
    b.append(g(rukhsana(flip=False, lids=0.35, glasses='cord'), tf='translate(120,420) scale(1.02)', filt='roughS'))
    b.append(vignette_dark(0.45))
    return svg(''.join(b), d)

@shot('c31', 'tungsten')
def c31():
    # macro: Papa's own handwriting, the machine line
    d = PROPS_DEF + VIG
    b = [R(0, 0, W, H, 'url(#pagec)')]
    b.append(''.join(S(f'M-20,{y} L1100,{y-8}', '#9fb2b6', 3, 0.6) for y in range(260, 1900, 230)))
    b.append(S('M160,0 L150,1920', '#d08a8a', 4, 0.5))
    b.append(kalam(200, 720, '₹ 30,000', 190, weight=700, rot=-3))
    b.append(kalam(260, 1000, '— मशीन', 150, rot=-3))
    b.append(kalam(260, 1260, '2006', 120, rot=-3, op=0.8))
    b.append(g(R(0, 0, W, H, '#ffd896', 0.08)))
    b.append(vignette_dark(0.4))
    return svg(''.join(b), d)

@shot('c32', 'tungsten')
def c32():
    # the diary pushed back across the cutting table toward Kabir; her hand just leaving it
    d = PROPS_DEF + VIG
    b = [cutting_table(14), light_pool(540, 1000, 620, 600, '#ffd896', 0.3)]
    b.append(g(ledger_closed(540, 1150, 520, 720, -8), filt='roughS'))
    b.append(hand(560, 470, 178, 1.3, 'L', FLAT, 4, thumb=(0.9, 0), sleeve=KAMEEZ, sleeve_rim='#c9a874', bangles=BANG, forearm=300, **SKIN_R))
    b.append(vignette_dark(0.45))
    return svg(''.join(b), d)

@shot('c33', 'tungsten')
def c33():
    # two-shot: Kabir's back in the foreground, Rukhsana across the table facing him, the unused machine behind her
    d = PROPS_DEF + VIG
    b = [R(0, 0, W, H, '#3a2e24'), g(cloth_shelves(0, 100, 1080, 900, rows=5, seed=5), filt='b6'), R(0, 0, W, H, '#1a120c', 0.3)]
    b.append(g(treadle_table(560, 1010, 520, 36, 0.8, legs=False) + sewing_machine(820, 1010, 0.66, cover='half', decal=0.5), filt='b2'))
    b.append(bulb(540, 140, -40, 0.9))
    b.append(g(rukhsana(flip=True, lids=0.2, glasses='cord'), tf='translate(250,430) scale(0.78)', filt='roughS'))
    b.append(R(0, 1240, W, 680, '#5a4030'))
    b.append(g(ledger_closed(640, 1420, 220, 300, 72), filt='roughS'))
    b.append(g(kabir_back(240, 1460, 1.05), filt='roughS'))
    b.append(vignette_dark(0.45))
    return svg(''.join(b), d)

@shot('c34', 'tungsten')
def c34():
    # Kabir, lit profile, holding the question
    d = PROPS_DEF + VIG
    b = [shop_bokeh()]
    b.append(g(kabir_lit() + kabir_kurta(fill=BLUE, edge='#e9c58e', shirt=True), tf='translate(110,380) scale(1.12)', filt='roughS'))
    b.append(vignette_dark(0.45))
    return svg(''.join(b), d)

@shot('v01', 'neutral')
def v01():
    d = PROPS_DEF + rg('cl', [(0, '#a5141e'), (0.7, '#5e0c12'), (1, '#2a0508')], 0.5, 0.45, 0.8)
    b = [R(0, 0, W, H, 'url(#cl)'), R(0, 0, W, H, 'url(#weave)')]
    return svg(''.join(b), d)

if __name__ == '__main__':
    out = sys.argv[1]; ids = sys.argv[2:] or list(SH)
    for i in ids:
        open(f'{out}/{i}.svg', 'w').write(SH[i]())
    print(' '.join(f'{i}:{GRADE[i]}' for i in ids))
