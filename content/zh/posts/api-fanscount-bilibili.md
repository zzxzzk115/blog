---
title: '轮子那点事儿(1)：获取 bilibili 粉丝数的 API 的制作'
date: 2020-11-02T21:15:26
categories: [后端]
tags: [tutorial, API, bilibili, codefromscratch, python]
toc: true
---

Subsats 的速度还是感人，我猜作者全是用 Selenium 爬的，能用 request 的为什么要用 Selenium？于是我打算自己做一个类似的 API 服务。我目前已经做好了获取 bilibili 粉丝数的服务，看看加载速度的对比效果吧（第一次加载才有意义，后面可能已经有缓存了就没有比较的必要了。左边是用的我自己做的 API，右边用的是 Subsats）：

<div class="align-left">
    <img src="https://img.shields.io/badge/dynamic/json?color=282c34&label=bilibili%E7%B2%89%E4%B8%9D%E6%95%B0&query=%24.data.value&url=http%3A%2F%2Fwww.zhangkexuan.cn%3A40001%2Fapi%2Ffanscount%2Fbilibili%2Fuid%2F33320940&logo=bilibili&labelColor=FE7398&logoColor=white" class="nofancybox">
    <img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.spencerwoo.com%2Fsubstats%2F%3Fsource%3Dbilibili%26queryKey%3D33320940&label=bilibili%20fans&query=$.data.totalSubs&color=282c34&logo=bilibili&labelColor=FE7398&logoColor=white" class="nofancybox">
</div>
<!--more-->

>  造轮子的定义：
>
> Reinventing the wheels
>
> 一般把可以直接使用的功能、库或是代码块比喻作轮子，那么我重新发明它的意义就在于，在它们能正常被我使用的前提下，我再重新学习、打一遍代码，使轮子背后的原理被自己彻底掌握。

这个项目里，Subsats 是轮子，我要造一个类似的。但我没必要完全自己从 0 开始制作，比如 fastapi、uvicorn、request、BeautifulSoup 这些 python 包我还是可以用的。

# 造前的分析

在用爬虫之前，我在想官方有没有提供开放的 API 接口来获取用户信息。因为之前已经见过很多 up 主展示自己的屏幕可以显示粉丝数，我觉得我去 b 站搜 `实时粉丝数` 就能得到这个 API 网址。

果不其然，我还是得到了：

`http://api.bilibili.com/x/web-interface/card?mid={uid}&;jsonp=jsonp&article=true`

`uid` 填写自己的 uid，可以访问自己的 bilibili 主页得到。

我的 uid 为 `33320940`,那么我可以通过访问 `http://api.bilibili.com/x/web-interface/card?mid=33320940&;jsonp=jsonp&article=true` 来得到相关 json 数据。

返回的内容为：

```json
{"code":0,"message":"0","ttl":1,"data":{"card":{"mid":"33320940","name":"Lazy_V","approve":false,"sex":"男","rank":"10000","face":"http://i0.hdslb.com/bfs/face/be95dbc3e9cc048ef8b661a2fab5d875ed206778.jpg","DisplayRank":"0","regtime":0,"spacesta":0,"birthday":"","place":"","description":"","article":0,"attentions":[],"fans":467,"friend":379,"attention":379,"sign":"软件工程大四，游戏公司offer已拿。业余网易音乐人。交流群:1049766562，欢迎交流你爱好的一切！","level_info":{"current_level":4,"current_min":0,"current_exp":0,"next_exp":0},"pendant":{"pid":0,"name":"","image":"","expire":0,"image_enhance":""},"nameplate":{"nid":7,"name":"见习搬运工","image":"http://i1.hdslb.com/bfs/face/8478fb7c54026cd47f09daa493a1b1683113a90d.png","image_small":"http://i1.hdslb.com/bfs/face/50eef47c3a30a75659d3cc298cfb09031d1a2ce5.png","level":"普通勋章","condition":"转载视频投稿通过总数\u003e=10"},"Official":{"role":0,"title":"","desc":"","type":-1},"official_verify":{"type":-1,"desc":""},"vip":{"vipType":0,"dueRemark":"","accessStatus":0,"vipStatus":0,"vipStatusWarn":"","theme_type":0}},"following":false,"archive_count":40,"article_count":1,"follower":467}}
```

很明显，`$.data.card.fans` 就是粉丝数。`code` 是响应码，`message` 是消息。

其实到这里，功能上讲，如果只考虑 bilibili 的话，我已经不用做了，因为这本身就已经满足 Shields.io 的规则了（url 和 query 已经都清楚了)。但是，为了做到整合多个接口，统一数据规范，做一个比 Subsats 速度更快更好的粉丝数查询 API 服务，我们还是要搭一架桥。

# 开造

## 根据需求导入包

要快速搭建 API 服务，服务器这边我采用 python，使用 fastapi 以及 uvicorn。可以参考我之前的一篇文章 [关于服务器通过 Python 搭建 API 服务](/posts/about-python-api)

我们还需要用到 python 的 request 和 json 两个包，这两个包应该是 python 默认自带的，如果没有，就用 pip 安装。它们分别对应请求 url 并获得数据、数据解析。

所以，服务端程序的前部分应该是这样：

```python
import uvicorn as uvicorn
from fastapi import FastAPI
import requests
import json

app = FastAPI()  # 必须实例化该类，启动的时候调用
```

## 添加完成核心功能的函数

添加一个函数，该函数完成的功能是：输入一个 uid，返回一个元组(status_code, fanscount, message)。即输入用户 ID，返回状态码、粉丝数、消息的一个元组。

函数的源码：

