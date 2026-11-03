import sys; sys.path.insert(0,"/home/claude/udhaar/scripts")
from art import *; from shapes import *; from manq import *; from station import *
import random, math
# MEMORY: Papa (khaki uniform, cap) walking the same platform years ago - same gait (sepia)
d=lg('bg',[(0,'#d6bf94'),(1,'#7d6748')])
VY=900
b=[R(0,0,W,H,'url(#bg)')]
b.append(P(f"M0,1920 L0,1400 L510,{VY+10} L570,{VY+10} L1080,1400 L1080,1920 Z",'#8a7656'))
b.append(g(canopy(0,VY,'#6a5a42'),filt='rough'))
b.append(g(pillars(VY,side=-1,x0=120,col='#cdb78e',shade='#9a8462')+pillars(VY,side=1,x0=120,col='#cdb78e',shade='#9a8462'),filt='roughS'))
P_=pose_stand_side(); P_['ankleR']=(14,-6); P_['toeR']=(9,-2); P_['ankleL']=(-12,-2)
cap='<path d="M-7,-97 C-7,-104 7,-104 7,-97 L10,-96 L-7,-95 Z" fill="#3a2e20"/><rect x="-9" y="-96" width="20" height="2.4" fill="#2a2018"/>'
b.append(g(f'<g transform="translate(600,1720) scale(-9,9)">{body2(P_,"#4a3c2a")}{cap}</g>',filt='roughS'))
b.append(g(f'<g transform="translate(600,1720) scale(-9,9)">'+poly([(-11,-80),(11,-80),(12,-56),(-12,-56)],'#7a6646')+'</g>',filt='roughS',op=0.9))
open(sys.argv[1],'w').write(svg(''.join(b),d))
