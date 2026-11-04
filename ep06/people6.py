# Ep6 people: Rukhsana Begum (late 50s, tailor), Dr Gauri Patil (40), plus helpers.
# Profiles are drawn facing LEFT in a ~1100x1500 unit box (crown y~120, chin y~640), like KABIR_PROFILE.
# Use flip=True to face RIGHT (mirrored about x=560).
import sys, math
sys.path.insert(0, '/home/claude/udhaar/scripts')
from shapes import cr_path

_u = [0]
def _id(p): _u[0] += 1; return f'{p}{_u[0]}'

# female face + neck + shoulders, facing LEFT
WFACE = [(470, 150), (430, 178), (404, 222), (392, 276), (388, 322), (393, 352), (386, 378), (372, 410),
         (356, 440), (346, 458), (350, 468), (364, 474), (376, 480), (377, 490), (370, 500), (374, 508),
         (384, 514), (379, 522), (372, 532), (376, 546), (388, 556), (384, 572), (390, 596), (408, 614),
         (442, 626), (476, 632), (494, 660), (500, 720), (496, 790), (470, 850), (380, 920), (300, 990),
         (260, 1100), (240, 1500), (1120, 1500), (1100, 1100), (1000, 960), (860, 880), (720, 820),
         (680, 760), (672, 690), (676, 620), (700, 560), (722, 470), (726, 370), (708, 270), (668, 196), (600, 152), (530, 140)]

def _face_details(o, skin_lo, lip, eye_y=338, eye_x=402, lids=0.0, look=0, age=0.0, brow='#2a1a12'):
    ey = eye_y
    # eye (profile: small almond wedge), lid can lower
    o.append(f'<path d="M{eye_x-8},{ey} C{eye_x+2},{ey-9} {eye_x+18},{ey-9} {eye_x+28},{ey-1} C{eye_x+16},{ey+7} {eye_x+2},{ey+7} {eye_x-8},{ey} Z" fill="#e7d3bb"/>')
    o.append(f'<ellipse cx="{eye_x+2+look}" cy="{ey+1+lids*2}" rx="6.5" ry="{7-lids*2.5}" fill="#1d130e"/>')
    if lids < 0.6: o.append(f'<circle cx="{eye_x+look}" cy="{ey-2}" r="1.8" fill="#fff4dc"/>')
    # upper lid (thicker with lids)
    o.append(f'<path d="M{eye_x-10},{ey-1+lids*4} C{eye_x+2},{ey-12+lids*8} {eye_x+18},{ey-12+lids*8} {eye_x+30},{ey-2+lids*3}" stroke="#2a1a12" stroke-width="{4+lids*2}" fill="none" stroke-linecap="round"/>')
    if lids > 0.2:
        o.append(f'<path d="M{eye_x-9},{ey-1+lids*4} C{eye_x+2},{ey-11+lids*8} {eye_x+18},{ey-11+lids*8} {eye_x+29},{ey-2+lids*3} L{eye_x+30},{ey-10} C{eye_x+16},{ey-18} {eye_x},{ey-16} {eye_x-10},{ey-6} Z" fill="{skin_lo}" fill-opacity="0.35"/>')
    # brow
    o.append(f'<path d="M{eye_x-14},{ey-26} C{eye_x+4},{ey-36} {eye_x+26},{ey-36} {eye_x+44},{ey-28}" stroke="{brow}" stroke-width="6" fill="none" stroke-linecap="round"/>')
    # nostril, lips
    o.append(f'<path d="M360,468 C366,462 374,463 378,470" stroke="{skin_lo}" stroke-width="3.5" fill="none"/>')
    o.append(f'<path d="M372,508 C378,512 384,513 392,512" stroke="#3a2016" stroke-width="3" fill="none"/>')
    o.append(f'<path d="M376,492 C372,500 374,506 384,512 L392,511 C386,504 384,498 380,490 Z" fill="{lip}" fill-opacity="0.75"/>')
    o.append(f'<path d="M372,532 C376,526 384,518 392,514 C388,524 386,532 380,540 Z" fill="{lip}" fill-opacity="0.6"/>')
    if age > 0:
        o.append(f'<path d="M392,478 C412,500 420,526 414,552" stroke="{skin_lo}" stroke-width="3" fill="none" stroke-opacity="{0.35*age+0.1}"/>')
        o.append(f'<path d="M{eye_x+4},{ey+16} C{eye_x+16},{ey+22} {eye_x+30},{ey+20} {eye_x+38},{ey+12}" stroke="{skin_lo}" stroke-width="2.5" fill="none" stroke-opacity="{0.4*age}"/>')
        o.append(f'<path d="M{eye_x+34},{ey+2} L{eye_x+48},{ey-4} M{eye_x+34},{ey+8} L{eye_x+48},{ey+10}" stroke="{skin_lo}" stroke-width="2" fill="none" stroke-opacity="{0.45*age}"/>')
        o.append(f'<path d="M404,626 C430,640 456,642 476,636" stroke="{skin_lo}" stroke-width="3" fill="none" stroke-opacity="{0.3*age}"/>')
    # cheek warmth
    o.append(f'<ellipse cx="470" cy="470" rx="60" ry="44" fill="#c98a66" fill-opacity="0.18" filter="url(#b16)"/>')

