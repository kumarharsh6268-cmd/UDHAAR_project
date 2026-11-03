import sys; sys.path.insert(0,'/home/claude/udhaar/scripts')
from art import *; from shapes import *
import random
random.seed(22)
# Floor: the passbook (212) beside the open red ledger (38.4 lakh). Top-down, single bulb
d=RED_DEF+PAGE_DEF+lg('cover',[(0,'#355a5e'),(1,'#264346')])+rg('bulb',[(0,'#ffe2a6',0.5),(1,'#ffe2a6',0)],0.55,0.4,0.7)
b=[R(0,0,W,H,'#3b3934')]
b.append(g(''.join(E(random.uniform(0,W),random.uniform(0,H),random.uniform(3,7),random.uniform(2,4),random.choice(['#55534c','#2e2c28','#6a6860']),0.6) for _ in range(700)),filt='roughS'))
b.append(g(''.join(S(f"M0,{y} L1080,{y}",'#2a2824',3,0.5) for y in range(0,1920,180))+''.join(S(f"M{x},0 L{x},1920",'#2a2824',3,0.5) for x in range(0,1080,180)),filt='rough'))
# passbook small, left, slightly tilted
pb=g(R(-8,-8,286,396,'url(#cover)',1,'rx="10"')+R(0,0,134,380,'#e9e0c8')+R(136,0,134,380,'#e9e0c8')+''.join(S(f"M8,{y} L126,{y} M144,{y} L262,{y}",'#9aa7a6',1.4,0.8) for y in range(30,370,22))+''.join(S(f"M{x},{y} c10,-4 20,3 30,-2",'#3d4a5a',2,0.8) for x in (14,60,150,200) for y in range(28,200,22)),tf='translate(90,760) rotate(-8)')
b.append(g(R(100,780,300,400,'#141210',0.5),filt='b12'))
b.append(g(pb,filt='roughS'))
# ledger open big, right
b.append(g(R(450,560,600,820,'#141210',0.5),filt='b16'))
b.append(g(R(420,520,600,820,'url(#ledger)',1,'rx="12" transform="rotate(4 720 930)"')+g(R(440,540,275,780,'url(#pagec)')+R(725,540,275,780,'url(#pagec)')+''.join(S(f"M460,{y} L700,{y} M745,{y} L985,{y}",'#9fb2b6',1.4,0.7) for y in range(600,1300,40))+htext(470,640,'सलीम',44)+htext(470,700,'₹ 40,000',34)+htext(760,640,'गौरी',44)+htext(760,700,'₹ 1,20,000',34),tf='rotate(4 720 930)'),filt='roughS'))
b.append(R(0,0,W,H,'url(#bulb)'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
