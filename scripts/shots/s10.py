import sys, json; sys.path.insert(0,'/home/claude/udhaar/scripts')
from art import *; from shapes import *; from manq import hand
import random, math
random.seed(10)
d=(lg('table',[(0,'#5b4330'),(1,'#3a2a1e')])+rg('lamp',[(0,'#ffe3b0',0.65),(0.5,'#f2b866',0.18),(1,'#f2b866',0)],0.72,0.18,0.75)
   +lg('page',[(0,'#efe6d0'),(1,'#d9ccb0')],0,0,1,0)+lg('cover',[(0,'#355a5e'),(1,'#264346')]))
b=[R(0,0,W,H,'url(#table)')]
b.append(g(''.join(S(f"M0,{y} C300,{y+random.uniform(-20,20)} 700,{y+random.uniform(-20,20)} 1080,{y+random.uniform(-10,10)}",random.choice(['#4a3626','#614733','#3e2d20']),random.uniform(3,9),0.6) for y in range(0,1920,26)),filt='rough'))
# passbook open, slight angle
pb=g(R(-20,-10,760,1040,'url(#cover)',1,'rx="18"')+R(0,0,355,1020,'url(#page)')+R(365,0,355,1020,'url(#page)')+R(350,0,20,1020,'#bfb093'),tf='translate(170,420) rotate(-6 360 510)')
lines=''
for side in (0,365):
    for i in range(22):
        y=60+i*42; lines+=S(f"M{side+18},{y} L{side+340},{y}",'#9aa7a6',1.6,0.8)
    for x in (80,180,270): lines+=S(f"M{side+x},40 L{side+x},990",'#c49a8a',1.6,0.6)
    for i in range(14 if side==0 else 9):
        y=52+i*42
        for x0,w in ((22,50),(90,80),(190,70),(280,55)):
            if random.random()<0.85: lines+=S(f"M{side+x0},{y} c{w*0.2},-6 {w*0.4},4 {w*0.6},-3 s{w*0.3},5 {w*0.4},-2",'#3d4a5a',2.2,0.8)
# highlight last balance cell (right page, row 9)
cell=f'<rect x="{365+275}" y="{20+9*42}" width="62" height="36" fill="#fff6d8" fill-opacity="0.55"/>'
b.append(g(R(190,450,760,1040,'#1b130d',0.55,'rx="18"'),filt='b24'))
b.append(g(pb.replace('</g>',lines+cell+'</g>',1) if False else g(R(-20,-10,760,1040,'url(#cover)',1,'rx="18"')+R(0,0,355,1020,'url(#page)')+R(365,0,355,1020,'url(#page)')+R(350,0,20,1020,'#bfb093')+lines+cell,tf='translate(170,420) rotate(-6 360 510)'),filt='roughS'))
# Papa's reading glasses folded at top-left
b.append(g(E(160,300,70,46,'none',1,'stroke="#2a221b" stroke-width="7"')+E(300,312,70,46,'none',1,'stroke="#2a221b" stroke-width="7"')+S("M228,300 C236,290 246,290 252,302",'#2a221b',6)+S("M95,290 L40,250 M365,300 L420,262",'#2a221b',6)+E(160,300,62,38,'#e8d9b8',0.18)+E(300,312,62,38,'#e8d9b8',0.18),filt='roughS'))
# steel tumbler of chai
b.append(g(E(900,330,80,26,'#9aa0a0')+P("M820,330 L840,560 C860,580 940,580 960,560 L980,330 Z",'#8d9393')+E(900,330,72,22,'#6a4a2c')+S("M845,350 L860,550",'#d8dcdc',8,0.6),filt='roughS'))
# Kabir's finger pointing at the balance
b.append(g(hand(1040,1180,118,9,(1,1,0,0,0),'R',skin='#6b4632',hi='#a06e4c',lo='#3e281c'),filt='roughS'))
b.append(R(0,0,W,H,'url(#lamp)'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
