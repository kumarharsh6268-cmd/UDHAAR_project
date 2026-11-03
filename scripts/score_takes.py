import sys, json, glob, numpy as np, importlib.util
sys.argv=[sys.argv[0]]
spec=importlib.util.spec_from_file_location('sc','/home/claude/udhaar/scripts/score.py')
# reuse score() by importing module body without CLI
src=open('/home/claude/udhaar/scripts/score.py').read().split("text=sys.argv_saved[1]")[0]
ns={}; exec(src.replace("sys.argv_saved=sys.argv; sys.argv=[sys.argv[0]]","sys.argv_saved=['x']"),ns)
score=ns['score']; A=ns['A']
sys.path.insert(0,'/home/claude/udhaar/scripts'); import f0 as F
res={}
for l in open('/home/claude/udhaar/vo/script.tsv'):
    id,p,sp,r,d=l.rstrip('\n').split('\t'); res[id]=[]
    for f in sorted(glob.glob(f'/home/claude/udhaar/vo/takes/{id}_*.wav')):
        phi,top,ll=score(f,d); tr=A.run(f)
        tr_f,dur=F.f0track(f); v=tr_f[tr_f>0]; st=12*np.log2(v/np.median(v))
        jumps=np.abs(np.diff(12*np.log2(np.where(tr_f>0,tr_f,np.nan))))
        jumps=jumps[~np.isnan(jumps)]
        res[id].append(dict(f=f,ll=float(ll),phi=float(phi),tr=tr,med=float(np.median(v)),sd=float(st.std()),bigjump=int((jumps>5).sum())))
        print(id, f.split('_')[-1], f"ll={ll:.3f} med={np.median(v):.0f} sd={st.std():.2f} jumps={(jumps>5).sum()} | {tr}", flush=True)
json.dump(res,open('/home/claude/udhaar/vo/scores.json','w'),ensure_ascii=False,indent=1)
print('SCORE_DONE')
