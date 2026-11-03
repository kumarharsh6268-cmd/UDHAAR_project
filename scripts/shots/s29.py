import sys; sys.path.insert(0,'/home/claude/udhaar/scripts')
from art import *; from shapes import *; from manq import *
import random
random.seed(29)
# Wide: Kabir on the floor by the open trunk, red diary in hand; Ma appears in the doorway, backlit
d=RED_DEF+lg('wall',[(0,'#46524b'),(1,'#262d29')])+lg('hall',[(0,'#f6d59a'),(1,'#d79a54')])+rg('bulb',[(0,'#ffe2a6',0.5),(1,'#ffe2a6',0)],0.3,0.15,0.7)
b=[R(0,0,W,H,'url(#wall)')]
b.append(R(610,380,330,960,'#1a1512')); b.append(R(640,410,270,930,'url(#hall)'))
b.append(g(P("M640,1340 L910,1340 L1080,1920 L520,1920 Z",'#f2c47a',0.28),filt='b16'))
b.append(P("M0,1340 L1080,1340 L1080,1920 L0,1920 Z",'#2a2825',0.92))
b.append(g(P("M640,1340 L910,1340 L1060,1920 L560,1920 Z",'#e8b46a',0.22),filt='b24'))
# Ma in doorway
b.append(g(f'<path d="{shape("womanc")}" fill="#f6dcab" transform="translate(779,1338) scale(8.6)"/>',filt='b4'))
b.append(g(f'<path d="{shape("womanc")}" fill="#191614" transform="translate(775,1340) scale(8.6)"/>',filt='roughS'))
# trunk left foreground
b.append(g(R(60,1430,380,210,'#2c4344')+P("M60,1430 L150,1380 L530,1380 L440,1430 Z",'#0f1414')+P("M150,1380 L530,1380 L510,1170 L130,1170 Z",'#3e5a5a')+R(230,1424,40,40,'#9a7a3a'),filt='rough'))
# Kabir sitting on floor right of trunk, facing left, ledger red on his knees
P_=pose_sit_floor()
b.append(g(f'<g transform="translate(600,1720) scale(8.4)">{body2(P_,"#24282b")}</g>',filt='roughS'))
b.append(g(R(330,1360,110,140,'url(#ledger)',1,'transform="rotate(-20 385 1430)"'),filt='roughS'))
b.append(S("M540,0 L540,120",'#151412',4)); b.append(E(540,140,18,24,'#fff3d4'))
b.append(R(0,0,W,H,'url(#bulb)'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
