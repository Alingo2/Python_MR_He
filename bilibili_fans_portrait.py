from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
import xlwt
import requests
from http import cookiejar

def get_source():
    WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#server-search-app > div.contain > div.body-contain > div > div.result-wrap.clearfix')))
    html = browser.page_source
    soup = bs(html, 'lxml')
    #save_to_excel(soup)

browser = webdriver.Firefox()        #拿到浏览器的对象
WAIT = WebDriverWait(browser, 10)   #设置最长超时时间
browser.set_window_size(1400, 900)
header={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'
}       #Firefox的用户代理

def search():
    try:
        print('访问b站....')
        browser.get("https://bilibili.com/")    #访问b站
        s = requests.Session()
        s.cookies = cookiejar.CookieJar()

        index = WAIT.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#primary_menu > ul > li.home > a")))
        # 被那个登录遮住了 解决：先去主页刷新一下，再登陆
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
        return int(total)
    except TimeoutException:
        return search()

def get_pagenum(site):
    soup = bs(site.text, 'html.parser')
    Num = soup.find_all('button', class_='pagination-btn num-btn')
    count = 0   #统计一下有几页
    for i in Num:
        count += 1
    print(count)
    return count
#主函数
total=search()
print(total)
