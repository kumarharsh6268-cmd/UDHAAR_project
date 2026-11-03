import sys; sys.path.insert(0,"/home/claude/udhaar/scripts")
from art import *; from shapes import *; from manq import *; from station import *
import random, math
# Shankar stops, recognises Kabir: his warm side-lit profile, steam drifting between
d=rg('bg',[(0,'#e9c88e'),(0.5,'#8a6a46'),(1,'#2e2620')],0.1,0.3,0.9)
b=[R(0,0,W,H,'#2a221c'),R(0,0,W,H,'url(#bg)')]
b.append(g(shankar_lit(),tf='translate(170,330) scale(1.12)',filt='roughS'))
b.append(g(''.join(E(120+i*50,1200-i*120,90,140,'#ffffff',0.06) for i in range(8)),filt='b24'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
