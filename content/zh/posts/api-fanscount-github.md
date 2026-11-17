---
title: '轮子那点事儿(2)：获取 GitHub Followers, Stars, Forks 的 API 的制作'
date: 2020-11-05T17:32:26
categories: [后端]
tags: [tutorial, API, github, codefromscratch, python]
toc: true
---

> [!NOTE]
> 文中自建接口的服务器早已停用，代码里的地址已失效，仅作记录。页面上显示的 Followers / Stars 徽章已改用 shields.io 自带的 GitHub 徽章；按用户统计的 Forks 徽章没有现成替代，已移除。

上次我们完成了 bilibili 粉丝数 API 的制作，并应用于 Shields.io，成功显示。这次我们来造 GitHub！先看看效果：

<div class="align-left">
    <img src="https://img.shields.io/github/followers/zzxzzk115?label=GitHub%20Followers&logo=github&labelColor=303030&color=A8A8A8&logoColor=white" class="nofancybox">
    <img src="https://img.shields.io/github/stars/zzxzzk115?label=GitHub%20Stars&logo=github&labelColor=303030&color=A8A8A8&logoColor=white" class="nofancybox">
</div>

<!--more-->

# 造前的分析

首先 GitHub 官方提供了 API：

例如我访问：`https://api.github.com/users/zzxzzk115`

得到的结果为：

```json
{
  "login": "zzxzzk115",
  "id": 33739170,
  "node_id": "MDQ6VXNlcjMzNzM5MTcw",
  "avatar_url": "https://avatars2.githubusercontent.com/u/33739170?v=4",
  "gravatar_id": "",
  "url": "https://api.github.com/users/zzxzzk115",
  "html_url": "https://github.com/zzxzzk115",
  "followers_url": "https://api.github.com/users/zzxzzk115/followers",
  "following_url": "https://api.github.com/users/zzxzzk115/following{/other_user}",
  "gists_url": "https://api.github.com/users/zzxzzk115/gists{/gist_id}",
  "starred_url": "https://api.github.com/users/zzxzzk115/starred{/owner}{/repo}",
  "subscriptions_url": "https://api.github.com/users/zzxzzk115/subscriptions",
  "organizations_url": "https://api.github.com/users/zzxzzk115/orgs",
  "repos_url": "https://api.github.com/users/zzxzzk115/repos",
  "events_url": "https://api.github.com/users/zzxzzk115/events{/privacy}",
  "received_events_url": "https://api.github.com/users/zzxzzk115/received_events",
  "type": "User",
  "site_admin": false,
  "name": "Lazy_V",
  "company": "HugeSoft",
  "blog": "https://blog.zhangkexuan.cn",
  "location": "Wuhan,Hubei,China",
  "email": null,
  "hireable": null,
  "bio": "The OpenSource is fantastic.",
  "twitter_username": null,
  "public_repos": 43,
  "public_gists": 0,
  "followers": 4,
  "following": 6,
  "created_at": "2017-11-17T01:27:49Z",
  "updated_at": "2020-11-02T05:54:04Z"
}
```

但是里面有 Followers 并没有 Stars 和 Forks。

那怎么知道 Stars 和 Forks 的值呢？

聪明的同学会思考，Stars 和 Forks 都是对于仓库(Repo, Repository) 而言的，所以我们要从

`https://api.github.com/users/zzxzzk115/repos` 得到我 github 用户所有仓库的信息：

