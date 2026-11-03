import sys; sys.path.insert(0,"/home/claude/udhaar/scripts")
from art import *; from shapes import *; from manq import *; from station import *
import random, math
# Kabir walking down Platform 4 (from behind), blue shirt, diary in hand; pillars and light shafts; stall glowing far end
d=RED_DEF+lg('sky',[(0,'#e9d6b0'),(1,'#c9b896')])+lg('plat',[(0,'#8f887a'),(1,'#3e3a34')])+rg('far',[(0,'#fff4d8',1),(1,'#f2d6a6',0)])
VY=900
b=[R(0,0,W,H,'url(#sky)'),E(540,VY-30,380,260,'url(#far)')]
b.append(P(f"M0,1920 L0,1400 L510,{VY+10} L570,{VY+10} L1080,1400 L1080,1920 Z",'url(#plat)'))
b.append(g(canopy(0,VY,'#5e5a52'),filt='rough'))
b.append(g(pillars(VY,side=-1,x0=120)+pillars(VY,side=1,x0=120),filt='roughS'))
b.append(g(''.join(P(f"M{x},170 L{x+60},170 L{x+340},1400 L{x+170},1400 Z",'#fff3d6',0.15) for x in (220,520)),filt='b16'))
b.append(g(E(470,VY+30,60,40,'#ffd890',0.6)+''.join(E(470+i*3,VY-i*26,14+i*4,18,'#ffffff',0.14) for i in range(7)),filt='b3'))
P_=pose_stand_side()
b.append(g(f'<path d="{shape("boy")}" fill="#3f566c" transform="translate(600,1760) scale(8.2)"/>'+f'<path d="M-6.2,-92.5 C-6.5,-101 6.5,-101 6.2,-92.5 L6,-86 L-6,-86 Z" fill="#141010" transform="translate(600,1760) scale(8.2)"/>'+S("M548,1000 C540,1100 540,1300 552,1420",'#f3dcae',4,0.6),filt='roughS'))
b.append(g(R(686,1340,52,70,'url(#ledger)',1,'rx="4"'),filt='roughS'))
b.append(g(P("M560,1760 L650,1760 L760,1920 L520,1920 Z",'#1b1915',0.45),filt='b6'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
