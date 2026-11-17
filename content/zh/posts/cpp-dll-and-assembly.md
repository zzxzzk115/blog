---
title: 动态链接库 DLL 和.NET Framework 程序集的区别与联系
date: 2020-11-21T21:31:18
categories: [编程语言]
tags: [DLL, CLR]
toc: true
---

在认识.NET Framework 之前，我们就见过各种 DLL 文件。它们可能是通过 C++ 编译的。

认识.NET Framework 以后，我们知道程序集可以导出成一个 DLL 文件。

同样是以.DLL 为后缀的文件，动态链接库(DLL) 和 .NET Framework 程序集有什么区别和联系吗？

<!--more-->

# 动态链接库(DLL)

## DLL 的概念

动态链接库(Dynamic Link Library, DLL) 是一个包含可由多个程序同时使用的代码和数据的库。 例如，在 Windows 操作系统中，Comdlg32 DLL 执行与常见的对话框相关的功能。 因此，每个程序都可以使用此 DLL 中包含的功能来实现 **打开** 的对话框。 这有助于促进代码重用和高效的内存使用。

通过使用 DLL，可以将程序模块化到单独的组件中。 例如，会计程序可能按模块销售。 如果安装了模块，每个模块都可以在运行时加载到主程序中。 由于模块是独立的，因此程序的加载时间更快，并且仅在请求该功能时才会加载模块。

此外，更新更易于应用于每个模块，而不会影响程序的其他部分。 例如，您可能有一个工资计划，税率每年都会发生变化。 当这些更改被隔离到 DLL 时，您可以应用更新，而无需再次生成或安装整个程序。

## DLL 的优势

- 使用较少的资源

  当多个程序使用相同的函数库时，DLL 可以减少在磁盘上和物理内存中加载的代码的重复。 这样不仅可以大大影响在前台运行的程序，还能影响 Windows 操作系统上运行的其他程序的性能。

- 促进模块化体系结构

  DLL 可帮助促进模块化程序的开发。 这可帮助您开发需要多个语言版本的大型程序或需要模块化体系结构的程序。 模块化程序的一个示例是一个计帐程序，其中包含可在运行时动态加载的多个模块。

- 简化部署和安装

  当 DLL 中的函数需要更新或修补程序时，DLL 的部署和安装不需要重新链接 DLL 中的程序。 此外，如果多个程序使用同一个 DLL，则多个程序都将从更新或修补程序中受益。 如果使用的是定期更新或修复的第三方 DLL，则可能会更频繁地发生此问题。

## DLL 的依赖问题和 DLL hell(DLL 冲突)

当某个程序或 DLL 在另一个 DLL 中使用 DLL 函数时，将创建一个依赖项。 因此，该程序不再是独立的，如果依赖项断开，该程序可能会遇到问题。 例如，如果发生下列操作之一，则该程序可能无法运行：

- 依赖 DLL 升级到新版本。
- 固定的 DLL 是固定的。
- 早期版本会覆盖依赖 DLL。
- 将从计算机中删除依赖 DLL。

这些操作称为 DLL 冲突。 如果没有强制实现向后兼容性，该程序可能无法成功运行。

# 程序集(Assembly)

## 程序集的概念

随着 .NET 和 .NET Framework 的推出，使用程序集消除了与 Dll 相关联的大多数问题。 程序集是在 .NET 公共语言运行时的控制下运行的逻辑功能单元 (CLR) 。 程序集实际作为 .dll 文件或 .exe 文件存在。 但是，内部程序集与 Microsoft Win32 DLL 不同。

程序集文件包含程序集清单、类型元数据、Microsoft 中间语言 (MSIL) 代码和其他资源。 程序集清单包含程序集元数据，该元数据提供程序集自描述所需的所有信息。 程序集清单中包含以下信息：

- 程序集名称
- 版本信息
- 区域性信息
- 强名称信息
- 文件的程序集列表
- 类型引用信息
- 引用的和依赖的程序集信息

无法直接执行程序集中包含的 MSIL 代码。 相反，MSIL 代码执行通过 CLR 进行管理。 默认情况下，当您创建程序集时，程序集是应用程序的专用程序集。 若要创建共享程序集，需要为程序集分配一个强名称，然后将该程序集发布到全局程序集缓存中。

## 程序集的功能

- 自我描述

  创建程序集时，CLR 运行程序集所需的所有信息都包含在程序集清单中。 程序集清单包含依赖程序集的列表。 因此，CLR 可以维护在应用程序中使用的一组一致的程序集。 在 Win32 Dll 中，您无法在使用共享 Dll 时保持应用程序中使用的一组 Dll 之间的一致性。

- 版本控制

  在程序集清单中，版本信息由 CLR 记录和强制实施。 此外，版本策略允许您强制实施特定于版本的用法。 在 Win32 Dll 中，操作系统不能强制实施版本控制。 相反，您必须确保 Dll 是向后兼容的。

- 并行部署

  程序集支持并行部署。 一个应用程序可以使用程序集的一个版本，另一个应用程序可以使用不同版本的程序集。 在 Windows 2000 中启动时，将通过在应用程序文件夹中查找 Dll 来支持并行部署。 此外，Windows 文件保护阻止系统 Dll 被未授权的代理覆盖或替换。

- 自包含和隔离

  使用程序集开发的应用程序可以是独立的，并与计算机上运行的其他应用程序隔离。 此功能可帮助您创建零影响安装。

