---
title: 回顾 CLR(1)：基础部分
date: 2020-11-16T14:37:09
categories: [编程语言]
tags: [CLR, CSharp]
toc: true
---

什么是 CLR？什么是元数据？什么是 JIT？CLR 是如何工作的？

本篇文章较深入地探索《CLR via C#》前三章。

<!--more-->

# 前言

《CLR via C#》这本书，我已经通读过 2-3 次了，但很多内容我依旧没有深入挖掘和探索。

为什么要读这本书，为什么要多次读这本书？我一开始也不是很清楚。后来我搞明白了。

Unity 之所以能够跨平台，和 Mono 或者 IL2CPP 有关。而 Mono 和.NET Framework 息息相关。Mono 是可跨平台的.NET 平台，.NET Framework 只能服务于 Windows。CLR 是 Mono 或者.NET Framework 中的一部分，它起到非常关键的作用。关于 Unity 跨平台背后的原理，下次再聊。

市面上关于 CLR 的书籍不是很多，而同时关于 C# 和 CLR 的书籍也就只有这本《CLR via C#》。Unity 使用 C# 作为脚本编程语言，脚本编译的工作流程又和 CLR 息息相关，所以我们要读这本 Unity 程序员必看的《CLR via C#》。如果我们学习 Unity 编程，却不了解 CLR 的工作规则，不了解 IL 代码相关的概念，只会写出低效率、低性能、低水准的代码。

我决定从这次开始，不光阅读书籍，还要动手实践，在网上查阅更多资料，对比一些已有的概念，来加深对 CLR 的认识。所以，这篇博文不光会有理论部分，还会有实践部分。

# CLR 的执行模型

聊 CLR 之前，先聊聊 Java 以及 Java 虚拟机。Java 借助于其跨平台特性而风靡各个平台。Java 能跨平台，得益于 Java 虚拟机。javac 编译器将 Java 的源码编译为字节码，字节码是在 Java 虚拟机上可执行的二进制文件。

![Java 执行模型](/img/markdown_20201116150437.png)

只要电脑安装了 Java 运行时，就可以通过 Java 运行时运行 Java 程序。回顾一下 Java 的命令行编译运行过程：先 `javac ***.java` 得到一个 `***.class` 的字节码文件（你可以用文本编辑器打开，里面都是 0 和 1），再用 `java ***` 来运行这个字节码文件。

微软想开发出一款类似 Java 虚拟机一样的一种运行时，让程序可以在任何安装了某种虚拟机（或者叫运行时）的机器上运行，但是又不想像 Java 虚拟机一样限定只能用 Java 语言。所以，微软推出了.NET Framework。

.NET Framework 包含两部分，一个是.NET Framework 类库，另一个就是 CLR。CLR 可以理解为微软版 Java 虚拟机。CLR 在设计时考虑支持的特性：多语言支持、程序集加载、垃圾回收机制、类型安全、异常处理、线程同步等。简单说，CLR 为了方便，为了安全，为了简化编码过程。CLR 比 Java 虚拟机更加强大，因为它生来就拥有.NET Framework 类库的支撑。CLR 不局限于一种编程语言，它支持多种语言，这样，开发面向 CLR 的程序对于熟悉不同语言的程序员将会变得简单，并且，可以利用编程语言各自的特性来完成特定工作，从而提高效率。但是.NET Framework 并不能做到跨平台，它只服务于 Windows。

真正跨平台的是 Xamarin 推出的 Mono。Mono 项目不仅可以运行于 Windows 系统上，还可以运行于 Linux，FreeBSD，Unix，Mac OS 和 Solaris，甚至一些游戏平台，例如：Playstation 3/4，Wii U/Switch，XBox 360/XBox One 之上。它和.NET Framework 相似，也是一种对 CLI(Common Language Infrastructrue) 的实现。微软的.NET Framework 利用.NET Framework 类库作为运行时库，Mono 利用 Mono VM 作为运行时库。Unity 引擎在一开始就选择了 Mono 作为跨平台解决方案，我觉得这在当时的确是明智之选（当然，后面使用了 IL2CPP，这个以后再说）。不管怎么说，Mono 和.NET Framework 都包含 CLR，都依赖于 CLR 完成核心工作。说了这么久，CLR 到底是什么？它是怎么工作的？

## 什么是 CLR

**CLR**，**C**ommon **L**anguage **R**untime，**公共语言运行时**。它可以由多种编程语言使用，只要编程语言是面向 CLR 的。得益于这种特性，我们可以选择不同的编程语言完成不同领域的工作，进而达到最高效的效果。例如：用 APL 语言处理数学或金融应用程序、用 Iron Python 处理一些脚本化的工作等等...这样节省了许多的时间。只要电脑里安装了.NET Framework，就可以运行面向 CLR 的程序。

## 将源代码编译成托管模块

类比于 Java 生成的字节码，CLR 也有类似字节码的东西，但却截然不同。不同的面向 CLR 的编程语言的编译器可以将各自源代码编译成托管模块。

![clr-runtime1](/img/markdown_20201116152543.png)

