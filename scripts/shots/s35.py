import sys; sys.path.insert(0,'/home/claude/udhaar/scripts')
from art import *; from shapes import *; from manq import *
import random
random.seed(35)
# Dawn: Kabir steps out of the blue door into the lane, diary in hand; a municipal bus crosses the far end
d=RED_DEF+lg('sky',[(0,'#8c98a2'),(0.6,'#e2cfae'),(1,'#f0d9b0')])+lg('lane',[(0,'#7a746a'),(1,'#3a3732')])+lg('busg',[(0,'#6f8f99'),(1,'#4f6d76')])
b=[R(0,0,W,H,'url(#sky)')]
b.append(g(E(540,820,420,200,'#fff0d0',0.5),filt='b40'))
# lane walls receding
b.append(g(P("M0,0 L380,600 L380,1300 L0,1920 Z",'#5d5a52')+P("M1080,0 L700,600 L700,1300 L1080,1920 Z",'#544f48'),filt='rough'))
b.append(''.join(S(f"M{x},{y0} L{x2},{y1}",'#3a3732',3,0.6) for x,y0,x2,y1 in [(0,300,380,750),(0,800,380,1000),(1080,400,700,800),(1080,900,700,1050)]))
# bus at far end, crossing
b.append(g(R(330,1000,420,190,'url(#busg)',1,'rx="18"')+''.join(R(350+i*62,1020,48,60,'#d8dcd0',0.85) for i in range(6))+R(330,1120,420,12,'#c9b48a')+E(400,1192,24,24,'#1f1f1f')+E(680,1192,24,24,'#1f1f1f'),filt='b3'))
b.append(P("M380,1300 L700,1300 L1080,1920 L0,1920 Z",'url(#lane)'))
b.append(g(R(380,1200,320,100,'#e8d2a8',0.4),filt='b16'))
# door frame (blue) foreground left
b.append(g(R(-40,0,240,1920,'#2a2018')+R(-40,0,200,1920,'#4a6964'),filt='rough'))
# Kabir walking away down the lane (back view), blue shirt, red diary in right hand
P_=pose_stand_side()
P_['ankleR']=(12,-6); P_['toeR']=(8,-2); P_['ankleL']=(-10,-2)
b.append(g(f'<path d="{shape("boy")}" fill="#46607a" transform="translate(560,1700) scale(6.2)"/>'+f'<path d="M-6.2,-92.5 C-6.5,-101 6.5,-101 6.2,-92.5 L6,-86 L-6,-86 Z" fill="#141010" transform="translate(560,1700) scale(6.2)"/>',filt='roughS'))
b.append(g(R(630,1430,46,64,'url(#ledger)',1,'rx="4"'),filt='roughS'))
b.append(g(E(560,1704,90,14,'#1b1915',0.5),filt='b6'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
