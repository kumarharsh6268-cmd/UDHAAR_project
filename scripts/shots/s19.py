import sys; sys.path.insert(0,'/home/claude/udhaar/scripts')
from art import *; from shapes import *; from manq import hand
import random
random.seed(19)
# Reveal: the uniform lifted away; at the bottom of the trunk, the red cloth ledger (the only saturated red)
d=(BRASS_DEF+RED_DEF+lg('khaki',[(0,'#a08a62'),(1,'#7a6646')],0,0,1,1)+rg('bulb',[(0,'#ffe2a6',0.5),(1,'#ffe2a6',0)],0.5,0.45,0.6))
b=[R(0,0,W,H,'#0f1514')]
b.append(g(R(60,120,960,1700,'#1c2a2a',1,'rx="10"')+R(90,150,900,1640,'#151d1d')+R(120,190,840,1560,'#241f1a',1,'rx="6"'),filt='rough'))
# a few other things: folded cloth bundle, the bell moved aside top-right
b.append(g(R(150,220,300,180,'#5d5a52',1,'rx="18"')+S("M160,300 L440,300",'#4a4841',5),filt='roughS'))
b.append(g(bell(800,330,1.0),filt='roughS'))
# the ledger, centred, slightly rotated
b.append(g(ledger_closed(560,1060,560,760,-4),filt='roughS'))
# uniform being lifted: edge of khaki at top, out of focus
b.append(g(P("M-40,-40 L1120,-40 L1120,170 C900,260 600,250 300,210 L-40,180 Z",'url(#khaki)')+S("M-40,178 C300,206 600,248 900,258",'#5f4f35',8,0.8),filt='b6'))
b.append(R(0,0,W,H,'url(#bulb)'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
