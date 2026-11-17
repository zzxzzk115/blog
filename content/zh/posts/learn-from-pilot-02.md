---
title: '从 Pilot 引擎学知识(2)-文件目录结构'
date: 2022-04-05T16:47:40
tags: [PilotEngine, GAMES104]
categories: [游戏引擎]
toc: true
---

![](http://img.zhangkexuan.cn/markdown_20220405172221.png)

接下来分析一下 Pilot 引擎的文件目录结构，并在过程中简单讲讲 Pilot 引擎使用的第三方库及作用。

<!--more-->

# Pilot 文件目录结构

分析源代码之前，首先需要分析项目的目录结构，以及涉及到的第三方库及作用。

没有经过任何编译操作的 Pilot 源码包含两个文件夹和一些文件。

文件夹：

- cmake - 一些 cmake 函数相关内容
- engine - 引擎相关内容

文件：

- .clang-format - 格式化代码风格
- .clang-tidy - 静态检查与修复
- .gitignore - git 忽略设置
- build_linux.sh - 在 Linux 上编译
- build_windows.bat - 在 Windows 上编译
- LICENSE - 许可证
- README.md - 说明

接下来逐一分析。

## cmake 文件夹

cmake 文件夹中主要包含了一些 cmake 编译函数相关的内容:

- GenerateShaderCPPFile.cmake - 用于生成 Shader 对应的 CPP 文件
- ShaderCompile.cmake - 用于遍历并编译每一个 Shader
- tools.cmake - 包含了一些工具函数

## engine 文件夹

engine 文件夹主要包含了第三方库、资产、二进制文件、Shader、源代码以及一些配置文件。

- 3rdparty - 第三方库，包括：
  - [glfw](https://github.com/glfw/glfw) - 开源的跨平台 OpenGL 的应用框架，通常用于窗口管理，还提供了处理手柄、键盘、鼠标输入的功能，类似于 SDL。
  - [glm](https://github.com/g-truc/glm) - 开源的 OpenGL 数学库。
  - [imgui](https://github.com/ocornut/imgui) - Dear IMGUI，非常受欢迎的开源即时 GUI 框架。
  - [json11](https://github.com/dropbox/json11) - Dropbox 的开源 JSON 框架。
  - [spdlog](https://github.com/gabime/spdlog) - 开源的轻量级日志框架。
  - [stb](https://github.com/nothings/stb) - 开源的图像、字体相关处理库。
  - [tinyobjloader](https://github.com/tinyobjloader/tinyobjloader) - 开源的轻量级 OBJ 文件加载器。
  - [vulkanmemoryallocator](https://github.com/GPUOpen-LibrariesAndSDKs/VulkanMemoryAllocator) - 开源的 Vulkan 内存分配器。
  - [VulkanSDK](https://www.lunarg.com/vulkan-sdk/) - Vulkan 的开发包，包括头文件、预编译的静态库等等。
- asset - 资产，运行时相关的资产，包括关卡(场景)、对象、纹理贴图、世界。
  - level - 关卡，类似于 Unity 中的 Scene。
  - object - 对象，包括对象的纹理贴图、模型、组件等等。
  - texture - 纹理贴图，目前包括默认的纹理、天空盒贴图。
  - world - 世界，世界是关卡(level) 的容器。
- bin - 二进制文件。包含各个平台需要的库、程序等，例如目前包含了 Clang 库和 meta_parser。
- shader - 着色器代码
- source - 源码，包括编辑器代码、预编译内容、运行时代码：

  - editor - 编辑器代码
  - precompile - cmake 脚本 + json 参数配置，用于预编译一些内容
  - runtime - 运行时代码
- .gitignore - git 忽略设置
- CMakeLists.txt - CMake 项目相关配置
- PilotEditor.ini - Pilot 编辑器相关配置

以上就是 Pilot 文件目录结构的简单分析，下一次会简单分析 Pilot 是如何利用 CMake 将源代码之间建立联系的，以及更新一些第三方库的专题。



  
