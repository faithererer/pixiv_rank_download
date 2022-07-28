# pixiv_rank_download

下载p站排行榜原图

## 使用说明

你需要下载到你本地，并安装以下依赖

```
pip install requests
pip install lxml
pip install json
```

在运行前你需要填写以下参数：

```python
# 你需要填写的=================================================

# mode(可填) 有daily(今日),weekly(每周),monthly(每月),rookie(新人),original(原创),male(受男性欢迎),female(受女性欢迎)七种mode，默认为daily
mode = "monthly"

# content(可填)  有illust(插画),默认为综合
content = "illust"

# page(必填) 你要下载的页数，注意:每一页有50张图片
page = 2

# filepath(选填)默认为该目录下的img如没有可自行创建
filepath = 'img'
# ------------注意:如果你想应用上述这些参数请把data里面注释取消掉，不需要的参数请不要取消注释,data在main的开头附近


# proxies pixiv因GFW国内无法访问你需要一个代理,以下代理每个人都不一样需要自己填写
proxies = {
    'http': 'http://127.0.0.1:7890/',
    'https': 'http://127.0.0.1:7890/'
}
# =======================================================
```

##  关于代理

你可以在这个位置找到

![image-20220728153124190](https://blog-faithererer.oss-cn-qingdao.aliyuncs.com/blog/typoraImg202207281531728.png)