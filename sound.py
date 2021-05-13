import numpy as np
import sounddevice as sd
import Interface_class as Ic


sd.default.latency = [0.0, 0.0]
samplerate = sd.query_devices(sd.default.device, 'input')['default_samplerate']
blocksize = 1024 * 2
data = np.zeros([blocksize])
interface = Ic.Interface(blocksize, samplerate)

# while True:
#     data1 = np.sin(np.linspace(0, 8 * np.pi, 2049))
#     data2 = np.cos(np.linspace(0, 8 * np.pi, 2049))
#     interface.update(data1, data2)

stream = sd.InputStream(channels=2, blocksize=blocksize, latency=0.0)

with stream as s:
    while True:
        data, over = s.read(blocksize)
        interface.update(data[:, 0], data[:, 1])
