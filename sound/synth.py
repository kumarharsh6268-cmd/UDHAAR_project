"""UDHAAR sound synthesis library. Everything generated from scratch. 48 kHz float32.
Mono functions return 1-D arrays; beds return (N,2) stereo arrays."""
import numpy as np
import scipy.signal as ss

SR = 48000
RNG = np.random.default_rng(47)


# ---------------------------------------------------------------- helpers
def t_(dur):
    return np.arange(int(dur * SR)) / SR


def noise(n, rng=RNG):
    return rng.standard_normal(n).astype(np.float32)


def sos_bp(lo, hi, order=2):
    return ss.butter(order, [lo, hi], 'bandpass', fs=SR, output='sos')


def sos_lp(f, order=2):
    return ss.butter(order, f, 'lowpass', fs=SR, output='sos')


def sos_hp(f, order=2):
    return ss.butter(order, f, 'highpass', fs=SR, output='sos')


def filt(sos, x):
    return ss.sosfilt(sos, x).astype(np.float32)


def peak(x, f, q=8.0, gain=1.0):
    b, a = ss.iirpeak(f, q, fs=SR)
    return (ss.lfilter(b, a, x) * gain).astype(np.float32)


def env_ad(n, a, d, curve=4.0):
    """attack seconds then exponential decay time-constant d (s)"""
    t = np.arange(n) / SR
    e = np.where(t < a, (t / max(a, 1e-4)) ** 1.5, np.exp(-(t - a) / max(d, 1e-4)))
    return e.astype(np.float32)


def smooth_rand(n, rate_hz, rng=RNG, lo=0.0, hi=1.0):
    """smooth random control signal in [lo,hi] varying at about rate_hz"""
    k = max(4, int(n / SR * rate_hz) + 4)
    pts = rng.uniform(lo, hi, k)
    x = np.interp(np.linspace(0, k - 1, n), np.arange(k), pts)
    w = max(1, int(SR / max(rate_hz, 1e-3) / 2))
    if w > 1 and n > 2 * w:
        c = np.cumsum(np.concatenate([np.full(w, x[0]), x, np.full(w, x[-1])]))
        x = (c[2 * w:2 * w + n] - c[w:w + n]) / w
    return x.astype(np.float32)


def norm(x, peak_db=-1.0):
    m = np.max(np.abs(x)) + 1e-12
    return (x / m * 10 ** (peak_db / 20)).astype(np.float32)


def db(x):
    return 10 ** (x / 20)


def fade(x, fi=0.01, fo=0.05):
    x = x.copy()
    a, b = int(fi * SR), int(fo * SR)
    if a: x[:a] *= np.linspace(0, 1, a)[:, None] if x.ndim == 2 else np.linspace(0, 1, a)
    if b: x[-b:] *= np.linspace(1, 0, b)[:, None] if x.ndim == 2 else np.linspace(1, 0, b)
    return x


def pan(x, p=0.0):
    """p -1..1 equal-power"""
    a = (p + 1) * np.pi / 4
    return np.stack([x * np.cos(a), x * np.sin(a)], 1).astype(np.float32)


def place(buf, x, t0, gain=1.0):
    """add stereo or mono x into stereo buf at time t0 seconds"""
    i = int(round(t0 * SR))
    if x.ndim == 1:
        x = pan(x, 0)
    if i < 0:
        x = x[-i:]; i = 0
    n = min(len(x), len(buf) - i)
    if n > 0:
        buf[i:i + n] += x[:n] * gain


def reverb_ir(dur=1.6, decay=0.45, bright=5000, pre=0.012, rng=None):
    rng = rng or np.random.default_rng(3)
    n = int(dur * SR)
    t = np.arange(n) / SR
    L = filt(sos_lp(bright), noise(n, rng)) * np.exp(-t / decay)
    R = filt(sos_lp(bright), noise(n, rng)) * np.exp(-t / decay)
    p = int(pre * SR)
    ir = np.zeros((n + p, 2), np.float32)
    ir[p:, 0] = L; ir[p:, 1] = R
    ir /= np.sqrt((ir ** 2).sum(0)) + 1e-9
    return ir


