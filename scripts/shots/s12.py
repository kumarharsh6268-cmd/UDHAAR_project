import sys; sys.path.insert(0,'/home/claude/udhaar/scripts')
from art import *; from shapes import *
import random, math
random.seed(12)
# Front door of the Verma house with a bank notice pasted on it, morning
d=(lg('wall',[(0,'#c9bda4'),(1,'#a99d86')])+lg('door',[(0,'#5d7f7a'),(1,'#4a6964')],0,0,1,0)+lg('paper',[(0,'#f2efe6'),(1,'#dcd7ca')])+lg('sun',[(0,'#fff0cf',0.5),(1,'#fff0cf',0)],1,0,0,1))
b=[R(0,0,W,H,'url(#wall)')]
b.append(g(''.join(E(random.uniform(0,W),random.uniform(0,H),random.uniform(40,200),random.uniform(30,160),random.choice(['#b9ad95','#d4c8af','#a2967f','#8e846f']),0.4) for _ in range(60)),filt='roughL'))
# door frame + double door
b.append(g(R(170,180,740,1480,'#3a2c20')+R(200,210,680,1450,'url(#door)')+R(536,210,8,1450,'#2b3d3a'),filt='rough'))
for x0 in (200,544):
    b.append(g(R(x0+40,260,256,560,'none',1,'stroke="#3e5b56" stroke-width="10"')+R(x0+40,900,256,640,'none',1,'stroke="#3e5b56" stroke-width="10"'),filt='roughS'))
# peeling paint patches
b.append(g(''.join(E(random.uniform(220,860),random.uniform(240,1640),random.uniform(6,30),random.uniform(4,20),'#9aa79d',0.6) for _ in range(40)),filt='roughS'))
# iron latch + hasp + old lock
b.append(g(R(500,980,86,22,'#2b2a28',1,'rx="6"')+R(560,960,18,70,'#2b2a28',1,'rx="6"')+P("M520,1040 C520,1010 560,1010 560,1040 L556,1040 C556,1018 524,1018 524,1040 Z",'#2b2a28')+R(510,1040,60,56,'#4d4a44',1,'rx="8"'),filt='roughS'))
# the notice, pasted with tape corners, slightly askew, at eye level on right door leaf
nt=g(R(0,0,300,420,'url(#paper)')+R(20,24,260,22,'#1f2a3a',0.85)+''.join(R(24,70+i*22,250-(i%3)*40,6,'#4a5160',0.7) for i in range(12))+R(24,350,120,30,'#2a3550',0.15)+E(220,370,40,28,'none',1,'stroke="#6a4a6a" stroke-width="3" stroke-opacity="0.6"')
     +''.join(R(x,y,46,18,'#e8e2c8',0.75,f'transform="rotate({r} {x+23} {y+9})"') for x,y,r in [(-14,-6,-30),(268,-6,30),(-14,408,30),(268,408,-30)]),tf='translate(590,520) rotate(2)')
b.append(g(R(598,530,300,420,'#1d1712',0.4),filt='b8'))
b.append(g(nt,filt='roughS'))
# threshold steps + faded rangoli
b.append(g(R(120,1660,840,50,'#7b7466')+R(80,1710,920,60,'#6a6458')+R(40,1770,1000,150,'#5a554b'),filt='rough'))
b.append(g(''.join(E(540+math.cos(a)*r,1740+math.sin(a)*r*0.25,10,4,'#d8d2c4',0.55) for r in (60,110,160) for a in [i*0.4 for i in range(16)]),filt='roughS'))
b.append(R(0,0,W,H,'url(#sun)'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
