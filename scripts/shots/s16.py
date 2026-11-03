import sys; sys.path.insert(0,'/home/claude/udhaar/scripts')
from art import *; from shapes import *; from manq import hand
import random, math
random.seed(16)
# Night: tin trunk pulled out from under the cot, lid lifting; single bulb
d=(lg('wall',[(0,'#4e5a51'),(1,'#2c332e')])+rg('bulb',[(0,'#ffe2a6',0.9),(0.25,'#f3b45e',0.35),(1,'#f3b45e',0)],0.5,0.0,0.9)
   +lg('floor',[(0,'#5c5a53'),(1,'#232220')])+lg('tin',[(0,'#3f5b5c'),(1,'#263a3b')],0,0,1,0)+lg('lid',[(0,'#5d7b7a'),(1,'#36504f')]))
b=[R(0,0,W,H,'url(#wall)')]
SHADOW_AT=1
b.append(P("M0,1050 L1080,1050 L1080,1920 L0,1920 Z",'url(#floor)'))
b.append(g(''.join(E(random.uniform(0,W),random.uniform(1060,1920),random.uniform(3,7),random.uniform(2,4),random.choice(['#77756d','#4a4842','#8d8b82']),0.6) for _ in range(500)),filt='roughS'))
# cot (charpai/iron bed) behind
b.append(g(R(0,820,1080,40,'#2a2420')+R(40,860,20,200,'#221d1a')+R(1010,860,20,200,'#221d1a')+R(0,780,1080,46,'#7a6e60')+P("M0,780 C300,760 700,770 1080,776 L1080,800 L0,806 Z",'#9a8e7c'),filt='rough'))
b.append(g(R(0,860,1080,200,'#0e0d0c',0.7),filt='b24'))
# Kabir's big soft shadow on the wall, bending over the trunk (cast by the bulb)
import manq
P_=manq.pose_old_kneel()
b.append(g(f'<g transform="translate(720,1060) scale(13,11)">{manq.body2(P_,"#141816")}</g>',filt='b16',op=0.55))
# bulb hanging
b.append(S("M540,0 L540,150",'#1b1a18',4))
b.append(g(E(540,175,26,34,'#fff4d6')+R(526,140,28,22,'#5a5046'),filt='roughS'))
b.append(E(540,175,900,900,'url(#bulb)'))
# trunk: front face, side, lid open ~70deg
fx,fy,fw,fh=200,1220,620,330
front=P(f"M{fx},{fy} L{fx+fw},{fy} L{fx+fw},{fy+fh} L{fx},{fy+fh} Z",'url(#tin)')
side=P(f"M{fx+fw},{fy} L{fx+fw+150},{fy-90} L{fx+fw+150},{fy+fh-90} L{fx+fw},{fy+fh} Z",'#1f3031')
inside=P(f"M{fx},{fy} L{fx+150},{fy-90} L{fx+fw+150},{fy-90} L{fx+fw},{fy} Z",'#0f1414')
lid=P(f"M{fx+150},{fy-90} L{fx+fw+150},{fy-90} L{fx+fw+120},{fy-430} L{fx+120},{fy-430} Z",'url(#lid)')
lidin=P(f"M{fx+165},{fy-100} L{fx+fw+138},{fy-100} L{fx+fw+112},{fy-410} L{fx+132},{fy-410} Z",'#2c3f3f')
rust=''.join(E(fx+random.uniform(0,fw),fy+random.uniform(0,fh),random.uniform(6,24),random.uniform(4,14),'#7a4a2a',0.5) for _ in range(26))
bands=''.join(R(fx,fy+t,fw,10,'#2e4546') for t in (40,fh-50))+R(fx+fw/2-30,fy-6,60,70,'#a8843e')+R(fx+fw/2-12,fy+40,24,26,'#6e5426')
handle=S(f"M{fx+fw+40},{fy+90} C{fx+fw+70},{fy+70} {fx+fw+100},{fy+60} {fx+fw+120},{fy+40}",'#1a2526',10)
glow=g(P(f"M{fx+150},{fy-90} L{fx+fw+150},{fy-90} L{fx+fw},{fy} L{fx},{fy} Z",'#f0b860',0.10),filt='b8')
b.append(g(E(fx+fw/2+60,fy+fh+20,420,50,'#0a0908',0.6),filt='b16'))
b.append(g(side+front+rust+bands+handle+inside+lidin+lid+glow,filt='rough'))
b.append(g(S(f"M{fx+120},{fy-430} L{fx+fw+120},{fy-430}",'#a9c2bc',4,0.6)+S(f"M{fx},{fy} L{fx+fw},{fy}",'#9fb8b2',3,0.5),filt='roughS'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
