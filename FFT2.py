import scipy.fftpack as fft
import numpy as np
import matplotlib.pyplot as plt
import sound2

# create matplotlib figure and axes
fig, (ax1, ax2) = plt.subplots(2, figsize=(15, 7))

# variable for plotting
x = np.arange(0, sound2.blocksize)
xf = np.linspace(0, sound2.samplerate, sound2.blocksize)

# create a line object with random data
line, = ax1.plot(x)

# create semilogx line for spectrum
line_fft, = ax2.semilogx(xf, sound2.data, '-', lw=2)

# format waveform axes
ax1.set_title('AUDIO WAVEFORM')
ax1.set_xlabel('samples')
ax1.set_ylabel('volume')
ax1.set_ylim(-1, 1)
ax1.set_xlim(0, sound2.blocksize)
plt.setp(ax1, xticks=[0, sound2.blocksize], yticks=np.linspace(-1, 1, num=5, endpoint=True))

# format spectrum axes
ax2.set_xlim(20, sound2.samplerate / 2)
