"""UDHAAR Ep0 original score, generated from code and keyed to narration line times.

Tonal centre: Sa = D. Colour: Todi/Bhairav-flavoured (komal re = Eb, komal dha = Bb),
motif = d P r S  (Bb3 A3 Eb4 D4) -- sparse, lots of air.

score(timeline) -> stereo float32 at 48 kHz, peak-normalised to -3 dBFS (mix.py sets level).
Anchors (all optional; defaults derived from line times):
  drop_at       : music falls to near-silence for ~1 s           (default: end of L06)
  diary_reveal  : warm return of the motif                       (default: start of L12)
  torn_page     : dissonant low bowed swell                       (default: start of L18)
  final_bell    : soft landing chord, then a tail under end card  (default: end of L22 + 0.35)
"""
import numpy as np
import scipy.signal as ss
import synth as S

SR = S.SR
RNG = np.random.default_rng(2026)
NOTE = {'D2': 73.42, 'A2': 110.0, 'Bb2': 116.54, 'D3': 146.83, 'Eb3': 155.56, 'F3': 174.61, 'A3': 220.0,
        'Bb3': 233.08, 'C#4': 277.18, 'D4': 293.66, 'Eb4': 311.13, 'F4': 349.23, 'G4': 392.0, 'A4': 440.0,
        'Ab2': 103.83, 'E2': 82.41, 'Eb2': 77.78, 'D5': 587.33}


# ------------------------------------------------------------- instruments (mono)
def tanpura_pluck(f, dur=4.6, bright=1.0, rng=RNG):
    t = S.t_(dur)
    y = np.zeros_like(t)
    c = 5 + 22 * np.exp(-t / 1.1) + 4 * np.sin(2 * np.pi * 0.35 * t)  # moving jawari formant
    for k in range(1, 34):
        fk = f * k * (1 + 0.00015 * k)
        if fk > 9000: break
        a = (1 / k ** 0.75) * np.exp(-t / (3.2 / (1 + 0.04 * k))) * (0.35 + bright * 1.6 * np.exp(-((k - c) / 3.2) ** 2))
        y += a * np.sin(2 * np.pi * fk * t + rng.uniform(0, 6))
    y *= np.minimum(1, t / 0.006) * np.clip((dur - t) / 0.8, 0, 1)
    return y.astype(np.float32)


def tanpura(start, end, gain=1.0, sa='D3', cycle=4.6):
    """Pa Sa' Sa' Sa(low) pattern"""
    notes = [NOTE['A2'], NOTE['D3'], NOTE['D3'], NOTE['D2']]
    n = int((end - start + 5) * SR)
    out = np.zeros(n, np.float32)
    tt, k = 0.0, 0
    while tt < end - start:
        p = tanpura_pluck(notes[k % 4] * (1 + RNG.uniform(-0.0006, 0.0006)), 4.6, 0.8 + 0.4 * RNG.random())
        i = int(tt * SR); m = min(len(p), n - i); out[i:i + m] += p[:m] * (0.9 if k % 4 else 1.0)
        tt += cycle / 4; k += 1
    e = np.ones(n, np.float32); fi = int(2.0 * SR); fo = int(2.5 * SR)
    e[:fi] = np.linspace(0, 1, fi); L = int((end - start) * SR)
    e[L:] = 0; e[max(0, L - fo):L] *= np.linspace(1, 0, min(fo, L))
    return out * e * gain


def felt_piano(f, dur=5.0, vel=0.7, rng=RNG):
    t = S.t_(dur)
    y = np.zeros_like(t)
    B = 0.00035
    for k in range(1, 14):
        fk = f * k * np.sqrt(1 + B * k * k)
        if fk > 10000: break
        a = vel ** (0.6 + 0.15 * k) / k ** 1.6
        d = 3.2 / (1 + 0.35 * (k - 1)) * (220 / f) ** 0.3
        y += a * np.exp(-t / d) * (np.sin(2 * np.pi * fk * t) + 0.5 * np.sin(2 * np.pi * fk * 1.0012 * t + 1.0))
    n = int(0.03 * SR)
    y[:n] += S.filt(S.sos_lp(600), S.noise(n, rng)) * np.linspace(1, 0, n) * 0.25 * vel
    y *= np.minimum(1, t / 0.008) * np.clip((dur - t) / 1.0, 0, 1)
    return S.filt(S.sos_lp(3800), y)


