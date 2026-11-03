import sys, numpy as np, scipy.io.wavfile as w, scipy.signal as ss
def f0track(path):
    sr,x=w.read(path); x=x.astype(np.float32); x/=np.abs(x).max()+1e-9
    if x.ndim>1: x=x.mean(1)
    x=ss.resample_poly(x,16000,sr); sr=16000
    hop=160; win=640; f=[]
    for i in range(0,len(x)-win,hop):
        fr=x[i:i+win]; e=np.sqrt((fr**2).mean())
        if e<0.03: f.append(0); continue
        fr=fr-fr.mean(); ac=np.correlate(fr,fr,'full')[win-1:]
        lo,hi=int(sr/400),int(sr/60); k=lo+np.argmax(ac[lo:hi])
        f.append(sr/k if ac[k]>0.45*ac[0] else 0)
    return np.array(f), len(x)/sr
for p in sys.argv[1:]:
    f,d=f0track(p); v=f[f>0]
    st=12*np.log2(v/np.median(v))
    print(f"{p.split('/')[-1]:16s} dur={d:5.2f}s medF0={np.median(v):6.1f}Hz  range(5-95%)={np.percentile(st,95)-np.percentile(st,5):5.1f}st  sd={st.std():4.2f}st voiced={len(v)/len(f):.2f}")
