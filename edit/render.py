import sys, json, re, subprocess, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0,'/home/claude/udhaar/edit'); from edl import EDL, DUR, OVERLAYS
FPS=30; W,H=1080,1920; F='/home/claude/udhaar/fonts/'
ART='/home/claude/udhaar/art/final/'
OUT=sys.argv[1] if len(sys.argv)>1 else '/home/claude/udhaar/edit/video_noaudio.mp4'
ONLY=None
if len(sys.argv)>2: ONLY=[float(t) for t in sys.argv[2].split(',')]   # render stills at these times
imgs={s:cv2.imread(ART+s+'.png')[:,:,::-1].astype(np.float32)/255 for s,_,_,_ in EDL}
def font(n,s): return ImageFont.truetype(F+n,s,layout_engine=ImageFont.Layout.RAQM)
# ---------- captions ----------
vo=json.load(open('/home/claude/udhaar/edit/vo_lines.json'))
chunks=[]   # (start,end,[(word,t)])
for l in vo['lines']:
    words=l['text'].split(); segs=l['segs'] or [(l['start'],l['end'])]
    # clause split by punctuation
    clauses=[]; cur=[]
    for wd in words:
        cur.append(wd)
        if re.search(r'[,.?!]$',wd): clauses.append(cur); cur=[]
    if cur: clauses.append(cur)
    if len(clauses)!=len(segs):
        tot=sum(b-a for a,b in segs); cl=sum(len(w) for w in words); allw=[]
        # proportional over concatenated speech time
        acc=0; times=[]
        for wd in words:
            frac=acc/cl; tt=frac*tot
            for a,b in segs:
                if tt<=b-a: times.append(a+tt); break
                tt-=(b-a)
            else: times.append(segs[-1][1])
            acc+=len(wd)+1
        groups=[(words,times)]
    else:
        groups=[]
        for cw,(a,b) in zip(clauses,segs):
            cl=sum(len(w)+1 for w in cw); acc=0; ts=[]
            for wd in cw: ts.append(a+(b-a)*acc/cl); acc+=len(wd)+1
            groups.append((cw,ts))
    allw=[(w_,t_) for cw,ts in groups for w_,t_ in zip(cw,ts)]
    cur=[]; n=0
    for w_,t_ in allw:
        if cur and (len(cur)>=6 or n+len(w_)>34) and not (re.search(r'[,.?!]$',w_) and len(cur)<=7): chunks.append([cur[0][1],None,cur]); cur=[]; n=0
        cur.append((w_,t_)); n+=len(w_)+1
        if re.search(r'[,.?!]$',w_) and len(cur)>=2: chunks.append([cur[0][1],None,cur]); cur=[]; n=0
    if cur:
        if len(cur)==1 and chunks and chunks[-1][2][-1][1]>=l['start']: chunks[-1][2]+=cur
        else: chunks.append([cur[0][1],None,cur])
for k in range(len(chunks)):
    nxt=chunks[k+1][0] if k+1<len(chunks) else DUR
    lastw=chunks[k][2][-1][1]
    chunks[k][1]=min(nxt, lastw+1.1)