托管模块并不是二进制的字节码。托管模块通常包含几个部分：

1. PE32 或者 PE32+ 头
2. CLR 头
3. 元数据
4. IL 代码

**PE32/PE32+ 头**是标准 Windows PE 头，**标识了可运行 Windows 版本**，32 代表运行于 32 位或者 64 位，32+ 代表仅运行于 64 位。它也**标识了文件类型**（GUI，CUI，DLL 等），并**包含了一个时间标记**（生成文件的时间戳）。如果托管模块只包含 IL 代码，则 PE 头这部分信息大多数会被忽略。如果模块包含了本机 CPU 代码，则 PE 头中还会包含本机 CPU 代码相关的信息。

**CLR 头包含了一个模块成为托管模块的一些信息**。例如要求的 CLR 版本，一些标志(flag)，托管模块入口方法(Main 方法) 的 MethodDef 元数据 token，以及模块的元数据、资源、强名称、一些标志及其他不太重要的数据项的位置或者大小。

**元数据，实际上是几种表构成的数据块，是数据表的集合。共包含三种表：定义表、引用表、清单表。**（书中说主要有两种，实际有三种）。定义表描述源代码中定义的类型和成员；引用表描述源代码引用的类型和成员；清单表主要包含作为程序集组成部分的那些文件的名称，还描述了程序集的版本、语言文化、发布者、公开导出的类型以及构成程序集的所有文件。当然，后面会再次详谈元数据。

**IL 代码**，中间语言（**I**ntermediate **L**anguage) 代码，编译器编译源代码时生成的代码。IL 顾名思义，一种中间语言，意思就是 IL 代码可以进一步编译成本机 CPU 代码。运行时，CLR 将 IL 代码编译成本机 CPU 代码。由于 CLR 管理它的执行，所以它 **也被称作为托管代码(managed code)** 。

### 元数据

元数据是数据表的集合，包含定义表、引用表、清单表。三种表的作用参照上面已经提及的概念。元数据总是与包含 IL 代码的文件相关联，它总是嵌入和 IL 代码相同的 EXE/DLL 中，使得这两者密不可分。编译器同时生产元数据和 IL 代码，把它们绑定在一起，并嵌入最终生成的托管模块中，所以**元数据和它描述的 IL 代码永远不会失去同步**。

元数据的部分用途：

- 避免了编译时对原生 C/C++ 头和库文件的需求。因为 IL 代码中已经包含了引用类型/成员的全部信息。 **编译器直接从托管模块读取元数据，进而获得引用类型/成员的信息，而不需要依赖于 C/C++ 头文件。** 
-  **智能感知(IntelliSense)** 技术，利用了元数据。它 **解析元数据** ，可以 **获取** 到一个类型提供了哪些 **方法、属性、事件、字段** 等。对于方法，还能获得方法的参数和方法的重载个数等等。这就是我们平时写代码时的智能提醒功能。
-  **CLR** 利用元数据，**验证代码的安全性**， **确保** 代码只执行 **类型安全** 的操作。
- 支持序列化/反序列化对象的字段信息。
- 允许垃圾回收器跟踪对象生命周期。 **垃圾回收器根据元数据判断任何对象的类型的字段引用了哪些其他的对象。** 

关于元数据具体的应用，后面还会提及。

### C++ 与 CLR

C++ 默认生成的是非托管代码的 EXE/DLL 模块，运行时操作非托管数据(native 内存)。C++ 也能生成包含托管代码的模块，只需要开启 **/CLR** 指令，但这种代码想要运行，用户必须拥有 CLR 环境（也就是要装有.NET Framework）。C++ 可以同时编写托管代码和非托管代码，生成到同一个模块中。它也支持托管代码中先使用 C/C++ 原生代码，后面有需要再使用托管类型。

## 将托管模块合并成程序集

### 程序集

可能到这里你会觉得 CLR 会和托管模块直接工作，实际上并不是。 **CLR 和程序集直接工作** ，而 **程序集包含多个模块和资源文件** ，所以 CLR 是间接管理托管模块的。 **程序集(assembly) 是一个或多个模块/资源文件的逻辑性分组，是重用、安全性以及版本控制的最小单元** 。你可以生成单文件程序集或者多文件程序集，这取决于你选择的编译器或工具。CLR 中，程序集相当于“ **组件** ”。

简单理解，程序集是一个集合，一个清单表，它包含了一个或多个托管模块或者资源文件(.jpeg, .gif, .html, .xml, .json 等等等等)。

程序集是可重用的、可保护的、可版本控制的“组件”，它把它的逻辑表示和物理表示区分开。

程序集包含与引用程序集有关的信息，使得它能够 **自描述(self-describing)** 。CLR 能判断为了执行程序集中的代码，程序的 **直接依赖对象(immediate dependency)** 是什么， **不用在注册表或 Active Directory Domain Services(ADDS) 中保存额外信息** ，从而比 **非托管组件更加容易部署** 。

### 合并过程

编译器生成了托管模块以后，还会将生成的托管模块和资源文件（如果有）合并，生成一个程序集。如果一个程序集里只有一个托管模块，并且没有资源文件，那么这个程序集就是托管模块，无需进行额外的操作。

 ![clr_assembly](/img/markdown_20201116180054.png)