def reverb(x, wet=0.25, ir=None):
    """mono in -> mono out (summed tail); stereo in -> stereo out"""
    ir = reverb_ir() if ir is None else ir
    if x.ndim == 1:
        y = 0.5 * (ss.fftconvolve(x, ir[:, 0])[:len(x)] + ss.fftconvolve(x, ir[:, 1])[:len(x)]) * 1.2
        return ((1 - wet) * x + wet * y).astype(np.float32)
    y = np.stack([ss.fftconvolve(x[:, c], ir[:, c])[:len(x)] for c in range(2)], 1)
    return ((1 - wet) * x + wet * y).astype(np.float32)

def reverb_st(x, wet=0.25, ir=None):
    """mono in -> stereo out with decorrelated tails"""
    ir = reverb_ir() if ir is None else ir
    y = np.stack([ss.fftconvolve(x, ir[:, c])[:len(x)] for c in range(2)], 1)
    return ((1 - wet) * x[:, None] + wet * y).astype(np.float32)


def loop_xfade(x, xf=1.0):
    """make a stereo/mono bed loopable by crossfading its tail into its head"""
    n = int(xf * SR)
    head, body, tail = x[:n], x[n:-n], x[-n:]
    w = np.linspace(0, 1, n)
    if x.ndim == 2: w = w[:, None]
    seam = tail * (1 - w) + head * w
    return np.concatenate([body, seam]).astype(np.float32)


# ---------------------------------------------------------------- bell
def bell_strike(f0=1320.0, dur=4.8, hard=1.0, rng=RNG):
    """small brass bus bell: inharmonic partials with beating doublets"""
    t = t_(dur)
    ratios = [0.505, 1.0, 1.183, 1.506, 2.0, 2.514, 2.75, 3.76, 4.07, 5.2, 6.3]
    amps = [0.20, 1.0, 0.55, 0.42, 0.50, 0.30, 0.22, 0.18, 0.12, 0.08, 0.05]
    decs = [2.6, 2.0, 1.5, 1.2, 0.95, 0.7, 0.62, 0.42, 0.36, 0.25, 0.18]
    y = np.zeros_like(t, dtype=np.float32)
    for r, a, d in zip(ratios, amps, decs):
        f = f0 * r
        if f > 20000: continue
        det = 1 + rng.uniform(0.0008, 0.0025)
        ph = rng.uniform(0, 2 * np.pi, 2)
        e = np.exp(-t / (d * (0.85 + 0.3 * rng.random())))
        y += a * e * (np.sin(2 * np.pi * f * t + ph[0]) + 0.6 * np.sin(2 * np.pi * f * det * t + ph[1])) / 1.6
    # strike transient
    n = int(0.012 * SR)
    tr = filt(sos_bp(2500, 9000), noise(n, rng)) * np.linspace(1, 0, n) ** 2 * 0.6 * hard
    y[:n] += tr
    y *= np.minimum(1, t / 0.0015) * np.clip((dur - t) / 1.2, 0, 1) ** 2
    return norm(y, -1)


def bell_dingding(gap=0.28, f0=1320.0):
    a = bell_strike(f0, 4.8, 1.0)
    b = bell_strike(f0 * 1.0015, 4.8, 0.85) * 0.82
    out = np.zeros(int((gap + 4.8) * SR), np.float32)
    out[:len(a)] += a
    i = int(gap * SR)
    out[i:i + len(b)] += b
    # the second strike partly damps the first ring
    out = reverb(out, 0.18, reverb_ir(1.2, 0.3, 7000))
    return norm(out, -1)


def bell_clink():
    """bell bumped inside the trunk: soft, partly muffled by cloth"""
    a = bell_strike(1320, 2.2, 0.4)
    a = filt(sos_lp(4200), a) * env_ad(len(a), 0.001, 0.55)
    # little rattle of the clapper
    r = np.zeros_like(a)
    for k, dt in enumerate([0.07, 0.115, 0.15]):
        r[int(dt * SR):] += bell_strike(1320, 2.2 - dt, 0.15)[:len(a) - int(dt * SR)] * (0.25 / (k + 1))
    y = a + filt(sos_lp(3500), r) * env_ad(len(a), 0.001, 0.4)
    return norm(reverb(y, 0.12, reverb_ir(0.6, 0.15, 5000)), -3)


