import sys; sys.path.insert(0,"/home/claude/udhaar/scripts")
from art import *; from shapes import *; from manq import *; from station import *
import random, math
random.seed(1)
# HOOK: Shankar's left hand wrapped around the chipped chai glass: thumb, index, middle only; healed stumps below
d=GLASS_DEF+lg('bg',[(0,'#8b8f88'),(0.5,'#e6d2aa'),(1,'#5c5246')])+rg('sun',[(0,'#fff3d8'),(1,'#f2cf9a',0)])+lg('skin',[(0,'#8a5c40'),(1,'#4a3020')],0,0,0,1)
b=[R(0,0,W,H,'url(#bg)'),E(760,560,620,620,'url(#sun)',0.9)]
b.append(g(''.join(R(560+i*90,0,40,1920,'#fff4dc',0.08,'transform="rotate(18 540 960)"') for i in range(5)),filt='b16'))
b.append(g(R(0,1430,W,500,'#3a2c20')+R(0,1430,W,26,'#5a4430'),filt='rough'))
gx,gy,gs=560,880,3.3
# palm behind the glass (left side), wrist + shawl sleeve from left edge
b.append(g(P("M-80,1100 C40,1060 200,1020 330,1000 C400,990 430,1060 420,1140 C410,1230 360,1300 280,1330 C180,1360 40,1380 -80,1400 Z",'url(#skin)')+P("M-80,1050 L120,1040 L150,1420 L-80,1450 Z",'#6d6a62'),filt='roughS'))
b.append(g(chai_glass(gx,gy,gs,True,0.72,True),filt='roughS'))
# thumb over the far side top-left
b.append(g(P(f"M360,1000 C420,960 470,940 500,950 C520,960 515,985 495,992 C460,1004 420,1020 390,1040 Z",'url(#skin)')+E(498,968,16,13,'#d8b394',0.8),filt='roughS'))
# index + middle fingers wrapping the front of the glass
for yy,ln in ((1080,330),(1172,318)):
    b.append(g(P(f"M380,{yy} C470,{yy-14} {380+ln},{yy-14} {390+ln},{yy+14} C{396+ln},{yy+44} {370+ln},{yy+58} {340+ln},{yy+54} C450,{yy+60} 400,{yy+66} 370,{yy+60} Z",'url(#skin)')
       +S(f"M{380+ln*0.45},{yy-6} C{384+ln*0.45},{yy+20} {384+ln*0.45},{yy+38} {378+ln*0.45},{yy+56}",'#3a2418',3,0.6)+S(f"M{380+ln*0.8},{yy-8} C{384+ln*0.8},{yy+18} {384+ln*0.8},{yy+36} {378+ln*0.8},{yy+54}",'#3a2418',2.5,0.5)
       +E(372+ln,yy+20,16,20,'#d8b394',0.7)+S(f"M392,{yy-4} C480,{yy-16} {380+ln*0.9},{yy-14} {386+ln},{yy+6}",'#f6d6a6',3,0.7),filt='roughS'))
# healed stumps where ring & little fingers should be
b.append(g(P("M360,1250 C400,1242 430,1250 440,1270 C444,1290 420,1300 392,1298 C372,1296 360,1284 360,1250 Z",'url(#skin)')+S("M420,1262 C430,1272 432,1284 424,1294",'#3a2418',2.5,0.7)
   +P("M340,1310 C372,1304 396,1312 402,1328 C404,1344 384,1350 362,1348 C346,1346 338,1334 340,1310 Z",'url(#skin)'),filt='roughS'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
