---
title: 'Enabling OpenGL Hardware Acceleration on PocketChip'
date: 2020-04-14T15:44:00
tags: [PocketChip, OpenGL]
categories: [Retro Handhelds]
toc: true
aiTranslated: true
cnblogs: 12698439
---

> Originally published on my old cnblogs blog: [\[转载\]Pocketchip开启OpenGL硬件加速，性能大提升！](https://www.cnblogs.com/lazy-v/p/12698439.html) (written 2020-04-14).

> This post is reposted with permission. Original article: https://www.xuefei.net.cn/index.php/archives/89/
>
> Author: [xuefei](https://www.xuefei.net.cn/index.php/author/1/) · Date: 2020-04-14 · Category: [pocketchip](https://www.xuefei.net.cn/index.php/category/pocketchip/)

Install the dependencies:

```bash
sudo apt-get install cmake
sudo apt-get install libx11-dev
```

Build [gl4es](https://github.com/ptitSeb/gl4es):

```bash
git clone https://github.com/ptitSeb/gl4es.git
cd gl4es
mkdir build
cd build
cmake .. -DCHIP=1 -DCMAKE_BUILD_TYPE=RelWithDebInfo
# -j2 left out: it tends to run out of memory
make
```

Replace the system libGL:

```bash
cd ../
cd lib/
sudo mv libGL.so.1 /usr/lib/arm-linux-gnueabihf/libGL.so.1.2.0
```

If you installed [xf86-video-fbturbo](https://www.xuefei.net.cn/index.php/archives/90/) before, disable it first:

```bash
sudo nano /etc/X11/xorg.conf
```

Comment out the fbturbo device section:

```ini
#Section "Device"
#        Identifier      "Allwinner A10/A13 FBDEV"
#        Driver          "fbturbo"
#        Option          "fbdev" "/dev/fb0"
#        Option          "SwapbuffersWait" "true"
#EndSection
```

Then reboot and test:

```bash
sudo apt-get install mesa-utils
glxgears
```

On the GUI edition you should see the picture below; on the home edition you might not see the gears, because the window is too big…

![glxgears running](https://www.xuefei.net.cn/usr/uploads/2020/04/2157792144.jpg)

Links:

- https://github.com/ptitSeb/gl4es
- https://forum.armbian.com/topic/1420-opengl-on-mali-gpu-bananapi-orangepi-pc-etc/

Tags: PocketChip, hardware acceleration, opengl

----

Migrated here from cnblogs on 2022/05/12.
