import sys; sys.path.insert(0,"/home/claude/udhaar/scripts")
from art import *; from shapes import *; from manq import *; from station import *
import random, math
# Macro on Papa's handwriting: the amount and the year
d=PAGE_DEF+rg('bulb',[(0,'#ffe8b8',0.45),(1,'#ffe2a6',0)],0.5,0.4,0.8)
b=[R(0,0,W,H,'url(#pagec)')]
b.append(g(''.join(S(f"M0,{y} L1080,{y}",'#9fb2b6',4,0.5) for y in range(300,1920,330)),filt='roughS'))
b.append(g(htext(-40,820,'₹ 6,000',330,'#1f2142',-2)+htext(120,1380,'2003',300,'#1f2142',-2),filt='roughS'))
b.append(R(0,0,W,H,'url(#bulb)'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
