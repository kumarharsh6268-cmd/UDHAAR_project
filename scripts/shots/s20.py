import sys; sys.path.insert(0,'/home/claude/udhaar/scripts')
from art import *; from shapes import *; from manq import hand
import random
random.seed(20)
# Open ledger spread: one name per page, amount and year; Kabir's finger tracing
d=RED_DEF+PAGE_DEF+rg('bulb',[(0,'#ffe2a6',0.45),(1,'#ffe2a6',0)],0.6,0.3,0.8)
b=[R(0,0,W,H,'#1a1513')]
b.append(g(R(30,230,1020,1420,'url(#ledger)',1,'rx="16"')+R(30,230,1020,1420,'url(#weave)',1,'rx="16"'),filt='rough'))
def scribble(x,y,w):
    return S(f"M{x},{y} c{w*0.15},-8 {w*0.3},6 {w*0.45},-3 s{w*0.3},7 {w*0.55},-1",'#3a3c5a',2.4,0.75)
L=[htext(110,170,'तारा',62),htext(110,250,'₹ 40,000',46),htext(330,250,'2011',40),scribble(110,320,330),scribble(110,372,280),scribble(110,424,300)]
Rr=[htext(110,170,'दीपक - दिलीप',58),htext(110,250,'₹ 60,000',46),htext(350,250,'2012',40),scribble(110,320,320),scribble(110,372,340)]
b.append(g(ledger_page(70,280,465,1320,L,0)+ledger_page(545,280,465,1320,Rr,0)+R(530,280,22,1320,'#bba98a'),filt='roughS'))
b.append(g(R(530,280,22,1320,'#7a6a52',0.5),filt='b6'))
# Kabir's finger tracing the right page amount (from bottom right)
b.append(g(hand(900,1250,150,10,(1,1,0,0,0),'R',skin='#6b4632',hi='#a06e4c',lo='#3e281c')+P("M960,1340 L1120,1300 L1120,1700 L1000,1720 Z",'#6f8aa0'),filt='roughS'))
b.append(R(0,0,W,H,'url(#bulb)'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
