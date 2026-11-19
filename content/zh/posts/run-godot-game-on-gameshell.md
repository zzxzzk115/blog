---
title: 在 GameShell 上运行 Godot 游戏
date: 2021-09-20T12:43:02
tags: [GameShell, ClockworkPi, Godot]
categories: [复古掌机]
toc: true
---

> GameShell 是一款开源复古掌机，运行 Arm Linux 操作系统，软硬件均开源，是极客、游戏开发者以及手办爱好者(确实算手办，草) 的绝佳玩物。
>
> ![](/img/markdown_20210920125310.webp)
>
> Godot 是一款开源跨平台游戏引擎，目前发展迅速，原来仅支持 GDScript，后来支持 VisualScript(可视化逻辑节点编辑器)，现已经支持使用 GDNative 来使用 C++ 编写库，也开始慢慢支持 C#(BETA 测试)。
>
> ![](/img/markdown_20210920125347.png)
>
> 那么，Godot 制作的游戏，可以导出项目，在 Armv7 架构的 GameShell 上运行吗？
>
> 答案是：Godot, YYYYYYYEEEEEEEESSSSS!

接下来我将为大家展示在 GameShell 上运行 Godot 游戏的具体过程。

<!--more-->

# 具体过程

## 前期准备

首先准备好软件和硬件，确定版本号和硬件性能是 OK 的。

建议使用的 Godot 最低版本：3.2.3。本文采用的 Godot 版本：3.3.3。

GameShell 的需求：

- 1G RAM 版本，而非 512M RAM 版本

- 运行 0.5 版本镜像的操作系统(建议使用官方原版，比较稳定，DEOT v2 本人不建议使用)

## 下载导出模板

