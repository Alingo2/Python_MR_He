import matplotlib.pyplot as plt
import csv
path = r"D:\MyCodes\MyPython\Mr_He\Python_MR_He\何同学粉丝信息.csv"
file = open(path, "r")
reader = csv.reader(file)
Name = []
Sex = [0, 0, 0] #分别代表保密、男、女 用字典的话后续处理稍显麻烦
Level = [0, 0, 0, 0, 0, 0, 0]
for row in reader:
    name = row[0]
    sex = row[1]
    if sex == '保密':
        Sex[0] += 1
    elif sex == '男':
        Sex[1] += 1
    elif sex == '女':
        Sex[2] += 1
    level = eval(row[2])
    Level[level] += 1
    Name.append(name)
explode = [0.1, 0, 0]       #发现保密的占比最多  突出显示一下保密
fig, axes = plt.subplots()
plt.rcParams['font.sans-serif'] = ['SimHei']#需要正常显示中文
plt.axes(aspect=1)  # set this , Figure is round, otherwise it is an ellipse
# autopct ，show percet
plt.pie(x=Sex, labels=['保密', '男', '女'], explode= explode, autopct='%3.1f %%',
        shadow=True, labeldistance=1.1, startangle=90, pctdistance=0.6
        )
plt.show()
'''
labeldistance，文本的位置离原点有多远，1.1指1.1倍半径的位置
autopct，圆里面的文本格式，%3.1f%%表示小数有三位，整数有一位的浮点数
shadow，饼是否有阴影
startangle，起始角度，0，表示从0开始逆时针转，为第一块。一般选择从90度开始比较好看
pctdistance，百分比的text离圆心的距离
patches, l_texts, p_texts，为了得到饼图的返回值，p_texts饼图内部文本的，l_texts饼图外label的文本
'''
explode = [0.1, 0, 0, 0, 0, 0, 0]         #突出显示一下0级的号
plt.pie(x=Level, labels=['0级', '1级', '2级', '3级', '4级', '5级', '6级'], explode= explode, autopct='%3.1f %%',
        shadow=True, labeldistance=1.1, startangle=90, pctdistance=0.6
        )
plt.show()
