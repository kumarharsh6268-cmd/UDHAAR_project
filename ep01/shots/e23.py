import sys; sys.path.insert(0,"/home/claude/udhaar/scripts")
from art import *; from shapes import *; from manq import *; from station import *
import random, math
# On the counter: the folded bank notice next to Papa's chipped glass. What weighs more?
d=GLASS_DEF+lg('wood',[(0,'#6a4f38'),(1,'#3a2a1e')])+lg('paper',[(0,'#f2efe6'),(1,'#d8d2c4')],0,0,1,1)+rg('sun',[(0,'#fff0cc',0.5),(1,'#fff0cc',0)],0.7,0.2,0.8)
b=[R(0,0,W,H,'url(#wood)')]
b.append(g(''.join(S(f"M0,{y} C300,{y+random.uniform(-14,14)} 700,{y+random.uniform(-14,14)} 1080,{y}",'#4a3626',6,0.6) for y in range(0,1920,44)),filt='rough'))
b.append(g(R(150,820,380,520,'#120d09',0.45,'transform="rotate(-6 340 1080)"'),filt='b12'))
b.append(g(R(130,800,380,520,'url(#paper)',1,'transform="rotate(-6 320 1060)"')+''.join(R(170,850+i*30,300-(i%3)*60,8,'#4a5160',0.6,f'transform="rotate(-6 320 1060)"') for i in range(14))+S("M140,1060 L500,1020",'#c9c3b4',4,0.8),filt='roughS'))
b.append(g(E(780,1280,130,34,'#1a130d',0.5),filt='b8'))
b.append(g(chai_glass(780,1000,2.0,True,0.7,True),filt='roughS'))
b.append(R(0,0,W,H,'url(#sun)'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
