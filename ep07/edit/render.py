# Ep6 renderer: eased camera per shot, anchored overlays (move with the still), screen overlays, karaoke captions.
# usage: render.py OUT.mp4            or   render.py - 1.0,4.2,...   (stills to /tmp/claude-0/x/f_T.jpg)
import sys, json, re, math, subprocess, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, '/home/claude/udhaar/ep07/edit'); from edl import EDL, DUR, OVERLAYS, ANCHORED, CAP_LOW, CAP_END
FPS = 30; W, H = 1080, 1920; F = '/home/claude/udhaar/fonts/'
ART = '/home/claude/udhaar/ep07/art/final/'
OUT = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/udhaar/ep07/edit/video_noaudio.mp4'
ONLY = [float(t) for t in sys.argv[2].split(',')] if len(sys.argv) > 2 else None
imgs = {}
for s, *_ in EDL:
    if s not in imgs: imgs[s] = np.asarray(Image.open(ART + s + '.png').convert('RGBA'))
IW, IH = 1188, 2112; K = IW / 1080.0
_fc = {}
def font(n, s):
    if (n, s) not in _fc: _fc[(n, s)] = ImageFont.truetype(F + n, s, layout_engine=ImageFont.Layout.RAQM)
    return _fc[(n, s)]
CREAM = (250, 240, 222)
def ease(u): u = min(1, max(0, u)); return u * u * (3 - 2 * u)

# ---------------------------------------------------------------- captions (word times from the recording)
vo = json.load(open('/home/claude/udhaar/ep07/edit/vo_lines.json'))
chunks = []
for l in vo['lines']:
    ws = [(w, t) for w, t in l['words']]
    cur = []; n = 0
    for i, (w_, t_) in enumerate(ws):
        if cur and (len(cur) >= 6 or n + len(w_) > 32): chunks.append([cur[0][1], None, cur, l['end']]); cur = []; n = 0
        cur.append((w_, t_)); n += len(w_) + 1
        if re.search(r'[,.?!…"]$', w_) and len(cur) >= 3 and i < len(ws) - 2: chunks.append([cur[0][1], None, cur, l['end']]); cur = []; n = 0
    if cur:
        if len(cur) <= 2 and chunks and chunks[-1][3] == l['end'] and len(chunks[-1][2]) + len(cur) <= 7: chunks[-1][2] += cur
        else: chunks.append([cur[0][1], None, cur, l['end']])
for k in range(len(chunks)):
    nxt = chunks[k + 1][0] if k + 1 < len(chunks) else CAP_END
    chunks[k][1] = min(nxt - 0.02, max(chunks[k][3], chunks[k][2][-1][1] + 0.4) + 0.5)
CF = font('Mukta-Bold.ttf', 58)
def cap_layer(t):
    c = [ch for ch in chunks if ch[0] - 0.06 <= t < ch[1]]
    if not c or t >= CAP_END: return None
    st, en, ws, _ = c[-1]
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    lines = [[]]
    for w_, tt in ws:
        test = ' '.join(x for x, _ in lines[-1] + [(w_, tt)])
        if d.textlength(test, font=CF) > 860 and lines[-1]: lines.append([])
        lines[-1].append((w_, tt))
    y0 = (1590 if any(a <= t < b for a, b in CAP_LOW) else 1335) - (len(lines) - 1) * 38
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
    ds.rounded_rectangle((90, y0 - 26, W - 90, y0 + len(lines) * 76 + 18), 40, fill=(0, 0, 0, 78))
    for li, ln in enumerate(lines):
        txt = ' '.join(x for x, _ in ln); tw = d.textlength(txt, font=CF); x = (W - tw) / 2; y = y0 + li * 76
        ds.text((x, y + 3), txt, font=CF, fill=(0, 0, 0, 200))
        for w_, tt in ln:
            a = 255 if t >= tt - 0.05 else 120
            d.text((x, y), w_, font=CF, fill=CREAM + (a,), stroke_width=2, stroke_fill=(20, 16, 12, a))
            x += d.textlength(w_ + ' ', font=CF)
    sh = sh.filter(ImageFilter.GaussianBlur(14))
    out = Image.alpha_composite(sh, img)
    fade = min(1, (t - st + 0.06) / 0.12) * min(1, (en - t) / 0.1)
    if fade < 1: out.putalpha(out.getchannel('A').point(lambda v: int(v * max(0, fade))))
    return out

