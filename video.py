
import numpy as np
import cv2
from PIL import Image

cap = cv2.VideoCapture(r"何同学.avi")   #创建一个VideoCapture对象
# set blue thresh 设置HSV中颜色范围
lower_blue = np.array([0, 0, 0])
upper_blue = np.array([100, 100, 100])
score = 0
FrameNumber = 0
#统计视频基本信息
if cap.isOpened(): # 当成功打开视频时cap.isOpened()返回True,否则返回False
    width = cap.get(3)
    height = cap.get(4)
    score += 100*(width*height)/(2048*1080)
    subtitle_start = int(height*0.83)
    subtitle_end = int(subtitle_start+height*0.13)      #我自己测试算得大概屏占比为13％
    rate = cap.get(5)               #5对应的参数：帧速率
    FrameNumber = int(cap.get(7))        #7对应的参数：视频文件的帧数
    duration = FrameNumber/rate/60    # 帧速率/视频总帧数 是时间，除以60之后单位是分钟   即视频长度
    if 5 < duration <= 10:
        score += 100
    elif 10 < duration <= 20 or 0 <= duration <= 5:
        score += 80
    else:
        score += 60/(duration-20)
    score += (rate/30)*100
    print(width, height, rate, FrameNumber, duration, 'minutes')


def get_img_info(frame):
    if frame is not None:
        img = Image.fromarray(frame)
        im = frame[:, :, 0]
        im = im[subtitle_start:subtitle_end, :]    #确定字幕的范围，注意不同的视频文件剪切的索引值不同
        img = Image.fromarray(im)
        thresh = 220        #将二值化阈值设为 220
        _, im = cv2.threshold(im, thresh, 255, cv2.THRESH_BINARY)
        img = Image.fromarray(im)
        #img.show()
    return im


Frame = []          #将每帧的信息打包为列表
count = 0
for i in range(FrameNumber-1):
    sucess, frame = cap.read()
    im = get_img_info(frame)
    if ((im ** 2).sum() / im.size * 100) > 1:
        count += 1
        print(count)
if count/FrameNumber > 0.5:
    score += 100
else:
    score += 100*(count/FrameNumber)/0.5
print("字幕占比：", 100*count/FrameNumber, "％")
print("你的视频得分为：", score, "分")

"""while(True):
    # get a frame and show 获取视频帧并转成HSV格式, 利用cvtColor()将BGR格式转成HSV格式，参数为cv2.COLOR_BGR2HSV。
    ret, frame = cap.read()
    frame = cv2.resize(frame, (320, 240))
    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    #cv2.imshow('frame', gray)
    # change to hsv model
    cv2.imshow('Capture', frame)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # get mask 利用inRange()函数和HSV模型中蓝色范围的上下界获取mask，mask中原视频中的蓝色部分会被弄成白色，其他部分黑色。
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    cv2.imshow('Mask', mask)

    # detect blue 将mask于原视频帧进行按位与操作，则会把mask中的白色用真实的图像替换：
    res = cv2.bitwise_and(frame, frame, mask=mask)
    cv2.imshow('Result', res)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()"""