# Episode 7 "Papa Ki Aawaaz" — shot generators.  usage: python3 shots7.py OUTDIR [ids...]
import sys, math, random
sys.path.insert(0, '/home/claude/udhaar/scripts'); sys.path.insert(0, '/home/claude/udhaar/ep06'); sys.path.insert(0, '/home/claude/udhaar/ep07')
from art import *
from shapes import *
from props6 import *
from props7 import *
from hands6 import hand, FLAT, RELAXED, POINT, GRIP, PENCIL
from people6 import rukhsana, kabir_eyes_down
from people7 import ma_lit, bablu, joined_palms, fist
import shots6 as S6

BLUE, BLUE_RIM = '#55708a', '#9fb6c8'
KAMEEZ = '#8b6a3e'; BANG = ['#3d6b5a', '#c9a24a', '#3d6b5a', '#6a3a4a']
SKIN_K = dict(skin='#8a5a3e', hi='#b47e5a', lo='#4a2c1d')
SKIN_R = dict(skin='#865838', hi='#ad7a56', lo='#43281a', age=0.7)
SKIN_M = dict(skin='#8a5c40', hi='#b07e5c', lo='#46291b', age=0.5)
SKIN_B = dict(skin='#8a5a3e', hi='#b47e58', lo='#4a2c1d')
SHIRT_B = '#8a7444'
D = PROPS_DEF + P7_DEF + S6.VIG
SH, GRADE = {}, {}
def shot(i, gr):
    def deco(f): SH[i] = f; GRADE[i] = gr; return f
    return deco
vig = S6.vignette_dark; pool = S6.light_pool

def room_wall(bulb_x=540, door=False):
    o = R(0, 0, W, H, '#4e5a51') + g(''.join(E(random.Random(i).uniform(0, 1080), random.Random(i + 5).uniform(0, 1300), random.Random(i).uniform(60, 200), 40, '#3e4a42', 0.5) for i in range(26)), filt='b24')
    o += R(0, 1300, W, 620, '#5c5a53')
    o += g(''.join(R(x, 1300, 3, 620, '#46443e', 0.7) for x in range(0, 1080, 96)) + ''.join(R(0, y, 1080, 3, '#46443e', 0.7) for y in range(1300, 1920, 96)))
    o += ''.join(E(random.Random(i).uniform(0, 1080), random.Random(i + 2).uniform(1310, 1910), 3, 2, '#8a877c', 0.6) for i in range(160))
    return o

# ============================================================= SHOP (opening, Ep6 = ASK)
@shot('d01', 'tungsten')
def d01():
    # her hand counting ₹500 notes down onto the cutting table, hard
    b = [S6.cutting_table(21), pool(540, 900, 640, 560, '#ffd896', 0.3)]
    b.append(note_stack(250, 820, 10, -8, 1.45, 3))
    b.append(note500(520, 700, 14, 1.45)); b.append(note500(380, 1060, -20, 1.45, 0.1))
    b.append(hand(600, 560, 182, 1.3, 'L', FLAT, 2, thumb=(0.9, 0), sleeve=KAMEEZ, sleeve_rim='#c9a874', bangles=BANG, forearm=280, **SKIN_R))
    b.append(vig(0.45))
    return svg(''.join(b), D)

@shot('d02', 'tungsten')
def d02():
    # the notes pressed into Kabir's hand: her hand on top (from above), his fingers under the bundle
    b = [S6.cutting_table(22), pool(540, 980, 600, 560, '#ffd896', 0.3)]
    b.append(hand(540, 1520, 2, 1.45, 'R', RELAXED, 4, thumb=(0.95, -6), sleeve=BLUE, sleeve_rim=BLUE_RIM, **SKIN_K))
    b.append(note_stack(330, 1060, 9, -4, 1.4, 5))
    b.append(hand(560, 800, 178, 1.35, 'L', FLAT, 3, thumb=(0.9, 0), sleeve=KAMEEZ, sleeve_rim='#c9a874', bangles=BANG, forearm=280, **SKIN_R))
    b.append(vig(0.45))
    return svg(''.join(b), D)

