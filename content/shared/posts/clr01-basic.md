---
title: 回顾CLR(1)：基础部分
date: 2020-11-16T14:37:09
categories: [Tech]
tags: [CLR, CSharp]
toc: true
---

什么是CLR？什么是元数据？什么是JIT？CLR是如何工作的？

本篇文章较深入地探索《CLR via C#》前三章。

<!--more-->

# 前言

《CLR via C#》这本书，我已经通读过2-3次了，但很多内容我依旧没有深入挖掘和探索。

为什么要读这本书，为什么要多次读这本书？我一开始也不是很清楚。后来我搞明白了。

Unity之所以能够跨平台，和Mono或者IL2CPP有关。而Mono和.NET Framework息息相关。Mono是可跨平台的.NET平台，.NET Framework只能服务于Windows。CLR是Mono或者.NET Framework中的一部分，它起到非常关键的作用。关于Unity跨平台背后的原理，下次再聊。

市面上关于CLR的书籍不是很多，而同时关于C#和CLR的书籍也就只有这本《CLR via C#》。Unity使用C#作为脚本编程语言，脚本编译的工作流程又和CLR息息相关，所以我们要读这本Unity程序员必看的《CLR via C#》。如果我们学习Unity编程，却不了解CLR的工作规则，不了解IL代码相关的概念，只会写出低效率、低性能、低水准的代码。

我决定从这次开始，不光阅读书籍，还要动手实践，在网上查阅更多资料，对比一些已有的概念，来加深对CLR的认识。所以，这篇博文不光会有理论部分，还会有实践部分。

# CLR的执行模型

聊CLR之前，先聊聊Java以及Java虚拟机。Java借助于其跨平台特性而风靡各个平台。Java能跨平台，得益于Java虚拟机。javac编译器将Java的源码编译为字节码，字节码是在Java虚拟机上可执行的二进制文件。

![Java执行模型](/img/markdown_20201116150437.png)

只要电脑安装了Java运行时，就可以通过Java运行时运行Java程序。回顾一下Java的命令行编译运行过程：先`javac ***.java`得到一个`***.class`的字节码文件（你可以用文本编辑器打开，里面都是0和1），再用`java ***`来运行这个字节码文件。

微软想开发出一款类似Java虚拟机一样的一种运行时，让程序可以在任何安装了某种虚拟机（或者叫运行时）的机器上运行，但是又不想像Java虚拟机一样限定只能用Java语言。所以，微软推出了.NET Framework。

.NET Framework包含两部分，一个是.NET Framework类库，另一个就是CLR。CLR可以理解为微软版Java虚拟机。CLR在设计时考虑支持的特性：多语言支持、程序集加载、垃圾回收机制、类型安全、异常处理、线程同步等。简单说，CLR为了方便，为了安全，为了简化编码过程。CLR比Java虚拟机更加强大，因为它生来就拥有.NET Framework类库的支撑。CLR不局限于一种编程语言，它支持多种语言，这样，开发面向CLR的程序对于熟悉不同语言的程序员将会变得简单，并且，可以利用编程语言各自的特性来完成特定工作，从而提高效率。但是.NET Framework并不能做到跨平台，它只服务于Windows。

真正跨平台的是Xamarin推出的Mono。Mono项目不仅可以运行于Windows系统上，还可以运行于 Linux，FreeBSD，Unix，Mac OS和Solaris，甚至一些游戏平台，例如：Playstation 3/4，Wii U/Switch，XBox 360/XBox One之上。它和.NET Framework相似，也是一种对CLI(Common Language Infrastructrue)的实现。微软的.NET Framework利用.NET Framework类库作为运行时库，Mono利用Mono VM作为运行时库。Unity引擎在一开始就选择了Mono作为跨平台解决方案，我觉得这在当时的确是明智之选（当然，后面使用了IL2CPP，这个以后再说）。不管怎么说，Mono和.NET Framework都包含CLR，都依赖于CLR完成核心工作。说了这么久，CLR到底是什么？它是怎么工作的？

## 什么是CLR

**CLR**，**C**ommon **L**anguage **R**untime，**公共语言运行时**。它可以由多种编程语言使用，只要编程语言是面向CLR的。得益于这种特性，我们可以选择不同的编程语言完成不同领域的工作，进而达到最高效的效果。例如：用APL语言处理数学或金融应用程序、用Iron Python处理一些脚本化的工作等等...这样节省了许多的时间。只要电脑里安装了.NET Framework，就可以运行面向CLR的程序。

## 将源代码编译成托管模块

类比于Java生成的字节码，CLR也有类似字节码的东西，但却截然不同。不同的面向CLR的编程语言的编译器可以将各自源代码编译成托管模块。

