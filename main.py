# _*_ coding : utf-8 _*_
# @Time : 2022/7/27 9:13
# @File : main
# @Project : pixiv
import time
import random
import requests
import urllib3
from lxml import etree
import json
# 关闭在设置了verify=False后的错误提示
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
urllib3.disable_warnings()

# 你需要填写的=================================================

# mode(可填)  有daily,weekly,monthly,rookie(新人),original(原创),male,female七种模式,默认为今日
mode = "monthly"

# content(可填)  有illust(插画),默认为综合
content = "illust"

# page(必填) 你要爬取多少页，注意:每一页有50张图片
page = 2

# filepath(选填)默认为该目录下的img如没有可自行创建
filepath = 'img'
# ------------注意:如果你想应用上述这些参数请把下面data里面注释取消掉，不需要的参数请不要取消注释


# proxies pixiv因GFW国内无法访问你需要一个代理,以下代理每个人都不一样需要自己填写
proxies = {
    'http': 'http://127.0.0.1:7890/',
    'https': 'http://127.0.0.1:7890/'
}
# =======================================================

# 参数

url_ranklist = 'https://www.pixiv.net/ranking.php?'
part_page_url = 'https://www.pixiv.net/artworks/'
headers_ranklist = {
"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36"
}

headers_download = {
    "accept-language": "zh-CN,zh;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36",
    "Referer": "https://www.pixiv.net/"
}



def session_dem(headers, url, params, trytimes):
    timec = 0
    while timec<trytimes:
        try:
            response = session.get(headers=headers, url=url, params=params, proxies=proxies, verify=False,timeout=(9, 30))
            return response
        except requests.exceptions.RequestException:
            print(f'出错了,尝试重连第{timec+1}次.....')
            timec = timec+1
            time.sleep(5)
        if timec == trytimes-1:
            print('===============失败！请检查你的网络设置==============')


if __name__ == '__main__':
    # 在session里访问防止请求次数过多被ban
    session = requests.session()
    session.keep_alive = False
    p = 1
    for p in range(1, page+1):
        data = {
            "mode": f"{mode}",
            "content": f"{content}",
            "p": f"{p}"
        }
        response = session_dem(url=url_ranklist, headers=headers_ranklist, params=data, trytimes=3)

        # 节点树
        tree = etree.HTML(response.text)

        # 找到所有id
        id_list = []
        for punch in tree:
            id_list = tree.xpath('//*[@id="wrapper"]/div[1]/div/div[2]/div[1]//section/@data-id')

        count = 0

        for unit in id_list:
            page_url = part_page_url+unit
            response = session_dem(headers=headers_download, url=page_url, params=None, trytimes=3)
            tree = etree.HTML(response.text)
            ori = tree.xpath('//*[@id="meta-preload-data"]/@content')
            ori = json.loads(str(ori[0]))
            print('正在下载来自:', ori['illust'][unit]['urls']['original'])
            response = session_dem(headers=headers_download, url=ori['illust'][unit]['urls']['original'], params=None, trytimes=3)
            print(f'下载成功,正在写入{unit}...')
            count = count + 1
            with open(f'{filepath}/{count}_{unit}.jpg', 'wb+') as fp:
                fp.write(response.content)
            print(f"写入{unit}成功,第{count}个,page:{p}")
            time.sleep(random.randint(0, 4))
    print('下载完成！')







