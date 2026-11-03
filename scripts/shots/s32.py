import sys; sys.path.insert(0,'/home/claude/udhaar/scripts')
from art import *; from shapes import *
# Kabir looking up toward Ma (faces RIGHT, tilted up), lit by the bulb above
d=lg('bg',[(0,'#2a2622'),(1,'#121010')])+rg('top',[(0,'#ffe2a6',0.45),(1,'#ffe2a6',0)],0.6,0.0,0.8)
b=[R(0,0,W,H,'url(#bg)'),R(0,0,W,H,'url(#top)')]
b.append(g(R(860,0,260,H,'#e0a95e',0.25),filt='b40'))
b.append(g(kabir_lit(skin_hi='#b88360',look=-6)+kabir_kurta(fill='#55708a',edge='#d9b37a',shirt=True),tf='translate(1180,300) scale(-1.12,1.12) rotate(12 560 700)',filt='roughS'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
