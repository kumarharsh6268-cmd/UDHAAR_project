import sys; sys.path.insert(0,'/home/claude/udhaar/scripts')
from art import *; from shapes import *; from manq import *
import random
random.seed(9)
d=(lg('sky',[(0,'#7b868a'),(0.45,'#c9bea7'),(0.58,'#ead6b0'),(0.66,'#d6c8ad'),(1,'#4a453e')])+rg('sun',[(0,'#fff3dc'),(1,'#efc995',0)])+lg('fogb',[(0,'#e2d4b8',0),(0.5,'#e2d4b8',0.8),(1,'#e2d4b8',0)]))
HZ=1180
b=[R(0,0,W,H,'url(#sky)'),E(260,1060,620,500,'url(#sun)',0.85),E(260,1060,40,40,'#fff6e4',0.9)]
b.append(g(''.join(E(150+i*22+random.uniform(-10,10),1080-i*70,60+i*14,50,'#f1e8d6',0.15) for i in range(14)),filt='smoke'))
b.append(g(''.join(f'<path d="{shape(n)}" fill="#8d877c" transform="translate({x},{HZ+12}) scale({h/100})"/>' for x,h,n in [(90,170,'manc'),(420,150,'womanc'),(860,180,'womanc'),(1000,200,'manc')]),filt='b6',op=0.75))
b.append(R(0,HZ-150,W,300,'url(#fogb)'))
b.append(P(f"M0,{HZ} L1080,{HZ} L1080,1920 L0,1920 Z",'#5b554c',0.9))
b.append(g(P(f"M220,{HZ} L300,{HZ} L760,1920 L-120,1920 Z",'#f0d6a8',0.16),filt='b40'))
# old man walking in, facing left, stick, shawl, dhoti-kurta
P_=pose_old_walk(); C='#27241f'; RIM='#f7dcab'
shawl=poly([(-4,-84),(4,-86),(10,-80),(12,-66),(10,-54),(-2,-54),(-8,-60),(-9,-72)],C)
dhoti=poly([(-1,-52),(9,-52),(12,-36),(10,-24),(-6,-24),(-8,-34)],C)
stick=f'<path d="M-15,-50 L-22,0" stroke="{C}" stroke-width="1.6" stroke-linecap="round"/>'
def fig_(c): 
    return body2(P_,c)+shawl.replace(C,c)+dhoti.replace(C,c)+stick.replace(C,c)
x,y,s=640,1640,6.0
b.append(g(P(f"M{x-40},{y} L{x+60},{y} L{x+380},1920 L{x+120},1920 Z",'#1a1713',0.5),filt='b8'))
b.append(g(f'<g transform="translate({x-4},{y-2}) scale({s})">{fig_(RIM)}</g><g transform="translate({x},{y}) scale({s})">{fig_(C)}</g>',filt='roughS'))
b.append(g(S(f"M{x-40},{y-596} C{x-16},{y-604} {x+8},{y-596} {x+20},{y-580}",'#f8e8c8',5,0.9),filt='roughS'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