## 加载公共语言运行时

### 判断 CLR 是否安装

程序集可以生成为.EXE（可执行应用程序）和.DLL（动态链接库，可供其他可执行应用程序使用）。而想运行或者使用程序集，需要先在电脑里加载 CLR，电脑里必须安装 CLR 环境（Windows 中是.NET Framework）。现在的 Windows 10 出厂就自带了.NET Framework，如果是 Windows 7/8，可能需要手动下载安装。

想要检查自己的 Windows 电脑是否已经安装了.NET Framework，只需要访问 `%SystemRoot%\System32` 路径，查看有没有 `MSCorEE.dll` 文件。

![mscoree.dll](/img/markdown_20201116194902.png)

如果有，说明电脑已经安装好了.NET Framework。

当然，一台电脑可能安装了多个.NET Framework 的不同版本。访问 `%SystemRoot%\Microsoft.NET\Framework` 和 `%SystemRoot%\Microsoft.NET\Framework64` 查看。

![framework](/img/markdown_20201116195015.png)

![framework64](/img/markdown_20201116195046.png)

### 查看 CLR 版本号

.NET Framework SDK 也提供了名为 CLRVer.exe 的程序，它可以列出电脑上安装的所有 CLR 版本，也能列出机器中正在运行的进程使用的 CLR 版本号。

我先用 Everything 找到 clrver.exe 所在的位置：

![find_clrver.exe](/img/markdown_20201116200557.png)

然后在所在目录打开 cmder：

```batch
clrver.exe -all
```

![clrver.exe -all](/img/markdown_20201116195445.png)

可以看到有不同的版本。

然后我随便找了一个客户端-服务器的游戏的 DEMO 运行，去任务管理器查看它们的 PID（进程 ID），再：

```batch
clrver.exe <PID>
```

![clrver<PID>](/img/markdown_20201116200221.png)

也可以查看它们对应使用 CLR 的版本号。

### 生成特定平台的程序集

如果程序集文件只包含类型安全的托管代码，代码在 32 为和 64 位 Windows 上都能正常工作。不论你是 Windows 10 还是 Windows RT，不论你是 32 位还是 64 位。

但是有些情况下，开发人员希望代码只在特定版本特定架构的 Windows 上运行。这就需要利用 C# 的命令行开关 `/platform`。

C# 编译器提供了 `/platform` 命令行开关选项，它提供了一些备选项，对应不同的效果：

| /platform 开关        | 生成的托管模块   | x86 Windows          | x64 Windows           | ARM Windows RT       |
| -------------------- | ---------------- | -------------------- | --------------------- | -------------------- |
| anycpu(默认)         | PE32/任意 CPU 架构 | 作为 32 位应用程序运行 | 作为 64 位应用程序运行  | 作为 32 位应用程序运行 |
| anycpu32bitpreferred | PE32/任意 CPU 架构 | 作为 32 位应用程序运行 | 作为 WoW64 应用程序运行 | 作为 32 位应用程序运行 |
| x86                  | PE32/x86         | 作为 32 位应用程序运行 | 作为 WoW64 应用程序运行 | 不运行               |
| x64                  | PE32+/x64        | 不运行               | 作为 64 位应用程序运行  | 不运行               |
| ARM                  | PE32/ARM         | 不运行               | 不运行                | 作为 32 位应用程序运行 |

> WoW64(Windows on Windows64) 是在 64 位 Windows 中运行 32 位应用程序的一种技术。

微软发布了 SDK 命令行使用程序 DumpBin.exe 和 CorFlags.exe，可以用它们检查编译器生成的托管模块所嵌入的信息。具体操作流程，会在本篇的实践部分中尝试。

### 加载 CLR 的过程

可执行程序运行时，Windows 检查文件头，判断需要 32 位还是 64 位地址空间。PE32 文件在 32 位或者 64 位地址空间中均可运行，PE32+ 只能在 64 位地址空间中运行。Windows 还会检查头中嵌入的 CPU 架构信息，确保当前计算机的 CPU 符合要求。最后，Windows 的 64 位版本通过 WoW64 技术运行 32 位 Windows 应用程序。

Windows 检查 EXE 文件头，决定是创建 32 位还是 64 位进程后，会在进程地址空间加载 MSCorEE.dll 的 x86,x64 或 ARM 版本。如果是 Windows 的 x86 或 ARM 版本，MSCoreEE.dll 的 x86 版本在 `%SystemRoot%\System32` 目录中。如果是 Windows 的 x64 版本，MSCoreEE.dll 的 x86 版本在 `%SystemRoot%\SysWow64` 目录中，x64 版本在 `%SystemRoot%\System32` 中（向后兼容）。然后，进程的主线程调用 `MSCorEE.dll` 中定义的一个方法，这个方法初始化 CLR，加载 EXE 程序集，再调用其入口方法(Main)。然后，托管应用程序就启动并运行了。

![load_clr](/img/markdown_20201116212756.png)

