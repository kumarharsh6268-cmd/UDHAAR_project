import sys; sys.path.insert(0,"/home/claude/udhaar/scripts")
from art import *; from shapes import *; from manq import *; from station import *
import random, math
random.seed(17)
# Shankar's LEFT hand resting on the counter beside the glass: thumb, index, middle; healed stumps where two fingers were
d=GLASS_DEF+lg('wood',[(0,'#6a4f38'),(1,'#3a2a1e')])+lg('skin',[(0,'#9a6a4c'),(1,'#4a3020')],0,0,1,1)+rg('sun',[(0,'#fff0cc',0.5),(1,'#fff0cc',0)],0.3,0.2,0.8)
b=[R(0,0,W,H,'url(#wood)')]
b.append(g(''.join(S(f"M0,{y} C300,{y+random.uniform(-14,14)} 700,{y+random.uniform(-14,14)} 1080,{y}",'#4a3626',6,0.6) for y in range(0,1920,44)),filt='rough'))
b.append(g(E(820,620,140,40,'#1a130d',0.45),filt='b8'))
b.append(g(chai_glass(820,360,1.7,True,0.7,True),filt='roughS'))
hd=cr_path(HAND_L3)
b.append(g(f'<path d="{hd}" fill="#1a130d" fill-opacity="0.45" transform="translate(480,1700) rotate(14) scale(4.2)" filter="url(#b16)"/>'))
b.append(g(f'<path d="{hd}" fill="url(#skin)" transform="translate(450,1660) rotate(14) scale(4.2)"/>'
  +'<g transform="translate(450,1660) rotate(14) scale(4.2)"><path d="M-10,-112 C-4,-108 4,-108 10,-112 M14,-114 C20,-110 28,-110 36,-114 M-8,-150 C-2,-147 4,-147 8,-150 M18,-145 C24,-142 30,-142 34,-145" stroke="#2a1b13" stroke-width="1.4" fill="none" stroke-opacity="0.7"/>'
  +'<path d="M-44,-104 C-40,-100 -36,-100 -32,-104 M-28,-110 C-22,-106 -16,-106 -12,-110" stroke="#2a1b13" stroke-width="1.2" fill="none" stroke-opacity="0.7"/>'
  +'<ellipse cx="-2" cy="-182" rx="5" ry="6" fill="#d8b89a" fill-opacity="0.8"/><ellipse cx="28" cy="-170" rx="5" ry="6" fill="#d8b89a" fill-opacity="0.8"/><ellipse cx="94" cy="-124" rx="5" ry="5" fill="#d8b89a" fill-opacity="0.8"/>'
  +'<path d="M-20,-10 C-16,-50 -10,-80 -4,-104 M10,-10 C12,-50 18,-80 24,-104" stroke="#b07a56" stroke-width="2" fill="none" stroke-opacity="0.5"/></g>'
  +P("M150,1620 L560,1560 L640,1920 L120,1920 Z",'#6d6a62'),filt='roughS'))
b.append(R(0,0,W,H,'url(#sun)'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
