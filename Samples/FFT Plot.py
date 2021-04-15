import scipy.fft as fft
import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd

# Number of sample points
N = 600
# sample spacing
T = 1.0 / 800.0
x = np.linspace(0.0, N*T, N, endpoint=False)
y = np.sin(50.0 * 2.0*np.pi*x) + 0.5*np.sin(80.0 * 2.0*np.pi*x)
yf = fft.fft(y)[:N//2]
xf = fft.fftfreq(N, T)[:N//2]

# signal = np.array([-2, 8, 6, 4, 1, 0, 3, 5, -3, 4], dtype=float)
# fourier = fft.rfft(signal)
# n = signal.size
# sample_rate = 100
# freq = fft.rfftfreq(n, d=1./sample_rate)

plt.style.use('dark_background')
plt.plot(xf, np.abs(yf), '#00ff1e')
plt.grid()
plt.show()
