---
title: 'Pocketchip 安装 Love2D 11.3 折腾分享'
date: 2020-04-10T02:19:00
tags: [PocketChip, Love2D]
categories: [复古掌机]
toc: true
cnblogs: 12670880
---

> 本文最初发表于我在博客园的旧博客：[Pocketchip 安装 Love2D(最新 11.3) 折腾分享[成功]](https://www.cnblogs.com/lazy-v/p/12670880.html)（写于 2020-04-10）。

[Love2d](https://love2d.org)![](/img/markdown_20220512181405.png) 是一款游戏引擎，基于 C/C++ 编写，使用 Lua 脚本进行封装，简单易用、跨平台。

Pocketchip 换源、更新以后，通过 `sudo apt-get -f install love` 安装的版本实在是太老了(0.9)。

当然，0.10.2 比 0.9 稍微新一点，但是还是相对太老了，我试过，`No909.love` 无法正常运行，因为它是基于 11.1 版本编写的。

所以这次我尝试安装 11.3 版本。目标是能够运行 GameShell 默认自带的 `No909.love`。

<!--more-->

# 准备工作

## 下载 Love2D_11.3 版本的 Linux 源码

首先当然要下载 11.3 版本的 Love2d。

但是 11 开始不提供 armhf 版本的 deb 安装包了，所以我们选择源码编译安装。

下载 [love-11.3-linux-src.tar.gz](https://github.com/love2d/love/releases/download/11.3/love-11.3-linux-src.tar.gz)

## 安装 C/C++ 编译器与 Make

由于 Love2D 是 C/C++ 写的，就需要 `gcc` 和 `g++`，当然，由于 Love2D 源码安装使用了 `make`，我们也要安装 `make` 工具。其实很多软件包的依赖项都是 gcc、g++ 和 make，所以我们必须先装好它们。

`sudo apt-get install gcc g++ make`

## 安装 pkg-config

Pocketchip 没有自带 `pkg-config`，我们也要安装它，其他软件包也需要它。

`sudo apt-get install pkg-config`

## 安装 Lua 环境及 LuaJIT

`sudo apt-get install lua5.2` 安装 Lua5.2

LuaJIT 需要下载这个文件 [LuaJIT-2.0.5.tar.gz](https://web.archive.org/web/20240805175559/http://luajit.org/download/LuaJIT-2.0.5.tar.gz)（官网已不再提供，此为 Wayback Machine 存档）

LuaJIT 的安装很简单，先解压这个压缩包：

`tar -xzvf LuaJIT-2.0.5.tar.gz`

然后进入 LuaJIT 的根目录 `cd LuaJIT-2.0.5`

最后 `make & sudo make install` 即可。

## 安装 SDL2

大部分使用 C/C++ 编写的跨平台脚本游戏引擎，例如 Pygame、Love2D 等，都使用了 SDL2。

我们要安装它：

`sudo apt-get install libsdl2-dev`

## 安装 OpenAL

Love2D 音频采用 OpenAL，所以我们也要安装它：

`sudo apt-get install libopenal-dev`

## 安装 FreeType2

### 安装 python2 python3 环境

FreeType2 需要 Python2 Python3 以及对应的 pip 和 pip3。

我们安装它们：

`sudo apt-get install python python-pip python3 python3-pip`

### 下载 FreeType2 源码

下载：[freetype-2.10.1.tar.gz](https://download.savannah.gnu.org/releases/freetype/freetype-2.10.1.tar.gz)

解压:

`tar -xzvf freetype-2.10.1.tar.gz`

进入 FreeType2 根目录:

`cd freetype-2.10.1`

安装：

`make & sudo make install`

安装过程比较慢，可以看看书。

## 安装 libmodplug、libvorbis、libmpg123 以及 libtheora

`sudo apt-get install libmodplug-dev libvorbis-dev libmpg123-dev libtheora-dev` 

# 一切就绪，开始源码安装！

先解压 `love-11.3-linux-src.tar.gz`：

(tips: 这里看起来是 tar.gz，你以为是 gzip 压缩的，其实不然 hhh)

`tar -xvf love-11.3-linux-src.tar.gz`

然后进入它的根目录:

`cd love-11.3`

最后可以先确认一下有没有问题：

`./configure`

提示 `no` 不代表报错，最后执行完，没有错误提示的话就行

最后

`make & sudo make install`

安装过程更慢，可以睡个觉，第二天再看安装好了没吧，记得给 pocketchip 供电（开玩笑，不过的确要比较久，大概一个多小时，因为要编译的有很多...，用时间换最新的 Love2d，不亏！）。

安装成功！现在是 2020.04.10 的 01:59，终于等到你！

![](/img/markdown_20220512181430.png)

# 测试运行 No.909

把 GameShell 里的 No.909 和对应的 Logo 拷贝到 Pocketchip，我这里安装了增强版桌面，可以添加图标，指定运行的 shell，和 GameShell 添加自定义应用类似：

![](/img/markdown_20220512181445.png)

运行：

![](/img/markdown_20220512181507.png)



![](/img/markdown_20220512181544.png)



成功！

这说明 Love2D 的新游戏（分辨率合适）都能用 Pocketchip 玩了，怎么样，很赞吧！

但是实测，需要优化，帧数感人...，可能和 GPU 渲染有关。

用 Terminal 运行会报这个错，暂时不知道如何解决...

![](/img/markdown_20220512181603.png)

----

2022/05/12 从博客园迁移至此。
