import requests
from pyquery import PyQuery as pq

headers = {
    'Host': 'm.weibo.cn',
    'Referer': 'https://m.weibo.cn/u/6529876887?uid=6529876887&luicode=10000011&lfid=1076036529876887&featurecode=20000320',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'X-DevTools-Emulate-Network-Conditions-Client-Id': 'A20EA5B172E6DC82709D213A40AD0E8F'
}
#header里边儿配置了何同学微博的主页，我尝试过用网页PC端的微博，发现爬取时的异步链接似乎没有规律，于是尝试改用m.开头的手机移动端登陆微博进行爬取

def get_page(page):
    url = 'https://m.weibo.cn/api/container/getIndex?uid=6529876887&luicode=10000011&lfid=1076036529876887&featurecode=20000320&type=uid&value=6529876887&containerid=1076036529876887&page=%d' % page
    #因为转发量、评论数、点赞数这些都是动态数据，是Ajax异步加载的，这个url就是异步加载时的申请链接
    try:
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return res.json()
    except requests.ConnectionError as e:
        print("Error", e.args)


def parse_page(json):
#处理返回回来的json信息，这里要得到这些信息头，得读取网页的json文件，我是用的chrome所以直接使用的jsonview插件
    if json:
        items = json.get('data').get('cards')
        for item in items:
            item = item.get('mblog')
            weibo = {}
            weibo['text'] = pq(item.get('text')).text()
            weibo['attitudes'] = item.get('attitudes_count')
            weibo['comments'] = item.get('comments_count')
            weibo['reposts'] = item.get('reposts_count')
            yield weibo


if __name__ == '__main__':
#打包整理信息
    data = ''
    for page in range(1, 200):
        json = get_page(page)
        results = parse_page(json)
        for res in results:
            data += '\n'.join(
                [res['text'], '【评论数: ' + str(res['comments']) + ' 转发数: ' + str(res['reposts']) + ' 点赞数: ' + str(res['attitudes']) + '】\n\n'])
    with open('weibo.txt', 'w', encoding='utf-8') as f:
        f.write(data)