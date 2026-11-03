import sys; sys.path.insert(0,'/home/claude/udhaar/scripts')
from art import *; from shapes import *
# Night: Kabir's face lit by the diya under Papa's portrait, looking at it (we see portrait frame edge, blurred)
d=rg('dg',[(0,'#ffcf86',0.55),(0.4,'#e08a3c',0.18),(1,'#e08a3c',0)],0.2,0.75,0.7)
b=[R(0,0,W,H,'#14110f')]
b.append(g(R(-160,200,300,900,'#3a2a1e')+R(-130,240,250,820,'#6a573e')+E(20,1180,40,26,'#e9a95a',0.7),filt='b12'))
b.append(R(0,0,W,H,'url(#dg)'))
b.append(g(kabir_lit()+kabir_kurta(fill='#4b4337',edge='#e5b779'),tf='translate(60,380) scale(1.12)',filt='roughS'))
b.append(g(E(330,1100,60,40,'#ffd08a',0.35),filt='b24'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