# ---------------------------------------------------------------- anchored overlays (drawn on the still)
PENC = (58, 58, 72)
def anchored(sid, t):
    items = [it for it in ANCHORED.get(sid, []) if t >= it[1]]
    if not items: return None
    lay = Image.new('RGBA', (IW, IH), (0, 0, 0, 0))
    for kind, t0, p in items:
        u = min(1, (t - t0) / max(0.01, p.get('dur', 0.4)))
        if kind == 'circle':
            d = ImageDraw.Draw(lay); cx, cy, rx, ry = (v * K for v in (p['cx'], p['cy'], p['rx'], p['ry']))
            n = int(120 * u); pts = []
            for i in range(n + 1):
                a = -2.2 + 2 * math.pi * 1.08 * i / 120
                r = 1 + 0.06 * math.sin(i * 0.11)
                pts.append((cx + rx * r * math.cos(a), cy + ry * r * math.sin(a)))
            if len(pts) > 1: d.line(pts, fill=(150, 36, 36, 225), width=9, joint='curve')
        elif kind == 'write':
            f = font('Kalam-Bold.ttf' if p.get('bold') else 'Kalam-Regular.ttf', int(p['size'] * K))
            tl = Image.new('RGBA', (int(1000 * K), int(p['size'] * K * 1.9)), (0, 0, 0, 0)); dt = ImageDraw.Draw(tl)
            dt.text((10, int(p['size'] * K * 0.15)), p['text'], font=f, fill=PENC + (235,))
            tw = dt.textlength(p['text'], font=f)
            if p.get('under'):
                yy = int(p['size'] * K * 1.55)
                dt.line((10, yy, 10 + tw, yy + 4), fill=PENC + (220,), width=7); dt.line((20, yy + 16, 10 + tw * 0.96, yy + 18), fill=PENC + (200,), width=5)
            # write-on reveal left -> right
            m = Image.new('L', tl.size, 0); ImageDraw.Draw(m).rectangle((0, 0, int(10 + (tw + 20) * ease(u)), tl.size[1]), fill=255)
            tl.putalpha(Image.fromarray(np.minimum(np.asarray(tl.getchannel('A')), np.asarray(m))))
            if p.get('rot'): tl = tl.rotate(-p['rot'], resample=Image.BICUBIC, expand=True)
            lay.alpha_composite(tl, (int(p['x'] * K), int((p['y'] - p['size'] * 1.1) * K)))
        elif kind == 'hilite':
            hl = Image.new('RGBA', (int(p['w'] * K), int(p['h'] * K)), (255, 214, 90, 0))
            ImageDraw.Draw(hl).rounded_rectangle((0, 0, int(p['w'] * K * ease(u * 2.5)), int(p['h'] * K)), 18, fill=(255, 214, 90, 95))
            hl = hl.rotate(-p['rot'], resample=Image.BICUBIC, expand=True)
            lay.alpha_composite(hl, (int(p['x'] * K), int(p['y'] * K)))
    return lay

# ---------------------------------------------------------------- screen overlays
def shadow_text(lay, xy, txt, f, col, A, blur=10, off=6):
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).text((xy[0], xy[1] + off), txt, font=f, fill=(0, 0, 0, int(A * 0.75)))
    lay = Image.alpha_composite(lay, sh.filter(ImageFilter.GaussianBlur(blur)))
    ImageDraw.Draw(lay).text(xy, txt, font=f, fill=col + (A,)); return lay