def rukhsana(flip=True, lids=0.0, chin=0, glasses='cord', look=0, dupatta='#556f63', dup_hi='#a9c2b0', kameez='#8b6a3e',
             skin_hi='#b07c58', skin_lo='#3a2418', rim='#f5d6a0'):
    """Rukhsana Begum, late 50s: dupatta over hair, measuring tape round neck, spectacles (on cord / on nose)."""
    gid = _id('rsk')
    o = [f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0.12" stop-color="{skin_hi}"/>'
         f'<stop offset="0.55" stop-color="#77492f"/><stop offset="1" stop-color="{skin_lo}"/></linearGradient></defs>']
    face = cr_path(WFACE)
    o.append(f'<path d="{face}" fill="{rim}" transform="translate(-5,-2)"/>')
    o.append(f'<path d="{face}" fill="url(#{gid})"/>')
    # kameez body
    kz = [(470, 850), (380, 920), (300, 990), (260, 1100), (240, 1500), (1120, 1500), (1100, 1100), (1000, 960), (860, 880), (700, 840), (600, 860)]
    o.append(f'<path d="{cr_path(kz)}" fill="{kameez}"/>')
    o.append(f'<path d="M478,852 C520,900 560,930 600,940 C640,930 670,900 690,846" fill="none" stroke="#3a2a18" stroke-width="5" stroke-opacity="0.6"/>')
    # measuring tape round the neck: two strips falling down the front
    o.append(f'<path d="M520,812 C470,880 432,980 420,1120 C414,1240 418,1380 424,1500" stroke="#e6d39a" stroke-width="30" fill="none"/>')
    o.append(f'<path d="M520,812 C470,880 432,980 420,1120 C414,1240 418,1380 424,1500" stroke="#3a3020" stroke-width="30" fill="none" stroke-dasharray="2 12" stroke-opacity="0.55"/>')
    o.append(f'<path d="M640,830 C600,920 580,1040 576,1180 C574,1300 580,1420 586,1500" stroke="#d9c58a" stroke-width="28" fill="none"/>')
    o.append(f'<path d="M640,830 C600,920 580,1040 576,1180 C574,1300 580,1420 586,1500" stroke="#3a3020" stroke-width="28" fill="none" stroke-dasharray="2 12" stroke-opacity="0.5"/>')
    _face_details(o, skin_lo, '#7a3e34', lids=lids, look=look, age=0.8)
    # a few grey strands peeking at the temple
    o.append('<path d="M470,190 C500,180 540,190 560,206 M474,206 C506,198 538,206 556,220" stroke="#cfc6b6" stroke-width="5" fill="none" stroke-opacity="0.8"/>')
    # dupatta over the head and down the back/shoulders
    dp = [(452, 150), (420, 182), (470, 196), (540, 202), (600, 232), (640, 300), (650, 420), (640, 540), (660, 640),
          (700, 740), (780, 830), (900, 900), (1040, 980), (1130, 1080), (1140, 1500), (900, 1500), (860, 1200),
          (790, 1000), (760, 900), (740, 820), (760, 700), (780, 560), (780, 420), (756, 290), (700, 190), (620, 130), (530, 118)]
    o.append(f'<path d="{cr_path(dp)}" fill="{dup_hi}" transform="translate(-6,-3)"/>')
    o.append(f'<path d="{cr_path(dp)}" fill="{dupatta}"/>')
    # dupatta folds + border
    o.append(f'<path d="M430,180 C520,196 600,226 640,300 C660,380 650,500 664,640 C690,760 800,860 1000,960" stroke="#c9b27a" stroke-width="9" fill="none" stroke-opacity="0.75"/>')
    o.append(f'<path d="M700,220 C740,320 760,460 750,600 M820,640 C840,760 900,880 960,1000" stroke="#2c3a33" stroke-width="7" fill="none" stroke-opacity="0.45"/>')
    o.append(''.join(f'<circle cx="{560 + i*38}" cy="{300 + (i%3)*120 + i*40}" r="5" fill="#cfe0d2" fill-opacity="0.35"/>' for i in range(10)))
    # spectacles
    if glasses == 'cord':
        o.append('<path d="M640,640 C620,760 560,880 470,960" stroke="#2a2016" stroke-width="3" fill="none" stroke-opacity="0.8"/>')
        o.append('<g transform="translate(470,980) rotate(-18)"><ellipse cx="0" cy="0" rx="34" ry="24" fill="#fff6e0" fill-opacity="0.18" stroke="#2a2016" stroke-width="5"/>'
                 '<ellipse cx="74" cy="6" rx="32" ry="23" fill="#fff6e0" fill-opacity="0.12" stroke="#2a2016" stroke-width="5"/>'
                 '<path d="M32,0 C40,-6 44,-6 44,2" stroke="#2a2016" stroke-width="5" fill="none"/>'
                 '<ellipse cx="-10" cy="-8" rx="10" ry="4" fill="#ffffff" fill-opacity="0.35"/></g>')
    elif glasses == 'on':
        o.append('<path d="M384,336 L640,330" stroke="#2a2016" stroke-width="5"/>')
        o.append('<ellipse cx="404" cy="344" rx="26" ry="22" fill="#fff6e0" fill-opacity="0.14" stroke="#2a2016" stroke-width="5"/>')
        o.append('<ellipse cx="396" cy="336" rx="8" ry="4" fill="#ffffff" fill-opacity="0.4"/>')
    s = ''.join(o)
    if chin: s = f'<g transform="rotate({chin} 560 700)">{s}</g>'
    if flip: s = f'<g transform="translate(1120,0) scale(-1,1)">{s}</g>'
    return s

