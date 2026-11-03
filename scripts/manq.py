# Jointed mannequin silhouettes: pose = dict of joint -> (x,y) in units where standing height ~ 100
import math
from shapes import cr_path
def _cap(a,b,w1,w2,fill):
    (x1,y1),(x2,y2)=a,b; dx,dy=x2-x1,y2-y1; L=math.hypot(dx,dy)+1e-9; nx,ny=-dy/L,dx/L
    p=[(x1+nx*w1/2,y1+ny*w1/2),(x2+nx*w2/2,y2+ny*w2/2),(x2-nx*w2/2,y2-ny*w2/2),(x1-nx*w1/2,y1-ny*w1/2)]
    s=f'<path d="M{p[0][0]:.2f},{p[0][1]:.2f} L{p[1][0]:.2f},{p[1][1]:.2f} L{p[2][0]:.2f},{p[2][1]:.2f} L{p[3][0]:.2f},{p[3][1]:.2f} Z" fill="{fill}"/>'
    s+=f'<circle cx="{x1}" cy="{y1}" r="{w1/2}" fill="{fill}"/><circle cx="{x2}" cy="{y2}" r="{w2/2}" fill="{fill}"/>'
    return s
def body(P,fill,build=1.0,head_r=(6.0,7.2),female=False):
    o=[]
    W=lambda w: w*build
    # legs (back first doesn't matter in silhouette)
    for s in 'LR':
        o.append(_cap(P['hip'+s],P['knee'+s],W(8.5),W(6.4),fill))
        o.append(_cap(P['knee'+s],P['ankle'+s],W(6.2),W(3.6),fill))
        o.append(_cap(P['ankle'+s],P['toe'+s],W(3.4),W(2.6),fill))
    # torso: smooth polygon around shoulders, chest, waist, hips
    sL,sR,hL,hR=P['shL'],P['shR'],P['hipL'],P['hipR']
    ch=P['chest']; pv=P['pelvis']
    tor=[sL,((sL[0]+ch[0])/2,(sL[1]+ch[1])/2),P.get('waistL',((sL[0]+hL[0])/2,(sL[1]+hL[1])/2)),hL,pv,hR,P.get('waistR',((sR[0]+hR[0])/2,(sR[1]+hR[1])/2)),((sR[0]+ch[0])/2,(sR[1]+ch[1])/2),sR,P['neck']]
    o.append(f'<path d="{cr_path(tor)}" fill="{fill}"/>')
    o.append(_cap(sL,sR,W(7),W(7),fill)); o.append(_cap(P['neck'],ch,W(9),W(13),fill)); o.append(_cap(ch,pv,W(14),W(14),fill))
    o.append(_cap(P['neck'],P['head'],W(4.6),W(4.6),fill))
    # arms
    for s in 'LR':
        o.append(_cap(P['sh'+s],P['elb'+s],W(5.2),W(4.4),fill))
        o.append(_cap(P['elb'+s],P['wr'+s],W(4.2),W(3.0),fill))
        if 'hand'+s in P: o.append(_cap(P['wr'+s],P['hand'+s],W(3.4),W(2.6),fill))
    hx,hy=P['head']; ang=P.get('head_ang',0)
    o.append(f'<ellipse cx="{hx}" cy="{hy}" rx="{head_r[0]}" ry="{head_r[1]}" fill="{fill}" transform="rotate({ang} {hx} {hy})"/>')
    if 'nose' in P: nx_,ny_=P['nose']; o.append(f'<ellipse cx="{nx_}" cy="{ny_}" rx="1.6" ry="1.2" fill="{fill}"/>')
    return ''.join(o)
def poly(pts,fill,op=1): return f'<path d="{cr_path(pts)}" fill="{fill}" fill-opacity="{op}"/>'
def figure(P,fill,rim=None,rim_dx=0,rim_dy=0,garments=(),build=1.0,tf=''):
    inner=body(P,fill,build)+''.join(garments)
    out=''
    if rim:
        rb=body(P,rim,build)+''.join(gm.replace(f'fill="{fill}"',f'fill="{rim}"') for gm in garments)
        out+=f'<g transform="{tf} translate({rim_dx},{rim_dy})">{rb}</g>'
    out+=f'<g transform="{tf}">{inner}</g>'
    return out
# ---------------- poses (side views facing LEFT unless noted) ----------------
def pose_old_walk():
    return dict(head=(-6,-90),head_ang=20,nose=(-12.5,-89),neck=(-1,-83),chest=(2,-74),pelvis=(3,-50),shL=(-2,-79),shR=(5,-80),
        elbL=(-6,-63),wrL=(-12,-52),handL=(-14,-49),elbR=(8,-63),wrR=(5,-50),handR=(4,-46),
        hipL=(1,-50),hipR=(5,-50),kneeL=(-7,-27),ankleL=(-9,-3),toeL=(-15,-1),kneeR=(7,-26),ankleR=(14,-4),toeR=(9,-1),waistL=(-1,-62),waistR=(7,-62))