@shot('d03', 'tungsten')
def d03():
    # Rukhsana turned away, chin up: it hurt her
    b = [S6.shop_bokeh(), g(rukhsana(flip=False, lids=0.45, chin=-6, glasses='cord'), tf='translate(140,380) scale(1.06)', filt='roughS'), vig(0.45)]
    return svg(''.join(b), D)

@shot('d04', 'tungsten')
def d04():
    # facing him, chin raised: "Ab main karzdaar nahi."
    b = [S6.shop_bokeh(), g(rukhsana(flip=True, lids=0.1, chin=-6, glasses='cord'), tf='translate(-230,280) scale(1.3)', filt='roughS'), vig(0.45)]
    return svg(''.join(b), D)

@shot('d05', 'tungsten')
def d05():
    # leaving: Kabir's back in the shop doorway, the lane bright beyond; the old black machine at the edge
    b = [R(0, 0, W, H, '#2e241c'), R(250, 260, 600, 1500, '#f1dcb2'), g(E(550, 900, 380, 640, '#fff6e0', 0.6), filt='b60')]
    b.append(R(220, 230, 40, 1560, '#3a2c20')); b.append(R(840, 230, 40, 1560, '#3a2c20')); b.append(R(220, 230, 660, 40, '#3a2c20'))
    b.append(g(''.join(f'<g transform="translate({300+i*120},{300+(i%2)*20}) scale(0.7)"><path d="M-60,10 L-20,0 L20,0 L60,10 L80,70 L48,80 L44,200 L-44,200 L-48,80 L-80,70 Z" fill="{c}" fill-opacity="0.7"/></g>' for i, c in enumerate(['#8a5a5a', '#5a7a8a', '#a08850', '#6a7a5a', '#7a5a7a'])), filt='b4'))
    b.append(g(treadle_table(-120, 1150, 360, 40, 0.9) + sewing_machine(60, 1150, 0.62, cover='half', decal=0.5), filt='roughS'))
    b.append(g(kabir_back(560, 1240, 1.05), filt='roughS'))
    b.append(vig(0.5))
    return svg(''.join(b), D)

@shot('d06', 'memory')
def d06():
    # memory, winter 2001: young Ma at her black machine through the night, a lamp, frost on the window; the cloth is unidentifiable
    d = D + rg('lamp', [(0, '#ffd99a', 0.85), (0.35, '#e9a050', 0.25), (1, '#e9a050', 0)], 0.42, 0.45, 0.6)
    b = [R(0, 0, W, H, '#2e3533')]
    b.append(R(640, 330, 320, 460, '#5a6a80')); b.append(g(''.join(E(random.Random(i).uniform(650, 950), random.Random(i * 7).uniform(340, 780), 30, 18, '#e8eef4', 0.5) for i in range(20)), filt='b8'))
    b.append(''.join(R(640 + i * 80, 330, 8, 460, '#1d2220') for i in range(5))); b.append(R(640, 556, 320, 8, '#1d2220'))
    b.append(R(0, 1350, W, 570, '#26221f'))
    b.append(g(E(440, 940, 640, 640, 'url(#lamp)'), filt='b40'))
    b.append(g(treadle_table(240, 1080, 620, 40, 1.0) + sewing_machine(560, 1080, 0.95, decal=0.6, thread='#5a4a6a'), filt='roughS'))
    b.append(g(fabric(110, 1010, 300, 80, '#3e3a4a', 0, 2, 9), filt='roughS'))
    b.append(g(P('M390,640 L470,640 L500,720 L360,720 Z', '#3a3530') + R(426, 520, 8, 120, '#2a2622') + E(430, 730, 40, 10, '#fff0c8'), filt='roughS'))
    # young Ma (2001): seated silhouette, muted indigo saree, pallu over head, facing LEFT toward the machine
    ma = ('<path d="M820,1080 C800,1000 790,920 800,860 C808,812 830,786 860,772 C846,752 840,730 842,708 C846,664 878,636 914,640 '
          'C950,646 970,676 966,714 C962,742 950,762 934,772 C966,790 990,830 996,880 C1004,960 1000,1040 1010,1100 Z"/>'
          '<path d="M832,868 C790,900 740,960 700,1010 L716,1030 C756,990 806,940 850,906 Z"/>')
    b.append(f'<g fill="#f2cf94" transform="translate(-5,-4)">{ma}</g><g fill="#2c2a3a">{ma}</g>')
    b.append(S('M862,700 C880,668 920,660 950,676', '#c9b8a0', 6, 0.6))
    b.append(vig(0.55))
    return svg(''.join(b), d)

