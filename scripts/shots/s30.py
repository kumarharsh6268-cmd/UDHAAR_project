import sys; sys.path.insert(0,'/home/claude/udhaar/scripts')
from art import *; from shapes import *
# Ma's face, half lit by the room bulb, at the door frame; eyes on the diary
d=('<linearGradient id="mskin" x1="1" y1="0" x2="0" y2="0"><stop offset="0.1" stop-color="#a87554"/><stop offset="0.55" stop-color="#6a4330"/><stop offset="1" stop-color="#2a1a12"/></linearGradient>'
   +lg('pal',[(0,'#d8d0bd'),(0.5,'#a49c89'),(1,'#4f4b43')],1,0,0,0)+lg('bg',[(0,'#e9b86e'),(1,'#5a4026')],0,0,1,0))
b=[R(0,0,W,H,'#14110f'),R(0,0,330,H,'url(#bg)')]
b.append(g(R(260,0,120,H,'#3a2a1e')+R(300,0,30,H,'#5a4430'),filt='rough'))
face=cr_path(mirror_x(MA_L)); pal=cr_path(mirror_x(MA_PALLU_L))
tf='translate(-60,300) scale(1.05) rotate(4 560 500)'
body=(f'<path d="{face}" fill="url(#mskin)"/>'+f'<path d="{pal}" fill="url(#pal)"/>'
 '<path d="M770,370 C756,360 738,360 724,370 C738,380 756,380 770,370 Z" fill="#e4d2ba"/><ellipse cx="760" cy="371" rx="7" ry="7" fill="#1a110c"/><circle cx="762" cy="368" r="2" fill="#fff"/>'
 '<path d="M778,360 C760,350 740,350 720,360" stroke="#2a1a12" stroke-width="4" fill="none"/>'
 '<path d="M786,336 C764,322 738,322 714,332" stroke="#3a2a20" stroke-width="7" fill="none" stroke-linecap="round"/>'
 '<path d="M790,330 C800,322 806,312 808,300" stroke="#2a1a12" stroke-width="3" fill="none" stroke-opacity="0.6"/>'
 '<path d="M770,395 C760,402 748,404 736,400" stroke="#5a3a28" stroke-width="2.5" fill="none" stroke-opacity="0.6"/>'
 '<path d="M796,528 C786,532 776,532 766,528" stroke="#4a2a1e" stroke-width="3.5" fill="none"/>'
 '<path d="M700,230 C680,250 660,280 650,320" stroke="#7a7266" stroke-width="10" fill="none" stroke-opacity="0.5"/>'
 '<path d="M660,250 C700,236 740,232 780,238" stroke="#3a3632" stroke-width="12" fill="none" stroke-opacity="0.55"/>')
b.append(g(body,tf=tf,filt='roughS'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
