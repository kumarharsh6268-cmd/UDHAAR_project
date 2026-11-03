import sys; sys.path.insert(0,'/home/claude/udhaar/scripts')
from art import *; from shapes import *
d=(lg('bg',[(0,'#87908f'),(0.4,'#cbbfa6'),(0.62,'#ecd7ae'),(1,'#5f594f')])+rg('sun',[(0,'#fff3da'),(1,'#f0cf9e',0)])+'<linearGradient id="mskin" x1="1" y1="0" x2="0" y2="0"><stop offset="0.05" stop-color="#9a6a4c"/><stop offset="0.5" stop-color="#5a3828"/><stop offset="1" stop-color="#2a1a12"/></linearGradient>'+lg('pal',[(0,'#6d6a62'),(0.6,'#8b877d'),(1,'#b9b3a5')],1,0,0,0))
b=[R(0,0,W,H,'url(#bg)'),E(980,820,600,600,'url(#sun)',0.85)]
bk=''.join(f'<path d="{shape(n)}" fill="#3f3b35" transform="translate({x},{y}) scale({h/100})"/>' for x,y,h,n in [(860,1330,380,'manc'),(1030,1420,500,'womanc'),(700,1240,280,'womanc')])
b.append(g(bk,filt='b16',op=0.75))
face=cr_path(mirror_x(MA_L)); pal=cr_path(mirror_x(MA_PALLU_L))
tf='translate(-170,360) scale(1.02) rotate(6 560 500)'
body=(f'<path d="{face}" fill="#fbe3b6" transform="translate(7,-3)"/>'
      f'<path d="{face}" fill="url(#mskin)"/>'
      f'<path d="{pal}" fill="#f4e4c4" transform="translate(6,-4)"/>'
      f'<path d="{pal}" fill="url(#pal)"/>'
      # downcast eye + faint warm fill on cheek

      '<path d="M786,336 C764,324 738,324 716,332" stroke="#3a2418" stroke-width="5" fill="none" stroke-linecap="round" stroke-opacity="0.8"/>'
      '<path d="M772,372 C760,378 744,378 732,372" stroke="#2a1a12" stroke-width="3.5" fill="none"/>'
      '<path d="M770,395 C760,402 748,404 736,400" stroke="#3a2418" stroke-width="2.5" fill="none" stroke-opacity="0.5"/>'
      '<path d="M796,528 C786,532 776,532 766,528" stroke="#3a2418" stroke-width="3.5" fill="none"/>')
b.append(g(body,tf=tf,filt='roughS'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