def pose_old_kneel():
    # sitting on heels, torso bent forward, hands reaching to front (feet of bier at left)
    return dict(head=(-30,-46),head_ang=55,nose=(-34,-41),neck=(-23,-49),chest=(-14,-50),pelvis=(4,-30),shL=(-20,-53),shR=(-14,-55),
        elbL=(-32,-36),wrL=(-42,-26),handL=(-47,-24),elbR=(-28,-38),wrR=(-38,-27),handR=(-43,-25),
        hipL=(2,-30),hipR=(6,-31),kneeL=(-12,-6),ankleL=(14,-4),toeL=(20,-2),kneeR=(-10,-5),ankleR=(16,-5),toeR=(22,-3),waistL=(-8,-40),waistR=(2,-44))
def pose_sit_floor():
    # Kabir sitting on floor, knees up, leaning over trunk (facing LEFT)
    return dict(head=(-14,-68),head_ang=25,nose=(-20,-66),neck=(-8,-61),chest=(-3,-50),pelvis=(4,-20),shL=(-8,-57),shR=(-1,-58),
        elbL=(-18,-42),wrL=(-28,-36),handL=(-33,-35),elbR=(-12,-40),wrR=(-24,-34),handR=(-29,-33),
        hipL=(2,-18),hipR=(6,-19),kneeL=(-16,-36),ankleL=(-26,-4),toeL=(-33,-2),kneeR=(-12,-34),ankleR=(-22,-3),toeR=(-29,-1),waistL=(-5,-34),waistR=(4,-36))
def pose_stand_front():
    return dict(head=(0,-92),neck=(0,-84),chest=(0,-74),pelvis=(0,-50),shL=(-11.5,-80),shR=(11.5,-80),elbL=(-13.5,-63),wrL=(-12,-49),handL=(-11.5,-44),elbR=(13.5,-63),wrR=(9,-55),handR=(5,-58),
        hipL=(-6,-50),hipR=(6,-50),kneeL=(-6.5,-27),ankleL=(-6,-4),toeL=(-7,-1),kneeR=(6.5,-27),ankleR=(6,-4),toeR=(7,-1),waistL=(-9,-62),waistR=(9,-62))
HEAD_PROF=[(0,-7.4),(4.5,-6.2),(7,-2.5),(6.8,2),(5,5),(3,6.4),(3.2,8.6),(-2.4,8.6),(-3.0,6.8),(-5.2,6.0),(-5.6,4.9),(-6.1,3.8),(-5.8,3.2),(-6.4,2.5),(-6.5,1.7),(-8.3,0.9),(-6.7,-1.3),(-6.9,-2.6),(-6.4,-4.8),(-4,-6.8)]
def head_prof(cx,cy,ang,fill,scale=1.0):
    return f'<path d="{cr_path([(x*scale,y*scale) for x,y in HEAD_PROF])}" fill="{fill}" transform="translate({cx},{cy}) rotate({ang})"/>'
def body2(P,fill,build=1.0):
    """body with a profile head instead of ellipse (side views)"""
    Q=dict(P); hx,hy=Q['head']; ang=Q.get('head_ang',0)
    s=body({k:v for k,v in Q.items() if k!='nose'},fill,build,head_r=(0.01,0.01))
    return s+head_prof(hx,hy,ang,fill)