![clr-runtime1](/img/markdown_20201116152543.png)

托管模块并不是二进制的字节码。托管模块通常包含几个部分：

1. PE32或者PE32+头
2. CLR头
3. 元数据
4. IL代码

**PE32/PE32+头**是标准Windows PE头，**标识了可运行Windows版本**，32代表运行于32位或者64位，32+代表仅运行于64位。它也**标识了文件类型**（GUI，CUI，DLL等），并**包含了一个时间标记**（生成文件的时间戳）。如果托管模块只包含IL代码，则PE头这部分信息大多数会被忽略。如果模块包含了本机CPU代码，则PE头中还会包含本机CPU代码相关的信息。

**CLR头包含了一个模块成为托管模块的一些信息**。例如要求的CLR版本，一些标志(flag)，托管模块入口方法(Main方法)的MethodDef元数据token，以及模块的元数据、资源、强名称、一些标志及其他不太重要的数据项的位置或者大小。

**元数据，实际上是几种表构成的数据块，是数据表的集合。共包含三种表：定义表、引用表、清单表。**（书中说主要有两种，实际有三种）。定义表描述源代码中定义的类型和成员；引用表描述源代码引用的类型和成员；清单表主要包含作为程序集组成部分的那些文件的名称，还描述了程序集的版本、语言文化、发布者、公开导出的类型以及构成程序集的所有文件。当然，后面会再次详谈元数据。

**IL代码**，中间语言（**I**ntermediate **L**anguage)代码，编译器编译源代码时生成的代码。IL顾名思义，一种中间语言，意思就是IL代码可以进一步编译成本机CPU代码。运行时，CLR将IL代码编译成本机CPU代码。由于CLR管理它的执行，所以它 **也被称作为托管代码(managed code)** 。

### 元数据

元数据是数据表的集合，包含定义表、引用表、清单表。三种表的作用参照上面已经提及的概念。元数据总是与包含IL代码的文件相关联，它总是嵌入和IL代码相同的EXE/DLL中，使得这两者密不可分。编译器同时生产元数据和IL代码，把它们绑定在一起，并嵌入最终生成的托管模块中，所以**元数据和它描述的IL代码永远不会失去同步**。

元数据的部分用途：

- 避免了编译时对原生C/C++头和库文件的需求。因为IL代码中已经包含了引用类型/成员的全部信息。 **编译器直接从托管模块读取元数据，进而获得引用类型/成员的信息，而不需要依赖于C/C++头文件。** 
-  **智能感知(IntelliSense)** 技术，利用了元数据。它 **解析元数据** ，可以 **获取** 到一个类型提供了哪些 **方法、属性、事件、字段** 等。对于方法，还能获得方法的参数和方法的重载个数等等。这就是我们平时写代码时的智能提醒功能。
-  **CLR** 利用元数据，**验证代码的安全性**， **确保** 代码只执行 **类型安全** 的操作。
- 支持序列化/反序列化对象的字段信息。
- 允许垃圾回收器跟踪对象生命周期。 **垃圾回收器根据元数据判断任何对象的类型的字段引用了哪些其他的对象。** 

关于元数据具体的应用，后面还会提及。

### C++与CLR

C++默认生成的是非托管代码的EXE/DLL模块，运行时操作非托管数据(native内存)。C++也能生成包含托管代码的模块，只需要开启 **/CLR** 指令，但这种代码想要运行，用户必须拥有CLR环境（也就是要装有.NET Framework）。C++可以同时编写托管代码和非托管代码，生成到同一个模块中。它也支持托管代码中先使用C/C++原生代码，后面有需要再使用托管类型。

## 将托管模块合并成程序集

### 程序集

可能到这里你会觉得CLR会和托管模块直接工作，实际上并不是。 **CLR和程序集直接工作** ，而 **程序集包含多个模块和资源文件** ，所以CLR是间接管理托管模块的。 **程序集(assembly)是一个或多个模块/资源文件的逻辑性分组，是重用、安全性以及版本控制的最小单元** 。你可以生成单文件程序集或者多文件程序集，这取决于你选择的编译器或工具。CLR中，程序集相当于“ **组件** ”。

简单理解，程序集是一个集合，一个清单表，它包含了一个或多个托管模块或者资源文件(.jpeg, .gif, .html, .xml, .json等等等等)。

程序集是可重用的、可保护的、可版本控制的“组件”，它把它的逻辑表示和物理表示区分开。

程序集包含与引用程序集有关的信息，使得它能够 **自描述(self-describing)** 。CLR能判断为了执行程序集中的代码，程序的 **直接依赖对象(immediate dependency)** 是什么， **不用在注册表或Active Directory Domain Services(ADDS)中保存额外信息** ，从而比 **非托管组件更加容易部署** 。