@shot('d07', 'dawn')
def d07():
    # walking home at dusk through the lanes, over Kabir's shoulder; a streetlight coming on
    b = [R(0, 0, W, H, '#5d6a73')]
    b.append(g(E(540, 640, 600, 500, '#e3c89a', 0.7), filt='b60'))
    b.append(P('M0,0 L420,460 L420,1100 L0,1920 Z', '#3a3a3e')); b.append(P('M1080,0 L660,460 L660,1100 L1080,1920 Z', '#34353a'))
    b.append(P('M420,1100 L660,1100 L1080,1920 L0,1920 Z', '#4a4846'))
    b.append(''.join(R(40 + i * 70, 300 + i * 50, 50, 70, '#ffcf86', 0.5) for i in range(5)))
    b.append(''.join(R(980 - i * 70, 320 + i * 50, 50, 70, '#ffcf86', 0.45) for i in range(5)))
    b.append(''.join(S(f'M0,{160+i*40} C300,{260+i*30} 700,{240+i*25} 1080,{180+i*45}', '#1e1a16', 2.5, 0.8) for i in range(3)))
    b.append(S('M760,200 L760,900', '#1e1a16', 8) + S('M760,210 L700,230', '#1e1a16', 6) + g(E(700, 240, 80, 80, '#ffe2a6', 0.8), filt='b24') + E(700, 240, 12, 12, '#fff6dc'))
    b.append(sil('man', 520, 1150, 120, '#2e2c2a', rim='#f6dcb0')); b.append(sil('woman', 600, 1140, 110, '#2e2c2a', rim='#f6dcb0'))
    b.append(g(kabir_back(380, 1440, 1.05, rim='#f3c890'), filt='roughS'))
    b.append(vig(0.45))
    return svg(''.join(b), D)

@shot('d08', 'dawn')
def d08():
    # Kabir's profile in the dusk light, thinking of everything he never knew
    d = D + rg('bgd', [(0, '#e9c48e'), (0.55, '#6a6e72'), (1, '#2e3236')], 0.15, 0.3, 0.9)
    b = [R(0, 0, W, H, 'url(#bgd)'), g(''.join(E(120 + i * 140, 260 + (i % 3) * 90, 40, 40, '#ffe2a6', 0.5) for i in range(7)), filt='b16')]
    b.append(g(kabir_eyes_down(lids=0.35) + kabir_kurta(fill=BLUE, edge='#e9c58e', shirt=True), tf='translate(150,500) scale(1.05)', filt='roughS'))
    b.append(vig(0.45))
    return svg(''.join(b), d)

# ============================================================= HOME
@shot('d09', 'night')
def d09():
    # the Verma door at dusk, bank notice still taped on it; the bulb on inside
    b = [R(0, 0, W, H, '#3a3e4a'), g(E(540, 300, 700, 400, '#7a7690', 0.5), filt='b60')]
    b.append(R(120, 200, 840, 1300, '#8a8478')); b.append(g(''.join(E(random.Random(i).uniform(120, 960), random.Random(i).uniform(200, 1500), 80, 40, '#6e695f', 0.5) for i in range(20)), filt='b16'))
    b.append(R(300, 420, 480, 1080, '#2a2420')); b.append(R(320, 440, 215, 1060, 'url(#doorg)')); b.append(R(545, 440, 215, 1060, 'url(#doorg)'))
    b.append(''.join(R(340 + k * 225, 480 + j * 320, 175, 260, '#000', 0.12) for k in range(2) for j in range(3)))
    b.append(R(560, 640, 150, 200, '#efede4')); b.append(''.join(R(578, 668 + i * 22, 112, 6, '#7a7a80', 0.6) for i in range(7)))
    b.append(R(510, 900, 60, 26, '#2a2420')); b.append(E(540, 960, 18, 26, '#2a2420'))
    b.append(R(80, 1500, 920, 60, '#6a665c')); b.append(R(40, 1560, 1000, 360, '#4a4844'))
    b.append(g(E(540, 1540, 180, 30, '#c9a87a', 0.4), filt='b8'))
    b.append(S('M0,120 C300,220 700,200 1080,140', '#1a1816', 3))
    b.append(g(E(880, 300, 120, 120, '#ffe2a6', 0.5), filt='b24'))
    b.append(vig(0.5))
    return svg(''.join(b), D)

