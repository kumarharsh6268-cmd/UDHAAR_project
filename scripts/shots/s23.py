import sys; sys.path.insert(0,'/home/claude/udhaar/scripts')
from art import *; from shapes import *; from manq import hand
import math
# Counting: pages fanning under Kabir's thumb (fore-edge view), motion
d=RED_DEF+PAGE_DEF+rg('bulb',[(0,'#ffe2a6',0.45),(1,'#ffe2a6',0)],0.5,0.3,0.8)
b=[R(0,0,W,H,'#18130f')]
b.append(g(R(140,1180,800,80,'url(#ledger)',1,'rx="10"'),filt='rough'))
pages=''
for i in range(46):
    a=-80+i*3.4; r=760
    x2=540+r*math.cos(math.radians(a-90))*0.95; y2=1200+r*math.sin(math.radians(a-90))
    pages+=f'<path d="M540,1200 Q{(540+x2)/2+40},{(1200+y2)/2} {x2},{y2}" stroke="{["#efe5cc","#e2d6b8","#d8c8a6"][i%3]}" stroke-width="9" fill="none" stroke-opacity="0.95"/>'
b.append(g(pages,filt='b2'))
b.append(g(R(140,1150,800,60,'url(#ledger)',1,'rx="10"'),filt='rough'))
b.append(g(hand(700,1520,200,10,(1,1,1,1,1),'R',skin='#6b4632',hi='#a06e4c',lo='#3e281c')+P("M720,1560 L1100,1500 L1100,1920 L760,1920 Z",'#6f8aa0'),filt='roughS'))
b.append(R(0,0,W,H,'url(#bulb)'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
