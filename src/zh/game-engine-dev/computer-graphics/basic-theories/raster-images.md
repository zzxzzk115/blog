---
title: 光栅图像
author: Lazy_V
date: 2023-04-05 15:55:00
category:
  - 游戏引擎开发
tag:
  - 游戏引擎开发
  - 计算机图形学
  - 理论
  - 图像
isOriginal: true
---

## 图像

图像有两种主流类型

- 光栅图像
- 矢量图像

光栅图像存储了一个二维的矩形像素阵列，而矢量图像则是存储了一些点和它们的路径。

举个例子，JPEG 格式的图像是光栅图像，SVG 格式的图像是矢量图像。

::: info
以下是一些光栅图像的主流格式：
- PNG
  
  一种无损压缩格式，且有一系列的开源管理工具。
- JPEG
  
  一种有损压缩格式，适用于自然图像。
- TIFF
  
  二进制图像或无损压缩的8 或 16 位的 RGB。  
:::

在计算机图形学中，我们通常关注于光栅图像，而不是矢量图像。这是由于我们广泛地使用一个名为 **光栅化** 的技术进行渲染。

## 光栅设备

输出:

- 显示器
  - 投射性的: 液晶显示器 (LCD)
  - 放射性的: 发光二极管 (LED) 显示器

- 印刷
  - 二进制: 喷墨打印机
  - [连续色调](https://en.wikipedia.org/wiki/Continuous_tone): 热敏打印机/染料热升华打印机

输入:

- 二维阵列传感器: 数码相机
- 一维阵列传感器: 平板式扫描仪

### 显示器

放射性显示器: 使用一些直接可发光的像素，这些像素可以控制发光量。

投射性显示器: 像素并不发光，而是改变它们允许通过的光量。需要一个光源去照亮它们。

**LED** 显示器是发射型的一个例子。每个像素由一个或多个LED组成，LED是半导体器件，其发光强度取决于通过它们的电流。

![The operation of a light-emitting diode (LED) display.](/images/game-engine-dev/basic-theories/LED1.png)

彩色显示器中的像素被分为三个独立控制的子像素--一个红色、一个绿色和一个蓝色--每个都有自己的LED，使用不同的材料制成，因此它们发出不同颜色的光线。

![The red, green, and blue subpixels within a pixel of a flat-panel display.](/images/game-engine-dev/basic-theories/subpixels.png)

**LCD** 是透射型的一个例子。液晶是一种仪表，其分子结构使其能够旋转通过它的光的偏振，旋转的程度可以通过施加电压来调整。

![The operation of a liquid crystal display (LCD).](/images/game-engine-dev/basic-theories/LCD1.png)

![One pixel of an LCD in the off state (bottom), in which the front polarizer blocks all the light that passes the back polarizer, and the on state (top), in which the liquid crystal cell rotates the polarization of the light so that it can pass through the front polarizer.](/images/game-engine-dev/basic-theories/LCD2.png)

### 印刷设备

打印机是像显示器一样的光栅设备，但许多打印机只能打印二进制图像--颜料在每个网格位置要么沉积，要么不沉积，没有中间量的可能性。

**喷墨打印机** 是一个通过扫描形成光栅图像的设备的例子。它没有像素的物理阵列；分辨率是由水滴的大小和每次扫描后纸张的推进程度决定的。

![The operation of an ink-jet printer](/images/game-engine-dev/basic-theories/ink-jet-printer.png)

**热染料转移** 工艺是连续色调印刷工艺的一个例子，这意味着在每个像素上可以沉积不同数量的染料--它不像喷墨打印机那样是全有或全无的。

![The operation of a thermal dye transfer printer](/images/game-engine-dev/basic-theories/thermal-dye-transfer-printer.png)

### 输入设备

**数码相机** 是二维阵列输入设备的一个例子。相机中的图像传感器是一个具有感光像素网格的半导体装置。

![The operation of a digital camera.](/images/game-engine-dev/basic-theories/digital-camera.png)

- CCD (charge-coupled devices 电荷耦合器件)
- CMOS (complementary metal-oxide-semiconductor 互补性氧化金属半导体)

与彩色显示器使用红、绿、蓝子像素的方式大致相同，大多数彩色相机的工作方式是使用彩色过滤器阵列或马赛克，让每个像素只看到红、绿或蓝光，让图像处理软件在一个被称为去马赛克的过程中填补缺失的数值。

![Most color digital cameras use a color-filter array. Each pixel measures either red, green or blue light.](/images/game-engine-dev/basic-theories/color-filter-array.png)

**平板扫描仪** 也测量每个像素网格的红、绿、蓝值，但像热敏染料转移打印机一样，它使用一维阵列，扫过被扫描的页面，每秒钟进行许多测量。

![The operation of a flatbed scanner.](/images/game-engine-dev/basic-theories/flatbed-scanner.png)
