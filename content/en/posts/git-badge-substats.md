---
title: 'Git Badges: Shields.io and Substats'
date: 2020-11-02T15:41:21
categories: [Jottings]
tags: [tutorial, git, beautify]
toc: true
aiTranslated: true
---

When using online code hosting services like GitHub, have you often seen little badges like these?

<div class="align-left"><img src="https://img.shields.io/badge/Language-C++-blue" class="nofancybox"><img src="https://img.shields.io/badge/License-MIT-green" class="nofancybox"></div>

Want badges of your own?

Or maybe you'd like badges that update dynamically? (Doesn't matter if you don't have many followers yet, maybe you'll have more someday \^_\^)

<div class="align-left"><a href="https://space.bilibili.com/33320940" target="_blank"><img src="https://img.shields.io/badge/dynamic/json?labelColor=FE7398&label=bilibili%20fans&query=$.data.totalSubs&url=https%3A%2F%2Fapi.spencerwoo.com%2Fsubstats%2F%3Fsource%3Dbilibili%26queryKey%3D33320940&logo=bilibili&logoColor=white&color=282c34&longCache=true" class="nofancybox"></a><a href="https://music.163.com/#/user/home?id=1330462180" target="_blank"><img src="https://img.shields.io/badge/dynamic/json?label=%E7%BD%91%E6%98%93%E4%BA%91%E9%9F%B3%E4%B9%90%E7%B2%89%E4%B8%9D&query=%24.data.totalSubs&url=https%3A%2F%2Fapi.spencerwoo.com%2Fsubstats%2F%3Fsource%3DneteaseMusic%26queryKey%3D1330462180&color=282c34&labelColor=e72d2c&logo=data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iaWNvbiIgdmlld0JveD0iMCAwIDEwMjQgMTAyNCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB3aWR0aD0iOTYiIGhlaWdodD0iOTYiPjxkZWZzPjxzdHlsZS8+PC9kZWZzPjxwYXRoIGQ9Ik02MjcuMDg2IDUuMTE1YzI4LjEzMi03LjY3MiA1OC44MjItNy42NzIgODYuOTUzIDAgMzMuMjQ3IDcuNjcyIDYzLjkzNyAyMy4wMTcgODkuNTEyIDQzLjQ3NyAxMC4yMyA3LjY3MyAxNy45MDIgMTUuMzQ0IDIzLjAxNyAyOC4xMzEgNy42NzIgMTcuOTAzIDUuMTE0IDM4LjM2My01LjExNSA1My43MDgtNy42NzIgMTIuNzg3LTIzLjAxNyAyMy4wMTctNDAuOTIgMjUuNTc0LTEyLjc4NyAyLjU1OC0yNS41NzQgMC0zOC4zNjItNy42NzItNS4xMTUtMi41NTgtMTAuMjMtMTAuMjMtMTcuOTAyLTEyLjc4Ny0xNy45MDItMTAuMjMtMzUuODA0LTIwLjQ2LTU2LjI2NC0xNy45MDMtMTUuMzQ1IDAtMjguMTMyIDcuNjczLTM1LjgwNCAxNy45MDMtMTAuMjMgMTAuMjMtMTIuNzg4IDIzLjAxNy0xMC4yMyAzNS44MDQgNy42NzIgMjUuNTc0IDEyLjc4NyA1My43MDYgMjAuNDYgNzkuMjgxIDUxLjE1IDIuNTU4IDk5Ljc0IDE1LjM0NSAxNDMuMjE4IDQwLjkyIDQwLjkyIDI1LjU3NSA3OS4yOCA1OC44MjEgMTA5Ljk3IDk3LjE4MyAyNS41NzUgMzMuMjQ3IDQ2LjAzNSA3MS42MSA1Ni4yNjUgMTEyLjUzIDEyLjc4NiA0My40NzYgMTcuOTAxIDg5LjUxIDEyLjc4NiAxMzIuOTg2LTIuNTU3IDM4LjM2My0xMC4yMyA3NC4xNjYtMjMuMDE2IDEwOS45NzEtMzMuMjQ3IDg0LjM5Ni05Mi4wNyAxNjEuMTItMTcxLjM1IDIwOS43MTMtNTYuMjY1IDM1LjgwMy0xMjIuNzYgNTguODIxLTE4OS4yNTMgNjYuNDkzLTQ2LjAzNCA1LjExNS05Mi4wNjkgNS4xMTUtMTM4LjEwMi0yLjU1Ny05NC42MjctMTUuMzQ1LTE4MS41OC02MS4zOC0yNTAuNjMxLTEzMC40MzEtNjYuNDk1LTY2LjQ5My0xMTIuNTMtMTUzLjQ0OC0xMzIuOTktMjQ1LjUxNi03LjY3MS02OS4wNTItNy42NzEtMTM4LjEwMyA3LjY3My0yMDcuMTU0IDE3LjkwMy04MS44NCA2MS4zOC0xNjEuMTIgMTE3LjY0NC0yMjIuNSA0OC41OTItNTEuMTUgMTA3LjQxNC04OS41MTEgMTcxLjM1LTExNy42NDMgNy42NzItMi41NTggMTIuNzg3LTUuMTE1IDIwLjQ2LTcuNjczIDE1LjM0NC0yLjU1NyAzMC42OSAwIDQzLjQ3NyAxMC4yMyAxNy45MDIgMTIuNzg4IDI1LjU3NCAzMy4yNDggMjMuMDE3IDUzLjcwNy0yLjU1NyAyMC40Ni0xNy45MDIgMzguMzYzLTM1LjgwNSA0Ni4wMzQtNjMuOTM3IDI1LjU3NS0xMjIuNzU4IDY5LjA1Mi0xNjMuNjc4IDEyMi43Ni0zOC4zNjIgNTMuNzA1LTYzLjkzNiAxMTIuNTI3LTcxLjYwOCAxNzMuOTA2LTcuNjcyIDYxLjM4IDAgMTIyLjc1OCAyMC40NiAxODEuNTggMzAuNjkgODQuMzk2IDk0LjYyNiAxNTYuMDA0IDE3My45MDcgMTk2LjkyNCA0OC41OTIgMjUuNTc1IDEwMi4yOTggMzguMzYyIDE1Ni4wMDUgMzguMzYyIDQzLjQ3NyAwIDg5LjUxMS03LjY3MiAxMzAuNDMtMjMuMDE3IDM1LjgwNS0xMi43ODcgNzEuNjEtMzMuMjQ3IDk5Ljc0MS01OC44MjIgMjguMTMzLTIzLjAxNiA1MS4xNS01My43MDYgNjYuNDk1LTg0LjM5NiA3LjY3Mi0xNS4zNDUgMTcuOTAxLTMzLjI0NyAyMC40Ni01MS4xNSAxNS4zNDQtNTEuMTQ5IDE3LjkwMS0xMDcuNDEzIDIuNTU2LTE1OC41NjEtMTIuNzg2LTQzLjQ3OC0zOC4zNjEtODEuODQtNzEuNjA5LTEwOS45NzEtMTUuMzQ0LTEyLjc4Ny0zMC42OS0yNS41NzUtNDguNTkyLTM1LjgwNS0xNS4zNDQtNy42NzItMzAuNjktMTUuMzQ1LTQ4LjU5MS0xNy45MDIgMTIuNzg4IDQ2LjAzNCAyMy4wMTggOTIuMDcgMzUuODA0IDEzNS41NDUgMi41NTggMTAuMjMgNS4xMTUgMjMuMDE4IDUuMTE1IDMzLjI0OCAyLjU1OCA0Ni4wMzMtMTUuMzQ0IDk0LjYyNS00Ni4wMzQgMTMwLjQzLTI4LjEzMiAzMy4yNDYtNjkuMDUyIDU4LjgyMS0xMTIuNTI4IDY2LjQ5NC00Ni4wMzQgMTAuMjMtOTcuMTg0IDAtMTM4LjEwMy0yNS41NzUtMzguMzYyLTI1LjU3NC02Ni40OTQtNjMuOTM2LTgxLjg0LTEwNC44NTYtNy42NzItMjMuMDE3LTEyLjc4Ny00OC41OTEtMTIuNzg3LTc0LjE2Ni0yLjU1Ni01Ni4yNjQgMTIuNzg4LTEwOS45NzEgNDMuNDc4LTE1Ni4wMDUgMzUuODA0LTUzLjcwNyA5NC42MjUtOTIuMDcgMTU4LjU2Mi0xMDkuOTcxLTUuMTE1LTE3LjkwMi0xMC4yMy0zNS44MDUtMTIuNzg3LTUzLjcwNy0xMi43ODctMzguMzYxLTEwLjIzLTgxLjgzOSA3LjY3Mi0xMTUuMDg2IDEwLjIzLTIwLjQ2IDIzLjAxOC0zOC4zNjEgNDAuOTItNTEuMTUgMjMuMDE2LTIwLjQ2IDQzLjQ3Ni0zMy4yNDYgNjYuNDk0LTQwLjkxOE00NzguNzUzIDQxOS40MjRjLTE3LjkwMyAxNy45MDItMjguMTMzIDQwLjkyLTMzLjI0NyA2My45MzYtNS4xMTQgMjAuNDYtNS4xMTQgNDMuNDc3IDAgNjYuNDk1IDUuMTE0IDIzLjAxNiAxNy45MDIgNDYuMDMzIDM4LjM2MiA2MS4zOCAxNS4zNDUgMTAuMjI4IDM1LjgwNCAxNS4zNDMgNTYuMjY0IDEwLjIyOCAzNS44MDQtNS4xMTUgNjMuOTM2LTM4LjM2MiA2My45MzYtNzQuMTY2LTIuNTU3LTcuNjcyLTIuNTU3LTE3LjkwMi01LjExNS0yNS41NzUtMTIuNzg3LTQ4LjU5Mi0yNS41NzMtOTkuNzQxLTM4LjM2MS0xNDguMzMzLTMwLjY5IDcuNjczLTU4LjgyMiAyMy4wMTgtODEuODQgNDYuMDM1eiIgZmlsbD0iI2ZmZiIvPjwvc3ZnPg==&longCache=true" class="nofancybox"></a></div>

