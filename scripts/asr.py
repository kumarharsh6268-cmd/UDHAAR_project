import sys, base64, numpy as np, onnxruntime as ort, scipy.io.wavfile as w, scipy.signal as ss
W='/home/claude/udhaar/tts/sherpa-onnx-whisper-turbo/'
def hz2mel(f):
    f=np.asarray(f,float); m=f/(200/3); lg=f>=1000
    m=np.where(lg,15+np.log(np.maximum(f,1e-9)/1000)/(np.log(6.4)/27),m); return m
def mel2hz(m):
    m=np.asarray(m,float); f=m*(200/3); lg=m>=15
    return np.where(lg,1000*np.exp((np.log(6.4)/27)*(m-15)),f)
def melfb(sr=16000,n_fft=400,n_mels=128):
    fft=np.linspace(0,sr/2,n_fft//2+1); mp=mel2hz(np.linspace(hz2mel(0),hz2mel(8000),n_mels+2))
    fd=np.diff(mp); ramps=mp[:,None]-fft[None,:]; W_=np.zeros((n_mels,len(fft)))
    for i in range(n_mels):
        lo=-ramps[i]/fd[i]; hi=ramps[i+2]/fd[i+1]; W_[i]=np.maximum(0,np.minimum(lo,hi))
    W_*= (2.0/(mp[2:n_mels+2]-mp[:n_mels]))[:,None]; return W_
FB=melfb()
def feats(path):
    sr,x=w.read(path); x=x.astype(np.float32)
    if x.dtype!=np.float32 or np.abs(x).max()>2: x=x/32768.0
    if x.ndim>1: x=x.mean(1)
    if sr!=16000: x=ss.resample_poly(x,16000,sr).astype(np.float32)
    xp=np.pad(x,(200,200),mode='reflect'); win=np.hanning(401)[:-1]
    n=1+(len(xp)-400)//160; fr=np.stack([xp[i*160:i*160+400]*win for i in range(n)])
    S=np.abs(np.fft.rfft(fr,400,axis=1))**2; M=S@FB.T; M=M[:-1]
    L=np.log10(np.maximum(M,1e-10)); L=np.maximum(L,L.max()-8); L=(L+4)/4
    L=np.pad(L,((0,1500),(0,0))); 
    if L.shape[0]>3000: L=np.pad(L[:2950],((0,50),(0,0)))
    return L.T[None].astype(np.float32)
so=ort.SessionOptions(); so.intra_op_num_threads=2
enc=ort.InferenceSession(W+'turbo-encoder.int8.onnx',so); dec=ort.InferenceSession(W+'turbo-decoder.int8.onnx',so)
meta=enc.get_modelmeta().custom_metadata_map; g=lambda k:int(meta[k])
L,C,S=g('n_text_layer'),g('n_text_ctx'),g('n_text_state')
codes=meta['all_language_codes'].split(','); ltoks=list(map(int,meta['all_language_tokens'].split(',')))
sot=list(map(int,meta['sot_sequence'].split(',')))+[g('no_timestamps')]; sot[1]=ltoks[codes.index('hi')]
tok={}
for line in open(W+'turbo-tokens.txt'):
    p=line.split(); 
    if len(p)==2: tok[int(p[1])]=p[0]
def run(path):
    ck,cv=enc.run(None,{enc.get_inputs()[0].name:feats(path)})
    kc=np.zeros((L,1,C,S),np.float32); vc=kc.copy(); off=np.zeros(1,np.int64)
    ins=[i.name for i in dec.get_inputs()]
    t=np.array([sot],np.int64); res=[]
    for step in range(C):
        out=dec.run(None,dict(zip(ins,[t,kc,vc,ck,cv,off])))
        lg,kc,vc=out[0][0,-1],out[1],out[2]; off=off+t.shape[1]
        for k in ['no_timestamps','sot','no_speech','translate']: lg[g(k)]=-1e9
        if step==0: lg[g('eot')]=-1e9
        m=int(lg.argmax())
        if m==g('eot') or len(res)>200: break
        res.append(m); t=np.array([[m]],np.int64)
    return b''.join(base64.b64decode(tok[i]) for i in res if i in tok).decode('utf-8','replace').strip()
if __name__=='__main__':
    for p in sys.argv[1:]: print(p.split('/')[-1], '|', run(p), flush=True)
