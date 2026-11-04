# Episode 6 arrangement ("Bahattar Hazaar"): same instruments + series motif (Bb3 A3 Eb4 D4), centre D.
# Arc: cold hospital -> last words (bell colour, hush) -> three 47s (pulse + clock) -> morning, lighter ->
# the shop (warmth) -> refusal (music drops out) -> arithmetic (soft pulse) -> the turn (low drone, 1.4 s air) -> question -> land.
import numpy as np
import score as B
from score import SR, NOTE, tanpura, felt_piano, bowed, heartbeat, low_sine_pad, RNG
import synth as S
def score(tl):
    dur=float(tl['duration']); n=int((dur+1)*SR)
    dry=np.zeros(n,np.float32); low=np.zeros(n,np.float32)
    s=lambda i: B._L(tl,i,'start'); e=lambda i: B._L(tl,i,'end')
    fbell=tl.get('music_cues',{}).get('final_bell',e('g35')+0.3)
    def add(buf,x,t0,g=1.0):
        i=int(t0*SR); m=min(len(x),n-i)
        if m>0 and i>=0: buf[i:i+m]+=x[:m]*g
    def motif(t0,notes,sp=1.4,vel=0.5,g=1.0):
        for k,nn in enumerate(notes): add(dry,felt_piano(NOTE[nn],5.5,vel*(1-0.08*k)),t0+k*sp*(1+0.04*RNG.standard_normal()),g)
    # cold open: thin drone, one motif statement
    add(low,low_sine_pad(NOTE['D2'],e('g02')+1.0,1.5,1.5),0.4,0.10)
    motif(s('g00')+0.2,['Bb3','A3','Eb4','D4'],1.35,0.42,0.9)
    # last words: hush, bowed swell under the quote, then silence (bell clink is SFX)
    add(low,bowed([NOTE['D3'],NOTE['Eb3']],e('g04')-s('g03')+1.2,1.4,0.9,1200,4.0,0.002),s('g03'),0.20)
    # home, the three 47s: heartbeat + low pad
    add(low,heartbeat(s('g06')-0.2,e('g09')+0.4,1.15,0.9),s('g06')-0.2,0.75)
    add(low,low_sine_pad(NOTE['D2'],e('g09')-s('g05')+1.5,2.0,1.5),s('g05'),0.13)
    add(dry,felt_piano(NOTE['Eb4'],6.0,0.38),s('g09')+0.5,0.9)           # "mera naam nahi tha"
    # morning, page 6, the lane: lighter colour
    motif(s('g10')+0.2,['D4','F4','A4','G4'],1.5,0.32,0.85)
    add(low,tanpura(0.0,e('g15')-s('g11')+1.0,1.0),s('g11'),0.18)
    # the shop: warmth on the old machine
    motif(s('g15')+0.6,['A3','Bb3','D4'],1.5,0.36,0.85)
    # refusal: music steps away (silence under g17-g19); one low note on "beizzati"
    add(low,bowed([NOTE['D2'],NOTE['A2']],e('g23')-s('g23')+1.6,1.0,1.6,900,3.5,0.002),s('g23'),0.22)
    # arithmetic: soft pulse + ticks
    add(low,heartbeat(s('g24')-0.1,e('g26')+0.3,0.95,0.8),s('g24')-0.1,0.6)
    add(low,low_sine_pad(NOTE['D2'],e('g26')-s('g24')+1.0,1.2,1.2),s('g24'),0.12)
    # the turn: low drone (g27-g30)
    add(low,bowed([NOTE['D2']],e('g30')-s('g27')+2.0,1.6,2.0,800,3.5,0.0015),s('g27'),0.42)
    # Papa's handwriting: the series motif, gentle
    motif(s('g32')+0.1,['Bb3','A3','Eb4','D4'],1.25,0.36,0.85)
    # the question: near silence, then land on the bell
    add(low,low_sine_pad(NOTE['D2'],e('g35')-s('g34')+1.0,1.0,1.0),s('g34'),0.05)
    for nn,v in [('D3',0.5),('A3',0.45),('D4',0.45)]: add(dry,felt_piano(NOTE[nn],6.0,v),fbell,0.8)
    add(low,tanpura(0.0,dur-fbell+0.5,1.0),fbell,0.2)
    add(low,bowed([NOTE['D3'],NOTE['A3'],NOTE['D4']],dur-fbell+0.5,0.8,2.5,1500,4.0),fbell,0.16)
    motif(fbell+2.2,['Bb3','A3'],1.8,0.3,0.8)
    big=S.reverb_ir(3.2,1.0,5000,0.03,np.random.default_rng(5)); small=S.reverb_ir(1.2,0.35,3000,0.01,np.random.default_rng(6))
    st=S.reverb_st(dry,0.45,big)+S.reverb_st(low,0.22,small)
    st=st[:int(dur*SR)]; st=np.stack([S.filt(S.sos_hp(30),st[:,c]) for c in range(2)],1)
    return S.norm(st,-3)
