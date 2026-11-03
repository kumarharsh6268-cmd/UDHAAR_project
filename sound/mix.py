"""UDHAAR Ep0 mixer.   python3 mix.py timeline.json vo.wav out.wav [--stems DIR]

TIMELINE (seconds):
 {
  "duration": 92.0,
  "lines": [{"id":"L01","start":0.8,"end":6.1}, ...],     # VO line spans, L01..L22 (score sections key off these)
  "sfx":   [{"t":0.1,"type":"bell_dingding","gain_db":0, "pan":0.0, "variant":0}, ...],
  "beds":  [{"type":"dawn","start":0,"end":28.5,"fade":1.0,"gain_db":0, "dog_at":12.0, "bus_at":2.0}, ...],
  "music_cues": {"drop_at":26.0, "diary_reveal":41.0, "torn_page":66.0, "final_bell":88.4},
  "music_gain_db": 0, "beds_gain_db": 0, "sfx_gain_db": 0          # optional global trims
 }

SFX "type" strings (one-shots; each is auto-levelled relative to the VO, then gain_db is added):
  bell_dingding  signature brass bus bell, two strikes 0.28 s apart, ~4.5 s ring      (default -6 LU re VO)
  bell_clink     bell bumped inside the trunk, muffled single clink + clapper rattle   (-14)
  trunk_open     tin trunk dragged (0-1.3 s), latch clacks (1.7, 1.95 s), lid creak (2.2-3.3 s), lid thump (3.35 s)  (-12)
  latch          single metal latch clack (-16)
  cloth          cloth/uniform rustle ~1 s (-20)
  page_turn      single diary page turn, "variant" 0-3 (-16)
  page_flutter   several pages riffled, "pages" (default 8) (-16)
  paper_handle   paper pressed/handled ~1.2 s (-18)
  paper_tear     soft torn-paper texture ~1.1 s (-15)
  ma_arrives     two soft bare footsteps, cloth, door-frame creak ~2.4 s (-15)
  footsteps      two soft footsteps (-18)
  door_creak     wooden door-frame creak (-18)
  passbook_flip  passbook pages flipped (3 quick) (-16)
  notice_rustle  notice paper rustle ~1.4 s (-18)
  pencil         pencil scratching numbers, "dur" (default 1.6 s) (-20)
  breath         very subtle male inhale ~0.55 s, place ~0.6 s before a line (-30)
  clock_tick     one wall-clock tick (-22)  (the score already adds ticks in L08-L09 and L15-L16)
  crackle        wood-fire crackle, "dur" (default 3 s) (-22)
  kite           one distant kite call (-24)
  dog_far        distant dog bark x2 (-28)
  bus_pass       municipal bus passing, 7 s (-14)
  horn_far       distant bus horn (-24)
  whoosh         very soft air whoosh for a title card, "dur" (-22)

BED types (looped/crossfaded, faded in/out with "fade" seconds):
  dawn          cremation-ground dawn: wind, distant murmur, fire crackle, sparse kites/crows
  night_room    night interior: 50 Hz hum, room noise, crickets outside; optional "dog_at" (s, relative to bed start)
  morning_lane  lane at dawn: sparrows, wind, distant scooter; municipal bus passes at "bus_at" (s, rel., default 2.0)
                with a far horn ~5 s later (set "bus_at": null for none)
  room_tone     neutral room tone
A continuous low room-tone floor is always added so silences are never digital black.

MUSIC (score.py) follows line ids L01..L22 plus the optional anchors in music_cues (defaults in score.py).
Music sits ~19 LU under the VO in gaps and ducks a further ~7 dB while Kabir speaks (≈ -26 dB under speech).
Final master: stereo 48 kHz 24-bit, -14 LUFS integrated, true peak <= -1.5 dBTP (ffmpeg loudnorm, two-pass linear).
"""
import sys, os, json, subprocess, tempfile
import numpy as np
import scipy.signal as ss
import scipy.io.wavfile as wavfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import synth as S
import score as SC

SR = S.SR
FFMPEG = '/usr/local/bin/ffmpeg'
SFX_LEVEL = {'bell_dingding': -6, 'bell_clink': -14, 'trunk_open': -12, 'latch': -16, 'cloth': -20, 'page_turn': -16,
             'page_flutter': -16, 'paper_handle': -18, 'paper_tear': -15, 'ma_arrives': -15, 'footsteps': -18,
             'door_creak': -18, 'passbook_flip': -16, 'notice_rustle': -18, 'pencil': -20, 'breath': -30,
             'clock_tick': -22, 'crackle': -22, 'kite': -24, 'dog_far': -28, 'bus_pass': -14, 'horn_far': -24,
             'whoosh': -22}


