import sys; sys.path.insert(0,'/home/claude/udhaar/scripts')
from art import *; from shapes import *; from manq import *
import random
random.seed(15)
# Dusk interior: Ma alone at her sewing machine under a small lamp; the home that could be lost
d=lg('wall',[(0,'#4e5a56'),(1,'#2b322f')])+rg('lamp',[(0,'#ffd99a',0.8),(0.35,'#e9a050',0.25),(1,'#e9a050',0)],0.42,0.42,0.6)+lg('win',[(0,'#7c86a0'),(1,'#a89090')])
b=[R(0,0,W,H,'url(#wall)')]
b.append(g(R(700,380,260,420,'url(#win)')+R(700,380,260,420,'none',1,'stroke="#1f2422" stroke-width="16"')+''.join(R(700+i*65,380,6,420,'#1f2422') for i in range(1,4))+R(700,580,260,8,'#1f2422'),filt='rough'))
b.append(P("M0,1350 L1080,1350 L1080,1920 L0,1920 Z",'#2a2623'))
b.append(g(E(460,900,640,640,'url(#lamp)'),filt='b40'))
# table + machine
b.append(g(R(120,1060,560,30,'#3a2c20')+R(140,1090,20,280,'#2a2018')+R(640,1090,20,280,'#2a2018')+R(150,1300,500,18,'#2a2018'),filt='rough'))
mach=(P("M230,1060 L230,960 C230,900 270,880 330,880 L560,880 C600,880 620,900 620,940 L620,1000 L580,1000 L580,950 C580,930 570,925 550,925 L360,925 C340,925 330,935 330,960 L330,1060 Z",'#121212')
      +E(600,1000,40,40,'#1a1a1a')+R(250,1046,380,14,'#1c1c1c')+S("M350,905 L550,905",'#c9a64a',4,0.6)+E(255,1000,14,30,'#2a2a2a'))
b.append(g(mach,filt='roughS'))
b.append(g(R(150,1048,240,16,'#d9d0bd')+P("M150,1060 C120,1120 110,1200 130,1290 L200,1290 C190,1200 190,1120 210,1060 Z",'#cfc6b2'),filt='roughS'))
# lamp
b.append(g(P("M390,700 L470,700 L500,780 L360,780 Z",'#3a3530')+R(426,600,8,100,'#2a2622')+E(430,790,40,10,'#fff0c8'),filt='roughS'))
# Ma seated, facing left, saree
P_=pose_sew(); C='#2c2a27'
saree=poly([(-6,-60),(6,-62),(10,-46),(9,-32),(4,-20),(-8,-16),(-18,-24),(-18,-32),(-8,-40)],C)
pallu=poly([(-10,-74),(-2,-78),(6,-72),(8,-60),(4,-56),(-6,-60)],'#8c877c')
fig=body2(P_,C)+saree+pallu
b.append(g(f'<g transform="translate(830,1350) scale(9)">{body2(P_,"#e5b779")}{saree.replace(C,"#e5b779")}</g>',filt='b2',op=0.8))
b.append(g(f'<g transform="translate(834,1352) scale(9)">{fig}</g>',filt='roughS'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
