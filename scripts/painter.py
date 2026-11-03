# Stroke-based painterly rendering (after Hertzmann 1998) with colour jitter and detail re-injection
import sys, json, numpy as np, cv2
def paint(src, dst, radii=(22,11,6,3), T=0.045, maxlen=12, jitter=0.035, detail=0.55, seed=3, keep_mask=None, flow_angle=-35, gmin=0.02):
    rng=np.random.default_rng(seed)
    img=cv2.imread(src,cv2.IMREAD_COLOR).astype(np.float32)/255.0
    H,W=img.shape[:2]
    canvas=cv2.GaussianBlur(img,(0,0),40)*1.0
    # coherent painter's-hand flow field for flat regions
    fl=cv2.GaussianBlur(rng.random((H//32+2,W//32+2)).astype(np.float32),(0,0),1.5)
    fl=cv2.resize(fl,(W,H),interpolation=cv2.INTER_CUBIC); fl=(fl-fl.min())/(fl.max()-fl.min()+1e-9)
    ang=np.deg2rad(flow_angle)+ (fl-0.5)*np.pi*0.9
    fdx,fdy=np.cos(ang),np.sin(ang)
    for li,R in enumerate(radii):
        ref=cv2.GaussianBlur(img,(0,0),max(0.8,R*0.45))
        lum=cv2.cvtColor((ref*255).astype(np.uint8),cv2.COLOR_BGR2GRAY).astype(np.float32)/255
        lum=cv2.GaussianBlur(lum,(0,0),R*0.6+1)
        gx=cv2.Sobel(lum,cv2.CV_32F,1,0,ksize=3); gy=cv2.Sobel(lum,cv2.CV_32F,0,1,ksize=3)
        mag=np.sqrt(gx*gx+gy*gy)
        diff=np.sqrt(((canvas-ref)**2).sum(2))
        step=max(2,int(R*0.9))
        pts=[]
        for y in range(0,H,step):
            for x in range(0,W,step):
                y2,x2=min(H,y+step),min(W,x+step)
                cell=diff[y:y2,x:x2]
                if li==0 or cell.mean()>T:
                    k=np.argmax(cell); cy,cx=y+k//(x2-x),x+k%(x2-x); pts.append((cy,cx))
        order=rng.permutation(len(pts))
        thick=max(1,int(round(R)))
        for oi in order:
            cy,cx=pts[oi]
            col=ref[cy,cx].copy()
            col=np.clip(col*(1+rng.normal(0,jitter))+rng.normal(0,jitter*0.5,3),0,1)
            path=[(cx,cy)]; x,y=float(cx),float(cy); ldx,ldy=0.0,0.0
            for s in range(maxlen if R>4 else max(3,maxlen//2)):
                xi,yi=int(x),int(y)
                if s>2 and np.abs(ref[yi,xi]-col).sum()>np.abs(canvas[yi,xi]-col).sum()+0.02: break
                if mag[yi,xi]<gmin: dx,dy=fdx[yi,xi],fdy[yi,xi]
                else: dx,dy=-gy[yi,xi],gx[yi,xi]
                if ldx*dx+ldy*dy<0: dx,dy=-dx,-dy
                if s>0: dx,dy=0.6*dx+0.4*ldx,0.6*dy+0.4*ldy
                n=np.hypot(dx,dy)+1e-9; dx,dy=dx/n,dy/n
                x+=dx*R; y+=dy*R
                if not(0<=x<W-1 and 0<=y<H-1): break
                path.append((int(x),int(y))); ldx,ldy=dx,dy
            c=tuple(float(v) for v in col)
            if len(path)==1: cv2.circle(canvas,path[0],max(1,thick//2),c,-1,cv2.LINE_AA)
            else: cv2.polylines(canvas,[np.array(path,np.int32)],False,c,thick,cv2.LINE_AA)
    # re-inject crisp detail where the source has strong edges (faces, hands, lettering)
    g=cv2.cvtColor((img*255).astype(np.uint8),cv2.COLOR_BGR2GRAY).astype(np.float32)/255
    e=np.abs(cv2.Laplacian(cv2.GaussianBlur(g,(0,0),1.0),cv2.CV_32F,ksize=3))
    m=np.clip(cv2.GaussianBlur(e,(0,0),2.5)*8,0,1)*detail
    if keep_mask is not None:
        km=cv2.imread(keep_mask,0).astype(np.float32)/255; km=cv2.resize(km,(W,H)); m=np.maximum(m,cv2.GaussianBlur(km,(0,0),3))
    out=canvas*(1-m[...,None])+img*m[...,None]
    cv2.imwrite(dst,(np.clip(out,0,1)*255+0.5).astype(np.uint8))
if __name__=='__main__':
    cfg=json.loads(sys.argv[3]) if len(sys.argv)>3 else {}
    paint(sys.argv[1],sys.argv[2],**cfg)