# ---------------------------------------------------------------- nature / ambience elements
def kite_call(rng=RNG):
    """black kite whistle: descending tremulous 'cheeee-l-l-l'"""
    d = rng.uniform(1.0, 1.5)
    t = t_(d)
    f = 3400 - 1300 * (t / d) ** 0.7
    trem = 1 + 0.06 * np.sin(2 * np.pi * rng.uniform(16, 22) * t) * (t / d)
    ph = 2 * np.pi * np.cumsum(f * trem) / SR
    y = np.sin(ph) + 0.25 * np.sin(2 * ph)
    e = np.minimum(1, t / 0.08) * np.exp(-((t - 0.25 * d) / (0.5 * d)) ** 2 * 0.8) * (1 - t / d) ** 0.5
    return (y * e).astype(np.float32)


def crow_caw(rng=RNG):
    d = rng.uniform(0.32, 0.45)
    t = t_(d)
    f0 = rng.uniform(520, 640) * (1 - 0.12 * t / d)
    ph = 2 * np.pi * np.cumsum(f0) / SR
    src = np.sign(np.sin(ph)) * 0.5 + 0.5 * np.sin(ph * 2)
    src += 0.35 * noise(len(t), rng)
    y = peak(src, 1150, 4) + peak(src, 2300, 5) * 0.6
    e = np.minimum(1, t / 0.025) * np.exp(-t / (d * 0.55))
    return (y * e).astype(np.float32)


def sparrow_chirp(rng=RNG):
    d = rng.uniform(0.05, 0.12)
    t = t_(d)
    f = rng.uniform(3800, 5200) + rng.uniform(-1500, 1500) * (t / d)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / d) ** 2
    return y.astype(np.float32)


def crackle(dur, density=6.0, rng=RNG):
    n = int(dur * SR)
    y = np.zeros(n, np.float32)
    k = rng.poisson(density * dur)
    pos = rng.integers(0, n - 2000, k)
    for p in pos:
        L = int(rng.uniform(0.002, 0.012) * SR)
        burst = noise(L, rng) * np.exp(-np.arange(L) / (L * 0.25)) * rng.uniform(0.2, 1.0) ** 2
        y[p:p + L] += burst
    y = filt(sos_bp(700, 7000), y)
    # soft fire roar
    y += filt(sos_lp(350, 4), noise(n, rng)) * 0.08 * (0.6 + 0.4 * smooth_rand(n, 0.7, rng))
    return y


def wind(dur, rng=RNG, lo=80, hi=900):
    n = int(dur * SR)
    out = []
    for c in range(2):
        x = filt(sos_lp(hi, 4), filt(sos_hp(lo, 2), noise(n, rng)))
        g = 0.35 + 0.65 * smooth_rand(n, 0.25, rng) ** 2
        sweep = filt(sos_lp(1600, 4), filt(sos_hp(300, 2), noise(n, rng))) * 0.25 * smooth_rand(n, 0.15, rng)
        out.append(x * g + sweep * g)
    return np.stack(out, 1).astype(np.float32)


def murmur(dur, rng=RNG):
    """distant low murmur of people: syllabic-modulated formant noise, very lowpassed"""
    n = int(dur * SR)
    y = np.zeros(n, np.float32)
    for v in range(6):
        src = noise(n, rng)
        syl = np.clip(filt(sos_lp(5), noise(n, rng)) * 6, 0, None)
        f1, f2 = rng.uniform(350, 650), rng.uniform(1000, 1600)
        y += (peak(src, f1, 3) + 0.5 * peak(src, f2, 4)) * syl * (0.4 + 0.6 * smooth_rand(n, 0.1, rng))
    y = filt(sos_lp(900), y)
    return y


def bed_dawn(dur=40.0, seed=1):
    rng = np.random.default_rng(seed)
    n = int(dur * SR)
    bed = wind(dur, rng) * 0.32
    m = murmur(dur, rng)
    bed += np.stack([m * 0.55, filt(sos_lp(800), np.roll(m, 4800)) * 0.5], 1) * 0.10
    cr = crackle(dur, 4.0, rng)
    bed += pan(cr, -0.35) * 0.08
    # distant birds, sparse
    t = 1.5
    while t < dur - 2:
        if rng.random() < 0.55:
            c = kite_call(rng); p = rng.uniform(-0.8, 0.8); g = 0.035
        else:
            c = np.concatenate([crow_caw(rng), np.zeros(int(0.12 * SR), np.float32), crow_caw(rng)]) if rng.random() < 0.6 else crow_caw(rng)
            p = rng.uniform(-0.9, 0.9); g = 0.03
        c = filt(sos_lp(5000), c)
        place(bed, reverb_st(c * 0.7, 0.55, reverb_ir(2.5, 0.8, 4000, 0.04, rng)) * np.array([[1 - 0.5 * p, 1 + 0.5 * p]], np.float32), t, g)
        t += rng.uniform(3.5, 8.0)
    return bed.astype(np.float32)