### 合并过程

编译器生成了托管模块以后，还会将生成的托管模块和资源文件（如果有）合并，生成一个程序集。如果一个程序集里只有一个托管模块，并且没有资源文件，那么这个程序集就是托管模块，无需进行额外的操作。

 ![clr_assembly](/img/markdown_20201116180054.png)

## 加载公共语言运行时

### 判断CLR是否安装

程序集可以生成为.EXE（可执行应用程序）和.DLL（动态链接库，可供其他可执行应用程序使用）。而想运行或者使用程序集，需要先在电脑里加载CLR，电脑里必须安装CLR环境（Windows中是.NET Framework）。现在的Windows 10出厂就自带了.NET Framework，如果是Windows 7/8，可能需要手动下载安装。

想要检查自己的Windows电脑是否已经安装了.NET Framework，只需要访问`%SystemRoot%\System32`路径，查看有没有`MSCorEE.dll`文件。

![mscoree.dll](/img/markdown_20201116194902.png)

如果有，说明电脑已经安装好了.NET Framework。

当然，一台电脑可能安装了多个.NET Framework的不同版本。访问`%SystemRoot%\Microsoft.NET\Framework`和`%SystemRoot%\Microsoft.NET\Framework64`查看。

![framework](/img/markdown_20201116195015.png)

![framework64](/img/markdown_20201116195046.png)

### 查看CLR版本号

.NET Framework SDK也提供了名为CLRVer.exe的程序，它可以列出电脑上安装的所有CLR版本，也能列出机器中正在运行的进程使用的CLR版本号。

我先用Everything找到clrver.exe所在的位置：

![find_clrver.exe](/img/markdown_20201116200557.png)

然后在所在目录打开cmder：

```
clrver.exe -all
```

![clrver.exe -all](/img/markdown_20201116195445.png)

可以看到有不同的版本。

然后我随便找了一个客户端-服务器的游戏的DEMO运行，去任务管理器查看它们的PID（进程ID），再：

```
clrver.exe <PID>
```

![clrver<PID>](/img/markdown_20201116200221.png)

也可以查看它们对应使用CLR的版本号。

### 生成特定平台的程序集

如果程序集文件只包含类型安全的托管代码，代码在32为和64位Windows上都能正常工作。不论你是Windows 10还是Windows RT，不论你是32位还是64位。

但是有些情况下，开发人员希望代码只在特定版本特定架构的Windows上运行。这就需要利用C#的命令行开关`/platform`。

C#编译器提供了`/platform`命令行开关选项，它提供了一些备选项，对应不同的效果：

| /platform开关        | 生成的托管模块   | x86 Windows          | x64 Windows           | ARM Windows RT       |
| -------------------- | ---------------- | -------------------- | --------------------- | -------------------- |
| anycpu(默认)         | PE32/任意CPU架构 | 作为32位应用程序运行 | 作为64位应用程序运行  | 作为32位应用程序运行 |
| anycpu32bitpreferred | PE32/任意CPU架构 | 作为32位应用程序运行 | 作为WoW64应用程序运行 | 作为32位应用程序运行 |
| x86                  | PE32/x86         | 作为32位应用程序运行 | 作为WoW64应用程序运行 | 不运行               |
| x64                  | PE32+/x64        | 不运行               | 作为64位应用程序运行  | 不运行               |
| ARM                  | PE32/ARM         | 不运行               | 不运行                | 作为32位应用程序运行 |

> WoW64(Windows on Windows64)是在64位Windows中运行32位应用程序的一种技术。

微软发布了SDK命令行使用程序DumpBin.exe和CorFlags.exe，可以用它们检查编译器生成的托管模块所嵌入的信息。具体操作流程，会在本篇的实践部分中尝试。

### 加载CLR的过程

可执行程序运行时，Windows检查文件头，判断需要32位还是64位地址空间。PE32文件在32位或者64位地址空间中均可运行，PE32+只能在64位地址空间中运行。Windows还会检查头中嵌入的CPU架构信息，确保当前计算机的CPU符合要求。最后，Windows的64位版本通过WoW64技术运行32位Windows应用程序。

Windows检查EXE文件头，决定是创建32位还是64位进程后，会在进程地址空间加载MSCorEE.dll的x86,x64或ARM版本。如果是Windows的x86或ARM版本，MSCoreEE.dll的x86版本在`%SystemRoot%\System32`目录中。如果是Windows的x64版本，MSCoreEE.dll的x86版本在`%SystemRoot%\SysWow64`目录中，x64版本在`%SystemRoot%\System32`中（向后兼容）。然后，进程的主线程调用`MSCorEE.dll`中定义的一个方法，这个方法初始化CLR，加载EXE程序集，再调用其入口方法(Main)。然后，托管应用程序就启动并运行了。

