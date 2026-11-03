import sys; sys.path.insert(0,'/home/claude/udhaar/scripts')
from art import *; from shapes import *; from papa_face import papa_face
import random, math
random.seed(9)
# Papa's garlanded portrait on the wall. Photo is sepia; frame wood; marigold garland; diya below.
d=(lg('wall',[(0,'#7d8a80'),(0.5,'#93a094'),(1,'#5f6a62')])
   +rg('win',[(0,'#fff2d6',0.55),(1,'#fff2d6',0)],0.85,0.2,0.7)
   +lg('photo',[(0,'#a48a6a'),(1,'#7d654a')])
   +rg('face',[(0,'#c9ab86'),(0.6,'#a98a68'),(1,'#7a5f45')],0.42,0.42,0.6)
   +lg('shirt',[(0,'#8d7a5c'),(1,'#6d5c43')],0,0,1,0)
   +rg('glass',[(0,'#ffffff',0.0),(1,'#ffffff',0)])
   +rg('diya',[(0,'#ffe2a8',0.9),(0.3,'#f7b45a',0.4),(1,'#f7b45a',0)]))
b=[R(0,0,W,H,'url(#wall)')]
b.append(g(''.join(E(random.uniform(0,W),random.uniform(0,H),random.uniform(60,220),random.uniform(40,160),random.choice(['#7a877d','#8e9b8f','#6d7a70']),0.35) for _ in range(40)),filt='roughL'))
b.append(R(0,0,W,H,'url(#win)'))
# frame
FX,FY,FW,FH=150,250,780,1000
b.append(g(R(FX+18,FY+26,FW,FH,'#2b2620',0.5),filt='b16'))
b.append(g(R(FX,FY,FW,FH,'#4a3424')+R(FX+14,FY+14,FW-28,FH-28,'#5c4330')+R(FX+40,FY+40,FW-80,FH-80,'#e8dcc2'),filt='rough'))
PX,PY,PW,PH=FX+70,FY+70,FW-140,FH-140
ph=[R(PX,PY,PW,PH,'url(#photo)')]
cx=PX+PW/2
# shoulders / khaki uniform with collar and epaulettes
ph.append(P(f"M{PX-10},{PY+PH} L{PX-10},{PY+PH-130} C{PX+40},{PY+PH-200} {cx-110},{PY+PH-235} {cx-60},{PY+PH-250} L{cx+60},{PY+PH-250} C{cx+110},{PY+PH-235} {PX+PW-40},{PY+PH-200} {PX+PW+10},{PY+PH-130} L{PX+PW+10},{PY+PH} Z",'url(#shirt)'))
ph.append(P(f"M{cx-62},{PY+PH-252} L{cx},{PY+PH-150} L{cx+62},{PY+PH-252} L{cx+30},{PY+PH-262} L{cx},{PY+PH-200} L{cx-30},{PY+PH-262} Z",'#5a4a35'))
ph.append(P(f"M{cx-64},{PY+PH-252} L{cx-120},{PY+PH-196} L{cx-30},{PY+PH-180} Z",'#97845f')+P(f"M{cx+64},{PY+PH-252} L{cx+120},{PY+PH-196} L{cx+30},{PY+PH-180} Z",'#86734f'))
ph.append(R(PX+18,PY+PH-215,110,22,'#7a6849',1,f'rx="5" transform="rotate(14 {PX+70} {PY+PH-205})"')+R(PX+PW-128,PY+PH-215,110,22,'#6e5d41',1,f'rx="5" transform="rotate(-14 {PX+PW-70} {PY+PH-205})"'))
ph.append(S(f"M{cx},{PY+PH-150} L{cx},{PY+PH}",'#5a4a35',3)+''.join(E(cx+6,PY+PH-120+i*55,5,5,'#c9b48c') for i in range(3)))
ph.append(R(cx+70,PY+PH-120,70,52,'#7a6849',1,'rx="4"'))  # pocket
# neck
ph.append(P(f"M{cx-42},{PY+PH-330} L{cx-48},{PY+PH-240} C{cx-20},{PY+PH-215} {cx+20},{PY+PH-215} {cx+48},{PY+PH-240} L{cx+42},{PY+PH-330} Z",'#9c7e5e'))
ph.append(P(f"M{cx-46},{PY+PH-270} C{cx-20},{PY+PH-250} {cx+20},{PY+PH-250} {cx+46},{PY+PH-270} L{cx+48},{PY+PH-240} C{cx+20},{PY+PH-218} {cx-20},{PY+PH-218} {cx-48},{PY+PH-240} Z",'#836648'))
hy=PY+330
ph.append(f'<g transform="translate({cx},{hy}) scale(1.22)">'+papa_face()+'</g>')
# studio vignette inside photo, sepia fade
ph.append(R(PX,PY,PW,PH,'url(#glass)'))
b.append(g(g(''.join(ph),filt='b2'),extra=f'clip-path="url(#pc)"'))
# glass glare streak
b.append(g(P(f"M{FX+90},{FY+60} L{FX+190},{FY+60} L{FX+70},{FY+FH-60} L{FX+40},{FY+FH-60} Z",'#ffffff',0.07),filt='b8'))
# chandan tilak on glass (forehead)
b.append(g(E(cx,hy-75,8,13,'#e9b77a',0.85)+E(cx,hy-75,3.5,6,'#d9853e',0.85),filt='roughS'))
# marigold garland draped across frame
gar=''
for i in range(70):
    t=i/69; x=FX+20+t*(FW-40); y=FY+FH-360+ (math.sin(t*math.pi))*380
    for k in range(6):
        a=k*1.05+i; gar+=E(x+math.cos(a)*10,y+math.sin(a)*10,12,10,random.choice(['#dd9a3c','#cf8932','#e6ab4f','#c27a2c']),0.97,f'transform="rotate({k*30+i*7} {x} {y})"')
b.append(g(E(FX+FW/2,FY+FH+20,300,40,'#2a2620',0.35),filt='b16'))
b.append(g(gar,filt='roughS'))
# shelf + diya below
b.append(g(R(100,1520,880,34,'#3d2f23')+R(110,1552,860,14,'#2a2119'),filt='rough'))
b.append(E(540,1420,320,320,'url(#diya)'))
b.append(g(P("M500,1520 C505,1495 575,1495 580,1520 Z",'#8a5a36')+E(540,1496,10,22,'#ffd98a')+E(540,1502,5,10,'#fff4d6'),filt='roughS'))
b.append(g(E(540,1400,90,60,'#ffd08a',0.18),filt='b24'))
clip=f'<clipPath id="pc"><rect x="{PX}" y="{PY}" width="{PW}" height="{PH}"/></clipPath>'
open(sys.argv[1],'w').write(svg(''.join(b),d+clip))
