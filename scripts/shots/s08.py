import sys; sys.path.insert(0,'/home/claude/udhaar/scripts')
from art import *; from shapes import *; from manq import *
# Kabir's reaction: closer profile, looking DOWN at the kneeling old man (blurred foreground-left)
d=(lg('bg',[(0,'#8a9293'),(0.45,'#d3c5aa'),(0.62,'#efd9b0'),(1,'#5a544b')])+rg('sun',[(0,'#fff2da'),(1,'#efcd9a',0)])+lg('kg',[(0,'#5d5a53'),(0.5,'#3d3b37'),(1,'#2a2926')],0,0,1,0))
b=[R(0,0,W,H,'url(#bg)'),E(160,760,560,560,'url(#sun)',0.9)]
b.append(g(''.join(E(120+i*40,700-i*30,150,60,'#f4ead6',0.10) for i in range(8)),filt='smoke'))
# blurred old man kneeling bottom-left (foreground, out of focus)
P_=pose_old_kneel()
b.append(g(P("M-60,1700 C120,1640 380,1630 560,1660 L560,1920 L-60,1920 Z",'#e4dccb')+''.join(E(20+i*40,1668-(i%2)*8,16,13,'#d89a45') for i in range(14)),filt='b16'))
tf='translate(240,300) rotate(-10 560 700) scale(1.12)'
b.append(g(kabir_profile(fill='#f6d6a4',rim='#f6d6a4',rimw=0),tf=tf+' translate(-6,-2)',filt='b6',op=0.55))
b.append(g(kabir_profile(fill='#201914',rim='#f8dcac',rimw=7,hair='#0d0b0a')+kabir_kurta(),tf=tf,filt='roughS'))
rimd=kabir_front_rim()
b.append(g(f'<path d="{rimd}" fill="none" stroke="#fff0d0" stroke-width="4"/>',tf=tf,filt='roughS'))
# brow knit hint
b.append(g(S("M360,618 C372,612 386,612 396,618",'#f3d2a0',3,0.55),filt='b1'))

open(sys.argv[1],'w').write(svg(''.join(b),d))
