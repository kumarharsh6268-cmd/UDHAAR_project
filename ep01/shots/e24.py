import sys; sys.path.insert(0,"/home/claude/udhaar/scripts")
from art import *; from shapes import *; from manq import *; from station import *
import random, math
# Home, the house to be saved: the blue-green door with the notice, Ma's shadow behind the window grille (memory of this morning)
d=lg('wall',[(0,'#bfb39b'),(1,'#9a8f79')])+lg('door',[(0,'#5d7f7a'),(1,'#4a6964')],0,0,1,0)+lg('win',[(0,'#ffe2a6'),(1,'#e0a860')])
b=[R(0,0,W,H,'url(#wall)')]
b.append(g(''.join(E(random.uniform(0,W),random.uniform(0,H),random.uniform(40,200),random.uniform(30,160),random.choice(['#b0a48c','#c9bda3','#968a74']),0.4) for _ in range(50)),filt='roughL'))
b.append(g(R(90,380,560,1300,'#3a2c20')+R(115,405,510,1275,'url(#door)')+R(368,405,6,1275,'#2b3d3a'),filt='rough'))
b.append(g(R(430,700,170,240,'#efece2')+''.join(R(445,730+i*18,140-(i%3)*30,5,'#4a5160',0.6) for i in range(9)),filt='roughS'))
b.append(g(R(730,520,280,380,'url(#win)')+''.join(R(730+i*56,520,7,380,'#2a2622') for i in range(6))+R(730,520,280,380,'none',1,'stroke="#2a2622" stroke-width="14"'),filt='roughS'))
b.append(g(f'<path d="{shape("womanc")}" fill="#4a3424" transform="translate(880,1000) scale(4.6)"/>',filt='b4'))
b.append(g(R(40,1680,1000,240,'#6a6458'),filt='rough'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
