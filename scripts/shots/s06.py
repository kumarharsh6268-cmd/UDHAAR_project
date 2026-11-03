import sys; sys.path.insert(0,'/home/claude/udhaar/scripts')
from art import *; from shapes import *
import random, math
random.seed(6)
d=(rg('cloth',[(0,'#f6f1e6'),(0.7,'#e2dbcb'),(1,'#bdb5a4')],0.5,0.35,0.7)+rg('lightc',[(0,'#fff0d2',0.35),(1,'#fff0d2',0)],0.2,0.1,0.9)+lg('skin',[(0,'#6b4834'),(1,'#3b281e')],0,0,1,1))
b=[R(0,0,W,H,'#2f2922')]
b.append(g(''.join(E(random.uniform(0,W),random.uniform(0,H),random.uniform(20,80),random.uniform(4,10),'#4a4034',0.5) for _ in range(60)),filt='rough'))
# shroud over the feet: two mounds + cloth spreading down
sh=R(0,0,W,H,'url(#cloth)')+g(E(330,1060,300,330,'#fbf7ee',0.55)+E(760,1100,300,330,'#fbf7ee',0.55)+E(545,1150,40,500,'#a9a292',0.35),filt='b40')+''.join(S(f"M{x},{0} C{x+random.uniform(-60,60)},{700} {x+random.uniform(-80,80)},{1300} {x+random.uniform(-40,40)},1920",'#bdb5a4',random.uniform(4,10),0.35) for x in (90,200,420,650,880,1000))
cleft=S('M545,800 C548,1080 546,1400 542,1920','#a9a292',8,0.45)
tie=S('M-10,1420 C350,1470 720,1470 1090,1420','#8f8470',8,0.8)
mg=''
for i in range(34):
    t=i/33; x=-20+t*1120; y=1640+math.sin(t*math.pi)*70
    for k in range(9):
        a=k*0.7; mg+=E(x+math.cos(a)*9,y+math.sin(a)*9,10,8,random.choice(['#d99b3e','#c98734','#e2ad55']),0.95,f'transform="rotate({k*40} {x} {y})"')
mg+=''.join(E(random.uniform(90,990),random.uniform(1000,1900),7,5,random.choice(['#d99b3e','#c98734']),0.85,f'transform="rotate({random.uniform(0,180)} 540 960)"') for _ in range(40))
b.append(g(sh+cleft+tie+mg,filt='roughS'))
# hand shadows
b.append(g(E(380,900,190,260,'#3a2c20',0.22)+E(780,930,190,260,'#3a2c20',0.22),filt='b40'))
# hands (fingers down onto the feet). viewer-right = Shankar's LEFT hand: three fingers
def handg(pts,x,y,rot,sc):
    dd=cr_path(pts)
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({sc})">'
            f'<path d="{dd}" fill="#e9c08a" transform="translate(-2.5,-2)"/>'
            f'<path d="{dd}" fill="url(#skin)"/>'
            # knuckle creases + tendons + wrinkles
            '<path d="M-30,-110 C-20,-104 -8,-104 2,-108 M14,-110 C22,-104 32,-104 40,-108" stroke="#2a1b13" stroke-width="1.6" fill="none" stroke-opacity="0.7"/>'
            '<path d="M-14,-150 C-8,-147 -2,-147 4,-150 M-14,-170 C-8,-167 -2,-167 4,-170 M18,-145 C24,-142 30,-142 34,-145 M20,-160 C25,-158 30,-158 34,-160" stroke="#2a1b13" stroke-width="1.2" fill="none" stroke-opacity="0.6"/>'
            '<path d="M-20,-10 C-16,-50 -10,-80 -4,-104 M10,-10 C12,-50 18,-80 24,-104 M-34,-14 C-34,-50 -34,-80 -36,-100" stroke="#8a5e43" stroke-width="2" fill="none" stroke-opacity="0.55"/>'
            '<path d="M-38,-30 C-44,-50 -46,-70 -46,-90" stroke="#e7b987" stroke-width="2.2" fill="none" stroke-opacity="0.5"/>'
            '</g>')
b.append(g(handg(HAND_R5,330,330,176,3.1)+handg(HAND_L3,760,380,184,3.1),filt='roughS'))
# sleeves / shawl at top edge
b.append(g(P("M170,0 L500,0 L480,330 C420,372 250,372 190,330 Z",'#5f5a51')+P("M600,0 L930,0 L910,380 C850,422 680,422 620,380 Z",'#5f5a51')+S("M190,330 C250,372 420,372 480,330",'#3b3833',12)+S("M620,380 C680,422 850,422 910,380",'#3b3833',12)+S("M300,0 C310,120 312,220 306,340 M760,0 C770,140 772,260 766,390",'#4a463f',6,0.6),filt='rough'))
b.append(R(0,0,W,H,'url(#lightc)'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