![load_clr](/img/markdown_20201116212756.png)

> 非托管应用程序用LoadLibrary加载托管程序集，Windows会自动加载并初始化CLR。64为进程无法完全加载/platform:x86开关编译的托管程序集，但是/platform:x86开关编译的可执行文件在64位Windows中可以用WoW64技术来加载。

## 执行程序集的代码

### 初识IL

程序集的代码，实际上就是指IL。 **IL是与CPU无关的代码，它是一种比大多数CPU机器语言都高级的语言** 。它能访问和操作对象类型，提供了指令来创建和初始化对象、调用对象上的虚方法以及直接操作数组元素。甚至提供了抛出和捕获异常的指令来实现异常处理。没错，它很像我们熟悉的面向对象编程语言，你 **可以理解它是面向对象的机器语言** 。

在编写面向CLR的程序时使用C#、VB等高级语言，C#、VB的编译器会生成IL。当然，IL也能用汇编语言写。微软提供了IL的汇编器ILAsm.exe和IL的反汇编器ILDasm.exe，关于他们的具体操作在实践部分提及。

高级语言通常只公开了CLR全部功能的一个子集。但是 **IL能够访问CLR的全部功能** 。如果你选用的语言隐藏了CLR的一个功能，你可能需要用IL来编写那部分代码。

### 执行方法的过程

方法首次被执行时，CLR通过JIT(just-in-time，即时)编译器将方法的IL转换成本机CPU指令。

举个例子，有一个托管EXE，它的源程序的Main方法如下：

```csharp
static void Main()
{
    Console.WriteLine("Hello");
    Console.WriteLine("Goodbye");
}
```

在执行Main方法以前，CLR **首先检测** 出Main方法里 **引用的所有类型** 。CLR **分配一个内部数据结构** 来管理对引用类型的访问，上面的代码引用了Console类型，则分配的内部数据结构存放的都是Console类型的方法的记录项， **每一个记录项里包含方法的地址** ，根据这个地址可以找到方法的具体实现。这个结构初始化时，CLR将 **每个记录项都指向一个JITCompiler函数** ，它来完成后续的工作。

![data_struct](/img/markdown_20201116220042.png)



Main方法首次调用WriteLine(string)方法时，JITCompiler函数会被调用。JITCompiler函数完成以下工作：

1. 在负责实现类型（上面的例子中是Console类型）的程序集的元数据中查找被调用的方法（上面的例子中是WriteLine(string)）
2. 从元数据中获取该方法的IL
3. 分配内存块
4. 将IL编译成本机CPU指令，然后将这些本机代码存储到3中分配的内存中
5. 在Type表中修改与方法对应的条目，使它指向3分配的内存块
6. 跳转到内存块中的本机代码

![jitcompiler](/img/markdown_20201116222714.png)

这么做的 **目的就是，第一次先在内存块中存储编译好的本机CPU代码，下一次再调用同一方法时，直接跳转到该内存块，执行本机CPU代码，而不用再次将IL编译为本机CPU代码** 。

所以当调用`Console.WriteLine("Goodbye");`的时候，不再调用JITCompiler函数，而是直接跳转到之前分配的内存块中执行已经生成好的本机CPU指令。

![second_time](/img/markdown_20201116223435.png)

这样做的话， **方法第一次调用的时候有一定的性能损失，但是对于后面该方法的调用，就是全速运行了** （执行的是本机CPU指令）。

JIT编译器将编译生成的本机CPU指令存储在动态内存中，这意味着 **应用程序终止，编译好的代码也就被丢弃了** 。再次运行应用程序（或者同时运行应用程序的两个不同实例）JIT编译器必须再次将IL编译成本机CPU代码。相比而言，本机应用程序的只读代码页可由应用程序正在运行的所有实例共享。

### 代码的优化

 **JIT编译器默认会对本机代码进行优化** 。可能需要较多时间生成优化代码，但是优化后的代码性能更佳。

使用C#编译的开关`/optimize`和`/debug`会影响代码的优化。

| 编译器开关设置                      | C# IL代码质量 | JIT 本机代码质量 |
| ----------------------------------- | ------------- | ---------------- |
| /optimize- /debug-(默认)            | 未优化        | 有优化           |
| /optimize- /debug(+/full/pdbonly)   | 未优化        | 未优化           |
| /optimize+ /debug(-/+/full/pdbonly) | 有优化        | 有优化           |

**/optimize开关是针对IL是否优化的开关，/debug开关是针对JIT本机代码是否优化的开关。**

