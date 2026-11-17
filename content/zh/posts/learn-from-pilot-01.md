---
title: '从 Pilot 引擎学知识(1)-在 Windows 上跑起来'
date: 2022-04-05T15:29:43
tags: [PilotEngine, GAMES104]
categories: [游戏引擎]
toc: true
---

![在 Windows 上成功编译并运行 Pilot](/img/markdown_20220405155248.png)

Pilot 引擎是 GAMES104 课程组共同开发的一款迷你游戏引擎，麻雀虽小五脏俱全。它开源，我们可以在 GitHub 上可以获取到它的源代码。接下来简单讲讲如何在 Windows 上跑通并断点调试 Pilot 引擎。

<!--more-->

# 在 Windows 上跑起来

让 Pilot 在 Windows 中成功编译并运行，是 GAMES104 的第一次作业，也是我们从 Pilot 学知识的开始。

## 准备好工具

需要准备的工具有: 

- Git 2.1 及以上版本，直接安装，生成公钥，GitHub 添加公钥即可。
- CMake 3.19 及以上版本，直接安装，注意添加到 PATH 即可。
- Visual Studio 2019 及以上版本，安装时勾选桌面 C++ 相关环境即可。
- Vulkan SDK for Windows [点我下载](https://sdk.lunarg.com/sdk/download/latest/windows/vulkan-sdk.exe) ，直接安装即可。

## 获取源代码

访问 https://github.com/BoomingTech/Pilot

可以 clone 仓库，也可以直接作为 ZIP 文件下载，当然也可以先 fork，再 clone。

目前建议 clone 仓库，并且有更新后拉取更新。

## 编译得到 Release 版本

如果只需要得到 Release 版本，双击根目录下的 `build_windows.bat` 即可

![](/img/markdown_20220405161120.png)

然后会执行编译指令，当指令执行完后，根目录会产生两个新文件夹:

- bin
- build

此时可以直接运行 `bin/PilotEditor.exe` 运行 Release 版本的 Pilot 编辑器，此时已经可以截图交作业了 hhh。

## 编译并调试 Debug 版本

我们需要从 Pilot 学习知识，那么断点调试是必不可少的。

在刚刚生成的 build 文件夹中，已经生成了我们需要的解决方案文件: `Pilot.sln`，双击会通过 Visual Studio 打开。

打开后，解决方案目录看起来是这样的：

![](/img/markdown_20220405161614.png)

目前默认启动项目是 ALL_BUILD，我们需要将默认启动项目改为 `PilotEditor`。

右键 PilotEditor 项目->设为启动项目 即可。

![](/img/markdown_20220405161817.png)

项目默认的模式已经是 Debug 了，我们直接点击绿色三角形即可开始断点调试。

例如我们在 `PilotEditor::run` 函数中设置一个断点:

![](/img/markdown_20220405162317.png)

接下来就可以一步一步看到 runtime 内部如何 Tick 各个模块了：

![](/img/markdown_20220405163057.png)

