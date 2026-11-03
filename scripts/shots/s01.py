import sys; sys.path.insert(0,'/home/claude/udhaar/scripts')
from art import *; from shapes import *
import random, math
random.seed(7)
def mix(c1,c2,t):
    a=[int(c1[i:i+2],16) for i in (1,3,5)]; b_=[int(c2[i:i+2],16) for i in (1,3,5)]
    return '#'+''.join(f'{int(a[i]+(b_[i]-a[i])*t):02x}' for i in range(3))
HZ=1265; SX,SY=575,1150
d=(lg('sky',[(0,'#5d6a73'),(0.30,'#8b9597'),(0.50,'#c2b8a3'),(0.60,'#e3cfa9'),(0.66,'#f0dcb6'),(0.70,'#dccdb0'),(1,'#b0a796')])
   +rg('sun',[(0,'#fff6e4'),(0.07,'#fde8c2',0.95),(0.3,'#f0cb97',0.5),(1,'#e8c08e',0)])
   +lg('ground',[(0,'#7c7468'),(0.15,'#5a544b'),(1,'#1e1c19')])
   +lg('haze',[(0,'#efdcb8',0),(0.5,'#efdcb8',0.9),(1,'#efdcb8',0)]))
b=[R(0,0,W,H,'url(#sky)')]
b.append(E(SX,SY,640,520,'url(#sun)'))
b.append(E(SX,SY,58,58,'#fff8ea'))
rays=''.join(P(f"M{SX},{SY} L{SX+math.cos(a)*1600},{SY+math.sin(a)*1600} L{SX+math.cos(a+0.03)*1600},{SY+math.sin(a+0.03)*1600} Z",'#fff0d2',0.09) for a in [math.radians(t) for t in (-170,-155,-141,-126,-113,-101,-88,-76,-63,-50,-36,-22,-10)])
b.append(g(rays,filt='b16'))
# smoke column (distant pyre), lit
sm=''.join(E(820+(i**1.5)*3.2+random.uniform(-8,8),HZ-40-i*70,22+i*8,44+i*5,'#efe5d0',0.32-0.009*i) for i in range(17))
b.append(g(sm,filt='smoke'))
# kites circling high
b.append(''.join(S(f"M{x-14*k},{y} q{7*k},{-7*k} {14*k},0 q{7*k},{-7*k} {14*k},0",'#3b3f40',2.2*k,0.8) for x,y,k in [(640,420,1.0),(720,470,0.8),(560,520,0.7),(820,380,0.6)]))
# far treeline/shed silhouettes
far='#9d978a'
b.append(g(P(f"M0,{HZ-22} C120,{HZ-60} 180,{HZ-40} 260,{HZ-64} C340,{HZ-86} 380,{HZ-50} 470,{HZ-48} L700,{HZ-46} C780,{HZ-62} 880,{HZ-44} 1080,{HZ-70} L1080,{HZ+10} L0,{HZ+10} Z",far),filt='rough'))
b.append(g(P(f"M760,{HZ-58} L960,{HZ-80} L985,{HZ-56} L756,{HZ-36} Z",mix(far,'#6c6860',0.3))+R(770,HZ-38,5,40,mix(far,'#6c6860',0.3))+R(955,HZ-60,5,62,mix(far,'#6c6860',0.3)),filt='roughS'))
# tiny far mourners on horizon (very hazy) + wheelchair
fm=mix('#8f8a80','#efdcb8',0.35)
b.append(g(''.join(f'<path d="{shape(n)}" fill="{fm}" transform="translate({x},{HZ+6}) scale({h/100})"/>' for x,h,n in [(80,70,'manc'),(130,66,'womanc'),(355,62,'manc'),(805,64,'womanc'),(1010,70,'man'),(1050,64,'womanc')]),filt='roughS'))
b.append(g(E(168,HZ-40,7,7,fm)+R(158,HZ-32,20,14,fm)+S(f"M156,{HZ-2} a10 10 0 1 0 20 0 a10 10 0 1 0 -20 0",fm,2.4),filt='roughS'))
b.append(R(0,HZ-120,W,200,'url(#haze)',0.55))
# peepal tree (left) silhouette with leaves
T='#2a2f2d'
trunk=P(f"M40,{HZ+30} C60,{HZ-120} 70,{HZ-300} 50,{HZ-420} C40,{HZ-480} 20,{HZ-520} 0,{HZ-540} L0,{HZ+30} Z",T)+P(f"M55,{HZ-300} C110,{HZ-380} 190,{HZ-420} 300,{HZ-450} L304,{HZ-436} C200,{HZ-406} 120,{HZ-360} 70,{HZ-280} Z",T)+P(f"M48,{HZ-410} C90,{HZ-500} 150,{HZ-560} 230,{HZ-600} L236,{HZ-588} C160,{HZ-546} 104,{HZ-490} 62,{HZ-400} Z",T)
b.append(g(trunk,filt='rough'))
leaves=[]
for i in range(420):
    a=random.uniform(0,2*math.pi); r=random.uniform(0,1)**0.55
    x=170+math.cos(a)*r*330; y=HZ-640+math.sin(a)*r*230
    if x>330 and y>HZ-520: continue
    sz=random.uniform(0.8,1.4)
    leaves.append(P(f"M{x},{y} c{12*sz},{-20*sz} {34*sz},{-22*sz} {40*sz},{-3*sz} c{-9*sz},{18*sz} {-28*sz},{21*sz} {-40*sz},{3*sz} z",random.choice(['#262b29','#2d3330','#232826']),1,f'transform="rotate({random.uniform(0,360)} {x} {y})"'))
