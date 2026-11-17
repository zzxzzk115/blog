---
title: 'PocketChip安装RetroArch'
date: 2022-05-12T19:47:41
tags: [PocketChip, RetroArch]
categories: [Devices]
toc: true
---

> RetroArch是一款万能模拟器，通过加载不同的模拟器核心，可以运行各种模拟器游戏，你也可以设置各种配置，加滤镜和Shader，让一般的屏幕有着复古的体验。

# 准备工作

## 1. 下载依赖项

这次就不一一说明了，直接把要装的依赖项一口气发出来吧！

```bash
sudo apt update
sudo apt install -y libsdl1.2-dev libsdl2-dev libboost-system-dev libboost-filesystem-dev libboost-date-time-dev libfreeimage-dev libfreetype6-dev libeigen3-dev libcurl4-openssl-dev libasound2-dev libgl1-mesa-dev cmake build-essential pkg-config
```

## 2. 下载RetroArch的源码

```bash
git clone https://github.com/zzxzzk115/RetroArch.git
```

# 安装RetroArch

```bash
cd RetroArch
./configure --prefix=/home/chip/retroarch --enable-opengles --disable-oss --disable-sdl --disable-ffmpeg --disable-vg --disable-cg --enable-neon --enable-floathard --disable-wayland --disable-pulse --enable-dylib --enable-hid --enable-zlib --enable-7zip
make -j2
sudo make install
sudo chmod +x /home/chip/retroarch/bin/retroarch
sudo ln -s /home/chip/retroarch/bin/retroarch /usr/bin/retroarch
```

# 运行

`retroarch`

# 遇到的问题

一开始会有部分内容是黑框，这是因为没有下载assets。

我们选择`Online Updater->Update Assets`等候下载并自动解压。

自动解压完以后，图标能够正常显示，但屏幕的字体变得非常模糊。

接下来进入配置环节：

# 配置RetroArch

按ESC退出，我们把默认主题的字体删掉：

```bash
sudo rm ~/.config/retroarch/assets/xmb/monochrome/font.ttf
```

然后不想要打开后有鼠标显示，你就需要设置全屏。

重新打开retroarch

第二栏的`Video->Start in FullScreen Mode`打开即可。

你可能需要在玩游戏的时候呼出快捷菜单，你就要改绑一个热键设置：

第二栏的`Input->Input Hotkey Binds`里Menu toggle先回车，再按退格键(backspace)，完成绑定。

你可能觉得系统提示的字体太大，你可以修改配置：
`sudo nano .config/retroarch/retroarch.cfg`

找到video_font_size，从32改到16或者你想要的大小。

这样基本就配置完成了。

当然，想要运行够顺畅，你得先看看这篇:

[Pocketchip开启OpenGL硬件加速](http://blog.zhangkexuan.cn/2022/05/12/pocketchip-opengl-hardware-speedup/)

----

2022/05/12 从博客园迁移至此。