- 执行

  程序集在程序集清单中提供且由 CLR 控制的安全权限下运行。

- 独立于语言

  可以使用任意一种受支持的 .NET 语言来开发程序集。 例如，您可以在 Microsoft Visual C# 中开发程序集，然后在 Visual Basic .NET 项目中使用程序集。

# DLL 和程序集的区别和联系

从真实的测试中得到答案。

## C++/CLI 生成 DLL


Visual Studio 添加 C++/CLI 功能(使用 Visual Studio Installer，修改，找到 C++ 中的 C++/CLI，打勾，确认) 后，新建 Visual C++ -> CLR -> 类库 ：

![](/img/markdown_20201122000948.png)

在 CLR_DLL.h 中添加 Add 方法:

![add_clr_def](/img/markdown_20201122001432.png)

在 CLR_DLL.cpp 中实现 Add 方法：

![add_clr_impl](/img/markdown_20201122001450.png)

生成解决方案，得到 CLR_DLL.dll:

![log1](/img/markdown_20201122001551.png)

![CLR_DLL.dll](/img/markdown_20201122001636.png)

文件大小 95232 字节。打开设置查看：

![clr_dll_settings](/img/markdown_20201122001751.png)

开启了/CLR 开关。

如果用 ILDasm.exe 打开：

![clr_dll_ildasm](/img/markdown_20201122001918.png)

可以查看清单、元数据表、标头、以及 IL 代码，说明此时的 DLL_Test.dll 是程序集。

- Add 方法:

![add_clr](/img/markdown_20201122002357.png)

- 元数据表：

![metainfo_clr](/img/markdown_20201122002502.png)

- 标头：

![headers](/img/markdown_20201122002630.png)

这说明，开启/CLR 开关生成的 DLL 文件是程序集。

## 非托管 C++ 生成 DLL

新建 Visual C++ -> Windows 桌面 -> 动态链接库(DLL):

![noclr_dll](/img/markdown_20201122002901.png)

在 NOCLR_DLL.cpp 中添加 Add 方法：

![noclr_dll.cpp](/img/markdown_20201122003240.png)

生成解决方案，得到 NOCLR_DLL.dll：

![log2](/img/markdown_20201122003401.png)

![NOCLR_DLL.dll](/img/markdown_20201122003433.png)

文件大小 35328 字节，代码虽然差不多，但目前得到的 DLL 文件比上面 C++/CLI 编译生成的 DLL 文件明显小了几倍。打开设置查看：

![NOCLR_DLL_settings](/img/markdown_20201122003554.png)

没有开启/CLR 开关。

如果用 ILDasm.exe 打开：

![NOCLR_headers](/img/markdown_20201122003828.png)

报错，提示没有有效的 CLR 头。这在我们的预料中。因为非托管 C++ 生成的 DLL 文件根本就不是程序集，没有 CLR 头，没有元数据、IL、资源文件等等。

那么 C# 如何调用 C++/CLI 编译的 DLL 中的方法，如何调用非托管 C++ 编译的 DLL 中的方法呢？

## C# 调用 C++/CLI 编译的 DLL 中的方法

C# 项目中，右键解决方案，添加引用：

![add_ref](/img/markdown_20201122004729.png)

浏览之前生成的 CLR_DLL.dll，点击添加：

![browse_and_add](/img/markdown_20201122004911.png)

然后在 Main 方法中可以调用 CLRDLL.Class1.Add() 方法了：

![call_add_clr](/img/markdown_20201122005130.png)

结果：

![result_clr](/img/markdown_20201122005209.png)

正确调用。

## C# 调用非托管 C++ 编译的 DLL 中的方法

想要调用非托管 C++ 编译的 DLL 中的方法，就需要用到 C# 的 [DllImport] 属性。

首先要用 Depends.exe 查看 Add 方法的入口：

![search_for_Add_EntryPoint](/img/markdown_20201122010356.png)

![EntryPoint_of_Add](/img/markdown_20201122010500.png)

可以得到 Add 方法的 EntryPoint 为：`?Add@@YAHHH@Z`。

把之前生成的 NOCLR_DLL.dll 复制到 C# 项目的 bin/Debug 中：

![copy_to_Debug](/img/markdown_20201122005906.png)

然后在 Main 方法前用 DllImport 导入 DLL：

![import](/img/markdown_20201122010609.png)

运行结果：

![result_noclr](/img/markdown_20201122010638.png)

正确调用。

## 总结

"DLL=程序集"或者"程序集=DLL"的说法肯定是错误的。你只能说后缀是.DLL 的文件有可能是程序集，而且程序集的后缀也可能是.EXE。C++ 编译得到的 DLL 文件不一定是程序集。如果是 C++/CLI，它面向 CLR，开启了/CLR 开关，编译出的就是程序集。如果是非托管 C++，它不面向 CLR，没有开启/CLR 开关，编译出的就是普通 DLL。程序集虽然后缀可以是 DLL，但它还包含了诸如元数据、IL 代码、清单、CLR 头、资源文件等等数据。

C# 对于调用 C++/CLI 导出的 DLL 中的方法和调用非托管 C++ 导出的 DLL 中的方法，采用的方式不一样。

----

上面都是我自身的想法和测试过程，如有不正确、不严谨的地方，欢迎指正！

