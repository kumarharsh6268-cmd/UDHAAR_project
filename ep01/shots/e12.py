import sys; sys.path.insert(0,"/home/claude/udhaar/scripts")
from art import *; from shapes import *; from manq import *; from station import *
import random, math
# His three-fingered hand lifting the chipped glass off the hook under the tin awning
d=GLASS_DEF+lg('bg',[(0,'#7d6c55'),(1,'#d8c29a')])+lg('skin',[(0,'#8a5c40'),(1,'#4a3020')],0,0,0,1)
b=[R(0,0,W,H,'url(#bg)')]
b.append(g(P("M-40,0 L1120,0 L1120,420 L-40,520 Z",'#5c5d58')+''.join(S(f"M{x},0 L{x},{520-x*0.09}",'#46473f',8) for x in range(0,1100,70))+S("M-40,520 L1120,420",'#2a2a26',14),filt='rough'))
b.append(g(S("M560,470 L560,620 C560,660 600,668 612,640",'#2a2622',10),filt='roughS'))
b.append(g(chai_glass(600,700,2.0,True,0,False,True),filt='roughS'))
hd=cr_path(HAND_L3)
b.append(g(f'<path d="{hd}" fill="url(#skin)" transform="translate(470,1360) rotate(-20) scale(2.6)"/>'+P("M300,1350 L560,1300 L620,1920 L260,1920 Z",'#6d6a62'),filt='roughS'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
