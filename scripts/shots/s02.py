import sys; sys.path.insert(0,'/home/claude/udhaar/scripts')
from art import *; from shapes import *
import random, math
random.seed(2)
d=(lg('bg',[(0,'#7d878b'),(0.35,'#b8b2a2'),(0.55,'#ead5ae'),(0.75,'#cdbfa5'),(1,'#5e584f')])
   +lg('kg',[(0,'#5d5a53'),(0.5,'#3d3b37'),(1,'#2a2926')],0,0,1,0)+rg('sun',[(0,'#fff3dc',1),(0.2,'#f7dcae',0.7),(1,'#e9c492',0)]))
b=[R(0,0,W,H,'url(#bg)'),E(250,980,520,520,'url(#sun)')]
# defocused mourners behind
bk=''.join(f'<path d="{shape(n)}" fill="#3a3834" transform="translate({x},{y}) scale({h/100})"/>' for x,y,h,n in [(80,1500,640,'womanc'),(330,1260,420,'manc'),(520,1210,330,'womanc'),(170,1180,300,'manc')])
b.append(g(bk,filt='b16',op=0.85))
b.append(g(R(0,1180,W,800,'#2a2622',0.5),filt='b24'))
# smoke drift
b.append(g(''.join(E(200+i*40,700-i*30,140,60,'#f4ead6',0.10) for i in range(8)),filt='smoke'))
# Kabir profile big, right side
b.append(g(kabir_profile(fill='#f6d6a4',rim='#f6d6a4',rimw=0),tf='translate(238,318) scale(1.06)',filt='b6',op=0.55))
b.append(g(kabir_profile(fill='#1f1814',rim='#f8dcac',rimw=7,hair='#0d0b0a')+kabir_kurta(),tf='translate(245,320) scale(1.06)',filt='roughS'))
# white kurta collar hint at bottom (in shadow)
rimd=kabir_front_rim()
b.append(g(f'<path d="{rimd}" fill="none" stroke="#ffe4b4" stroke-width="16" stroke-opacity="0.55"/>',tf='translate(239,318) scale(1.06)',filt='b8'))
b.append(g(f'<path d="{rimd}" fill="none" stroke="#fff0d0" stroke-width="4.5"/>',tf='translate(239,318) scale(1.06)',filt='roughS'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
