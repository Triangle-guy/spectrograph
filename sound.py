import numpy as np
import sounddevice as sd
import FFT2


# sd.default.latency = [0.0, 0.0]
# samplerate = sd.query_devices(sd.default.device, 'input')['default_samplerate']
# blocksize = 1024 * 2
# data = np.zeros([blocksize])
# fig, line, line_fft = FFT.format_figure(blocksize, samplerate, data)
#
#
# def callback(indata, frames, time, status):
#     FFT.update(fig, line, line_fft, indata[:, 0], frames)
#
#
# stream = sd.InputStream(channels=1, blocksize=blocksize, latency=0.0)
#
# with stream as s:
#     while True:
#         data, over = s.read(blocksize)
#         FFT.update(fig, line, line_fft, data[:, 0], blocksize)

sd.default.latency = [0.0, 0.0]
samplerate = sd.query_devices(sd.default.device, 'input')['default_samplerate']
blocksize = 1024 * 2
data = np.zeros([blocksize])
fig, line1, sl_x_sc, sl_y_sc = FFT2.format_figure(blocksize)

stream = sd.InputStream(channels=2, blocksize=blocksize, latency=0.0)

with stream as s:
    while True:
        data, over = s.read(blocksize)
        FFT2.update(fig, line1, data[:, 0], xscale=sl_x_sc.val, yscale=sl_y_sc.val)
        # Testing.update(fig, line2, data[:, 1])
