import sys; sys.path.insert(0,'/home/claude/udhaar/scripts')
from art import *; from shapes import *; from manq import hand
# The first page: a single line in Papa's hand
d=RED_DEF+PAGE_DEF+rg('bulb',[(0,'#ffe8b8',0.5),(1,'#ffe2a6',0)],0.5,0.4,0.7)
b=[R(0,0,W,H,'#17120f')]
b.append(g(R(90,250,900,1360,'url(#ledger)',1,'rx="16"')+R(90,250,900,1360,'url(#weave)',1,'rx="16"'),filt='rough'))
b.append(g(R(130,290,820,1280,'url(#pagec)'),filt='roughS'))
b.append(g(htext(540,900,'किसी से पैसे मत माँगना।',66,'#1f2142',-2,anchor='middle')+S("M300,940 C420,930 560,934 690,926",'#1f2142',2.5,0.35),filt='roughS'))
b.append(g(hand(140,1500,40,9,(1,1,1,1,1),'L',skin='#6b4632',hi='#a06e4c',lo='#3e281c')+hand(950,1500,-40,9,(1,1,1,1,1),'R',skin='#6b4632',hi='#a06e4c',lo='#3e281c'),filt='roughS'))
b.append(R(0,0,W,H,'url(#bulb)'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
