import scipy.fftpack as fft
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import sounddevice as sd

# samplerate = sd.query_devices(sd.default.device, 'input')['default_samplerate']
# q = queue.Queue()
#
#
# def callback(indata, frames, time, status):
#     if status:
#         print(status, file=sys.stderr)
#     q.put(indata[:, 0])
#
#
# def update_plot(frame):
#     while True:
#         try:
#             data = q.get_nowait()
#         except queue.Empty:
#             break
#
#         yf = fft.rfft(data)
#         xf = fft.rfftfreq(len(data), 1./samplerate)
#         plt.cla()
#         plt.semilogx(xf, np.abs(yf), '#00ff1e')
#         plt.grid()
#
#
# plt.style.use('dark_background')
#
# stream = sd.InputStream(channels=1, samplerate=samplerate, callback=callback)
# ani = ani.FuncAnimation(plt.gcf(), update_plot)
# with stream:
#     plt.show()


samplerate = sd.query_devices(sd.default.device, 'input')['default_samplerate']
blocksize = 1024 * 2
data = np.zeros(blocksize)


def callback(indata, frames, time, status):
    global data
    data = indata[:, 0]


def update(frame):

    line.set_ydata(data)

    yf = fft.fft(data)
    line_fft.set_ydata(np.abs(yf) * 2 / blocksize)

    # print(data.shape)
    fig.canvas.draw()
    fig.canvas.flush_events()


# create matplotlib figure and axes
fig, (ax1, ax2) = plt.subplots(2, figsize=(15, 7))

# variable for plotting
x = np.arange(0, blocksize)
xf = np.linspace(0, samplerate, blocksize)

# create a line object with random data
line, = ax1.plot(x, data, '-', lw=2)

# create semilogx line for spectrum
line_fft, = ax2.semilogx(xf, data, '-', lw=2)

# format waveform axes
ax1.set_title('AUDIO WAVEFORM')
ax1.set_xlabel('samples')
ax1.set_ylabel('volume')
ax1.set_ylim(-1, 1)
ax1.set_xlim(0, blocksize)
plt.setp(ax1, xticks=[0, blocksize], yticks=np.linspace(-1, 1, num=5, endpoint=True))

# format spectrum axes
ax2.set_xlim(20, samplerate / 2)

# print(data.shape)
fig.canvas.draw()
ani = ani.FuncAnimation(fig, update)

stream = sd.InputStream(channels=1, samplerate=samplerate, callback=callback, blocksize=blocksize)
with stream:
    plt.show()
