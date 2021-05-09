import numpy as np
import sounddevice as sd
import FFT2


sd.default.latency = [0.0, 0.0]
samplerate = sd.query_devices(sd.default.device, 'input')['default_samplerate']
blocksize = 1024 * 2
data = np.zeros([blocksize])
fig, sl_x_sc, sl_x_sh, \
    b_on_off_1, line1, sl_y_sc_1, sl_y_sh_1, \
    b_on_off_2, line2, sl_y_sc_2, sl_y_sh_2, \
    b_on_off_s, line_fft_1, line_fft_2, r_sl, dot, \
    xcur1, xcur2, ycur1, ycur2, b_on_off_cur, \
    b_reset, b_single, b_run_stop, b_on_off_tr, \
    sl_tr, bm = FFT2.format_figure(blocksize)

stream = sd.InputStream(channels=2, blocksize=blocksize, latency=0.0)

with stream as s:
    while True:
        data, over = s.read(blocksize)
        if b_run_stop.color == '#4cd147':
            if b_on_off_1.color == '#f4bb32':
                FFT2.update(fig, line1, data[:, 0], sl_x_sc.val, sl_y_sc_1.val, sl_x_sh.val, sl_y_sh_1.val)
                if b_on_off_s.color == '0.95':
                    FFT2.update_fft(fig, line_fft_1, data[:, 0])

            if b_on_off_2.color == '#81b78f':
                FFT2.update(fig, line2, data[:, 1], sl_x_sc.val, sl_y_sc_2.val, sl_x_sh.val, sl_y_sh_2.val)
                if b_on_off_s.color == '0.95':
                    FFT2.update_fft(fig, line_fft_2, data[:, 1])

        bm.update()