# ------------------------------------------------------------ loudness (ITU-R BS.1770-4)
def kweight(x):
    b1, a1 = [1.53512485958697, -2.69169618940638, 1.19839281085285], [1.0, -1.69065929318241, 0.73248077421585]
    b2, a2 = [1.0, -2.0, 1.0], [1.0, -1.99004745483398, 0.99007225036621]
    return ss.lfilter(b2, a2, ss.lfilter(b1, a1, x, axis=0), axis=0)


def _blocks(x, win=0.4, hop=0.1):
    y = kweight(x if x.ndim == 2 else x[:, None])
    p = (y ** 2).sum(1)
    w, h = int(win * SR), int(hop * SR)
    if len(p) < w: return np.array([p.mean() + 1e-12])
    c = np.concatenate([[0], np.cumsum(p)])
    idx = np.arange(0, len(p) - w + 1, h)
    return (c[idx + w] - c[idx]) / w


def lufs(x):
    z = _blocks(x)
    l = -0.691 + 10 * np.log10(z + 1e-12)
    z = z[l > -70]
    if not len(z): return -70.0
    rel = -0.691 + 10 * np.log10(z.mean()) - 10
    z2 = z[(-0.691 + 10 * np.log10(z)) > rel]
    return float(-0.691 + 10 * np.log10(z2.mean() + 1e-12))


def loudest(x):
    z = _blocks(x)
    return float(-0.691 + 10 * np.log10(z.max() + 1e-12))


def gain_to(x, cur, target):
    return x * 10 ** ((target - cur) / 20)


# ------------------------------------------------------------ VO processing
def process_vo(vo):
    vo = S.filt(S.sos_hp(80, 2), vo)
    b, a = ss.iirpeak(3500, 1.2, fs=SR)
    vo = vo + 0.22 * ss.lfilter(b, a, vo)          # ~ +2 dB presence
    vo = vo - 0.10 * S.filt(S.sos_bp(250, 400), vo)  # tiny mud cut
    # light compression 2.5:1 above -20 dBFS (after peak-norm)
    vo = S.norm(vo, -3)
    from scipy.ndimage import maximum_filter1d
    lvl = maximum_filter1d(np.abs(vo), int(0.005 * SR))
    r = np.exp(-1 / (0.12 * SR)); lvl = ss.lfilter([1 - r], [1, -r], lvl)
    ldb = 20 * np.log10(lvl + 1e-9)
    th, ratio = -20.0, 2.5
    gr = np.where(ldb > th, (ldb - th) * (1 - 1 / ratio), 0)
    vo = vo * 10 ** (-gr / 20)
    return vo.astype(np.float32)


def duck_curve(vo, depth_db, att=0.08, rel=0.5):
    from scipy.ndimage import maximum_filter1d
    e = maximum_filter1d(np.abs(vo), int(0.03 * SR))
    e = ss.lfilter([1 - np.exp(-1 / (0.02 * SR))], [1, -np.exp(-1 / (0.02 * SR))], e)
    act = (20 * np.log10(e + 1e-9) > 20 * np.log10(np.abs(vo).max() + 1e-9) - 35).astype(np.float32)
    # asymmetric smoothing: fast attack, slow release
    ra, rr = np.exp(-1 / (att * SR)), np.exp(-1 / (rel * SR))
    up = ss.lfilter([1 - ra], [1, -ra], act)
    dn = ss.lfilter([1 - rr], [1, -rr], act)
    a = np.maximum(up, dn)
    return (10 ** (-depth_db * a / 20)).astype(np.float32)


