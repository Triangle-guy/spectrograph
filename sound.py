import numpy as np
import sounddevice as sd
import FFT

samplerate = sd.query_devices(sd.default.device, 'input')['default_samplerate']
blocksize = 1024 * 2
data = np.zeros([blocksize, 2])
fig, line, line_fft = FFT.format_figure(blocksize, samplerate, data)


stream = sd.InputStream(channels=1, samplerate=samplerate, blocksize=blocksize)

with stream as s:
    while True:
        data, over = s.read(blocksize)
        FFT.update(fig, line, line_fft, data[:, 0], blocksize)
