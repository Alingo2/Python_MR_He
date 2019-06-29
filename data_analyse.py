import matplotlib.pyplot as plt
import csv
import re
path = r"D:\MyCodes\MyPython\Mr_He\Python_MR_He\何同学视频.csv"
file = open(path, "r")
reader = csv.reader(file)
num = 0

Time = []
Biubiu = []
Watch_num = []
Name = []
for row in reader:
    author = row[6]
    if author =="老师好我叫何同学":
        num += 1
        time = re.findall(r"\d+\.?\d*", str(row[5]))   #用正则表达式把数字都筛一遍
        date = str(time[0])+"年"+str(time[1])+"月"+str(time[2])+"日"
        Time.append(date)
        watch_num = eval((re.findall(r"\d+\.?\d*", row[3]))[0])
        Watch_num.append(watch_num)
        Biubiu_num = eval((re.findall(r"\d+\.?\d*", row[4]))[0])  #因为正则表达式返回的是一个列表！
        Biubiu.append(Biubiu_num)
        Name.append(row[0])
print(num)
for i in range(0, num):
    print(Name[i], Watch_num[i], Biubiu[i], Time[i])
#图像绘制
fig, ax = plt.subplots()
pic = ax.barh(Time, Watch_num, color='#6699CC')
plt.rcParams['font.sans-serif'] = ['SimHei']#需要正常显示中文...换了几个字体似乎就这个可以正常显示...
plt.xlabel(u'                                                                       万') #强行制表符把单位加在右下角哈哈哈
plt.title('播放量与时间统计图', fontsize='large', fontweight='bold')
plt.show()

fig2, ax = plt.subplots()
pic2 = ax.barh(Time, Biubiu, color='blue')
plt.rcParams['font.sans-serif'] = ['SimHei']#需要正常显示中文...换了几个字体似乎就这个可以正常显示...
plt.title('弹幕数与时间统计图', fontsize='large', fontweight='bold')
plt.show()


