import csv
import re
import requests
from http import cookiejar
from bs4 import BeautifulSoup as bs
import xlwt
path = r"D:\MyCodes\MyPython\Mr_He\Python_MR_He\粉丝数据.csv"
file = open(path, "r")
reader = csv.reader(file)
num = 0

book = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet = book.add_sheet('何同学粉丝信息', cell_overwrite_ok=True)
n = 0

#设置 cookie
s = requests.Session()
s.cookies=cookiejar.CookieJar()
Level = []      #等级、性别等个人信息果然不出我所料也在Ajax异步里边儿
Name = []
Sex = []
Coin = []


def get_info(url):
    url = "http:" + url
    headers = {
        'Host': 'api.bilibili.com',
        'Referer': url,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'X-DevTools-Emulate-Network-Conditions-Client-Id': 'A20EA5B172E6DC82709D213A40AD0E8F'
    }
    url2 = str((re.findall(r"\d+", url))[0])
    url2 = r"https://api.bilibili.com/x/space/acc/info?mid=" + url2 + "&jsonp=jsonp"
    response = s.get(url2, headers=headers)
    soup = bs(response.text, 'html.parser')
    text = str(soup)
    list = re.split(r'"', text)
    if len(list) >= 16:         #防止有时候越界
        name = list[15]         #split后一个一个找出对应数据位置（毕竟都有规律嘛）
    if len(list) >= 20:
        sex = list[19]
    if len(list) >= 33:
        level = re.findall(r"\d+", list[32])[0]
    if len(list) >= 45:
        coin = re.findall(r"\d+", list[44])[0]
    print(name, sex, level, coin)
    Level.append(level)
    Name.append(name)
    Coin.append(coin)
    Sex.append(sex)
    global n        #global关键字可以对全局变量进行修改！
    sheet.write(n, 0, name)
    sheet.write(n, 1, sex)
    sheet.write(n, 2, level)
    sheet.write(n, 3, coin)
    n += 1


for row in reader:
    url = row[0]
    get_info(url)
book.save(u'何同学粉丝信息.xlsx')