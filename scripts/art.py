# Shared illustration library for UDHAAR (SVG generators)
import math, random
W,H=1080,1920
def defs(extra=''):
    return f'''<defs>
<filter id="rough" x="-10%" y="-10%" width="120%" height="120%"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="3" seed="3" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="7" xChannelSelector="R" yChannelSelector="G"/></filter>
<filter id="roughS" x="-10%" y="-10%" width="120%" height="120%"><feTurbulence type="fractalNoise" baseFrequency="0.06" numOctaves="2" seed="5" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="3.5" xChannelSelector="R" yChannelSelector="G"/></filter>
<filter id="roughL" x="-20%" y="-20%" width="140%" height="140%"><feTurbulence type="fractalNoise" baseFrequency="0.012" numOctaves="4" seed="8" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="40" xChannelSelector="R" yChannelSelector="G"/></filter>
<filter id="wash" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.008 0.02" numOctaves="4" seed="11" result="t"/><feColorMatrix in="t" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -1.1 1.05" result="a"/><feComposite in="SourceGraphic" in2="a" operator="in" result="m"/><feBlend in="SourceGraphic" in2="m" mode="multiply"/></filter>
<filter id="washS" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.03 0.06" numOctaves="3" seed="21" result="t"/><feColorMatrix in="t" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -0.9 0.85" result="a"/><feComposite in="SourceGraphic" in2="a" operator="in" result="m"/><feBlend in="SourceGraphic" in2="m" mode="multiply"/></filter>
<filter id="smoke" x="-50%" y="-20%" width="200%" height="140%"><feTurbulence type="fractalNoise" baseFrequency="0.012 0.006" numOctaves="5" seed="4" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="120" xChannelSelector="R" yChannelSelector="G" result="d"/><feGaussianBlur in="d" stdDeviation="10"/></filter>
<filter id="fog" x="-20%" y="-50%" width="140%" height="200%"><feTurbulence type="fractalNoise" baseFrequency="0.004 0.012" numOctaves="4" seed="9" result="n"/><feColorMatrix in="n" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 1.6 -0.55" result="a"/><feComposite in="SourceGraphic" in2="a" operator="in"/><feGaussianBlur stdDeviation="6"/></filter>
''' + ''.join(f'<filter id="b{s}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{s}"/></filter>' for s in (1,2,3,4,6,8,12,16,24,40,60)) + extra + '</defs>'
def svg(body, extra_defs='', bg='#000'):
    return f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="background:{bg}">{defs(extra_defs)}{body}</svg>'
def lg(id,stops,x1=0,y1=0,x2=0,y2=1):
    s=''.join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o,c,a in [(t+(1,) if len(t)==2 else t) for t in stops])
    return f'<linearGradient id="{id}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{s}</linearGradient>'
def rg(id,stops,cx=.5,cy=.5,r=.5,fx=None,fy=None):
    s=''.join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o,c,a in [(t+(1,) if len(t)==2 else t) for t in stops])
    f=f' fx="{fx}" fy="{fy}"' if fx is not None else ''
    return f'<radialGradient id="{id}" cx="{cx}" cy="{cy}" r="{r}"{f}>{s}</radialGradient>'
def g(content,tf='',filt=None,op=1,extra=''):
    a=f' transform="{tf}"' if tf else ''
    f=f' filter="url(#{filt})"' if filt else ''
    o=f' opacity="{op}"' if op!=1 else ''
    return f'<g{a}{f}{o} {extra}>{content}</g>'
def P(d,fill,op=1,extra=''):
    o=f' fill-opacity="{op}"' if op!=1 else ''
    return f'<path d="{d}" fill="{fill}"{o} {extra}/>'
def S(d,stroke,w=2,op=1,cap='round',extra=''):
    return f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{w}" stroke-opacity="{op}" stroke-linecap="{cap}" stroke-linejoin="round" {extra}/>'