```json
[
  {
    "id": 253395689,
    "node_id": "MDEwOlJlcG9zaXRvcnkyNTMzOTU2ODk=",
    "name": "30dayMakeOS",
    "full_name": "zzxzzk115/30dayMakeOS",
    "private": false,
    "owner": {
      "login": "zzxzzk115",
      "id": 33739170,
      "node_id": "MDQ6VXNlcjMzNzM5MTcw",
      "avatar_url": "https://avatars2.githubusercontent.com/u/33739170?v=4",
      "gravatar_id": "",
      "url": "https://api.github.com/users/zzxzzk115",
      "html_url": "https://github.com/zzxzzk115",
      "followers_url": "https://api.github.com/users/zzxzzk115/followers",
      "following_url": "https://api.github.com/users/zzxzzk115/following{/other_user}",
      "gists_url": "https://api.github.com/users/zzxzzk115/gists{/gist_id}",
      "starred_url": "https://api.github.com/users/zzxzzk115/starred{/owner}{/repo}",
      "subscriptions_url": "https://api.github.com/users/zzxzzk115/subscriptions",
      "organizations_url": "https://api.github.com/users/zzxzzk115/orgs",
      "repos_url": "https://api.github.com/users/zzxzzk115/repos",
      "events_url": "https://api.github.com/users/zzxzzk115/events{/privacy}",
      "received_events_url": "https://api.github.com/users/zzxzzk115/received_events",
      "type": "User",
      "site_admin": false
    },
    "html_url": "https://github.com/zzxzzk115/30dayMakeOS",
    "description": "《30天自制操作系统》源码中文版。自己制作一个操作系统（OSASK）的过程",
    "fork": true,
    "url": "https://api.github.com/repos/zzxzzk115/30dayMakeOS",
    "forks_url": "https://api.github.com/repos/zzxzzk115/30dayMakeOS/forks",
    "keys_url": "https://api.github.com/repos/zzxzzk115/30dayMakeOS/keys{/key_id}",
    "collaborators_url": "https://api.github.com/repos/zzxzzk115/30dayMakeOS/collaborators{/collaborator}",
    "teams_url": "https://api.github.com/repos/zzxzzk115/30dayMakeOS/teams",
    "hooks_url": "https://api.github.com/repos/zzxzzk115/30dayMakeOS/hooks",
    "issue_events_url": "https://api.github.com/repos/zzxzzk115/30dayMakeOS/issues/events{/number}",
    "events_url": "https://api.github.com/repos/zzxzzk115/30dayMakeOS/events",
    "assignees_url": "https://api.github.com/repos/zzxzzk115/30dayMakeOS/assignees{/user}",
    "branches_url": "https://api.github.com/repos/zzxzzk115/30dayMakeOS/branches{/branch}",
    "tags_url": "https://api.github.com/repos/zzxzzk115/30dayMakeOS/tags",
    "blobs_url": "https://api.github.com/repos/zzxzzk115/30dayMakeOS/git/blobs{/sha}",
    "git_tags_url": "https://api.github.com/repos/zzxzzk115/30dayMakeOS/git/tags{/sha}",
    "git_refs_url": "https://api.github.com/repos/zzxzzk115/30dayMakeOS/git/refs{/sha}",
    "trees_url": "https://api.github.com/repos/zzxzzk115/30dayMakeOS/git/trees{/sha}",
    "statuses_url": "https://api.github.com/repos/zzxzzk115/30dayMakeOS/statuses/{sha}",
    "languages_url": "https://api.github.com/repos/zzxzzk115/30dayMakeOS/languages",
    "stargazers_url": "https://api.github.com/repos/zzxzzk115/30dayMakeOS/stargazers",
    "contributors_url": "https://api.github.com/repos/zzxzzk115/30dayMakeOS/contributors",
    "subscribers_url": "https://api.github.com/repos/zzxzzk115/30dayMakeOS/subscribers",
    "subscription_url": "https://api.github.com/repos/zzxzzk115/30dayMakeOS/subscription",
    "commits_url": "https://api.github.com/repos/zzxzzk115/30dayMakeOS/commits{/sha}",
    "git_commits_url": "https://api.github.com/repos/zzxzzk115/30dayMakeOS/git/commits{/sha}",
    "comments_url": "https://api.github.com/repos/zzxzzk115/30dayMakeOS/comments{/number}",
    "issue_comment_url": "https://api.github.com/repos/zzxzzk115/30dayMakeOS/issues/comments{/number}",
    "contents_url": "https://api.github.com/repos/zzxzzk115/30dayMakeOS/contents/{+path}",
    "compare_url": "https://api.github.com/repos/zzxzzk115/30dayMakeOS/compare/{base}...{head}",
    "merges_url": "https://api.github.com/repos/zzxzzk115/30dayMakeOS/merges",
    "archive_url": "https://api.github.com/repos/zzxzzk115/30dayMakeOS/{archive_format}{/ref}",
    "downloads_url": "https://api.github.com/repos/zzxzzk115/30dayMakeOS/downloads",
    "issues_url": "https://api.github.com/repos/zzxzzk115/30dayMakeOS/issues{/number}",
    "pulls_url": "https://api.github.com/repos/zzxzzk115/30dayMakeOS/pulls{/number}",
    "milestones_url": "https://api.github.com/repos/zzxzzk115/30dayMakeOS/milestones{/number}",
    "notifications_url": "https://api.github.com/repos/zzxzzk115/30dayMakeOS/notifications{?since,all,participating}",
    "labels_url": "https://api.github.com/repos/zzxzzk115/30dayMakeOS/labels{/name}",
    "releases_url": "https://api.github.com/repos/zzxzzk115/30dayMakeOS/releases{/id}",
    "deployments_url": "https://api.github.com/repos/zzxzzk115/30dayMakeOS/deployments",
    "created_at": "2020-04-06T04:37:45Z",
    "updated_at": "2020-05-01T02:52:01Z",
    "pushed_at": "2019-05-27T14:13:55Z",
    "git_url": "git://github.com/zzxzzk115/30dayMakeOS.git",
    "ssh_url": "git@github.com:zzxzzk115/30dayMakeOS.git",
    "clone_url": "https://github.com/zzxzzk115/30dayMakeOS.git",
    "svn_url": "https://github.com/zzxzzk115/30dayMakeOS",
    "homepage": "https://github.com/yourtion/YOS",
    "size": 3567,
    "stargazers_count": 1,
    "watchers_count": 1,
    "language": null,
    "has_issues": false,
    "has_projects": true,
    "has_downloads": true,
    "has_wiki": true,
    "has_pages": false,
    "forks_count": 0,
    "mirror_url": null,
    "archived": false,
    "disabled": false,
    "open_issues_count": 0,
    "license": {
      "key": "other",
      "name": "Other",
      "spdx_id": "NOASSERTION",
      "url": null,
      "node_id": "MDc6TGljZW5zZTA="
    },
    "forks": 0,
    "open_issues": 0,
    "watchers": 1,
    "default_branch": "master"
  },
  {
    "id": 224566255,
    "node_id": "MDEwOlJlcG9zaXRvcnkyMjQ1NjYyNTU=",
    "name": "arduboy-mario",
    "full_name": "zzxzzk115/arduboy-mario",
    "private": false,
    "owner": {
      "login": "zzxzzk115",
      "id": 33739170,
..................................
```

