import sys; sys.path.insert(0,'/home/claude/udhaar/scripts')
from art import *; from shapes import *
# End card on red cloth (the ledger cover)
d=RED_DEF+rg('vig',[(0,'#000',0),(1,'#000',0.6)])
b=[R(0,0,W,H,'url(#ledger)'),R(0,0,W,H,'url(#weave)'),R(0,0,W,H,'url(#vig)')]
b.append(g(R(0,0,W,H,'#000',0.15),filt='wash'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