def E(cx,cy,rx,ry,fill,op=1,extra=''):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" fill-opacity="{op}" {extra}/>'
def R(x,y,w,h,fill,op=1,extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" fill-opacity="{op}" {extra}/>'

# ---------- distant figures (unit: feet at 0, height 100) ----------
FIG={
# man in kurta-pajama, standing, arms down
'man': "M-6,-100 C-1,-101 6,-99 6,-92 C6,-86 3,-84 2.5,-82 L11,-79 C15,-77 16,-71 16,-62 L17.5,-40 C17.5,-37 15,-37 14,-40 L13,-56 L13.5,-34 L11,-33 L9,-2 L10,0 L3,0 L2,-28 L0,-30 L-2,-28 L-3,0 L-10,0 L-9,-2 L-11,-33 L-13.5,-34 L-13,-56 L-14,-40 C-15,-37 -17.5,-37 -17.5,-40 L-16,-62 C-16,-71 -15,-77 -11,-79 L-2.5,-82 C-3,-84 -6,-86 -6,-92 C-6,-97 -8,-99 -6,-100 Z",
# woman in saree with pallu over head
'woman': "M0,-100 C7,-100 10,-94 10,-88 C12,-86 14,-82 15,-74 C18,-60 18,-46 17,-30 C19,-18 20,-8 21,0 L-21,0 C-20,-8 -19,-18 -17,-30 C-18,-46 -18,-60 -15,-74 C-14,-82 -12,-86 -10,-88 C-10,-94 -7,-100 0,-100 Z",
# old man, slightly stooped, with shawl
'oldman': "M2,-96 C8,-96 10,-90 9,-85 C8,-82 6,-81 5,-80 L13,-76 C18,-73 19,-66 18,-58 L19,-38 C19,-35 16,-35 15,-38 L14,-52 L14,-32 L11,-31 L9,-2 L10,0 L3,0 L2,-27 L0,-29 L-2,-27 L-3,0 L-10,0 L-9,-2 L-11,-32 L-13,-33 L-12,-52 L-13,-40 C-14,-37 -16.5,-37 -16.5,-40 L-15,-60 C-14,-70 -11,-76 -6,-79 L-1,-81 C-3,-84 -4,-88 -3,-92 C-2,-95 -1,-96 2,-96 Z",
# man in shirt-trousers with cap (auto driver)
'capman': "M-7,-99 L7,-99 C9,-99 9,-96 9,-95 L11,-94 L-7,-94 Z M-6,-94 L6,-94 C6,-88 4,-84 2.5,-82 L11,-79 C15,-77 16,-71 16,-62 L17.5,-42 C17.5,-39 15,-39 14,-42 L13,-56 L12,-48 L11,-2 L12,0 L3,0 L2,-40 L0,-44 L-2,-40 L-3,0 L-12,0 L-11,-2 L-12,-48 L-13,-56 L-14,-42 C-15,-39 -17.5,-39 -17.5,-42 L-16,-62 C-16,-71 -15,-77 -11,-79 L-2.5,-82 C-4,-84 -6,-88 -6,-94 Z",
# wheelchair figure (seated woman + wheel) height ~70
'wheel': "M-2,-72 C4,-72 7,-67 7,-62 C9,-60 11,-56 12,-50 L14,-34 L22,-34 L22,-30 L14,-30 L16,-14 L12,-14 L10,-28 L-6,-28 C-10,-28 -12,-32 -12,-38 L-12,-50 C-11,-57 -9,-60 -8,-62 C-8,-68 -6,-72 -2,-72 Z M-14,-22 A 20 20 0 1 0 26 -22 A 20 20 0 1 0 -14 -22 Z M-10,-22 A 16 16 0 1 1 22 -22 A 16 16 0 1 1 -10 -22 Z",
}
def fig(kind,x,y,h,fill,op=1,flip=False,extra=''):
    s=h/100.0; sx=-s if flip else s
    return f'<path d="{FIG[kind]}" fill="{fill}" fill-opacity="{op}" fill-rule="evenodd" transform="translate({x},{y}) scale({sx},{s})" {extra}/>'

# ---------- high-angle figure (seen from above ~60deg) ----------
def top_fig(x,y,s,kind='man',sun=(0.85,0.42),shadow_len=190,lit='#ece6d6',mid='#bdb9ae',dark='#8e8f88',hair='#1c1814',skin='#8a5a3e',pose='stand'):
    out=[]
    dx,dy=sun; L=shadow_len*s
    # long shadow on ground
    sx,sy=x+dx*L,y+dy*L; w=11*s
    nx,ny=-dy,dx
    out.append(g(P(f"M{x-nx*w},{y-ny*w} L{sx-nx*w*1.4},{sy-ny*w*1.4} C{sx+dx*14*s},{sy+dy*14*s} {sx+dx*14*s},{sy+dy*14*s} {sx+nx*w*1.4},{sy+ny*w*1.4} L{x+nx*w},{y+ny*w} Z",'#2f2b26',0.5),filt='b3'))
    if kind=='woman':
        # saree: wider lower body, pallu over head
        out.append(P(f"M{x-15*s},{y-2*s} C{x-17*s},{y-20*s} {x-14*s},{y-34*s} {x-9*s},{y-42*s} L{x+9*s},{y-42*s} C{x+14*s},{y-34*s} {x+17*s},{y-20*s} {x+15*s},{y-2*s} C{x+6*s},{y+3*s} {x-6*s},{y+3*s} {x-15*s},{y-2*s} Z",mid))
        out.append(P(f"M{x-15*s},{y-2*s} C{x-17*s},{y-20*s} {x-14*s},{y-34*s} {x-9*s},{y-42*s} L{x-1*s},{y-42*s} C{x-4*s},{y-30*s} {x-6*s},{y-14*s} {x-5*s},{y+1*s} Z",lit,0.85))
        out.append(E(x,y-42*s,15*s,9*s,mid)); out.append(E(x-4*s,y-44*s,10*s,6*s,lit,0.8))
        out.append(E(x+0.5*s,y-50*s,8.5*s,8.5*s,mid)); out.append(E(x-2*s,y-52*s,6*s,6*s,lit,0.9))
    else:
        body = mid
        out.append(P(f"M{x-12*s},{y-3*s} C{x-14*s},{y-18*s} {x-15*s},{y-32*s} {x-14*s},{y-40*s} L{x+14*s},{y-40*s} C{x+15*s},{y-32*s} {x+14*s},{y-18*s} {x+12*s},{y-3*s} C{x+5*s},{y+1*s} {x-5*s},{y+1*s} {x-12*s},{y-3*s} Z",body))
        out.append(P(f"M{x-12*s},{y-3*s} C{x-14*s},{y-18*s} {x-15*s},{y-32*s} {x-14*s},{y-40*s} L{x-2*s},{y-40*s} C{x-4*s},{y-28*s} {x-5*s},{y-14*s} {x-4*s},{y} Z",lit,0.85))
        out.append(E(x,y-40*s,17*s,9.5*s,mid)); out.append(E(x-5*s,y-42*s,11*s,6*s,lit,0.85))
        out.append(E(x+0.5*s,y-49*s,7.5*s,8*s,skin))
        if kind=='bald': out.append(E(x+1*s,y-50*s,6.5*s,6.5*s,'#9a9890'))
        elif kind=='cap': out.append(E(x+0.5*s,y-50*s,8*s,7.5*s,'#d9d4c4'))
        else: out.append(E(x+1*s,y-50*s,7.6*s,7.2*s,hair))
    return ''.join(out)

# ---------- eye-level person with shading + rim light ----------
_pid=[0]
def person(kind,x,y,h,body='#c9c6bc',shade='#8f918c',rim='#f6e7c8',skin='#7e5238',hair='#1b1613',rim_side=1,flip=False,op=1,rimw=2.6,bow=0,extra_defs=None,blur=None):
    """kind in FIG; rim_side +1 light from right, -1 from left"""
    _pid[0]+=1; gid=f'pg{_pid[0]}'
    s=h/100.0; sx=-s if flip else s
    gr=lg(gid,[(0,shade if rim_side>0 else body),(1,body if rim_side>0 else shade)],0,0,1,0)
    if extra_defs is not None: extra_defs.append(gr)
    tf=f'translate({x},{y}) scale({sx},{s})'
    pth=FIG[kind]
    off=rimw*rim_side/s*(-1 if flip else 1)
    out=[]
    out.append(f'<path d="{pth}" fill="{rim}" fill-rule="evenodd" transform="{tf} translate({off},{-abs(off)*0.4})"/>')
    out.append(f'<path d="{pth}" fill="url(#{gid})" fill-rule="evenodd" transform="{tf}"/>')
    # head detail: hair / pallu / face shadow  (unit coords)
    hd=''
    if kind in ('man','oldman','capman'):
        hy={'man':-92,'oldman':-88,'capman':-90}[kind]
        hd+=E(0,hy+bow,5.8,7.2,skin)
        if kind=='man': hd+=P(f"M-6.2,{hy-1+bow} C-6.5,{hy-9+bow} 6.5,{hy-9+bow} 6.2,{hy-1+bow} C4,{hy-4.5+bow} -4,{hy-4.5+bow} -6.2,{hy-1+bow} Z",hair)
        if kind=='oldman': hd+=P(f"M-5.8,{hy+bow} C-6,{hy-8+bow} 6,{hy-8+bow} 5.8,{hy+bow} C5,{hy-3+bow} 3,{hy-5+bow} 0,{hy-5+bow} C-3,{hy-5+bow} -5,{hy-3+bow} -5.8,{hy+bow} Z",'#bdb9ae')
        if kind=='capman': hd+=P("M-7,-99 L7,-99 C9,-99 9,-96 9,-95 L11,-94 L-7,-94 Z",'#4a4f55')
        # hands
        hd+=E(-15.8,-38.5,2.3,3,skin)+E(15.8,-38.5,2.3,3,skin)
    elif kind=='woman':
        hd+=E(0,-88+bow,5.2,6.4,skin,0.9)+P(f"M0,-100 C7,-100 10,-94 10,-88 C8,-90 6,-95 0,-95 C-6,-95 -8,-90 -10,-88 C-10,-94 -7,-100 0,-100 Z",body)
    out.append(f'<g transform="{tf}">{hd}</g>')
    # face/hand shadow side
    content=''.join(out)
    if blur: content=g(content,filt=blur)
    return g(content,op=op)

# ---------- props ----------
def bell(x,y,s=1.0,glint=True):
    """brass dome bus bell with striker & bracket; centre top at (x,y); width ~170*s"""
    o=(f'<g transform="translate({x},{y}) scale({s})">'
       '<rect x="-14" y="-60" width="28" height="64" rx="5" fill="#3b3226"/>'
       '<path d="M-90,70 C-90,10 -50,-12 0,-12 C50,-12 90,10 90,70 C90,82 -90,82 -90,70 Z" fill="url(#brass)"/>'
       '<ellipse cx="0" cy="72" rx="92" ry="16" fill="#6e5222"/>'
       '<ellipse cx="0" cy="70" rx="84" ry="11" fill="#2a1f12"/>'
       '<path d="M-70,40 C-60,8 -30,-4 0,-4" fill="none" stroke="#fff1c0" stroke-width="8" stroke-opacity="0.75" stroke-linecap="round"/>'
       '<ellipse cx="0" cy="-12" rx="18" ry="7" fill="#8a6a2a"/>'
       '<circle cx="0" cy="-20" r="10" fill="#b48a3a"/><path d="M-6,74 L-4,96 L4,96 L6,74 Z" fill="#3a2c1a"/><circle cx="0" cy="98" r="7" fill="#7a5a28"/>')
    if glint: o+='<circle cx="-40" cy="8" r="6" fill="#fffbe8" fill-opacity="0.9"/>'
    return o+'</g>'
BRASS_DEF='<linearGradient id="brass" x1="0" y1="0" x2="1" y2="0.3"><stop offset="0" stop-color="#e9c56a"/><stop offset="0.35" stop-color="#c79a3c"/><stop offset="0.7" stop-color="#8d6624"/><stop offset="1" stop-color="#5a4016"/></linearGradient>'
RED_DEF=('<linearGradient id="ledger" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#c8202a"/><stop offset="0.6" stop-color="#a5141e"/><stop offset="1" stop-color="#6e0c14"/></linearGradient>'
         '<pattern id="weave" width="6" height="6" patternUnits="userSpaceOnUse"><rect width="6" height="6" fill="none"/><path d="M0,3 L6,3 M3,0 L3,6" stroke="#000" stroke-opacity="0.12" stroke-width="1"/></pattern>')
def ledger_closed(x,y,w,h,rot=0):
    return (f'<g transform="translate({x},{y}) rotate({rot})">'
            f'<rect x="{-w/2+10}" y="{-h/2+12}" width="{w}" height="{h}" rx="10" fill="#120c0a" fill-opacity="0.5" filter="url(#b8)"/>'
            f'<rect x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" rx="10" fill="url(#ledger)"/>'
            f'<rect x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" rx="10" fill="url(#weave)"/>'
            f'<rect x="{-w/2}" y="{-h/2}" width="{w*0.12}" height="{h}" rx="8" fill="#7a0e16" fill-opacity="0.8"/>'
            f'<rect x="{w/2-8}" y="{-h/2+8}" width="10" height="{h-16}" fill="#efe6cf"/>'
            f'<path d="M{w/2-6},{-h/2+20} L{w/2-6},{h/2-20}" stroke="#bdb29a" stroke-width="2" stroke-dasharray="2 3"/>'
            f'<path d="M{-w/2+20},{-h/2+6} L{w/2-14},{-h/2+6}" stroke="#e05a5a" stroke-opacity="0.35" stroke-width="3"/>'
            f'<path d="M{-w/2},{h*0.1} C{-w/4},{h*0.12} {w/4},{h*0.08} {w/2+30},{h*0.14}" stroke="#d9c9a2" stroke-width="4" fill="none"/>'
            '</g>')
def htext(x,y,t,size=40,fill='#2a2a4a',rot=0,font='Kalam',weight=400,op=0.92,anchor='start'):
    return f'<text x="{x}" y="{y}" font-family="{font}" font-weight="{weight}" font-size="{size}" fill="{fill}" fill-opacity="{op}" text-anchor="{anchor}" transform="rotate({rot} {x} {y})">{t}</text>'
def ledger_page(x,y,w,h,entries,rot=0,lines=True,ink='#26284a'):
    o=f'<g transform="translate({x},{y}) rotate({rot})">'
    o+=f'<rect width="{w}" height="{h}" fill="url(#pagec)"/>'
    if lines: o+=''.join(f'<path d="M30,{yy} L{w-20},{yy}" stroke="#9fb2b6" stroke-width="1.6" stroke-opacity="0.7"/>' for yy in range(110,h-30,52))
    o+=f'<path d="M80,20 L80,{h-20}" stroke="#d08a8a" stroke-width="2" stroke-opacity="0.6"/>'
    for e in entries: o+=e
    return o+'</g>'
PAGE_DEF='<linearGradient id="pagec" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#efe5cc"/><stop offset="1" stop-color="#d8c8a6"/></linearGradient>'
