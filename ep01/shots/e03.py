import sys; sys.path.insert(0,"/home/claude/udhaar/scripts")
from art import *; from shapes import *; from manq import *; from station import *
import random, math
# Shankar's page: name, Papa's small note "प्लेटफ़ॉर्म 4"; amount/year out of focus for now
d=PAGE_DEF+RED_DEF+rg('bulb',[(0,'#ffe8b8',0.5),(1,'#ffe2a6',0)],0.4,0.4,0.8)
b=[R(0,0,W,H,'#17120f')]
b.append(g(R(40,180,1000,1560,'url(#ledger)',1,'rx="16"'),filt='rough'))
b.append(g(R(80,220,920,1480,'url(#pagec)')+''.join(S(f"M110,{y} L970,{y}",'#9fb2b6',1.8,0.6) for y in range(330,1680,64))+S("M190,240 L190,1690",'#d08a8a',2.5,0.6),filt='roughS'))
b.append(g(htext(220,440,'1.',90,'#1f2142')+htext(330,440,'शंकर',150,'#1f2142',-2),filt='roughS'))
b.append(g(htext(230,610,'₹ 6,000  —  2003',70,'#1f2142'),filt='b8',op=0.45))
b.append(g(htext(290,860,'प्लेटफ़ॉर्म चार',96,'#1f2142',-4)+S("M290,900 C420,884 580,880 720,868",'#1f2142',3,0.5),filt='roughS'))
b.append(g(hand(930,1050,120,11,(1,1,0,0,0),'R',skin='#6b4632',hi='#a06e4c',lo='#3e281c')+P("M980,1140 L1120,1100 L1120,1500 L1020,1520 Z",'#6f8aa0'),filt='roughS'))
b.append(R(0,0,W,H,'url(#bulb)'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
