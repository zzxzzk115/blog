---
title: 'Enabling OpenGL Hardware Acceleration on PocketChip'
date: 2022-05-12T19:47:41
tags: [PocketChip, OpenGL]
categories: [Retro Handhelds]
toc: true
aiTranslated: true
---

> This post is reposted with permission. Original article: https://www.xuefei.net.cn/index.php/archives/89/

<article class="post" itemscope="" itemtype="http://schema.org/BlogPosting">
        <ul class="post-meta">
            <li itemprop="author" itemscope="" itemtype="http://schema.org/Person">Author: <a itemprop="name" href="https://www.xuefei.net.cn/index.php/author/1/" rel="author">xuefei</a></li>
            <li>Date: <time datetime="2020-04-14T15:18:00+08:00" itemprop="datePublished">2020-04-14</time></li>
            <li>Category: <a href="https://www.xuefei.net.cn/index.php/category/pocketchip/">pocketchip</a></li>
        </ul>
        <div class="post-content" itemprop="articleBody">
            <p>sudo apt-get install cmake<br>sudo apt-get install libx11-dev</p><p>git clone <a href="https://github.com/ptitSeb/gl4es.git">https://github.com/ptitSeb/gl4es.git</a></p><pre><code>cd gl4es
mkdir build
cd build
cmake .. -DCHIP=1 -DCMAKE_BUILD_TYPE=RelWithDebInfo
//leave out -j2, otherwise it easily runs out of memory
make </code></pre><p>cd ../<br>cd lib/ <br>sudo mv libGL.so.1 /usr/lib/arm-linux-gnueabihf/libGL.so.1.2.0</p><p>If you previously installed <a href="https://www.xuefei.net.cn/index.php/archives/90/">xf86-video-fbturbo</a>, disable it first<br>sudo nano /etc/X11/xorg.conf</p><pre><code>#Section "Device"
#        Identifier      "Allwinner A10/A13 FBDEV"
#        Driver          "fbturbo"
#        Option          "fbdev" "/dev/fb0" 
#        Option          "SwapbuffersWait" "true"
#EndSection</code></pre><p>Then reboot</p><p>sudo apt-get install mesa-utils<br>glxgears</p><p>On the GUI version you'll see the image below. On the home version you may not see the gears, because the window is too big...<br><img src="https://www.xuefei.net.cn/usr/uploads/2020/04/2157792144.jpg" alt="TIM图片20200414151753.jpg" title="TIM图片20200414151753.jpg"></p><p>Related links<br><a href="https://github.com/ptitSeb/gl4es"></a><a href="https://github.com/ptitSeb/gl4es">https://github.com/ptitSeb/gl4es</a><br><a href="https://forum.armbian.com/topic/1420-opengl-on-mali-gpu-bananapi-orangepi-pc-etc/"></a><a href="https://forum.armbian.com/topic/1420-opengl-on-mali-gpu-bananapi-orangepi-pc-etc/">https://forum.armbian.com/topic/1420-opengl-on-mali-gpu-bananapi-orangepi-pc-etc/</a></p>        </div>
        <p itemprop="keywords" class="tags">Tags: <a href="https://www.xuefei.net.cn/index.php/tag/PocketChip/">PocketChip</a>, <a href="https://www.xuefei.net.cn/index.php/tag/%E7%A1%AC%E4%BB%B6%E5%8A%A0%E9%80%9F/">Hardware acceleration</a>, <a href="https://www.xuefei.net.cn/index.php/tag/opengl/">opengl</a></p>
    </article>

----

2022/05/12 Migrated here from cnblogs.
