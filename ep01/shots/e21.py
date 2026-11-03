import sys; sys.path.insert(0,"/home/claude/udhaar/scripts")
from art import *; from shapes import *; from manq import *; from station import *
import random, math
# Shankar's page in full: amount and year now sharp
d=PAGE_DEF+RED_DEF+rg('bulb',[(0,'#ffe8b8',0.5),(1,'#ffe2a6',0)],0.4,0.4,0.8)
b=[R(0,0,W,H,'url(#pagec)')]
b.append(g(''.join(S(f"M0,{y} L1080,{y}",'#9fb2b6',2,0.5) for y in range(150,1920,110))+S("M120,0 L120,1920",'#d08a8a',2.5,0.6),filt='roughS'))
b.append(g(htext(160,560,'1.',100,'#1f2142')+htext(290,560,'शंकर',170,'#1f2142',-2)+htext(170,860,'₹ 6,000',150,'#1f2142',-2)+htext(260,1080,'2003',110,'#1f2142',-2)+htext(170,1330,'प्लेटफ़ॉर्म चार',80,'#1f2142',-3),filt='roughS'))
b.append(g(hand(900,1060,150,10,(1,1,0,0,0),'R',skin='#6b4632',hi='#a06e4c',lo='#3e281c')+P("M940,1150 L1120,1110 L1120,1500 L1000,1520 Z",'#6f8aa0'),filt='roughS'))
b.append(R(0,0,W,H,'url(#bulb)'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
