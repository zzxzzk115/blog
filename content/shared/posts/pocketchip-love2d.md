---
title: 'Pocketchip安装Love2D 11.3折腾分享'
date: 2022-05-12T19:47:41
tags: [PocketChip, Love2D]
categories: [Devices]
toc: true
---

[Love2d](https://love2d.org)![](http://img.zhangkexuan.cn/markdown_20220512181405.png)是一款游戏引擎，基于C/C++编写，使用Lua脚本进行封装，简单易用、跨平台。

Pocketchip换源、更新以后，通过`sudo apt-get -f install love`安装的版本实在是太老了(0.9)。

当然，0.10.2比0.9稍微新一点，但是还是相对太老了，我试过，`No909.love`无法正常运行，因为它是基于11.1版本编写的。

所以这次我尝试安装11.3版本。目标是能够运行GameShell默认自带的`No909.love`。

<!--more-->

# 准备工作

## 1. 下载Love2D_11.3版本的Linux源码

首先当然要下载11.3版本的Love2d。

但是11开始不提供armhf版本的deb安装包了，所以我们选择源码编译安装。

下载[love-11.3-linux-src.tar.gz](https://bitbucket.org/rude/love/downloads/love-11.3-linux-src.tar.gz)

## 2. 安装C/C++编译器与Make

由于Love2D是C/C++写的，就需要`gcc`和`g++`，当然，由于Love2D源码安装使用了`make`，我们也要安装`make`工具。其实很多软件包的依赖项都是gcc、g++和make，所以我们必须先装好它们。

`sudo apt-get install gcc g++ make`

## 3. 安装pkg-config

Pocketchip没有自带`pkg-config`，我们也要安装它，其他软件包也需要它。

`sudo apt-get install pkg-config`

## 4. 安装Lua环境及LuaJIT

`sudo apt-get install lua5.2`安装Lua5.2

LuaJIT需要下载这个文件[LuaJIT-2.0.5.tar.gz](http://luajit.org/download/LuaJIT-2.0.5.tar.gz)

LuaJIT的安装很简单，先解压这个压缩包：

`tar -xzvf LuaJIT-2.0.5.tar.gz`

然后进入LuaJIT的根目录`cd LuaJIT-2.0.5`

最后`make & sudo make install`即可。

## 5. 安装SDL2

大部分使用C/C++编写的跨平台脚本游戏引擎，例如Pygame、Love2D等，都使用了SDL2。

我们要安装它：

`sudo apt-get install libsdl2-dev`

## 6. 安装OpenAL

Love2D音频采用OpenAL，所以我们也要安装它：

`sudo apt-get install libopenal-dev`

## 7. 安装FreeType2

### 1. 安装python2 python3环境

FreeType2需要Python2 Python3 以及对应的pip和pip3。

我们安装它们：

`sudo apt-get install python python-pip python3 python3-pip`

### 2. 下载FreeType2源码

下载：[freetype-2.10.1.tar.gz](https://ayera.dl.sourceforge.net/project/freetype/freetype2/2.10.1/freetype-2.10.1.tar.gz)

解压:

`tar -xzvf freetype-2.10.1.tar.gz`

进入FreeType2根目录:

`cd freetype-2.10.1`

安装：

`make & sudo make install`

安装过程比较慢，可以看看书。

## 8. 安装libmodplug、libvorbis、libmpg123以及libtheora

`sudo apt-get install libmodplug-dev libvorbis-dev libmpg123-dev libtheora-dev` 

# 一切就绪，开始源码安装！

先解压`love-11.3-linux-src.tar.gz`：

(tips: 这里看起来是tar.gz，你以为是gzip压缩的，其实不然hhh)

`tar -xvf love-11.3-linux-src.tar.gz`

然后进入它的根目录:

`cd love-11.3`

最后可以先确认一下有没有问题：

`./configure`

提示`no`不代表报错，最后执行完，没有错误提示的话就行

最后

`make & sudo make install`

安装过程更慢，可以睡个觉，第二天再看安装好了没吧，记得给pocketchip供电（开玩笑，不过的确要比较久，大概一个多小时，因为要编译的有很多...，用时间换最新的Love2d，不亏！）。

安装成功！现在是2020.04.10的01:59，终于等到你！

![](http://img.zhangkexuan.cn/markdown_20220512181430.png)

# 测试运行No.909

把GameShell里的No.909和对应的Logo拷贝到Pocketchip，我这里安装了增强版桌面，可以添加图标，指定运行的shell，和GameShell添加自定义应用类似：

![](http://img.zhangkexuan.cn/markdown_20220512181445.png)

运行：

![](http://img.zhangkexuan.cn/markdown_20220512181507.png)



![](http://img.zhangkexuan.cn/markdown_20220512181544.png)



成功！

这说明Love2D的新游戏（分辨率合适）都能用Pocketchip玩了，怎么样，很赞吧！

但是实测，需要优化，帧数感人...，可能和GPU渲染有关。

用Terminal运行会报这个错，暂时不知道如何解决...

![](http://img.zhangkexuan.cn/markdown_20220512181603.png)

----

2022/05/12 从博客园迁移至此。
