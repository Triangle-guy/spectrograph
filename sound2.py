import numpy as np
import sounddevice as sd
import FFT


sd.default.latency = [0.0, 0.0]
samplerate = sd.query_devices(sd.default.device, 'input')['default_samplerate']
blocksize = 1024 * 2
data = np.zeros([blocksize])
fig, line, line_fft = FFT.format_figure(blocksize, samplerate, data)
inbuf = np.zeros(blocksize)


def callback(indata, frames, time, status):
    global inbuf
    shift = len(indata[:, 0])
    inbuf = np.roll(inbuf, -shift)
    inbuf[-shift:] = indata[:, 0]

    FFT.update(fig, line, line_fft, inbuf, blocksize)


stream = sd.InputStream(channels=1, callback=callback, latency=0.0)

with stream as s:
    while True:
        sd.sleep(1000)