> 非托管应用程序用 LoadLibrary 加载托管程序集，Windows 会自动加载并初始化 CLR。64 为进程无法完全加载/platform:x86 开关编译的托管程序集，但是/platform:x86 开关编译的可执行文件在 64 位 Windows 中可以用 WoW64 技术来加载。

## 执行程序集的代码

### 初识 IL

程序集的代码，实际上就是指 IL。 **IL 是与 CPU 无关的代码，它是一种比大多数 CPU 机器语言都高级的语言** 。它能访问和操作对象类型，提供了指令来创建和初始化对象、调用对象上的虚方法以及直接操作数组元素。甚至提供了抛出和捕获异常的指令来实现异常处理。没错，它很像我们熟悉的面向对象编程语言，你 **可以理解它是面向对象的机器语言** 。

在编写面向 CLR 的程序时使用 C#、VB 等高级语言，C#、VB 的编译器会生成 IL。当然，IL 也能用汇编语言写。微软提供了 IL 的汇编器 ILAsm.exe 和 IL 的反汇编器 ILDasm.exe，关于他们的具体操作在实践部分提及。

高级语言通常只公开了 CLR 全部功能的一个子集。但是 **IL 能够访问 CLR 的全部功能** 。如果你选用的语言隐藏了 CLR 的一个功能，你可能需要用 IL 来编写那部分代码。

### 执行方法的过程

方法首次被执行时，CLR 通过 JIT(just-in-time，即时) 编译器将方法的 IL 转换成本机 CPU 指令。

举个例子，有一个托管 EXE，它的源程序的 Main 方法如下：

```csharp
static void Main()
{
    Console.WriteLine("Hello");
    Console.WriteLine("Goodbye");
}
```

在执行 Main 方法以前，CLR **首先检测** 出 Main 方法里 **引用的所有类型** 。CLR **分配一个内部数据结构** 来管理对引用类型的访问，上面的代码引用了 Console 类型，则分配的内部数据结构存放的都是 Console 类型的方法的记录项， **每一个记录项里包含方法的地址** ，根据这个地址可以找到方法的具体实现。这个结构初始化时，CLR 将 **每个记录项都指向一个 JITCompiler 函数** ，它来完成后续的工作。

![data_struct](/img/markdown_20201116220042.png)



Main 方法首次调用 WriteLine(string) 方法时，JITCompiler 函数会被调用。JITCompiler 函数完成以下工作：

1. 在负责实现类型（上面的例子中是 Console 类型）的程序集的元数据中查找被调用的方法（上面的例子中是 WriteLine(string)）
2. 从元数据中获取该方法的 IL
3. 分配内存块
4. 将 IL 编译成本机 CPU 指令，然后将这些本机代码存储到 3 中分配的内存中
5. 在 Type 表中修改与方法对应的条目，使它指向 3 分配的内存块
6. 跳转到内存块中的本机代码

![jitcompiler](/img/markdown_20201116222714.png)

这么做的 **目的就是，第一次先在内存块中存储编译好的本机 CPU 代码，下一次再调用同一方法时，直接跳转到该内存块，执行本机 CPU 代码，而不用再次将 IL 编译为本机 CPU 代码** 。

所以当调用 `Console.WriteLine("Goodbye");` 的时候，不再调用 JITCompiler 函数，而是直接跳转到之前分配的内存块中执行已经生成好的本机 CPU 指令。

![second_time](/img/markdown_20201116223435.png)

这样做的话， **方法第一次调用的时候有一定的性能损失，但是对于后面该方法的调用，就是全速运行了** （执行的是本机 CPU 指令）。

JIT 编译器将编译生成的本机 CPU 指令存储在动态内存中，这意味着 **应用程序终止，编译好的代码也就被丢弃了** 。再次运行应用程序（或者同时运行应用程序的两个不同实例）JIT 编译器必须再次将 IL 编译成本机 CPU 代码。相比而言，本机应用程序的只读代码页可由应用程序正在运行的所有实例共享。

### 代码的优化

 **JIT 编译器默认会对本机代码进行优化** 。可能需要较多时间生成优化代码，但是优化后的代码性能更佳。

使用 C# 编译的开关 `/optimize` 和 `/debug` 会影响代码的优化。

| 编译器开关设置                      | C# IL 代码质量 | JIT 本机代码质量 |
| ----------------------------------- | ------------- | ---------------- |
| /optimize- /debug-(默认)            | 未优化        | 有优化           |
| /optimize- /debug(+/full/pdbonly)   | 未优化        | 未优化           |
| /optimize+ /debug(-/+/full/pdbonly) | 有优化        | 有优化           |

**/optimize 开关是针对 IL 是否优化的开关，/debug 开关是针对 JIT 本机代码是否优化的开关。**

