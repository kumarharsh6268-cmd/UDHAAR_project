import sys; sys.path.insert(0,"/home/claude/udhaar/scripts")
from art import *; from shapes import *; from manq import *; from station import *
import random, math
random.seed(6)
# The tea stall: tin awning, kettle steaming on kerosene stove, glasses on a tray, a hook under the awning with one glass apart
d=GLASS_DEF+lg('wall',[(0,'#7d6c55'),(1,'#3e3329')])+rg('sun',[(0,'#fff2d4',0.7),(1,'#fff2d4',0)],0.8,0.1,0.8)
b=[R(0,0,W,H,'url(#wall)')]
b.append(g(''.join(R(random.uniform(0,W),random.uniform(0,1200),random.uniform(40,160),random.uniform(30,120),random.choice(['#655f53','#7a7466','#5a554b']),0.4) for _ in range(30)),filt='roughL'))
# tin awning (chhappar) top
b.append(g(P("M-40,120 L1120,60 L1120,300 L-40,360 Z",'#5c5d58')+''.join(S(f"M{x},{110-x*0.055} L{x},{350-x*0.055}",'#46473f',6) for x in range(0,1100,60))+S("M-40,360 L1120,300",'#2a2a26',10),filt='rough'))
# hook with the single chipped glass hanging apart
b.append(g(S("M820,318 L820,380 C820,400 840,404 846,388",'#2a2622',6),filt='roughS'))
b.append(g(P("M700,300 L900,300 L1000,1300 L780,1300 Z",'#fff0cc',0.18),filt='b24'))
b.append(g(chai_glass(842,430,1.3,True,0,False,True),filt='roughS'))
b.append(g(E(842,470,80,90,'#fff6dc',0.25),filt='b24'))
# counter
b.append(g(R(60,1240,960,60,'#5a4330')+R(80,1300,920,620,'#3e2e22')+''.join(R(80,1330+i*120,920,6,'#2e2218') for i in range(5)),filt='rough'))
b.append(g(stove(320,1180,1.4)+kettle(320,1180,1.5),filt='roughS'))
b.append(g(''.join(E(560+i*14,900-i*80,80+i*20,60,'#ffffff',0.10) for i in range(9)),filt='smoke'))
b.append(g(''.join(R(110+i*70,1110,56,120,'#c9b89a',0.7,'rx="10"')+R(110+i*70,1096,56,20,'#6a5a44',1,'rx="4"') for i in range(2)),filt='roughS'))
b.append(g(R(600,1220,340,24,'#7a7a74',1,'rx="8"')+''.join(chai_glass(640+i*62,1110,0.55,False,0.0,False,True) for i in range(5)),filt='roughS'))
b.append(R(0,0,W,H,'url(#sun)'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
