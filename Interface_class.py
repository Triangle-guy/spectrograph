import sys
import scipy.fftpack as fft
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as wdgt

import Cursor_class as Cc
import BlittingManager_class as BMc


class Interface:
    def __init__(self, blocksize, samplerate):
        # choosing style
        plt.style.use('dark_background')

        # creating figure and gridspec instance
        self.fig = plt.figure(figsize=(16, 9))
        self.gs = self.fig.add_gridspec(90, 160)

        def on_close(event):
            sys.exit()

        # connecting on_close event
        self.fig.canvas.mpl_connect('close_event', on_close)

        # creating and formatting axes for waveform
        self.ax1 = self.fig.add_subplot(self.gs[5:44, 0:63])
        self.ax1.grid(True, lw=0.2)

        self.x_max_span = np.round(blocksize * 1000 / samplerate, 1)

        self.ax1.set_xlim(-np.round(self.x_max_span / 8, 1), np.round(self.x_max_span / 8, 1))
        self.ax1.set_xticks(np.linspace(-np.round(self.x_max_span / 8, 1), np.round(self.x_max_span / 8, 1),
                                        11, endpoint=True))
        self.ax1.set_xticklabels([])

        self.ax1.set_ylim(-1, 1)
        self.ax1.set_yticks(np.linspace(-1, 1, 9, endpoint=True))
        self.ax1.set_yticklabels([])

        self.ax1.tick_params(axis='both', length=0)

        # creating and formatting axes for spectrum
        self.ax2 = self.fig.add_subplot(self.gs[45:84, 0:63])
        self.ax2.grid(True, lw=0.2)

        self.ax2.set_xlim(0, 22050)
        self.ax2.set_xticks(np.linspace(0, 22050, 11, endpoint=True))
        self.ax2.set_xticklabels([])

        self.ax2.set_ylim(0, 0.5)
        self.ax2.set_yticks(np.linspace(0, 0.5, 9, endpoint=True))
        self.ax2.set_yticklabels([])

        self.ax2.tick_params(axis='both', length=0)

        # creating text boxes for distances between cursors
        self.ax_t_1_l = self.fig.add_subplot(self.gs[0:4, 8:23])
        self.ax_t_1_l.set_xticklabels([])
        self.ax_t_1_l.set_yticklabels([])
        self.ax_t_1_l.tick_params(axis='both', length=0)
        self.t_1_l = self.ax_t_1_l.text(0.5, 0.5, '', ha='center', va='center')

        self.ax_t_1_r = self.fig.add_subplot(self.gs[0:4, 40:55])
        self.ax_t_1_r.set_xticklabels([])
        self.ax_t_1_r.set_yticklabels([])
        self.ax_t_1_r.tick_params(axis='both', length=0)
        self.t_1_r = self.ax_t_1_r.text(0.5, 0.5, '', ha='center', va='center')

        self.ax_t_2_l = self.fig.add_subplot(self.gs[85:89, 8:23])
        self.ax_t_2_l.set_xticklabels([])
        self.ax_t_2_l.set_yticklabels([])
        self.ax_t_2_l.tick_params(axis='both', length=0)
        self.t_2_l = self.ax_t_2_l.text(0.5, 0.5, '', ha='center', va='center')

        self.ax_t_2_r = self.fig.add_subplot(self.gs[85:89, 40:55])
        self.ax_t_2_r.set_xticklabels([])
        self.ax_t_2_r.set_yticklabels([])
        self.ax_t_2_r.tick_params(axis='both', length=0)
        self.t_2_r = self.ax_t_2_r.text(0.5, 0.5, '', ha='center', va='center')

        # creating text boxes for cell scales
        self.ax_t_y_ch_1 = self.fig.add_subplot(self.gs[9:13, 90:101])
        self.ax_t_y_ch_1.set_xticklabels([])
        self.ax_t_y_ch_1.set_yticklabels([])
        self.ax_t_y_ch_1.tick_params(axis='both', length=0)
        self.t_y_ch_1 = self.ax_t_y_ch_1.text(0.5, 0.5, '0.25', ha='center', va='center')

        self.ax_t_y_ch_2 = self.fig.add_subplot(self.gs[9:13, 108:119])
        self.ax_t_y_ch_2.set_xticklabels([])
        self.ax_t_y_ch_2.set_yticklabels([])
        self.ax_t_y_ch_2.tick_params(axis='both', length=0)
        self.t_y_ch_2 = self.ax_t_y_ch_2.text(0.5, 0.5, '0.25', ha='center', va='center')

        self.ax_t_y_ch_3 = self.fig.add_subplot(self.gs[9:14, 126:138])
        self.ax_t_y_ch_3.set_xticklabels([])
        self.ax_t_y_ch_3.set_yticklabels([])
        self.ax_t_y_ch_3.tick_params(axis='both', length=0)
        self.t_y_ch_3 = self.ax_t_y_ch_3.text(0.5, 0.5, '0.25', ha='center', va='center')

        self.ax_t_y_ch_4 = self.fig.add_subplot(self.gs[9:13, 144:157])
        self.ax_t_y_ch_4.set_xticklabels([])
        self.ax_t_y_ch_4.set_yticklabels([])
        self.ax_t_y_ch_4.tick_params(axis='both', length=0)
        self.t_y_ch_4 = self.ax_t_y_ch_4.text(0.5, 0.5, '0.25', ha='center', va='center')

        self.ax_t_x = self.fig.add_subplot(self.gs[54:58, 104:115])
        self.ax_t_x.set_xticklabels([])
        self.ax_t_x.set_yticklabels([])
        self.ax_t_x.tick_params(axis='both', length=0)
        self.t_x = self.ax_t_x.text(0.5, 0.5, str(np.round(self.x_max_span / 40, 1)) + ' ms',
                                    ha='center', va='center')

        # creating X-scale slider
        self.ax_sl_x_sc = self.fig.add_subplot(self.gs[54:57, 66:97])
        self.ax_sl_x_sc.set_title('X-scale', {'fontsize': 10})
        self.sl_x_sc = wdgt.Slider(self.ax_sl_x_sc, '', -4, 0, -2,
                                   valstep=0.5, facecolor='0.95')
        self.sl_x_sc.valtext.set_visible(False)

        # making X-scale slider work
        def scale_x(event):
            xcur1pos = ((self.xcur1.line.get_xdata()[0] - self.ax1.get_xlim()[0]) /
                        (self.ax1.get_xlim()[1] - self.ax1.get_xlim()[0]))
            xcur2pos = ((self.xcur2.line.get_xdata()[0] - self.ax1.get_xlim()[0]) /
                        (self.ax1.get_xlim()[1] - self.ax1.get_xlim()[0]))

            self.ax1.set_xlim(-np.round(self.x_max_span * 2.0 ** (self.sl_x_sc.val - 1), 1) - self.sl_x_sh.val,
                              np.round(self.x_max_span * 2.0 ** (self.sl_x_sc.val - 1), 1) - self.sl_x_sh.val)
            self.ax1.set_xticks(np.linspace(
                -np.round(self.x_max_span * 2.0 ** (self.sl_x_sc.val - 1), 1) - self.sl_x_sh.val,
                np.round(self.x_max_span * 2.0 ** (self.sl_x_sc.val - 1), 1) - self.sl_x_sh.val, 11, endpoint=True))

            self.xcur1.line.set_xdata([xcur1pos * (self.ax1.get_xlim()[1] - self.ax1.get_xlim()[0])
                                          + self.ax1.get_xlim()[0],
                                       xcur1pos * (self.ax1.get_xlim()[1] - self.ax1.get_xlim()[0])
                                          + self.ax1.get_xlim()[0]])
            self.xcur2.line.set_xdata([xcur2pos * (self.ax1.get_xlim()[1] - self.ax1.get_xlim()[0])
                                          + self.ax1.get_xlim()[0],
                                          xcur2pos * (self.ax1.get_xlim()[1] - self.ax1.get_xlim()[0])
                                          + self.ax1.get_xlim()[0]])

            self.t_x.set_text(str(np.round(self.x_max_span * (2.0 ** self.sl_x_sc.val) / 10, 1)) + ' ms')

        self.sl_x_sc.on_changed(scale_x)

        # creating X-shift slider
        self.ax_sl_x_sh = self.fig.add_subplot(self.gs[62:65, 66:97])
        self.ax_sl_x_sh.set_title('X-shift', {'fontsize': 10})
        self.sl_x_sh = wdgt.Slider(self.ax_sl_x_sh, '',
                                   -np.round(self.x_max_span / 2, 1), np.round(self.x_max_span / 2, 1), 0.0,
                                   facecolor='0.95')
        self.sl_x_sh.valtext.set_visible(False)

        # making X-shift slider work
        def shift_x(event):
            xcur1pos = (self.xcur1.line.get_xdata()[0] - self.ax1.get_xlim()[0])
            xcur2pos = (self.xcur2.line.get_xdata()[0] - self.ax1.get_xlim()[0])

            self.ax1.set_xlim(-np.round(self.x_max_span * 2.0 ** (self.sl_x_sc.val - 1), 1) - self.sl_x_sh.val,
                              np.round(self.x_max_span * 2.0 ** (self.sl_x_sc.val - 1), 1) - self.sl_x_sh.val)

            self.ax1.set_xticks(np.linspace(self.ax1.get_xlim()[0], self.ax1.get_xlim()[1], 11, endpoint=True))

            self.xcur1.line.set_xdata([xcur1pos + self.ax1.get_xlim()[0], xcur1pos + self.ax1.get_xlim()[0]])
            self.xcur2.line.set_xdata([xcur2pos + self.ax1.get_xlim()[0], xcur2pos + self.ax1.get_xlim()[0]])

        self.sl_x_sh.on_changed(shift_x)

        # creating on/off button for channel 1
        self.ax_b_on_off_1 = self.fig.add_subplot(self.gs[47:50, 96:99])
        self.b_on_off_1 = wdgt.Button(self.ax_b_on_off_1, '1', None, '#f4bb32', '#efc35b')
        self.b_on_off_1.label.set_color('0')

        # making on/off button for channel 1 change color on click
        def button_change_1(event):
            if self.b_on_off_1.color == '#f4bb32':
                self.b_on_off_1.color = '0.85'
                self.line1.set_linestyle('')
                self.line_fft_1.set_linestyle('')
            else:
                self.b_on_off_1.color = '#f4bb32'
                self.line1.set_linestyle('-')
                if self.b_on_off_s.color == '0.95':
                    self.line_fft_1.set_linestyle('-')

        self.b_on_off_1.on_clicked(button_change_1)

        # creating Y-scale slider for channel 1
        self.ax_sl_y_sc_1 = self.fig.add_subplot(self.gs[17:40, 94:97])
        self.ax_sl_y_sc_1.set_title('Y-scale', {'fontsize': 10})
        self.sl_y_sc_1 = wdgt.Slider(self.ax_sl_y_sc_1, '', -2, 2, 0, orientation='vertical',
                                     valstep=0.5, facecolor='#f4bb32')
        self.sl_y_sc_1.valtext.set_visible(False)

        # making Y-scale slider for channel 1 affect scale box
        def scale_1(event):
            self.t_y_ch_1.set_text(str(np.round(0.25 / (2 ** self.sl_y_sc_1.val), 3)))
            if self.data1 is not None:
                self.line1.set_ydata((self.data1 * (2 ** self.sl_y_sc_1.val)) + self.sl_y_sh_1.val)

        self.sl_y_sc_1.on_changed(scale_1)

        # creating Y-shift slider for channel 1
        self.ax_sl_y_sh_1 = self.fig.add_subplot(self.gs[5:44, 102:105])
        self.ax_sl_y_sh_1.set_title('Y-shift', {'fontsize': 10})
        self.sl_y_sh_1 = wdgt.Slider(self.ax_sl_y_sh_1, '', -1.0, 1.0, 0.0, orientation='vertical', facecolor='#f4bb32')
        self.sl_y_sh_1.valtext.set_visible(False)

        # making Y-shift slider for channel 1 move trigger
        # self.prev1 = 0

        # def shift_1(event):
        #     if self.b_on_off_tr.color == '0.95' and self.r_b.value_selected == 'Channel 1':
        #         if self.sl_tr.val + self.sl_y_sh_1.val - self.prev1 > 1:
        #             self.sl_tr.set_val(1)
        #         elif self.sl_tr.val + self.sl_y_sh_1.val - self.prev1 < -1:
        #             self.sl_tr.set_val(-1)
        #         else:
        #             self.sl_tr.set_val(self.sl_tr.val + self.sl_y_sh_1.val - self.prev1)

        #     self.prev1 = self.sl_y_sh_1.val

        # self.sl_y_sh_1.on_changed(shift_1)

        # creating on/off button for channel 2
        self.ax_b_on_off_2 = self.fig.add_subplot(self.gs[47:50, 114:117])
        self.b_on_off_2 = wdgt.Button(self.ax_b_on_off_2, '2', None, '0.85', '#9fd1ac')
        self.b_on_off_2.label.set_color('0')

        # making on/off button for channel 2 change color on click
        def button_change_2(event):
            if self.b_on_off_2.color == '#81b78f':
                self.b_on_off_2.color = '0.85'
                self.line2.set_linestyle('')
                self.line_fft_2.set_linestyle('')
            else:
                self.b_on_off_2.color = '#81b78f'
                self.line2.set_linestyle('-')
                if self.b_on_off_s.color == '0.95':
                    self.line_fft_2.set_linestyle('-')

        self.b_on_off_2.on_clicked(button_change_2)

        # creating Y-scale slider for channel 2
        self.ax_sl_y_sc_2 = self.fig.add_subplot(self.gs[17:40, 112:115])
        self.ax_sl_y_sc_2.set_title('Y-scale', {'fontsize': 10})
        self.sl_y_sc_2 = wdgt.Slider(self.ax_sl_y_sc_2, '', -2, 2, 0, orientation='vertical',
                                     valstep=0.5, facecolor='#81b78f')
        self.sl_y_sc_2.valtext.set_visible(False)

        # making Y-scale slider for channel 2 affect scale box
        def scale_2(event):
            self.t_y_ch_2.set_text(str(np.round(0.25 / (2 ** self.sl_y_sc_2.val), 3)))
            if self.data2 is not None:
                self.line2.set_ydata((self.data2 * (2 ** self.sl_y_sc_2.val)) + self.sl_y_sh_2.val)

        self.sl_y_sc_2.on_changed(scale_2)

        # creating Y-shift slider for channel 2
        self.ax_sl_y_sh_2 = self.fig.add_subplot(self.gs[5:44, 120:123])
        self.ax_sl_y_sh_2.set_title('Y-shift', {'fontsize': 10})
        self.sl_y_sh_2 = wdgt.Slider(self.ax_sl_y_sh_2, '', -1.0, 1.0, 0.0, orientation='vertical', facecolor='#81b78f')
        self.sl_y_sh_2.valtext.set_visible(False)

        # making Y-shift slider for channel 2 move trigger
        self.prev2 = 0

        def shift_2(event):
            if self.b_on_off_tr.color == '0.95' and self.r_b.value_selected == 'Channel 2':
                if self.sl_tr.val + self.sl_y_sh_2.val - self.prev2 > 1:
                    self.sl_tr.set_val(1)
                elif self.sl_tr.val + self.sl_y_sh_2.val - self.prev2 < -1:
                    self.sl_tr.set_val(-1)
                else:
                    self.sl_tr.set_val(self.sl_tr.val + self.sl_y_sh_2.val - self.prev2)

            self.prev2 = self.sl_y_sh_2.val

        self.sl_y_sh_2.on_changed(shift_2)

        # creating on/off button for channel 3
        self.ax_b_on_off_3 = self.fig.add_subplot(self.gs[47:50, 132:135])
        self.b_on_off_3 = wdgt.Button(self.ax_b_on_off_3, '3', None, '0.85', '#89a8db')
        self.b_on_off_3.label.set_color('0')

        # making on/off button for channel 3 change color on click
        def button_change_3(event):
            if self.b_on_off_3.color == '#6590d8':
                self.b_on_off_3.color = '0.85'
                self.line3.set_linestyle('')
                self.line_fft_3.set_linestyle('')
            else:
                self.b_on_off_3.color = '#6590d8'
                self.line3.set_linestyle('-')
                if self.b_on_off_s.color == '0.95':
                    self.line_fft_3.set_linestyle('-')

        self.b_on_off_3.on_clicked(button_change_3)

        # creating Y-scale slider for channel 3
        self.ax_sl_y_sc_3 = self.fig.add_subplot(self.gs[17:40, 130:133])
        self.ax_sl_y_sc_3.set_title('Y-scale', {'fontsize': 10})
        self.sl_y_sc_3 = wdgt.Slider(self.ax_sl_y_sc_3, '', -2, 2, 0, orientation='vertical',
                                     valstep=0.5, facecolor='#6590d8')
        self.sl_y_sc_3.valtext.set_visible(False)

        # making Y-scale slider for channel 3 affect scale box
        def scale_3(event):
            self.t_y_ch_3.set_text(str(np.round(0.25 / (2 ** self.sl_y_sc_3.val), 3)))
            if self.data3 is not None:
                self.line3.set_ydata((self.data3 * (2 ** self.sl_y_sc_3.val)) + self.sl_y_sh_3.val)

        self.sl_y_sc_3.on_changed(scale_3)

        # creating Y-shift slider for channel 3
        self.ax_sl_y_sh_3 = self.fig.add_subplot(self.gs[5:44, 138:141])
        self.ax_sl_y_sh_3.set_title('Y-shift', {'fontsize': 10})
        self.sl_y_sh_3 = wdgt.Slider(self.ax_sl_y_sh_3, '', -1.0, 1.0, 0.0, orientation='vertical', facecolor='#6590d8')
        self.sl_y_sh_3.valtext.set_visible(False)

        # making Y-shift slider for channel 3 move trigger
        self.prev3 = 0

        def shift_3(event):
            if self.b_on_off_tr.color == '0.95' and self.r_b.value_selected == 'Channel 3':
                if self.sl_tr.val + self.sl_y_sh_3.val - self.prev3 > 3:
                    self.sl_tr.set_val(1)
                elif self.sl_tr.val + self.sl_y_sh_3.val - self.prev3 < -1:
                    self.sl_tr.set_val(-1)
                else:
                    self.sl_tr.set_val(self.sl_tr.val + self.sl_y_sh_3.val - self.prev3)

            self.prev3 = self.sl_y_sh_3.val

        self.sl_y_sh_3.on_changed(shift_3)

        # creating on/off button for channel 4
        self.ax_b_on_off_4 = self.fig.add_subplot(self.gs[47:50, 150:153])
        self.b_on_off_4 = wdgt.Button(self.ax_b_on_off_4, '4', None, '0.85', '#f5b8d8')
        self.b_on_off_4.label.set_color('0')

        # making on/off button for channel 4 change color on click
        def button_change_4(event):
            if self.b_on_off_4.color == '#de8fb9':
                self.b_on_off_4.color = '0.85'
                self.line4.set_linestyle('')
                self.line_fft_4.set_linestyle('')
            else:
                self.b_on_off_4.color = '#de8fb9'
                self.line4.set_linestyle('-')
                if self.b_on_off_s.color == '0.95':
                    self.line_fft_4.set_linestyle('-')

        self.b_on_off_4.on_clicked(button_change_4)

        # creating Y-scale slider for channel 4
        self.ax_sl_y_sc_4 = self.fig.add_subplot(self.gs[17:40, 148:151])
        self.ax_sl_y_sc_4.set_title('Y-scale', {'fontsize': 10})
        self.sl_y_sc_4 = wdgt.Slider(self.ax_sl_y_sc_4, '', -2, 2, 0, orientation='vertical',
                                     valstep=0.5, facecolor='#de8fb9')
        self.sl_y_sc_4.valtext.set_visible(False)

        # making Y-scale slider for channel 4 affect scale box
        def scale_4(event):
            self.t_y_ch_4.set_text(str(np.round(0.25 / (2 ** self.sl_y_sc_4.val), 3)))
            if self.data4 is not None:
                self.line4.set_ydata((self.data4 * (2 ** self.sl_y_sc_4.val)) + self.sl_y_sh_4.val)

        self.sl_y_sc_4.on_changed(scale_4)

        # creating Y-shift slider for channel 4
        self.ax_sl_y_sh_4 = self.fig.add_subplot(self.gs[5:44, 156:159])
        self.ax_sl_y_sh_4.set_title('Y-shift', {'fontsize': 10})
        self.sl_y_sh_4 = wdgt.Slider(self.ax_sl_y_sh_4, '', -1.0, 1.0, 0.0, orientation='vertical', facecolor='#de8fb9')
        self.sl_y_sh_4.valtext.set_visible(False)

        # making Y-shift slider for channel 4 move trigger
        self.prev4 = 0

        def shift_4(event):
            if self.b_on_off_tr.color == '0.95' and self.r_b.value_selected == 'Channel 4':
                if self.sl_tr.val + self.sl_y_sh_4.val - self.prev4 > 1:
                    self.sl_tr.set_val(1)
                elif self.sl_tr.val + self.sl_y_sh_4.val - self.prev4 < -1:
                    self.sl_tr.set_val(-1)
                else:
                    self.sl_tr.set_val(self.sl_tr.val + self.sl_y_sh_4.val - self.prev4)

            self.prev4 = self.sl_y_sh_4.val

        self.sl_y_sh_4.on_changed(shift_4)

        # creating on/off button spectrum
        self.ax_b_on_off_s = self.fig.add_subplot(self.gs[70:74, 66:77])
        self.b_on_off_s = wdgt.Button(self.ax_b_on_off_s, 'Spectrum', None, '0.85', 'w')
        self.b_on_off_s.label.set_color('0')

        # making on/off button for spectrum change color on click
        def button_change_s(event):
            if self.b_on_off_s.color == '0.95':
                self.b_on_off_s.color = '0.85'
                self.line_fft_1.set_linestyle('')
                self.line_fft_2.set_linestyle('')
            else:
                self.b_on_off_s.color = '0.95'
                if self.b_on_off_1.color == '#f4bb32':
                    self.line_fft_1.set_linestyle('-')
                if self.b_on_off_2.color == '#81b78f':
                    self.line_fft_2.set_linestyle('-')

        self.b_on_off_s.on_clicked(button_change_s)

        # creating lin/log button for spectrum

        # self.ax_b_lin_log = self.fig.add_subplot(self.gs[70:74, 82:93])
        # self.b_lin_log = wdgt.Button(self.ax_b_lin_log, 'Lin/Log', None, '0.85', 'w')
        # self.b_lin_log.label.set_color('0')

        # self.flag2 = False

        # making lin/log button for spectrum work
        # def lin_log_switch(event):
        #     if self.flag2:
        #         self.flag2 = False

        #         self.ax2.set_ylim(0, 0.2)
        #         self.ax2.set_yticks(np.linspace(0, 0.2, 9, endpoint=True))
        #         self.ax2.set_yscale('linear')
        #         self.ax2.set_yticklabels([])
        #     else:
        #         self.flag2 = True

        #         self.ax2.set_ylim(0, 1)
        #         self.ax2.set_yticks(np.linspace(0, 1, 9, endpoint=True))
        #         self.ax2.set_yscale('log')
        #         # self.ax2.set_yticklabels([])
        #         self.ax2.tick_params(axis='y', length=0)
        #         print(self.ax2.get_yticks())
        #         print(self.ax2.get_ylim())

        # self.b_lin_log.on_clicked(lin_log_switch)

        # creating range slider for spectrum
        self.ax_r_sl = self.fig.add_subplot(self.gs[79:82, 66:97])
        self.ax_r_sl.set_title('Frequency range, Hz', fontsize=10)
        self.r_sl = wdgt.RangeSlider(self.ax_r_sl, '', 0.0, 22050.0, facecolor='0.95')
        self.r_sl.set_val([0.0, 22050.0])

        # making range slider for spectrum work
        def change_size(event):
            xfftcur1pos = ((self.xfftcur1.line.get_xdata()[0] - self.ax2.get_xlim()[0]) /
                           (self.ax2.get_xlim()[1] - self.ax2.get_xlim()[0]))
            xfftcur2pos = ((self.xfftcur2.line.get_xdata()[0] - self.ax2.get_xlim()[0]) /
                           (self.ax2.get_xlim()[1] - self.ax2.get_xlim()[0]))

            self.ax2.set_xlim(self.r_sl.val[0], self.r_sl.val[1])
            self.ax2.set_xticks(np.linspace(self.r_sl.val[0], self.r_sl.val[1], 11, endpoint=True))

            self.xfftcur1.line.set_xdata([xfftcur1pos * (self.ax2.get_xlim()[1] - self.ax2.get_xlim()[0])
                                          + self.ax2.get_xlim()[0],
                                          xfftcur1pos * (self.ax2.get_xlim()[1] - self.ax2.get_xlim()[0])
                                          + self.ax2.get_xlim()[0]])
            self.xfftcur2.line.set_xdata([xfftcur2pos * (self.ax2.get_xlim()[1] - self.ax2.get_xlim()[0])
                                          + self.ax2.get_xlim()[0],
                                          xfftcur2pos * (self.ax2.get_xlim()[1] - self.ax2.get_xlim()[0])
                                          + self.ax2.get_xlim()[0]])

        self.r_sl.on_changed(change_size)

        # creating on/off button for waveform cursors
        self.ax_b_on_off_cur = self.fig.add_subplot(self.gs[54:58, 125:136])
        self.b_on_off_cur = wdgt.Button(self.ax_b_on_off_cur, 'Waveform \ncursors', None, '0.85', '0.95')
        self.b_on_off_cur.label.set_color('0')

        # making on/off button for waveform cursors change color on click
        def button_change_cur(event):
            if self.b_on_off_cur.color == '#4cd147':
                self.b_on_off_cur.color = '0.85'
                self.b_on_off_cur.hovercolor = '0.95'
                self.xcur1.line.set_linestyle('')
                self.xcur2.line.set_linestyle('')
                self.ycur1.line.set_linestyle('')
                self.ycur2.line.set_linestyle('')
            else:
                self.b_on_off_cur.color = '#4cd147'
                self.b_on_off_cur.hovercolor = '#2fff27'
                self.xcur1.line.set_linestyle('--')
                self.xcur2.line.set_linestyle('--')
                self.ycur1.line.set_linestyle('--')
                self.ycur2.line.set_linestyle('--')

        self.b_on_off_cur.on_clicked(button_change_cur)

        # creating on/off button for spectrum cursors
        self.ax_b_on_off_fft_cur = self.fig.add_subplot(self.gs[63:67, 125:136])
        self.b_on_off_fft_cur = wdgt.Button(self.ax_b_on_off_fft_cur, 'Spectrum \ncursors', None, '0.85', '0.95')
        self.b_on_off_fft_cur.label.set_color('0')

        # making on/off button for cursors change color on click
        def button_change_fft_cur(event):
            if self.b_on_off_fft_cur.color == '#4cd147':
                self.b_on_off_fft_cur.color = '0.85'
                self.b_on_off_fft_cur.hovercolor = '0.95'
                self.xfftcur1.line.set_linestyle('')
                self.xfftcur2.line.set_linestyle('')
                self.yfftcur1.line.set_linestyle('')
                self.yfftcur2.line.set_linestyle('')
            else:
                self.b_on_off_fft_cur.color = '#4cd147'
                self.b_on_off_fft_cur.hovercolor = '#2fff27'
                self.xfftcur1.line.set_linestyle('--')
                self.xfftcur2.line.set_linestyle('--')
                self.yfftcur1.line.set_linestyle('--')
                self.yfftcur2.line.set_linestyle('--')

        self.b_on_off_fft_cur.on_clicked(button_change_fft_cur)

        # creating reset button
        self.ax_b_reset = self.fig.add_subplot(self.gs[72:76, 133:144])
        self.b_reset = wdgt.Button(self.ax_b_reset, 'Reset', None, '#f96b6b', '#fa9494')

        # making reset button reset all sliders' and cursors' positions
        def reset(event):
            self.sl_x_sc.reset()
            self.sl_x_sh.reset()
            self.sl_y_sc_1.reset()
            self.sl_y_sh_1.reset()
            self.sl_y_sc_2.reset()
            self.sl_y_sh_2.reset()
            self.sl_y_sc_3.reset()
            self.sl_y_sh_3.reset()
            self.sl_y_sc_4.reset()
            self.sl_y_sh_4.reset()
            self.sl_tr.reset()
            self.r_sl.set_val([0.0, 22050.0])
            self.r_b.set_active(0)

            self.xcur1.line.set_xdata([-np.round(self.x_max_span * 2.0 ** (self.sl_x_sc.val - 2), 1),
                                       -np.round(self.x_max_span * 2.0 ** (self.sl_x_sc.val - 2), 1)])
            self.xcur2.line.set_xdata([np.round(self.x_max_span * 2.0 ** (self.sl_x_sc.val - 2), 1),
                                       np.round(self.x_max_span * 2.0 ** (self.sl_x_sc.val - 2), 1)])
            self.ycur1.line.set_ydata([-0.5, -0.5])
            self.ycur2.line.set_ydata([0.5, 0.5])

            xfftcur1pos = self.ax2.get_xlim()[0] + (self.ax2.get_xlim()[1] - self.ax2.get_xlim()[0]) / 4
            xfftcur2pos = self.ax2.get_xlim()[1] - (self.ax2.get_xlim()[1] - self.ax2.get_xlim()[0]) / 4
            yfftcur1pos = self.ax2.get_ylim()[0] + (self.ax2.get_ylim()[1] - self.ax2.get_ylim()[0]) / 4
            yfftcur2pos = self.ax2.get_ylim()[1] - (self.ax2.get_ylim()[1] - self.ax2.get_ylim()[0]) / 4
            self.xfftcur1.line.set_xdata([xfftcur1pos, xfftcur1pos])
            self.xfftcur2.line.set_xdata([xfftcur2pos, xfftcur2pos])
            self.yfftcur1.line.set_ydata([yfftcur1pos, yfftcur1pos])
            self.yfftcur2.line.set_ydata([yfftcur2pos, yfftcur2pos])

        self.b_reset.on_clicked(reset)

        # creating single frame button
        self.ax_b_single = self.fig.add_subplot(self.gs[54:58, 141:152])
        self.b_single = wdgt.Button(self.ax_b_single, 'Single', None, '0.85', 'w')
        self.b_single.label.set_color('0')

        self.flag1 = False

        # making single frame button work
        def single(event):
            if self.b_run_stop.color == '#4cd147':
                self.b_run_stop.color = '0.85'
                self.b_run_stop.hovercolor = '0.95'
            else:
                self.b_run_stop.color = '#4cd147'
                self.b_run_stop.hovercolor = '#2fff27'
                self.flag1 = True

        self.b_single.on_clicked(single)

        # creating run/stop button
        self.ax_b_run_stop = self.fig.add_subplot(self.gs[63:67, 141:152])
        self.b_run_stop = wdgt.Button(self.ax_b_run_stop, 'Run/Stop', None, '0.85', 'w')
        self.b_run_stop.label.set_color('0')

        # making run/stop button work
        def run_stop(event):
            if self.b_run_stop.color == '#4cd147':
                self.b_run_stop.color = '0.85'
                self.b_run_stop.hovercolor = '0.95'
            else:
                self.b_run_stop.color = '#4cd147'
                self.b_run_stop.hovercolor = '#2fff27'

        self.b_run_stop.on_clicked(run_stop)

        # creating trigger on/off button
        self.ax_b_on_off_tr = self.fig.add_subplot(self.gs[47:51, 66:77])
        self.b_on_off_tr = wdgt.Button(self.ax_b_on_off_tr, 'Trigger', None, '0.85', 'w')
        self.b_on_off_tr.label.set_color('0')

        # making trigger on/off button work
        def trigger_on_off(event):
            if self.b_on_off_tr.color == '0.95':
                self.b_on_off_tr.color = '0.85'
                self.trigger.set_linestyle('')
            else:
                self.b_on_off_tr.color = '0.95'
                self.trigger.set_linestyle('-')

        self.b_on_off_tr.on_clicked(trigger_on_off)

        # creating trigger position slider
        self.ax_sl_tr = self.fig.add_subplot(self.gs[5:44, 66:69])
        self.ax_sl_tr.set_title('Trigger \nposition', fontsize=10)
        self.sl_tr = wdgt.Slider(self.ax_sl_tr, '', -1, 1, 0, orientation='vertical', facecolor='0.95')
        self.sl_tr.valtext.set_visible(False)

        # making trigger position slider work
        def trigger_move(event):
            self.trigger.set_ydata([self.sl_tr.val, self.sl_tr.val])

        self.sl_tr.on_changed(trigger_move)

        # creating radio buttons for channel selection
        self.ax_r_b = self.fig.add_subplot(self.gs[17:40, 72:89])
        self.ax_r_b.set_title('Channel \nselection', fontsize=10)
        self.r_b = wdgt.RadioButtons(self.ax_r_b, ('Channel 1', 'Channel 2', 'Channel 3', 'Channel 4'), 0, '#4cd147')

        # creating starter plots for all channels
        self.line1, = self.ax1.plot(np.linspace(-np.round(self.x_max_span / 2, 1), np.round(self.x_max_span / 2, 1), blocksize),
                                    np.zeros(blocksize), '#f4bb32')
        self.line2, = self.ax1.plot(np.linspace(-np.round(self.x_max_span / 2, 1), np.round(self.x_max_span / 2, 1), blocksize),
                                    np.zeros(blocksize), '#81b78f')
        self.line3, = self.ax1.plot(np.linspace(-np.round(self.x_max_span / 2, 1), np.round(self.x_max_span / 2, 1), blocksize),
                                    np.zeros(blocksize), '#6590d8')
        self.line4, = self.ax1.plot(np.linspace(-np.round(self.x_max_span / 2, 1), np.round(self.x_max_span / 2, 1), blocksize),
                                    np.zeros(blocksize), '#de8fb9')
        self.line2.set_linestyle('')
        self.line3.set_linestyle('')
        self.line4.set_linestyle('')

        self.line_fft_1, = self.ax2.plot(np.linspace(0, 22050, blocksize), np.zeros(blocksize), '#f4bb32')
        self.line_fft_2, = self.ax2.plot(np.linspace(0, 22050, blocksize), np.zeros(blocksize), '#81b78f')
        self.line_fft_3, = self.ax2.plot(np.linspace(0, 22050, blocksize), np.zeros(blocksize), '#6590d8')
        self.line_fft_4, = self.ax2.plot(np.linspace(0, 22050, blocksize), np.zeros(blocksize), '#de8fb9')
        self.line_fft_1.set_linestyle('')
        self.line_fft_2.set_linestyle('')
        self.line_fft_3.set_linestyle('')
        self.line_fft_4.set_linestyle('')

        self.trigger = self.ax1.axhline(0, c='0.95', ls='', lw=0.5)

        self.xcur1 = Cc.Cursor(self.ax1.axvline(-self.x_max_span / 16, c='r', ls='', pickradius=2), self.b_on_off_cur)
        self.xcur2 = Cc.Cursor(self.ax1.axvline(self.x_max_span / 16, c='r', ls='', pickradius=2), self.b_on_off_cur)
        self.ycur1 = Cc.Cursor(self.ax1.axhline(-0.5, c='r', ls='', pickradius=2), self.b_on_off_cur)
        self.ycur2 = Cc.Cursor(self.ax1.axhline(0.5, c='r', ls='', pickradius=2), self.b_on_off_cur)

        self.xfftcur1 = Cc.Cursor(self.ax2.axvline(self.ax2.get_xlim()[0] +
                                                   (self.ax2.get_xlim()[1] - self.ax2.get_xlim()[0]) / 4,
                                                   c='r', ls='', pickradius=2), self.b_on_off_fft_cur)
        self.xfftcur2 = Cc.Cursor(self.ax2.axvline(self.ax2.get_xlim()[1] -
                                                   (self.ax2.get_xlim()[1] - self.ax2.get_xlim()[0]) / 4,
                                                   c='r', ls='', pickradius=2), self.b_on_off_fft_cur)
        self.yfftcur1 = Cc.Cursor(self.ax2.axhline(self.ax2.get_ylim()[0] +
                                                   (self.ax2.get_ylim()[1] - self.ax2.get_ylim()[0]) / 4,
                                                   c='r', ls='', pickradius=2), self.b_on_off_fft_cur)
        self.yfftcur2 = Cc.Cursor(self.ax2.axhline(self.ax2.get_ylim()[1] -
                                                   (self.ax2.get_ylim()[1] - self.ax2.get_ylim()[0]) / 4,
                                                   c='r', ls='', pickradius=2), self.b_on_off_fft_cur)

        self.data1 = None
        self.data2 = None
        self.data3 = None
        self.data4 = None

        # creating blitting manager
        self.bm = BMc.BlitManager(self.fig.canvas,
                                  [self.line1, self.line2, self.line3, self.line4,
                                   self.line_fft_1, self.line_fft_2, self.line_fft_3, self.line_fft_4,
                                   self.trigger, self.xcur1.line, self.xcur2.line, self.ycur1.line, self.ycur2.line,
                                   self.xfftcur1.line, self.xfftcur2.line, self.yfftcur1.line, self.yfftcur2.line,
                                   self.t_1_l, self.t_1_r, self.t_2_l, self.t_2_r])

        # making plot visible
        plt.show(block=False)
        plt.pause(.1)

    def update(self, data1=None, data2=None, data3=None, data4=None):
        if self.b_run_stop.color == '#4cd147':
            if self.b_on_off_tr.color == '0.85':
                if data1 is not None and self.b_on_off_1.color == '#f4bb32':
                    xdata = np.linspace(-np.round(self.x_max_span / 2, 1), np.round(self.x_max_span / 2, 1), len(data1))
                    self.line1.set_data(xdata, (data1 * (2 ** self.sl_y_sc_1.val)) + self.sl_y_sh_1.val)
                    self.data1 = data1

                    if self.b_on_off_s.color == '0.95':
                        ydata = fft.fft(data1)[:len(data1) // 2]
                        xdata = np.linspace(0, 22050, len(ydata))

                        self.line_fft_1.set_data(xdata, np.abs(ydata) * 2 / len(ydata))

                if data2 is not None and self.b_on_off_2.color == '#81b78f':
                    xdata = np.linspace(-np.round(self.x_max_span / 2, 1), np.round(self.x_max_span / 2, 1), len(data2))
                    self.line2.set_data(xdata, (data2 * (2 ** self.sl_y_sc_2.val)) + self.sl_y_sh_2.val)
                    self.data2 = data2

                    if self.b_on_off_s.color == '0.95':
                        ydata = fft.fft(data2)[:len(data2) // 2]
                        xdata = np.linspace(0, 22050, len(ydata))

                        self.line_fft_2.set_data(xdata, np.abs(ydata) * 2 / len(ydata))

                if data3 is not None and self.b_on_off_3.color == '#6590d8':
                    xdata = np.linspace(-np.round(self.x_max_span / 2, 1), np.round(self.x_max_span / 2, 1), len(data3))
                    self.line3.set_data(xdata, (data3 * (2 ** self.sl_y_sc_3.val)) + self.sl_y_sh_3.val)
                    self.data3 = data3

                    if self.b_on_off_s.color == '0.95':
                        ydata = fft.fft(data3)[:len(data3) // 2]
                        xdata = np.linspace(0, 22050, len(ydata))

                        self.line_fft_3.set_data(xdata, np.abs(ydata) * 2 / len(ydata))

                if data4 is not None and self.b_on_off_4.color == '#de8fb9':
                    xdata = np.linspace(-np.round(self.x_max_span / 2, 1), np.round(self.x_max_span / 2, 1), len(data4))
                    self.line4.set_data(xdata, (data4 * (2 ** self.sl_y_sc_4.val)) + self.sl_y_sh_4.val)
                    self.data4 = data4

                    if self.b_on_off_s.color == '0.95':
                        ydata = fft.fft(data4)[:len(data4) // 2]
                        xdata = np.linspace(0, 22050, len(ydata))

                        self.line_fft_4.set_data(xdata, np.abs(ydata) * 2 / len(ydata))
            else:
                if data1 is not None and self.b_on_off_1.color == '#f4bb32' and self.r_b.value_selected == 'Channel 1':
                    tr_range = data1[len(data1) // 4 - 1:3 * len(data1) // 4 + 1]
                    k = None

                    for i in range(len(tr_range) - 1):
                        if tr_range[i] + self.sl_y_sh_1.val / (2 ** self.sl_y_sc_1.val) < \
                                self.sl_tr.val / (2 ** self.sl_y_sc_1.val) < \
                                tr_range[i + 1] + self.sl_y_sh_1.val / (2 ** self.sl_y_sc_1.val):
                            k = i
                            break

                    if k is not None:
                        data1_tr = data1[k:k + len(data1) // 2]
                        xdata = np.linspace(-np.round(self.x_max_span / 2, 1),
                                            np.round(self.x_max_span / 2, 1), len(data1_tr))

                        self.line1.set_data(xdata, (data1_tr * (2 ** self.sl_y_sc_1.val)) + self.sl_y_sh_1.val)

                        if self.b_on_off_s.color == '0.95':
                            ydata = fft.fft(data1_tr)[:len(data1_tr) // 2]
                            xdata = np.linspace(0, 22050, len(ydata))

                            self.line_fft_1.set_data(xdata, np.abs(ydata) * 2 / len(ydata))

                if data2 is not None and self.b_on_off_2.color == '#81b78f' and self.r_b.value_selected == 'Channel 2':
                    tr_range = data2[len(data2) // 4 - 1:3 * len(data2) // 4 + 1]
                    k = None

                    for i in range(len(tr_range) - 1):
                        if tr_range[i] + self.sl_y_sh_2.val / (2 ** self.sl_y_sc_2.val) < \
                                self.sl_tr.val / (2 ** self.sl_y_sc_2.val) < \
                                tr_range[i + 1] + self.sl_y_sh_2.val / (2 ** self.sl_y_sc_2.val):
                            k = i
                            break

                    if k is not None:
                        data2_tr = data2[k:k + len(data2) // 2]
                        xdata = np.linspace(-np.round(self.x_max_span / 2, 1),
                                            np.round(self.x_max_span / 2, 1), len(data2_tr))

                        self.line2.set_data(xdata, (data2_tr * (2 ** self.sl_y_sc_2.val)) + self.sl_y_sh_2.val)

                        if self.b_on_off_s.color == '0.95':
                            ydata = fft.fft(data2_tr)[:len(data2_tr) // 2]
                            xdata = np.linspace(0, 22050, len(ydata))

                            self.line_fft_2.set_data(xdata, np.abs(ydata) * 2 / len(ydata))

                if data3 is not None and self.b_on_off_3.color == '#6590d8' and self.r_b.value_selected == 'Channel 3':
                    tr_range = data3[len(data3) // 4 - 1:3 * len(data3) // 4 + 1]
                    k = None

                    for i in range(len(tr_range) - 1):
                        if tr_range[i] + self.sl_y_sh_3.val / (2 ** self.sl_y_sc_3.val) < \
                                self.sl_tr.val / (2 ** self.sl_y_sc_3.val) < \
                                tr_range[i + 1] + self.sl_y_sh_3.val / (2 ** self.sl_y_sc_3.val):
                            k = i
                            break

                    if k is not None:
                        data3_tr = data3[k:k + len(data3) // 2]
                        xdata = np.linspace(-np.round(self.x_max_span / 2, 1),
                                            np.round(self.x_max_span / 2, 1), len(data3_tr))

                        self.line3.set_data(xdata, (data3_tr * (2 ** self.sl_y_sc_3.val)) + self.sl_y_sh_3.val)

                        if self.b_on_off_s.color == '0.95':
                            ydata = fft.fft(data3_tr)[:len(data3_tr) // 2]
                            xdata = np.linspace(0, 22050, len(ydata))

                            self.line_fft_3.set_data(xdata, np.abs(ydata) * 2 / len(ydata))

                if data4 is not None and self.b_on_off_4.color == '#de8fb9' and self.r_b.value_selected == 'Channel 4':
                    tr_range = data4[len(data4) // 4 - 1:3 * len(data4) // 4 + 1]
                    k = None

                    for i in range(len(tr_range) - 1):
                        if tr_range[i] + self.sl_y_sh_4.val / (2 ** self.sl_y_sc_4.val) < \
                                self.sl_tr.val / (2 ** self.sl_y_sc_4.val) < \
                                tr_range[i + 1] + self.sl_y_sh_4.val / (2 ** self.sl_y_sc_4.val):
                            k = i
                            break

                    if k is not None:
                        data4_tr = data4[k:k + len(data4) // 2]
                        xdata = np.linspace(-np.round(self.x_max_span / 2, 1),
                                            np.round(self.x_max_span / 2, 1), len(data4_tr))

                        self.line4.set_data(xdata, (data4_tr * (2 ** self.sl_y_sc_4.val)) + self.sl_y_sh_4.val)

                        if self.b_on_off_s.color == '0.95':
                            ydata = fft.fft(data4_tr)[:len(data4_tr) // 2]
                            xdata = np.linspace(0, 22050, len(ydata))

                            self.line_fft_4.set_data(xdata, np.abs(ydata) * 2 / len(ydata))

            if self.flag1:
                self.b_run_stop.color = '0.85'
                self.b_run_stop.hovercolor = '0.95'
                self.flag1 = False

        if self.b_on_off_cur.color == '#4cd147':
            self.t_1_l.set_text(r'$\Delta x = $' + str(np.round(np.abs(self.xcur1.line.get_xdata()[0] -
                                                                       self.xcur2.line.get_xdata()[0]), 1)))
            if self.r_b.value_selected == 'Channel 1':
                self.t_1_r.set_text(r'$\Delta y = $' + str(np.round(np.abs(self.ycur1.line.get_ydata()[0] -
                                                                           self.ycur2.line.get_ydata()[0]) /
                                                                    (2 ** self.sl_y_sc_1.val), 3)))
            elif self.r_b.value_selected == 'Channel 2':
                self.t_1_r.set_text(r'$\Delta y = $' + str(np.round(np.abs(self.ycur1.line.get_ydata()[0] -
                                                                           self.ycur2.line.get_ydata()[0]) /
                                                                    (2 ** self.sl_y_sc_2.val), 3)))
            elif self.r_b.value_selected == 'Channel 3':
                self.t_1_r.set_text(r'$\Delta y = $' + str(np.round(np.abs(self.ycur1.line.get_ydata()[0] -
                                                                           self.ycur2.line.get_ydata()[0]) /
                                                                    (2 ** self.sl_y_sc_3.val), 3)))
            elif self.r_b.value_selected == 'Channel 4':
                self.t_1_r.set_text(r'$\Delta y = $' + str(np.round(np.abs(self.ycur1.line.get_ydata()[0] -
                                                                           self.ycur2.line.get_ydata()[0]) /
                                                                    (2 ** self.sl_y_sc_4.val), 3)))
        else:
            self.t_1_l.set_text('')
            self.t_1_r.set_text('')

        if self.b_on_off_fft_cur.color == '#4cd147':
            self.t_2_l.set_text(r'$\Delta x = $' + str(np.round(np.abs(self.xfftcur1.line.get_xdata()[0] -
                                                                       self.xfftcur2.line.get_xdata()[0]), 3)))
            self.t_2_r.set_text(r'$\Delta x = $' + str(np.round(np.abs(self.yfftcur1.line.get_ydata()[0] -
                                                                       self.yfftcur2.line.get_ydata()[0]), 3)))
        else:
            self.t_2_l.set_text('')
            self.t_2_r.set_text('')

        self.bm.update()
