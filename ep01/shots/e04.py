import sys; sys.path.insert(0,"/home/claude/udhaar/scripts")
from art import *; from shapes import *; from manq import *; from station import *
import random, math
random.seed(4)
# WIDE: Platform 4 in the morning. Canopy, pillars, light shafts, steam from a small tea stall at the far end
d=lg('sky',[(0,'#e9d6b0'),(1,'#c9b896')])+lg('plat',[(0,'#8f887a'),(1,'#3e3a34')])+rg('far',[(0,'#fff4d8',1),(1,'#f2d6a6',0)])
VY=980
b=[R(0,0,W,H,'url(#sky)'),E(540,VY-40,420,300,'url(#far)'),E(540,VY-20,140,90,'#fff8e8',0.9)]
b.append(P(f"M0,1920 L0,1500 L500,{VY+10} L580,{VY+10} L1080,1500 L1080,1920 Z",'url(#plat)'))
b.append(P(f"M500,{VY+10} L580,{VY+10} L1080,1500 L1080,1560 Z",'#d9b84a',0.5))
b.append(g(P(f"M580,{VY+10} L1080,1560 L1080,1920 L760,1920 Z",'#2b2824'),filt='rough'))
b.append(g(''.join(S(f"M{600+i*6},{VY+12} L{1080+i*200},{1920}",'#6a645a',4,0.6) for i in range(2)),filt='roughS'))
b.append(g(canopy(0,VY,'#58554e'),filt='rough'))
b.append(g(''.join(R(220+i*120,40+i*60,90,30,'#fff2d2',0.55,f'transform="skewX(-20)"') for i in range(4)),filt='b6'))
b.append(g(pillars(VY,side=-1,x0=180)+pillars(VY,side=1,x0=200),filt='roughS'))
b.append(g(''.join(P(f"M{x},{170} L{x+50},{170} L{x+360},1500 L{x+190},1500 Z",'#fff3d6',0.16) for x in (240,470,700)),filt='b16'))
# tea stall at far left end, small, with steam
sx,sy=430,1080
b.append(g(R(sx-60,sy-80,120,80,'#4a3a2a')+R(sx-70,sy-96,140,18,'#6a5a44')+E(sx-20,sy-80,12,10,'#9aa0a0')+''.join(E(sx-20+i*4,sy-110-i*30,16+i*5,22,'#ffffff',0.12) for i in range(7)),filt='roughS'))
b.append(g(fig('oldman',sx+30,sy,82,'#3a3530'),filt='roughS'))
# a few commuters, silhouettes
for x,y,h,n in [(640,1180,190,'manc'),(330,1260,250,'womanc'),(820,1380,330,'man')]:
    b.append(g(sil(n,x,y,h,'#2e2b27',rim='#f6e2bc',rim_side=(1 if x<540 else -1),rimw=2),filt='roughS'))
b.append(g(number_board(250,420,1.4,'4'),filt='roughS'))
b.append(g(''.join(E(random.uniform(0,W),random.uniform(200,700),3,2,'#3a3a3a',0.8) for _ in range(5)),filt='roughS'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