b.append(g(''.join(E(x,y,rx,ry,T) for x,y,rx,ry in [(90,HZ-640,210,150),(230,HZ-600,150,110),(310,HZ-690,110,90),(150,HZ-760,160,110),(-10,HZ-700,150,130)]),filt='roughL'))
b.append(g(''.join(leaves),filt='roughS'))
# ground
b.append(P(f"M0,{HZ} L1080,{HZ} L1080,1920 L0,1920 Z",'url(#ground)'))
b.append(g(P(f"M{SX-40},{HZ} L{SX+40},{HZ} L{SX+260},1920 L{SX-330},1920 Z",'#f0d6a8',0.22),filt='b40'))
b.append(g(''.join(E(random.uniform(0,W),random.uniform(HZ+30,1900),random.uniform(30,150),random.uniform(3,9),random.choice(['#6d665b','#3b3732','#857e71']),0.4) for _ in range(40)),filt='rough'))
# pyre silhouette (center, slightly left of sun) with rim + marigolds catching light
px,py=530,HZ+90
D='#2a231d'; RIM='#f7dcaa'
pyre=[]
for j in range(7):
    yy=py-j*19; w0=320-j*6
    pyre.append(R(px-w0/2+random.uniform(-5,5),yy-19,w0+random.uniform(-8,8),18,D,1,'rx="5"'))
    if j%2:
        for i in range(10): xc=px-w0/2+12+i*(w0-24)/9+random.uniform(-3,3); pyre.append(E(xc,yy-10,8.5,8,'#3a3027'))
pyre.append(P(f"M{px-160},{py-134} C{px-145},{py-160} {px-80},{py-168} {px-20},{py-164} C{px+60},{py-162} {px+125},{py-158} {px+158},{py-144} C{px+172},{py-137} {px+170},{py-128} {px+152},{py-126} L{px-152},{py-124} C{px-164},{py-126} {px-168},{py-130} {px-160},{py-134} Z",'#4a453d'))
b.append(g(P(f"M{px-160},{py-136} C{px-145},{py-162} {px-80},{py-170} {px-20},{py-166} C{px+60},{py-164} {px+125},{py-160} {px+160},{py-146}",'none',extra=f'stroke="{RIM}" stroke-width="4"'),filt='roughS'))
b.append(g(''.join(pyre),filt='roughS'))
b.append(g(''.join(E(px-140+t*280, py-156+math.sin(t*10)*5,5,4.5,random.choice(['#d99a4a','#c98a3d','#e2ad62'])) for t in [i/30 for i in range(31)]),filt='roughS'))
b.append(g(E(px,py+4,240,18,'#0f0d0b',0.6),filt='b6'))
# mourners: true silhouettes with rim light, standing apart
S_='#2c2b29'
mid=[(105,HZ+300,500,'womanc',False,0),(292,HZ+96,330,'manc',False,-2),(372,HZ+34,236,'womanc',False,0),(745,HZ+52,276,'manc',True,0),(880,HZ+168,384,'man',True,1),(1040,HZ+330,520,'womanc',True,1.5),(985,HZ+20,214,'manc',True,0)]
for x,y,h,n,fl,tl in sorted(mid,key=lambda m:m[1]):
    side=1 if x<SX else -1
    b.append(g(sil(n,x,y,h,S_,rim=RIM,rim_side=-side,rimw=2.8,flip=fl,tilt=tl),filt='roughS'))
    b.append(g(P(f"M{x-h*0.08},{y} L{x+h*0.08},{y} L{x+(x-SX)*0.9+h*0.12},1920 L{x+(x-SX)*0.9-h*0.12},1920 Z",'#14120f',0.45),filt='b6'))
# foreground: Kabir's shoulder & head, defocused dark, bottom right
k=('<g transform="translate(985,1905) scale(1.6) rotate(-4)">'
   + P("M-300,420 L-292,200 C-280,112 -200,64 -70,32 C-52,26 -42,12 -40,2 L40,2 C42,12 52,26 70,32 C200,64 280,112 292,200 L300,420 Z",'#1c1b19')
   + P("M-42,14 L-39,-62 L35,-62 L38,14 Z",'#1a1410')+E(-2,-130,80,94,'#1a1410')+E(-82,-128,15,25,'#1a1410')
   + P("M-84,-118 C-90,-205 -44,-238 4,-235 C56,-233 90,-196 83,-122 C81,-95 70,-76 54,-63 C28,-56 -32,-56 -58,-63 C-76,-76 -84,-95 -84,-118 Z",'#0f0c0a')
   + S("M-84,-118 C-90,-205 -44,-238 4,-235",'#f2d4a2',6,0.8)+S("M-82,-140 C-92,-130 -92,-114 -84,-104",'#f2c792',4,0.8)
   + S("M-292,200 C-280,112 -200,64 -70,32",'#e9cd9e',6,0.7)
   + '</g>')
b.append(g(k,filt='b6'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
