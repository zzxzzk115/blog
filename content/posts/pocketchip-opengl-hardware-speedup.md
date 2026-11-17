---
title: 'PocketChip开启OpenGL硬件加速'
date: 2022-05-12T19:47:41
tags: [PocketChip, OpenGL]
categories: [Devices]
toc: true
---

> 此篇为转载内容，经过转载许可 原文地址https://www.xuefei.net.cn/index.php/archives/89/

<article class="post" itemscope="" itemtype="http://schema.org/BlogPosting">
        <ul class="post-meta">
            <li itemprop="author" itemscope="" itemtype="http://schema.org/Person">作者: <a itemprop="name" href="https://www.xuefei.net.cn/index.php/author/1/" rel="author">xuefei</a></li>
            <li>时间: <time datetime="2020-04-14T15:18:00+08:00" itemprop="datePublished">2020-04-14</time></li>
            <li>分类: <a href="https://www.xuefei.net.cn/index.php/category/pocketchip/">pocketchip</a></li>
        </ul>
        <div class="post-content" itemprop="articleBody">
            <p>sudo apt-get install cmake<br>sudo apt-get install libx11-dev</p><p>git clone <a href="https://github.com/ptitSeb/gl4es.git">https://github.com/ptitSeb/gl4es.git</a></p><pre><code>cd gl4es
mkdir build
cd build
cmake .. -DCHIP=1 -DCMAKE_BUILD_TYPE=RelWithDebInfo
//-j2不加了易报内存不够
make </code></pre><p>cd ../<br>cd lib/ <br>sudo mv libGL.so.1 /usr/lib/arm-linux-gnueabihf/libGL.so.1.2.0</p><p>如果之前安装了<a href="https://www.xuefei.net.cn/index.php/archives/90/">xf86-video-fbturbo</a> 请先禁用<br>sudo nano /etc/X11/xorg.conf</p><pre><code>#Section "Device"
#        Identifier      "Allwinner A10/A13 FBDEV"
#        Driver          "fbturbo"
#        Option          "fbdev" "/dev/fb0" 
#        Option          "SwapbuffersWait" "true"
#EndSection</code></pre><p>然后重启</p><p>sudo apt-get install mesa-utils<br>glxgears</p><p>如果是GUI版会看到下图，如果是home版可能看不到齿轮，因为窗口太大……<br><img src="https://www.xuefei.net.cn/usr/uploads/2020/04/2157792144.jpg" alt="TIM图片20200414151753.jpg" title="TIM图片20200414151753.jpg"></p><p>相关地址<br><a href="https://github.com/ptitSeb/gl4es"></a><a href="https://github.com/ptitSeb/gl4es">https://github.com/ptitSeb/gl4es</a><br><a href="https://forum.armbian.com/topic/1420-opengl-on-mali-gpu-bananapi-orangepi-pc-etc/"></a><a href="https://forum.armbian.com/topic/1420-opengl-on-mali-gpu-bananapi-orangepi-pc-etc/">https://forum.armbian.com/topic/1420-opengl-on-mali-gpu-bananapi-orangepi-pc-etc/</a></p>        </div>
        <p itemprop="keywords" class="tags">标签: <a href="https://www.xuefei.net.cn/index.php/tag/PocketChip/">PocketChip</a>, <a href="https://www.xuefei.net.cn/index.php/tag/%E7%A1%AC%E4%BB%B6%E5%8A%A0%E9%80%9F/">硬件加速</a>, <a href="https://www.xuefei.net.cn/index.php/tag/opengl/">opengl</a></p>
    </article>

----

2022/05/12 从博客园迁移至此。
