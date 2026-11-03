import sys; sys.path.insert(0,'/home/claude/udhaar/scripts')
from art import *; from shapes import *
import random
random.seed(24)
# Wall at night: wall clock above a paper calendar; time running
d=lg('wall',[(0,'#58645c'),(1,'#333c37')])+rg('bulb',[(0,'#ffe2a6',0.45),(1,'#ffe2a6',0)],0.7,0.05,0.9)
b=[R(0,0,W,H,'url(#wall)')]
b.append(g(''.join(E(random.uniform(0,W),random.uniform(0,H),random.uniform(60,200),random.uniform(40,160),random.choice(['#55615a','#647068','#4a5550']),0.35) for _ in range(30)),filt='roughL'))
# clock
b.append(g(E(552,412,214,214,'#1a1714',0.5),filt='b12'))
b.append(g(E(540,400,210,210,'#3a2c20')+E(540,400,186,186,'#e8dfc8')+''.join(R(536,226,8,26,'#2a2a2a',1,f'transform="rotate({i*30} 540 400)"') for i in range(12))+R(534,280,12,130,'#1e1e1e',1,'rx="5" transform="rotate(35 540 400)"')+R(536,240,8,170,'#1e1e1e',1,'rx="4" transform="rotate(-62 540 400)"')+R(538,230,4,180,'#8a2a2a',1,'transform="rotate(140 540 400)"')+E(540,400,12,12,'#1e1e1e'),filt='roughS'))
# calendar (one month grid), nail + string
cal=R(220,760,640,880,'#ece5d2')+R(220,760,640,200,'#9a8f78')+R(220,960,640,10,'#7a705c')
for r in range(5):
    for c in range(7):
        n=r*7+c+1
        if n<=31: cal+=htext(262+c*86,1040+r*120,str(n),44,'#3a3a3a',0,'Mukta',500,0.85)
cal+=''.join(S(f"M{250+c*86},{1000+r*120} l50,50 M{300+c*86},{1000+r*120} l-50,50",'#5a2a2a',4,0.75) for r in range(2) for c in range(7) if r*7+c<10)
b.append(g(R(236,780,640,880,'#121110',0.5),filt='b12'))
b.append(g(S("M540,690 L330,770 M540,690 L750,770",'#3a3530',3)+E(540,690,8,8,'#222')+cal,filt='roughS'))
b.append(R(0,0,W,H,'url(#bulb)'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
