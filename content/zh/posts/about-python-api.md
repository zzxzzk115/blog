---
title: 关于服务器通过 Python 搭建 API 服务
date: 2020-11-01T12:27:04
tags: [python, API]
categories: [后端]
toc: true
---

想要快速搭建自己的 API 服务？本文教会你用 Python 完成最简单最快速的搭建！

<!--more-->

# 前言

曾几何时，我还在用着 Django+jsonrpc，做自己的 API 服务。一个字：“慢”，两个字：“难写”，三个字：“难搭建”。

当初做 API 服务的需求主要是有两个项目需要远程服务器执行 Python 代码，返回 JSON 数据。一个是 `高校快递帮`，是我和 [ringotc](https://ringotc.github.io) 还有我的一个发小一起完成的，是微信小程序大赛作品。另一个是 `FamilyDrugHelper`（家庭药物助手），是和大学同学 xc 以及高中同学共同完成的，是互联网+参赛作品。虽然前者未获奖，后者奖项一般，但对我都是技能的提升。

好了，回归正题。两个项目都需要服务器远程执行一些 python 实现的逻辑，返回 json 数据。两个项目我都采用了 Django+jsonrpc。这样既可以解决 HTTP API 请求的需求，也能解决小程序 JavaScript 直接通过 jsonrpc 调用远程程序的需求。但是，确实速度一般，而且写起来复杂，django+jsonrpc 环境搭建更是麻烦。

后来也了解了 flask 框架，还不错，但是异常处理相关很蛋疼。

# 飞起来吧，FastAPI

FastAPI 是 python 里面我觉得做的非常好的 API 框架，不仅速度快，而且搭建也快，写起来也非常简单。

## 安装 fastapi 和 uvicorn 包

> fastapi 本身就是快速的异步服务，uvicorn 是基于 uvloop 和 httptools 构建的非常快速的 ASGI 服务器，简单来说，是高性能异步服务器。通过 uvicorn 运行 fastapi 服务，快上加快！

```python
pip install fastapi
pip install uvicorn
```

环境搭建好了，可以直接上手写代码了。是不是很简单呢( ^ _ ^)

## 案例代码

### 最简单的代码

```python
# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
    return {'message': '你已经正确创建 FastApi 服务！'}
```

和 flask 写法比较类似。

然后用 uvicorn 运行它：

```bash
uvicorn main:app -- reload
```

`main` 代表程序源文件名 `main.py`，`app` 表示我们初始化 FastAPI 对象的名字。

访问 `http://127.0.0.1:8000` 即可看到页面显示 `{"message": "你已经正确创建 FastApi 服务！"}`

刚刚是根目录 get 的案例，那么带参数的 get 如何实现呢？

### GET 带参数

加入以下函数：

```python
@app.get('/query/{uid}')
def query(uid: int):
    msg = f'你查询的 uid 为：{uid}'
    return {'success': True, 'msg': msg}
```

保存代码后，服务自动重启。

请求 `http://127.0.0.1:8000/query/123`，会返回 ` {"success": True, "msg": "你查询的 uid 为：123"}`

上面函数限制了 uid 参数的类型为 int 类型。如果请求 `http://127.0.0.1:8000/query/abc`，返回的结果会提示报错，而不是程序崩溃。flask 框架则需要手动判断参数的正确性，否则程序崩溃。

### POST

导入 pydantic 的 BaseModel：

```python
from pydantic import BaseModel
```

构建参数模型，以 User 为例：

```python
class User(BaseModel):
    id: str
    passwd: str
```

加入处理 post 的函数：

```python
@app.post('/login')
def login(user: User):
    if user.id == 'test' and user.passwd == 'test':
        msg = '登录成功'
        return {'success': True, 'msg': msg}
    else:
        msg = '登录失败'
        return {'success': False, 'msg': msg}
```

这样，给 `http://127.0.0.1:8000/login` 发送 POST 表单，如果发送的 id 是 test，密码也是 test，则返回登录成功，否则返回登录失败。这里只是举例，相应逻辑可能还需要其他模块。

## 服务器中需要注意的点

### ip 要改为 0.0.0.0，端口自定义

uvicorn 的指令需要添加 host 参数和 port 参数:

```bash
uvicorn main:app --host '0.0.0.0'--port 8080 --reload
```

端口一定要是在云服务器安全组策略中开启的。

### 要用 screen 来挂服务，以免终端关闭后服务终止

**安装 screen**

```bash
apt-get install screen
```

**新建 screen**

```bash
screen -S fastapi
```

**执行指令**

```bash
uvicorn main:app --host '0.0.0.0'--port 8080 --reload
```

**后台挂起 screen**

按 CTRL + A + D 组合键挂起。

然后关掉终端程序后依旧执行。

**恢复 screen**

```bash
screen -ls # 查看screen列表
screen -r [screen会话号]
```

# 更多

搭配 Selenium，可以有更多你想不到的玩法。