def cricket_chirps(dur, rng=RNG):
    n = int(dur * SR)
    y = np.zeros(n, np.float32)
    t = t_(dur)
    for k in range(3):  # three crickets at different distances
        f = rng.uniform(4300, 5200)
        car = np.sin(2 * np.pi * f * t + rng.uniform(0, 6))
        rate = rng.uniform(1.4, 2.4)  # chirps per second
        period = 1 / rate
        ph = (t + rng.uniform(0, 1)) % period
        nb = rng.integers(3, 5)
        pulse = (ph < nb * 0.022) * (np.sin(np.pi * (ph % 0.022) / 0.022) ** 2)
        gate = (smooth_rand(n, 0.08, rng) > 0.35).astype(np.float32)
        gate = filt(sos_lp(2), gate)
        y += car * pulse * gate * rng.uniform(0.3, 1.0)
    return filt(sos_bp(3000, 8000), y)


def dog_bark_far(rng=RNG):
    out = []
    for i in range(2):
        d = 0.22
        t = t_(d)
        f0 = 420 * (1 + 0.3 * np.sin(np.pi * t / d))
        ph = 2 * np.pi * np.cumsum(f0) / SR
        src = np.tanh(3 * np.sin(ph)) + 0.4 * noise(len(t), rng)
        y = peak(src, 900, 3) + 0.5 * peak(src, 1800, 4)
        y *= np.sin(np.pi * t / d) ** 0.6 * np.exp(-t / 0.15)
        out += [y, np.zeros(int(0.25 * SR), np.float32)]
    y = filt(sos_lp(1800), np.concatenate(out))
    return reverb(y, 0.6, reverb_ir(2.0, 0.7, 2500, 0.05))


def bed_night_room(dur=40.0, seed=2, dog_at=None):
    rng = np.random.default_rng(seed)
    n = int(dur * SR)
    t = t_(dur)
    hum = (np.sin(2 * np.pi * 50 * t) * 0.5 + np.sin(2 * np.pi * 100 * t) * 0.35 + np.sin(2 * np.pi * 150 * t) * 0.12)
    hum *= 0.9 + 0.1 * smooth_rand(n, 0.2, rng)
    room = filt(sos_lp(700, 4), noise(n, rng)) * 0.12
    bed = np.stack([hum * 0.05 + room, hum * 0.05 + filt(sos_lp(700, 4), noise(n, rng)) * 0.12], 1)
    cr = cricket_chirps(dur, rng)
    bed += np.stack([cr * 0.6, np.roll(cr, 3000) * 0.45], 1) * 0.05
    if dog_at is not None and dog_at < dur - 2:
        place(bed, pan(dog_bark_far(rng), -0.6), dog_at, 0.03)
    return bed.astype(np.float32)


def clock_tick(tock=False, rng=RNG):
    n = int(0.09 * SR)
    x = noise(n, rng) * np.exp(-np.arange(n) / (0.0018 * SR))
    f = 2700 if not tock else 2250
    y = peak(x, f, 14) * 1.0 + peak(x, f * 1.9, 18) * 0.5 + filt(sos_bp(600, 1400), x) * 0.4
    body = np.sin(2 * np.pi * 820 * np.arange(n) / SR) * np.exp(-np.arange(n) / (0.012 * SR)) * 0.25
    y = (y + body) * env_ad(n, 0.0003, 0.02)
    return norm(reverb(y, 0.15, reverb_ir(0.5, 0.12, 6000)), -6)


def clock_ticks(dur, rate=1.0, start_tock=False):
    """one tick per second (rate in ticks/s); returns stereo"""
    n = int(dur * SR)
    buf = np.zeros((n, 2), np.float32)
    k = 0
    tt = 0.0
    while tt < dur - 0.1:
        place(buf, clock_tick((k % 2 == 1) ^ start_tock), tt, 1.0)
        tt += 1.0 / rate; k += 1
    return buf


