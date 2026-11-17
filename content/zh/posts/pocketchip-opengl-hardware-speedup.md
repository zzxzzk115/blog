---
title: 'PocketChip 开启 OpenGL 硬件加速'
date: 2020-04-14T15:44:00
tags: [PocketChip, OpenGL]
categories: [复古掌机]
toc: true
cnblogs: 12698439
---

> 本文最初发表于我在博客园的旧博客：[\[转载\]Pocketchip 开启 OpenGL 硬件加速，性能大提升！](https://www.cnblogs.com/lazy-v/p/12698439.html)（写于 2020-04-14）。

> 此篇为转载内容，经过转载许可。原文地址：https://www.xuefei.net.cn/index.php/archives/89/
>
> 作者：[xuefei](https://www.xuefei.net.cn/index.php/author/1/) · 时间：2020-04-14 · 分类：[pocketchip](https://www.xuefei.net.cn/index.php/category/pocketchip/)

安装依赖：

```bash
sudo apt-get install cmake
sudo apt-get install libx11-dev
```

编译 [gl4es](https://github.com/ptitSeb/gl4es)：

```bash
git clone https://github.com/ptitSeb/gl4es.git
cd gl4es
mkdir build
cd build
cmake .. -DCHIP=1 -DCMAKE_BUILD_TYPE=RelWithDebInfo
# -j2 不加了，易报内存不够
make
```

替换系统的 libGL：

```bash
cd ../
cd lib/
sudo mv libGL.so.1 /usr/lib/arm-linux-gnueabihf/libGL.so.1.2.0
```

如果之前安装了 [xf86-video-fbturbo](https://www.xuefei.net.cn/index.php/archives/90/)，请先禁用：

```bash
sudo nano /etc/X11/xorg.conf
```

把 fbturbo 的设备段注释掉：

```ini
#Section "Device"
#        Identifier      "Allwinner A10/A13 FBDEV"
#        Driver          "fbturbo"
#        Option          "fbdev" "/dev/fb0"
#        Option          "SwapbuffersWait" "true"
#EndSection
```

然后重启，再测试：

```bash
sudo apt-get install mesa-utils
glxgears
```

如果是 GUI 版会看到下图，如果是 home 版可能看不到齿轮，因为窗口太大……

![glxgears 运行效果](https://www.xuefei.net.cn/usr/uploads/2020/04/2157792144.jpg)

相关地址：

- https://github.com/ptitSeb/gl4es
- https://forum.armbian.com/topic/1420-opengl-on-mali-gpu-bananapi-orangepi-pc-etc/

标签：PocketChip、硬件加速、opengl

----

2022/05/12 从博客园迁移至此。
