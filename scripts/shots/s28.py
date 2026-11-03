import sys; sys.path.insert(0,'/home/claude/udhaar/scripts')
from art import *; from shapes import *
import random, math
random.seed(28)
# Macro: the torn hole, bulb light glowing through it from behind; ink gouges around
d=PAGE_DEF+rg('thru',[(0,'#fff3d0',1),(0.4,'#f4b35c',0.6),(1,'#f4b35c',0)])
b=[R(0,0,W,H,'url(#pagec)')]
b.append(g(''.join(S(f"M{random.uniform(-100,300)},{random.uniform(500,1400)} C400,{random.uniform(700,1200)} 700,{random.uniform(700,1200)} {random.uniform(900,1200)},{random.uniform(500,1400)}",random.choice(['#14142a','#1c1a30','#2a1418']),random.uniform(10,26),0.8) for _ in range(40)),filt='roughS'))
pts=[]
for i in range(28):
    a=i/28*2*math.pi; r=230+random.uniform(-70,60)
    pts.append((540+math.cos(a)*r*1.2,960+math.sin(a)*r))
hole=cr_path(pts)
b.append(g(f'<path d="{hole}" fill="#efe5cc" transform="translate(540 960) scale(1.12) translate(-540 -960)"/>',filt='roughS'))
b.append(g(f'<path d="{hole}" fill="url(#thru)"/>',filt='roughS'))
b.append(g(''.join(S(f"M{x},{y} l{random.uniform(-14,14)},{random.uniform(-14,14)}",'#f7eedb',2,0.9) for x,y in pts for _ in range(4)),filt='b1'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
