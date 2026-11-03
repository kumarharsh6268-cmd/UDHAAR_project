import sys; sys.path.insert(0,"/home/claude/udhaar/scripts")
from art import *; from shapes import *; from manq import *; from station import *
import random, math
random.seed(8)
# Two-shot: Kabir arrives at the stall (left, silhouette); Shankar behind the counter stops still, steam between
d=GLASS_DEF+lg('bg',[(0,'#d9c49c'),(1,'#7a6a52')])+rg('sun',[(0,'#fff2d4',0.8),(1,'#fff2d4',0)],0.7,0.3,0.7)
b=[R(0,0,W,H,'url(#bg)'),R(0,0,W,H,'url(#sun)')]
b.append(g(P("M200,520 L1120,470 L1120,620 L200,680 Z",'#4e4f4a')+S("M200,680 L1120,620",'#2a2a26',10),filt='rough'))
P_=pose_old_walk(); C='#2b2824'
sh=poly([(-4,-84),(4,-86),(10,-80),(12,-66),(10,-54),(-2,-54),(-8,-60),(-9,-72)],C)
b.append(g(f'<g transform="translate(866,1640) scale(10)">{body2(P_,"#f6dcae")}{sh.replace(C,"#f6dcae")}</g>',filt='b2',op=0.8))
b.append(g(f'<g transform="translate(870,1642) scale(10)">{body2(P_,C)}{sh.replace(C,"#57544d")}</g>',filt='roughS'))
b.append(g(R(380,1180,700,60,'#5a4330')+R(400,1240,680,680,'#3e2e22'),filt='rough'))
b.append(g(stove(560,1130,1.0)+kettle(560,1130,1.05),filt='roughS'))
b.append(g(''.join(E(700+i*10,1000-i*70,70+i*16,55,'#ffffff',0.12) for i in range(9)),filt='smoke'))
# Kabir foreground left, back/three-quarter, blue shirt, out of focus
b.append(g(f'<path d="{shape("boy")}" fill="#2f4254" transform="translate(150,2120) scale(14)"/>'+f'<path d="M-6.2,-92.5 C-6.5,-101 6.5,-101 6.2,-92.5 L6,-86 L-6,-86 Z" fill="#100c0c" transform="translate(150,2120) scale(14)"/>',filt='b6'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
