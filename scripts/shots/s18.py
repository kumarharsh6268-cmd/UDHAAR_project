import sys; sys.path.insert(0,'/home/claude/udhaar/scripts')
from art import *; from shapes import *
# MEMORY (sepia): Papa's big hand resting over the brass bell on a high shelf; a child's small hand reaching up, not allowed
d=BRASS_DEF+lg('wall',[(0,'#bba57f'),(1,'#8a7656')])+rg('glow',[(0,'#fff1cc',0.6),(1,'#fff1cc',0)],0.5,0.35,0.7)+lg('pskin',[(0,'#8a6448'),(1,'#5a3e2c')],0,0,1,1)+lg('cskin',[(0,'#b88a64'),(1,'#8a5f42')],0,0,1,1)
b=[R(0,0,W,H,'url(#wall)'),R(0,0,W,H,'url(#glow)')]
b.append(g(R(80,860,920,44,'#5a4630')+R(80,904,920,18,'#3e301f')+R(120,920,840,30,'#2e2418',0.4),filt='rough'))
b.append(g(bell(560,720,1.5),filt='roughS'))
hr=cr_path(HAND_R5)
# Papa's hand coming from top-right, palm resting on the dome (fingers down over it)
b.append(g(f'<path d="{hr}" fill="url(#pskin)" transform="translate(640,430) rotate(165) scale(1.75)"/>'+P("M600,420 L760,0 L1080,0 L1080,140 L760,470 Z",'#8c7853'),filt='roughS'))
# child's hand reaching up from bottom-left (small)
b.append(g(f'<path d="{hr}" fill="url(#cskin)" transform="translate(400,1500) rotate(-12) scale(1.05)"/>'+P("M330,1500 L470,1500 L520,1920 L260,1920 Z",'#7f8fa0'),filt='roughS'))
b.append(g(E(420,1280,160,120,'#fff4d6',0.25),filt='b40'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
