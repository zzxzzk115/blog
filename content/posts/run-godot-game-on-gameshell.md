---
title: 在GameShell上运行Godot游戏
date: 2021-09-20T12:43:02
tags: [Godot, GameShell]
categories: [Devices]
toc: true
---

> GameShell是一款开源复古掌机，运行Arm Linux操作系统，软硬件均开源，是极客、游戏开发者以及手办爱好者(确实算手办，草)的绝佳玩物。
>
> ![](http://img.zhangkexuan.cn/markdown_20210920125310.png)
>
> Godot是一款开源跨平台游戏引擎，目前发展迅速，原来仅支持GDScript，后来支持VisualScript(可视化逻辑节点编辑器)，现已经支持使用GDNative来使用C++编写库，也开始慢慢支持C#(BETA测试)。
>
> ![](http://img.zhangkexuan.cn/markdown_20210920125347.png)
>
> 那么，Godot制作的游戏，可以导出项目，在Armv7架构的GameShell上运行吗？
>
> 答案是：Godot, YYYYYYYEEEEEEEESSSSS!

接下来我将为大家展示在GameShell上运行Godot游戏的具体过程。

<!--more-->

# 具体过程

## 前期准备

首先准备好软件和硬件，确定版本号和硬件性能是OK的。

建议使用的Godot最低版本：3.2.3。本文采用的Godot版本：3.3.3。

GameShell的需求：

- 1G RAM版本，而非512M RAM版本

- 运行0.5版本镜像的操作系统(建议使用官方原版，比较稳定，DEOT v2本人不建议使用)

## 下载导出模板

已经有外国老哥，在GameShell上安装Godot，并且通过Scons生成了Godot的导出模板，我们这里就直接偷懒，使用他做好的导出模板，[repo link](https://github.com/samdze/godot-gameshell)：

![](http://img.zhangkexuan.cn/markdown_20210920131020.png)

如果你使用Godot 3.2.3及以上，则下载3.2.3版本的导出模板，[点击下载](https://github.com/samdze/godot-gameshell/releases/download/3.2.3-stable/godot-3.2.3-gameshell-templates.zip)

如果你使用Godot 3.3及以上，则下载3.3版本的导出模板，[点击下载](https://github.com/samdze/godot-gameshell/releases/download/3.3-stable/godot-3.3-single-board-gameshell-templates.zip)

## 打开游戏项目

这里，我以官方2D Platformer Demo为例子。

![](http://img.zhangkexuan.cn/markdown_20210920132154.png)

导入官方Demo以后，主界面如下：

![](http://img.zhangkexuan.cn/markdown_20210920132416.png)

## 添加GameShell导出模板

点击 项目->导出：

![](http://img.zhangkexuan.cn/markdown_20210920132825.png)

点击添加：

![](http://img.zhangkexuan.cn/markdown_20210920132857.png)

点击Linux/X11：

![](http://img.zhangkexuan.cn/markdown_20210920132921.png)

进行如下设置，必须注意的是，取消勾选64 Bits：

![](http://img.zhangkexuan.cn/markdown_20210920133149.png)

其中，Custom Template->Debug选择之前下载的godot.x11.debug.32文件：

![](http://img.zhangkexuan.cn/markdown_20210920133252.png)

Custom Template->Release则同理选择godot.x11.opt.32文件。

点击特性，在自定义中输入GameShell，这样，我们在代码逻辑中可以判断是否是GameShell平台，方便我们处理一些GameShell特定的逻辑：

![](http://img.zhangkexuan.cn/markdown_20210920133421.png)

## 设置Godot游戏设置参数

为了导出适用于GameShell运行的项目，我们首先打开项目设置：

![](http://img.zhangkexuan.cn/markdown_20210920132434.png)

### 设置屏幕显示参数

GameShell目前屏幕的分辨率是320\*240。

所以我们需要修改Godot显示设置，我们在为GameShell开发游戏的时候，也要注意控制分辨率在320\*240。

点击Display->Window：

![](http://img.zhangkexuan.cn/markdown_20210920132658.png)

选择Width，点击覆盖，选择GameShell：

![](http://img.zhangkexuan.cn/markdown_20210920133718.png)

然后会新增一个专门为GameShell设置的配置栏：

![](http://img.zhangkexuan.cn/markdown_20210920133826.png)

将 Width.GameShell 从800改为320。

Height同理覆盖修改为240。

更改完后如下：

![](http://img.zhangkexuan.cn/markdown_20210920134021.png)

如果想在Godot编辑器界面测试时测试，还需要设置Test Width和Test Height为320和240(直接设置，并非覆盖)：

![](http://img.zhangkexuan.cn/markdown_20210920145620.png)

此时点击播放按钮，会发现屏幕显示有点奇怪，有黑边：

![](http://img.zhangkexuan.cn/markdown_20210920145712.png)

这是因为默认的屏幕拉伸比例模式为 keep_height:

![](http://img.zhangkexuan.cn/markdown_20210920145917.png)

我们需要为GameShell将Aspect覆盖为keep_width，然后因为老哥提供的模板，禁用了3D，所以他的模板仅支持2D游戏，我们的Mode要覆盖为2d：

![](http://img.zhangkexuan.cn/markdown_20210920151154.png)

运行效果：

![](http://img.zhangkexuan.cn/markdown_20210920150028.png)

可以看到，显示效果非常好！

最后，为了让窗口一直处于最上层，覆盖勾选Always On Top选项：

![](http://img.zhangkexuan.cn/markdown_20210920150613.png)

### 设置渲染参数 

GameShell仅支持GLES2，所以我们需要修改游戏的渲染参数。

点击 Rendering->Quality，覆盖以下内容：

![](http://img.zhangkexuan.cn/markdown_20210921142035.png)

一般来说是不需要采样的，所以Framebuffer Allocation覆盖为2D Without Sampling。

 ## 设置按键

游戏必须写一个按键退出的逻辑，否则只能SSH连接GameShell然后ps -ef | grep xxx，然后kill当前游戏进程，非常麻烦。

GameShell的退出按键是Menu键，映射的是PC中的Escape键，我们在写游戏逻辑的时候，注意写按下ESC退出或者退到主菜单，然后UI支持方向键和回车确认即可。

这里代码部分我就不多提。注意利用之前的GameShell特性，可以特殊处理一些GameShell特定的逻辑。

2D Platformer Demo默认支持ESC显示主菜单，主菜单UI支持方向键导航，也支持回车确认，所以不需要做额外的按键退出逻辑。

## 导出

点击 项目->导出：

![](http://img.zhangkexuan.cn/markdown_20210921152501.png)

选择导出路径：

![](http://img.zhangkexuan.cn/markdown_20210921152551.png)

创建文件夹 GameShellExport:

![](http://img.zhangkexuan.cn/markdown_20210921152622.png)

![](http://img.zhangkexuan.cn/markdown_20210921152802.png)

然后文件名就叫gameshell_demo吧，点 保存：

![](http://img.zhangkexuan.cn/markdown_20210921152843.png)

点 全部导出：

![](http://img.zhangkexuan.cn/markdown_20210921152901.png)

建议选择 发布(Release)，除非你需要调试，则选择调试(Debug)：

![](http://img.zhangkexuan.cn/markdown_20210921153008.png)

最后导出的文件会在GameShellExport文件夹中，是一个可执行文件+一个PCK资源文件：

![](http://img.zhangkexuan.cn/markdown_20210921153104.png)

## 上传至GameShell

这里我使用MobaXterm来进行SSH和SFTP连接的建立。建立过程懂的都懂，不懂请百度。

### 建立连接

先建立连接：

![](http://img.zhangkexuan.cn/markdown_20210921153818.png)

### 创建文件夹

然后再左侧文件系统中，进入games文件夹，新建一个Godot文件夹：

![](http://img.zhangkexuan.cn/markdown_20210921154002.png)

再在新建的Godot文件夹中新建一个2d_platformer_demo文件夹并进去：

![](http://img.zhangkexuan.cn/markdown_20210921154243.png)

### 导入游戏文件并给予执行权限

把我们导出的两个文件拖进去：

![](http://img.zhangkexuan.cn/markdown_20210921154316.png)

右侧Shell界面，cd进去，给这两个文件执行权限：

![](http://img.zhangkexuan.cn/markdown_20210921154611.png)

```bash
cd games/Godot/2d_platformer_demo/

sudo chmod +x gameshell_demo.* 
```

### 使用Bean文件管理器测试运行效果

WDNMD，教程做到这里，我发现我GameShell的电池坏了，充不进电，开不了机，我去淘宝又买了个新的大容量电池，具体演示效果下次补！玩肯定是能玩的，不然我做教程干嘛，是吧。

这里趁着开机的一丝电流来拍一些照片证明一下效果：

<img src="http://img.zhangkexuan.cn/markdown_20210921161258.png" style="zoom:50%;" />

<img src="http://img.zhangkexuan.cn/markdown_20210921161408.png" style="zoom:50%;" />

<img src="http://img.zhangkexuan.cn/markdown_20210921161509.png" style="zoom:50%;" />

<img src="http://img.zhangkexuan.cn/markdown_20210921161539.png" style="zoom:50%;" />

<img src="http://img.zhangkexuan.cn/markdown_20210921161603.png" style="zoom: 50%;" />

### 制作Menu启动项

待补充.........................................................................

# 稍微硬核一点的内容：编译导出模板

老哥能自己编译得到GameShell的导出模板，我们也可以自己编译得到，而且不局限于2D，不局限于GameShell，什么树莓派、S905盒子、香橙派、Devterm、PocketC.H.I.P(理论上可以)应该都是可以编译得到导出模板的。

待补充.........................................................................

# 总结

Godot没有Unity那么"重"，对于嵌入式设备的支持非常好，如果希望给树莓派、GameShell、Devterm这种ARM Linux设备编写游戏，Godot是绝佳的选择。它是少有的图形化游戏引擎，同时还开源，跨平台，功能多，社区氛围好，支持ARM设备，真香！

如果你不习惯纯代码游戏编程(比如使用SDL2，Love2D，Pygame，MonoGame，FNA，Raylib这些)，而习惯于带有图形化编辑器界面的游戏引擎，同时又想为嵌入式设备开发游戏，那么，无脑选择Godot吧！你甚至可以不会编码，直接使用Godot的VisualScript，通过节点编辑来完成游戏逻辑！