如果 **选择/optimize-** ，那么在 C# 编译器生成的为优化 IL 代码中，将会 **包含许多 NOP** (no-operation，空操作) 指令，还 **包含** 许多跳转到下一行代码的 **分支指令** 。Visual Studio 利用这些指令在调试期间提供“编辑并继续”(edit-and-continue) 功能。利用这些指令还可以在 if、else、for、while、try、catch、finally 等控制语句块上设置断点，使得代码调试更加容易。但是，如果生成优化的 IL 代码，C# 编译器会删除这些多余的 NOP 和分支指令，从而难以单步调试。在调试中执行，一些函数的求值可能也无法进行。不过优化后的 IL 代码更小也更易读，生成的 EXE/DLL 也更小。

只有 **指定/debug(+/full/pdbonly)** 开关，编译器才会 **生成 PDB(Program Database)** 文件。

> PDB 文件帮助调试器查找局部变量并将 IL 指令映射到源代码。

 **指定/debug:full** 开关 JIT 记录每条 IL 指令所生成的本机代码，用于 **即时调试** ；不指定则不记录 IL 与本机代码之间的联系，JIT 编译运行较快，使用内存较少。 **如果用 VS 的调试器启动进程，无论/debug 开关的设置是什么，JIT 会被强制记录 IL 与本机代码之间的联系（除非 VS 关闭了“在模块中加载时取消 JIT 优化(仅限托管)”的选项）** 。

> 在 VS 的项目设置配置中：
>
> 调试(Debug) 指定/optimize-和/debug:full 开关。
>
> 发布(Release) 指定/optimize+ 和/debug:pdbonly 开关。

### 托管代码相较于非托管代码的优势

- JIT 编译器能判断应用程序在特定 CPU 上（例如奔腾 4）是否能运行，可以利用 CPU 的特殊指令，达到提升性能的效果，但非托管应用是针对最小功能集合的 CPU 编译的，无法使用提升性能的特殊指令。
- JIT 编译器能判断一个特定的测试在它运行的机器上是否总是失败。如果一个 if 根据 JIT 判断总是不满足，那 JIT 会直接不对该 if 进行编译。这样代码更小，执行更快。
- 应用程序运行时，CLR 可以评估代码的执行。

如果觉得 JIT 的性能还是不够好，可以尝试.NET Framework SDK 提供的 **NGen.exe** 工具。NGen 有利有弊，后面再说。还可以使用 **System.Runtime.ProfileOptimization** 类。

### IL 和验证

 **IL 基于栈** 。指令都将操作数压入执行栈，从栈弹出结果。IL 没有寄存器指令，所以可以很容易地创建新的语言和编译器，生成面向 CLR 的代码（我理解为：IL 对 CPU 底层进行了抽象，与 CPU 无关，不用考虑 CPU 寄存器，所以容易创建新的语言和编译器）

 **IL 指令是无类型(typeless) 的** 。例如 add 指令，操作数不区分 32 位和 64 位版本，它自动判断操作数类型，执行恰当的操作。

 **验证是指：CLR 对高级 IL 代码进行安全检查。** (核实方法的参数数量和类型是否正确，返回值是否正确使用，方法是否有一个返回语句等等) 验证托管代码，可以确保代码不会不正确的访问内存，不会干扰另一个应用程序的代码。

 **CLR 允许一个进程执行多个托管应用程序。** 每个托管应用程序都在一个 AppDomain 中执行，每个托管 EXE 文件默认在自己的独立地址空间中运行，这个空间只有一个 AppDomain。但是 CLR 宿主进程可以在一个进程中运行多个 AppDomain。

### 不安全的代码

**不安全的代码运行直接操作内存地址和操作地址处的字节**。一般只有在与非托管代码操作或提高效率和性能时才这么做。

如果 C# 要使用不安全的代码，则需要使用/unsafe 开关。JIT 编译不安全代码时，会查看 SecurityPermission 权限，查看 SkipVerification 标志，如果没有权限或没有设置标志，则抛出 InvalidProgramException 或 VerificationException 异常，禁止方法执行，程序可能直接终止，防止造成危害。

微软提供了 **PEVeify.exe** 的工具**可以检查程序集中所有的代码，报告其中含有不安全的代码的方法。**

## 本机代码生成器 NGen.exe

**NGen.exe——应用程序安装时将 IL 编译为本机代码。**

### NGen.exe 的作用

1. **提高应用程序启动速度**。因为直接执行本机代码，不用再进行 JIT 编译。
2. **减小应用程序工具集(working set，已映射的物理内存的一部分，CPU 可以直接访问)。** NGen.exe 将 IL 编译为本机代码，并保存到单独的文件，该文件可以通过“内存映射”同时映射到多个进程地址空间，达到代码共享的作用。这样，减小了工作集（不用每个进程都单独映射一个物理内存）。

### NGen.exe 的缺点

- NGen 生成的文件可能失去同步(CLR 版本问题，CPU 类型问题，Windows 版本问题等等导致的不同步)。
- 较差的执行时性能。NGen 没有对环境进行假定，生成的代码较差，也不能使用特定 CPU 指令等等。

## Framework 类库 FCL

Framework 类库，**F**rameworkd **C**lass **L**ibrary，**FCL**。FCL 是一组 DLL 程序集的统称。

利用 FCL，可以创建：

