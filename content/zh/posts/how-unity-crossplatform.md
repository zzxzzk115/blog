---
title: Unity 为什么能做到跨平台
date: 2020-11-17T14:49:51
categories: [游戏引擎]
tags: [Unity, 跨平台, Mono, CIL, DotNET, CLR]
toc: true
---

Unity 是如何做到跨平台的？Mono 和.NET Framework 之间到底是什么关系？IL 是啥？CIL 和 CLI 这俩长得很像的又是啥？

本文我来讲解一下这些令许多人都好奇的问题。

<!--more-->

# 我对 Unity 的回忆

Unity 原名 Unity3D，最开始是一款跨平台的 3D 游戏引擎。后来由于业务范围不局限于 3D，也不局限于游戏，故改名为 Unity。

我最早接触 Unity 的时候是 2013 年，那一年，我萌发了做游戏开发的想法。故事我就不多说了，多说说和 Unity 有关的描述。那个时候的 Unity 版本是 4.x，大多数人还使用 MonoDevelopment 作为脚本 IDE。我当时对 Mono 的印象就是：写 C# 脚本用的，好像可以做到跨平台，但我并没有研究 Mono 是如何做到跨平台的。我只记得，当时可以导出到 H5、Playstation3、Android、Linux、Windows 等平台，这在当时是非常超前的。当时能做到横跨多个平台的引擎真的不多。我当时搜索了很多有关游戏引擎的资料，都说 Unity 是非常具有潜力的跨平台 3D 游戏引擎。当时手游市场基本上是 Unity 和 Cocos2D 两家游戏引擎的江山，但是 Cocos 的跨平台能力实际上不如 Unity，Cocos2D-X 也并不是可视化的，对于新手的我而言相对硬核，所以我当时选择了 Unity 作为以后学习的对象。（虽然也没学到太多东西...）

可以说，当时正是有了 Mono 这个伟大的项目，Unity 才得以做到跨平台。其实当时同期使用 Mono 完成跨平台的游戏框架还有 MonoGame、XNA 等，不过它们的工作流都是纯代码编辑和调试，对于当时的我而言太过硬核，我也没考虑和研究。Mono 是当时跨平台的关键。

> XNA 已经被微软遗弃，感兴趣的可以看看 FNA，它是 XNA 4.0 的开源实现。

# 回顾跨平台的历程

## 多个平台的烦恼

不同的平台、不同的架构越来越多。在 Windows 编写的程序，可能无法在 Linux 运行，可能还需要做平台移植。简单说就是要“交叉编译”，这是一件很麻烦的事情。虽然 C/C++ 项目有 make/cmake 可以跨平台编译，但其他语言的项目做到跨平台十分困难。

## 平台和指令集一样就好了

如果所有的平台和对应的指令集都是一样的话，好像就不用交叉编译了。那样就可以做到“一次编译，处处执行”。能不能模拟出这样一个虚拟的平台和对应的指令集呢？

## CLI 的诞生

为了虚拟一个通用的指令集并编译执行，IL(Intermediate Language， 中间语言) 和 JIT(Just In Time，即时) 编译器的概念诞生了。IL 是一种中间语言，它基于堆栈，具有面向对象的特性。JIT 是一种即时编译器，在运行时编译。高级语言被各自编译器编译成 IL，IL 经过 JIT 编译后，得到 Native Code（本机代码），从而可以运行在对应原生平台。

为了让多种高级语言编译出统一的 IL，CLI(Common Language Infrastructure，通用语言基础结构) 诞生了。CLI 是一种通用语言规范，只要高级语言遵守 CLI 的规范，编译出的 IL 就是完全一致的。

## 微软对 CLI 的实现: .NET Framework

微软的.NET Framework 就是对 CLI 的一个实现。.NET Framework 包括.NET Framework 类库和 CLR(Common Language Runtime，公共语言运行时) 还有一些编译器等等。CLR 可以看做是一个虚拟机，运行在 CLR 中的语言叫做 CIL(Common Intermediate Language，通用中间语言，又称 MSIL，微软中间语言)。

.NET Framework 当时并不开源，也只能在 Windows 上运行。

## Mono 的诞生

由于.NET Framework 不开源，不跨平台，Mono 应运而生。

Mono 由 Xamarin 公司所赞助，是一个开源项目。它和.NET Framework 一样也是 CLI 的一个实现，也符合 C# 的 ECMA 标准，但与微软的.NET 框架不同的是，Mono 具备跨平台能力。

Mono 不仅可以运行在 Windows 上，还可以运行在 Mac OS、Linux 和一些游戏主机/掌机平台上。

相比于.NET Framework 运行时库，Mono 有自己的 Mono VM 作为运行时库。

### Mono 的架构

