import sys; sys.path.insert(0,"/home/claude/udhaar/scripts")
from art import *; from shapes import *; from manq import *; from station import *
import random, math
# Shankar behind the stall seen through thick kettle steam: a stranger until yesterday
d=lg('bg',[(0,'#d9c49c'),(1,'#6a5a46')])+rg('sun',[(0,'#fff2d4',0.9),(1,'#fff2d4',0)],0.65,0.35,0.6)
b=[R(0,0,W,H,'url(#bg)'),R(0,0,W,H,'url(#sun)')]
P_=pose_old_walk(); C='#2b2824'
sh=poly([(-4,-84),(4,-86),(10,-80),(12,-66),(10,-54),(-2,-54),(-8,-60),(-9,-72)],C)
b.append(g(f'<g transform="translate(600,1750) scale(13)">{body2(P_,C)}{sh}</g>',filt='b4'))
b.append(g(R(0,1300,W,620,'#3e2e22')+R(0,1290,W,40,'#5a4330'),filt='rough'))
b.append(g(stove(300,1270,1.3)+kettle(300,1270,1.4),filt='roughS'))
b.append(g(''.join(E(380+i*22,1050-i*90,140+i*26,90,'#ffffff',0.16) for i in range(12)),filt='smoke'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
