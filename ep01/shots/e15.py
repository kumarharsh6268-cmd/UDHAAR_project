import sys; sys.path.insert(0,"/home/claude/udhaar/scripts")
from art import *; from shapes import *; from manq import *; from station import *
import random, math
# Now: Shankar pours fresh chai from the kettle into the chipped glass
d=GLASS_DEF+lg('bg',[(0,'#5e4e3c'),(1,'#2e241c')])+rg('sun',[(0,'#ffe8b8',0.6),(1,'#ffe8b8',0)],0.7,0.2,0.7)
b=[R(0,0,W,H,'url(#bg)'),R(0,0,W,H,'url(#sun)')]
b.append(g(R(0,1380,W,540,'#4a3828')+R(0,1370,W,26,'#6a5238'),filt='rough'))
b.append(g(chai_glass(560,1130,1.9,True,0.55,True),filt='roughS'))
b.append(g(P("M520,400 C520,600 540,800 556,1110 L568,1110 C556,800 548,600 548,400 Z",'#b87a3a'),filt='roughS'))
b.append(g(f'<g transform="rotate(-38 560 300)">'+kettle(560,380,2.2)+'</g>',filt='roughS'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
