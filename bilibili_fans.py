from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
import xlwt
import requests
from http import cookiejar

browser = webdriver.Chrome()        #拿到浏览器的对象
browser.set_window_size(1400, 900)
WAIT = WebDriverWait(browser, 5)   #设置最长超时时间
header={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}       #Chrome的用户代理

print('访问b站....')
browser.get("https://space.bilibili.com/163637592/fans/fans")    #访问b站

Url = []
Name = []
book = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet = book.add_sheet('粉丝数据', cell_overwrite_ok=True)
sheet.write(0, 0, '粉丝名')
sheet.write(0, 1, '地址')
n = 1


def get_fans(i):
    print("第 %d 页开始爬取" % i)
    html = browser.page_source
    soup = bs(html, 'lxml')
    if soup.find('div', class_='s-space'):
        List = soup.find('div', class_='s-space').find_all('li', class_='list-item clearfix')
        for item in List:
            url = item.find('a').get('href')
            Url.append(url)
            name = item.find('span').get('vip-name-check fans-name')
            Name.append(name)
            global n  # global关键字可以对全局变量进行修改！
            sheet.write(n, 0, name)
            sheet.write(n, 1, url)
            n += 1

    else:
        return get_fans(i)

def get_the_page(i):
    try:
        print("开始访问第 %d 页" % i)       #尝试一下格式化输出~
        get_fans(i)
        next_btn = WAIT.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#server-search-app > div.contain > div.body-contain > div > div.page-wrap > div > ul > li.page-item.next > button')))
        next_btn.click()
    except TimeoutException:        #如果超时，应该是在最后一页了（nextbutton 不存在 超时）
        return


for i in range(1, 100):
    get_the_page(i)
print(Name)
print(Url)
book.save(u'粉丝数据.xlsx')