def bowed(freqs, dur, attack=1.5, release=2.0, bright=2500, vib=4.5, detune=0.003, rng=RNG):
    t = S.t_(dur)
    y = np.zeros_like(t)
    for f in freqs:
        for dd in (-detune, 0, detune):
            ph = 2 * np.pi * np.cumsum(f * (1 + dd) * (1 + 0.0025 * np.sin(2 * np.pi * vib * t + rng.uniform(0, 6)))) / SR
            for k in range(1, 18):
                if f * k > 6000: break
                y += np.sin(k * ph) / k * (0.9 if k % 2 else 0.6)
    y += S.filt(S.sos_bp(200, 1500), S.noise(len(t), rng)) * 0.02  # bow hair noise
    y = S.filt(S.sos_lp(bright), y)
    e = np.clip(t / attack, 0, 1) ** 2 * np.clip((dur - t) / release, 0, 1) ** 1.5
    return (y * e).astype(np.float32)


def heartbeat(t0, t1, period=1.1, gain=1.0, period_end=None):
    n = int((t1 - t0 + 1) * SR)
    out = np.zeros(n, np.float32)
    tt = 0.0
    while tt < t1 - t0:
        frac = tt / max(1e-3, (t1 - t0))
        p = period if period_end is None else period + (period_end - period) * frac
        for dt, f, a in [(0, 54, 1.0), (0.27, 46, 0.65)]:
            L = int(0.32 * SR); tl = np.arange(L) / SR
            b = np.sin(2 * np.pi * f * tl * (1 - 0.25 * tl)) * np.exp(-tl / 0.07) * np.minimum(1, tl / 0.006) * a
            i = int((tt + dt) * SR)
            if i + L < n: out[i:i + L] += b
        tt += p
    out = S.filt(S.sos_lp(180), out)
    e = np.ones(n, np.float32); fi = int(1.5 * SR); out[:fi] *= np.linspace(0, 1, fi)
    L = int((t1 - t0) * SR); fo = int(1.2 * SR); out[L:] = 0; out[max(0, L - fo):L] *= np.linspace(1, 0, min(fo, L))
    return out * gain


def low_sine_pad(f, dur, attack=2.0, release=2.0):
    t = S.t_(dur)
    y = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2 * f * t + 0.5) + 0.12 * np.sin(2 * np.pi * 3 * f * t)
    e = np.clip(t / attack, 0, 1) * np.clip((dur - t) / release, 0, 1)
    return (y * e * (0.85 + 0.15 * np.sin(2 * np.pi * 0.2 * t))).astype(np.float32)


# ------------------------------------------------------------- arrangement
def _L(tl, lid, key):
    for l in tl['lines']:
        if l['id'] == lid: return float(l[key])
    raise KeyError(lid)


