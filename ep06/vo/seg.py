import numpy as np, scipy.io.wavfile as w, json
sr,x=w.read('/home/claude/udhaar/ep06/vo/vo_raw.wav'); x=x.astype(np.float32)
hop=int(0.01*sr); n=len(x)//hop
rms=np.array([np.sqrt((x[i*hop:(i+1)*hop]**2).mean()+1e-12) for i in range(n)])
db=20*np.log10(rms)
voiced=db>-38
# fill tiny gaps < 0.20s
segs=[];on=False
for i,v in enumerate(voiced):
    if v and not on: s=i;on=True;last=i
    elif v: last=i
    elif on and i-last>20: segs.append([s,last]);on=False
if on: segs.append([s,last])
segs=[[a*0.01,b*0.01+0.01] for a,b in segs if (b-a)>8]
print(len(segs))
for k,(a,b) in enumerate(segs):
    print(k,round(a,2),round(b,2),round(b-a,2))
    y=x[max(0,int((a-0.08)*sr)):int((b+0.1)*sr)]
    w.write(f'/home/claude/udhaar/ep06/vo/segs/g{k:02d}.wav',sr,y)
json.dump(segs,open('/home/claude/udhaar/ep06/vo/segs.json','w'))
