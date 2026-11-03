import sys; sys.path.insert(0,'/home/claude/udhaar/scripts')
from art import *; from shapes import *
import random
random.seed(13)
# Kabir's hands holding the bank notice (blue shirt cuffs). Overlay text added in edit.
d=(lg('bg',[(0,'#6b6f68'),(1,'#3d403b')])+lg('paper',[(0,'#f4f1e8'),(1,'#dcd6c8')],0,0,1,1)+rg('light',[(0,'#fff2d8',0.35),(1,'#fff2d8',0)],0.3,0.2,0.9)+lg('skin',[(0,'#8a5c40'),(1,'#5e3d2b')],0,0,1,0))
b=[R(0,0,W,H,'url(#bg)')]
b.append(g(R(0,1300,W,620,'#2e302c',0.6),filt='b40'))
# paper with folds
pp=P("M150,300 L930,330 L910,1420 L170,1390 Z",'url(#paper)')
fold=S("M160,845 L920,875",'#c9c3b4',4,0.8)+S("M160,850 L920,880",'#ffffff',2,0.6)
txt=R(220,380,640,46,'#1f2a3a',0.9,'transform="rotate(2 540 400)"')+''.join(R(220,460+i*34,600-(i%4)*70,9,'#4a5160',0.65,f'transform="rotate(2 540 {460+i*34})"') for i in range(10))+''.join(R(220,920+i*34,560-(i%3)*90,9,'#4a5160',0.6,f'transform="rotate(2 540 {920+i*34})"') for i in range(8))
stamp=E(740,1250,80,56,'none',1,'stroke="#5a4a72" stroke-width="5" stroke-opacity="0.5"')+S("M300,1260 c20,-30 40,20 60,-10 s30,10 50,-6",'#2a3050',3,0.7)
b.append(g(R(170,330,780,1110,'#15140f',0.45),filt='b16'))
b.append(g(pp+fold+txt+stamp,filt='roughS'))
# hands gripping edges (thumbs on front), shirt cuffs faded blue
def thumbhand(x,y,flip):
    s=-1 if flip else 1
    return (f'<g transform="translate({x},{y}) scale({s},1)">'
            f'<path d="M-40,140 C-60,60 -50,-10 -20,-40 C0,-60 30,-58 40,-30 C50,0 46,60 40,140 Z" fill="url(#skin)"/>'
            f'<path d="M10,-30 C30,-70 60,-90 84,-86 C100,-82 104,-66 92,-56 C70,-40 46,-20 30,10 Z" fill="#9a6a4a"/>'
            f'<ellipse cx="88" cy="-74" rx="12" ry="9" fill="#d8b89a" fill-opacity="0.8"/>'
            f'<path d="M-60,140 L60,140 L70,380 L-80,380 Z" fill="#6f8aa0"/><path d="M-60,140 L60,140 L62,170 L-62,170 Z" fill="#5a7488"/>'
            f'<path d="M-30,-10 C-20,-20 0,-24 20,-20" stroke="#4a2f20" stroke-width="3" fill="none" stroke-opacity="0.6"/></g>')
b.append(g(thumbhand(140,1060,False)+thumbhand(950,1040,True),filt='roughS'))
b.append(R(0,0,W,H,'url(#light)'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