def score(tl):
    dur = float(tl['duration'])
    n = int((dur + 1) * SR)
    mono_dry = np.zeros(n, np.float32)   # gets big reverb
    mono_low = np.zeros(n, np.float32)   # low stuff, little reverb
    st = np.zeros((n, 2), np.float32)
    mc = tl.get('music_cues', {})
    s = lambda i: _L(tl, i, 'start'); e = lambda i: _L(tl, i, 'end')
    drop = mc.get('drop_at', e('L06'))
    reveal = mc.get('diary_reveal', s('L12'))
    torn = mc.get('torn_page', s('L18'))
    fbell = mc.get('final_bell', e('L22') + 0.35)

    def add(buf, x, t0, g=1.0):
        i = int(t0 * SR); m = min(len(x), n - i)
        if m > 0 and i >= 0: buf[i:i + m] += x[:m] * g

    def motif(t0, notes, spacing=1.35, vel=0.55, g=1.0):
        for k, nn in enumerate(notes):
            add(mono_dry, felt_piano(NOTE[nn], 5.5, vel * (1 - 0.08 * k)), t0 + k * spacing * (1 + 0.06 * RNG.standard_normal()), g)

    # A: funeral dawn ------------------------------------------------------
    tp = tanpura(0.0, drop, 1.0)
    add(mono_low, tp, 0.0, 0.22)
    motif(s('L01') + 1.6, ['Bb3', 'A3', 'Eb4', 'D4'], 1.45, 0.5)
    motif(s('L04') + 0.4, ['F4', 'Eb4', 'D4', 'A3'], 1.6, 0.42)
    add(mono_dry, felt_piano(NOTE['Bb3'], 5.0, 0.38), s('L06') + 0.3)
    # drop: silence ~1 s, then single sustained low note under L07
    t7 = max(drop + 1.0, s('L07') - 0.2)
    add(mono_low, bowed([NOTE['D2']], e('L07') - t7 + 2.5, 1.4, 2.0, 900, 4.0, 0.0015), t7, 0.55)
    # B: notice -- heartbeat pulse, low pad
    add(mono_low, heartbeat(s('L08') - 0.3, e('L09') + 0.6, 1.12, 1.0), s('L08') - 0.3, 0.9)
    add(mono_low, low_sine_pad(NOTE['D2'], e('L09') - s('L08') + 2.5, 2.0, 2.0), s('L08'), 0.18)
    # C: trunk/diary -- thin, intimate: a faint high harmonic + warm motif at reveal
    add(mono_dry, low_sine_pad(NOTE['D5'], reveal - s('L10') + 1.5, 2.5, 1.5), s('L10'), 0.05)
    add(mono_low, low_sine_pad(NOTE['D2'], reveal - s('L10') + 1.5, 2.5, 1.5), s('L10'), 0.10)
    add(mono_low, bowed([NOTE['D3'], NOTE['A3']], e('L14') - reveal + 2.5, 2.0, 2.2, 1400, 4.5), reveal - 0.2, 0.22)
    motif(reveal + 0.15, ['D4', 'Eb4', 'D4', 'A3'], 1.5, 0.48, 1.05)
    add(mono_dry, felt_piano(NOTE['D3'], 6.0, 0.5), reveal + 0.15, 0.6)
    # D: 47 names / 47 days -- pulse tightens, low cluster swells, cut at L17
    t15, t17 = s('L15'), s('L17')
    add(mono_low, heartbeat(t15, t17 - 0.15, 1.0, 1.0, 0.78), t15, 1.0)
    cl = bowed([NOTE['D3'], NOTE['Eb3'], NOTE['A3'], NOTE['Bb2']], t17 - t15 + 0.1, (t17 - t15) * 0.75, 0.25, 1800, 5.0, 0.004)
    add(mono_low, cl, t15, 0.30)
    # E: L17 -- near silence (just a breath of the D drone, very low)
    add(mono_low, low_sine_pad(NOTE['D2'], e('L17') - t17 + 1.0, 1.0, 1.0), t17 + 0.2, 0.05)
    # F: torn page -- dissonant low bowed swell
    sw = bowed([NOTE['D2'], NOTE['Eb2'], NOTE['Ab2']], e('L18') - torn + 2.8, 1.8, 2.2, 1100, 3.2, 0.006)
    add(mono_low, sw, torn - 0.3, 0.30)
    # G: Ma at the door -- slow pulse returns, quiet tension, hold at L20 end
    t19, t21 = s('L19'), s('L21')
    add(mono_low, heartbeat(t19, e('L20') + 0.4, 1.2, 0.8), t19, 0.75)
    add(mono_low, bowed([NOTE['D3'], NOTE['Eb3']], e('L20') - t19 + 1.0, 2.5, 0.6, 1200, 4.0, 0.002), t19, 0.16)
    hold = bowed([NOTE['A2'], NOTE['D3']], t21 - e('L20') + 1.8, 0.4, 1.4, 1300, 4.0, 0.002)
    add(mono_low, hold, e('L20') - 0.2, 0.22)
    # H: resolve into forward motion; land on the final bell
    add(mono_low, tanpura(0.0, fbell - t21 + 3.5, 1.0), t21 - 0.3, 0.2)
    beat = 0.72
    tt = t21
    while tt < fbell - 0.3:
        L = int(0.3 * SR); tl_ = np.arange(L) / SR
        add(mono_low, (np.sin(2 * np.pi * 73.4 * tl_) * np.exp(-tl_ / 0.09) * np.minimum(1, tl_ / 0.01)).astype(np.float32), tt, 0.35)
        tt += beat
    k = 0; notes = ['Bb3', 'A3', 'Eb4', 'D4', 'F4', 'Eb4']
    tt = t21 + 0.1
    while tt < fbell - 1.2 and k < len(notes):
        add(mono_dry, felt_piano(NOTE[notes[k]], 4.0, 0.5), tt, 0.9); tt += beat * 2; k += 1
    for nn, v in [('D3', 0.55), ('A3', 0.5), ('D4', 0.5)]:
        add(mono_dry, felt_piano(NOTE[nn], 6.0, v), fbell, 0.85)
    add(mono_low, bowed([NOTE['D3'], NOTE['A3'], NOTE['D4']], dur - fbell + 0.5, 0.8, 2.5, 1500, 4.0), fbell, 0.18)

    # reverbs + stereo
    big = S.reverb_ir(3.2, 1.0, 5000, 0.03, np.random.default_rng(5))
    small = S.reverb_ir(1.2, 0.35, 3000, 0.01, np.random.default_rng(6))
    st += S.reverb_st(mono_dry, 0.45, big)
    st += S.reverb_st(mono_low, 0.22, small)
    st = st[:int(dur * SR)]
    st = S.filt(S.sos_hp(30), st.T).T.astype(np.float32) if False else st
    st = np.stack([S.filt(S.sos_hp(30), st[:, c]) for c in range(2)], 1)
    return S.norm(st, -3)
