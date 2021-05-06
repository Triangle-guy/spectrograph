import sys
import scipy.fftpack as fft
import scipy.signal as sig
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as wdgt
from commpy.filters import rcosfilter

import Cursor_class as Cc
import BlittingManager_class as BMc


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

    # creating figure and gridspec instance
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(43, 67)

    # connecting on_close event
    fig.canvas.mpl_connect('close_event', on_close)

    # creating and formatting axes for waveform
    ax1 = fig.add_subplot(gs[3:22, 3:34])
    plt.grid(lw=0.2)

    ax1.set_xlim(-1, 1)
    ax1.set_xticks(np.linspace(-1, 1, 11, endpoint=True))
    ax1.set_xticklabels([])

    ax1.set_ylim(-1, 1)
    ax1.set_yticks(np.linspace(-1, 1, 9, endpoint=True))
    ax1.set_yticklabels([])

    ax1.tick_params(axis='both', length=0)

    # creating and formatting axes for spectrum
    ax2 = fig.add_subplot(gs[23:42, 3:34])
    plt.grid(lw=0.2)

    ax2.set_xlim(0, 1)
    ax2.set_xticks(np.linspace(0, 1, 11, endpoint=True))
    ax2.set_xticklabels([])

    ax2.set_ylim(0, 0.2)
    ax2.set_yticks(np.linspace(0, 0.2, 9, endpoint=True))
    ax2.set_yticklabels([])

    ax2.tick_params(axis='both', length=0)

    #
    ax_t_1 = fig.add_subplot(gs[0:2, 3:10])
    ax_t_1.set_xticklabels([])
    ax_t_1.set_yticklabels([])
    ax_t_1.tick_params(axis='both', length=0)
    ax_t_1.text(0.05, 0.4, 'x=')

    ax_t_2 = fig.add_subplot(gs[0:2, 11:18])
    ax_t_2.set_xticklabels([])
    ax_t_2.set_yticklabels([])
    ax_t_2.tick_params(axis='both', length=0)

    ax_t_3 = fig.add_subplot(gs[0:2, 19:26])
    ax_t_3.set_xticklabels([])
    ax_t_3.set_yticklabels([])
    ax_t_3.tick_params(axis='both', length=0)

    ax_t_4 = fig.add_subplot(gs[0:2, 27:34])
    ax_t_4.set_xticklabels([])
    ax_t_4.set_yticklabels([])
    ax_t_4.tick_params(axis='both', length=0)

    # creating X-scale slider
    ax_sl_x_sc = fig.add_subplot(gs[3:4, 35:50])
    ax_sl_x_sc.set_title('X-scale', {'fontsize': 10})
    sl_x_sc = wdgt.Slider(ax_sl_x_sc, '', 0.01, 1.0, 0.5, facecolor='0.95')

    # creating X-shift slider
    ax_sl_x_sh = fig.add_subplot(gs[5:6, 35:50])
    ax_sl_x_sh.set_title('X-shift', {'fontsize': 10})
    sl_x_sh = wdgt.Slider(ax_sl_x_sh, '', -1.0, 1.0, 0.0, facecolor='0.95')

    # creating on/off button for channel 1
    ax_b_on_off_1 = fig.add_subplot(gs[18:19, 36:37])
    b_on_off_1 = wdgt.Button(ax_b_on_off_1, '1', None, '#f4bb32', '#efc35b')
    b_on_off_1.label.set_color('0.0')

    # making on/off button for channel 1 change color on click
    def button_change_1(event):
        if b_on_off_1.color == '#f4bb32':
            b_on_off_1.color = '0.85'
        else:
            b_on_off_1.color = '#f4bb32'

    b_on_off_1.on_clicked(button_change_1)

    # creating Y-scale slider for channel 1
    ax_sl_y_sc_1 = fig.add_subplot(gs[15:22, 39:40])
    ax_sl_y_sc_1.set_title('Y-scale', {'fontsize': 8})
    sl_y_sc_1 = wdgt.Slider(ax_sl_y_sc_1, '', 0.2, 5.0, 1.0, orientation='vertical',
                            valstep=[0.2, 0.25, 1 / 3, 0.5, 1.0, 2.0, 3.0, 4.0, 5.0], facecolor='#f4bb32')

    # creating Y-shift slider for channel 1
    ax_sl_y_sh_1 = fig.add_subplot(gs[15:22, 41:42])
    ax_sl_y_sh_1.set_title('Y-shift', {'fontsize': 8})
    sl_y_sh_1 = wdgt.Slider(ax_sl_y_sh_1, '', -1.0, 1.0, 0.0, orientation='vertical', facecolor='#f4bb32')

    # creating on/off button for channel 2
    ax_b_on_off_2 = fig.add_subplot(gs[18:19, 44:45])
    b_on_off_2 = wdgt.Button(ax_b_on_off_2, '2', None, '0.85', '#9fd1ac')
    b_on_off_2.label.set_color('0.0')

    # making on/off button for channel 2 change color on click
    def button_change_2(event):
        if b_on_off_2.color == '#81b78f':
            b_on_off_2.color = '0.85'
        else:
            b_on_off_2.color = '#81b78f'

    b_on_off_2.on_clicked(button_change_2)

    # creating Y-scale slider for channel 2
    ax_sl_y_sc_2 = fig.add_subplot(gs[15:22, 47:48])
    ax_sl_y_sc_2.set_title('Y-scale', {'fontsize': 8})
    sl_y_sc_2 = wdgt.Slider(ax_sl_y_sc_2, '', 0.2, 5.0, 1.0, orientation='vertical',
                            valstep=[0.2, 0.25, 1 / 3, 0.5, 1.0, 2.0, 3.0, 4.0, 5.0], facecolor='#81b78f')

    # creating Y-shift slider for channel 2
    ax_sl_y_sh_2 = fig.add_subplot(gs[15:22, 49:50])
    ax_sl_y_sh_2.set_title('Y-shift', {'fontsize': 8})
    sl_y_sh_2 = wdgt.Slider(ax_sl_y_sh_2, '', -1.0, 1.0, 0.0, orientation='vertical', facecolor='#81b78f')

    # creating on/off button for channel 3
    ax_b_on_off_3 = fig.add_subplot(gs[18:19, 52:53])
    b_on_off_3 = wdgt.Button(ax_b_on_off_3, '3', None, '0.85', '#89a8db')
    b_on_off_3.label.set_color('0.0')

    # making on/off button for channel 3 change color on click
    def button_change_3(event):
        if b_on_off_3.color == '#6590d8':
            b_on_off_3.color = '0.85'
        else:
            b_on_off_3.color = '#6590d8'

    b_on_off_3.on_clicked(button_change_3)

    # creating Y-scale slider for channel 3
    ax_sl_y_sc_3 = fig.add_subplot(gs[15:22, 55:56])
    ax_sl_y_sc_3.set_title('Y-scale', {'fontsize': 8})
    sl_y_sc_3 = wdgt.Slider(ax_sl_y_sc_3, '', 0.2, 5.0, 1.0, orientation='vertical',
                            valstep=[0.2, 0.25, 1 / 3, 0.5, 1.0, 2.0, 3.0, 4.0, 5.0], facecolor='#6590d8')

    # creating Y-shift slider for channel 3
    ax_sl_y_sh_3 = fig.add_subplot(gs[15:22, 57:58])
    ax_sl_y_sh_3.set_title('Y-shift', {'fontsize': 8})
    sl_y_sh_3 = wdgt.Slider(ax_sl_y_sh_3, '', -1.0, 1.0, 0.0, orientation='vertical', facecolor='#6590d8')

    # creating on/off button for channel 4
    ax_b_on_off_4 = fig.add_subplot(gs[18:19, 60:61])
    b_on_off_4 = wdgt.Button(ax_b_on_off_4, '4', None, '0.85', '#f5b8d8')
    b_on_off_4.label.set_color('0.0')

    # making on/off button for channel 4 change color on click
    def button_change_4(event):
        if b_on_off_4.color == '#de8fb9':
            b_on_off_4.color = '0.85'
        else:
            b_on_off_4.color = '#de8fb9'

    b_on_off_4.on_clicked(button_change_4)

    # creating Y-scale slider for channel 4
    ax_sl_y_sc_4 = fig.add_subplot(gs[15:22, 63:64])
    ax_sl_y_sc_4.set_title('Y-scale', {'fontsize': 8})
    sl_y_sc_4 = wdgt.Slider(ax_sl_y_sc_4, '', 0.2, 5.0, 1.0, orientation='vertical',
                            valstep=[0.2, 0.25, 1 / 3, 0.5, 1.0, 2.0, 3.0, 4.0, 5.0], facecolor='#de8fb9')

    # creating Y-shift slider for channel 4
    ax_sl_y_sh_4 = fig.add_subplot(gs[15:22, 65:66])
    ax_sl_y_sh_4.set_title('Y-shift', {'fontsize': 8})
    sl_y_sh_4 = wdgt.Slider(ax_sl_y_sh_4, '', -1.0, 1.0, 0.0, orientation='vertical', facecolor='#de8fb9')

    # creating on/off button spectrum
    ax_b_on_off_s = fig.add_subplot(gs[24:26, 35:40])
    b_on_off_s = wdgt.Button(ax_b_on_off_s, 'Spectrum', None, '0.85', 'w')
    b_on_off_s.label.set_color('0.0')

    # making on/off button for spectrum change color on click
    def button_change_s(event):
        if b_on_off_s.color == '0.95':
            b_on_off_s.color = '0.85'
        else:
            b_on_off_s.color = '0.95'

    b_on_off_s.on_clicked(button_change_s)

    # creating range slider for spectrum
    ax_r_sl = fig.add_subplot(gs[28:29, 35:50])
    ax_r_sl.set_title('Frequency range, Hz', fontsize=10)
    r_sl = wdgt.RangeSlider(ax_r_sl, '', 0.0, 22050.0, facecolor='0.95')
    r_sl.set_val([0.0, 22050.0])

    def change_size(event):
        ax2.set_xlim(r_sl.val[0] / 22050.0, r_sl.val[1] / 22050.0)
        ax2.set_xticks(np.linspace(r_sl.val[0] / 22050.0, r_sl.val[1] / 22050.0, 11, endpoint=True))

    r_sl.on_changed(change_size)

    # creating on/off button for cursors
    ax_b_on_off_cur = fig.add_subplot(gs[8:10, 35:40])
    b_on_off_cur = wdgt.Button(ax_b_on_off_cur, 'Cursors', None, '0.85', '0.95')
    b_on_off_cur.label.set_color('0.0')

    # making on/off button for cursors change color on click
    def button_change_cur(event):
        if b_on_off_cur.color == '#4cd147':
            b_on_off_cur.color = '0.85'
            b_on_off_cur.hovercolor = '0.95'
        else:
            b_on_off_cur.color = '#4cd147'
            b_on_off_cur.hovercolor = '#2fff27'

    b_on_off_cur.on_clicked(button_change_cur)

    # making reset button
    ax_b_reset = fig.add_subplot(gs[3:5, 53:58])
    b_reset = wdgt.Button(ax_b_reset, 'Reset', None, '#f96b6b', '#fa9494')

    # making reset button reset all sliders' and cursors' positions
    def reset(event):
        sl_x_sc.reset()
        sl_x_sh.reset()
        sl_y_sc_1.reset()
        sl_y_sh_1.reset()
        sl_y_sc_2.reset()
        sl_y_sh_2.reset()
        sl_y_sc_3.reset()
        sl_y_sh_3.reset()
        sl_y_sc_4.reset()
        sl_y_sh_4.reset()
        r_sl.set_val([0.0, 22050.0])
        xcur1.line.set_xdata([-0.5, -0.5])
        xcur2.line.set_xdata([0.5, 0.5])
        ycur1.line.set_ydata([-0.5, -0.5])
        ycur2.line.set_ydata([0.5, 0.5])

    b_reset.on_clicked(reset)

    # making single frame button
    ax_b_single = fig.add_subplot(gs[3:5, 61:66])
    b_single = wdgt.Button(ax_b_single, 'Single', None, '0.85', 'w')
    b_single.label.set_color('0.0')

    # making single frame button work

    # making run/stop button
    ax_b_run_stop = fig.add_subplot(gs[6:8, 61:66])
    b_run_stop = wdgt.Button(ax_b_run_stop, 'Run/Stop', None, '0.85', 'w')
    b_run_stop.label.set_color('0.0')

    # making run/stop button work

    # creating starter plots for all channels
    dot, = ax1.plot([0], [0], '')
    line1, = ax1.plot(np.linspace(-1, 1, blocksize), np.zeros(blocksize), '#f4bb32')
    line2, = ax1.plot(np.linspace(-1, 1, blocksize), np.zeros(blocksize), '#81b78f')
    line3, = ax1.plot(np.linspace(-1, 1, blocksize), np.zeros(blocksize), '#6590d8')
    line4, = ax1.plot(np.linspace(-1, 1, blocksize), np.zeros(blocksize), '#de8fb9')
    line2.set_linestyle('')
    line3.set_linestyle('')
    line4.set_linestyle('')
    line_fft_1, = ax2.plot(np.linspace(0, 1, blocksize), np.zeros(blocksize), '#f4bb32')
    line_fft_2, = ax2.plot(np.linspace(0, 1, blocksize), np.zeros(blocksize), '#81b78f')
    line_fft_3, = ax2.plot(np.linspace(0, 1, blocksize), np.zeros(blocksize), '#6590d8')
    line_fft_4, = ax2.plot(np.linspace(0, 1, blocksize), np.zeros(blocksize), '#de8fb9')
    line_fft_1.set_linestyle('')
    line_fft_2.set_linestyle('')
    line_fft_3.set_linestyle('')
    line_fft_4.set_linestyle('')

    xcur1 = Cc.Cursor(ax1.axvline(-0.5, c='r', ls=''), b_on_off_cur)
    xcur2 = Cc.Cursor(ax1.axvline(0.5, c='r', ls=''), b_on_off_cur)
    ycur1 = Cc.Cursor(ax1.axhline(-0.5, c='r', ls=''), b_on_off_cur)
    ycur2 = Cc.Cursor(ax1.axhline(0.5, c='r', ls=''), b_on_off_cur)

    # making blitting manager
    bm = BMc.BlitManager(fig.canvas,
                         [line1, line2, line3, line4, line_fft_1, line_fft_2, line_fft_3, line_fft_4,
                          xcur1.line, xcur2.line, ycur1.line, ycur2.line])

    # making plot visible
    plt.show(block=False)
    plt.pause(.1)

    return fig, sl_x_sc, sl_x_sh, \
           b_on_off_1, line1, sl_y_sc_1, sl_y_sh_1, \
           b_on_off_2, line2, sl_y_sc_2, sl_y_sh_2, \
           b_on_off_s, line_fft_1, line_fft_2, r_sl, dot, \
           xcur1, xcur2, ycur1, ycur2, b_on_off_cur, \
           b_reset, bm


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
