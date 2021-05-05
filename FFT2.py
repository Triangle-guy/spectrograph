import sys
import scipy.fftpack as fft
import scipy.signal as sig
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as wdgt
from commpy.filters import rcosfilter


class Cursor:
    def __init__(self, line):
        self.line = line
        self.press = None
        if self.line.get_xdata()[0] == self.line.get_xdata()[1]:
            self.orient = 'v'
        elif self.line.get_ydata()[0] == self.line.get_ydata()[1]:
            self.orient = 'h'
        self.line.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.line.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.line.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        if event.inaxes != self.line.axes:
            return
        if event.button != 1:
            return

        if self.orient == 'v':
            if np.abs(event.xdata - self.line.get_xdata()[0]) > 0.05:
                return
            self.press = self.line.get_xdata()[0], event.xdata
        elif self.orient == 'h':
            if np.abs(event.ydata - self.line.get_ydata()[0]) > 0.05:
                return
            self.press = self.line.get_ydata()[0], event.ydata

    def on_motion(self, event):
        if self.press is None or event.inaxes != self.line.axes:
            return
        if self.orient == 'v':
            x0, xpress = self.press
            dx = event.xdata - xpress
            self.line.set_xdata([x0 + dx, x0 + dx])

            self.line.figure.canvas.draw()
        elif self.orient == 'h':
            y0, ypress = self.press
            dy = event.ydata - ypress
            self.line.set_ydata([y0 + dy, y0 + dy])

            self.line.figure.canvas.draw()

    def on_release(self, event):
        self.press = None
        self.line.figure.canvas.draw()


def on_close(event):
    sys.exit()


def interpolate(data, n):

    interdata = np.zeros(len(data) * n)
    interdata[:: n] = data

    rc = rcosfilter(len(interdata), 1, 1, n)[1]
    interdata = sig.lfilter(rc, np.ones(len(interdata)), interdata)

    return interdata