@shot('d10', 'tungsten')
def d10():
    # the tin trunk under the cot; Kabir's two hands lift the bell out for the first time
    b = [room_wall(), pool(540, 900, 600, 500, '#ffd896', 0.3), bulb(540, 140, -40, 1.0)]
    b.append(g(trunk_open(540, 1760, 1.25), filt='roughS'))
    b.append(g(bell_dusty(540, 1060, 1.35), filt='roughS'))
    b.append(hand(300, 1330, 40, 1.25, 'L', GRIP, 0, thumb=(0.6, 10), sleeve=BLUE, sleeve_rim=BLUE_RIM, **SKIN_K))
    b.append(hand(780, 1330, -40, 1.25, 'R', GRIP, 0, thumb=(0.6, 10), sleeve=BLUE, sleeve_rim=BLUE_RIM, **SKIN_K))
    b.append(vig(0.5))
    return svg(''.join(b), D)

@shot('d11', 'tungsten')
def d11():
    # polishing: a cloth wipes a bright streak through years of dust
    b = [S6.wood_grain('#4a3626', '#2a1e14', 31), pool(540, 800, 560, 520, '#ffd896', 0.35)]
    b.append(g(E(540, 1130, 330, 50, '#000', 0.5), filt='b16'))
    b.append(g(bell_dusty(540, 760, 3.0, clean_side=0.9), filt='roughS'))
    b.append(g(fabric(520, 960, 300, 200, '#c9c2b0', -20, 2, 4), filt='roughS'))
    b.append(hand(780, 1240, -28, 1.3, 'R', GRIP, 0, thumb=(0.6, 12), sleeve=BLUE, sleeve_rim=BLUE_RIM, **SKIN_K))
    b.append(vig(0.5))
    return svg(''.join(b), D)

@shot('d12', 'tungsten')
def d12():
    # turned over: inside the dome, a riveted brass plate engraved 47
    b = [R(0, 0, W, H, '#1a140e'), pool(540, 760, 560, 560, '#ffd896', 0.35)]
    b.append(g(bell_underside(540, 760, 1.4), filt='roughS'))
    b.append(hand(180, 1300, 35, 1.2, 'L', GRIP, 0, thumb=(0.5, 10), sleeve=BLUE, sleeve_rim=BLUE_RIM, **SKIN_K))
    b.append(vig(0.5))
    return svg(''.join(b), D)

@shot('d13', 'tungsten')
def d13():
    # the ticket held up beside the plate: the same 47
    b = [R(0, 0, W, H, '#1a140e'), pool(540, 760, 560, 560, '#ffd896', 0.35)]
    b.append(g(bell_underside(380, 600, 0.95), filt='roughS'))
    b.append(g(ticket(620, 620, 1.05, 6), filt='roughS'))
    b.append(hand(800, 1440, -4, 1.2, 'R', GRIP, 0, thumb=(0.5, 14), sleeve=BLUE, sleeve_rim=BLUE_RIM, **SKIN_K))
    b.append(vig(0.5))
    return svg(''.join(b), D)

@shot('d14', 'night')
def d14():
    # a knock: Bablu at the open door at dusk, sweets box held to his chest, hair shining under the porch bulb
    d = D + lg('dusk', [(0, '#3a4058'), (1, '#8a6a5a')])
    b = [R(0, 0, W, H, 'url(#dusk)'), R(0, 0, 130, H, '#2a2420'), R(950, 0, 130, H, '#2a2420'), R(90, 0, 60, H, 'url(#doorg)')]
    b.append(g(E(520, 250, 260, 200, '#ffe2a6', 0.5), filt='b40'))
    b.append(g(bablu(mouth='smile', gleam=1.2), tf='translate(150,380) scale(0.98)', filt='roughS'))
    b.append(g(sweets_box(250, 1260, 1.3, -4), filt='roughS'))
    b.append(hand(300, 1640, -10, 1.0, 'R', GRIP, 0, thumb=(0.5, 18), sleeve=SHIRT_B, sleeve_rim='#c9b27a', **SKIN_B))
    b.append(hand(560, 1660, 10, 1.0, 'L', GRIP, 0, thumb=(0.5, 18), sleeve=SHIRT_B, sleeve_rim='#c9b27a', **SKIN_B))
    b.append(vig(0.45))
    return svg(''.join(b), d)

