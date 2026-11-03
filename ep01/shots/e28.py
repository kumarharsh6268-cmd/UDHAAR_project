import sys; sys.path.insert(0,"/home/claude/udhaar/scripts")
from art import *; from shapes import *; from manq import *; from station import *
import random, math
# Vote card background: red ledger cloth
d=RED_DEF+rg('vig',[(0,'#000',0),(1,'#000',0.62)])
b=[R(0,0,W,H,'url(#ledger)'),R(0,0,W,H,'url(#weave)'),R(0,0,W,H,'url(#vig)')]
open(sys.argv[1],'w').write(svg(''.join(b),d))
