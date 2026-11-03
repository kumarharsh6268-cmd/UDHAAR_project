import sys; sys.path.insert(0,"/home/claude/udhaar/scripts")
from art import *; from shapes import *; from manq import *; from station import *
import random, math
# Two glasses steaming on the wooden counter: one for Kabir, and Papa's chipped one
d=GLASS_DEF+lg('bg',[(0,'#c9b28a'),(1,'#5a4a38')])
b=[R(0,0,W,H,'url(#bg)')]
b.append(g(R(0,1080,W,840,'#5a4330')+''.join(S(f"M0,{y} C300,{y+random.uniform(-10,10)} 700,{y+random.uniform(-10,10)} 1080,{y}",'#4a3626',5,0.6) for y in range(1100,1920,40)),filt='rough'))
b.append(g(chai_glass(330,1180,2.0,False,0.7,True)+chai_glass(740,1210,2.0,True,0.7,True),filt='roughS'))
b.append(g(E(330,1500,170,26,'#2a1f16',0.5)+E(740,1530,170,26,'#2a1f16',0.5),filt='b8'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