def bed_morning_lane(dur=12.0, seed=3, bus_at=2.0):
    rng = np.random.default_rng(seed)
    n = int(dur * SR)
    bed = wind(dur, rng, 100, 2000) * 0.12
    # sparrows
    t = 0.3
    while t < dur - 0.5:
        k = rng.integers(2, 6); p = rng.uniform(-0.9, 0.9)
        for j in range(k):
            place(bed, pan(filt(sos_lp(7000), sparrow_chirp(rng)), p), t + j * rng.uniform(0.08, 0.16), 0.05)
        t += rng.uniform(0.6, 2.0)
    # distant scooter pass
    place(bed, scooter_pass(5.0, rng), 0.4, 0.05)
    # municipal bus passing + far horn
    if bus_at is not None:
        place(bed, bus_pass(7.0, rng), bus_at, 0.20)
        place(bed, horn_far(rng), bus_at + 5.2, 0.05)
    return bed.astype(np.float32)


def scooter_pass(dur=5.0, rng=RNG):
    t = t_(dur)
    x = (t / dur - 0.5) * 2  # -1..1
    dop = 1 + 0.04 * (-x)
    f = 58 * dop * (1 + 0.03 * np.sin(2 * np.pi * 3 * t))
    ph = 2 * np.pi * np.cumsum(f) / SR
    src = sum(np.sin(k * ph) / k ** 0.8 for k in range(1, 14)) + 0.3 * noise(len(t), rng)
    src = filt(sos_bp(80, 2500), src)
    amp = 1 / (1 + 6 * x ** 2)
    y = src * amp
    return np.stack([y * (0.5 - 0.4 * x), y * (0.5 + 0.4 * x)], 1).astype(np.float32)


def bus_pass(dur=7.0, rng=RNG):
    """old diesel municipal bus passing at the end of the lane"""
    t = t_(dur)
    x = (t / dur - 0.45) * 2.2
    dop = 1 + 0.03 * (-np.tanh(2 * x))
    f = 34 * dop * (1 + 0.04 * smooth_rand(len(t), 0.5, rng))
    ph = 2 * np.pi * np.cumsum(f) / SR
    eng = sum(np.sin(k * ph + rng.uniform(0, 6)) / k ** 0.6 for k in range(1, 30))
    knock = filt(sos_bp(150, 900), noise(len(t), rng)) * (0.5 + 0.5 * np.sin(ph * 0.5) ** 8)
    tyre = filt(sos_bp(300, 3000), noise(len(t), rng)) * 0.6
    rattle = filt(sos_bp(1500, 5000), noise(len(t), rng)) * (smooth_rand(len(t), 8, rng) > 0.7) * 0.4
    y = filt(sos_lp(3000), eng * 0.5 + knock * 0.6 + tyre + rattle)
    amp = 1 / (1 + 4 * x ** 2)
    y = y * amp
    st = np.stack([y * (0.55 - 0.35 * np.tanh(x)), y * (0.55 + 0.35 * np.tanh(x))], 1)
    return norm(reverb(st, 0.2, reverb_ir(1.5, 0.4, 3000, 0.02)), -3)


def horn_far(rng=RNG):
    d = 0.7
    t = t_(d)
    y = np.zeros_like(t)
    for f in (405, 508):
        ph = 2 * np.pi * f * t
        y += np.tanh(2.5 * np.sin(ph)) * 0.5
    y = filt(sos_bp(300, 2500), y) * np.minimum(1, t / 0.02) * np.minimum(1, (d - t) / 0.08)
    return norm(reverb(filt(sos_lp(2000), y), 0.6, reverb_ir(2.5, 0.8, 2500, 0.08)), -6)


# ---------------------------------------------------------------- foley
def friction(dur, lo, hi, rate=12, rng=RNG, rough=0.6):
    n = int(dur * SR)
    x = filt(sos_bp(lo, hi), noise(n, rng))
    jitter = np.clip(1 - rough + rough * filt(sos_lp(rate), noise(n, rng)) * 4, 0, None)
    return (x * jitter).astype(np.float32)


def metal_hit(f0=900, dur=0.35, rng=RNG, damp=0.08):
    t = t_(dur)
    y = np.zeros_like(t)
    for r, a in [(1, 1), (1.62, 0.6), (2.31, 0.45), (3.4, 0.3), (4.7, 0.2)]:
        y += a * np.sin(2 * np.pi * f0 * r * t + rng.uniform(0, 6)) * np.exp(-t / (damp / r ** 0.3))
    n = int(0.004 * SR)
    y[:n] += noise(n, rng) * np.linspace(1, 0, n) * 0.8
    return y.astype(np.float32)


