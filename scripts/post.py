# Painterly post-process: paper, granulation, pigment edges, grade, bloom, vignette, grain
import sys, json, numpy as np, cv2, pathlib
W,H=1188,2112
rng=np.random.default_rng(7)
def fbm(h,w,octaves=6,base=4,seed=0,persist=0.55):
    r=np.random.default_rng(seed); out=np.zeros((h,w),np.float32); amp=1; tot=0
    for o in range(octaves):
        n=base*2**o; g=r.random((n*h//w+2,n+2)).astype(np.float32)
        out+=amp*cv2.resize(g,(w,h),interpolation=cv2.INTER_CUBIC); tot+=amp; amp*=persist
    out/=tot; return (out-out.min())/(out.max()-out.min()+1e-9)
CACHE=pathlib.Path('/home/claude/udhaar/art/paper.npz')
if CACHE.exists():
    z=np.load(CACHE); PAPER,GRAN,FIB=z['p'],z['g'],z['f']
else:
    PAPER=fbm(H,W,7,3,1); GRAN=fbm(H,W,3,90,2,0.6)
    f=np.zeros((H,W),np.float32)
    for i in range(2600):
        x,y=rng.integers(0,W),rng.integers(0,H); a=rng.random()*np.pi; L=rng.integers(6,30)
        cv2.line(f,(x,y),(int(x+L*np.cos(a)),int(y+L*np.sin(a))),float(rng.random()),1)
    FIB=cv2.GaussianBlur(f,(0,0),0.7)
    np.savez_compressed(CACHE,p=PAPER,g=GRAN,f=FIB)
GRADES={
 'dawn':    dict(lift=(0.10,0.11,0.13), gain=(0.97,0.98,1.0), sat=0.72, warm_hi=(1.03,1.0,0.95), cool_lo=(0.95,1.0,1.06)),
 'day':     dict(lift=(0.09,0.09,0.10), gain=(1.0,0.99,0.97), sat=0.75, warm_hi=(1.03,1.0,0.96), cool_lo=(0.97,1.0,1.04)),
 'tungsten':dict(lift=(0.06,0.05,0.05), gain=(1.02,0.98,0.90), sat=0.85, warm_hi=(1.05,1.0,0.88), cool_lo=(0.94,0.98,1.06)),
 'night':   dict(lift=(0.04,0.05,0.07), gain=(0.95,0.97,1.0), sat=0.8, warm_hi=(1.04,1.0,0.9), cool_lo=(0.92,0.98,1.08)),
 'memory':  dict(lift=(0.12,0.10,0.07), gain=(1.0,0.95,0.84), sat=0.55, warm_hi=(1.05,1.0,0.88), cool_lo=(1.0,0.97,0.92)),
 'neutral': dict(lift=(0.06,0.06,0.06), gain=(1,1,1), sat=0.85, warm_hi=(1,1,1), cool_lo=(1,1,1)),
}
def process(src,dst,grade='dawn',paper=1.0,gran=1.0,edge=1.0,bloom=0.35,vig=0.35,grain=0.035,protect_red=True):
    im=cv2.imread(src,cv2.IMREAD_COLOR)[:,:,::-1].astype(np.float32)/255.0
    im=cv2.resize(im,(W,H),interpolation=cv2.INTER_AREA)
    lum=im@np.array([0.299,0.587,0.114],np.float32)
    # red protection mask (ledger stays saturated)
    r,g,b=im[...,0],im[...,1],im[...,2]
    redm=np.clip((r-np.maximum(g,b)-0.18)*4,0,1); redm=cv2.GaussianBlur(redm,(0,0),2)[...,None] if protect_red else 0
    # pigment edge darkening (watercolor accumulation at boundaries)
    bl=cv2.GaussianBlur(im,(0,0),3.0); e=np.abs(im-bl).sum(2); e=cv2.GaussianBlur(e,(0,0),1.2)
    im=im*(1-np.clip(e*0.9*edge,0,0.22))[...,None]
    # slight wet bleed: soften chroma
    ycc=cv2.cvtColor(im,cv2.COLOR_RGB2YCrCb); ycc[...,1:]=cv2.GaussianBlur(ycc[...,1:],(0,0),1.6); im=cv2.cvtColor(ycc,cv2.COLOR_YCrCb2RGB)
    # granulation in mid/dark tones
    gmask=(1-lum)*0.8+0.2
    im=im*(1-(GRAN-0.5)[...,None]*0.16*gran*gmask[...,None])
    # paper texture multiply
    pap=0.93+0.07*PAPER-0.05*FIB
    im=im*(1-(1-pap)[...,None]*paper)
    # grade
    G=GRADES[grade]; lum=np.clip(im@np.array([0.299,0.587,0.114],np.float32),0,1)[...,None]
    gray=lum; sat=G['sat']; im2=gray+(im-gray)*sat
    im2=im2*(lum*np.array(G['warm_hi'])+(1-lum)*np.array(G['cool_lo']))
    im2=np.array(G['lift'])+im2*(np.array(G['gain'])-np.array(G['lift']))
    im=im2*(1-redm)+ (np.array(G['lift'])*0.5+im*(1-np.array(G['lift'])*0.5))*redm if protect_red else im2
    # bloom
    hi=np.clip((im-0.72)*3,0,1); hb=cv2.GaussianBlur(hi,(0,0),28)+cv2.GaussianBlur(hi,(0,0),8)*0.5
    im=1-(1-im)*(1-hb*bloom)
    # vignette
    yy,xx=np.mgrid[0:H,0:W]; d=np.sqrt(((xx-W/2)/(W*0.62))**2+((yy-H*0.48)/(H*0.6))**2)
    im=im*(1-vig*np.clip(d-0.45,0,1)**1.6)[...,None]
    # static fine grain
    gn=rng.normal(0,1,(H,W)).astype(np.float32); gn=cv2.GaussianBlur(gn,(0,0),0.6)
    im=im+gn[...,None]*grain*(0.6+0.4*(1-lum))
    im=np.clip(im,0,1)
    cv2.imwrite(dst,(im[...,::-1]*255+0.5).astype(np.uint8))
if __name__=='__main__':
    cfg=json.loads(sys.argv[3]) if len(sys.argv)>3 else {}
    process(sys.argv[1],sys.argv[2],**cfg)
