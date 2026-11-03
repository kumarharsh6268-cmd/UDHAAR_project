import sys, numpy as np, scipy.io.wavfile as w, scipy.signal as ss, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fs=sys.argv[2:]; out=sys.argv[1]
fig,ax=plt.subplots(len(fs),1,figsize=(14,2.6*len(fs)))
ax=np.atleast_1d(ax)
for a,f in zip(ax,fs):
    sr,x0=w.read(f); x=x0.astype(float)
    if np.issubdtype(x0.dtype,np.integer): x/=np.iinfo(x0.dtype).max
    x=x.mean(1) if x.ndim>1 else x
    F,T,S=ss.spectrogram(x,sr,nperseg=2048,noverlap=1536)
    m=F<12000; a.pcolormesh(T,F[m],10*np.log10(S[m]+1e-14),vmin=-120,vmax=-30,cmap='magma',shading='auto'); a.set_title(f.split('/')[-1],fontsize=9)
    t=np.arange(len(x))/sr; a2=a.twinx(); a2.plot(t,20*np.log10(np.abs(x)+1e-6),lw=0.3,color='c',alpha=0.4); a2.set_ylim(-80,0)
plt.tight_layout(); plt.savefig(out,dpi=55)
