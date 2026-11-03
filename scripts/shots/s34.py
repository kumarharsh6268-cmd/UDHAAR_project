import sys; sys.path.insert(0,'/home/claude/udhaar/scripts')
from art import *; from shapes import *
# The first name page: 1. Shankar (amount deliberately out of frame / blurred for Ep1)
d=PAGE_DEF+rg('bulb',[(0,'#ffe8b8',0.5),(1,'#ffe2a6',0)],0.45,0.35,0.8)
b=[R(0,0,W,H,'url(#pagec)')]
b.append(g(''.join(S(f"M0,{y} L1080,{y}",'#9fb2b6',2,0.5) for y in range(160,1920,120))+S("M150,0 L150,1920",'#d08a8a',2.5,0.6),filt='roughS'))
b.append(g(htext(190,830,'1.',110,'#1f2142')+htext(330,830,'शंकर',200,'#1f2142',-2),filt='roughS'))
b.append(g(htext(200,1040,'₹ 6,000 — 2003',80,'#1f2142')+S("M200,1150 c120,-10 240,10 360,-4 s200,8 300,-2",'#1f2142',4,0.7),filt='b8',op=0.55))
b.append(R(0,0,W,H,'url(#bulb)'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