- Web 服务（利用 ASP.NET 或者 WCF)
- GUI 程序（Windows Store，WPF，WinForm 等）
- Windows 控制台应用
- Windows 服务
- 数据库存储过程
- 组件库

## 通用类型系统 CTS

通用类型系统(Common Type System, CTS) 可以通过一些通用的类型，让用一种编程语言写的代码能与用另一种编程语言写的代码沟通。

CTS 规定一个类型包括零个或多个成员，成员可以是：

- 字段(Field)
- 方法(Method)
- 属性(Property)
- 事件(Event)

CTS 指定了类型可见性规则以及类型成员的访问规则：

- private：成员只能由同一个类型中的其他成员访问。
- family：成员可以由派生类型访问。C# 使用 protected 修饰。
- family and assembly：成员可以由派生类型访问，但派生类型必须在同一个程序集中定义。C# 没有提供这种访问控制。
- assembly：成员可由同一程序集中的任何代码访问。C# 使用 internal 修饰。
- family or assembly：成员可由任何程序集中的派生类型访问，也可由同一个程序集中的任意类型访问。C# 使用 protected internal 修饰。
- public：成员可由任意程序集中的任何代码访问。

CTS 规定只能单继承。

CTS 规定所有类型都从 System.Object 继承。

System.Object 做以下操作：

- 比较两个实例的相等性(Equals)
- 获取实例的哈希码(GetHashCode)
- 查询一个实例的真正类型(GetType)
- 执行实例的浅拷贝(MemberwiseClone)
- 获取实例对象当前状态的字符串表示(ToString)

这在后面类型基础会再次提及。

## 公共语言规范 CLS

公共语言规范，**C**ommon **L**anguage **S**pecification，**CLS**。它是一个最小的功能集，任何编译器只有支持这个功能集，生成的类型才能兼容其他符合 CLS、面向 CLR 的语言生成的组件。

使用 **[assembly: CLSCompliant(true)]** 特性，判断是否存在不符合 CTS 的类型。

使用反汇编工具(ILDasm.exe) 可以从元数据中查看类型的字段和方法。

## 与非托管代码的互操作性

- 托管代码能调用 DLL 中的非托管函数
- 托管代码可以使用现有 COM 组件（服务器）
- 非托管代码可以使用托管类型（服务器）

> COM:The Component Object Model 组件对象模型，COM 对象是遵循 COM 规范编写、以 Win32 动态链接库（DLL）或可执行文件（EXE）形式发布的可执行二进制代码，能够满足对组件架构的所有需求。

# 生成、打包、部署和管理应用程序及类型

### .NET Framework 的部署目标

由于出现了 DLL hell、安装复杂、不够安全等问题，.NET Framework 需要考虑如何解决这些问题。

> DLL hell，DLL 冲突，安装新软件时，新的 DLL 影响到了已有软件的正常使用。
>
> 安装复杂：安装时，文件分散到多个目录，还需要注册表，桌面快捷方式，启动栏等等。卸载时也卸载不干净。
>
> 不够安全：有些代码可以在不知不觉中删发文件，用户害怕这种软件的存在。

对于安装复杂的问题，.NET Framework 很大程度上解决了。它与 COM 不同，类型不再需要注册表中的设置，文件目录不会四处繁多。但还是有应用的快捷方式。

对于安全问题，.NET Framework 包含了称为“代码访问安全性”(Code Access Security) 的安全模型。代码访问安全性允许宿主设置权限，控制组件能做的事情，而不是原来的 Windows 安全性，赋予软件用户权限后，全部功能就拥有了用户权限，获得了完全的信任。.NET Framework 允许用户控制哪些组件能安装，哪些组件能运行，这是很灵活的。

对于 DLL hell，马上进入正题。

### 将类型生成到模块中

#### 最简单的命令行编译

对于这样一个简单的 C# 源程序 Program.cs：

```csharp
//Program.cs
public sealed class Program
{
    public static void Main()
    {
        System.Console.WriteLine("Hi");
    }
}
```

System.Console 定义自微软提供的 MSCorLib.dll，想要编译以上代码为 exe 可执行控制台应用程序，按照原本的规则需要指明引用：

```bash
csc.exe /out:Program.exe /t:exe /r:MSCorLib.dll Program.cs
```

/out:Program.exe 指生成的输出文件名为 Program.exe。

/t，/target 的简单表达。指输出文件的类型，/t:exe 指可执行控制台应用程序(还有/t:winexe 指 GUI 程序，/t:appcontainerexe 指 Windows Store 应用)，还有/t:library、/t:winmdobj、/t:module。

/r，/reference 的简单表达。指引用程序集的名称。/r:MSCorLib.dll 指引用了微软提供的 MSCorLib.dll。

最后一个参数是源码路径，这里是相对路径，所以是源码带后缀的名称 Program.cs。

MSCorLib.dll 包含所有核心类型：Byte, Char, String, Int32 等等。由于 MSCorLib.dll 经常被引用，所以 C# 编译器实际上会自动引用 MSCorLib.dll 程序集。

上面的命令行可以简化：

```bash
csc.exe /out:Program.exe /t:exe Program.cs
```

