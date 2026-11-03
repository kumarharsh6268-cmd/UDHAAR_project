import sys; sys.path.insert(0,"/home/claude/udhaar/scripts")
from art import *; from shapes import *; from manq import *; from station import *
import random, math
# Back on its hook, alone in a beam of morning light: the glass he kept for twenty-three years
d=GLASS_DEF+lg('bg',[(0,'#3e3226'),(1,'#1e1812')])
b=[R(0,0,W,H,'url(#bg)')]
b.append(g(P("M380,0 L700,0 L860,1920 L240,1920 Z",'#fff0cc',0.20),filt='b24'))
b.append(g(P("M-40,0 L1120,0 L1120,300 L-40,360 Z",'#2e2e2a')+S("M-40,360 L1120,300",'#1a1a18',12),filt='rough'))
b.append(g(S("M520,340 L520,520 C520,560 560,568 572,540",'#1e1c1a',9),filt='roughS'))
b.append(g(chai_glass(560,620,2.3,True,0,False,True),filt='roughS'))
b.append(g(E(560,780,240,260,'#fff4d6',0.18),filt='b40'))
b.append(g(''.join(E(random.uniform(300,800),random.uniform(200,1700),2.5,2.5,'#fff6dc',random.uniform(0.3,0.8)) for _ in range(40)),filt='b1'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
