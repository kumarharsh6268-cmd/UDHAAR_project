import json, numpy as np, scipy.io.wavfile as w, scipy.signal as ss, re
SR=48000
sel=json.load(open('/home/claude/udhaar/vo/selected.json'))
rows=[l.rstrip('\n').split('\t') for l in open('/home/claude/udhaar/vo/script.tsv') if l.strip()]
LEAD=0.6
out=[np.zeros(int(LEAD*SR),np.float32)]; t=LEAD; lines=[]; words=[]
for id,p,sp,roman,deva in rows:
    sr,x=w.read(f'/home/claude/udhaar/vo/tempo/{id}_{sel[id]}.wav'); x=x.astype(np.float32)
    if np.abs(x).max()>2: x/=32768
    x=ss.resample_poly(x,SR//300*1,sr//300).astype(np.float32) if sr!=SR else x
    if sr==44100: x=ss.resample_poly(w.read(f'/home/claude/udhaar/vo/tempo/{id}_{sel[id]}.wav')[1].astype(np.float32)/ (32768 if w.read(f'/home/claude/udhaar/vo/tempo/{id}_{sel[id]}.wav')[1].dtype!=np.float32 else 1),160,147).astype(np.float32)
    env=np.convolve(np.abs(x),np.ones(480)/480,'same'); thr=0.02*env.max()
    idx=np.where(env>thr)[0]; a=max(0,idx[0]-int(0.06*SR)); b=min(len(x),idx[-1]+int(0.12*SR))
    x=x[a:b]
    # soft gate: attenuate low-level gaps (kills vocoder hum in pauses)
    env=np.convolve(np.abs(x),np.ones(960)/960,'same'); g=np.clip((env-0.004)/0.02,0.08,1.0)
    g=np.convolve(g,np.ones(960)/960,'same'); x=x*g
    x[:240]*=np.linspace(0,1,240); x[-480:]*=np.linspace(1,0,480)
    st=t; dur=len(x)/SR; out.append(x); t+=dur
    # internal segments for caption timing (gaps > 0.18 s)
    e2=np.convolve(np.abs(x),np.ones(480)/480,'same')>0.03*np.abs(x).max()
    segs=[]; on=False
    for i in range(0,len(e2),240):
        v=e2[i]
        if v and not on: s0=i; on=True; last=i
        elif v: last=i
        elif on and (i-last)>0.18*SR: segs.append((s0/SR,last/SR)); on=False
    if on: segs.append((s0/SR,last/SR))
    lines.append(dict(id=id,start=round(st,3),end=round(st+dur,3),text=roman,segs=[(round(st+a_,3),round(st+b_,3)) for a_,b_ in segs]))
    pz=float(p)*0.7; out.append(np.zeros(int(pz*SR),np.float32)); t+=pz
y=np.concatenate(out); y=y/np.abs(y).max()*0.89
w.write('/home/claude/udhaar/edit/vo.wav',SR,y.astype(np.float32))
json.dump(dict(duration=round(t,3),lines=lines),open('/home/claude/udhaar/edit/vo_lines.json','w'),indent=1,ensure_ascii=False)
for l in lines: print(l['id'],l['start'],l['end'],len(l['segs']))
print('total',round(t,2))
