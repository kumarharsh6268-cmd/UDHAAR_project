import sys; sys.path.insert(0,"/home/claude/udhaar/scripts")
from art import *; from shapes import *; from manq import *; from station import *
import random, math
random.seed(2)
# MEMORY of the funeral: the old man bowed at Papa's feet, closer, smoke drifting (cool memory)
d=lg('sky',[(0,'#7a858a'),(0.6,'#d8c8aa'),(1,'#4a453e')])+rg('sun',[(0,'#fff4de'),(1,'#efc995',0)])
b=[R(0,0,W,H,'url(#sky)'),E(780,1000,620,520,'url(#sun)',0.9)]
b.append(g(''.join(E(700+i*14+random.uniform(-10,10),1100-i*72,80+i*14,58,'#f3ead8',0.16) for i in range(14)),filt='smoke'))
b.append(P("M0,1350 L1080,1350 L1080,1920 L0,1920 Z",'#57514a',0.92))
b.append(g(P("M-40,1580 C80,1500 220,1490 330,1500 C380,1505 400,1530 410,1560 L410,1640 L-40,1660 Z",'#d6cfbf')+''.join(E(10+i*26,1505-(i%3)*3,8,7,'#dc9f4c') for i in range(14)),filt='roughS'))
P_=pose_old_kneel(); C='#26231f'; RIM='#f8ddaa'
shawl=poly([(-24,-52),(-12,-58),(-2,-50),(4,-36),(-6,-36),(-16,-42)],C)
def F(c): return body2(P_,c)+shawl.replace(C,c)
x,y,s=650,1760,11.5
b.append(g(f'<g transform="translate({x+5},{y-4}) scale({s})">{F(RIM)}</g><g transform="translate({x},{y}) scale({s})">{F(C)}</g>',filt='roughS'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