This post shows you how to make badges like these and display them on a web page!

<!--more-->

# Shields.io

[Shield.io](https://shields.io/) provides a badge-making service, with two kinds of badges: static and dynamic. Static badges have fixed text values; neither the badge's label nor its text ever changes. Dynamic badges are a service where, given a request URL and the corresponding query field that you provide, Shields.io requests that URL for you, gets the JSON data, and shows the data you want displayed in the badge text.

## Static Badges

The general badge format is: `https://img.shields.io/badge/{左标签文本}-{右消息文本}-{右消息背景颜色}` (left label text, right message text, right message background color).

For the message background color, Shields.io provides some default options made of English words, or you can use a color's HEX value:

<div class="align-left">
    <p><span><span display="inline" height="20px" class="common__BadgeWrapper-v13icv-3 dBqSYE"><img alt="brightgreen" src="https://img.shields.io/badge/-brightgreen-brightgreen" class="nofancybox"></span><span display="inline" height="20px" class="common__BadgeWrapper-v13icv-3 dBqSYE"><img alt="green" src="https://img.shields.io/badge/-green-green" class="nofancybox"></span><span display="inline" height="20px" class="common__BadgeWrapper-v13icv-3 dBqSYE"><img alt="yellowgreen" src="https://img.shields.io/badge/-yellowgreen-yellowgreen" class="nofancybox"></span><span display="inline" height="20px" class="common__BadgeWrapper-v13icv-3 dBqSYE"><img alt="yellow" src="https://img.shields.io/badge/-yellow-yellow" class="nofancybox"></span><span display="inline" height="20px" class="common__BadgeWrapper-v13icv-3 dBqSYE"><img alt="orange" src="https://img.shields.io/badge/-orange-orange" class="nofancybox"></span><span display="inline" height="20px" class="common__BadgeWrapper-v13icv-3 dBqSYE"><img alt="red" src="https://img.shields.io/badge/-red-red" class="nofancybox"></span><span display="inline" height="20px" class="common__BadgeWrapper-v13icv-3 dBqSYE"><img alt="blue" src="https://img.shields.io/badge/-blue-blue" class="nofancybox"></span><span display="inline" height="20px" class="common__BadgeWrapper-v13icv-3 dBqSYE"><img alt="lightgrey" src="https://img.shields.io/badge/-lightgrey-lightgrey" class="nofancybox"></span></span><br><span><span display="inline" height="20px" class="common__BadgeWrapper-v13icv-3 dBqSYE"><img alt="success" src="https://img.shields.io/badge/-success-success" class="nofancybox"></span><span display="inline" height="20px" class="common__BadgeWrapper-v13icv-3 dBqSYE"><img alt="important" src="https://img.shields.io/badge/-important-important" class="nofancybox"></span><span display="inline" height="20px" class="common__BadgeWrapper-v13icv-3 dBqSYE"><img alt="critical" src="https://img.shields.io/badge/-critical-critical" class="nofancybox"></span><span display="inline" height="20px" class="common__BadgeWrapper-v13icv-3 dBqSYE"><img alt="informational" src="https://img.shields.io/badge/-informational-informational" class="nofancybox"></span><span display="inline" height="20px" class="common__BadgeWrapper-v13icv-3 dBqSYE"><img alt="inactive" src="https://img.shields.io/badge/-inactive-inactive" class="nofancybox"></span></span><br><span><span display="inline" height="20px" class="common__BadgeWrapper-v13icv-3 dBqSYE"><img alt="blueviolet" src="https://img.shields.io/badge/-blueviolet-blueviolet" class="nofancybox"></span><span display="inline" height="20px" class="common__BadgeWrapper-v13icv-3 dBqSYE"><img alt="ff69b4" src="https://img.shields.io/badge/-ff69b4-ff69b4" class="nofancybox"></span><span display="inline" height="20px" class="common__BadgeWrapper-v13icv-3 dBqSYE"><img alt="9cf" src="https://img.shields.io/badge/-9cf-9cf" class="nofancybox"></span></span></p>
</div>


For example, say I want the left label text to be `Language`, the right message text to be `C++`, and the right message background color to be `blue`:

`https://img.shields.io/badge/Language-C++-blue`

<img src="https://img.shields.io/badge/Language-C++-blue" class="nofancybox"></img>

Chinese works too, and it looks super professional (totally):

`https://img.shields.io/badge/语言-C加加-blue`

<img src="https://img.shields.io/badge/%E8%AF%AD%E8%A8%80-C%E5%8A%A0%E5%8A%A0-blue" class="nofancybox"></img>

## Dynamic Badges

Here's how dynamic badges work: first you need an API service. You fill in the relevant parameters, request the service, and it returns JSON data containing the dynamic data you need. Honestly, I could reinvent the wheel and write my own API service, since this wheel is really easy to build. But since it's so easy, and someone has already built one, I can leave the wheel for later, hahaha, and just use someone else's for now. (To be honest, Substats is a bit slow, so I really do plan to build my own.)

### Substats

[Substats](https://substats.spencerwoo.com) is exactly that kind of service. It mainly makes requests to various social platforms and returns follower or subscriber counts. The principle isn't hard either: request the social platform's profile page URL, grab the value of the corresponding HTML tag, and wrap it in JSON when returning it. If you're interested, you can refer to my earlier post [Building an API Service on a Server with Python](/posts/about-python-api) and give it a try yourself.

So how do you use Substats? Here's an example:

`https://api.spencerwoo.com/substats/?source=bilibili&queryKey=33320940`

Set `source` to the name of the corresponding social site; for the supported name values, see the [Substats API](https://substats.spencerwoo.com/api.html#api-endpoint).

`queryKey` is a value that uniquely identifies the account, like an id; here it's the uid in the bilibili profile page URL.

`https://space.bilibili.com/33320940`

Here, `queryKey` is `33320930`.

First, visit it directly and look at the returned JSON:

```json
{"status":200,"data":{"totalSubs":467,"subsInEachSource":{"bilibili":467},"failedSources":{}}}
```

`status` is the status code designed by Substats; `200` means the request succeeded.

`data` is the JSON object designed by Substats, and what we need is the value of the `totalSubs` key. Here it's 467.

Now, using the fixed API service URL and the key in the fixed JSON object whose value we want, we can tell Shields.io to do the job for us.

### Shields' Dynamic Badge API

The format is:

`https://img.shields.io/badge/dynamic/json?url=<API请求网址>&label=<左标签文本>&query=<JSON的键>&color=<右消息背景颜色>&prefix=<前缀>&suffix=<后缀>`

(API request URL, left label text, JSON key, right message background color, prefix, suffix)

You generally won't need the prefix and suffix.

Again, let's use displaying my bilibili follower count as the example:

`https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.spencerwoo.com%2Fsubstats%2F%3Fsource%3Dbilibili%26queryKey%3D33320940&label=bilibili%20fans&query=%24.data.totalSubs&color=282c34`

<img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.spencerwoo.com%2Fsubstats%2F%3Fsource%3Dbilibili%26queryKey%3D33320940&label=bilibili%20fans&query=$.data.totalSubs&color=282c34" class="nofancybox">

The URL above has been escaped. In reality, `API请求网址` (API request URL) is `https://api.spencerwoo.com/substats/?source=bilibili&queryKey=33320940`, `左标签文本` (left label text) is `bilibili fans`, `JSON的键` (JSON key) is `$.data.totalSubs`, and `右消息背景颜色` (right message background color) is `282c34`. The prefix and suffix are simply ignored, so we don't add `&prefix=<..>&suffix=<..>`.

You can also go to Shields.io, fill in the corresponding fields, and click `Make Badge`:

![shields-dynamic-badge](/img/markdown_20201102171657.png)

That covers static and dynamic badges. You may have noticed: wait, the earlier examples also had a pink label and the little bilibili TV logo! That's right, next up is the "beautification" stuff everyone really cares about.

## Beautification

### Showing an Icon

You can add `&logo=bilibili` to the URL above; the result looks like this:

<img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.spencerwoo.com%2Fsubstats%2F%3Fsource%3Dbilibili%26queryKey%3D33320940&label=bilibili%20fans&query=$.data.totalSubs&color=282c34&logo=bilibili" class="nofancybox">

For icons, search by name on [simpleicons](https://simpleicons.org/). If the icon is there, you can use its name directly.

For example, I could change it to `&logo=baidu`

and the result becomes:

<img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.spencerwoo.com%2Fsubstats%2F%3Fsource%3Dbilibili%26queryKey%3D33320940&label=bilibili%20fans&query=$.data.totalSubs&color=282c34&logo=baidu" class="nofancybox">

If simpleicons doesn't have the icon you want, you can use a custom icon

A custom icon needs to be passed in as base64. For example, simpleicons doesn't have a NetEase Cloud Music icon, so I had to find a NetEase Cloud Music SVG icon myself and convert it to base64. You can do the conversion on this site: https://www.css-js.com/tools/base64.html

You can find icons on easyicon.net: https://www.easyicon.net

There are plenty of other SVG icon search sites worth checking out too.

Here I [searched easyicon for NetEase Cloud Music](https://www.easyicon.net/language.en/iconsearch/%E7%BD%91%E6%98%93%E4%BA%91%E9%9F%B3%E4%B9%90/)

Drag the SVG file of the NetEase Cloud Music logo onto the conversion site mentioned above, uncheck "使用在 css 中" (use in CSS), and click "Copy code" to get the base64 code on your clipboard:

![tobase64](/img/markdown_20201102180827.png)

```text
data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiBwcmVzZXJ2ZUFzcGVjdFJhdGlvPSJ4TWlkWU1pZCIgd2lkdGg9IjMxLjAzMSIgaGVpZ2h0PSIzNCIgdmlld0JveD0iMCAwIDMxLjAzMSAzNCI+CiAgPGRlZnM+CiAgICA8c3R5bGU+CiAgICAgIC5jbHMtMSB7CiAgICAgICAgZmlsbDogIzAwMDsKICAgICAgICBmaWxsLXJ1bGU6IGV2ZW5vZGQ7CiAgICAgIH0KICAgIDwvc3R5bGU+CiAgPC9kZWZzPgogIDxwYXRoIGQ9Ik0yMS4yNzksLTAuMDE1IEMyMS42MzAsMC4wNDEgMjEuOTg1LDAuMDgxIDIyLjMzMywwLjE1NiBDMjMuNTUzLDAuNDE5IDI0LjY0NiwwLjk0OCAyNS42MTEsMS43MjMgQzI2LjI0NCwyLjIzMSAyNi41MDIsMi44OTQgMjYuMzE5LDMuNjc5IEMyNi4xNTQsNC4zODUgMjUuNjkzLDQuODYxIDI0Ljk4MSw1LjA2NCBDMjQuMzA3LDUuMjU2IDIzLjY5OSw1LjExMCAyMy4xNDYsNC42NzcgQzIyLjQ0NSw0LjEyNyAyMS42NjcsMy43NDcgMjAuNzM1LDMuODI4IEMxOS45NDUsMy44OTcgMTkuMTkwLDQuNzEwIDE5LjI1OCw1LjQzNiBDMTkuMjg4LDUuNzYxIDE5LjQwNyw2LjA3OCAxOS40OTEsNi4zOTggQzE5LjY0MCw2Ljk2MiAxOS43OTQsNy41MjUgMTkuOTQ1LDguMDg5IEMxOS45NzEsOC4xODYgMTkuOTk2LDguMjYzIDIwLjEzNSw4LjI3MSBDMjIuMjU4LDguMzg0IDI0LjE3MSw5LjA2MCAyNS44NzYsMTAuMzEzIEMyNy41NTIsMTEuNTQ1IDI4LjkyNCwxMy4wMjQgMjkuODQ0LDE0Ljg4MiBDMzAuNTE5LDE2LjI0NiAzMC44OTcsMTcuNjg2IDMwLjk5NywxOS4xOTcgQzMxLjEzMCwyMS4yMDYgMzAuODg5LDIzLjE3MSAzMC4wOTAsMjUuMDI2IEMyOC4yMzIsMjkuMzM4IDI0Ljk2NSwzMi4xMTkgMjAuMzcxLDMzLjM5NyBDMTguNjIzLDMzLjg4NCAxNi44MzIsMzQuMDc0IDE1LjAxOSwzMy45NzMgQzExLjI1MCwzMy43NjMgNy45ODUsMzIuMzcwIDUuMjM1LDI5Ljg1MSBDMi41MjEsMjcuMzY3IDAuODI5LDI0LjMxMiAwLjI0MSwyMC43MjYgQy0wLjU2MCwxNS44NDggMC42NjgsMTEuNDc1IDMuOTE3LDcuNjgyIEM1LjcwMSw1LjU5OCA3LjkyOCw0LjA5NyAxMC41MjUsMy4xMjggQzExLjQyMCwyLjc5MyAxMi4zOTksMy4xMDUgMTIuODkwLDMuODY5IEMxMy4zOTIsNC42NTAgMTMuMjc0LDUuNjU1IDEyLjU3OSw2LjI3NiBDMTIuMzgzLDYuNDUyIDEyLjEzNSw2LjU5MSAxMS44ODcsNi42OTAgQzcuOTI4LDguMjcxIDUuMzEzLDExLjA1NiA0LjI3NCwxNS4xMTggQzMuMjY2LDE5LjA1OCA0LjE1NywyMi42NjUgNi43MzAsMjUuODQzIEM4LjM0MywyNy44MzUgMTAuNDI3LDI5LjE3MyAxMi45NDksMjkuODMwIEMxNC41NzksMzAuMjU1IDE2LjIyNiwzMC4yODIgMTcuODg2LDMwLjAzMSBDMTkuNTk5LDI5Ljc3MiAyMS4xOTksMjkuMjIxIDIyLjYzNCwyOC4yNjAgQzI0LjYwOCwyNi45MzcgMjYuMDE1LDI1LjE3NCAyNi43MTgsMjIuOTMwIEMyNy4zMjUsMjAuOTkzIDI3LjM0NiwxOS4wMzcgMjYuNTk2LDE3LjExNSBDMjUuOTkyLDE1LjU2OCAyNC45MjQsMTQuMzc4IDIzLjU4NSwxMy4zOTYgQzIyLjg3MCwxMi44NzEgMjIuMTAyLDEyLjQ2MiAyMS4yMjYsMTIuMjYxIEMyMS4xODYsMTIuMjUyIDIxLjE0NSwxMi4yNDcgMjEuMDczLDEyLjIzNiBDMjEuMTkzLDEyLjY4NCAyMS4zMDQsMTMuMTEwIDIxLjQxOSwxMy41MzUgQzIxLjY5NywxNC41NTkgMjEuOTgxLDE1LjU4MiAyMi4yNTQsMTYuNjA4IEMyMi44NDcsMTguODM4IDIyLjI3MywyMC43OTEgMjAuNzA0LDIyLjQ1NSBDMTkuMjUyLDIzLjk5NSAxNy40MDQsMjQuNjY1IDE1LjI4NSwyNC40NjQgQzEyLjkyNSwyNC4yNDAgMTEuMjQwLDIyLjk4NyAxMC4xNDEsMjAuOTU4IEM5LjU2NSwxOS44OTYgOS4zMTcsMTguNzUxIDkuMjcxLDE3LjU1MyBDOS4xOTgsMTUuNjQ1IDkuNjUzLDEzLjg4NCAxMC43NzAsMTIuMzA5IEMxMS45NzAsMTAuNjE4IDEzLjYzMSw5LjUzMyAxNS41OTUsOC44NTkgQzE1Ljc0OSw4LjgwNiAxNS45MDYsOC43NTggMTYuMDg3LDguNjk5IEMxNS45ODEsOC4zMDYgMTUuODcxLDcuOTIzIDE1Ljc3Niw3LjUzNyBDMTUuNjQ1LDcuMDA1IDE1LjQ3Nyw2LjQ3NiAxNS40MTEsNS45MzYgQzE1LjIxNyw0LjMzOCAxNS43MTgsMi45NDkgMTYuODQ2LDEuNzg1IEMxNy43NzAsMC44MzMgMTguODkwLDAuMjI5IDIwLjIzMiwwLjA0OCBDMjAuMzgwLDAuMDI4IDIwLjUyNywwLjAwNiAyMC42NzUsLTAuMDE1IEMyMC44NzYsLTAuMDE1IDIxLjA3NywtMC4wMTUgMjEuMjc5LC0wLjAxNSBaTTE3LjA4OCwxMi4zODcgQzE1LjkyNSwxMi43NDkgMTQuOTIxLDEzLjMwMSAxNC4xNjgsMTQuMjE5IEMxMy4xNjEsMTUuNDQ5IDEyLjk2MCwxNi44NjIgMTMuMjgxLDE4LjM2MyBDMTMuNDQ4LDE5LjE0MyAxMy44MzgsMTkuODEwIDE0LjUyMiwyMC4yNzYgQzE1LjM3NywyMC44NTggMTYuNTQyLDIwLjgzMyAxNy40MzYsMjAuMjI4IEMxOC4zNTAsMTkuNjA4IDE4Ljc1NywxOC42MDkgMTguNDkwLDE3LjU4NSBDMTguMTk4LDE2LjQ2MyAxNy44ODcsMTUuMzQ1IDE3LjU4NCwxNC4yMjUgQzE3LjQyMSwxMy42MjMgMTcuMjU4LDEzLjAxOSAxNy4wODgsMTIuMzg3IFoiIGNsYXNzPSJjbHMtMSIvPgo8L3N2Zz4K
```

Then you can pass in

```text
&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiBwcmVzZXJ2ZUFzcGVjdFJhdGlvPSJ4TWlkWU1pZCIgd2lkdGg9IjMxLjAzMSIgaGVpZ2h0PSIzNCIgdmlld0JveD0iMCAwIDMxLjAzMSAzNCI+CiAgPGRlZnM+CiAgICA8c3R5bGU+CiAgICAgIC5jbHMtMSB7CiAgICAgICAgZmlsbDogIzAwMDsKICAgICAgICBmaWxsLXJ1bGU6IGV2ZW5vZGQ7CiAgICAgIH0KICAgIDwvc3R5bGU+CiAgPC9kZWZzPgogIDxwYXRoIGQ9Ik0yMS4yNzksLTAuMDE1IEMyMS42MzAsMC4wNDEgMjEuOTg1LDAuMDgxIDIyLjMzMywwLjE1NiBDMjMuNTUzLDAuNDE5IDI0LjY0NiwwLjk0OCAyNS42MTEsMS43MjMgQzI2LjI0NCwyLjIzMSAyNi41MDIsMi44OTQgMjYuMzE5LDMuNjc5IEMyNi4xNTQsNC4zODUgMjUuNjkzLDQuODYxIDI0Ljk4MSw1LjA2NCBDMjQuMzA3LDUuMjU2IDIzLjY5OSw1LjExMCAyMy4xNDYsNC42NzcgQzIyLjQ0NSw0LjEyNyAyMS42NjcsMy43NDcgMjAuNzM1LDMuODI4IEMxOS45NDUsMy44OTcgMTkuMTkwLDQuNzEwIDE5LjI1OCw1LjQzNiBDMTkuMjg4LDUuNzYxIDE5LjQwNyw2LjA3OCAxOS40OTEsNi4zOTggQzE5LjY0MCw2Ljk2MiAxOS43OTQsNy41MjUgMTkuOTQ1LDguMDg5IEMxOS45NzEsOC4xODYgMTkuOTk2LDguMjYzIDIwLjEzNSw4LjI3MSBDMjIuMjU4LDguMzg0IDI0LjE3MSw5LjA2MCAyNS44NzYsMTAuMzEzIEMyNy41NTIsMTEuNTQ1IDI4LjkyNCwxMy4wMjQgMjkuODQ0LDE0Ljg4MiBDMzAuNTE5LDE2LjI0NiAzMC44OTcsMTcuNjg2IDMwLjk5NywxOS4xOTcgQzMxLjEzMCwyMS4yMDYgMzAuODg5LDIzLjE3MSAzMC4wOTAsMjUuMDI2IEMyOC4yMzIsMjkuMzM4IDI0Ljk2NSwzMi4xMTkgMjAuMzcxLDMzLjM5NyBDMTguNjIzLDMzLjg4NCAxNi44MzIsMzQuMDc0IDE1LjAxOSwzMy45NzMgQzExLjI1MCwzMy43NjMgNy45ODUsMzIuMzcwIDUuMjM1LDI5Ljg1MSBDMi41MjEsMjcuMzY3IDAuODI5LDI0LjMxMiAwLjI0MSwyMC43MjYgQy0wLjU2MCwxNS44NDggMC42NjgsMTEuNDc1IDMuOTE3LDcuNjgyIEM1LjcwMSw1LjU5OCA3LjkyOCw0LjA5NyAxMC41MjUsMy4xMjggQzExLjQyMCwyLjc5MyAxMi4zOTksMy4xMDUgMTIuODkwLDMuODY5IEMxMy4zOTIsNC42NTAgMTMuMjc0LDUuNjU1IDEyLjU3OSw2LjI3NiBDMTIuMzgzLDYuNDUyIDEyLjEzNSw2LjU5MSAxMS44ODcsNi42OTAgQzcuOTI4LDguMjcxIDUuMzEzLDExLjA1NiA0LjI3NCwxNS4xMTggQzMuMjY2LDE5LjA1OCA0LjE1NywyMi42NjUgNi43MzAsMjUuODQzIEM4LjM0MywyNy44MzUgMTAuNDI3LDI5LjE3MyAxMi45NDksMjkuODMwIEMxNC41NzksMzAuMjU1IDE2LjIyNiwzMC4yODIgMTcuODg2LDMwLjAzMSBDMTkuNTk5LDI5Ljc3MiAyMS4xOTksMjkuMjIxIDIyLjYzNCwyOC4yNjAgQzI0LjYwOCwyNi45MzcgMjYuMDE1LDI1LjE3NCAyNi43MTgsMjIuOTMwIEMyNy4zMjUsMjAuOTkzIDI3LjM0NiwxOS4wMzcgMjYuNTk2LDE3LjExNSBDMjUuOTkyLDE1LjU2OCAyNC45MjQsMTQuMzc4IDIzLjU4NSwxMy4zOTYgQzIyLjg3MCwxMi44NzEgMjIuMTAyLDEyLjQ2MiAyMS4yMjYsMTIuMjYxIEMyMS4xODYsMTIuMjUyIDIxLjE0NSwxMi4yNDcgMjEuMDczLDEyLjIzNiBDMjEuMTkzLDEyLjY4NCAyMS4zMDQsMTMuMTEwIDIxLjQxOSwxMy41MzUgQzIxLjY5NywxNC41NTkgMjEuOTgxLDE1LjU4MiAyMi4yNTQsMTYuNjA4IEMyMi44NDcsMTguODM4IDIyLjI3MywyMC43OTEgMjAuNzA0LDIyLjQ1NSBDMTkuMjUyLDIzLjk5NSAxNy40MDQsMjQuNjY1IDE1LjI4NSwyNC40NjQgQzEyLjkyNSwyNC4yNDAgMTEuMjQwLDIyLjk4NyAxMC4xNDEsMjAuOTU4IEM5LjU2NSwxOS44OTYgOS4zMTcsMTguNzUxIDkuMjcxLDE3LjU1MyBDOS4xOTgsMTUuNjQ1IDkuNjUzLDEzLjg4NCAxMC43NzAsMTIuMzA5IEMxMS45NzAsMTAuNjE4IDEzLjYzMSw5LjUzMyAxNS41OTUsOC44NTkgQzE1Ljc0OSw4LjgwNiAxNS45MDYsOC43NTggMTYuMDg3LDguNjk5IEMxNS45ODEsOC4zMDYgMTUuODcxLDcuOTIzIDE1Ljc3Niw3LjUzNyBDMTUuNjQ1LDcuMDA1IDE1LjQ3Nyw2LjQ3NiAxNS40MTEsNS45MzYgQzE1LjIxNyw0LjMzOCAxNS43MTgsMi45NDkgMTYuODQ2LDEuNzg1IEMxNy43NzAsMC44MzMgMTguODkwLDAuMjI5IDIwLjIzMiwwLjA0OCBDMjAuMzgwLDAuMDI4IDIwLjUyNywwLjAwNiAyMC42NzUsLTAuMDE1IEMyMC44NzYsLTAuMDE1IDIxLjA3NywtMC4wMTUgMjEuMjc5LC0wLjAxNSBaTTE3LjA4OCwxMi4zODcgQzE1LjkyNSwxMi43NDkgMTQuOTIxLDEzLjMwMSAxNC4xNjgsMTQuMjE5IEMxMy4xNjEsMTUuNDQ5IDEyLjk2MCwxNi44NjIgMTMuMjgxLDE4LjM2MyBDMTMuNDQ4LDE5LjE0MyAxMy44MzgsMTkuODEwIDE0LjUyMiwyMC4yNzYgQzE1LjM3NywyMC44NTggMTYuNTQyLDIwLjgzMyAxNy40MzYsMjAuMjI4IEMxOC4zNTAsMTkuNjA4IDE4Ljc1NywxOC42MDkgMTguNDkwLDE3LjU4NSBDMTguMTk4LDE2LjQ2MyAxNy44ODcsMTUuMzQ1IDE3LjU4NCwxNC4yMjUgQzE3LjQyMSwxMy42MjMgMTcuMjU4LDEzLjAxOSAxNy4wODgsMTIuMzg3IFoiIGNsYXNzPSJjbHMtMSIvPgo8L3N2Zz4K
```

Result:

<img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.spencerwoo.com%2Fsubstats%2F%3Fsource%3Dbilibili%26queryKey%3D33320940&label=bilibili%20fans&query=$.data.totalSubs&color=282c34&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiBwcmVzZXJ2ZUFzcGVjdFJhdGlvPSJ4TWlkWU1pZCIgd2lkdGg9IjMxLjAzMSIgaGVpZ2h0PSIzNCIgdmlld0JveD0iMCAwIDMxLjAzMSAzNCI+CiAgPGRlZnM+CiAgICA8c3R5bGU+CiAgICAgIC5jbHMtMSB7CiAgICAgICAgZmlsbDogIzAwMDsKICAgICAgICBmaWxsLXJ1bGU6IGV2ZW5vZGQ7CiAgICAgIH0KICAgIDwvc3R5bGU+CiAgPC9kZWZzPgogIDxwYXRoIGQ9Ik0yMS4yNzksLTAuMDE1IEMyMS42MzAsMC4wNDEgMjEuOTg1LDAuMDgxIDIyLjMzMywwLjE1NiBDMjMuNTUzLDAuNDE5IDI0LjY0NiwwLjk0OCAyNS42MTEsMS43MjMgQzI2LjI0NCwyLjIzMSAyNi41MDIsMi44OTQgMjYuMzE5LDMuNjc5IEMyNi4xNTQsNC4zODUgMjUuNjkzLDQuODYxIDI0Ljk4MSw1LjA2NCBDMjQuMzA3LDUuMjU2IDIzLjY5OSw1LjExMCAyMy4xNDYsNC42NzcgQzIyLjQ0NSw0LjEyNyAyMS42NjcsMy43NDcgMjAuNzM1LDMuODI4IEMxOS45NDUsMy44OTcgMTkuMTkwLDQuNzEwIDE5LjI1OCw1LjQzNiBDMTkuMjg4LDUuNzYxIDE5LjQwNyw2LjA3OCAxOS40OTEsNi4zOTggQzE5LjY0MCw2Ljk2MiAxOS43OTQsNy41MjUgMTkuOTQ1LDguMDg5IEMxOS45NzEsOC4xODYgMTkuOTk2LDguMjYzIDIwLjEzNSw4LjI3MSBDMjIuMjU4LDguMzg0IDI0LjE3MSw5LjA2MCAyNS44NzYsMTAuMzEzIEMyNy41NTIsMTEuNTQ1IDI4LjkyNCwxMy4wMjQgMjkuODQ0LDE0Ljg4MiBDMzAuNTE5LDE2LjI0NiAzMC44OTcsMTcuNjg2IDMwLjk5NywxOS4xOTcgQzMxLjEzMCwyMS4yMDYgMzAuODg5LDIzLjE3MSAzMC4wOTAsMjUuMDI2IEMyOC4yMzIsMjkuMzM4IDI0Ljk2NSwzMi4xMTkgMjAuMzcxLDMzLjM5NyBDMTguNjIzLDMzLjg4NCAxNi44MzIsMzQuMDc0IDE1LjAxOSwzMy45NzMgQzExLjI1MCwzMy43NjMgNy45ODUsMzIuMzcwIDUuMjM1LDI5Ljg1MSBDMi41MjEsMjcuMzY3IDAuODI5LDI0LjMxMiAwLjI0MSwyMC43MjYgQy0wLjU2MCwxNS44NDggMC42NjgsMTEuNDc1IDMuOTE3LDcuNjgyIEM1LjcwMSw1LjU5OCA3LjkyOCw0LjA5NyAxMC41MjUsMy4xMjggQzExLjQyMCwyLjc5MyAxMi4zOTksMy4xMDUgMTIuODkwLDMuODY5IEMxMy4zOTIsNC42NTAgMTMuMjc0LDUuNjU1IDEyLjU3OSw2LjI3NiBDMTIuMzgzLDYuNDUyIDEyLjEzNSw2LjU5MSAxMS44ODcsNi42OTAgQzcuOTI4LDguMjcxIDUuMzEzLDExLjA1NiA0LjI3NCwxNS4xMTggQzMuMjY2LDE5LjA1OCA0LjE1NywyMi42NjUgNi43MzAsMjUuODQzIEM4LjM0MywyNy44MzUgMTAuNDI3LDI5LjE3MyAxMi45NDksMjkuODMwIEMxNC41NzksMzAuMjU1IDE2LjIyNiwzMC4yODIgMTcuODg2LDMwLjAzMSBDMTkuNTk5LDI5Ljc3MiAyMS4xOTksMjkuMjIxIDIyLjYzNCwyOC4yNjAgQzI0LjYwOCwyNi45MzcgMjYuMDE1LDI1LjE3NCAyNi43MTgsMjIuOTMwIEMyNy4zMjUsMjAuOTkzIDI3LjM0NiwxOS4wMzcgMjYuNTk2LDE3LjExNSBDMjUuOTkyLDE1LjU2OCAyNC45MjQsMTQuMzc4IDIzLjU4NSwxMy4zOTYgQzIyLjg3MCwxMi44NzEgMjIuMTAyLDEyLjQ2MiAyMS4yMjYsMTIuMjYxIEMyMS4xODYsMTIuMjUyIDIxLjE0NSwxMi4yNDcgMjEuMDczLDEyLjIzNiBDMjEuMTkzLDEyLjY4NCAyMS4zMDQsMTMuMTEwIDIxLjQxOSwxMy41MzUgQzIxLjY5NywxNC41NTkgMjEuOTgxLDE1LjU4MiAyMi4yNTQsMTYuNjA4IEMyMi44NDcsMTguODM4IDIyLjI3MywyMC43OTEgMjAuNzA0LDIyLjQ1NSBDMTkuMjUyLDIzLjk5NSAxNy40MDQsMjQuNjY1IDE1LjI4NSwyNC40NjQgQzEyLjkyNSwyNC4yNDAgMTEuMjQwLDIyLjk4NyAxMC4xNDEsMjAuOTU4IEM5LjU2NSwxOS44OTYgOS4zMTcsMTguNzUxIDkuMjcxLDE3LjU1MyBDOS4xOTgsMTUuNjQ1IDkuNjUzLDEzLjg4NCAxMC43NzAsMTIuMzA5IEMxMS45NzAsMTAuNjE4IDEzLjYzMSw5LjUzMyAxNS41OTUsOC44NTkgQzE1Ljc0OSw4LjgwNiAxNS45MDYsOC43NTggMTYuMDg3LDguNjk5IEMxNS45ODEsOC4zMDYgMTUuODcxLDcuOTIzIDE1Ljc3Niw3LjUzNyBDMTUuNjQ1LDcuMDA1IDE1LjQ3Nyw2LjQ3NiAxNS40MTEsNS45MzYgQzE1LjIxNyw0LjMzOCAxNS43MTgsMi45NDkgMTYuODQ2LDEuNzg1IEMxNy43NzAsMC44MzMgMTguODkwLDAuMjI5IDIwLjIzMiwwLjA0OCBDMjAuMzgwLDAuMDI4IDIwLjUyNywwLjAwNiAyMC42NzUsLTAuMDE1IEMyMC44NzYsLTAuMDE1IDIxLjA3NywtMC4wMTUgMjEuMjc5LC0wLjAxNSBaTTE3LjA4OCwxMi4zODcgQzE1LjkyNSwxMi43NDkgMTQuOTIxLDEzLjMwMSAxNC4xNjgsMTQuMjE5IEMxMy4xNjEsMTUuNDQ5IDEyLjk2MCwxNi44NjIgMTMuMjgxLDE4LjM2MyBDMTMuNDQ4LDE5LjE0MyAxMy44MzgsMTkuODEwIDE0LjUyMiwyMC4yNzYgQzE1LjM3NywyMC44NTggMTYuNTQyLDIwLjgzMyAxNy40MzYsMjAuMjI4IEMxOC4zNTAsMTkuNjA4IDE4Ljc1NywxOC42MDkgMTguNDkwLDE3LjU4NSBDMTguMTk4LDE2LjQ2MyAxNy44ODcsMTUuMzQ1IDE3LjU4NCwxNC4yMjUgQzE3LjQyMSwxMy42MjMgMTcuMjU4LDEzLjAxOSAxNy4wODgsMTIuMzg3IFoiIGNsYXNzPSJjbHMtMSIvPgo8L3N2Zz4K" class="nofancybox">

As you can see, the NetEase Cloud Music logo shows up successfully.

### Label Color

You can add another parameter, `&labelColor={颜色值}` (color value)

For example, in the earlier bilibili example, I want the label to be pink, `FE7398`

So I add the parameter `&labelColor=FE7398`

The result:

<img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.spencerwoo.com%2Fsubstats%2F%3Fsource%3Dbilibili%26queryKey%3D33320940&label=bilibili%20fans&query=$.data.totalSubs&color=282c34&logo=bilibili&labelColor=FE7398" class="nofancybox">

Of course, as before, the existing English color options are supported. Putting in pink probably won't look too different.

But now the icon is blue, which doesn't quite go with the white text, and it doesn't contrast well with the pink either. I think white would be better, so what do we do?

### Icon Color

Just add the parameter `&logoColor={颜色值}` (color value).

Here I'll add `&logoColor=white` and see how it looks:

<img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.spencerwoo.com%2Fsubstats%2F%3Fsource%3Dbilibili%26queryKey%3D33320940&label=bilibili%20fans&query=$.data.totalSubs&color=282c34&logo=bilibili&labelColor=FE7398&logoColor=white" class="nofancybox">

Look, that looks great!

### Badge Style

Badges come in 5 styles. Here's the example from the official site:

![badge-style](/img/markdown_20201102180012.png)

The 5 styles are `plastic`, `flat`, `flat-square`, `for-the-badge` and `social`

Let's add `&style=for-the-badge` to the earlier URL and see how it looks:

<img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.spencerwoo.com%2Fsubstats%2F%3Fsource%3Dbilibili%26queryKey%3D33320940&label=bilibili%20fans&query=$.data.totalSubs&color=282c34&logo=bilibili&labelColor=FE7398&logoColor=white&style=for-the-badge" class="nofancybox">

WOW! Not bad, huh

At this point, the badge URL is

```text
https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.spencerwoo.com%2Fsubstats%2F%3Fsource%3Dbilibili%26queryKey%3D33320940&label=bilibili%20fans&query=$.data.totalSubs&color=282c34&logo=bilibili&labelColor=FE7398&logoColor=white&style=for-the-badge
```

Finally, just display the badge with an \<img\> tag or markdown's \!\[\]\(\) syntax and you're done!

For example

```html
<img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.spencerwoo.com%2Fsubstats%2F%3Fsource%3Dbilibili%26queryKey%3D33320940&label=bilibili%20fans&query=$.data.totalSubs&color=282c34&logo=bilibili&labelColor=FE7398&logoColor=white&style=for-the-badge">
```

or

```markdown
![bilibili fans badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.spencerwoo.com%2Fsubstats%2F%3Fsource%3Dbilibili%26queryKey%3D33320940&label=bilibili%20fans&query=$.data.totalSubs&color=282c34&logo=bilibili&labelColor=FE7398&logoColor=white&style=for-the-badge)
```

### More Parameters

For more parameters, see the [Shields.io website](https://shields.io/), which provides examples.

# Summary

After all that fiddling, I've finally gone through how to use Shields.io and Substats.

Badges look great. Have you learned how to make them? If you can, try writing your own API service (after all, Substats is only so-so in terms of speed).