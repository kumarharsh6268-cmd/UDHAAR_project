import sys, json, glob, re, numpy as np
src=open('/home/claude/udhaar/scripts/score.py').read().split("text=sys.argv_saved[1]")[0]
ns={}; exec(src.replace("sys.argv_saved=sys.argv; sys.argv=[sys.argv[0]]","sys.argv_saved=['x']"),ns)
score=ns['score']
sys.path.insert(0,'/home/claude/udhaar/scripts'); import f0 as F
done={}
for line in open('/home/claude/udhaar/vo/score.log'):
    m=re.match(r'(L\d+) (\d)\.wav ll=(\S+) med=(\d+) sd=(\S+) jumps=(\d+) \| (.*)',line)
    if m: done[(m[1],m[2])]=dict(ll=float(m[3]),med=float(m[4]),sd=float(m[5]),jumps=int(m[6]),tr=m[7])
res={}
for l in open('/home/claude/udhaar/vo/script.tsv'):
    id,p,sp,r,d=l.rstrip('\n').split('\t'); res[id]={}
    for k in '1234':
        f=f'/home/claude/udhaar/vo/takes/{id}_{k}.wav'
        if (id,k) in done: res[id][k]=done[(id,k)]; continue
        phi,top,ll=score(f,d); tr_f,dur=F.f0track(f); v=tr_f[tr_f>0]; st=12*np.log2(v/np.median(v))
        j=np.abs(np.diff(12*np.log2(np.where(tr_f>0,tr_f,np.nan)))); j=j[~np.isnan(j)]
        res[id][k]=dict(ll=float(ll),med=float(np.median(v)),sd=float(st.std()),jumps=int((j>5).sum()),tr='')
        print(id,k,f"ll={ll:.3f} sd={st.std():.2f} jumps={(j>5).sum()}",flush=True)
json.dump(res,open('/home/claude/udhaar/vo/scores.json','w'),ensure_ascii=False,indent=1)
print('SCORE_DONE')
