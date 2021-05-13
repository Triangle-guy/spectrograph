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
    fig = plt.figure(figsize=(16, 9))
    gs = fig.add_gridspec(90, 160)

    # connecting on_close event
    fig.canvas.mpl_connect('close_event', on_close)

    # creating and formatting axes for waveform
    ax1 = fig.add_subplot(gs[5:44, 0:63])
    plt.grid(lw=0.2)

    ax1.set_xlim(-1, 1)
    ax1.set_xticks(np.linspace(-1, 1, 11, endpoint=True))
    ax1.set_xticklabels([])

    ax1.set_ylim(-1, 1)
    ax1.set_yticks(np.linspace(-1, 1, 9, endpoint=True))
    ax1.set_yticklabels([])

    ax1.tick_params(axis='both', length=0)

    # creating and formatting axes for spectrum
    ax2 = fig.add_subplot(gs[45:84, 0:63])
    plt.grid(lw=0.2)

    ax2.set_xlim(0, 1)
    ax2.set_xticks(np.linspace(0, 1, 11, endpoint=True))
    ax2.set_xticklabels([])

    ax2.set_ylim(0, 0.2)
    ax2.set_yticks(np.linspace(0, 0.2, 9, endpoint=True))
    ax2.set_yticklabels([])

    ax2.tick_params(axis='both', length=0)

    #
    ax_t_1 = fig.add_subplot(gs[0:4, 8:23])
    ax_t_1.set_xticklabels([])
    ax_t_1.set_yticklabels([])
    ax_t_1.tick_params(axis='both', length=0)
    ax_t_1.text(0.05, 0.4, 'x=')

    ax_t_2 = fig.add_subplot(gs[0:4, 40:55])
    ax_t_2.set_xticklabels([])
    ax_t_2.set_yticklabels([])
    ax_t_2.tick_params(axis='both', length=0)

    ax_t_3 = fig.add_subplot(gs[85:89, 8:23])
    ax_t_3.set_xticklabels([])
    ax_t_3.set_yticklabels([])
    ax_t_3.tick_params(axis='both', length=0)

    ax_t_4 = fig.add_subplot(gs[85:89, 40:55])
    ax_t_4.set_xticklabels([])
    ax_t_4.set_yticklabels([])
    ax_t_4.tick_params(axis='both', length=0)

    # creating X-scale slider
    ax_sl_x_sc = fig.add_subplot(gs[54:56, 66:97])
    ax_sl_x_sc.set_title('X-scale', {'fontsize': 10})
    sl_x_sc = wdgt.Slider(ax_sl_x_sc, '', 0.01, 1.0, 0.5, facecolor='0.95')

    # creating X-shift slider
    ax_sl_x_sh = fig.add_subplot(gs[62:64, 66:97])
    ax_sl_x_sh.set_title('X-shift', {'fontsize': 10})
    sl_x_sh = wdgt.Slider(ax_sl_x_sh, '', -1.0, 1.0, 0.0, facecolor='0.95')

    # creating on/off button for channel 1
    ax_b_on_off_1 = fig.add_subplot(gs[47:50, 91:94])
    b_on_off_1 = wdgt.Button(ax_b_on_off_1, '1', None, '#f4bb32', '#efc35b')
    b_on_off_1.label.set_color('0')

    # making on/off button for channel 1 change color on click
    def button_change_1(event):
        if b_on_off_1.color == '#f4bb32':
            b_on_off_1.color = '0.85'
            line1.set_linestyle('')
            line_fft_1.set_linestyle('')
        else:
            b_on_off_1.color = '#f4bb32'
            line1.set_linestyle('-')
            if b_on_off_s.color == '0.95':
                line_fft_1.set_linestyle('-')

    b_on_off_1.on_clicked(button_change_1)

    # creating Y-scale slider for channel 1
    ax_sl_y_sc_1 = fig.add_subplot(gs[17:40, 86:89])
    ax_sl_y_sc_1.set_title('Y-scale', {'fontsize': 10})
    sl_y_sc_1 = wdgt.Slider(ax_sl_y_sc_1, '', 0.2, 5.0, 1.0, orientation='vertical',
                            valstep=[0.2, 0.25, 1 / 3, 0.5, 1.0, 2.0, 3.0, 4.0, 5.0], facecolor='#f4bb32')

    # creating Y-shift slider for channel 1
    ax_sl_y_sh_1 = fig.add_subplot(gs[5:44, 96:99])
    ax_sl_y_sh_1.set_title('Y-shift', {'fontsize': 10})
    sl_y_sh_1 = wdgt.Slider(ax_sl_y_sh_1, '', -1.0, 1.0, 0.0, orientation='vertical', facecolor='#f4bb32')

    # creating on/off button for channel 2
    ax_b_on_off_2 = fig.add_subplot(gs[47:50, 111:114])
    b_on_off_2 = wdgt.Button(ax_b_on_off_2, '2', None, '0.85', '#9fd1ac')
    b_on_off_2.label.set_color('0')

    # making on/off button for channel 2 change color on click
    def button_change_2(event):
        if b_on_off_2.color == '#81b78f':
            b_on_off_2.color = '0.85'
            line2.set_linestyle('')
            line_fft_2.set_linestyle('')
        else:
            b_on_off_2.color = '#81b78f'
            line2.set_linestyle('-')
            if b_on_off_s.color == '0.95':
                line_fft_2.set_linestyle('-')

    b_on_off_2.on_clicked(button_change_2)

    # creating Y-scale slider for channel 2
    ax_sl_y_sc_2 = fig.add_subplot(gs[17:40, 106:109])
    ax_sl_y_sc_2.set_title('Y-scale', {'fontsize': 10})
    sl_y_sc_2 = wdgt.Slider(ax_sl_y_sc_2, '', 0.2, 5.0, 1.0, orientation='vertical',
                            valstep=[0.2, 0.25, 1 / 3, 0.5, 1.0, 2.0, 3.0, 4.0, 5.0], facecolor='#81b78f')

    # creating Y-shift slider for channel 2
    ax_sl_y_sh_2 = fig.add_subplot(gs[5:44, 116:119])
    ax_sl_y_sh_2.set_title('Y-shift', {'fontsize': 10})
    sl_y_sh_2 = wdgt.Slider(ax_sl_y_sh_2, '', -1.0, 1.0, 0.0, orientation='vertical', facecolor='#81b78f')

    # creating on/off button for channel 3
    ax_b_on_off_3 = fig.add_subplot(gs[47:50, 131:134])
    b_on_off_3 = wdgt.Button(ax_b_on_off_3, '3', None, '0.85', '#89a8db')
    b_on_off_3.label.set_color('0')

    # making on/off button for channel 3 change color on click
    def button_change_3(event):
        if b_on_off_3.color == '#6590d8':
            b_on_off_3.color = '0.85'
        else:
            b_on_off_3.color = '#6590d8'

    b_on_off_3.on_clicked(button_change_3)

    # creating Y-scale slider for channel 3
    ax_sl_y_sc_3 = fig.add_subplot(gs[17:40, 126:129])
    ax_sl_y_sc_3.set_title('Y-scale', {'fontsize': 10})
    sl_y_sc_3 = wdgt.Slider(ax_sl_y_sc_3, '', 0.2, 5.0, 1.0, orientation='vertical',
                            valstep=[0.2, 0.25, 1 / 3, 0.5, 1.0, 2.0, 3.0, 4.0, 5.0], facecolor='#6590d8')

    # creating Y-shift slider for channel 3
    ax_sl_y_sh_3 = fig.add_subplot(gs[5:44, 136:139])
    ax_sl_y_sh_3.set_title('Y-shift', {'fontsize': 10})
    sl_y_sh_3 = wdgt.Slider(ax_sl_y_sh_3, '', -1.0, 1.0, 0.0, orientation='vertical', facecolor='#6590d8')

    # creating on/off button for channel 4
    ax_b_on_off_4 = fig.add_subplot(gs[47:50, 151:154])
    b_on_off_4 = wdgt.Button(ax_b_on_off_4, '4', None, '0.85', '#f5b8d8')
    b_on_off_4.label.set_color('0')

    # making on/off button for channel 4 change color on click
    def button_change_4(event):
        if b_on_off_4.color == '#de8fb9':
            b_on_off_4.color = '0.85'
        else:
            b_on_off_4.color = '#de8fb9'

    b_on_off_4.on_clicked(button_change_4)

    # creating Y-scale slider for channel 4
    ax_sl_y_sc_4 = fig.add_subplot(gs[17:40, 146:149])
    ax_sl_y_sc_4.set_title('Y-scale', {'fontsize': 10})
    sl_y_sc_4 = wdgt.Slider(ax_sl_y_sc_4, '', 0.2, 5.0, 1.0, orientation='vertical',
                            valstep=[0.2, 0.25, 1 / 3, 0.5, 1.0, 2.0, 3.0, 4.0, 5.0], facecolor='#de8fb9')

    # creating Y-shift slider for channel 4
    ax_sl_y_sh_4 = fig.add_subplot(gs[5:44, 156:159])
    ax_sl_y_sh_4.set_title('Y-shift', {'fontsize': 10})
    sl_y_sh_4 = wdgt.Slider(ax_sl_y_sh_4, '', -1.0, 1.0, 0.0, orientation='vertical', facecolor='#de8fb9')

    # creating on/off button spectrum
    ax_b_on_off_s = fig.add_subplot(gs[70:74, 66:77])
    b_on_off_s = wdgt.Button(ax_b_on_off_s, 'Spectrum', None, '0.85', 'w')
    b_on_off_s.label.set_color('0')

    # making on/off button for spectrum change color on click
    def button_change_s(event):
        if b_on_off_s.color == '0.95':
            b_on_off_s.color = '0.85'
            line_fft_1.set_linestyle('')
            line_fft_2.set_linestyle('')
        else:
            b_on_off_s.color = '0.95'
            if b_on_off_1.color == '#f4bb32':
                line_fft_1.set_linestyle('-')
            if b_on_off_2.color == '#81b78f':
                line_fft_2.set_linestyle('-')

    b_on_off_s.on_clicked(button_change_s)

    # creating range slider for spectrum
    ax_r_sl = fig.add_subplot(gs[79:82, 66:97])
    ax_r_sl.set_title('Frequency range, Hz', fontsize=10)
    r_sl = wdgt.RangeSlider(ax_r_sl, '', 0.0, 22050.0, facecolor='0.95')
    r_sl.set_val([0.0, 22050.0])

    def change_size(event):
        xfftcur1pos = (xfftcur1.line.get_xdata()[0] - ax2.get_xlim()[0]) / (ax2.get_xlim()[1] - ax2.get_xlim()[0])
        xfftcur2pos = (xfftcur2.line.get_xdata()[0] - ax2.get_xlim()[0]) / (ax2.get_xlim()[1] - ax2.get_xlim()[0])

        ax2.set_xlim(r_sl.val[0] / 22050.0, r_sl.val[1] / 22050.0)
        ax2.set_xticks(np.linspace(r_sl.val[0] / 22050.0, r_sl.val[1] / 22050.0, 11, endpoint=True))

        xfftcur1.line.set_xdata([xfftcur1pos * (ax2.get_xlim()[1] - ax2.get_xlim()[0]) + ax2.get_xlim()[0],
                                 xfftcur1pos * (ax2.get_xlim()[1] - ax2.get_xlim()[0]) + ax2.get_xlim()[0]])
        xfftcur2.line.set_xdata([xfftcur2pos * (ax2.get_xlim()[1] - ax2.get_xlim()[0]) + ax2.get_xlim()[0],
                                 xfftcur2pos * (ax2.get_xlim()[1] - ax2.get_xlim()[0]) + ax2.get_xlim()[0]])

    r_sl.on_changed(change_size)

    # creating on/off button for waveform cursors
    ax_b_on_off_cur = fig.add_subplot(gs[54:58, 125:136])
    b_on_off_cur = wdgt.Button(ax_b_on_off_cur, 'Waveform \ncursors', None, '0.85', '0.95')
    b_on_off_cur.label.set_color('0')

    # making on/off button for waveform cursors change color on click
    def button_change_cur(event):
        if b_on_off_cur.color == '#4cd147':
            b_on_off_cur.color = '0.85'
            b_on_off_cur.hovercolor = '0.95'
            xcur1.line.set_linestyle('')
            xcur2.line.set_linestyle('')
            ycur1.line.set_linestyle('')
            ycur2.line.set_linestyle('')
        else:
            b_on_off_cur.color = '#4cd147'
            b_on_off_cur.hovercolor = '#2fff27'
            xcur1.line.set_linestyle('--')
            xcur2.line.set_linestyle('--')
            ycur1.line.set_linestyle('--')
            ycur2.line.set_linestyle('--')

    b_on_off_cur.on_clicked(button_change_cur)

    # creating on/off button for spectrum cursors
    ax_b_on_off_fft_cur = fig.add_subplot(gs[63:67, 125:136])
    b_on_off_fft_cur = wdgt.Button(ax_b_on_off_fft_cur, 'Spectrum \ncursors', None, '0.85', '0.95')
    b_on_off_fft_cur.label.set_color('0')

    # making on/off button for cursors change color on click
    def button_change_fft_cur(event):
        if b_on_off_fft_cur.color == '#4cd147':
            b_on_off_fft_cur.color = '0.85'
            b_on_off_fft_cur.hovercolor = '0.95'
            xfftcur1.line.set_linestyle('')
            xfftcur2.line.set_linestyle('')
            yfftcur1.line.set_linestyle('')
            yfftcur2.line.set_linestyle('')
        else:
            b_on_off_fft_cur.color = '#4cd147'
            b_on_off_fft_cur.hovercolor = '#2fff27'
            xfftcur1.line.set_linestyle('--')
            xfftcur2.line.set_linestyle('--')
            yfftcur1.line.set_linestyle('--')
            yfftcur2.line.set_linestyle('--')

    b_on_off_fft_cur.on_clicked(button_change_fft_cur)

    # making reset button
    ax_b_reset = fig.add_subplot(gs[72:76, 133:144])
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
        sl_tr.reset()
        # r_sl.set_val([0.0, 22050.0])
        xcur1.line.set_xdata([-0.5, -0.5])
        xcur2.line.set_xdata([0.5, 0.5])
        ycur1.line.set_ydata([-0.5, -0.5])
        ycur2.line.set_ydata([0.5, 0.5])

        xfftcur1pos = ax2.get_xlim()[0] + (ax2.get_xlim()[1] - ax2.get_xlim()[0]) / 4
        xfftcur2pos = ax2.get_xlim()[1] - (ax2.get_xlim()[1] - ax2.get_xlim()[0]) / 4
        yfftcur1pos = ax2.get_ylim()[0] + (ax2.get_ylim()[1] - ax2.get_ylim()[0]) / 4
        yfftcur2pos = ax2.get_ylim()[1] - (ax2.get_ylim()[1] - ax2.get_ylim()[0]) / 4
        xfftcur1.line.set_xdata([xfftcur1pos, xfftcur1pos])
        xfftcur2.line.set_xdata([xfftcur2pos, xfftcur2pos])
        yfftcur1.line.set_ydata([yfftcur1pos, yfftcur1pos])
        yfftcur2.line.set_ydata([yfftcur2pos, yfftcur2pos])

    b_reset.on_clicked(reset)

    # making single frame button
    ax_b_single = fig.add_subplot(gs[54:58, 141:152])
    b_single = wdgt.Button(ax_b_single, 'Single', None, '0.85', 'w')
    b_single.label.set_color('0')

    # making single frame button work
    def single(event):
        if b_run_stop.color == '#4cd147':
            b_run_stop.color = '0.85'
            b_run_stop.hovercolor = '0.95'

    b_single.on_clicked(single)

    # making run/stop button
    ax_b_run_stop = fig.add_subplot(gs[63:67, 141:152])
    b_run_stop = wdgt.Button(ax_b_run_stop, 'Run/Stop', None, '0.85', 'w')
    b_run_stop.label.set_color('0')

    # making run/stop button work
    def run_stop(event):
        if b_run_stop.color == '#4cd147':
            b_run_stop.color = '0.85'
            b_run_stop.hovercolor = '0.95'
        else:
            b_run_stop.color = '#4cd147'
            b_run_stop.hovercolor = '#2fff27'

    b_run_stop.on_clicked(run_stop)

    # making trigger on/off button
    ax_b_on_off_tr = fig.add_subplot(gs[47:51, 66:77])
    b_on_off_tr = wdgt.Button(ax_b_on_off_tr, 'Trigger', None, '0.85', 'w')
    b_on_off_tr.label.set_color('0')

    # making trigger on/off button work
    # ...

    # making trigger position slider

    ax_sl_tr = fig.add_subplot(gs[5:44, 70:73])
    ax_sl_tr.set_title('Trigger position', fontsize=10)
    sl_tr = wdgt.Slider(ax_sl_tr, '', -1, 1, 0, orientation='vertical', facecolor='0.95')

    # creating starter plots for all channels
    line1, = ax1.plot(np.linspace(-1, 1, blocksize), np.zeros(blocksize), '#f4bb32')
    line2, = ax1.plot(np.linspace(-1, 1, blocksize), np.zeros(blocksize), '#81b78f')
    # line3, = ax1.plot(np.linspace(-1, 1, blocksize), np.zeros(blocksize), '#6590d8')
    # line4, = ax1.plot(np.linspace(-1, 1, blocksize), np.zeros(blocksize), '#de8fb9')
    line2.set_linestyle('')
    # line3.set_linestyle('')
    # line4.set_linestyle('')
    line_fft_1, = ax2.plot(np.linspace(0, 1, blocksize), np.zeros(blocksize), '#f4bb32')
    line_fft_2, = ax2.plot(np.linspace(0, 1, blocksize), np.zeros(blocksize), '#81b78f')
    # line_fft_3, = ax2.plot(np.linspace(0, 1, blocksize), np.zeros(blocksize), '#6590d8')
    # line_fft_4, = ax2.plot(np.linspace(0, 1, blocksize), np.zeros(blocksize), '#de8fb9')
    line_fft_1.set_linestyle('')
    line_fft_2.set_linestyle('')
    # line_fft_3.set_linestyle('')
    # line_fft_4.set_linestyle('')

    xcur1 = Cc.Cursor(ax1.axvline(-0.5, c='r', ls='', pickradius=2), b_on_off_cur)
    xcur2 = Cc.Cursor(ax1.axvline(0.5, c='r', ls='', pickradius=2), b_on_off_cur)
    ycur1 = Cc.Cursor(ax1.axhline(-0.5, c='r', ls='', pickradius=2), b_on_off_cur)
    ycur2 = Cc.Cursor(ax1.axhline(0.5, c='r', ls='', pickradius=2), b_on_off_cur)

    xfftcur1 = Cc.Cursor(ax2.axvline(ax2.get_xlim()[0] + (ax2.get_xlim()[1] - ax2.get_xlim()[0]) / 4,
                                     c='r', ls='', pickradius=2), b_on_off_fft_cur)
    xfftcur2 = Cc.Cursor(ax2.axvline(ax2.get_xlim()[1] - (ax2.get_xlim()[1] - ax2.get_xlim()[0]) / 4,
                                     c='r', ls='', pickradius=2), b_on_off_fft_cur)
    yfftcur1 = Cc.Cursor(ax2.axhline(ax2.get_ylim()[0] + (ax2.get_ylim()[1] - ax2.get_ylim()[0]) / 4,
                                     c='r', ls='', pickradius=2), b_on_off_fft_cur)
    yfftcur2 = Cc.Cursor(ax2.axhline(ax2.get_ylim()[1] - (ax2.get_ylim()[1] - ax2.get_ylim()[0]) / 4,
                                     c='r', ls='', pickradius=2), b_on_off_fft_cur)

    # making blitting manager
    bm = BMc.BlitManager(fig.canvas,
                         [line1, line2, line_fft_1, line_fft_2,
                          xcur1.line, xcur2.line, ycur1.line, ycur2.line,
                          xfftcur1.line, xfftcur2.line, yfftcur1.line, yfftcur2.line])

    # making plot visible
    plt.show(block=False)
    plt.pause(.1)

    return fig, sl_x_sc, sl_x_sh, \
           b_on_off_1, line1, sl_y_sc_1, sl_y_sh_1, \
           b_on_off_2, line2, sl_y_sc_2, sl_y_sh_2, \
           b_on_off_s, line_fft_1, line_fft_2, r_sl, \
           xcur1, xcur2, ycur1, ycur2, b_on_off_cur, \
           b_reset, b_single, b_run_stop, b_on_off_tr,\
           sl_tr, bm


def update(fig, line, data, xscale=1.0, yscale=1.0, xshift=0.0, yshift=0.0):

    xdata = (np.linspace(-1, 1, len(data)) / xscale) - xshift
    line.set_data(xdata, (data * yscale) + yshift)


def update_fft(fig, line_fft, data):

    ydata = fft.fft(data)[:len(data) // 2]
    xdata = np.linspace(0, 1, len(ydata))

    line_fft.set_data(xdata, np.abs(ydata) * 2 / len(ydata))