@shot('d15', 'day')
def d15():
    # diary page 7 in his name: ₹50,000, 2007
    b = [S6.wood_grain('#4a3626', '#2a1e14', 15), pool(540, 700, 600, 600, '#ffd896', 0.3)]
    cont = (kalam(40, 92, '7.', 56) + kalam(100, 92, 'बबलू “हीरो”', 76, weight=700) +
            kalam(104, 306, '₹ 50,000', 72, weight=700) + kalam(104, 410, '2007', 54))
    b.append(g(ruled_paper(120, 260, 860, 1040, -2, step=104, first=130, content=cont), filt='roughS'))
    b.append(R(96, 250, 30, 1070, '#a5141e')); b.append(R(96, 250, 30, 1070, 'url(#weave)'))
    b.append(vig(0.45))
    return svg(''.join(b), D)

@shot('d16', 'tungsten')
def d16():
    # sheepish: no money to give back, eyes down, a small embarrassed smile
    b = [room_wall(), bulb(820, 120, -40, 0.9), pool(700, 500, 500, 500, '#ffd896', 0.25)]
    b.append(g(bablu(mouth='smile', brows=1, eye='open', gleam=0.9), tf='translate(-120,240) scale(1.32)', filt='roughS'))
    b.append(vig(0.45))
    return svg(''.join(b), D)

@shot('d17', 'tungsten')
def d17():
    # Bablu on the edge of the cot, sweets box on his knees, palms joined in apology
    b = [room_wall(), bulb(820, 120, -40, 0.9), pool(700, 500, 500, 500, '#ffd896', 0.25)]
    b.append(g(iron_cot(-60, 1300, 1260, 1.0), filt='roughS'))
    b.append(g(bablu(mouth='flat', brows=1) + joined_palms(250, 1050, 1.15, **{'skin': '#8a5a3e', 'lo': '#4a2c1d', 'sleeve': SHIRT_B}), tf='translate(110,330) scale(0.9)', filt='roughS'))
    b.append(g(sweets_box(220, 1280, 1.2, 2), filt='roughS'))
    b.append(vig(0.45))
    return svg(''.join(b), D)

@shot('d18', 'tungsten')
def d18():
    # mid-impression: hunched, fist at the mouth (Sharma uncle's cough), eyes squeezed
    b = [room_wall(), bulb(820, 120, -40, 0.9), pool(700, 500, 500, 500, '#ffd896', 0.25)]
    b.append(g(bablu(mouth='open', eye='squeeze', brows=1) + fist(300, 650, 1.05, -24, sleeve=SHIRT_B, arm=520), tf='translate(150,420) rotate(6 560 700) scale(0.98)', filt='roughS'))
    b.append(vig(0.45))
    return svg(''.join(b), D)

@shot('d19', 'tungsten')
def d19():
    # the next impression: eyebrows up, mouth wide, one hand up as if ringing a cycle bell
    b = [room_wall(), bulb(820, 120, -40, 0.9), pool(700, 500, 500, 500, '#ffd896', 0.25)]
    b.append(g(bablu(mouth='open', brows=2), tf='translate(160,420) scale(0.98)', filt='roughS'))
    b.append(hand(330, 1500, -20, 1.0, 'R', GRIP, 0, thumb=(1.0, -30), sleeve=SHIRT_B, sleeve_rim='#c9b27a', forearm=400, **SKIN_B))
    b.append(vig(0.45))
    return svg(''.join(b), D)

