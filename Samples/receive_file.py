import time, math, sys
import scipy.signal as sig
import scipy.fftpack as fft
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
import sounddevice as sd


class Filter(object):
    def __init__(self, b, a=[1], init=[]):
        self.b = b
        self.a = a
        self.state = sig.lfiltic(b, a, [], init)

    def __call__(self, x):
        y, self.state = sig.lfilter(self.b, self.a, x, zi=self.state)
        return y


diff = Filter([1, -1])


def fix_diff(x):
    x[x > math.pi] -= 2*math.pi
    x[x < -math.pi] += 2*math.pi
    return x


with sd.InputStream(channels=1) as ss:
    f = sf.SoundFile('out.wav', channels=ss.channels, mode='w', samplerate=int(ss.samplerate))
    fir_music = Filter(sig.firls(101, [0, 3400, 4000, ss.samplerate/2], [1, 1, 0, 0], nyq=ss.samplerate/2), [1])
    N = 2**14
    while True:
        x, overflowed = ss.read(N)
        if overflowed:
            print('Input overflowed')
        f.write(x)
