import sys; sys.path.insert(0,"/home/claude/udhaar/scripts")
from art import *; from shapes import *; from manq import *; from station import *
import random, math
# Macro: the chipped rim catching the morning light
d=GLASS_DEF+rg('bg',[(0,'#f6e2b8'),(1,'#6a5844')],0.6,0.3,0.8)
b=[R(0,0,W,H,'url(#bg)')]
b.append(g(R(0,1500,W,420,'#3a2c20'),filt='rough'))
b.append(g(chai_glass(420,700,6.2,True,0,False,True),filt='roughS'))
b.append(g(E(570,640,90,60,'#fffaf0',0.5),filt='b16'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
