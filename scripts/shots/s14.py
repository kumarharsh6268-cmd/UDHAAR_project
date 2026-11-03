import sys; sys.path.insert(0,'/home/claude/udhaar/scripts')
from art import *; from shapes import *
import random, math
random.seed(14)
# Dusk: the small Verma house in a narrow Ranipur lane; one warm window; Ma's silhouette; wires; streetlight
d=(lg('sky',[(0,'#2f3846'),(0.5,'#6b6a78'),(0.8,'#b59a8e'),(1,'#c9a88f')])+rg('win',[(0,'#ffd99a',1),(0.6,'#f0a85a',0.5),(1,'#f0a85a',0)])+lg('lane',[(0,'#4b4744'),(1,'#1f1d1c')]))
b=[R(0,0,W,H,'url(#sky)')]
# neighbouring houses, flat-roofed, layered
b.append(g(P("M0,520 L240,520 L240,600 L380,600 L380,1500 L0,1500 Z",'#3a3d44')+P("M760,560 L1080,560 L1080,1500 L760,1500 Z",'#353840')+R(800,640,80,110,'#5a5148')+R(940,640,80,110,'#2a2c31'),filt='rough'))
# water tank on roof, antenna
b.append(g(R(60,450,120,70,'#2c2f35',1,'rx="10"')+S("M300,600 L300,470 M270,500 L330,500 M280,530 L320,530",'#24262b',4),filt='roughS'))
# the Verma house (centre): small two-storey-ish, plaster, door, one lit window
H0=760
b.append(g(P(f"M360,{H0} L780,{H0} L780,1500 L360,1500 Z",'#5b5e5f')+R(350,H0-20,440,30,'#4a4c4e')+R(420,1060,180,440,'#33463f')+R(640,900,110,140,'#2a2a2a'),filt='rough'))
b.append(E(695,970,200,200,'url(#win)',0.6))
b.append(g(R(645,905,100,130,'#f6c680')+R(693,905,4,130,'#4a3a2a')+''.join(R(645,905+i*26,100,3,'#4a3a2a') for i in range(5)),filt='roughS'))
# Ma silhouette in window
b.append(g(E(680,950,18,22,'#3a2a1f')+P("M650,1035 C652,990 664,970 680,968 C700,970 712,990 716,1035 Z",'#3a2a1f'),filt='roughS'))
# notice on door (tiny pale rectangle)
b.append(g(R(520,1160,50,70,'#d9d4c6',0.8),filt='roughS'))
# overhead wires
b.append(''.join(S(f"M-20,{y} C300,{y+60} 700,{y+40} 1100,{y-20}",'#15171b',2.5,0.9) for y in (380,420,470)))
# streetlight flickering on
b.append(g(S("M900,1500 L900,700 C900,660 880,650 850,650",'#1d1f23',8)+E(840,660,26,10,'#ffe9c0'),filt='roughS'))
b.append(g(E(840,700,160,220,'#ffe2a6',0.18),filt='b40'))
# lane ground, wet sheen
b.append(P("M0,1500 L1080,1500 L1080,1920 L0,1920 Z",'url(#lane)'))
b.append(g(E(695,1600,80,240,'#ffcf86',0.18)+E(840,1620,60,220,'#ffe2a6',0.12),filt='b24'))
b.append(g(S("M0,1500 L1080,1500",'#2a2928',6),filt='roughS'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
