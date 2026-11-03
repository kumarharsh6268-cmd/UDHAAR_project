import sys; sys.path.insert(0,"/home/claude/udhaar/scripts")
from art import *; from shapes import *; from manq import *; from station import *
import random, math
# Kabir's walk: low angle on the platform, his feet in chappals and long morning shadow
d=lg('plat',[(0,'#a39a88'),(1,'#5a5348')])+rg('sun',[(0,'#fff0cc',0.6),(1,'#fff0cc',0)],0.5,0.0,0.8)
b=[R(0,0,W,H,'url(#plat)'),R(0,0,W,H,'url(#sun)')]
b.append(g(''.join(R(0,y,W,8,'#7a7264',0.6) for y in range(200,1920,240))+R(0,1500,W,40,'#d9b84a',0.7)+R(0,1540,W,380,'#2b2824'),filt='rough'))
P_=pose_stand_side(); P_['ankleR']=(14,-6); P_['toeR']=(9,-2); P_['ankleL']=(-12,-2); P_['kneeR']=(8,-26); P_['kneeL']=(-8,-27)
b.append(g(f'<g transform="translate(540,1440) scale(1,-0.35) translate(0,0) scale(17)">{body2(P_,"#2a2622")}</g>',filt='b8',op=0.5))
b.append(g(f'<g transform="translate(540,1440) scale(17)">{body2(P_,"#4a5a6a")}</g>',filt='roughS'))
b.append(g(R(0,0,W,620,'#000',0)+E(540,300,300,200,'#fff4dc',0.0),filt='b6'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
