import sys; sys.path.insert(0,'/home/claude/udhaar/scripts')
from art import *; from shapes import *; from manq import hand
import random
random.seed(21)
# Totalling on the BACK of the bank notice with a pencil
d=lg('paper',[(0,'#efece2'),(1,'#d7d1c2')],0,0,1,1)+rg('bulb',[(0,'#ffe2a6',0.45),(1,'#ffe2a6',0)],0.4,0.2,0.9)
b=[R(0,0,W,H,'#2a2420')]
b.append(g(R(110,160,860,1560,'url(#paper)',1,'transform="rotate(-3 540 940)"'),filt='roughS'))
# faint show-through of print from the front (mirrored blocks)
b.append(g(''.join(R(220,260+i*30,560-(i%4)*60,8,'#8a8f9a',0.18,'transform="rotate(-3 540 940)"') for i in range(14)),filt='b2'))
amts=['6,000','14,000','25,000','40,000','1,20,000','30,000','50,000','35,000','60,000','45,000','70,000','20,000','80,000','2,00,000']
t=[]
for i,a in enumerate(amts): t.append(htext(720,330+i*62,a,44,'#3d3d3d',-3,anchor='end',op=0.85))
t.append(htext(560,330+len(amts)*62+10,'. . .',44,'#3d3d3d',-3,op=0.7))
y=330+len(amts)*62+80
t.append(S(f"M330,{y} L760,{y-22}",'#3d3d3d',3,0.85))
t.append(htext(740,y+80,'38,40,000',78,'#262626',-3,anchor='end',weight=700))
t.append(S(f"M330,{y+100} L770,{y+78}",'#3d3d3d',3,0.85)+S(f"M330,{y+112} L770,{y+90}",'#3d3d3d',3,0.85))
t.append(htext(300,y+80,'=',70,'#262626',-3))
b.append(g(''.join(t)))
# pencil + hand bottom right
b.append(g(P("M760,1600 L1040,1180 L1064,1196 L790,1620 Z",'#d9a63a')+P("M760,1600 L790,1620 L768,1646 Z",'#e8cfa0')+P("M768,1646 L772,1632 L778,1638 Z",'#333')+P("M1040,1180 L1064,1196 L1080,1170 L1056,1154 Z",'#c07a7a'),filt='roughS'))
b.append(g(hand(900,1460,220,9.5,(1,1,1,1,1),'R',skin='#6b4632',hi='#a06e4c',lo='#3e281c')+P("M960,1420 L1120,1300 L1120,1920 L1000,1920 Z",'#6f8aa0'),filt='roughS'))
b.append(R(0,0,W,H,'url(#bulb)'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