def chip(lay, txt, y, A, f=None):
    f = f or font('Mukta-Bold.ttf', 50); d = ImageDraw.Draw(lay); tw = d.textlength(txt, font=f); x = (W - tw) / 2
    bx = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(bx).rounded_rectangle((x - 34, y - 14, x + tw + 34, y + 74), 40, fill=(14, 10, 8, int(A * 0.62)), outline=(250, 238, 214, int(A * 0.5)), width=2)
    lay = Image.alpha_composite(lay, bx); ImageDraw.Draw(lay).text((x, y), txt, font=f, fill=(255, 246, 228, A)); return lay
def ov_layer(t):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); any_ = False
    for kind, a, b, p in OVERLAYS:
        if not (a <= t < b): continue
        any_ = True; k = min(1, (t - a) / 0.25) * min(1, (b - t) / 0.18); A = int(255 * max(0, k))
        d = ImageDraw.Draw(lay)
        if kind == 'status':
            f = font('Mukta-SemiBold.ttf', 27); fb = font('Mukta-Bold.ttf', 27)
            parts = [('DIN', f"{p['day']}/47"), ('QARZ', p['qarz']), ('JAMA', p['jama']), ('SAATH', p['saath'])]
            segs = []
            for i, (k_, v) in enumerate(parts): segs += [(k_ + ' ', f, (235, 222, 200)), (v, fb, (255, 246, 228))] + ([('   |   ', f, (200, 170, 150))] if i < 3 else [])
            tw = sum(d.textlength(t_, font=ff) for t_, ff, _ in segs); x = (W - tw) / 2
            s2 = f"KAL KA FAISLA:  {p['kal']}"; f2 = font('Mukta-Bold.ttf', 30); tw2 = d.textlength(s2, font=f2)
            bar = Image.new('RGBA', (W, H), (0, 0, 0, 0)); db = ImageDraw.Draw(bar)
            db.rounded_rectangle((x - 26, 128, x + tw + 26, 176), 24, fill=(12, 9, 8, int(A * 0.58)))
            db.rounded_rectangle(((W - tw2) / 2 - 22, 192, (W + tw2) / 2 + 22, 240), 24, fill=(12, 9, 8, int(A * 0.5)))
            lay = Image.alpha_composite(lay, bar); d = ImageDraw.Draw(lay)
            for t_, ff, c_ in segs: d.text((x, 134), t_, font=ff, fill=c_ + (A,)); x += d.textlength(t_, font=ff)
            d.line(((W - tw) / 2 - 26, 180, (W + tw) / 2 + 26, 180), fill=(178, 22, 30, int(A * 0.8)), width=2)
            d.text(((W - tw2) / 2, 196), s2, font=f2, fill=(255, 224, 170, A))
        elif kind == 'big':
            u = ease((t - a) / 0.35); f = font('Mukta-ExtraBold.ttf', p['size']); tw = d.textlength(p['text'], font=f)
            lay = shadow_text(lay, ((W - tw) / 2, p['y'] + 30 * (1 - u)), p['text'], f, (250, 238, 214), int(A * u))
            if p.get('sub'):
                f2 = font('Mukta-SemiBold.ttf', 40); s2 = p['sub']; d = ImageDraw.Draw(lay)
                lay = shadow_text(lay, ((W - d.textlength(s2, font=f2)) / 2, p['y'] + 132), s2, f2, (255, 224, 170), int(A * ease((t - a - 0.4) / 0.3)))
        elif kind == 'quote':
            f = font('Kalam-Bold.ttf', p['size'])
            for i, s_ in enumerate(p['lines']):
                ta = a if i == 0 else p['t2']; Ai = int(A * ease((t - ta) / 0.35))
                if Ai <= 0: continue
                tw = d.textlength(s_, font=f)
                lay = shadow_text(lay, ((W - tw) / 2, p['y'] + i * 120), s_, f, (250, 236, 210), Ai, 12, 4); d = ImageDraw.Draw(lay)
        elif kind == 'q47':
            u = ease((t - a) / 0.4); f = font('RozhaOne-Regular.ttf', 230); f2 = font('RozhaOne-Regular.ttf', 120)
            lay = shadow_text(lay, (p['x'] - 130, p['y']), '47', f, (250, 238, 214), int(A * u * 0.92), 14, 8)
            lay = shadow_text(lay, (p['x'] + 130, p['y'] + 92), '?', f2, (255, 224, 170), int(A * ease((t - a - 0.5) / 0.4)), 10, 6)
        elif kind == 'name':
            f = font('RozhaOne-Regular.ttf', 84); f2 = font('Mukta-SemiBold.ttf', 34)
            lay = shadow_text(lay, (80, 1468), p['text'], f, (250, 238, 214), A, 8, 6); d = ImageDraw.Draw(lay)
            d.line((84, 1570, 84 + d.textlength(p['text'], font=f), 1570), fill=(178, 22, 30, A), width=4)
            lay = shadow_text(lay, (84, 1578), p['sub'], f2, (250, 238, 214), int(A * 0.92), 6, 4)
        elif kind == 'chip':
            lay = chip(lay, p['text'], p['y'], A)
        elif kind == 'cmp':
            for i, (lab, amt, sub) in enumerate((p['a'], p['b'])):
                ta = a if i == 0 else p['t2']; Ai = int(A * ease((t - ta) / 0.3))
                if Ai <= 0: continue
                x0 = 70 + i * 480; y0 = 250
                bx = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(bx).rounded_rectangle((x0, y0, x0 + 460, y0 + 236), 34, fill=(14, 10, 8, int(Ai * 0.66)), outline=(250, 238, 214, int(Ai * 0.55)), width=3)
                lay = Image.alpha_composite(lay, bx); d = ImageDraw.Draw(lay)
                fl = font('Mukta-SemiBold.ttf', 34); fa = font('Mukta-ExtraBold.ttf', 92); fs = font('Mukta-Medium.ttf', 32)
                for s_, ff, yy, col in ((lab, fl, y0 + 18, (255, 224, 170)), (amt, fa, y0 + 56, (255, 246, 228)), (sub, fs, y0 + 178, (235, 222, 200))):
                    d.text((x0 + 230 - d.textlength(s_, font=ff) / 2, yy), s_, font=ff, fill=col + (Ai,))
            if t >= p['t2'] + 0.2:
                fv = font('Mukta-Bold.ttf', 40); d.text((W / 2 - d.textlength('vs', font=fv) / 2, 340), 'vs', font=fv, fill=(255, 224, 170, A))
        elif kind == 'vote':
            k2 = ease((t - a) / 0.5); A2 = int(255 * k2)
            f0 = font('Mukta-SemiBold.ttf', 40); s0 = f"DIN {p['day']} KA FAISLA  ·  AAPKA"; d.text(((W - d.textlength(s0, font=f0)) / 2, 270), s0, font=f0, fill=(250, 230, 200, A2))
            fq = font('Mukta-Bold.ttf', 56)
            for i, sq in enumerate(p['q']):
                d.text(((W - d.textlength(sq, font=fq)) / 2, 340 + i * 70), sq, font=fq, fill=(255, 246, 228, A2))
            fb_ = font('Mukta-ExtraBold.ttf', 112); fs = font('Mukta-Medium.ttf', 34)
            for j, ((lab, sub), y) in enumerate(((p['a'], 560), (p['b'], 890))):
                kk = ease((t - a - 0.25 - j * 0.2) / 0.4); Aj = int(255 * kk)
                box = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(box).rounded_rectangle((110, y, 970, y + 270), 40, fill=(250, 238, 214, int(Aj * 0.12)), outline=(250, 238, 214, int(Aj * 0.85)), width=4)
                lay = Image.alpha_composite(lay, box); d = ImageDraw.Draw(lay)
                d.text(((W - d.textlength(lab, font=fb_)) / 2, y + 28), lab, font=fb_, fill=(255, 246, 228, Aj))
                d.text(((W - d.textlength(sub, font=fs)) / 2, y + 192), sub, font=fs, fill=(250, 230, 200, Aj))
            k3 = ease((t - a - 1.0) / 0.5); A3 = int(255 * k3)
            fc = font('Mukta-Bold.ttf', 50); sc = f"Comment karo: {p['a'][0]} ya {p['b'][0]}"; d.text(((W - d.textlength(sc, font=fc)) / 2, 1236), sc, font=fc, fill=(255, 224, 170, A3))
            fr = font('Mukta-Medium.ttf', 31)
            for i, s_ in enumerate(['Ek account, ek vote. Pehla valid comment hi ginega.', f"Tie hua toh Papa ka ek rupaye ka sikka: heads = {p['tie']}."]):
                d.text(((W - d.textlength(s_, font=fr)) / 2, 1318 + i * 46), s_, font=fr, fill=(250, 238, 214, int(A3 * 0.85)))
            fe = font('Mukta-Bold.ttf', 44); se = f"EPISODE {p['next']}  ·  KAL"; d.text(((W - d.textlength(se, font=fe)) / 2, 1470), se, font=fe, fill=(255, 224, 170, A3))
    return lay if any_ else None

