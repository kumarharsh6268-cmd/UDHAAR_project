import sys; sys.path.insert(0,"/home/claude/udhaar/scripts")
from art import *; from shapes import *; from manq import *; from station import *
import random, math
# Beyond the platform end: tracks, and a faded municipal bus parked by the depot wall in the haze
d=lg('sky',[(0,'#d9cbb0'),(1,'#efe0c2')])+lg('gnd',[(0,'#8a8272'),(1,'#4a453c')])+lg('busg',[(0,'#7a929a'),(1,'#5a7078')])
b=[R(0,0,W,H,'url(#sky)')]
b.append(g(P("M0,980 L1080,940 L1080,1920 L0,1920 Z",'url(#gnd)'),filt='rough'))
b.append(g(R(0,820,1080,170,'#b4a890',0.9)+''.join(R(i*130,840,8,150,'#9a8e78') for i in range(9)),filt='rough'))
b.append(g(R(380,830,440,180,'url(#busg)',1,'rx="16"')+''.join(R(400+i*68,850,52,62,'#d9dccf',0.75) for i in range(6))+R(380,960,440,12,'#c9b48a',0.8)+E(450,1012,26,26,'#2a2a2a')+E(750,1012,26,26,'#2a2a2a')+''.join(E(random.uniform(390,810),random.uniform(840,990),random.uniform(6,20),random.uniform(4,12),'#8a6a4a',0.5) for _ in range(14)),filt='b2'))
for k in range(2):
    b.append(g(S(f"M{460+k*120},1920 L{530+k*40},1000",'#3a3632',10)+S(f"M{620+k*120},1920 L{560+k*40},1000",'#3a3632',10),filt='roughS'))
b.append(g(''.join(R(0,1100+i*120,1080,14,'#5a5245',0.8,f'transform="skewX({-10+i*3})"') for i in range(7)),filt='rough'))
b.append(g(R(0,0,1080,1920,'#f3e6c8',0.25),filt='b40'))
b.append(g(R(-40,0,200,1920,'#2b2a28')+R(-40,0,1160,120,'#2b2a28'),filt='rough'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
