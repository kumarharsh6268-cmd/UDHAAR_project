import sys; sys.path.insert(0,'/home/claude/udhaar/scripts')
from art import *; from shapes import *; from manq import hand
d=PAGE_DEF+rg('bulb',[(0,'#ffe8b8',0.55),(1,'#ffe2a6',0)],0.4,0.4,0.8)
b=[R(0,0,W,H,'url(#pagec)')]
b.append(g(''.join(S(f"M0,{y} L1080,{y}",'#9fb2b6',2,0.5) for y in range(120,1920,110)),filt='roughS'))
b.append(g(htext(-120,980,'किसी से पैसे मत माँगना।',190,'#1f2142',-2),filt='roughS'))
b.append(g(E(700,1010,140,60,'#1f2142',0.10),filt='b16'))
b.append(g(hand(860,1520,195,13,(1,1,1,1,1),'R',skin='#6b4632',hi='#a06e4c',lo='#3e281c')+P("M840,1560 L1100,1470 L1100,1920 L880,1920 Z",'#6f8aa0'),filt='roughS'))
b.append(R(0,0,W,H,'url(#bulb)'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
