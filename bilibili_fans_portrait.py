import selenium as sel
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import xlwt

def get_source():
    WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#server-search-app > div.contain > div.body-contain > div > div.result-wrap.clearfix')))
    html = browser.page_source
    soup = BeautifulSoup(html,'lxml')
    #save_to_excel(soup)

browser = webdriver.Chrome()        #拿到浏览器的对象
WAIT = WebDriverWait(browser, 10)   #设置最长超时时间
browser.set_window_size(1400,900)

browser.get("https://bilibili.com/")    #访问b站

index = WAIT.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#primary_menu > ul > li.home > a")))
# 被那个登录遮住了 解决：先去主页刷新一下，再登陆
index.click()

input = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#banner_link > div > div > form > input")))
submit = WAIT.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="banner_link"]/div/div/form/button')))
#这里等到这个元素可操作的时候才会继续执行下一步获取到输入框元素后输入「何同学」  确保可以正常搜索

input.send_keys('老师好我叫何同学')
submit.click()


# 跳转到新的窗口
print('跳转到新窗口')
all_h = browser.window_handles
browser.switch_to.window(all_h[1])
get_source()