已经有外国老哥，在 GameShell 上安装 Godot，并且通过 Scons 生成了 Godot 的导出模板，我们这里就直接偷懒，使用他做好的导出模板，[repo link](https://github.com/samdze/godot-gameshell)：

![](/img/markdown_20210920131020.png)

如果你使用 Godot 3.2.3 及以上，则下载 3.2.3 版本的导出模板，[点击下载](https://github.com/samdze/godot-gameshell/releases/download/3.2.3-stable/godot-3.2.3-gameshell-templates.zip)

如果你使用 Godot 3.3 及以上，则下载 3.3 版本的导出模板，[点击下载](https://github.com/samdze/godot-gameshell/releases/download/3.3-stable/godot-3.3-single-board-gameshell-templates.zip)

## 打开游戏项目

这里，我以官方 2D Platformer Demo 为例子。

![](/img/markdown_20210920132154.png)

导入官方 Demo 以后，主界面如下：

![](/img/markdown_20210920132416.png)

## 添加 GameShell 导出模板

点击 项目->导出：

![](/img/markdown_20210920132825.png)

点击添加：

![](/img/markdown_20210920132857.png)

点击 Linux/X11：

![](/img/markdown_20210920132921.png)

进行如下设置，必须注意的是，取消勾选 64 Bits：

![](/img/markdown_20210920133149.png)

其中，Custom Template->Debug 选择之前下载的 godot.x11.debug.32 文件：

![](/img/markdown_20210920133252.png)

Custom Template->Release 则同理选择 godot.x11.opt.32 文件。

点击特性，在自定义中输入 GameShell，这样，我们在代码逻辑中可以判断是否是 GameShell 平台，方便我们处理一些 GameShell 特定的逻辑：

![](/img/markdown_20210920133421.png)

## 设置 Godot 游戏设置参数

为了导出适用于 GameShell 运行的项目，我们首先打开项目设置：

![](/img/markdown_20210920132434.png)

### 设置屏幕显示参数

GameShell 目前屏幕的分辨率是 320\*240。

所以我们需要修改 Godot 显示设置，我们在为 GameShell 开发游戏的时候，也要注意控制分辨率在 320\*240。

点击 Display->Window：

![](/img/markdown_20210920132658.png)

选择 Width，点击覆盖，选择 GameShell：

![](/img/markdown_20210920133718.png)

然后会新增一个专门为 GameShell 设置的配置栏：

![](/img/markdown_20210920133826.png)

将 Width.GameShell 从 800 改为 320。

Height 同理覆盖修改为 240。

更改完后如下：

![](/img/markdown_20210920134021.png)

如果想在 Godot 编辑器界面测试时测试，还需要设置 Test Width 和 Test Height 为 320 和 240(直接设置，并非覆盖)：

![](/img/markdown_20210920145620.png)

此时点击播放按钮，会发现屏幕显示有点奇怪，有黑边：

![](/img/markdown_20210920145712.png)

这是因为默认的屏幕拉伸比例模式为 keep_height:

![](/img/markdown_20210920145917.png)

我们需要为 GameShell 将 Aspect 覆盖为 keep_width，然后因为老哥提供的模板，禁用了 3D，所以他的模板仅支持 2D 游戏，我们的 Mode 要覆盖为 2d：

![](/img/markdown_20210920151154.png)

运行效果：

![](/img/markdown_20210920150028.png)

可以看到，显示效果非常好！

最后，为了让窗口一直处于最上层，覆盖勾选 Always On Top 选项：

![](/img/markdown_20210920150613.png)

### 设置渲染参数 

GameShell 仅支持 GLES2，所以我们需要修改游戏的渲染参数。

点击 Rendering->Quality，覆盖以下内容：

![](/img/markdown_20210921142035.png)

一般来说是不需要采样的，所以 Framebuffer Allocation 覆盖为 2D Without Sampling。

 ## 设置按键

游戏必须写一个按键退出的逻辑，否则只能 SSH 连接 GameShell 然后 ps -ef | grep xxx，然后 kill 当前游戏进程，非常麻烦。

GameShell 的退出按键是 Menu 键，映射的是 PC 中的 Escape 键，我们在写游戏逻辑的时候，注意写按下 ESC 退出或者退到主菜单，然后 UI 支持方向键和回车确认即可。

这里代码部分我就不多提。注意利用之前的 GameShell 特性，可以特殊处理一些 GameShell 特定的逻辑。

2D Platformer Demo 默认支持 ESC 显示主菜单，主菜单 UI 支持方向键导航，也支持回车确认，所以不需要做额外的按键退出逻辑。

## 导出

点击 项目->导出：

![](/img/markdown_20210921152501.png)

选择导出路径：

![](/img/markdown_20210921152551.png)

创建文件夹 GameShellExport:

![](/img/markdown_20210921152622.png)

![](/img/markdown_20210921152802.png)

然后文件名就叫 gameshell_demo 吧，点 保存：

![](/img/markdown_20210921152843.png)

点 全部导出：

![](/img/markdown_20210921152901.png)

建议选择 发布(Release)，除非你需要调试，则选择调试(Debug)：

![](/img/markdown_20210921153008.png)

最后导出的文件会在 GameShellExport 文件夹中，是一个可执行文件+一个 PCK 资源文件：

![](/img/markdown_20210921153104.png)

## 上传至 GameShell

这里我使用 MobaXterm 来进行 SSH 和 SFTP 连接的建立。建立过程懂的都懂，不懂请百度。

### 建立连接

先建立连接：

![](/img/markdown_20210921153818.png)

### 创建文件夹

然后再左侧文件系统中，进入 games 文件夹，新建一个 Godot 文件夹：

![](/img/markdown_20210921154002.png)

再在新建的 Godot 文件夹中新建一个 2d_platformer_demo 文件夹并进去：

![](/img/markdown_20210921154243.png)

### 导入游戏文件并给予执行权限

把我们导出的两个文件拖进去：

![](/img/markdown_20210921154316.png)

右侧 Shell 界面，cd 进去，给这两个文件执行权限：

![](/img/markdown_20210921154611.png)

```bash
cd games/Godot/2d_platformer_demo/

sudo chmod +x gameshell_demo.* 
```

### 使用 Bean 文件管理器测试运行效果

WDNMD，教程做到这里，我发现我 GameShell 的电池坏了，充不进电，开不了机，我去淘宝又买了个新的大容量电池，具体演示效果下次补！玩肯定是能玩的，不然我做教程干嘛，是吧。

这里趁着开机的一丝电流来拍一些照片证明一下效果：

![](/img/markdown_20210921161258.webp)

![](/img/markdown_20210921161408.webp)

![](/img/markdown_20210921161509.webp)

![](/img/markdown_20210921161539.webp)

![](/img/markdown_20210921161603.webp)

### 制作 Menu 启动项

待补充.........................................................................

# 稍微硬核一点的内容：编译导出模板

老哥能自己编译得到 GameShell 的导出模板，我们也可以自己编译得到，而且不局限于 2D，不局限于 GameShell，什么树莓派、S905 盒子、香橙派、Devterm、PocketC.H.I.P(理论上可以) 应该都是可以编译得到导出模板的。

待补充.........................................................................

# 总结

Godot 没有 Unity 那么"重"，对于嵌入式设备的支持非常好，如果希望给树莓派、GameShell、Devterm 这种 ARM Linux 设备编写游戏，Godot 是绝佳的选择。它是少有的图形化游戏引擎，同时还开源，跨平台，功能多，社区氛围好，支持 ARM 设备，真香！

如果你不习惯纯代码游戏编程(比如使用 SDL2，Love2D，Pygame，MonoGame，FNA，Raylib 这些)，而习惯于带有图形化编辑器界面的游戏引擎，同时又想为嵌入式设备开发游戏，那么，无脑选择 Godot 吧！你甚至可以不会编码，直接使用 Godot 的 VisualScript，通过节点编辑来完成游戏逻辑！