而，/out:Program.exe 和 /t:exe 是 C# 编译器的默认参数，所以还可以更加简化：

```bash
csc.exe Program.cs
```

这样，就会得到一个可执行的控制台应用程序 Program.exe

如果不想默认引用 MSCorLib.dll，可以使用/nostdlib 参数。当然，上述代码如果使用/nostdlib 参数，编译会报错，因为 System.Console 类型定义自 MSCorLib.dll。

实际操作：打开.NET Framework 所在目录，可以发现 csc.exe 和 MSCorLib.dll 都在这同一个目录中（所以上面的命令行是可行的，使用的是相对路径）

![csc.exe](/img/markdown_20201118101403.png)

![mscorlib.dll](/img/markdown_20201118101509.png)

为了和书中的例子进行区分，我们先把.NET Framework 的路径加入环境变量 PATH 中，当然，可能环境变量中已经配置了这个路径，你可以自己看看：

![path](/img/markdown_20201118101713.png)

这样我们就可以在任意路径使用 csc.exe 和引用 mscorlib.dll 及其他微软提供的所有程序集了。

我选择在 D 盘新建文件夹 TestCSC，在 TestCSC 文件夹中新建文件 Hello.cs

```csharp
//Hello.cs
public sealed class Program
{
    public static void Main()
    {
        System.Console.WriteLine("Hello, World!");
    }
}
```

然后在 TestCSC 目录打开 cmder:

```bash
csc.exe /out:Hello.exe Hello.cs
```

![csc_cmder](/img/markdown_20201118102256.png)

这样就得到了 Hello.exe。最后用 cmder 运行 Hello.exe:

![csc_cmder_run](/img/markdown_20201118102339.png)

可以看到，运行成功。

如果加上/nostdlib 参数：

![nostdlib](/img/markdown_20201118102523.png)

的确报错了。错误指出 System.Object 未定义或未导入，可能是因为 System.Console 继承自 System.Object，System.Console 的声明不是在 mscorlib.dll 中，声明中得出它继承自 System.Object，但 System.Object 的声明和定义在 mscorlib.dll，加上/nostdlib 就无法得到 System.Object 的定义。

#### 使用响应文件

响应文件，实际上就是参数清单。例如上面的/t /r /out，都可以放在一个响应文件中，缩短命令行命令的长度，而且方便用户配置。

例如把上面的参数写到响应文件 TestRsp.rsp 中:

```text
/out:HelloRsp.exe
/t:exe
```

然后 cmder：

```bash
csc.exe @TestRsp.rsp Hello.cs
```

![](/img/markdown_20201118104328.png)

得到了 HelloRsp.exe。运行效果自然和 Hello.exe 一模一样。

命令行默认指定了全局响应文件 CSC.rsp，它在.NET Framework 的根目录中：

![csc.rsp](/img/markdown_20201118104510.png)

![csc.rsp.src](/img/markdown_20201118104609.png)

当然，如果指定了 csc.rsp，但没有引用到里面的任意程序集，就不会影响最后的程序集文件，不会影响程序执行性能。

如果不想指定 csc.rsp，可以添加/noconfig 参数，这将忽略 csc.rsp 文件。

#### 再谈元数据 和 ILDasm.exe 的使用

回顾一下：托管 PE 文件由 PE32(+) 头、CLR 头、元数据以及 IL 构成。

元数据由三种表构成：定义表(definition table)、引用表(reference table)、清单表(manifest table)。

常用定义表有：ModuleDef(模块定义表)、TypeDef(类型定义表)、MethodDef(方法定义表)、FieldDef(字段定义表)、ParamDef(参数定义表)、PropertyDef(属性定义表)、EventDef(事件定义表)。

常用的引用表有：AssemblyRef(程序集引用表)、ModuleRef(模块引用表)、TypeRef(类型引用表)、MemberRef(成员引用表)。

常用的清单表有：AssemblyDef(程序集定义表)、FileDef(文件定义表)、ManifestResourceDef(清单资源定义表)、ExportedTypesDef(导出类型定义表)

可以用 ILDasm.exe 查看元数据，ILDasm.exe 的具体位置可以用 Everything 找到

![ildasm](/img/markdown_20201118140145.png)

用 ildasm.exe 打开之前写的 Hello.exe:

![ildasm_hello.exe](/img/markdown_20201118203348.png)

可以看到这样的结构：

|-- D:\TestCSC\Hello.exe

​    | -- M A N I F E S T

​    | -- Program

​        | -- .class public auto ansi sealed beforefieldinit

​        | -- .ctor : void()

​        | -- Main : void()

MANIFEST 是清单文件:

![MANIFEST](/img/markdown_20201118204431.png)

大致可以分析出 Hello 程序集引用了程序集 mscorlib，并说明了 mscorlib 程序集的公钥和版本号，说明了 Hello 程序集的一些特性、哈希算法、版本号。

也看出来 Hello 程序集就只有一个模块：Hello.exe，也就是它本身，和之前说的吻合。

还有一些其他的标记，subsystem 是 WINDOWS_CUI 可以看出它是 CUI 程序也就是控制台应用程序。其他的标记暂时还不清楚。