def gauri(flip=False, lids=0.0, look=0, skin_hi='#b88563', skin_lo='#3c2519', rim='#e6eef0', hair='#16110e'):
    """Dr Gauri Patil, 40: short bob, plain white coat, stethoscope. Faces LEFT by default."""
    gid = _id('gsk')
    o = [f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0.12" stop-color="{skin_hi}"/>'
         f'<stop offset="0.55" stop-color="#7d5036"/><stop offset="1" stop-color="{skin_lo}"/></linearGradient></defs>']
    face = cr_path(WFACE)
    o.append(f'<path d="{face}" fill="{rim}" transform="translate(-5,-2)"/>')
    o.append(f'<path d="{face}" fill="url(#{gid})"/>')
    # blouse + white coat with lapel
    o.append(f'<path d="{cr_path([(470,850),(380,920),(300,990),(260,1100),(240,1500),(1120,1500),(1100,1100),(1000,960),(860,880),(700,840),(600,860)])}" fill="#d9dcd8"/>')
    o.append('<path d="M470,850 C520,940 560,1060 580,1500 L700,1500 C690,1200 690,1000 700,846 C640,880 560,880 470,850 Z" fill="#5a6470"/>')
    o.append('<path d="M470,850 C520,960 552,1080 566,1500" stroke="#9fa5a3" stroke-width="6" fill="none"/>')
    o.append('<path d="M700,846 C690,1000 692,1200 702,1500" stroke="#9fa5a3" stroke-width="6" fill="none"/>')
    o.append('<path d="M300,990 C340,960 400,930 470,880" stroke="#ffffff" stroke-width="6" fill="none" stroke-opacity="0.6"/>')
    # stethoscope round the neck
    o.append('<path d="M486,790 C470,880 452,980 440,1120 C436,1200 450,1260 500,1270" stroke="#26282c" stroke-width="13" fill="none" stroke-linecap="round"/>')
    o.append('<path d="M676,800 C700,900 720,1000 720,1080" stroke="#26282c" stroke-width="13" fill="none" stroke-linecap="round"/>')
    o.append('<circle cx="512" cy="1272" r="26" fill="#9aa2a6"/><circle cx="512" cy="1272" r="16" fill="#c7cdd0"/>')
    _face_details(o, skin_lo, '#7a4036', lids=lids, look=look, age=0.25, brow='#1d140f')
    # short bob: covers ear, ends at the jaw
    hb = [(446, 168), (420, 200), (410, 250), (430, 228), (470, 214), (520, 214), (580, 236), (610, 300), (616, 400),
          (604, 480), (600, 560), (628, 640), (680, 660), (730, 640), (760, 560), (770, 440), (756, 300), (710, 196), (630, 140), (530, 128)]
    o.append(f'<path d="{cr_path(hb)}" fill="{hair}"/>')
    o.append('<path d="M470,150 C560,128 660,150 720,214" stroke="#6a5a4e" stroke-width="5" fill="none" stroke-opacity="0.6"/>')
    o.append('<path d="M612,320 C622,420 610,520 640,620" stroke="#3a2e26" stroke-width="4" fill="none" stroke-opacity="0.7"/>')
    # small stud earring visible under bob edge
    o.append('<circle cx="626" cy="560" r="5" fill="#e8dcc0"/>')
    s = ''.join(o)
    if flip: s = f'<g transform="translate(1120,0) scale(-1,1)">{s}</g>'
    return s