```python
def get_bilibili_fans_count(uid):

    status_code = 200
    message = "success"
    fanscount = 0

    headers = {"Connection": "close"}
    response = requests.get(f"http://api.bilibili.com/x/web-interface/card?mid={uid}&;jsonp=jsonp&article=true", headers).text
    
    json_response = json.loads(response)
    
    status_code = json_response.get("code")
    message = json_response.get("message")

    if status_code != 0:
        fanscount = -1
        print(message)
    else:
        status_code = 200
        fanscount = json_response.get("data").get("card").get("fans")
        print("bilibili粉丝数：" + str(fanscount))
    return status_code, fanscount, message
```

函数的过程就是：

1. 初始化变量 status_code，fanscount，message
2. 同 request 请求 api 网址，得到响应文本 response
3. 用 json 解析 response，先得到 code(响应码)
4. 判断 code 的值，
   1. 如果 code 不为 0，代表参数有误，把 fanscount 设置为-1，代表错误值。
   2. 如果 code 为 0，我们把 code 定义为自己定义的正确响应码，这里我设置为 200。然后可以通过 json 解析获取到 fans 的值。
5. 最后返回 status_code，fanscount，message

## 添加 fastapi 的响应函数

```python
@app.get('/api/fanscount/bilibili/uid/{uid}')
def bilibili_fans(uid: str):
    status_code, fanscount, message = get_bilibili_fans_count(uid)
    return {'status' : status_code, "message":message, "data" : { "value" : fanscount}}
```

## 目前 bilibili 部分的完整源码

```python
import uvicorn as uvicorn
from fastapi import FastAPI
import re
import requests
import json


app = FastAPI()  # 必须实例化该类，启动的时候调用


def get_bilibili_fans_count(uid):

    status_code = 200
    message = "success"
    fanscount = 0

    headers = {"Connection": "close"}
    response = requests.get(f"http://api.bilibili.com/x/web-interface/card?mid={uid}&;jsonp=jsonp&article=true", headers).text
    
    json_response = json.loads(response)
    
    status_code = json_response.get("code")
    message = json_response.get("message")

    if status_code != 0:
        fanscount = -1
        print(message)
    else:
        status_code = 200
        fanscount = json_response.get("data").get("card").get("fans")
        print("bilibili粉丝数：" + str(fanscount))
    return status_code, fanscount, message


# 请求根目录
@app.get('/')
def index():
    return {'message': '欢迎来到FastApi 服务！'}


@app.get('/api/fanscount/bilibili/uid/{uid}')
def bilibili_fans(uid: str):
    status_code, fanscount, message = get_bilibili_fans_count(uid)
    return {'status' : status_code, "message":message, "data" : { "value" : fanscount}}


if __name__ == '__main__':
    uvicorn.run(app=app, host="0.0.0.0", port=40001)
```

# 效果

端口号我设置为 40001，我的服务器 A 类解析的域名为 `www.zhangkexuan.cn`。运行服务端程序以后，API 服务就启动了。

访问 `http://www.zhangkexuan.cn:40001/api/fanscount/bilibili/uid/33320940`

即可得到粉丝数：[点击访问](http://www.zhangkexuan.cn:40001/api/fanscount/bilibili/uid/33320940)

结果:

```json
{"status":200,"message":"0","data":{"value":469}}
```

如果故意输入错误的值：

`http://www.zhangkexuan.cn:40001/api/fanscount/bilibili/uid/abcd`

则会立马返回：

```json
{"status":-400,"message":"strconv.ParseInt: parsing \"abcd\": invalid syntax","data":{"value":-1}}
```

输入一个不存在的 id：

`http://www.zhangkexuan.cn:40001/api/fanscount/bilibili/uid/-1`

也会立马得到错误信息：

```json
{"status":-400,"message":"Key: 'Mid' Error:Field validation for 'Mid' failed on the 'min' tag","data":{"value":-1}}
```

对于同一个 uid 的请求，我们打开 Chrome 的开发者控制台，看看速度：

我的 FansCount（先这么叫吧，名字说实话还没想好）:

![fanscount-speed](/img/markdown_20201102224651.png)

Subsats:

![substat-speed](/img/markdown_20201102224746.png)

好家伙，这速度差别，我直接好家伙。120ms 和 2.34s 的差别！

# 使用

可以把下面代码里的 `33320940` 改为你自己的 uid，就能显示啦！

```html
<img src="https://img.shields.io/badge/dynamic/json?color=282c34&label=bilibili%E7%B2%89%E4%B8%9D%E6%95%B0&query=%24.data.value&url=http%3A%2F%2Fwww.zhangkexuan.cn%3A40001%2Fapi%2Ffanscount%2Fbilibili%2Fuid%2F33320940&logo=bilibili&labelColor=FE7398&logoColor=white">
```

举个例子，显示陈总(uid:208259) 的粉丝数：

```html
<img src="https://img.shields.io/badge/dynamic/json?color=282c34&label=bilibili%E7%B2%89%E4%B8%9D%E6%95%B0&query=%24.data.value&url=http%3A%2F%2Fwww.zhangkexuan.cn%3A40001%2Fapi%2Ffanscount%2Fbilibili%2Fuid%2F208259&logo=bilibili&labelColor=FE7398&logoColor=white">
```

<img src="https://img.shields.io/badge/dynamic/json?color=282c34&label=bilibili%E7%B2%89%E4%B8%9D%E6%95%B0&query=%24.data.value&url=http%3A%2F%2Fwww.zhangkexuan.cn%3A40001%2Fapi%2Ffanscount%2Fbilibili%2Fuid%2F208259&logo=bilibili&labelColor=FE7398&logoColor=white" class="nofancybox">

# 总结

这次只是搭了架桥，但是速度已经比 Subsats 快多了，以后我还会添加其他平台的 API 接口。