@shot('d20', 'tungsten')
def d20():
    # Ma at the kitchen doorway, pallu over her head, listening, not smiling
    d = D + lg('kit', [(0, '#e9b86e'), (1, '#7a5430')], 0, 0, 1, 0)
    b = [R(0, 0, W, H, '#1c1916'), R(0, 0, 360, H, 'url(#kit)')]
    b.append(g(R(300, 0, 120, H, '#3a2a1e') + R(330, 0, 30, H, '#5a4430'), filt='rough'))
    b.append(g(ma_lit(lids=0.35, look=-2), tf='translate(-40,330) scale(1.05) rotate(3 560 500)', filt='roughS'))
    b.append(vig(0.45))
    return svg(''.join(b), d)

@shot('d21', 'tungsten')
def d21():
    # at the threshold, half-turned, his hand at his throat: clearing it
    d = D + lg('dusk', [(0, '#3a4058'), (1, '#8a6a5a')])
    b = [R(0, 0, W, H, '#4e5a51'), R(560, 0, 520, H, 'url(#dusk)'), R(520, 0, 60, H, '#2a2420'), R(580, 0, 40, H, 'url(#doorg)')]
    b.append(g(bablu(mouth='flat', brows=0, gleam=0.8) + fist(470, 760, 1.0, -10, sleeve=SHIRT_B, arm=420), tf='translate(120,420) scale(1.0)', filt='roughS'))
    b.append(vig(0.5))
    return svg(''.join(b), d)

@shot('d22', 'tungsten')
def d22():
    # Kabir stops dead: eyes wide, the bell still in his hands
    d = D + rg('bgk', [(0, '#c9a46a'), (0.55, '#4e5a51'), (1, '#1e2420')], 0.2, 0.25, 0.9)
    b = [R(0, 0, W, H, 'url(#bgk)'), bulb(130, 200, -40, 0.9)]
    b.append(g(kabir_lit(look=-2) + kabir_kurta(fill=BLUE, edge='#e9c58e', shirt=True), tf='translate(150,420) scale(1.08)', filt='roughS'))
    b.append(vig(0.5))
    return svg(''.join(b), d)

@shot('d23', 'tungsten')
def d23():
    # the empty threshold; the sweets box left on the cot
    b = [room_wall(), R(620, 200, 380, 1100, '#2a2420'), R(650, 230, 320, 1070, '#5a6070'), g(E(810, 760, 200, 400, '#8a8aa0', 0.4), filt='b40')]
    b.append(g(iron_cot(-80, 1380, 760, 1.0), filt='roughS'))
    b.append(g(sweets_box(180, 1200, 1.0, -6), filt='roughS'))
    b.append(bulb(300, 120, -40, 0.8))
    b.append(vig(0.5))
    return svg(''.join(b), D)

@shot('d24', 'tungsten')
def d24():
    # Ma slides the iron bolt; her hand stays on it
    b = [R(0, 0, W, H, '#2a2420'), R(60, 0, 960, H, 'url(#doorg)')]
    b.append(''.join(R(110 + k * 470, 120 + j * 600, 380, 500, '#000', 0.12) for k in range(2) for j in range(3)))
    b.append(g(''.join(S(f'M{random.Random(i).uniform(60,1020):.0f},0 L{random.Random(i+1).uniform(60,1020):.0f},1920', '#2c4644', 2, 0.25) for i in range(30))))
    b.append(g(door_bolt(520, 900, 1.6, slid=1.0), filt='roughS'))
    b.append(hand(720, 1290, -8, 1.35, 'R', GRIP, 0, thumb=(0.6, 12), sleeve='#cfc8b6', sleeve_rim='#efe6d2', cuff_w=110, forearm=400, **SKIN_M))
    b.append(g(P('M-40,1500 C200,1460 500,1500 700,1560 L700,1920 L-40,1920 Z', '#d8d0bd') + S('M-40,1500 C200,1460 500,1500 700,1560', '#f2ead6', 6, 0.8), filt='roughS'))
    b.append(pool(400, 700, 500, 500, '#ffd896', 0.2)); b.append(vig(0.5))
    return svg(''.join(b), D)

