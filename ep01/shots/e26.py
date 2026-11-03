import sys; sys.path.insert(0,"/home/claude/udhaar/scripts")
from art import *; from shapes import *; from manq import *; from station import *
import random, math
random.seed(26)
# Wide two-shot in silhouette: Kabir at the counter, Shankar behind, steam rising between them; platform beyond
d=lg('bg',[(0,'#e6d2aa'),(1,'#a8946e')])+rg('sun',[(0,'#fff6e0',1),(1,'#fff6e0',0)],0.5,0.45,0.5)
b=[R(0,0,W,H,'url(#bg)'),R(0,0,W,H,'url(#sun)')]
b.append(g(P("M-40,380 L1120,330 L1120,520 L-40,580 Z",'#3a3934'),filt='rough'))
P_=pose_old_walk(); C='#262420'
sh=poly([(-4,-84),(4,-86),(10,-80),(12,-66),(10,-54),(-2,-54),(-8,-60),(-9,-72)],C)
b.append(g(f'<g transform="translate(790,1420) scale(8.5)">{body2(P_,"#f8e2b6")}{sh.replace(C,"#f8e2b6")}</g>',filt='b2',op=0.9))
b.append(g(f'<g transform="translate(794,1422) scale(8.5)">{body2(P_,C)}{sh}</g>',filt='roughS'))
b.append(g(R(380,1140,700,780,'#2e241c')+R(360,1120,740,40,'#3e3024'),filt='rough'))
b.append(g(kettle(560,1120,0.8),filt='roughS'))
b.append(g(''.join(E(620+i*8,950-i*70,60+i*14,50,'#ffffff',0.13) for i in range(9)),filt='smoke'))
b.append(g(f'<path d="{shape("boy")}" fill="#f8e2b6" transform="translate(246,1858) scale(9.6)"/>',filt='b2',op=0.8))
b.append(g(f'<path d="{shape("boy")}" fill="#22282e" transform="translate(250,1860) scale(9.6)"/>',filt='roughS'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
