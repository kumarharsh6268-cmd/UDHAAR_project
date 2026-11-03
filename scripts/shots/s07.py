import sys; sys.path.insert(0,'/home/claude/udhaar/scripts')
from art import *; from shapes import *; from manq import *
import random, math
random.seed(17)
d=(lg('sky',[(0,'#76828a'),(0.42,'#c4b9a3'),(0.56,'#eed9b1'),(0.64,'#dacbaf'),(1,'#3f3a34')])+rg('sun',[(0,'#fff4de'),(1,'#efc995',0)])+lg('fogb',[(0,'#e6d8bc',0),(0.5,'#e6d8bc',0.8),(1,'#e6d8bc',0)]))
HZ=1240
b=[R(0,0,W,H,'url(#sky)'),E(620,1120,640,520,'url(#sun)',0.9),E(620,1120,46,46,'#fff7e6',0.95)]
b.append(g(''.join(E(600+i*14+random.uniform(-10,10),1100-i*72,70+i*14,54,'#f3ead8',0.16) for i in range(14)),filt='smoke'))
b.append(g(''.join(f'<path d="{shape(n)}" fill="#958e82" transform="translate({x},{HZ+14}) scale({h/100})"/>' for x,h,n in [(110,190,'manc'),(260,170,'womanc'),(880,180,'womanc'),(1000,210,'manc')]),filt='b6',op=0.75))
b.append(R(0,HZ-160,W,320,'url(#fogb)'))
b.append(P(f"M0,{HZ} L1080,{HZ} L1080,1920 L0,1920 Z",'#57514a',0.92))
b.append(g(P(f"M580,{HZ} L660,{HZ} L900,1920 L340,1920 Z",'#f0d6a8',0.15),filt='b40'))
# bier (feet end) on left: bamboo + shroud silhouette, marigolds catching light
D='#2b251f'; RIM='#f8ddaa'
bier=P("M-40,1560 C40,1500 160,1490 250,1500 C300,1505 330,1520 340,1545 C345,1570 330,1590 300,1600 L-40,1610 Z",'#3a352f')+R(-40,1600,420,22,D,1,'rx="10"')+R(-40,1640,420,18,D,1,'rx="9"')+R(330,1600,14,120,D)
b.append(g(S("M-40,1558 C40,1498 160,1488 250,1498 C300,1503 330,1518 340,1543",RIM,5,0.9)+bier+''.join(E(10+i*24,1505-(i%3)*3,6,5,'#dc9f4c') for i in range(13)),filt='roughS'))
# old man kneeling at the feet, bowed, crying
P_=pose_old_kneel(); C='#26231f'
shawl=poly([(-24,-52),(-12,-58),(-2,-50),(4,-36),(-6,-36),(-16,-42)],C)
def F(c): return body2(P_,c)+shawl.replace(C,c)
x,y,s=560,1720,7.2
b.append(g(f'<g transform="translate({x+4},{y-3}) scale({s})">{F(RIM)}</g><g transform="translate({x},{y}) scale({s})">{F(C)}</g>',filt='roughS'))
b.append(g(E(x-20,y+6,260,24,'#15120f',0.55),filt='b8'))
# Kabir standing behind, right, soft focus
b.append(g(f'<path d="{shape("manc")}" fill="#2e2c28" transform="translate(900,1800) scale(6.2)"/>',filt='b6'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
