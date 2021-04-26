import scipy.fftpack as fft
import numpy as np
import matplotlib.pyplot as plt
from commpy.filters import rcosfilter as rc


def format_figure(blocksize, samplerate, data):
    scale = 4

    # create matplotlib figure and axes
    fig, (ax1, ax2) = plt.subplots(2, figsize=(15, 7))

    # variable for plotting
    x = np.arange(0, blocksize)
    xf = np.linspace(0, samplerate, blocksize)

    # create a line object with random data
    line, = ax1.plot(x)

    # create semilogx line for spectrum
    line_fft, = ax2.semilogx(xf, data, '-', lw=2)

    # format waveform axes
    ax1.set_title('AUDIO WAVEFORM')
    ax1.set_xlabel('samples')
    ax1.set_ylabel('volume')
    ax1.set_ylim(-1 / scale, 1 / scale)
    ax1.set_xlim(0, blocksize)
    plt.setp(ax1, xticks=[0, blocksize], yticks=np.linspace(-1 / scale, 1 / scale, num=5, endpoint=True))

    # format spectrum axes
    ax2.set_xlim(20, samplerate / 2)
    ax2.set_ylim(0, 0.2 / scale)

    plt.show(block=False)

    return fig, line, line_fft


def interpolate(data, n):

    interdata = np.zeros(len(data) * n)
    interdata[:: n] = data

    return


def update(fig, line, line_fft, data, blocksize):

    if blocksize != 0:
        line.set_ydata(data)

        yf = fft.fft(data)
        line_fft.set_ydata(np.abs(yf[0:blocksize]) * 2 / blocksize)

        fig.canvas.draw()
        fig.canvas.flush_events()
