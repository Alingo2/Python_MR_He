import wave  #音频处理库
import numpy as np
import matplotlib.pyplot as plt   #专业绘图库
from PIL import Image

img = Image.open(r"pic.png")
img.show()  #系统自带软件来显示图片

filepath = r"何同学.wav"
fwav = wave.open(filepath,)
print(fwav)

params = fwav.getparams()
print(params)

nchannels, sampwidth, framerate, nframes = params[:4]
strData = fwav.readframes(nframes)
w = np.fromstring(strData, dtype=np.int16)
w = w * 1.0 / (max(abs(w)))
w = np.reshape(w, [nframes, nchannels])  # 数据转为二维直角坐标

# 绘制波形图 第一个声道波形图
time = np.arange(0, nframes) * (1.0 / framerate)
plt.figure()
plt.subplot(5, 1, 1)
plt.plot(time, w[:, 0])
plt.xlabel("Time(s)")
plt.title("First Channel")
plt.show()
img.save("1.png")

# 绘制第二个声道的波形图
plt.subplot(5, 1, 2)
plt.plot(time, w[:, 1])
plt.xlabel("Time(s)")
plt.title("Second Channel")
img.save("result/Second Channel.png")

# 加大两幅图的距离
plt.subplot(5, 1, 3)
plt.plot(time, w[:, 1])
plt.xlabel("Time(s)")
plt.title("Second Channel")
img.save("result/Second1 Channel.png")