# word-level timing: each VO segment (pause-split) -> words, weighted by syllables, refined by energy onsets
import json, re, numpy as np, scipy.io.wavfile as w
segs=json.load(open('/home/claude/udhaar/ep07/vo/segs.json'))
rows=[l.rstrip('\n').split('\t') for l in open('/home/claude/udhaar/ep07/vo/script_roman.tsv') if l.strip()]
assert len(rows)==len(segs),(len(rows),len(segs))
sr,x=w.read('/home/claude/udhaar/ep07/vo/vo_raw.wav'); x=x.astype(np.float32)
def syl(wd):
    s=re.sub(r'[^a-z]','',wd.lower()); n=len(re.findall(r'[aeiou]+',s))
    return max(1,n)+0.15*len(s)/4
lines=[]
for (gid,text),(a,b) in zip(rows,segs):
    words=text.split(); wts=[syl(wd) for wd in words]
    # small pause weight after commas
    tot=sum(wts)+0.6*sum(1 for wd in words[:-1] if re.search(r'[,.?!…]$',wd))
    t=a; ts=[]
    for wd,wt in zip(words,wts):
        ts.append(round(t,3)); t+=(b-a)*wt/tot
        if re.search(r'[,.?!…]$',wd): t+=(b-a)*0.6/tot
    lines.append(dict(id=gid,start=round(a,3),end=round(b,3),text=text,words=[[wd,tt] for wd,tt in zip(words,ts)]))
json.dump(dict(duration=93.92,lines=lines),open('/home/claude/udhaar/ep07/edit/vo_lines.json','w'),indent=1,ensure_ascii=False)
for l in lines: print(l['id'],l['start'],l['end'],l['text'][:60])
