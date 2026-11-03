# Episode 1 assets: railway platform, tea stall, chipped chai glass, kettle, Shankar lit profile
import math, random
from art import *
from shapes import cr_path, KABIR_PROFILE
GLASS_DEF=('<linearGradient id="chai" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d49a52"/><stop offset="1" stop-color="#8a4f22"/></linearGradient>'
           '<linearGradient id="glassg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffffff" stop-opacity="0.55"/><stop offset="0.3" stop-color="#ffffff" stop-opacity="0.12"/><stop offset="0.75" stop-color="#ffffff" stop-opacity="0.05"/><stop offset="1" stop-color="#ffffff" stop-opacity="0.4"/></linearGradient>')
def chai_glass(x,y,s=1.0,chipped=True,level=0.7,steam=True,empty=False):
    """small ribbed cutting-chai glass; (x,y) = centre of rim; height ~150*s"""
    o=f'<g transform="translate({x},{y}) scale({s})">'
    body="M-52,0 L-40,150 C-30,158 30,158 40,150 L52,0 Z"
    if not empty:
        ly=150-150*level
        o+=f'<path d="M{-52+12*(ly/150)},{ly} L-40,150 C-30,158 30,158 40,150 L{52-12*(ly/150)},{ly} Z" fill="url(#chai)"/>'
        o+=f'<ellipse cx="0" cy="{ly}" rx="{52-12*(ly/150)}" ry="7" fill="#e0b070"/>'
    o+=f'<path d="{body}" fill="url(#glassg)"/>'
    o+=''.join(f'<path d="M{-50+i*10.5},4 L{-38.5+i*8.1},148" stroke="#ffffff" stroke-opacity="{0.18 if i%2 else 0.08}" stroke-width="3"/>' for i in range(11))
    o+='<ellipse cx="0" cy="0" rx="52" ry="9" fill="none" stroke="#fffaf0" stroke-opacity="0.75" stroke-width="3"/>'
    if chipped:
        o+='<path d="M10,-9 L16,4 L21,-1 L27,9 L34,-8 Z" fill="url(#bgcut)" fill-opacity="0"/>'
        o+='<path d="M10,-9 L34,-8" stroke="#6a5a48" stroke-width="2.5" stroke-opacity="0.6"/>'
        o+='<path d="M8,-9 L15,5 L21,0 L27,10 L36,-8" fill="none" stroke="#fffaf0" stroke-width="3"/>'
        o+='<path d="M27,10 L25,30 M15,5 L12,18" stroke="#fffaf0" stroke-opacity="0.55" stroke-width="1.6"/>'
    o+='<path d="M-40,150 C-30,158 30,158 40,150" stroke="#ffffff" stroke-opacity="0.4" stroke-width="3" fill="none"/>'
    if steam:
        o+=''.join(f'<path d="M{dx},-14 C{dx-18},-60 {dx+22},-90 {dx},-150 C{dx-20},-190 {dx+16},-220 {dx},-260" stroke="#ffffff" stroke-opacity="0.28" stroke-width="12" fill="none" filter="url(#b8)"/>' for dx in (-14,12))
    return o+'</g>'
def kettle(x,y,s=1.0):
    o=f'<g transform="translate({x},{y}) scale({s})">'
    o+='<path d="M-90,0 C-100,-80 -70,-130 0,-132 C70,-130 100,-80 90,0 Z" fill="#9aa0a0"/><path d="M-90,0 C-100,-80 -70,-130 0,-132" fill="none" stroke="#e6ecea" stroke-width="6" stroke-opacity="0.7"/>'
    o+='<ellipse cx="0" cy="-132" rx="40" ry="10" fill="#7a8080"/><rect x="-10" y="-150" width="20" height="18" rx="5" fill="#5a6060"/>'
    o+='<path d="M80,-40 C130,-60 150,-90 170,-120 L180,-112 C160,-70 130,-40 90,-20 Z" fill="#8a9090"/>'
    o+='<path d="M-60,-120 C-80,-200 80,-200 60,-120" fill="none" stroke="#3a3a3a" stroke-width="7"/>'
    o+='<ellipse cx="0" cy="2" rx="92" ry="10" fill="#4a4d4d"/>'
    o+=''.join(f'<path d="M{170+i*6},-126 C{150+i*10},-190 {200+i*6},-240 {170+i*8},-320" stroke="#ffffff" stroke-opacity="0.32" stroke-width="18" fill="none" filter="url(#b8)"/>' for i in range(2))
    return o+'</g>'
def stove(x,y,s=1.0):
    return f'<g transform="translate({x},{y}) scale({s})"><rect x="-70" y="0" width="140" height="60" rx="8" fill="#2c2c2a"/><rect x="-60" y="-14" width="120" height="16" fill="#3a3a38"/><ellipse cx="0" cy="-12" rx="56" ry="10" fill="#4a4e8a" fill-opacity="0.7"/><ellipse cx="0" cy="-14" rx="40" ry="6" fill="#9ab0ff" fill-opacity="0.6"/></g>'
def canopy(y0=0,depth_y=900,col='#2b2a28'):
    """platform roof seen from below/along, receding to vanishing point (540,depth_y)"""
    vx,vy=540,depth_y; o=''
    o+=P(f"M0,{y0} L1080,{y0} L1080,{y0+160} L{vx+60},{vy-40} L{vx-60},{vy-40} L0,{y0+160} Z",col)
    for i in range(9):
        t=i/9; yy=y0+160+(vy-40-y0-160)*(1-(1-t)**2.2)
        xl=0+(vx-60)*(1-(1-t)**2.2); xr=1080-(1080-vx-60)*(1-(1-t)**2.2)
        o+=S(f"M{xl},{yy} L{xr},{yy}",'#1a1918',max(1,8*(1-t)),0.9)
        o+=S(f"M{xl},{yy} C{(xl+540)/2},{yy-30*(1-t)} {(xr+540)/2},{yy-30*(1-t)} {xr},{yy}",'#1a1918',max(1,5*(1-t)),0.8)
    return o
