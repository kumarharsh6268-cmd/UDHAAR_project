import sys; sys.path.insert(0,'/home/claude/udhaar/scripts')
from art import *; from shapes import *; from manq import hand
# Decision: Kabir holds the red diary tight against his chest (faded blue shirt)
d=RED_DEF+lg('shirt',[(0,'#7f98ac'),(1,'#4f6678')],0,0,1,0)+rg('bulb',[(0,'#ffe2a6',0.4),(1,'#ffe2a6',0)],0.5,0.0,0.9)
b=[R(0,0,W,H,'url(#shirt)')]
b.append(g(S("M540,0 L540,1920",'#3e5262',6,0.6)+''.join(E(560,y,12,12,'#d9dcd8')+E(560,y,5,5,'#8a9096') for y in (200,520,1600))+S("M200,0 C240,600 220,1300 260,1920 M880,0 C840,600 870,1300 830,1920",'#46596a',10,0.5),filt='roughS'))
b.append(g(ledger_closed(540,1000,640,880,-6),filt='roughS'))
b.append(g(hand(250,1100,-70,11,(1,1,1,1,1),'L',skin='#6b4632',hi='#a06e4c',lo='#3e281c')+hand(830,820,110,11,(1,1,1,1,1),'R',skin='#6b4632',hi='#a06e4c',lo='#3e281c'),filt='roughS'))
b.append(R(0,0,W,H,'url(#bulb)'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