1. 编译器：Mono 的 C# 编译器是：MCS。MCS 可以把 C# 源码编译成托管模块(EXE/DLL)。
2. 运行时：JIT、AOT、FULL-AOT、GC、类库加载器等。
3. 基础类库(BCL, Basic Class Library)
4. Mono 类库：提供了超出微软.NET 的一些类，提供了许多额外功能，主要用于构建其他操作系统上的应用。

> JIT（Just-in-time），程序运行时将 IL（中间语言）转为对应平台原生码，并将原生码映射到虚拟内存执行。
>
> AOT（Ahead-of-time）,程序运行之前将.exe 或.dll 文件中部分转译为目标平台原生码存储。
>
> FULL-AOT（Full-Ahead-of-time）,程序运行之前，所有代码完全编译为目标平台原生码。
>
> GC 使用了贝姆垃圾回收方式、分代回收，和 CLR 不一样。

### Mono 和.NET Framework 在 Unity 中的关系

Mono 和.NET Framework 使用的是同一套标准，但 Mono 提供的功能要少一些。

一般情况下.NET Framework 编译出的 dll 可作为插件给 Unity 使用。但需要注意 Mono 所用的基础类库和.NET Framework 提供的基础类库不同，它们在不同的程序集中。

### Mono 跨平台流程

Mono 的 C# 编译器(MCS) 将 C# 代码编译成 IL（中间语言、符合 ECMA CLI 规范），其次 Mono 运行时提供 JIT 编译器或 AOT 编译器在运行时将 IL 编译成对应平台的原生码（Native Code），最后在不同平台执行各自编译出的原生码，做到跨平台。

![full_build_mono](/img/markdown_20201117155619.png)

## Unity 为什么跨平台

讲了这么多，大家也都明白了：Mono 能做到跨平台。而 Unity 利用 Mono 完成编译工作，当然可以实现跨平台。但是 Mono 慢慢也出现了一些问题，Unity 会想出什么对策呢？

## 后来的 Unity 与 IL2CPP

后来，iOS 禁止了 JIT 编译，这直接导致 Mono 无法导出 iOS 应用。Mono 又出现效率问题以及授权问题。

Unity 逐渐意识到，导致必须要想一个新的对策。新的对策就是 IL2CPP。

IL2CPP 顾名思义，就是将 IL 中间语言转换成 CPP 文件。转换成的 CPP 文件再通过 C++ 编译器和 libil2cpp 库编译成原生二进制可执行文件。

![il2cpp](/img/markdown_20201117160610.png)

首先通过 Mono 的 C# 编译器将高级语言编译成 IL，然后使用 IL2CPP.exe 将 IL 编译成 C++ 代码，然后再由各个平台的 C++ 编译器直接编译成能执行的原生可执行汇编代码，执行于 IL2CPP VM。

![IL2CPP_workflow](/img/markdown_20201117160737.png)

![IL2CPP_workflow2](/img/markdown_20201117160805.png)

最后一步的 IL2CPP VM 是一个内存管理器，它负责提供诸如 GC 管理，线程创建这类的服务性工作。但是由于去除了 IL 加载和动态解析的工作，使得 IL2CPP VM 可以做的很小，并且使得游戏载入时间缩短。

对于不同平台来说，IOS 平台之外的是使用了 JIT，IOS 平台是编译时把 IL 代码转为目标码，使用的是 FULL-AOT。总的来说 Unity 跨平台目前依靠 Mono。iOS 平台，由于不允许运行时生成 Native Code，因为 IOS 被禁止了 JIT，因此上面方式采用 Full-AOT 的模式，利用 IL2CPP 将所有 IL 先转成 C++ Code，而 C++ 是可以跨平台编译执行的，因此有效的解决的 IOS 问题。

Unity 是可以切换编译方式的(Mono 还是 IL2CPP)。

## 今天的 Unity 手游的编译构建过程

目前的 Unity 手游大多数的流程为：

C# 源码 -> Mono C# 编译器 -> IL -> IL2CPP -> C++ 代码 -> LLVM -> native code

> LLVM 是构架编译器(compiler) 的框架系统，以 C++ 编写而成，用于优化以任意程序语言编写的程序的编译时间(compile-time)、链接时间(link-time)、运行时间(run-time) 以及空闲时间(idle-time)，对开发者保持开放，并兼容已有脚本。简单说就是用于针对安卓和 iOS 进行优化。

# 展望未来

技术总是在不断革新的，未来会不会有一个新的概念的出现，一个新的工具的出现，让跨平台更加简单、高效呢？让我们拭目以待。相信在我们学习的过程中，总是会有新的技术让你觉得眼前一亮。

# 感谢

感谢段哥帮我搜集的资料，非常完整！