def hand(x,y,ang,sc,fingers=(1,1,1,1,1),side='R',skin='#5d3d2b',hi='#8c6046',lo='#3a261b',nail='#c9ab90',crease='#2e1e15'):
    """dorsal view, wrist at origin, fingers toward +y. side R: thumb on +x? (mirror for L)."""
    m=1 if side=='R' else -1
    o=[]
    # palm/back of hand
    palm=[(-4.6*m,0),(4.4*m,0),(5.4*m,4),(5.6*m,8.6),(2.2*m,10),(-1*m,10.2),(-4.2*m,9.6),(-5.6*m,6),(-5.2*m,2.5)]
    o.append(f'<path d="{cr_path(palm)}" fill="{skin}"/>')
    # fingers: (base x, length, width, angle)  order index..little from thumb side
    spec=[(3.9,7.4,2.6,-4),(1.3,8.3,2.7,-1),(-1.3,7.8,2.55,2),(-3.8,6.1,2.3,6)]
    for i,(bx,L,w,a) in enumerate(spec):
        if not fingers[i+1]:
            # healed stump
            o.append(f'<g transform="translate({bx*m},9.6) rotate({a*m})"><path d="M{-w/2},0 C{-w/2},1.6 {w/2},1.6 {w/2},0 Z" fill="{skin}"/><ellipse cx="0" cy="0.9" rx="{w/2}" ry="1.1" fill="{skin}"/><path d="M{-w*0.35},1.3 C0,1.9 {w*0.35},1.3" stroke="{lo}" stroke-width="0.25" fill="none"/></g>')
            continue
        seg=[L*0.42,L*0.32,L*0.26]
        g_=f'<g transform="translate({bx*m},9.4) rotate({a*m})">'
        yy=0; ww=w
        for k,sL in enumerate(seg):
            w2=ww*0.92
            g_+=f'<path d="M{-ww/2},{yy} L{-w2/2},{yy+sL} L{w2/2},{yy+sL} L{ww/2},{yy} Z" fill="{skin}"/><ellipse cx="0" cy="{yy+sL}" rx="{w2/2+0.05}" ry="{0.55}" fill="{skin}"/>'
            # knuckle creases
            g_+=f'<path d="M{-w2*0.3},{yy+sL-0.15} C{-w2*0.1},{yy+sL+0.25} {w2*0.1},{yy+sL+0.25} {w2*0.3},{yy+sL-0.15}" stroke="{crease}" stroke-width="0.22" fill="none" stroke-opacity="0.8"/>'
            yy+=sL; ww=w2
        g_+=f'<ellipse cx="0" cy="{yy}" rx="{ww/2}" ry="{ww*0.48}" fill="{skin}"/>'
        g_+=f'<ellipse cx="0" cy="{yy-0.55}" rx="{ww*0.3}" ry="{ww*0.42}" fill="{nail}" fill-opacity="0.75"/>'
        g_+=f'<path d="M{-ww*0.42},0.6 L{-ww*0.4},{yy-0.5}" stroke="{hi}" stroke-width="0.35" stroke-opacity="0.6"/>'
        o.append(g_+'</g>')
    # thumb (on thumb side, angled outward)
    if fingers[0]:
        o.append(f'<g transform="translate({4.8*m},3.2) rotate({-38*m})"><path d="M-1.6,0 L-1.3,6.4 L1.3,6.4 L1.7,0 Z" fill="{skin}"/><ellipse cx="0" cy="6.4" rx="1.32" ry="1.25" fill="{skin}"/><ellipse cx="0" cy="5.9" rx="0.75" ry="1.0" fill="{nail}" fill-opacity="0.7"/><path d="M-0.7,3.2 C0,3.6 0.7,3.2" stroke="{crease}" stroke-width="0.22" fill="none"/></g>')
    # knuckles, veins, tendons, light
    o.append(''.join(f'<ellipse cx="{bx*m}" cy="9.3" rx="1.1" ry="0.7" fill="{hi}" fill-opacity="0.45"/>' for bx,_,_,_ in spec))
    o.append(f'<path d="M{-1*m},1 C{-0.6*m},4 {0.4*m},6 {1.2*m},9 M{2*m},0.5 C{2.4*m},4 {3.1*m},6 {3.8*m},9 M{-3*m},1 C{-2.8*m},4 {-2.6*m},6 {-3.6*m},9" stroke="{lo}" stroke-width="0.35" fill="none" stroke-opacity="0.55"/>')
    o.append(f'<path d="M{-4.5*m},0.4 C{-4.9*m},3 {-5.2*m},6 {-4.8*m},9" stroke="{hi}" stroke-width="0.6" fill="none" stroke-opacity="0.5"/>')
    # wrist + sleeve cuff
    o.append(f'<path d="M-4.8,0.5 L-5.2,-12 L5.2,-12 L4.6,0.5 Z" fill="{skin}"/>')
    return f'<g transform="translate({x},{y}) rotate({ang}) scale({sc})">{"".join(o)}</g>'
def flipP(P):
    Q={}
    for k,v in P.items():
        if k=='head_ang': Q[k]=-v
        else: Q[k]=(-v[0],v[1])
    # swap L/R so draw order stays sane
    return Q
def pose_sew():
    # woman seated on low stool at sewing machine, facing LEFT, leaning forward
    return dict(head=(-6,-70),head_ang=18,neck=(-2,-63),chest=(0,-54),pelvis=(4,-32),shL=(-4,-60),shR=(3,-61),
        elbL=(-12,-46),wrL=(-24,-44),handL=(-28,-44),elbR=(-8,-44),wrR=(-20,-42),handR=(-25,-42),
        hipL=(2,-31),hipR=(6,-32),kneeL=(-14,-30),ankleL=(-14,-4),toeL=(-20,-1),kneeR=(-12,-28),ankleR=(-10,-3),toeR=(-16,-1),waistL=(-3,-44),waistR=(6,-44))
def pose_stand_side():
    return dict(head=(-1,-92),head_ang=0,neck=(0,-84),chest=(0,-74),pelvis=(1,-50),shL=(-2,-80),shR=(3,-80),
        elbL=(-3,-63),wrL=(-6,-49),handL=(-7,-45),elbR=(6,-63),wrR=(8,-49),handR=(8,-45),
        hipL=(-1,-50),hipR=(3,-50),kneeL=(-6,-27),ankleL=(-9,-3),toeL=(-15,-1),kneeR=(6,-27),ankleR=(10,-4),toeR=(5,-1),waistL=(-3,-62),waistR=(5,-62))
