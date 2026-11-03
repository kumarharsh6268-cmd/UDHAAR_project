import sys; sys.path.insert(0,"/home/claude/udhaar/scripts")
from art import *; from shapes import *; from manq import *; from station import *
import random, math
# Kabir alone mid-platform, diary in hand, half-turned back toward the stall glowing in the steam
d=RED_DEF+lg('sky',[(0,'#e9d6b0'),(1,'#c9b896')])+lg('plat',[(0,'#8f887a'),(1,'#3e3a34')])+rg('far',[(0,'#fff4d8',1),(1,'#f2d6a6',0)])
VY=900
b=[R(0,0,W,H,'url(#sky)'),E(300,VY-10,300,220,'url(#far)')]
b.append(P(f"M0,1920 L0,1400 L510,{VY+10} L570,{VY+10} L1080,1400 L1080,1920 Z",'url(#plat)'))
b.append(g(canopy(0,VY,'#5e5a52'),filt='rough'))
b.append(g(pillars(VY,side=-1,x0=120)+pillars(VY,side=1,x0=120),filt='roughS'))
b.append(g(E(320,VY+40,70,46,'#ffd890',0.7)+''.join(E(320+i*3,VY-i*26,16+i*4,18,'#ffffff',0.16) for i in range(7)),filt='b3'))
b.append(g(f'<path d="{shape("boy")}" fill="#f6e0b4" transform="translate(716,1716) scale(9.4) scale(-1,1)"/>',filt='b2',op=0.8))
b.append(g(f'<path d="{shape("boy")}" fill="#3a4e62" transform="translate(720,1720) scale(9.4)"/>'+f'<path d="M-6.2,-92.5 C-6.5,-101 6.5,-101 6.2,-92.5 L6,-86 L-6,-86 Z" fill="#141010" transform="translate(720,1720) scale(9.4)"/>',filt='roughS'))
b.append(g(R(600,1250,60,80,'url(#ledger)',1,'rx="5"'),filt='roughS'))
b.append(g(P("M680,1720 L780,1720 L1000,1920 L640,1920 Z",'#1b1915',0.45),filt='b6'))
open(sys.argv[1],'w').write(svg(''.join(b),d))