@shot('d25', 'tungsten')
def d25():
    # Ma turns, side-lit, eyes lowered: "Aaj Rukhsana aayi thi."
    d = D + lg('bgw', [(0, '#e9b86e'), (1, '#5a4026')], 0, 0, 1, 0)
    b = [R(0, 0, W, H, '#14110f'), R(0, 0, 300, H, 'url(#bgw)'), g(R(240, 0, 100, H, '#3a2a1e'), filt='rough')]
    b.append(g(ma_lit(lids=0.75), tf='translate(-80,290) scale(1.08) rotate(5 560 500)', filt='roughS'))
    b.append(vig(0.45))
    return svg(''.join(b), d)

@shot('d26', 'tungsten')
def d26():
    # then she looks straight at him: the question
    d = D + lg('bgw', [(0, '#e9b86e'), (1, '#5a4026')], 0, 0, 1, 0)
    b = [R(0, 0, W, H, '#14110f'), R(0, 0, 300, H, 'url(#bgw)'), g(R(240, 0, 100, H, '#3a2a1e'), filt='rough')]
    b.append(g(ma_lit(lids=0.0, look=3), tf='translate(-300,170) scale(1.4) rotate(2 560 500)', filt='roughS'))
    b.append(vig(0.45))
    return svg(''.join(b), d)

@shot('d27', 'tungsten')
def d27():
    # what she sees: the brass bell in Kabir's hands, the red diary on the cot behind
    b = [room_wall(), pool(540, 900, 600, 500, '#ffd896', 0.35)]
    b.append(g(iron_cot(-80, 1150, 1240, 1.0), filt='b2'))
    b.append(g(ledger_closed(820, 1110, 230, 300, 78), filt='b2'))
    b.append(g(bell(540, 860, 2.0), filt='roughS'))
    b.append(hand(230, 1215, 36, 1.3, 'L', GRIP, 0, thumb=(0.6, 10), sleeve=BLUE, sleeve_rim=BLUE_RIM, **SKIN_K))
    b.append(hand(850, 1215, -36, 1.3, 'R', GRIP, 0, thumb=(0.6, 10), sleeve=BLUE, sleeve_rim=BLUE_RIM, **SKIN_K))
    b.append(vig(0.5))
    return svg(''.join(b), D)

@shot('d28', 'tungsten')
def d28():
    # the secret: the diary's thick front cover with notes tucked in, the bank notice beside it
    b = [S6.wood_grain('#4a3626', '#2a1e14', 18), pool(540, 800, 600, 600, '#ffd896', 0.3)]
    b.append(g(notice_back(560, 300, 440, 620, 8, sums=False).replace('url(#paperw)', '#efede4'), filt='roughS'))
    b.append(note500(150, 640, -12, 1.5)); b.append(note500(190, 700, -4, 1.5)); b.append(note500(170, 760, 6, 1.5))
    b.append(g(ledger_closed(420, 1050, 560, 760, -6), filt='roughS'))
    b.append(vig(0.45))
    return svg(''.join(b), D)

@shot('d29', 'tungsten')
def d29():
    # beside the door: her calendar, today crossed in her own neat pencil, the pencil still swinging
    b = [room_wall(), R(700, 0, 380, H, '#2a2420'), R(740, 0, 340, H, 'url(#doorg)')]
    b.append(g(wall_calendar(160, 380, 1.25, crossed=range(11, 18), today=17, pencil_swing=9), filt='roughS'))
    b.append(pool(400, 700, 500, 500, '#ffd896', 0.25)); b.append(vig(0.45))
    return svg(''.join(b), D)

@shot('d30', 'tungsten')
def d30():
    # her hand on the door frame, steady this time (pilot s31, without the tremble)
    d = D + lg('bg', [(0, '#e9b86e'), (1, '#7a5430')], 0, 0, 1, 0)
    b = [R(0, 0, W, H, '#16120f'), R(620, 0, 460, H, 'url(#bg)')]
    b.append(g(R(470, 0, 180, H, '#4a3524') + R(500, 0, 30, H, '#6a5038') + R(620, 0, 26, H, '#2a1d14'), filt='rough'))
    b.append(hand(380, 1040, 96, 1.7, 'R', {'index': (0.2, 0.5, 0.3), 'middle': (0.2, 0.5, 0.3), 'ring': (0.25, 0.5, 0.3), 'little': (0.3, 0.5, 0.3)}, 2,
                  thumb=(0.8, 0), sleeve='#cfc8b6', sleeve_rim='#efe6d2', forearm=320, **SKIN_M))
    b.append(g(P('M-40,1180 C120,1160 320,1190 470,1260 L470,1920 L-40,1920 Z', '#bdb5a3') + S('M-40,1180 C120,1160 320,1190 470,1260', '#efe6d2', 6, 0.8), filt='roughS'))
    b.append(vig(0.45))
    return svg(''.join(b), d)