def creak(dur=0.9, f_start=60, f_end=140, res=(700, 1400, 2600), rng=RNG):
    """stick-slip hinge/wood creak: impulse train with wandering rate through resonances"""
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = f_start + (f_end - f_start) * (t / dur) + 15 * smooth_rand(n, 6, rng)
    ph = np.cumsum(f) / SR
    imp = np.diff(np.floor(ph), prepend=0).astype(np.float32) * rng.uniform(0.6, 1.0, n).astype(np.float32)
    y = sum(peak(imp, r, 12) * (1 / (i + 1)) for i, r in enumerate(res))
    e = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 0.7
    return (y * e).astype(np.float32)


def trunk_open(rng=None):
    """drag tin trunk out (0-1.4s), latch clack x2 (1.7, 1.95s), lid hinge creak (2.2-3.3s), lid thump"""
    rng = rng or np.random.default_rng(11)
    out = np.zeros(int(3.8 * SR), np.float32)
    drag = friction(1.3, 120, 1800, 18, rng, 0.8) * 0.5 + friction(1.3, 1800, 5000, 30, rng, 0.9) * 0.12
    drag += filt(sos_lp(200), noise(len(drag), rng)) * 0.3
    drag *= np.sin(np.pi * np.linspace(0, 1, len(drag))) ** 0.5
    # tin body resonance under drag
    drag = drag + peak(drag, 420, 10) * 0.5 + peak(drag, 1130, 14) * 0.3
    out[:len(drag)] += drag
    for tt, f in [(1.7, 1650), (1.95, 1500)]:
        h = metal_hit(f, 0.3, rng, 0.04) * 0.9
        i = int(tt * SR); out[i:i + len(h)] += h
    c = creak(1.1, 40, 110, (520, 1250, 2900), rng) * 0.6
    i = int(2.2 * SR); out[i:i + len(c)] += c
    th = filt(sos_lp(300), noise(int(0.2 * SR), rng)) * env_ad(int(0.2 * SR), 0.002, 0.04) * 0.9
    th += metal_hit(380, 0.2, rng, 0.05)[:len(th)] * 0.3
    i = int(3.35 * SR); out[i:i + len(th)] += th
    return norm(reverb(out, 0.18, reverb_ir(0.9, 0.22, 5000)), -3)


def latch_clack(rng=RNG):
    return norm(reverb(metal_hit(1600, 0.3, rng, 0.04), 0.15, reverb_ir(0.8, 0.2)), -3)


def cloth_rustle(dur=0.9, rng=RNG):
    n = int(dur * SR)
    x = filt(sos_bp(700, 6000), noise(n, rng))
    g = np.clip(filt(sos_lp(14), noise(n, rng)) * 5, 0, None) ** 1.3
    e = np.sin(np.pi * np.linspace(0, 1, n)) ** 0.8
    return norm(x * g * e, -6)


def page_turn(variant=0):
    rng = np.random.default_rng(100 + variant)
    d = [0.55, 0.7, 0.45, 0.85][variant % 4]
    n = int(d * SR)
    t = np.arange(n) / SR
    sw = filt(sos_bp(900, 9000), noise(n, rng))
    swish = np.exp(-((t - d * 0.45) / (d * 0.22)) ** 2)
    flutter = 1 + 0.6 * np.sin(2 * np.pi * rng.uniform(25, 45) * t) * swish
    snap_n = int(0.02 * SR)
    y = sw * swish * flutter * 0.6
    j = int(d * 0.72 * SR)
    y[j:j + snap_n] += filt(sos_bp(1500, 7000), noise(snap_n, rng)) * np.exp(-np.arange(snap_n) / (0.003 * SR)) * 1.2
    y[:int(0.03 * SR)] += filt(sos_bp(2000, 8000), noise(int(0.03 * SR), rng)) * 0.3
    return norm(reverb(y, 0.1, reverb_ir(0.4, 0.1, 8000)), -6)


def page_flutter(n_pages=8, rng=None):
    rng = rng or np.random.default_rng(9)
    out = np.zeros(int((0.12 * n_pages + 0.8) * SR), np.float32)
    for k in range(n_pages):
        p = page_turn(k)[: int(0.35 * SR)] * np.linspace(1, 0, int(0.35 * SR)) * (0.5 + 0.5 * rng.random())
        i = int(k * 0.12 * SR); out[i:i + len(p)] += p
    return norm(out, -6)


