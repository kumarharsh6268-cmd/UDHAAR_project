import sys; sys.path.insert(0,'/home/claude/udhaar/scripts')
from art import *; from shapes import *
import random
random.seed(27)
# The last page: the 47th name scratched out again and again until the paper tore
d=RED_DEF+PAGE_DEF+rg('bulb',[(0,'#ffe2a6',0.45),(1,'#ffe2a6',0)],0.5,0.3,0.8)
b=[R(0,0,W,H,'#15110e')]
b.append(g(R(90,200,900,1460,'url(#ledger)',1,'rx="16"'),filt='rough'))
b.append(g(R(130,240,820,1380,'url(#pagec)')+''.join(S(f"M160,{y} L920,{y}",'#9fb2b6',1.6,0.6) for y in range(320,1600,52)),filt='roughS'))
b.append(g(htext(170,330,'47.',54,'#26284a'),filt='roughS'))
sc=''
for i in range(90):
    x0=random.uniform(220,360); x1=random.uniform(700,900); y=random.uniform(560,700)
    sc+=S(f"M{x0},{y} C{(x0+x1)/2},{y+random.uniform(-40,40)} {(x0+x1)/2},{y+random.uniform(-40,40)} {x1},{y+random.uniform(-30,30)}",random.choice(['#14142a','#1c1a30','#2a1418']),random.uniform(3,8),0.75)
b.append(g(sc,filt='roughS'))
# tear in the middle of the scratched name
b.append(g(P("M470,600 L520,570 L560,610 L610,580 L640,630 L600,670 L620,700 L560,690 L520,720 L490,680 L450,660 Z",'#0b0807'),filt='roughS'))
b.append(g(S("M470,600 L520,570 L560,610 L610,580 L640,630",'#fff4dc',3,0.7),filt='b1'))
b.append(R(0,0,W,H,'url(#bulb)'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