@shot('d31', 'tungsten')
def d31():
    # Kabir, eyes down: a lie would have to live in this house
    d = D + rg('bgk', [(0, '#c9a46a'), (0.55, '#4e5a51'), (1, '#1e2420')], 0.2, 0.25, 0.9)
    b = [R(0, 0, W, H, 'url(#bgk)'), bulb(130, 200, -40, 0.8)]
    b.append(g(kabir_eyes_down(lids=0.75) + kabir_kurta(fill=BLUE, edge='#e9c58e', shirt=True), tf='translate(150,460) scale(1.06)', filt='roughS'))
    b.append(vig(0.5))
    return svg(''.join(b), d)

@shot('d32', 'tungsten')
def d32():
    # wide: Ma at the door, Kabir by the cot with the bell, the bulb between them
    d = D + lg('wall', [(0, '#46524b'), (1, '#262d29')])
    b = [R(0, 0, W, H, 'url(#wall)'), R(0, 1340, W, 580, '#2a2825')]
    b.append(R(620, 380, 330, 960, '#1a1512')); b.append(R(650, 410, 270, 930, '#34505a'))
    b.append(g(P('M650,1340 L920,1340 L1060,1920 L560,1920 Z', '#e8b46a', 0.12), filt='b24'))
    b.append(g(f'<path d="{shape("womanc")}" fill="#f6dcab" transform="translate(789,1338) scale(8.6)"/>', filt='b4'))
    b.append(g(f'<path d="{shape("womanc")}" fill="#191614" transform="translate(785,1340) scale(8.6)"/>', filt='roughS'))
    b.append(S('M430,0 L430,300', '#151412', 4)); b.append(g(E(430, 330, 200, 200, '#ffe2a6', 0.4), filt='b40')); b.append(E(430, 330, 18, 24, '#fff3d4'))
    # Kabir seated on the cot edge, back three-quarter silhouette (the cot frame hides his legs)
    kb = ('<path d="M120,1460 C110,1360 120,1250 160,1190 C190,1150 230,1140 250,1130 C236,1110 230,1086 232,1062 C236,1020 268,996 300,1000 '
          'C336,1004 356,1032 352,1070 C350,1094 340,1112 326,1124 C360,1136 400,1160 420,1210 C444,1270 450,1360 440,1460 Z"/>')
    b.append(f'<g fill="#f3d39e" transform="translate(4,-3)">{kb}</g><g fill="#1c2024">{kb}</g>')
    b.append(g(bell(400, 1290, 0.5), filt='roughS'))
    b.append(g(iron_cot(-40, 1440, 640, 1.0, sheet='#5d686a'), filt='roughS'))
    b.append(vig(0.45))
    return svg(''.join(b), d)

@shot('d33', 'tungsten')
def d33():
    # Ma's profile, waiting for his answer
    d = D + lg('bgw', [(0, '#e9b86e'), (1, '#5a4026')], 0, 0, 1, 0)
    b = [R(0, 0, W, H, '#14110f'), R(0, 0, 300, H, 'url(#bgw)'), g(R(240, 0, 100, H, '#3a2a1e'), filt='rough')]
    b.append(g(ma_lit(lids=0.15, look=1), tf='translate(-60,330) scale(1.05) rotate(3 560 500)', filt='roughS'))
    b.append(vig(0.45))
    return svg(''.join(b), d)

@shot('v01', 'neutral')
def v01(): return S6.v01()

if __name__ == '__main__':
    out = sys.argv[1]; ids = sys.argv[2:] or list(SH)
    for i in ids: open(f'{out}/{i}.svg', 'w').write(SH[i]())
    print(' '.join(f'{i}:{GRADE[i]}' for i in ids))
