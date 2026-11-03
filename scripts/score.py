# forced-alignment likelihood of a reference text under Whisper + language-ID prob
import sys, base64, numpy as np
sys.argv_saved=sys.argv; sys.argv=[sys.argv[0]]
import importlib.util
spec=importlib.util.spec_from_file_location('asr','/home/claude/udhaar/scripts/asr.py'); A=importlib.util.module_from_spec(spec); spec.loader.exec_module(A)
# build byte-level reverse table: greedy tokenization via trie over token bytes
tb={i:base64.b64decode(s) for i,s in A.tok.items() if i<50257+1000}
by={}
for i,b in tb.items():
    if b and b not in by: by[b]=i
def tokenize(text):
    b=text.encode(); out=[]; i=0
    while i<len(b):
        for L in range(min(24,len(b)-i),0,-1):
            if b[i:i+L] in by: out.append(by[b[i:i+L]]); i+=L; break
        else: raise Exception('no tok')
    return out
def lsm(x): x=x-x.max(); return x-np.log(np.exp(x).sum())
def score(path,text):
    ck,cv=A.enc.run(None,{A.enc.get_inputs()[0].name:A.feats(path)})
    ins=[i.name for i in A.dec.get_inputs()]
    kc=np.zeros((A.L,1,A.C,A.S),np.float32); vc=kc.copy(); off=np.zeros(1,np.int64)
    # language id
    out=A.dec.run(None,dict(zip(ins,[np.array([[A.sot[0]]],np.int64),kc,vc,ck,cv,off])))
    lg=lsm(out[0][0,-1]); lp=lg[A.ltoks]; p=np.exp(lp-np.log(np.exp(lp).sum()))
    phi=p[A.codes.index('hi')]; top=A.codes[int(p.argmax())]
    seq=A.sot+tokenize(text)
    out=A.dec.run(None,dict(zip(ins,[np.array([seq],np.int64),kc,vc,ck,cv,off])))
    lgs=out[0][0]; n0=len(A.sot); tot=0
    for j in range(n0,len(seq)): tot+=lsm(lgs[j-1])[seq[j]]
    return phi, top, tot/(len(seq)-n0)
text=sys.argv_saved[1]
for p in sys.argv_saved[2:]:
    phi,top,ll=score(p,text); print(f"{p.split('/')[-1]:16s} P(hi)={phi:.3f} top={top} avgLL={ll:.3f}",flush=True)
