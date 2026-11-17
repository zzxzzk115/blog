---
title: Building an API Service on a Server with Python
date: 2020-11-01T12:27:04
tags: [Python, API]
categories: [Backend-Networking]
toc: true
aiTranslated: true
---

Want to set up your own API service quickly? This post shows you the simplest and fastest way to do it with Python!

<!--more-->

# Preface

Once upon a time, I was building my own API services with Django + jsonrpc. In one word: "slow". In two words: "painful to write". In three words: "painful to set up".

Back then I needed an API service mainly because two projects required a remote server to run Python code and return JSON data. One was `高校快递帮` (Campus Delivery Helper), which I built with [ringotc](https://ringotc.github.io) and a childhood friend of mine as an entry for a WeChat Mini Program competition. The other was `FamilyDrugHelper` (Family Medicine Assistant), built with my university classmate xc and some high school classmates as an Internet+ competition entry. The former didn't win anything and the latter only got a modest award, but both leveled up my skills.

OK, back on topic. Both projects needed the server to remotely execute some logic implemented in Python and return JSON. For both I used Django + jsonrpc. That covered both the need for HTTP API requests and the need for the mini program's JavaScript to call remote code directly via jsonrpc. But honestly the speed was mediocre, the code was complicated to write, and setting up the Django + jsonrpc environment was even more of a hassle.

Later I also tried the Flask framework. Not bad, but its exception handling is a real pain.

# Take Off with FastAPI

FastAPI is, in my opinion, a really well-made API framework in Python. Not only is it fast, it's also quick to set up and very easy to write.

## Install the fastapi and uvicorn Packages

> fastapi itself is a fast asynchronous service, and uvicorn is a lightning-fast ASGI server built on uvloop and httptools; simply put, it's a high-performance async server. Running a fastapi service with uvicorn makes it even faster!

```python
pip install fastapi
pip install uvicorn
```

With the environment ready, you can jump straight into writing code. Pretty simple, right? ( ^ _ ^)

## Example Code

### The Simplest Code

```python
# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
    return {'message': '你已经正确创建 FastApi 服务！'}  # "You have successfully created a FastApi service!"
```

It's quite similar to how you'd write it in Flask.

Then run it with uvicorn:

```bash
uvicorn main:app -- reload
```

`main` refers to the source file name `main.py`, and `app` is the name of the FastAPI object we initialized.

Visit `http://127.0.0.1:8000` and you'll see the page display `{"message": "你已经正确创建 FastApi 服务！"}`

That was a GET on the root path. So how do you do a GET with parameters?

### GET with Parameters

Add the following function:

```python
@app.get('/query/{uid}')
def query(uid: int):
    msg = f'你查询的 uid 为：{uid}'  # "The uid you queried is: {uid}"
    return {'success': True, 'msg': msg}
```

After saving the code, the service restarts automatically.

Requesting `http://127.0.0.1:8000/query/123` returns ` {"success": True, "msg": "你查询的 uid 为：123"}`

The function above restricts the uid parameter to the int type. If you request `http://127.0.0.1:8000/query/abc`, the response will report an error instead of the program crashing. With Flask, you'd have to validate parameters manually, otherwise the program crashes.

### POST

Import pydantic's BaseModel:

```python
from pydantic import BaseModel
```

Build a parameter model, using User as an example:

```python
class User(BaseModel):
    id: str
    passwd: str
```

Add a function to handle the POST:

```python
@app.post('/login')
def login(user: User):
    if user.id == 'test' and user.passwd == 'test':
        msg = 'Login succeeded'
        return {'success': True, 'msg': msg}
    else:
        msg = 'Login failed'
        return {'success': False, 'msg': msg}
```

Now, if you send a POST form to `http://127.0.0.1:8000/login` with id test and password test, it returns a login success; otherwise it returns a login failure. This is just an example; the real logic would probably need other modules too.

## Things to Watch Out for on a Server

### Change the IP to 0.0.0.0 and pick your own port

The uvicorn command needs the host and port parameters:

```bash
uvicorn main:app --host '0.0.0.0'--port 8080 --reload
```

The port must be one that's opened in your cloud server's security group rules.

### Use screen to keep the service running so it doesn't stop when the terminal closes

**Install screen**

```bash
apt-get install screen
```

**Create a new screen**

```bash
screen -S fastapi
```

**Run the command**

```bash
uvicorn main:app --host '0.0.0.0'--port 8080 --reload
```

**Detach the screen into the background**

Press CTRL + A + D to detach.

After that, it keeps running even when you close the terminal.

**Resume the screen**

```bash
screen -ls # list screens
screen -r [screen session id]
```

# More

Combine it with Selenium and you can do all kinds of things you'd never have imagined.