CF=font('Mukta-Bold.ttf',58)
def cap_layer(t):
    c=[ch for ch in chunks if ch[0]-0.05<=t<ch[1]]
    if not c: return None
    st,en,ws=c[-1]
    img=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(img)
    # layout into max 2 lines width<=900
    lines=[[]]; 
    for w_,tt in ws:
        test=' '.join(x for x,_ in lines[-1]+[(w_,tt)])
        if d.textlength(test,font=CF)>880 and lines[-1]: lines.append([])
        lines[-1].append((w_,tt))
    y0=(1590 if 52.0<=t<55.0 else 1335)-(len(lines)-1)*38
    sh=Image.new('RGBA',(W,H),(0,0,0,0)); ds=ImageDraw.Draw(sh)
    for li,ln in enumerate(lines):
        txt=' '.join(x for x,_ in ln); tw=d.textlength(txt,font=CF); x=(W-tw)/2; y=y0+li*76
        ds.text((x,y+3),txt,font=CF,fill=(0,0,0,200))
        for w_,tt in ln:
            a=255 if t>=tt-0.04 else 120
            d.text((x,y),w_,font=CF,fill=(250,240,222,a),stroke_width=2,stroke_fill=(20,16,12,a))
            x+=d.textlength(w_+' ',font=CF)
    dsb=ImageDraw.Draw(sh); dsb.rounded_rectangle((90,y0-26,W-90,y0+len(lines)*76+18),40,fill=(0,0,0,70))
    sh=sh.filter(ImageFilter.GaussianBlur(14))
    fade=min(1,(t-st+0.05)/0.12)
    out=Image.alpha_composite(sh,img); 
    if fade<1: out.putalpha(out.getchannel('A').point(lambda v:int(v*fade)))
    return out
# ---------- overlays ----------
def ov_layer(t):
    lay=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(lay); any_=False
    for kind,a,b,p in OVERLAYS:
        if not (a<=t<b): continue
        any_=True; k=min(1,(t-a)/0.25)*min(1,(b-t)/0.15); A=int(255*k)
        if kind=='tag':
            f=font('Mukta-SemiBold.ttf',30); s='UDHAAR  ·  DIN 0 / 47'
            d.text((70,150),s,font=f,fill=(245,232,210,int(A*0.85)))
            d.line((70,196,70+d.textlength(s,font=f),196),fill=(178,22,30,int(A*0.9)),width=3)
        elif kind=='ink':
            f=font('Kalam-Bold.ttf',p['size']); tl=Image.new('RGBA',(700,200),(0,0,0,0)); dt=ImageDraw.Draw(tl)
            dt.text((10,40),p['text'],font=f,fill=(30,40,96,int(A*0.92)))
            tl=tl.rotate(-p['rot'],resample=Image.BICUBIC,expand=False)
            # soft highlight swipe behind
            hl=Image.new('RGBA',(W,H),(0,0,0,0)); dh=ImageDraw.Draw(hl); dh.ellipse((p['x']-40,p['y']+10,p['x']+340,p['y']+150),fill=(255,236,170,int(A*0.35)))
            lay=Image.alpha_composite(lay,hl.filter(ImageFilter.GaussianBlur(30))); lay.alpha_composite(tl,(p['x'],p['y'])); d=ImageDraw.Draw(lay)
        elif kind in ('big','big2'):
            f=font('Mukta-ExtraBold.ttf',p['size']); tw=d.textlength(p['text'],font=f); x=(W-tw)/2
            sh=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(sh).text((x,p['y']+6),p['text'],font=f,fill=(0,0,0,int(A*0.75)))
            lay=Image.alpha_composite(lay,sh.filter(ImageFilter.GaussianBlur(10))); d=ImageDraw.Draw(lay)
            col=(250,238,214,A)
            d.text((x,p['y']),p['text'],font=f,fill=col)
        elif kind=='count':
            n=int(round(p['n0']+(p['n1']-p['n0'])*min(1,max(0,(t-a)/(p['t1']-a))**0.8)))
            f=font('RozhaOne-Regular.ttf',260); s=str(n); tw=d.textlength(s,font=f); x=(W-tw)/2
            sh=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(sh).text((x,p['y']+8),s,font=f,fill=(0,0,0,int(A*0.8)))
            lay=Image.alpha_composite(lay,sh.filter(ImageFilter.GaussianBlur(14))); d=ImageDraw.Draw(lay)
            d.text((x,p['y']),s,font=f,fill=(250,238,214,A))
            f2=font('Mukta-SemiBold.ttf',44); s2='NAAM'; d.text(((W-d.textlength(s2,font=f2))/2,p['y']+310),s2,font=f2,fill=(250,238,214,int(A*0.8)))
        elif kind=='title':
            f=font('RozhaOne-Regular.ttf',250); s='उधार'; tw=d.textlength(s,font=f)
            k2=min(1,(t-a)/0.6)
            d.text(((W-tw)/2,560),s,font=f,fill=(248,236,214,int(255*k2)))
            f2=font('Mukta-SemiBold.ttf',56); s2='U D H A A R   ·   4 7   N A M E S'; d.text(((W-d.textlength(s2,font=f2))/2,930),s2,font=f2,fill=(248,236,214,int(230*k2)))
            k3=min(1,max(0,(t-a-0.5)/0.5))
            f3=font('Mukta-Bold.ttf',50); s3='EPISODE 1  ·  KAL'; d.text(((W-d.textlength(s3,font=f3))/2,1130),s3,font=f3,fill=(255,224,170,int(255*k3)))
            f4=font('Mukta-Medium.ttf',44); s4='Naam #1: Shankar.  Maangu ya chhod doon?'; d.text(((W-d.textlength(s4,font=f4))/2,1210),s4,font=f4,fill=(248,236,214,int(220*k3)))
            s5='Faisla aapka hoga.'; d.text(((W-d.textlength(s5,font=f4))/2,1268),s5,font=f4,fill=(248,236,214,int(220*k3)))
    return lay if any_ else None
