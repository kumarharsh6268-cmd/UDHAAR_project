import sys; sys.path.insert(0,'/home/claude/udhaar/scripts')
from art import *; from shapes import *
# Ma's hand gripping the door frame, trembling (ghosted double image); edge of white pallu
d=lg('skin',[(0,'#9a6a4c'),(1,'#5a3a28')],0,0,1,0)+lg('bg',[(0,'#e9b86e'),(1,'#7a5430')],0,0,1,0)
b=[R(0,0,W,H,'#16120f'),R(620,0,460,H,'url(#bg)')]
b.append(g(R(470,0,180,H,'#4a3524')+R(500,0,30,H,'#6a5038')+R(620,0,26,H,'#2a1d14'),filt='rough'))
hd=cr_path(HAND_R5)
for dx,op in ((10,0.35),(0,1)):
    b.append(g(f'<path d="{hd}" fill="url(#skin)" transform="translate({560+dx},980) rotate(-100) scale(2.6)"/>',filt='roughS',op=op))
b.append(g(P("M-40,1100 C120,1080 320,1110 470,1180 L470,1920 L-40,1920 Z",'#bdb5a3')+S("M-40,1100 C120,1080 320,1110 470,1180",'#efe6d2',6,0.8)+S("M60,1200 C140,1400 160,1600 150,1920 M300,1180 C350,1400 380,1650 390,1920",'#8f887a',8,0.6),filt='roughS'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
