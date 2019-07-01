import numpy as np
import cv2
from PIL import Image

cap = cv2.VideoCapture(r"何同学.avi")   #创建一个VideoCapture对象
# set blue thresh 设置HSV中颜色范围
lower_blue = np.array([0, 0, 0])
upper_blue = np.array([100, 100, 100])
score = 0
FrameNumber = 0
subtitle_start = 0
subtitle_end = 0
mark_height = 0
width = 0
height = 0

def basic_info():                           #统计视频基本信息
    if cap.isOpened(): # 当成功打开视频时cap.isOpened()返回True,否则返回False
        global score, subtitle_end, subtitle_start, FrameNumber,mark_height,width, height                #修改全局变量
        width = cap.get(3)
        height = cap.get(4)
        score += 100*(width*height)/(2048*1080)
        subtitle_start = int(height*0.83)
        mark_height = int(height*0.11)
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
    return


def get_img_info(frame):
    if frame is not None:
        Im = []
        #img = Image.fromarray(frame)
        im = frame[:, :, 0]
        im1 = im[subtitle_start:subtitle_end, :]    #确定字幕的范围，注意不同的视频文件剪切的索引值不同
        im2 = im[0:mark_height, int(width)-int(width*0.22):int(width)]                  #右上角水印
        im3 = im[0:mark_height, 0:int(width*0.22)]                      #左上角水印
        #img = Image.fromarray(im1)
        thresh = 220                                #将二值化阈值设为 220
        thresh2 = 130                               #水印虽然也是白色 但要淡很多
        _, im1 = cv2.threshold(im1, thresh, 255, cv2.THRESH_BINARY)
        _, im2 = cv2.threshold(im2, thresh2, 255, cv2.THRESH_BINARY)
        _, im3 = cv2.threshold(im3, thresh2, 255, cv2.THRESH_BINARY)
        Im.append(im1)
        Im.append(im2)
        Im.append(im3)
    return Im


basic_info()
#字幕打分：
Frame = []          #将每帧的信息打包为列表
sub_count = 0
n = 0
for i in range(FrameNumber-1):        #这里随机取了视频的第300帧来检测水印，因为水印肯定是要么没有要么一直存在的
    if n <= 300:
        n += 1
    sucess, frame = cap.read()
    if n == 300:
        global mark_dect
        mark_dect = frame
    im = get_img_info(frame)[0]
    if ((im ** 2).sum() / im.size * 100) > 1:
        sub_count += 1
        print(sub_count)
if sub_count/FrameNumber > 0.5:
    score += 100
else:
    score += 100*(sub_count/FrameNumber)/0.5
print("字幕占比：", 100*sub_count/FrameNumber, "％")

#水印检测：
im1 = get_img_info(mark_dect)[1]
im2 = get_img_info(mark_dect)[2]
img1 = Image.fromarray(im1)
img1.show()
img2 = Image.fromarray(im2)
img2.show()
if ((im1 ** 2).sum() / im1.size * 100) > 1 and ((im2 ** 2).sum() / im2.size * 100) > 1:         #有两条水印
    print("水印超过两条，怀疑为盗视频")
    score -= 200
else:
    print("水印小于等于1条")
    score += 200

print("你的视频得分为：", score, "分")
if score > 400:
    print("此视频质量很好")
else:
    print("此视频质量有待提高")
cap.release()
cv2.destroyAllWindows()
