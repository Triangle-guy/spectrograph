import numpy as np
import sounddevice as sd
import FFT


sd.default.latency = [0.0, 0.0]
samplerate = sd.query_devices(sd.default.device, 'input')['default_samplerate']
blocksize = 1024 * 2
data = np.zeros([blocksize])
fig, line, line_fft = FFT.format_figure(blocksize, samplerate, data)


def callback(indata, frames, time, status):
    FFT.update(fig, line, line_fft, indata[:, 0], frames)


stream = sd.InputStream(channels=1, blocksize=blocksize, latency=0.0)

with stream as s:
    while True:
        block = s.read_available
        data, over = s.read(block)
        FFT.update(fig, line, line_fft, data[:, 0], block)
