---
title: 'Reinventing the Wheel (2): Building an API for GitHub Followers, Stars and Forks'
date: 2020-11-05T17:32:26
categories: [Backend]
tags: [tutorial, API, github, codefromscratch, python]
toc: true
aiTranslated: true
---

Last time we built an API for bilibili follower counts, plugged it into Shields.io, and got it displaying. This time we're building one for GitHub! Here's what it looks like:

<div class="align-left">
    <img src="https://img.shields.io/badge/dynamic/json?color=A8A8A8&label=GitHub%20Followers&query=%24.data.value&url=http%3A%2F%2Fwww.zhangkexuan.cn%3A40001%2Fapi%2Ffanscount%2Fgithub%2Funame%2Fzzxzzk115%2Ffollowers&logo=github&labelColor=303030&logoColor=white" class="nofancybox">
    <img src="https://img.shields.io/badge/dynamic/json?color=A8A8A8&label=GitHub%20Stars&query=%24.data.value&url=http%3A%2F%2Fwww.zhangkexuan.cn%3A40001%2Fapi%2Ffanscount%2Fgithub%2Funame%2Fzzxzzk115%2Fstars&logo=github&labelColor=303030&logoColor=white" class="nofancybox">
    <img src="https://img.shields.io/badge/dynamic/json?color=A8A8A8&label=GitHub%20Forks&query=%24.data.value&url=http%3A%2F%2Fwww.zhangkexuan.cn%3A40001%2Fapi%2Ffanscount%2Fgithub%2Funame%2Fzzxzzk115%2Fforks&logo=github&labelColor=303030&logoColor=white" class="nofancybox">
</div>

<!--more-->

# Analysis Before Building

First of all, GitHub provides an official API:

For example, if I visit: `https://api.github.com/users/zzxzzk115`

I get:

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

But it only has Followers — no Stars or Forks.

So how do we get the Stars and Forks values?

Clever readers will realize that Stars and Forks belong to repositories (Repo, Repository), so we need to get info on all of my GitHub user's repositories from

`https://api.github.com/users/zzxzzk115/repos`:

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

Looking closely, for each repository, `stargazers_count` is the Stars value we want and `forks_count` is the Forks value we want. We just need to sum up `stargazers_count` and `forks_count` across all repositories.

Then, while building this, I discovered that GitHub's API requests are rate-limited to 60 per hour. I tested a few too many times and used them all up in no time.

However, once authenticated, the GitHub API's limit goes up to 5000.

There are two ways to do this:

1. OAuth
2. Personal Access Token

I'll go with a private Personal Access Token.

# Let's Build It

## Setting Up a Personal Access Token

Log in to GitHub, click your avatar, and click Settings

![github-settings](/img/markdown_20201105174801.png)

Click Developer settings

![github-develoer-settings](/img/markdown_20201105174855.png)

Click Personal access tokens

![github-personal-access-token](/img/markdown_20201105205557.png)

Click Generate new token

![github-new-token](/img/markdown_20201105205648.png)

In Note, enter a label for the token, e.g. GitHub User API. Since we don't need any other permissions, leave everything below unticked:

![github-token-note](/img/markdown_20201105205930.png)

Click Generate token

![github-generate-token](/img/markdown_20201105210031.png)

Then you can see or copy your token.

And with that, the prep work is done.

## Import Packages as Needed

Since this is similar to last time — requesting an API URL and parsing JSON — the imports are the same:

```python
import uvicorn as uvicorn
from fastapi import FastAPI
import requests
import json

app = FastAPI()  # This class must be instantiated; it's used at startup

git_token = "your_personal_access_token"
s = requests.session()
s.keep_alive = False
headers = {"Authorization": "token " + git_token, "Connection": "close", "User-Agent": "FansCount-GitHub"}
```

>  Note: in the code above, fill git_token with the token you just generated.
>
>  s.keep_alive = False and "Connection": "close" are both there to fix the Connection refused problem caused by too many API requests to the same domain. (Found during testing.)

## Add the Functions That Do the Core Work

### Followers

To get Followers, we just request `https://api.github.com/users/{username}` and parse the JSON. From testing, if the username is wrong or doesn't exist, the JSON returns a message with error info; otherwise there's no message key.

So the code should look like this:

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

### Stars and Forks

Stars and Forks need a request to `https://api.github.com/users/{zzxzzk115}/repos`. Most of the work is the same for both; only the field being queried differs.

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

## Add the FastAPI Handlers

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

## Full Source Code of the GitHub Part So Far

```python
import uvicorn as uvicorn
from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup


app = FastAPI()  # This class must be instantiated; it's used at startup

git_token = "your_personal_access_token"
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


# Request to the root path
@app.get('/')
def index():
    return {'message': 'Welcome to the FastApi service!'}


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

# Result

Visit `http://www.zhangkexuan.cn:40001/api/fanscount/github/uname/zzxzzk115/followers`

to get the GitHub Followers count: [click to visit](http://www.zhangkexuan.cn:40001/api/fanscount/github/uname/zzxzzk115/followers)

Result:

```python
{"status":200,"message":"success","data":{"value":4}}
```

If you deliberately enter a wrong value or a wrong id:

`http://www.zhangkexuan.cn:40001/api/fanscount/github/uname/***/followers`

you get:

```json
{"status":-400,"message":"Not Found","data":{"value":-1}}
```

I won't compare it with Substats this time.

Stars and Forks work the same way:

`http://www.zhangkexuan.cn:40001/api/fanscount/github/uname/zzxzzk115/stars`

`http://www.zhangkexuan.cn:40001/api/fanscount/github/uname/zzxzzk115/forks`

# Usage

Just change `zzxzzk115` in the code below to your GitHub username:

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

For example, here are the Followers and Stars of OneLoneCoder (a YouTuber I really like):

<div class="align-left">
    <img src="https://img.shields.io/badge/dynamic/json?color=A8A8A8&label=GitHub%20Followers&query=%24.data.value&url=http%3A%2F%2Fwww.zhangkexuan.cn%3A40001%2Fapi%2Ffanscount%2Fgithub%2Funame%2FOneLoneCoder%2Ffollowers&logo=github&labelColor=303030&logoColor=white" class="nofancybox">
    <img src="https://img.shields.io/badge/dynamic/json?color=A8A8A8&label=GitHub%20Stars&query=%24.data.value&url=http%3A%2F%2Fwww.zhangkexuan.cn%3A40001%2Fapi%2Ffanscount%2Fgithub%2Funame%2FOneLoneCoder%2Fstars&logo=github&labelColor=303030&logoColor=white" class="nofancybox">
    <img src="https://img.shields.io/badge/dynamic/json?color=A8A8A8&label=GitHub%20Forks&query=%24.data.value&url=http%3A%2F%2Fwww.zhangkexuan.cn%3A40001%2Fapi%2Ffanscount%2Fgithub%2Funame%2FOneLoneCoder%2Fforks&logo=github&labelColor=303030&logoColor=white" class="nofancybox">
</div>


# Summary

GitHub's API is rate-limited, but you can raise it to 5000 requests per hour.

An API like this is still pretty fast. Next time I'll build another one.