def pillars(vy=900,col='#cfc7b0',shade='#8f8874',n=7,side=1,x0=210):
    o=''
    for i in range(n):
        t=1-(1-i/n)**2.0
        x=x0+(540-x0)*t if side<0 else 1080-x0-(1080-x0-540)*t
        top=160+(vy-200)*t; bot=1500-(1500-vy-20)*t; w=max(4,46*(1-t))
        o+=R(x-w/2,top,w,bot-top,col)+R(x-w/2+w*0.6,top,w*0.4,bot-top,shade)
        o+=R(x-w,top,w*2,w*0.5,col)
    return o
def number_board(x,y,s=1.0,num='4'):
    return (f'<g transform="translate({x},{y}) scale({s})"><path d="M-30,-120 L-30,0 M30,-120 L30,0" stroke="#1d1c1a" stroke-width="5"/>'
            f'<rect x="-70" y="0" width="140" height="120" rx="6" fill="#e9c94a"/><rect x="-62" y="8" width="124" height="104" rx="4" fill="none" stroke="#1d1c1a" stroke-width="3"/>'
            f'<text x="0" y="96" font-family="Mukta" font-weight="800" font-size="96" text-anchor="middle" fill="#1d1c1a">{num}</text></g>')
def shankar_lit(gid='sskin'):
    """old man profile facing LEFT, warm side light; bald crown, white side hair, white stubble & moustache, wrinkles"""
    pts=list(KABIR_PROFILE)
    # droop nose tip & sharpen cheek: small tweaks
    pts=[(x+6,y+8) if 26<=i<=31 else (x,y) for i,(x,y) in enumerate(pts)]
    face=cr_path(pts)
    o=f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0.12" stop-color="#9c6a4a"/><stop offset="0.5" stop-color="#6a4330"/><stop offset="1" stop-color="#2e1d14"/></linearGradient></defs>'
    o+=f'<path d="{face}" fill="url(#{gid})"/>'
    o+=''.join(f'<circle cx="{620+i*14}" cy="{360+j*16+i*3}" r="2" fill="#cfc8ba" fill-opacity="0.55"/>' for i in range(10) for j in range(10) if 620+i*14<770-j*2)
    o+='<path d="M560,150 C640,150 720,200 760,300" fill="none" stroke="#f0c896" stroke-width="5" stroke-opacity="0.6"/>'
    # wrinkles
    o+='<path d="M352,250 C380,244 420,244 450,250 M350,285 C380,278 420,278 452,286 M356,214 C384,208 420,208 444,214" stroke="#3a2418" stroke-width="3" fill="none" stroke-opacity="0.55"/>'
    o+='<path d="M392,390 C410,400 426,402 442,398 M394,404 C412,418 430,420 446,414" stroke="#3a2418" stroke-width="2.6" fill="none" stroke-opacity="0.6"/>'
    o+='<path d="M330,505 C356,540 380,590 392,640" stroke="#3a2418" stroke-width="4" fill="none" stroke-opacity="0.6"/>'
    o+='<path d="M420,470 C450,520 460,560 450,600" stroke="#2e1d14" stroke-width="10" fill="none" stroke-opacity="0.25" stroke-linecap="round"/>'
    # eye (warm, wet)
    o+='<path d="M348,382 C358,375 372,375 384,382 C372,389 358,389 348,382 Z" fill="#e2cdb4"/><ellipse cx="356" cy="382" rx="6.5" ry="6.5" fill="#1d130e"/><circle cx="354" cy="379" r="2" fill="#fff4dc"/>'
    o+='<path d="M344,378 C356,368 374,368 390,376" stroke="#2a1a12" stroke-width="5" fill="none"/>'
    o+='<path d="M336,350 C356,342 380,344 398,352" stroke="#e6e0d4" stroke-width="8" fill="none" stroke-linecap="round" stroke-opacity="0.85"/>'
    # white moustache + stubble
    o+='<path d="M296,518 C312,506 336,508 352,528 C344,538 320,538 300,532 Z" fill="#e9e4da"/>'
    o+=''.join(f'<circle cx="{x}" cy="{y}" r="2.4" fill="#ece7dd" fill-opacity="0.85"/>' for x,y in [(338+i*9+random.Random(i).uniform(-3,3),600+j*14+random.Random(i*7+j).uniform(-4,4)+i*4) for i in range(10) for j in range(4)] if y<700)
    # ear (bigger)
    o+='<path d="M600,410 C640,392 670,432 660,486 C650,530 618,536 598,512 Z" fill="#6a4330"/><path d="M614,432 C636,428 646,456 638,484" stroke="#3a2418" stroke-width="4" fill="none"/>'
    # shawl over shoulder
    o+='<path d="M420,820 C520,800 700,800 820,850 L1140,1000 L1140,1520 L330,1520 C340,1260 370,1000 420,820 Z" fill="#6d6a62"/>'
    o+='<path d="M430,830 C520,812 700,812 820,860 C900,900 1000,950 1140,1010" fill="none" stroke="#d8c39a" stroke-width="6" stroke-opacity="0.6"/>'
    o+=''.join(f'<path d="M{480+i*70},{840+i*12} C{470+i*72},{1000} {460+i*74},{1200} {450+i*76},1520" stroke="#57544d" stroke-width="5" fill="none" stroke-opacity="0.6"/>' for i in range(8))
    return o