Program 是类，Program 下有三个元素，第一个是 Program 类的类型定义，是 public sealed class 三个 C# 关键字在 IL 中的表达:

![Programe-class-defination](/img/markdown_20201118204516.png)

可以看到 Program 类是公共密封类，继承自 mscorlib.dll 中定义的 System.Object 类。

.ctor : void() 是指无参、返回值类型为 void 的实例构造器

![constructor_of_Program](/img/markdown_20201118204822.png)

大致从 instance 和.ctor 可以看出它是实例构造器，从 cil managed 可以看出这个方法的内容属于 CIL 托管代码。

.ctor 中调用了 System.Object 的实例构造器，这符合逻辑，因为 Program 类继承自 Object 类，它的实例构造器默认就要调用父类的实例构造器，尽管 Object 类的实例构造器什么事也没做。

Main : void() 是指无参、返回值类型为 void 的入口方法 Main

![Main](/img/markdown_20201118205716.png)

.entrypoint 代表这个方法是入口方法。nop 命令是空操作。ldstr 命令是为字符串分配内存并存储，这里定义了"Hello, World"这样一个字符串。

call 命令调用了 mscorlib 程序集中的 System.Console 类型中的 WriteLine(string) 静态方法。

ret 操作自然是代表函数返回(return)

还可以查看元数据表，通过点击 视图->元信息->显示！:

![show_meta_manifest](/img/markdown_20201118210709.png)

![metainfo](/img/markdown_20201118210801.png)

里面可以看到关于 定义表、引用表和清单表的描述。

还可以通过 视图->统计 查看一些统计信息：

![statistics](/img/markdown_20201118211138.png)

大概可以根据字面意思了解很多统计数据。数据的单位默认是字节，除非打了括号，括号前的是数量，括号里是字节数。

通过 File Size 验证一下文件大小：

![file_size](/img/markdown_20201118211446.png)

的确是 3584 字节。

### 将模块合并成程序集

这部分内容主要是讲述方法。我就直接讲重点了。两种合并方法：

1. csc.exe(C# 编译器) 合并
2. AL.exe(程序集链接器) 合并

#### csc.exe 合并

csc.exe 支持将源文件导出为模块，使用/t:module 参数即可。

例如我现在有两个 C# 源码 A.cs 和 B.cs

```csharp
//A.cs
public sealed class A
{
    public static void Main()
    {
        System.Console.WriteLine("A");
    }
}
```

```csharp
//B.cs
public sealed class B
{
    public static void Main()
    {
        System.Console.WriteLine("B");
    }
}
```

我想让 A.cs 被编译为单一模块文件，再编译 B.cs 为宿主模块，将 A 模块添加到 B 宿主模块所在程序集中。

我先让 A.cs 被编译为单一模块：

```bash
csc.exe /t:module A.cs 
```

会得到 A.netmodule 模块文件

![a.netmodule](/img/markdown_20201118230226.png)

然后我编译 B.cs 的同时添加 A.netmodule，得到 C.dll 程序集:

```bash
csc.exe /out:C.dll /t:library /addmodule:A.netmodule B.cs
```

![c.dll](/img/markdown_20201118230622.png)

我们用 ILDasm.exe 打开这个 C.dll 看看文件结构和元数据表：

![ildasm.exe_c.dll](/img/markdown_20201118230748.png)

可以看到，里面并没有 A 类型，那 A 去哪了？我们再看看元数据表：

![A.netmodule_metainfo](/img/markdown_20201118231038.png)

程序集确实包含了对 A.netmodule 文件的类型的引用。

如果加载 C.dll 前，把 A.netmodule 删除，会报“找不到指定的文件”的错误。

#### AL.exe 合并

 如果程序集要包含不同编译器生成的模块，或者生成时不清楚程序集的打包要求，还或者打包附属程序集（只包含资源文件），程序集链接器就很有用了。

它可以将两个.netmodule 合并到程序集。

继续上面的操作，A.netmodule 已经生成了，我现在生成一个 B.netmodule

```bash
csc.exe /t:module B.cs
```

然后用 al.exe 把 A.netmodule 和 B.netmodule 合并到程序集 C(al).dll

```bash
al.exe /out:C(al).dll /t:library A.netmodule B.netmodule
```

![b.netmodule_c(al).dll](/img/markdown_20201119093959.png)

用 ILDasm.exe 来看看：

![c_al.dll_ildasm](/img/markdown_20201119094449.png)

可以看到里面没有 IL，而且只有一个清单。

再看看元数据表：

![metainfo_c(al).dll](/img/markdown_20201119094640.png)

可以看出，这是一个多文件程序集，而且它是有清单表的。

AL.exe 还可以使用/embed[resource] 嵌入资源文件到 PE 文件，用/link[resource] 链接资源文件（不嵌入到 PE 文件）

相同的，csc.exe 的/resource 可以嵌入资源文件到 PE 文件，用/linkresource 链接资源文件。

AL.exe 用/win32res 可嵌入标准 Win32 资源(.res)，用/win32icon 可以指定一个.ico 图标文件。