仔细观察，对于每个仓库，`stargazers_count` 是我们需要的 Stars 的值，`forks_count` 是我们需要的 Forks 的值。我们只用把所有仓库的 `stargazers_count` 累加、`forks_count` 累加即可。

然后，我在做的过程中，发现 GitHub 的 API 请求是有限制的，每小时 60 次，我测试多了，一下就没了。

但是 GitHub API 在身份认证后，请求次数可以上升到 5000。

这里有两种方式：

1. OAuth
2. Personal Access Token

我将采用私人 Personal Access Token 方式。

# 开造

## Personal Access Token 配置

登录 GitHub，点击头像，点击 Settings

![github-settings](/img/markdown_20201105174801.png)

点击 Developer settings

![github-develoer-settings](/img/markdown_20201105174855.png)

点击 Personal access tokens

![github-personal-access-token](/img/markdown_20201105205557.png)

点击 Generate new token

![github-new-token](/img/markdown_20201105205648.png)

Note 填写 Token 标记名，例如 GitHub User API，由于不需要其他的权限，底下都不用勾选：

![github-token-note](/img/markdown_20201105205930.png)

点击 Generate token

![github-generate-token](/img/markdown_20201105210031.png)

然后就可以看到或者访问获取你的 token 了。

到这里，准备就做好了。

## 根据需求导入包

由于和上次类似，都是请求 API 网址，解析 json，故导入包的部分一样：

