import scipy.fftpack as fft
import numpy as np
import matplotlib.pyplot as plt


def format_figure(blocksize, samplerate):
    # create matplotlib figure and axes
    fig, (ax1, ax2) = plt.subplots(2, figsize=(15, 7))

    # variable for plotting
    x = np.arange(0, blocksize)
    xf = np.linspace(0, samplerate, blocksize)

    # create a line object with random data
    line, = ax1.plot(x)

    # create semilogx line for spectrum
    line_fft, = ax2.semilogx(xf)

    # format waveform axes
    ax1.set_title('AUDIO WAVEFORM')
    ax1.set_xlabel('samples')
    ax1.set_ylabel('volume')
    ax1.set_ylim(-1, 1)
    ax1.set_xlim(0, blocksize)
    plt.setp(ax1, xticks=[0, blocksize], yticks=np.linspace(-1, 1, num=5, endpoint=True))

    # format spectrum axes
    ax2.set_xlim(20, samplerate / 2)

    return fig, line, line_fft


def update(fig, line, line_fft, data, blocksize):

    line.set_ydata(data)

    yf = fft.fft(data)
    line_fft.set_ydata(np.abs(yf[0:blocksize]) * 2 / blocksize)

    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.show()
