import numpy as np
import pandas as pd
import simpleaudio as sa
from audio2numpy import open_audio

#reduce voice to range between 250 Hz and 4 kHz

def mk_mid(inp,sampling_rate,mid_range=[250,4000]):
    t = np.linspace(0,1,sampling_rate) 
    T=int(np.ceil(len(inp)/sampling_rate))
    t=np.tile(t,T)[:len(inp)]
    low_bound = np.sin(mid_range[0] * t * 2 * np.pi)
    up_bound = np.sin(mid_range[1] * t * 2 * np.pi)
    low_ = low_bound * (2**15 - 1) / np.max(np.abs(low_bound))
    up_ = up_bound * (2**15 - 1) / np.max(np.abs(up_bound))
    sig = inp * (2**15 - 1) / np.max(np.abs(inp))
    zw=[]
    nn=-1
    for i in sig:
        nn+=1
        if i > low_[nn]:
            if i < up_[nn]:
                zw.append(i)
            else:
                zw.append(0)
        else:
            zw.append(0)
    return np.asarray(zw).astype(np.int16)

#apply ring modulation with 30 Hz carrier frequency

def ring_mod(inp,samp_freq,carr_freq=30):
    seconds = int(np.ceil(len(inp)/samp_freq))
    t = np.linspace(0, seconds, seconds * samp_freq, False)
    note = np.sin(carr_freq * t[:len(inp)] * 2 * np.pi)
    audio = note * (2**15 - 1) / np.max(np.abs(note))
    zw=[]
    nn=-1
    for i in inp:
        nn+=1
        note1 = np.sin((i - audio[nn]) * t[nn] * 2 * np.pi)
        note2 = np.sin((i + audio[nn]) * t[nn] * 2 * np.pi)
        zzw = (note1 + note2)/2
        zw.append(zzw * i + i)
    output = np.asarray(zw).astype(np.int16)
    return output

#play result with simpleaudio
  
def dalek_voice(inp):
    signal, sampling_rate = open_audio(inp)
    prc = mk_mid(signal,sampling_rate)
    voice = ring_mod(prc,sampling_rate,30)
    sa.play_buffer(voice, 1, 2, sampling_rate)
