import sys; sys.path.insert(0,"/home/claude/udhaar/scripts")
from art import *; from shapes import *; from manq import *; from station import *
import random, math
# Kabir's warm side-lit profile at the station, steam drifting, puzzled
d=rg('bg',[(0,'#efd6a6'),(0.6,'#8a7656'),(1,'#3a3028')],0.15,0.35,0.9)
b=[R(0,0,W,H,'#2e2720'),R(0,0,W,H,'url(#bg)')]
b.append(g(''.join(R(80+i*200,0,40,1920,'#cfc7b0',0.25) for i in range(3)),filt='b24'))
b.append(g(kabir_lit()+kabir_kurta(fill='#55708a',edge='#e9c58e',shirt=True),tf='translate(90,330) scale(1.12)',filt='roughS'))
b.append(g(''.join(E(150+i*40,1400-i*120,90,130,'#ffffff',0.06) for i in range(8)),filt='b24'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