如果 **选择/optimize-** ，那么在C#编译器生成的为优化IL代码中，将会 **包含许多NOP** (no-operation，空操作)指令，还 **包含** 许多跳转到下一行代码的 **分支指令** 。Visual Studio利用这些指令在调试期间提供“编辑并继续”(edit-and-continue)功能。利用这些指令还可以在if、else、for、while、try、catch、finally等控制语句块上设置断点，使得代码调试更加容易。但是，如果生成优化的IL代码，C#编译器会删除这些多余的NOP和分支指令，从而难以单步调试。在调试中执行，一些函数的求值可能也无法进行。不过优化后的IL代码更小也更易读，生成的EXE/DLL也更小。

只有 **指定/debug(+/full/pdbonly)** 开关，编译器才会 **生成PDB(Program Database)** 文件。

> PDB文件帮助调试器查找局部变量并将IL指令映射到源代码。

 **指定/debug:full** 开关JIT记录每条IL指令所生成的本机代码，用于 **即时调试** ；不指定则不记录IL与本机代码之间的联系，JIT编译运行较快，使用内存较少。 **如果用VS的调试器启动进程，无论/debug开关的设置是什么，JIT会被强制记录IL与本机代码之间的联系（除非VS关闭了“在模块中加载时取消JIT优化(仅限托管)”的选项）** 。

> 在VS的项目设置配置中：
>
> 调试(Debug)指定/optimize-和/debug:full开关。
>
> 发布(Release)指定/optimize+和/debug:pdbonly开关。

### 托管代码相较于非托管代码的优势

- JIT编译器能判断应用程序在特定CPU上（例如奔腾4）是否能运行，可以利用CPU的特殊指令，达到提升性能的效果，但非托管应用是针对最小功能集合的CPU编译的，无法使用提升性能的特殊指令。
- JIT编译器能判断一个特定的测试在它运行的机器上是否总是失败。如果一个if根据JIT判断总是不满足，那JIT会直接不对该if进行编译。这样代码更小，执行更快。
- 应用程序运行时，CLR可以评估代码的执行。

如果觉得JIT的性能还是不够好，可以尝试.NET Framework SDK提供的**NGen.exe**工具。NGen有利有弊，后面再说。还可以使用 **System.Runtime.ProfileOptimization** 类。

### IL和验证

 **IL基于栈** 。指令都将操作数压入执行栈，从栈弹出结果。IL没有寄存器指令，所以可以很容易地创建新的语言和编译器，生成面向CLR的代码（我理解为：IL对CPU底层进行了抽象，与CPU无关，不用考虑CPU寄存器，所以容易创建新的语言和编译器）

 **IL指令是无类型(typeless)的** 。例如add指令，操作数不区分32位和64位版本，它自动判断操作数类型，执行恰当的操作。

 **验证是指：CLR对高级IL代码进行安全检查。** (核实方法的参数数量和类型是否正确，返回值是否正确使用，方法是否有一个返回语句等等) 验证托管代码，可以确保代码不会不正确的访问内存，不会干扰另一个应用程序的代码。

 **CLR允许一个进程执行多个托管应用程序。** 每个托管应用程序都在一个AppDomain中执行，每个托管EXE文件默认在自己的独立地址空间中运行，这个空间只有一个AppDomain。但是CLR宿主进程可以在一个进程中运行多个AppDomain。

### 不安全的代码

**不安全的代码运行直接操作内存地址和操作地址处的字节。**一般只有在与非托管代码操作或提高效率和性能时才这么做。

如果C#要使用不安全的代码，则需要使用/unsafe开关。JIT编译不安全代码时，会查看SecurityPermission权限，查看SkipVerification标志，如果没有权限或没有设置标志，则抛出InvalidProgramException或VerificationException异常，禁止方法执行，程序可能直接终止，防止造成危害。

微软提供了 **PEVeify.exe** 的工具**可以检查程序集中所有的代码，报告其中含有不安全的代码的方法。**

## 本机代码生成器NGen.exe

**NGen.exe——应用程序安装时将IL编译为本机代码。**

### NGen.exe的作用

1. **提高应用程序启动速度。**因为直接执行本机代码，不用再进行JIT编译。
2. **减小应用程序工具集(working set，已映射的物理内存的一部分，CPU可以直接访问)。** NGen.exe将IL编译为本机代码，并保存到单独的文件，该文件可以通过“内存映射”同时映射到多个进程地址空间，达到代码共享的作用。这样，减小了工作集（不用每个进程都单独映射一个物理内存）。

### NGen.exe的缺点

- NGen生成的文件可能失去同步(CLR版本问题，CPU类型问题，Windows版本问题等等导致的不同步)。
- 较差的执行时性能。NGen没有对环境进行假定，生成的代码较差，也不能使用特定CPU指令等等。

## Framework类库 FCL