def paper_handle(dur=1.2, rng=RNG):
    n = int(dur * SR)
    x = filt(sos_bp(1200, 9000), noise(n, rng))
    g = np.clip(filt(sos_lp(10), noise(n, rng)) * 6 - 0.3, 0, None) ** 1.5
    # sharp crinkles
    k = rng.poisson(14 * dur); pos = rng.integers(0, n - 500, k)
    cr = np.zeros(n, np.float32)
    for p in pos:
        L = int(rng.uniform(0.001, 0.004) * SR); cr[p:p + L] += noise(L, rng) * rng.uniform(0.3, 1)
    y = x * g * 0.6 + filt(sos_bp(2000, 10000), cr)
    return norm(y * np.sin(np.pi * np.linspace(0, 1, n)) ** 0.4, -6)


def paper_tear(dur=1.1, rng=None):
    rng = rng or np.random.default_rng(21)
    n = int(dur * SR)
    t = np.arange(n) / SR
    rate = 300 + 1700 * np.sin(np.pi * t / dur)
    ph = np.cumsum(rate * (0.6 + 0.8 * rng.random(n))) / SR
    imp = np.diff(np.floor(ph), prepend=0).astype(np.float32) * rng.uniform(0.2, 1, n).astype(np.float32)
    y = filt(sos_bp(1200, 8000), imp) * 2 + filt(sos_bp(500, 4000), noise(n, rng)) * 0.15
    y *= np.sin(np.pi * t / dur) ** 0.6
    return norm(reverb(y, 0.08, reverb_ir(0.4, 0.1)), -6)


def footstep_soft(rng=RNG):
    n = int(0.25 * SR)
    th = filt(sos_lp(220), noise(n, rng)) * env_ad(n, 0.004, 0.03) * 1.6
    sc = filt(sos_bp(1000, 5000), noise(n, rng)) * env_ad(n, 0.01, 0.06) * 0.15
    return (th + sc).astype(np.float32)


def ma_arrives(rng=None):
    """two soft bare footsteps + door-frame creak as a hand rests on it"""
    rng = rng or np.random.default_rng(31)
    out = np.zeros(int(2.4 * SR), np.float32)
    for tt, g in [(0.0, 0.7), (0.55, 0.9)]:
        f = footstep_soft(rng); i = int(tt * SR); out[i:i + len(f)] += f * g
    c = creak(0.75, 30, 70, (300, 820, 1900), rng) * 0.35
    i = int(1.05 * SR); out[i:i + len(c)] += c
    r = cloth_rustle(0.6, rng) * 0.25
    i = int(0.9 * SR); out[i:i + len(r)] += r
    return norm(reverb(out, 0.22, reverb_ir(1.0, 0.25, 4000)), -4)


def passbook_flip(rng=None):
    rng = rng or np.random.default_rng(41)
    out = np.zeros(int(1.0 * SR), np.float32)
    for k, tt in enumerate([0.0, 0.18, 0.33]):
        p = page_turn(k + 1)[: int(0.4 * SR)] * (0.8 - 0.2 * k)
        i = int(tt * SR); out[i:i + len(p)] += p
    return norm(out, -6)


def notice_rustle(rng=None):
    rng = rng or np.random.default_rng(51)
    return paper_handle(1.4, rng)


def pencil_scratch(dur=1.6, rng=None):
    rng = rng or np.random.default_rng(61)
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = filt(sos_bp(2500, 9000), noise(n, rng))
    strokes = np.zeros(n, np.float32)
    tt = 0.05
    while tt < dur - 0.1:
        L = rng.uniform(0.06, 0.2)
        a, b = int(tt * SR), int(min(dur, tt + L) * SR)
        strokes[a:b] = np.sin(np.pi * np.linspace(0, 1, b - a)) * rng.uniform(0.5, 1)
        tt += L + rng.uniform(0.03, 0.12)
    grit = 1 + 0.5 * filt(sos_lp(200), noise(n, rng))
    return norm(x * strokes * grit, -8)


def breath_in(dur=0.55, rng=None):
    rng = rng or np.random.default_rng(71)
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = filt(sos_bp(450, 2600), noise(n, rng))
    x = peak(x, 1200, 2) * 0.6 + x * 0.4
    e = np.sin(np.pi * np.clip(t / dur, 0, 1) * 0.9) ** 1.5 * (t / dur) ** 0.3
    return norm(x * e, -6)