# ---------- frames ----------
rng=np.random.default_rng(1)
GR=[cv2.GaussianBlur(rng.normal(0,1,(H//2,W//2)).astype(np.float32),(0,0),0.6) for _ in range(12)]
def shot_frame(s,a,b,mo,t):
    im=imgs[s]; ih,iw=im.shape[:2]
    u=(t-a)/(b-a); u=u*u*(3-2*u)*0.3+u*0.7
    z0,z1,px,py=mo; z=z0+(z1-z0)*u
    # base crop = 1080x1920 region of 1188x2112 scaled by zoom
    cw,chh=iw/ (1.1*z), ih/(1.1*z)
    sx=(iw-cw)/2*(1+px*(u-0.5)*0.9*2/2); sy=(ih-chh)/2*(1+py*(u-0.5)*0.9*2/2)
    M=np.array([[W/cw,0,-sx*W/cw],[0,H/chh,-sy*H/chh]],np.float32)
    return cv2.warpAffine(im,M,(W,H),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
def frame(t):
    cur=[e for e in EDL if e[1]<=t<e[2]] or [EDL[-1]]
    s,a,b,mo=cur[0]; f=shot_frame(s,a,b,mo,t)
    i=EDL.index(cur[0]); XF=0.12
    if i>0 and t-a<XF:
        ps=EDL[i-1]; pf=shot_frame(ps[0],ps[1],ps[2],ps[3],t); k=(t-a)/XF; f=pf*(1-k)+f*k
    if t<0.25: f=f*(t/0.25)
    if t>DUR-0.4: f=f*max(0,(DUR-t)/0.4)
    g=cv2.resize(GR[int(t*FPS)%12],(W,H))
    f=np.clip(f+g[...,None]*0.022,0,1)
    out=Image.fromarray((f*255).astype(np.uint8)).convert('RGBA')
    o=ov_layer(t)
    if o: out=Image.alpha_composite(out,o)
    c=cap_layer(t) if t<89.3 else None
    if c: out=Image.alpha_composite(out,c)
    return np.asarray(out.convert('RGB'))
if ONLY:
    for t in ONLY: Image.fromarray(frame(t)).save(f'/tmp/claude-0/f_{t:.2f}.jpg',quality=85)
    sys.exit()
N=int(DUR*FPS)
p=subprocess.Popen(['ffmpeg','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','17','-pix_fmt','yuv420p',OUT],stdin=subprocess.PIPE)
for n in range(N):
    p.stdin.write(frame(n/FPS).tobytes())
    if n%300==0: print('frame',n,'/',N,flush=True)
p.stdin.close(); p.wait(); print('done',OUT)