# ---------------------------------------------------------------- camera
def shot_frame(i, t):
    s, a, b, mo = EDL[i]
    im = imgs[s]
    lay = anchored(s, t)
    if lay is not None:
        im = np.asarray(Image.alpha_composite(Image.fromarray(im), lay))
    u = ease((t - a) / (b - a)) * 0.35 + min(1, max(0, (t - a) / (b - a))) * 0.65
    z0, z1, fx0, fy0, fx1, fy1 = mo
    z = z0 + (z1 - z0) * u; fx = fx0 + (fx1 - fx0) * u; fy = fy0 + (fy1 - fy0) * u
    cw, chh = IW / (1.1 * z), IH / (1.1 * z)
    cx = min(max(fx * IW, cw / 2), IW - cw / 2); cy = min(max(fy * IH, chh / 2), IH - chh / 2)
    sx, sy = cx - cw / 2, cy - chh / 2
    M = np.array([[W / cw, 0, -sx * W / cw], [0, H / chh, -sy * H / chh]], np.float32)
    rgb = cv2.warpAffine(im[..., :3], M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
    return rgb.astype(np.float32) / 255

rng = np.random.default_rng(1)
GR = [cv2.GaussianBlur(rng.normal(0, 1, (H // 2, W // 2)).astype(np.float32), (0, 0), 0.6) for _ in range(12)]
def frame(t):
    i = max(j for j, e in enumerate(EDL) if e[1] <= t or j == 0)
    a = EDL[i][1]; f = shot_frame(i, t)
    XF = 0.14
    if i > 0 and t - a < XF:
        pf = shot_frame(i - 1, t); k = ease((t - a) / XF); f = pf * (1 - k) + f * k
    if t < 0.3: f = f * (t / 0.3)
    if t > DUR - 0.5: f = f * max(0, (DUR - t) / 0.5)
    g = cv2.resize(GR[int(t * FPS) % 12], (W, H))
    f = np.clip(f + g[..., None] * 0.02, 0, 1)
    out = Image.fromarray((f * 255).astype(np.uint8)).convert('RGBA')
    o = ov_layer(t)
    if o: out = Image.alpha_composite(out, o)
    c = cap_layer(t)
    if c: out = Image.alpha_composite(out, c)
    return np.asarray(out.convert('RGB'))

if ONLY:
    for t in ONLY: Image.fromarray(frame(t)).save(f'/tmp/claude-0/x/f_{t:.2f}.jpg', quality=85)
    sys.exit()
N = int(DUR * FPS)
p = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                      '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', '-pix_fmt', 'yuv420p', OUT], stdin=subprocess.PIPE)
for n in range(N):
    p.stdin.write(frame(n / FPS).tobytes())
    if n % 300 == 0: print('frame', n, '/', N, flush=True)
p.stdin.close(); p.wait(); print('done', OUT)