```python
import uvicorn as uvicorn
from fastapi import FastAPI
import requests
import json

app = FastAPI()  # 必须实例化该类，启动的时候调用

git_token = "你的personal_access_token"
s = requests.session()
s.keep_alive = False
headers = {"Authorization": "token " + git_token, "Connection": "close", "User-Agent": "FansCount-GitHub"}
```

>  说明：上面的代码，git_token 填入你刚刚生成的 token。
>
>  s.keep_alive = False 和"Connection": "close"都是为了解决在同一域名 API 请求次数过多导致的 Connection refused 的问题。（测试中发现的）

## 添加完成核心功能的函数

### Followers

Followers 的获取，只需要请求 `https://api.github.com/users/{username}` 然后解析 json 即可，经过测试，如果 username 是错误或不存在的值，json 将会返回一个带有错误信息的 message，否则没有这个 message 键。

那么代码应该这样写:

```python
def get_github_followers(uname):
    status_code = 200
    message = "success"
    followers = 0

    response = s.get(f"https://api.github.com/users/{uname}", headers = headers)
    # print(response.text)
    # print(response.headers)
    json_response = json.loads(response.text)

    message = json_response.get("message")
    print(message)

    if message == None:
        status_code = 200
        message = "success"
        followers = json_response.get("followers")
    else:
        status_code = -400
        followers = -1
    return status_code, message, followers
```

### Stars 和 Forks

Stars 和 Forks 需要请求 `https://api.github.com/users/{zzxzzk115}/repos`，它们的大部分工作都相同，也就一个需要查询的字段不同。

```python
def get_github_repoInfo_count(uname, query):
    status_code = 200
    message = "success"
    count = 0
    response = s.get(f"https://api.github.com/users/{uname}/repos", headers = headers)
    # print(response.headers)
    json_response = json.loads(response.text)
    try:
        message = json_response.get("message")
        print(message)
    except:
        message = None
    if message == None:
        status_code = 200
        message = "success"
        # print(len(list(json_response)))
        for repoJson in json_response:
            # query: 
            count += repoJson.get(query)
    else:
        status_code = -400
        count = -1
    return status_code, message, count
```

## 添加 fastapi 的响应函数

```python
@app.get('/api/fanscount/github/uname/{uname}/followers')
def github_followers(uname: str):
    status_code, message, followers = get_github_followers(uname)
    return {'status' : status_code, "message" : message, "data" : { "value" : followers}}

@app.get('/api/fanscount/github/uname/{uname}/stars')
def github_stars(uname: str):
    status_code, message, stars = get_github_repoInfo_count(uname, "stargazers_count")
    return {'status' : status_code, "message" : message, "data" : { "value" : stars}}

@app.get('/api/fanscount/github/uname/{uname}/forks')
def github_stars(uname: str):
    status_code, message, forks = get_github_repoInfo_count(uname, "forks_count")
    return {'status' : status_code, "message" : message, "data" : { "value" : forks}}
```

## 目前 GitHub 部分的完整源码

