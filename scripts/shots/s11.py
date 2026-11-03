import sys; sys.path.insert(0,'/home/claude/udhaar/scripts')
from art import *; from shapes import *; from manq import *
import random, math
random.seed(11)
# Low camera: Papa's worn chappals in foreground; Kabir sits on the threshold, backlit by morning, head down
d=(lg('wall',[(0,'#5d6a62'),(1,'#46514a')])+lg('door',[(0,'#fff3d8'),(1,'#f1dcae')])+lg('floor',[(0,'#6e6c65'),(1,'#33312d')])+rg('spill',[(0,'#fde9c2',0.55),(1,'#fde9c2',0)],0.5,0.0,0.8))
b=[R(0,0,W,H,'url(#wall)')]
b.append(g(''.join(E(random.uniform(0,W),random.uniform(0,1200),random.uniform(60,200),random.uniform(40,150),random.choice(['#58655d','#68756c','#4f5a53']),0.35) for _ in range(30)),filt='roughL'))
# doorway centre, bright; lane beyond hinted
b.append(R(250,140,580,1090,'#2f241a'))
b.append(R(280,170,520,1060,'url(#door)'))
b.append(g(R(280,820,520,410,'#e4cfa4',0.6)+R(600,300,30,600,'#d9c49a',0.5)+P("M280,700 L800,640 L800,700 L280,760 Z",'#e8d6b0',0.4),filt='b8'))
# Kabir sitting on threshold, backlit silhouette, head bowed (facing right)
P_=pose_sit_floor()
P_=flipP(P_)
b.append(g(f'<g transform="translate(476,1248) scale(7.4)">{body2(P_,"#f7e0b4")}</g>',filt='b3'))
b.append(g(f'<g transform="translate(480,1250) scale(7.4)">{body2(P_,"#1e1c1a")}</g>',filt='roughS'))
# threshold step
b.append(g(R(230,1228,620,30,'#5d4d3d')+R(230,1256,620,12,'#2c241d'),filt='rough'))
# floor
b.append(P("M0,1268 L1080,1268 L1080,1920 L0,1920 Z",'url(#floor)'))
b.append(g(''.join(E(random.uniform(0,W),random.uniform(1280,1920),random.uniform(3,8),random.uniform(2,5),random.choice(['#85837a','#55534c','#9e9c93']),0.6) for _ in range(500)),filt='roughS'))
b.append(g(P('M280,1268 L800,1268 L1080,1920 L0,1920 Z','#fde9c2',0.30),filt='b24'))
# chappals, foreground, large
def chappal(x,y,rot,flip=1,sc=1.9):
    sole=P("M-38,-120 C-48,-60 -46,40 -34,110 C-24,140 24,140 34,110 C46,40 48,-60 38,-120 C30,-150 -30,-150 -38,-120 Z",'#2e2a26')
    top=P("M-32,-114 C-42,-58 -40,38 -29,104 C-20,128 20,128 29,104 C40,38 42,-58 32,-114 C25,-140 -25,-140 -32,-114 Z",'#8b8578')
    wear=E(0,60,18,30,'#6a655a',0.9)+E(0,-80,16,22,'#6a655a',0.8)+E(-6,-20,8,30,'#7a7468',0.6)
    strap=P("M-40,-20 C-30,-80 -6,-104 0,-104 C6,-104 30,-80 40,-20 L28,-20 C20,-66 6,-86 0,-86 C-6,-86 -20,-66 -28,-20 Z",'#55707f')
    return f'<g transform="translate({x},{y}) rotate({rot}) scale({flip*sc},{sc*0.62})">{sole}{top}{wear}{strap}<circle cx="0" cy="-100" r="6" fill="#43596a"/></g>'
b.append(g(E(540,1760,330,70,'#141210',0.55),filt='b16'))
b.append(g(chappal(420,1700,-8)+chappal(670,1720,10,-1),filt='roughS'))
b.append(g(S("M330,1640 C360,1620 400,1612 430,1616",'#f6dfb2',4,0.5)+S("M600,1650 C630,1630 680,1624 710,1630",'#f6dfb2',4,0.5),filt='b2'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
