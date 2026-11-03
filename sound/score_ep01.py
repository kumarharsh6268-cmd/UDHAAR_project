# Episode 1 arrangement (same instruments/motif as the pilot; arc: memory -> morning -> the glass -> the hands -> money -> the question)
import numpy as np
import score as B
from score import SR, NOTE, tanpura, felt_piano, bowed, heartbeat, low_sine_pad, RNG
import synth as S
def score(tl):
    dur=float(tl['duration']); n=int((dur+1)*SR)
    dry=np.zeros(n,np.float32); low=np.zeros(n,np.float32)
    s=lambda i: B._L(tl,i,'start'); e=lambda i: B._L(tl,i,'end')
    fbell=tl.get('music_cues',{}).get('final_bell',e('L13')+0.35)
    def add(buf,x,t0,g=1.0):
        i=int(t0*SR); m=min(len(x),n-i)
        if m>0 and i>=0: buf[i:i+m]+=x[:m]*g
    def motif(t0,notes,sp=1.4,vel=0.5,g=1.0):
        for k,nn in enumerate(notes): add(dry,felt_piano(NOTE[nn],5.5,vel*(1-0.08*k)),t0+k*sp*(1+0.05*RNG.standard_normal()),g)
    # memory of the funeral: series theme returns
    tp=tanpura(0.0,e('L05')+1.0,1.0); add(low,tp,0.0,0.22)
    motif(s('L01')+0.9,['Bb3','A3','Eb4','D4'],1.45,0.48)
    # morning at the station: lighter, curious
    motif(s('L04')+0.3,['D4','F4','A4','G4'],1.6,0.34,0.9)
    add(dry,felt_piano(NOTE['F4'],5.0,0.3),s('L05')+1.8,0.8)
    # the glass: warmth
    add(low,low_sine_pad(NOTE['D2'],e('L07')-s('L06')+2.0,2.0,2.0),s('L06'),0.10)
    add(low,bowed([NOTE['D3'],NOTE['A3']],e('L07')-s('L06')+2.0,2.2,2.2,1400,4.5),s('L06')+0.2,0.20)
    motif(s('L07')+0.6,['A3','Bb3','D4'],1.6,0.42,0.9)
    # the hands: hush, low swell; one callback note on "wahi haath"
    add(low,bowed([NOTE['D2'],NOTE['A2']],e('L08')-s('L08')+1.5,1.6,2.0,1000,3.5,0.003),s('L08')+1.0,0.24)
    add(dry,felt_piano(NOTE['Bb3'],6.0,0.42),s('L08')+3.7,0.9)
    # puzzlement: one sustained low note
    add(low,bowed([NOTE['D2']],e('L09')-s('L09')+2.0,1.4,2.0,900,4.0,0.0015),s('L09'),0.45)
    # money: soft pulse
    add(low,heartbeat(s('L10')-0.2,e('L11')+0.3,1.12,0.9),s('L10')-0.2,0.8)
    add(low,low_sine_pad(NOTE['D2'],e('L11')-s('L10')+1.5,2.0,1.2),s('L10'),0.14)
    # the question: near silence, then land
    add(low,low_sine_pad(NOTE['D2'],e('L13')-s('L12')+1.0,1.0,1.0),s('L12')+0.2,0.05)
    for nn,v in [('D3',0.5),('A3',0.45),('D4',0.45)]: add(dry,felt_piano(NOTE[nn],6.0,v),fbell,0.8)
    add(low,tanpura(0.0,dur-fbell+0.5,1.0),fbell,0.2)
    add(low,bowed([NOTE['D3'],NOTE['A3'],NOTE['D4']],dur-fbell+0.5,0.8,2.5,1500,4.0),fbell,0.16)
    motif(fbell+2.2,['Bb3','A3'],1.8,0.3,0.8)
    big=S.reverb_ir(3.2,1.0,5000,0.03,np.random.default_rng(5)); small=S.reverb_ir(1.2,0.35,3000,0.01,np.random.default_rng(6))
    st=S.reverb_st(dry,0.45,big)+S.reverb_st(low,0.22,small)
    st=st[:int(dur*SR)]; st=np.stack([S.filt(S.sos_hp(30),st[:,c]) for c in range(2)],1)
    return S.norm(st,-3)