# ------------------------------------------------------------ main mix
def load_vo(path):
    sr, x0 = wavfile.read(path)
    x = x0.astype(np.float32)
    if np.issubdtype(x0.dtype, np.integer): x /= float(np.iinfo(x0.dtype).max)
    if x.ndim == 2: x = x.mean(1)
    if sr != SR:
        from math import gcd
        g = gcd(SR, sr); x = ss.resample_poly(x, SR // g, sr // g).astype(np.float32)
    return x


def render(tl, vo_path, stems_dir=None):
    dur = float(tl['duration']); n = int(dur * SR)
    vo = load_vo(vo_path)
    vo = np.pad(vo, (0, max(0, n - len(vo))))[:n]
    vo = process_vo(vo)
    voL = lufs(vo)
    vo_st = np.stack([vo, vo], 1)

    # music
    if tl.get('score_profile'):
        import importlib; mus = importlib.import_module('score_'+tl['score_profile']).score(tl)[:n]
    else:
        mus = SC.score(tl)[:n]
    mus = np.pad(mus, ((0, n - len(mus)), (0, 0)))
    mus = gain_to(mus, lufs(mus), voL - 19 + tl.get('music_gain_db', 0))
    mus *= duck_curve(vo, 7.0)[:, None]

    # beds
    beds = np.zeros((n, 2), np.float32)
    for bd in tl.get('beds', []):
        t0, t1 = float(bd['start']), min(dur, float(bd['end']))
        kw = {k: bd[k] for k in ('seed', 'dog_at', 'bus_at') if k in bd}
        x = S.bed(bd['type'], t1 - t0, **kw)
        x = gain_to(x, lufs(x), voL - 22 + bd.get('gain_db', 0) + tl.get('beds_gain_db', 0))
        f = bd.get('fade', 1.0)
        x = S.fade(x, f, f)
        S.place(beds, x, t0)
    beds *= duck_curve(vo, 3.0)[:, None]
    # room-tone floor
    rt = S.bed('room_tone', dur)
    beds += gain_to(rt, lufs(rt), voL - 40)

    # sfx
    fx = np.zeros((n, 2), np.float32)
    cache = {}
    for c in tl.get('sfx', []):
        kind = c['type']
        kw = {k: c[k] for k in ('variant', 'pages', 'dur') if k in c}
        key = (kind, tuple(sorted(kw.items())))
        if key not in cache: cache[key] = S.sfx(kind, **kw)
        x = cache[key]
        if 'pan' in c:
            m = x.mean(1); x = S.pan(m, float(c['pan']))
        x = gain_to(x, loudest(x), voL + SFX_LEVEL.get(kind, -18) + c.get('gain_db', 0) + tl.get('sfx_gain_db', 0))
        S.place(fx, x, float(c['t']))

    mix = vo_st + mus + beds + fx
    if stems_dir:
        os.makedirs(stems_dir, exist_ok=True)
        for nm, x in [('vo', vo_st), ('music', mus), ('beds', beds), ('sfx', fx)]:
            wavfile.write(os.path.join(stems_dir, nm + '.wav'), SR, (x / 4).astype(np.float32))
    return mix.astype(np.float32)


def master(mix, out):
    with tempfile.TemporaryDirectory() as td:
        pre = os.path.join(td, 'pre.wav')
        wavfile.write(pre, SR, (mix / (np.abs(mix).max() + 1e-9) * 0.5).astype(np.float32))
        r = subprocess.run([FFMPEG, '-hide_banner', '-nostats', '-i', pre, '-af',
                            'loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'],
                           capture_output=True, text=True)
        txt = r.stderr[r.stderr.rindex('{'):r.stderr.rindex('}') + 1]
        m = json.loads(txt)
        af = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
              f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
        subprocess.run([FFMPEG, '-hide_banner', '-loglevel', 'error', '-y', '-i', pre, '-af', af + ',aresample=48000',
                        '-ar', '48000', '-c:a', 'pcm_s24le', out], check=True)


def measure(path):
    r = subprocess.run([FFMPEG, '-hide_banner', '-nostats', '-i', path, '-af', 'ebur128=peak=true', '-f', 'null', '-'],
                       capture_output=True, text=True).stderr
    s = r[r.rindex('Summary:'):]
    import re
    I = float(re.search(r'I:\s+(-?[\d.]+) LUFS', s).group(1))
    TP = float(re.search(r'Peak:\s+(-?[\d.]+) dBFS', s).group(1))
    LRA = float(re.search(r'LRA:\s+(-?[\d.]+) LU', s).group(1))
    return I, TP, LRA


if __name__ == '__main__':
    tlp, vop, out = sys.argv[1:4]
    stems = sys.argv[sys.argv.index('--stems') + 1] if '--stems' in sys.argv else None
    tl = json.load(open(tlp))
    mix = render(tl, vop, stems)
    master(mix, out)
    I, TP, LRA = measure(out)
    print(f"wrote {out}: integrated {I:.1f} LUFS, true peak {TP:.1f} dBTP, LRA {LRA:.1f} LU")
