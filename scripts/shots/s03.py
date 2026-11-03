import sys; sys.path.insert(0,'/home/claude/udhaar/scripts')
from art import *; from shapes import *
import random, math
random.seed(33)
def mix(c1,c2,t):
    a=[int(c1[i:i+2],16) for i in (1,3,5)]; b_=[int(c2[i:i+2],16) for i in (1,3,5)]
    return '#'+''.join(f'{int(a[i]+(b_[i]-a[i])*t):02x}' for i in range(3))
# Wide, low: strangers standing far apart across the misty ground, each alone, none speaking
HZ=1100; FOG='#e3d3b4'
d=lg('sky',[(0,'#6f7a82'),(0.5,'#c3b8a2'),(0.62,'#ead6b0'),(1,'#d9c9aa')])+lg('gnd',[(0,'#9c9384'),(0.3,'#6e675c'),(1,'#2c2925')])+lg('fogb',[(0,FOG,0),(0.5,FOG,0.8),(1,FOG,0)])
b=[R(0,0,W,H,'url(#sky)'),P(f"M0,{HZ} L1080,{HZ} L1080,1920 L0,1920 Z",'url(#gnd)')]
b.append(g(E(540,HZ-40,700,260,'#fff0d2',0.35),filt='b40'))
figs=[(90,HZ+40,150,'manc'),(330,HZ+20,120,'womanc'),(560,HZ+60,170,'manc'),(800,HZ+28,130,'womanc'),(1000,HZ+70,180,'man'),
      (200,HZ+220,280,'womanc'),(700,HZ+260,320,'manc'),(450,HZ+430,420,'manc'),(930,HZ+470,460,'womanc'),(110,HZ+620,560,'manc')]
for x,y,h,n in sorted(figs,key=lambda f:f[1]):
    depth=(y-HZ)/700; col=mix('#2a2826',FOG,max(0,0.62-depth))
    b.append(g(P(f"M{x-h*0.06},{y} L{x+h*0.06},{y} L{x+h*0.25},{y+h*0.5} L{x-h*0.05},{y+h*0.5} Z",'#1a1814',0.35*min(1,depth+0.3)),filt='b4'))
    b.append(g(sil(n,x,y,h,col,rim='#f7e4bf',rim_side=(1 if x<540 else -1),rimw=1.5+depth*2,flip=(x>540),tilt=random.uniform(-2,2)),filt='roughS'))
b.append(R(0,HZ-120,W,260,'url(#fogb)',0.7))
open(sys.argv[1],'w').write(svg(''.join(b),d))