def format_figure(blocksize):
    # choosing style
    plt.style.use('dark_background')

    # creating figure and gridspec
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(40, 64)

    # connecting on_close event
    fig.canvas.mpl_connect('close_event', on_close)

    # creating and formatting axes for waveform
    ax1 = fig.add_subplot(gs[0:19, 0:31])
    plt.grid(lw=0.2)

    ax1.set_xlim(-1, 1)
    ax1.set_xticks(np.linspace(-1, 1, 11, endpoint=True))
    ax1.set_xticklabels([])

    ax1.set_ylim(-1, 1)
    ax1.set_yticks(np.linspace(-1, 1, 9, endpoint=True))
    ax1.set_yticklabels([])

    ax1.tick_params(axis='both', length=0)

    # creating and formatting axes for spectrum
    ax2 = fig.add_subplot(gs[20:39, 0:31])
    plt.grid(lw=0.2)

    ax2.set_xlim(0, 1)
    ax2.set_xticks(np.linspace(0, 1, 11, endpoint=True))
    ax2.set_xticklabels([])

    ax2.set_ylim(0, 0.2)
    ax2.set_yticks(np.linspace(0, 0.2, 9, endpoint=True))
    ax2.set_yticklabels([])

    ax2.tick_params(axis='both', length=0)

    # creating X-scale slider
    ax_sl_x_sc = fig.add_subplot(gs[0:1, 32:47])
    ax_sl_x_sc.set_title('X-scale', {'fontsize': 10})
    sl_x_sc = wdgt.Slider(ax_sl_x_sc, '', 0.01, 1.0, 0.5, facecolor='0.95')

    # creating X-shift slider
    ax_sl_x_sh = fig.add_subplot(gs[2:3, 32:47])
    ax_sl_x_sh.set_title('X-shift', {'fontsize': 10})
    sl_x_sh = wdgt.Slider(ax_sl_x_sh, '', -1.0, 1.0, 0.0, facecolor='0.95')

    # creating on/off button for channel 1
    ax_b_on_off_1 = fig.add_subplot(gs[15:16, 33:34])
    b_on_off_1 = wdgt.Button(ax_b_on_off_1, '1', None, '#f4bb32', '#efc35b')
    b_on_off_1.label.set_color('#000000')

    # making on/off button for channel 1 change color on click
    def button_change_1(event):
        if b_on_off_1.color == '#f4bb32':
            b_on_off_1.color = '0.85'
        else:
            b_on_off_1.color = '#f4bb32'

    b_on_off_1.on_clicked(button_change_1)

    # creating Y-scale slider for channel 1
    ax_sl_y_sc_1 = fig.add_subplot(gs[12:19, 36:37])
    sl_y_sc_1 = wdgt.Slider(ax_sl_y_sc_1, 'Y-scale', 0.2, 5.0, 1.0, orientation='vertical',
                            valstep=[0.2, 0.25, 1 / 3, 0.5, 1.0, 2.0, 3.0, 4.0, 5.0], facecolor='#f4bb32')

    # creating Y-shift slider for channel 1
    ax_sl_y_sh_1 = fig.add_subplot(gs[12:19, 38:39])
    sl_y_sh_1 = wdgt.Slider(ax_sl_y_sh_1, 'Y-shift', -1.0, 1.0, 0.0, orientation='vertical',
                            facecolor='#f4bb32')

    # creating on/off button for channel 2
    ax_b_on_off_2 = fig.add_subplot(gs[15:16, 41:42])
    b_on_off_2 = wdgt.Button(ax_b_on_off_2, '2', None, '0.85', '#9fd1ac')
    b_on_off_2.label.set_color('#000000')

    # making on/off button for channel 2 change color on click
    def button_change_2(event):
        if b_on_off_2.color == '#81b78f':
            b_on_off_2.color = '0.85'
        else:
            b_on_off_2.color = '#81b78f'

    b_on_off_2.on_clicked(button_change_2)

    # creating Y-scale slider for channel 2
    ax_sl_y_sc_2 = fig.add_subplot(gs[12:19, 44:45])
    sl_y_sc_2 = wdgt.Slider(ax_sl_y_sc_2, 'Y-scale', 0.2, 5.0, 1.0, orientation='vertical',
                            valstep=[0.2, 0.25, 1 / 3, 0.5, 1.0, 2.0, 3.0, 4.0, 5.0], facecolor='#81b78f')

    # creating Y-shift slider for channel 1
    ax_sl_y_sh_2 = fig.add_subplot(gs[12:19, 46:47])
    sl_y_sh_2 = wdgt.Slider(ax_sl_y_sh_2, 'Y-shift', -1.0, 1.0, 0.0, orientation='vertical',
                            facecolor='#81b78f')

    # creating range slider for spectrum
    ax_r_sl = fig.add_subplot(gs[29:30, 32:47])
    r_sl = wdgt.RangeSlider(ax_r_sl, '', 0.0, 22050.0)
    r_sl.set_val([0.0, 22050.0])

    def change_size(event):
        ax2.set_xlim(r_sl.val[0] / 22050.0, r_sl.val[1] / 22050.0)
        ax2.set_xticks(np.linspace(r_sl.val[0] / 22050.0, r_sl.val[1] / 22050.0, 11, endpoint=True))

    r_sl.on_changed(change_size)

    # creating starter plots for all channels
    dot, = ax1.plot([0], [0], '')
    line1, = ax1.plot(np.linspace(-1, 1, blocksize), np.zeros(blocksize), '#f4bb32')
    line2, = ax1.plot(np.linspace(-1, 1, blocksize), np.zeros(blocksize), '#81b78f')
    line_fft_1, = ax2.plot(np.linspace(0, 1, blocksize), np.zeros(blocksize), '#f4bb32')
    line_fft_2, = ax2.plot(np.linspace(0, 1, blocksize), np.zeros(blocksize), '#81b78f')

    xcur1_line = ax1.axvline(-0.5, c='r', ls='--')
    xcur1 = Cursor(xcur1_line)
    xcur2_line = ax1.axvline(0.5, c='r', ls='--')
    xcur2 = Cursor(xcur2_line)
    ycur1_line = ax1.axhline(-0.5, c='r', ls='--')
    ycur1 = Cursor(ycur1_line)
    ycur2_line = ax1.axhline(0.5, c='r', ls='--')
    ycur2 = Cursor(ycur2_line)

    # making plot visible
    plt.show(block=False)

    return fig, sl_x_sc, sl_x_sh, \
           b_on_off_1, line1, sl_y_sc_1, sl_y_sh_1, \
           b_on_off_2, line2, sl_y_sc_2, sl_y_sh_2, \
           line_fft_1, line_fft_2, r_sl, dot, \
           xcur1, xcur2, ycur1, ycur2


def update(fig, line, data, xscale=1.0, yscale=1.0, xshift=0.0, yshift=0.0):

    xdata = (np.linspace(-1, 1, len(data)) / xscale) - xshift
    line.set_data(xdata, (data * yscale) + yshift)

    fig.canvas.draw()
    fig.canvas.flush_events()


def update_fft(fig, line_fft, data):

    ydata = fft.fft(data)[:len(data) // 2]
    xdata = np.linspace(0, 1, len(ydata))

    line_fft.set_data(xdata, np.abs(ydata) * 2 / len(ydata))

    fig.canvas.draw()
    fig.canvas.flush_events()


def do_nothing(fig, dot):
    dot.set_data([0], [0])

    fig.canvas.draw()
    fig.canvas.flush_events()