Framework类库，**F**rameworkd **C**lass **L**ibrary，**FCL**。FCL是一组DLL程序集的统称。

利用FCL，可以创建：

- Web服务（利用ASP.NET或者WCF)
- GUI程序（Windows Store，WPF，WinForm等）
- Windows控制台应用
- Windows服务
- 数据库存储过程
- 组件库

## 通用类型系统CTS

通用类型系统(Common Type System, CTS)可以通过一些通用的类型，让用一种编程语言写的代码能与用另一种编程语言写的代码沟通。

CTS规定一个类型包括零个或多个成员，成员可以是：

- 字段(Field)
- 方法(Method)
- 属性(Property)
- 事件(Event)

CTS指定了类型可见性规则以及类型成员的访问规则：

- private：成员只能由同一个类型中的其他成员访问。
- family：成员可以由派生类型访问。C#使用protected修饰。
- family and assembly：成员可以由派生类型访问，但派生类型必须在同一个程序集中定义。C#没有提供这种访问控制。
- assembly：成员可由同一程序集中的任何代码访问。C#使用internal修饰。
- family or assembly：成员可由任何程序集中的派生类型访问，也可由同一个程序集中的任意类型访问。C#使用protected internal修饰。
- public：成员可由任意程序集中的任何代码访问。

CTS规定只能单继承。

CTS规定所有类型都从System.Object继承。

System.Object做以下操作：

- 比较两个实例的相等性(Equals)
- 获取实例的哈希码(GetHashCode)
- 查询一个实例的真正类型(GetType)
- 执行实例的浅拷贝(MemberwiseClone)
- 获取实例对象当前状态的字符串表示(ToString)

这在后面类型基础会再次提及。

## 公共语言规范CLS

公共语言规范，**C**ommon **L**anguage **S**pecification，**CLS**。它是一个最小的功能集，任何编译器只有支持这个功能集，生成的类型才能兼容其他符合CLS、面向CLR的语言生成的组件。

使用 **[assembly: CLSCompliant(true)]** 特性，判断是否存在不符合CTS的类型。

使用反汇编工具(ILDasm.exe)可以从元数据中查看类型的字段和方法。

## 与非托管代码的互操作性

- 托管代码能调用DLL中的非托管函数
- 托管代码可以使用现有COM组件（服务器）
- 非托管代码可以使用托管类型（服务器）

> COM:The Component Object Model 组件对象模型，COM对象是遵循COM规范编写、以Win32动态链接库（DLL）或可执行文件（EXE）形式发布的可执行二进制代码，能够满足对组件架构的所有需求。

# 生成、打包、部署和管理应用程序及类型

### .NET Framework的部署目标

由于出现了DLL hell、安装复杂、不够安全等问题，.NET Framework需要考虑如何解决这些问题。

> DLL hell，DLL冲突，安装新软件时，新的DLL影响到了已有软件的正常使用。
>
> 安装复杂：安装时，文件分散到多个目录，还需要注册表，桌面快捷方式，启动栏等等。卸载时也卸载不干净。
>
> 不够安全：有些代码可以在不知不觉中删发文件，用户害怕这种软件的存在。

对于安装复杂的问题，.NET Framework很大程度上解决了。它与COM不同，类型不再需要注册表中的设置，文件目录不会四处繁多。但还是有应用的快捷方式。

对于安全问题，.NET Framework包含了称为“代码访问安全性”(Code Access Security)的安全模型。代码访问安全性允许宿主设置权限，控制组件能做的事情，而不是原来的Windows安全性，赋予软件用户权限后，全部功能就拥有了用户权限，获得了完全的信任。.NET Framework允许用户控制哪些组件能安装，哪些组件能运行，这是很灵活的。

对于DLL hell，马上进入正题。

### 将类型生成到模块中

#### 最简单的命令行编译

对于这样一个简单的C#源程序 Program.cs：

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

System.Console定义自微软提供的MSCorLib.dll，想要编译以上代码为exe可执行控制台应用程序，按照原本的规则需要指明引用：

```bash
csc.exe /out:Program.exe /t:exe /r:MSCorLib.dll Program.cs
```

/out:Program.exe指生成的输出文件名为Program.exe。

/t，/target的简单表达。指输出文件的类型，/t:exe指可执行控制台应用程序(还有/t:winexe指GUI程序，/t:appcontainerexe指Windows Store应用)，还有/t:library、/t:winmdobj、/t:module。

/r，/reference的简单表达。指引用程序集的名称。/r:MSCorLib.dll指引用了微软提供的MSCorLib.dll。

最后一个参数是源码路径，这里是相对路径，所以是源码带后缀的名称Program.cs。

MSCorLib.dll包含所有核心类型：Byte, Char, String, Int32等等。由于MSCorLib.dll经常被引用，所以C#编译器实际上会自动引用MSCorLib.dll程序集。

