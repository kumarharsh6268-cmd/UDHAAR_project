import sys; sys.path.insert(0,'/home/claude/udhaar/scripts')
from art import *; from shapes import *
import random
random.seed(17)
# Top-down into the trunk: folded khaki uniform; the brass bell beneath at one corner
d=(BRASS_DEF+lg('khaki',[(0,'#a08a62'),(1,'#7a6646')],0,0,1,1)+rg('bulb',[(0,'#ffe2a6',0.55),(1,'#ffe2a6',0)],0.55,0.25,0.8))
b=[R(0,0,W,H,'#101615')]
b.append(g(R(60,120,960,1700,'#1c2a2a',1,'rx="10"')+R(90,150,900,1640,'#121b1b'),filt='rough'))
b.append(g(R(120,190,840,1560,'#2b2620',1,'rx="6"'),filt='rough'))
# bell peeking out lower-left corner from under shirt
b.append(g(bell(300,1420,1.25),filt='roughS'))
# folded uniform shirt (khaki) with collar, pocket, epaulette, buttons
sh=(P("M150,240 L930,260 L920,1360 C760,1400 540,1380 380,1330 L160,1300 Z",'url(#khaki)')
   +P("M360,240 L540,420 L720,250 L640,230 L540,330 L440,226 Z",'#6e5c3e')
   +P("M360,240 L270,360 L470,380 Z",'#a59068')+P("M720,250 L810,370 L610,388 Z",'#93805a')
   +R(560,420,8,900,'#5f4f35')+''.join(E(586,480+i*170,12,12,'#d8c9a0')+E(586,480+i*170,5,5,'#8a7650') for i in range(5))
   +R(640,560,200,170,'#8c7853',1,'rx="6"')+R(640,560,200,40,'#7d6a48')+E(740,590,9,9,'#d8c9a0')
   +R(150,300,200,60,'#8a7650',1,'transform="rotate(-8 250 330)"')+E(320,322,9,9,'#d8c9a0')
   +''.join(S(f"M{random.uniform(170,900)},{random.uniform(300,1300)} c{random.uniform(30,90)},{random.uniform(-10,10)} {random.uniform(60,160)},{random.uniform(-20,20)} {random.uniform(100,220)},{random.uniform(-10,10)}",'#6a5838',3,0.5) for _ in range(18)))
b.append(g(R(160,260,780,1110,'#0b0a08',0.5),filt='b16'))
b.append(g(sh,filt='roughS'))
# a sliver of RED cloth binding visible under the uniform's bottom edge (setup for reveal)
b.append(g(P("M520,1360 C600,1385 760,1395 900,1372 L905,1405 C760,1430 600,1420 515,1395 Z",'#b3161f'),filt='roughS'))
b.append(R(0,0,W,H,'url(#bulb)'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