def kabir_eyes_down(skin_hi='#b07a55', skin_lo='#3a2418', hair='#120e0c', gid=None, lids=0.7):
    """Kabir's locked profile (KABIR_PROFILE/HAIR) with lowered eyelids: facing LEFT."""
    from shapes import KABIR_PROFILE, KABIR_HAIR
    gid = gid or _id('kd')
    face = cr_path(KABIR_PROFILE)
    o = f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0.15" stop-color="{skin_hi}"/><stop offset="0.55" stop-color="#7a4e36"/><stop offset="1" stop-color="{skin_lo}"/></linearGradient></defs>'
    o += f'<path d="{face}" fill="url(#{gid})"/>'
    o += f'<path d="{cr_path(KABIR_HAIR)}" fill="{hair}"/>'
    ly = 378
    o += f'<path d="M346,{ly+2} C356,{ly-2} 372,{ly-2} 384,{ly+2} C372,{ly+7} 356,{ly+7} 346,{ly+2} Z" fill="#e8d6bf"/>'
    o += f'<ellipse cx="354" cy="{ly+4}" rx="7" ry="4" fill="#1d130e"/>'
    o += f'<path d="M342,{ly+1} C356,{ly-6+lids*6} 374,{ly-6+lids*6} 388,{ly+1}" stroke="#2a1a12" stroke-width="5" fill="none"/>'
    o += f'<path d="M343,{ly} C356,{ly-14} 374,{ly-14} 389,{ly} C374,{ly-6+lids*6} 356,{ly-6+lids*6} 343,{ly} Z" fill="#8a5a3e" fill-opacity="0.9"/>'
    o += f'<path d="M336,350 C356,342 380,342 400,350" stroke="#1a110c" stroke-width="9" fill="none" stroke-linecap="round"/>'
    o += '<path d="M300,492 C306,486 314,486 318,492" stroke="#3a2418" stroke-width="4" fill="none"/>'
    o += '<path d="M318,544 C324,548 332,548 340,545" stroke="#4a2a1e" stroke-width="3.5" fill="none"/>'
    o += '<path d="M610,420 C645,405 668,440 656,482 C646,520 620,524 606,506 Z" fill="#5e3b29"/><path d="M622,440 C640,436 648,460 640,482" stroke="#3a2418" stroke-width="4" fill="none"/>'
    o += ''.join(f'<circle cx="{x}" cy="{y}" r="1.6" fill="#2a1a12" fill-opacity="0.22"/>' for x, y in [(350,630),(362,648),(378,662),(396,672),(342,612),(420,640),(440,620),(410,600),(380,610),(460,660)])
    return o