```python
import uvicorn as uvicorn
from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup


app = FastAPI()  # 必须实例化该类，启动的时候调用

git_token = "你的personal_access_token"
s = requests.session()
s.keep_alive = False
headers = {"Authorization": "token " + git_token}


def get_github_followers(uname):
    status_code = 200
    message = "success"
    followers = 0

    response = s.get(f"https://api.github.com/users/{uname}", headers = headers)
    # print(response.text)
    # print(response.headers)
    json_response = json.loads(response.text)

    message = json_response.get("message")
    print(message)

    if message == None:
        status_code = 200
        message = "success"
        followers = json_response.get("followers")
    else:
        status_code = -400
        followers = -1
    return status_code, message, followers


def get_github_repoInfo_count(uname, query):
    status_code = 200
    message = "success"
    count = 0
    response = s.get(f"https://api.github.com/users/{uname}/repos", headers = headers)
    # print(response.headers)
    json_response = json.loads(response.text)
    try:
        message = json_response.get("message")
        print(message)
    except:
        message = None
    if message == None:
        status_code = 200
        message = "success"
        # print(len(list(json_response)))
        for repoJson in json_response:
            # query: 
            count += repoJson.get(query)
    else:
        status_code = -400
        count = -1
    return status_code, message, count


# 请求根目录
@app.get('/')
def index():
    return {'message': '欢迎来到FastApi 服务！'}


@app.get('/api/fanscount/github/uname/{uname}/followers')
def github_followers(uname: str):
    status_code, message, followers = get_github_followers(uname)
    return {'status' : status_code, "message" : message, "data" : { "value" : followers}}

@app.get('/api/fanscount/github/uname/{uname}/stars')
def github_stars(uname: str):
    status_code, message, stars = get_github_repoInfo_count(uname, "stargazers_count")
    return {'status' : status_code, "message" : message, "data" : { "value" : stars}}

@app.get('/api/fanscount/github/uname/{uname}/forks')
def github_stars(uname: str):
    status_code, message, forks = get_github_repoInfo_count(uname, "forks_count")
    return {'status' : status_code, "message" : message, "data" : { "value" : forks}}


if __name__ == '__main__':
    uvicorn.run(app=app, host="0.0.0.0", port=40001)
```

# 效果

访问 `http://www.zhangkexuan.cn:40001/api/fanscount/github/uname/zzxzzk115/followers`

即可得到 GitHub 的 Followers 的数值。（这个接口所在的服务器早已停用，地址已失效，仅作示例。）

结果：

```python
{"status":200,"message":"success","data":{"value":4}}
```

如果故意输入错误的值或者错误的 id：

`http://www.zhangkexuan.cn:40001/api/fanscount/github/uname/***/followers`

得到：

```json
{"status":-400,"message":"Not Found","data":{"value":-1}}
```

我这次就不和 Substats 比了。

Stars 和 Forks 用法类似:

`http://www.zhangkexuan.cn:40001/api/fanscount/github/uname/zzxzzk115/stars`

`http://www.zhangkexuan.cn:40001/api/fanscount/github/uname/zzxzzk115/forks`

# 使用

把下面代码里的 `zzxzzk115` 改为你的 GitHub 用户名，就可以了：

followers:

```html
<img src="https://img.shields.io/badge/dynamic/json?color=A8A8A8&label=GitHub%20Followers&query=%24.data.value&url=http%3A%2F%2Fwww.zhangkexuan.cn%3A40001%2Fapi%2Ffanscount%2Fgithub%2Funame%2Fzzxzzk115%2Ffollowers&logo=github&labelColor=303030&logoColor=white">
```

stars:

```html
<img src="https://img.shields.io/badge/dynamic/json?color=A8A8A8&label=GitHub%20Stars&query=%24.data.value&url=http%3A%2F%2Fwww.zhangkexuan.cn%3A40001%2Fapi%2Ffanscount%2Fgithub%2Funame%2Fzzxzzk115%2Fstars&logo=github&labelColor=303030&logoColor=white">
```

forks:

```html
<img src="https://img.shields.io/badge/dynamic/json?color=A8A8A8&label=GitHub%20Forks&query=%24.data.value&url=http%3A%2F%2Fwww.zhangkexuan.cn%3A40001%2Fapi%2Ffanscount%2Fgithub%2Funame%2Fzzxzzk115%2Fforks&logo=github&labelColor=303030&logoColor=white">
```

举个例子，显示 OneLoneCoder(我很喜欢的一个 Youtuber) 的 Followers 和 Stars:

<div class="align-left">
    <img src="https://img.shields.io/github/followers/OneLoneCoder?label=GitHub%20Followers&logo=github&labelColor=303030&color=A8A8A8&logoColor=white" class="nofancybox">
    <img src="https://img.shields.io/github/stars/OneLoneCoder?label=GitHub%20Stars&logo=github&labelColor=303030&color=A8A8A8&logoColor=white" class="nofancybox">
</div>


# 总结

GitHub 的 API 有访问限制，不过可以提高到每小时 5000 次请求次数。

这样的 API 速度还是挺快的。下次再搭别的。
