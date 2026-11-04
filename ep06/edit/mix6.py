# Ep6 mix wrapper: adds the tailoring-shop bed (treadle machines) and a hospital bed to the series synth, then runs sound/mix.py.
# Shop bed reuses the timeline keys mix.py forwards: "bus_at" = when machines start (rel s, null = from start),
# "dog_at" = when they stop one by one (rel s).
import sys, json, numpy as np
sys.path.insert(0, '/home/claude/udhaar/sound')
import synth as S, mix as M
SR = S.SR
def machine(dur, rate, seed, pan, start=0.0, stop=None):
    rng = np.random.default_rng(seed); n = int(dur * SR); out = np.zeros(n, np.float32)
    click = S.filt(S.sos_bp(2400, 6000), S.noise(int(0.012 * SR), rng)) * np.exp(-np.linspace(0, 9, int(0.012 * SR)))
    thump = S.filt(S.sos_bp(120, 420), S.noise(int(0.04 * SR), rng)) * np.exp(-np.linspace(0, 7, int(0.04 * SR)))
    t = start + rng.uniform(0, 0.6); stop = dur if stop is None else stop
    while t < stop:
        run = rng.uniform(1.8, 4.5); r = rate * rng.uniform(0.9, 1.1); tt = t
        while tt < min(t + run, stop):
            i = int(tt * SR)
            if i + len(thump) < n:
                out[i:i + len(click)] += click * rng.uniform(0.5, 0.9); out[i:i + len(thump)] += thump * rng.uniform(0.7, 1.0) * 1.6
            tt += 1.0 / r
        # whirr under the run
        a, b = int(t * SR), int(min(tt, dur) * SR)
        if b > a:
            w = S.filt(S.sos_bp(260, 900), S.noise(b - a, rng)) * 0.12
            w *= (0.6 + 0.4 * np.sin(2 * np.pi * r * np.arange(b - a) / SR)) * np.clip(np.minimum(np.arange(b - a), np.arange(b - a)[::-1]) / (0.15 * SR), 0, 1)
            out[a:b] += w
        t = tt + rng.uniform(0.5, 1.6)
    return S.pan(out, pan)
_old_bed = S.bed
def bed(kind, dur, **kw):
    if kind == 'shop':
        start = kw.get('bus_at') or 0.0; stop = kw.get('dog_at')
        x = np.zeros((int(dur * SR), 2), np.float32)
        for k, (rate, pan) in enumerate(((9.0, -0.45), (7.5, 0.35), (10.5, 0.05))):
            st = start + k * 0.5
            sp = None if stop is None else stop + k * 0.55
            x += machine(dur, rate, 30 + k, pan, st, sp) * (1.0 - 0.25 * k)
        lane = _old_bed('morning_lane', dur, seed=4, bus_at=None) * 0.25
        rt = _old_bed('room_tone', dur) * 0.4
        return (x + lane + rt).astype(np.float32)
    if kind == 'hospital':
        n = int(dur * SR); tt = np.arange(n) / SR
        hum = (np.sin(2 * np.pi * 100 * tt) * 0.02 + np.sin(2 * np.pi * 200 * tt) * 0.008).astype(np.float32)
        air = S.filt(S.sos_lp(1800, 2), S.noise(n)) * 0.05
        x = np.stack([hum + air, hum + S.filt(S.sos_lp(1800, 2), S.noise(n)) * 0.05], 1)
        return (x + _old_bed('room_tone', dur) * 0.5).astype(np.float32)
    return _old_bed(kind, dur, **kw)
S.bed = bed
tl = json.load(open(sys.argv[1])); mixed = M.render(tl, sys.argv[2], sys.argv[4] if len(sys.argv) > 4 else None)
M.master(mixed, sys.argv[3]); print('LUFS/TP/LRA', M.measure(sys.argv[3]))