上面的命令行可以简化：

```bash
csc.exe /out:Program.exe /t:exe Program.cs
```

而，/out:Program.exe 和 /t:exe 是C#编译器的默认参数，所以还可以更加简化：

```bash
csc.exe Program.cs
```

这样，就会得到一个可执行的控制台应用程序Program.exe

如果不想默认引用MSCorLib.dll，可以使用/nostdlib参数。当然，上述代码如果使用/nostdlib参数，编译会报错，因为System.Console类型定义自MSCorLib.dll。

实际操作：打开.NET Framework所在目录，可以发现csc.exe和MSCorLib.dll都在这同一个目录中（所以上面的命令行是可行的，使用的是相对路径）

![csc.exe](/img/markdown_20201118101403.png)

![mscorlib.dll](/img/markdown_20201118101509.png)

为了和书中的例子进行区分，我们先把.NET Framework的路径加入环境变量PATH中，当然，可能环境变量中已经配置了这个路径，你可以自己看看：

![path](/img/markdown_20201118101713.png)

这样我们就可以在任意路径使用csc.exe和引用mscorlib.dll及其他微软提供的所有程序集了。

我选择在D盘新建文件夹TestCSC，在TestCSC文件夹中新建文件Hello.cs

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

然后在TestCSC目录打开cmder:

```bash
csc.exe /out:Hello.exe Hello.cs
```

![csc_cmder](/img/markdown_20201118102256.png)

这样就得到了Hello.exe。最后用cmder运行Hello.exe:

![csc_cmder_run](/img/markdown_20201118102339.png)

可以看到，运行成功。

如果加上/nostdlib参数：

![nostdlib](/img/markdown_20201118102523.png)

的确报错了。错误指出System.Object未定义或未导入，可能是因为System.Console继承自System.Object，System.Console的声明不是在mscorlib.dll中，声明中得出它继承自System.Object，但System.Object的声明和定义在mscorlib.dll，加上/nostdlib就无法得到System.Object的定义。

#### 使用响应文件

响应文件，实际上就是参数清单。例如上面的/t /r /out，都可以放在一个响应文件中，缩短命令行命令的长度，而且方便用户配置。

例如把上面的参数写到响应文件TestRsp.rsp中:

```
/out:HelloRsp.exe
/t:exe
```

然后cmder：

```bash
csc.exe @TestRsp.rsp Hello.cs
```

![](/img/markdown_20201118104328.png)

得到了HelloRsp.exe。运行效果自然和Hello.exe一模一样。

命令行默认指定了全局响应文件CSC.rsp，它在.NET Framework的根目录中：

![csc.rsp](/img/markdown_20201118104510.png)

![csc.rsp.src](/img/markdown_20201118104609.png)

当然，如果指定了csc.rsp，但没有引用到里面的任意程序集，就不会影响最后的程序集文件，不会影响程序执行性能。

如果不想指定csc.rsp，可以添加/noconfig参数，这将忽略csc.rsp文件。

#### 再谈元数据 和 ILDasm.exe的使用

回顾一下：托管PE文件由PE32(+)头、CLR头、元数据以及IL构成。

元数据由三种表构成：定义表(definition table)、引用表(reference table)、清单表(manifest table)。

常用定义表有：ModuleDef(模块定义表)、TypeDef(类型定义表)、MethodDef(方法定义表)、FieldDef(字段定义表)、ParamDef(参数定义表)、PropertyDef(属性定义表)、EventDef(事件定义表)。

常用的引用表有：AssemblyRef(程序集引用表)、ModuleRef(模块引用表)、TypeRef(类型引用表)、MemberRef(成员引用表)。

常用的清单表有：AssemblyDef(程序集定义表)、FileDef(文件定义表)、ManifestResourceDef(清单资源定义表)、ExportedTypesDef(导出类型定义表)

可以用ILDasm.exe查看元数据，ILDasm.exe的具体位置可以用Everything找到

![ildasm](/img/markdown_20201118140145.png)

用ildasm.exe打开之前写的Hello.exe:

![ildasm_hello.exe](/img/markdown_20201118203348.png)

可以看到这样的结构：

|-- D:\TestCSC\Hello.exe

​    | -- M A N I F E S T

​    | -- Program

​        | -- .class public auto ansi sealed beforefieldinit

​        | -- .ctor : void()

​        | -- Main : void()

MANIFEST是清单文件:

![MANIFEST](/img/markdown_20201118204431.png)

大致可以分析出Hello程序集引用了程序集mscorlib，并说明了mscorlib程序集的公钥和版本号，说明了Hello程序集的一些特性、哈希算法、版本号。