def whoosh_soft(dur=1.2, rng=None):
    rng = rng or np.random.default_rng(81)
    n = int(dur * SR); t = np.arange(n) / SR
    fc = 300 + 2200 * (t / dur) ** 2
    x = noise(n, rng)
    # time-varying lowpass approximation by crossfading two bands
    lo = filt(sos_lp(500), x); hi = filt(sos_bp(800, 4000), x)
    w = (t / dur) ** 1.5
    y = lo * (1 - w) + hi * w
    return norm(y * np.sin(np.pi * t / dur) ** 2, -10)


# ---------------------------------------------------------------- registry
def sfx(kind, **kw):
    """returns stereo array for a one-shot type string"""
    reg = {
        'bell_dingding': lambda: pan(bell_dingding(), 0.0),
        'bell_clink': lambda: pan(bell_clink(), 0.1),
        'trunk_open': lambda: pan(trunk_open(), -0.1),
        'latch': lambda: pan(latch_clack(), 0),
        'cloth': lambda: pan(cloth_rustle(1.0), 0.15),
        'page_turn': lambda: pan(page_turn(kw.get('variant', 0)), 0.1),
        'page_flutter': lambda: pan(page_flutter(kw.get('pages', 8)), 0.1),
        'paper_handle': lambda: pan(paper_handle(1.2), 0),
        'paper_tear': lambda: pan(paper_tear(), 0),
        'ma_arrives': lambda: pan(ma_arrives(), -0.45),
        'footsteps': lambda: pan(np.concatenate([footstep_soft(), np.zeros(int(.3 * SR), np.float32), footstep_soft()]), -0.3),
        'door_creak': lambda: pan(creak(0.9, 30, 80, (300, 820, 1900)), -0.4),
        'passbook_flip': lambda: pan(passbook_flip(), 0),
        'notice_rustle': lambda: pan(notice_rustle(), 0),
        'pencil': lambda: pan(pencil_scratch(kw.get('dur', 1.6)), 0.1),
        'breath': lambda: pan(breath_in(), 0),
        'clock_tick': lambda: pan(clock_tick(), 0.35),
        'crackle': lambda: pan(crackle(kw.get('dur', 3.0), 6), -0.3),
        'kite': lambda: pan(reverb(filt(sos_lp(5000), kite_call()), 0.5, reverb_ir(2.5, 0.8, 4000, 0.04)), 0.4),
        'dog_far': lambda: pan(dog_bark_far(), -0.6),
        'bus_pass': lambda: bus_pass(7.0),
        'horn_far': lambda: pan(horn_far(), 0.3),
        'whoosh': lambda: pan(whoosh_soft(kw.get('dur', 1.2)), 0),
    }
    x = reg[kind]()
    return fade(norm(x, -6.0), 0.002, 0.04)


SFX_TYPES = ['bell_dingding', 'bell_clink', 'trunk_open', 'latch', 'cloth', 'page_turn', 'page_flutter',
             'paper_handle', 'paper_tear', 'ma_arrives', 'footsteps', 'door_creak', 'passbook_flip',
             'notice_rustle', 'pencil', 'breath', 'clock_tick', 'crackle', 'kite', 'dog_far', 'bus_pass',
             'horn_far', 'whoosh']


def bed(kind, dur, **kw):
    if kind == 'dawn':
        base = bed_dawn(min(dur, 45.0) + 2, kw.get('seed', 1))
    elif kind == 'night_room':
        base = bed_night_room(min(dur, 45.0) + 2, kw.get('seed', 2), kw.get('dog_at'))
    elif kind == 'morning_lane':
        return bed_morning_lane(dur, kw.get('seed', 3), kw.get('bus_at', 2.0))
    elif kind == 'room_tone':
        n = int((min(dur, 30) + 2) * SR)
        base = np.stack([filt(sos_lp(600, 4), noise(n)) * 0.1, filt(sos_lp(600, 4), noise(n)) * 0.1], 1)
    else:
        raise KeyError(kind)
    lp = loop_xfade(base, 1.0)
    n = int(dur * SR)
    reps = int(np.ceil(n / len(lp)))
    return np.tile(lp, (reps, 1))[:n]


BED_TYPES = ['dawn', 'night_room', 'morning_lane', 'room_tone']
