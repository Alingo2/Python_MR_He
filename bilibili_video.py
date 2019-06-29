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
WAIT = WebDriverWait(browser, 10)   #设置最长超时时间
browser.set_window_size(1400, 900)
header={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}       #Chrome的用户代理

book = xlwt.Workbook(encoding='utf-8', style_compression=0)

sheet = book.add_sheet('何同学视频', cell_overwrite_ok=True)
sheet.write(0, 0, '名称')
sheet.write(0, 1, '地址')
sheet.write(0, 2, '描述')
sheet.write(0, 3, '观看次数')
sheet.write(0, 4, '弹幕数')
sheet.write(0, 5, '发布时间')
sheet.write(0, 6, '作者')


n = 1

def save_to_excel(soup):
    list = soup.find(class_='all-contain').find_all(class_='info')
    print(list)
    for item in list:
        item_title = item.find('a').get('title')
        item_link = item.find('a').get('href')
        item_dec = item.find(class_='des hide').text
        item_view = item.find(class_='so-icon watch-num').text
        item_biubiu = item.find(class_='so-icon hide').text
        item_date = item.find(class_='so-icon time').text
        item_author = item.find(class_='up-name').text
        print('爬取：' + item_title)

        global n        #global关键字可以对全局变量进行修改！

        sheet.write(n, 0, item_title)
        sheet.write(n, 1, item_link)
        sheet.write(n, 2, item_dec)
        sheet.write(n, 3, item_view)
        sheet.write(n, 4, item_biubiu)
        sheet.write(n, 5, item_date)
        sheet.write(n, 6, item_author)

        n = n + 1

def get_source():
    WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#server-search-app > div.contain > div.body-contain > div > div.result-wrap.clearfix')))
    html = browser.page_source
    soup = bs(html, 'lxml')
    save_to_excel(soup)     #把数据添加到excel

def search():
    try:
        print('访问b站....')
        browser.get("https://bilibili.com/")    #访问b站
        s = requests.Session()
        s.cookies = cookiejar.CookieJar()

        index = WAIT.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#primary_menu > ul > li.home > a")))
        # 被那个登录遮住了 解决：先去主页刷新一下，再
        index.click()

        input = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#banner_link > div > div > form > input")))
        submit = WAIT.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="banner_link"]/div/div/form/button')))
        #这里等到这个元素可操作的时候才会继续执行下一步获取到输入框元素后输入「何同学」  确保可以正常搜索

        input.send_keys('老师好我叫何同学')
        submit.click()
        #输入搜索信息，提交

        #跳转到新的窗口
        print('跳转到新窗口')
        all_h = browser.window_handles
        browser.switch_to.window(all_h[1])
        print(str(browser.current_url))
        site = s.get(str(browser.current_url), headers=header)   #获取新网页当前的url 得转换成string
        get_source()

        total=get_pagenum(site)
        return total
    except TimeoutException:
        return search()

def get_pagenum(site):
    soup = bs(site.text, 'html.parser')
    Num = soup.find_all('button', class_='pagination-btn num-btn')
    count = 0                                                   #统计一下有几页
    for i in Num:
        count = count+1
    print(count)
    return count
def get_the_page(i):
    try:
        print("开始访问第 %d 页" % i)       #尝试一下格式化输出~
        next_btn = WAIT.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#server-search-app > div.contain > div.body-contain > div > div.page-wrap > div > ul > li.page-item.next > button')))
        next_btn.click()
        get_source()
    except TimeoutException:        #如果超时，应该是在最后一页了（nextbutton 不存在 超时）
        return

#主函数
def main():
    total = search()
    for i in range(1, total+1, 1):
        print(i)
        get_the_page(i)

main()
book.save(u'何同学视频.xlsx')        #一定记得保存！我检查了好久才发现自己少了这一句...