也看出来Hello程序集就只有一个模块：Hello.exe，也就是它本身，和之前说的吻合。

还有一些其他的标记，subsystem是WINDOWS_CUI可以看出它是CUI程序也就是控制台应用程序。其他的标记暂时还不清楚。

Program是类，Program下有三个元素，第一个是Program类的类型定义，是public sealed class三个C#关键字在IL中的表达:

![Programe-class-defination](/img/markdown_20201118204516.png)

可以看到Program类是公共密封类，继承自mscorlib.dll中定义的System.Object类。

.ctor : void() 是指无参、返回值类型为void的实例构造器

![constructor_of_Program](/img/markdown_20201118204822.png)

大致从instance和.ctor可以看出它是实例构造器，从cil managed可以看出这个方法的内容属于CIL托管代码。

.ctor中调用了System.Object的实例构造器，这符合逻辑，因为Program类继承自Object类，它的实例构造器默认就要调用父类的实例构造器，尽管Object类的实例构造器什么事也没做。

Main : void() 是指无参、返回值类型为void的入口方法Main

![Main](/img/markdown_20201118205716.png)

.entrypoint代表这个方法是入口方法。nop命令是空操作。ldstr命令是为字符串分配内存并存储，这里定义了"Hello, World"这样一个字符串。

call命令调用了mscorlib程序集中的System.Console类型中的WriteLine(string)静态方法。

ret操作自然是代表函数返回(return)

还可以查看元数据表，通过点击 视图->元信息->显示！:

![show_meta_manifest](/img/markdown_20201118210709.png)

![metainfo](/img/markdown_20201118210801.png)

里面可以看到关于 定义表、引用表和清单表的描述。

还可以通过 视图->统计 查看一些统计信息：

![statistics](/img/markdown_20201118211138.png)

大概可以根据字面意思了解很多统计数据。数据的单位默认是字节，除非打了括号，括号前的是数量，括号里是字节数。

通过File Size验证一下文件大小：

![file_size](/img/markdown_20201118211446.png)

的确是3584字节。

### 将模块合并成程序集

这部分内容主要是讲述方法。我就直接讲重点了。两种合并方法：

1. csc.exe(C# 编译器)合并
2. AL.exe(程序集链接器)合并

#### csc.exe合并

csc.exe支持将源文件导出为模块，使用/t:module参数即可。

例如我现在有两个C#源码A.cs和B.cs

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

我想让A.cs被编译为单一模块文件，再编译B.cs为宿主模块，将A模块添加到B宿主模块所在程序集中。

我先让A.cs被编译为单一模块：

```bash
csc.exe /t:module A.cs 
```

会得到A.netmodule模块文件

![a.netmodule](/img/markdown_20201118230226.png)

然后我编译B.cs的同时添加A.netmodule，得到C.dll程序集:

```bash
csc.exe /out:C.dll /t:library /addmodule:A.netmodule B.cs
```

![c.dll](/img/markdown_20201118230622.png)

我们用ILDasm.exe打开这个C.dll看看文件结构和元数据表：

![ildasm.exe_c.dll](/img/markdown_20201118230748.png)

可以看到，里面并没有A类型，那A去哪了？我们再看看元数据表：

![A.netmodule_metainfo](/img/markdown_20201118231038.png)

程序集确实包含了对A.netmodule文件的类型的引用。

如果加载C.dll前，把A.netmodule删除，会报“找不到指定的文件”的错误。

#### AL.exe合并

 如果程序集要包含不同编译器生成的模块，或者生成时不清楚程序集的打包要求，还或者打包附属程序集（只包含资源文件），程序集链接器就很有用了。

它可以将两个.netmodule合并到程序集。

继续上面的操作，A.netmodule已经生成了，我现在生成一个B.netmodule

```bash
csc.exe /t:module B.cs
```

然后用al.exe把A.netmodule和B.netmodule合并到程序集C(al).dll

```bash
al.exe /out:C(al).dll /t:library A.netmodule B.netmodule
```

![b.netmodule_c(al).dll](/img/markdown_20201119093959.png)

用ILDasm.exe来看看：

![c_al.dll_ildasm](/img/markdown_20201119094449.png)

可以看到里面没有IL，而且只有一个清单。

再看看元数据表：

![metainfo_c(al).dll](/img/markdown_20201119094640.png)

可以看出，这是一个多文件程序集，而且它是有清单表的。

AL.exe还可以使用/embed[resource]嵌入资源文件到PE文件，用/link[resource]链接资源文件（不嵌入到PE文件）

相同的，csc.exe的/resource可以嵌入资源文件到PE文件，用/linkresource链接资源文件。

AL.exe用/win32res可嵌入标准Win32资源(.res)，用/win32icon可以指定一个.ico图标文件。

