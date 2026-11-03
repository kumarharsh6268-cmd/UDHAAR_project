import sys; sys.path.insert(0,"/home/claude/udhaar/scripts")
from art import *; from shapes import *; from manq import *; from station import *
import random, math
# MEMORY: Papa's hand (khaki sleeve) around the same chipped glass at this stall, years ago
d=GLASS_DEF+lg('bg',[(0,'#d8c096'),(1,'#7a6344')])+lg('skin',[(0,'#9a7050'),(1,'#5a3e2a')],0,0,0,1)
b=[R(0,0,W,H,'url(#bg)')]
b.append(g(R(0,1300,W,620,'#5a4632')+R(0,1290,W,30,'#7a6244'),filt='rough'))
b.append(g(chai_glass(620,900,3.0,True,0.75,True),filt='roughS'))
hd=cr_path(HAND_R5)
b.append(g(P("M940,940 L1120,900 L1120,1240 L960,1260 Z",'#8c7853')+f'<path d="{hd}" fill="url(#skin)" transform="translate(990,1080) rotate(-90) scale(2.3)"/>',filt='roughS'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
