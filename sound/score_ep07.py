# Episode 7 arrangement ("Papa Ki Aawaaz"): same instruments + motif (Bb3 A3 Eb4 D4), centre D.
# Arc: shop coda (cool) -> 2001 memory (warm motif) -> dusk walk -> the bell (bowed swell, 47) -> Bablu (light plucked felt piano, comic)
# -> music cuts to nothing before "Kabir... kisi se mat maangna" (+silence) -> Ma's bolt: heartbeat pulse -> the question -> land.
import numpy as np
import score as B
from score import SR, NOTE, tanpura, felt_piano, bowed, heartbeat, low_sine_pad, RNG
import synth as S
def score(tl):
    dur=float(tl['duration']); n=int((dur+1)*SR)
    dry=np.zeros(n,np.float32); low=np.zeros(n,np.float32)
    s=lambda i: B._L(tl,i,'start'); e=lambda i: B._L(tl,i,'end')
    fbell=tl.get('music_cues',{}).get('final_bell',e('g38')+0.3)
    def add(buf,x,t0,g=1.0):
        i=int(t0*SR); m=min(len(x),n-i)
        if m>0 and i>=0: buf[i:i+m]+=x[:m]*g
    def motif(t0,notes,sp=1.4,vel=0.5,g=1.0,dur=5.5):
        for k,nn in enumerate(notes): add(dry,felt_piano(NOTE[nn],dur,vel*(1-0.08*k)),t0+k*sp*(1+0.04*RNG.standard_normal()),g)
    # shop coda: thin drone
    add(low,low_sine_pad(NOTE['D2'],e('g06')+1.0,1.5,1.5),0.4,0.09)
    add(dry,felt_piano(NOTE['A3'],5.0,0.34),s('g06')+0.1,0.8)
    # Rukhsana's 2001 line: the series motif, warm (memory)
    motif(s('g08')+1.6,['Bb3','A3','Eb4','D4'],1.3,0.40,0.9)
    add(low,tanpura(0.0,e('g10')-s('g08')+1.5,1.0),s('g08'),0.18)
    # home, the last words, the bell: bowed swell, low pad; one high note on the plate
    add(low,bowed([NOTE['D3'],NOTE['Eb3']],e('g13')-s('g12')+1.2,1.4,1.0,1200,4.0,0.002),s('g12'),0.20)
    add(low,low_sine_pad(NOTE['D2'],e('g16')-s('g14')+1.5,2.0,1.5),s('g14'),0.13)
    add(dry,felt_piano(NOTE['Eb4'],6.0,0.40),s('g15')+0.3,0.9)
    add(dry,felt_piano(NOTE['D4'],6.0,0.34),s('g16')+0.6,0.8)
    # Bablu: light, plucky (short felt notes), D major-ish colour
    for k,(nn,dt) in enumerate([('D4',0.0),('F4',0.32),('A4',0.64),('G4',1.3),('F4',1.62),('D4',2.6),('A3',2.92),('D4',3.6)]):
        add(dry,felt_piano(NOTE[nn],1.2,0.30),s('g17')+0.2+dt,0.8)
    for k,(nn,dt) in enumerate([('A4',0.0),('G4',0.28),('F4',0.56),('D4',1.4),('F4',2.4),('G4',2.68),('A4',2.96)]):
        add(dry,felt_piano(NOTE[nn],1.2,0.28),s('g21')+0.1+dt,0.8)
    # Ma at the kitchen door: single held low note (she is not smiling)
    add(low,low_sine_pad(NOTE['D2'],e('g22')-s('g22')+1.0,0.8,1.0),s('g22'),0.10)
    # cut to nothing before "Kabir... kisi se mat maangna"; first-page line: motif fragment after the silence
    motif(s('g27')+0.3,['Bb3','A3'],1.6,0.32,0.8)
    # Ma bolts the door: heartbeat under her question and the dilemma
    add(low,heartbeat(s('g29')+1.8,e('g35')+0.3,1.1,0.95),s('g29')+1.8,0.75)
    add(low,bowed([NOTE['D2'],NOTE['A2']],e('g35')-s('g31')+1.5,1.6,1.8,900,3.5,0.002),s('g31'),0.22)
    # the question: near silence, then land on the bell
    add(low,low_sine_pad(NOTE['D2'],e('g38')-s('g36')+1.0,1.0,1.0),s('g36'),0.05)
    for nn,v in [('D3',0.5),('A3',0.45),('D4',0.45)]: add(dry,felt_piano(NOTE[nn],6.0,v),fbell,0.8)
    add(low,tanpura(0.0,dur-fbell+0.5,1.0),fbell,0.2)
    add(low,bowed([NOTE['D3'],NOTE['A3'],NOTE['D4']],dur-fbell+0.5,0.8,2.5,1500,4.0),fbell,0.16)
    motif(fbell+2.2,['Bb3','A3'],1.8,0.3,0.8)
    # hard mute window: from end of g23 to start of g27 (the voice line + its silence)
    a,b=int((e('g23')+0.05)*SR),int((s('g27')-0.1)*SR)
    big=S.reverb_ir(3.2,1.0,5000,0.03,np.random.default_rng(5)); small=S.reverb_ir(1.2,0.35,3000,0.01,np.random.default_rng(6))
    st=S.reverb_st(dry,0.45,big)+S.reverb_st(low,0.22,small)
    ramp=int(0.4*SR); env=np.ones(len(st),np.float32); env[a:b]=0; env[max(0,a-ramp):a]=np.linspace(1,0,min(ramp,a))
    env[b:b+ramp]=np.linspace(0,1,ramp)[:len(env[b:b+ramp])]; st=st*env[:,None]
    st=st[:int(dur*SR)]; st=np.stack([S.filt(S.sos_hp(30),st[:,c]) for c in range(2)],1)
    return S.norm(st,-3)
