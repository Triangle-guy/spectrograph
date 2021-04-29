import sys
import scipy.signal as sig
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as wdgt
from commpy.filters import rcosfilter


def on_close(event):
    sys.exit()


def interpolate(data, n):

    interdata = np.zeros(len(data) * n)
    interdata[:: n] = data

    rc = rcosfilter(len(interdata), 1, 1, n)[1]
    interdata = sig.lfilter(rc, np.ones(len(interdata)), interdata)

    return interdata


def format_figure(blocksize):
    plt.style.use('dark_background')

    fig, ax = plt.subplots()

    fig.canvas.mpl_connect('close_event', on_close)

    line1, = ax.plot(np.linspace(-1, 1, blocksize), np.zeros(blocksize), '#f4bb32')

    # line2, = ax.plot(np.linspace(-1, 1, blocksize), np.zeros(blocksize), '#81b78f')

    ax.set_box_aspect(10/16)
    ax.set_aspect(10/16)

    ax.set_xlim(-1, 1)
    ax.set_xticks(np.linspace(-1, 1, 11, endpoint=True))
    ax.set_xticklabels([])

    ax.set_ylim(-1, 1)
    ax.set_yticks(np.linspace(-1, 1, 9, endpoint=True))
    ax.set_yticklabels([])

    ax.tick_params(axis='both', length=0)

    plt.grid(lw=0.2)
    plt.show(block=False)

    ax_sl_x_sc = plt.axes([0.15, 0.10, 0.65, 0.03])
    sl_x_sc = wdgt.Slider(ax_sl_x_sc, 'X scale', 0.01, 1.0, valinit=0.5)

    ax_sl_y_sc = plt.axes([0.15, 0.05, 0.65, 0.03])
    sl_y_sc = wdgt.Slider(ax_sl_y_sc, 'Y scale', 0.2, 5.0, valinit=1.0)

    return fig, line1, sl_x_sc, sl_y_sc


def update(fig, line, data, xscale=1.0, yscale=1.0, xshift=0.0, yshift=0.0):

    xdata = (np.linspace(-1, 1, len(data)) / xscale) - xshift
    line.set_data(xdata, (data * yscale) + yshift)

    fig.canvas.draw()
    fig.canvas.flush_events()
