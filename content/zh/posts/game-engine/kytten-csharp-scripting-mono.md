---
title: 'Kytten 的 C# 脚本系统：Mono 篇'
date: 2023-05-17T15:45:00
categories: [游戏引擎]
tags: [Kytten, 脚本系统, Mono, CSharp, DotNET]
toc: true
original: true
zhihu: 630199985
---

> 本文转载自我在知乎的专栏文章：[Kytten 的 C# 脚本系统：Mono 篇](https://zhuanlan.zhihu.com/p/630199985)（发布于 2023-05-17），迁移时整理了格式。

> [!NOTE]
> Kytten 引擎已经停止开发，但它确实存在过。它为后来的 [Snow Leopard Engine](https://github.com/SnowLeopardEngine/SnowLeopardEngine)（利兹大学硕士团队项目）以及 [libvultra](https://github.com/zzxzzk115/libvultra) 奠定了基础。文中的 Roadmap 和「后续会加入」的计划不再继续。

Kytten 的 C# 脚本系统正在开发中，部分技术还在调研和测试。

<!--more-->

## C# 脚本系统概述

### 什么是 C# 脚本系统？

C# 脚本系统，是指在引擎非托管层面内嵌 C# 托管运行时，从而实现非托管代码和 C# 托管代码的相互调用。

### 游戏引擎为什么通常需要 C# 脚本系统？

因为，C# 相比其他底层语言 (C/C++/Rust) 更容易掌握和理解。开发者如果使用 C# 进行脚本编程的话，上手会更简单，学习成本更低，开发效率更高。

还有一个原因是 C# 有更好的生态系统，C# 的背后是 .NET，而 .NET 具有庞大的生态体系。未来，.NET 将会成为一个真正大一统的平台，届时，C# 就是 YYDS。

## Mono VS CoreCLR

### Mono

Mono 是一个开源项目，由 Xamarin 公司发起。由于 .NET Framework 只支持 Windows，Mono 应运而生，它的目标是实现跨平台的运行时，实现与 .NET Framework 相同的 ECMA 规范，兼容大部分 .NET Framework 的代码，从而支持使用 C# 编写主流的桌面平台和移动平台的应用程序和库。后来，微软收购了 Xamarin。现在，Mono 具有两个版本，一个由原 Mono 团队继续维护，另一个由微软自己维护，两者功能有所区别，前者更通用，是游戏引擎脚本系统的常用第三方库，后者主要针对微软自家的产品做出了更多的兼容和优化，内嵌到游戏引擎的话并不合适。

- [GitHub - mono/mono](https://github.com/mono/mono)
- [runtime/src/mono at main · dotnet/runtime](https://github.com/dotnet/runtime/tree/main/src/mono)

### CoreCLR

CoreCLR 也是一个开源项目，由微软发起。考虑到 .NET Framework 不支持跨平台，不开源，无法得到社区的支持，微软决定开发一款全新的开源跨平台公共语言运行时，也就是 CoreCLR。它基于 .NET Framework CLR，但它针对平台相关实现进行了重写，对 GC 部分进行了升级和优化，同时提高了多线程和任务等核心功能的性能，其中最重要的是支持跨平台。不过目前，CoreCLR 只支持主流的桌面平台，对于移动平台，微软暂时还是采用 Mono。

[GitHub - dotnet/runtime](https://github.com/dotnet/runtime)

### Mono 与 CoreCLR 的优缺点

Mono 的优势在于，比 CoreCLR 支持更多平台，且内嵌更方便。为什么更方便？因为它的绑定机制更灵活。它支持两种绑定机制：

- P/Invoke (平台调用)
- Mono 内嵌 API

P/Invoke 涉及到更多关于 DLLImport 特性 (最新的为 [LibraryImport 特性](https://learn.microsoft.com/en-us/dotnet/standard/native-interop/pinvoke-source-generation))、调用约定 (Calling Convention)、封送 (Marshaling) 相关的种种内容，相对而言更加复杂，且容易出错，其中任意一个环节出了问题，绑定就失败了，如果我们使用 Mono 的话，通常不会使用 P/Invoke 进行内嵌。

Mono 内嵌 API 则支持在 C++ 层面添加内部调用 (Internal Call)，然后在 C# 层面声明为外部方法 (External Method)，只要命名空间、类名、方法名一一匹配，即可完成绑定。并且，封送也更加方便。以字符串为例，如果是 P/Invoke，则需要指定字符串的封送方式，编码格式等等。Mono 内嵌 API 使用 MonoString 则可以很好地解决字符串封送问题，mono 为此提供了很多便捷的 API。

| C Type | Mono Type | C to Mono | Mono to C |
|---|---|---|---|
| strings, char * | MonoString * | mono_string_new, mono_string_new_len, mono_string_new_wrapper, mono_string_new_utf16 | mono_string_to_utf8, mono_string_to_utf16 |

CoreCLR 的优势在于它具有更高的性能和更高的 C# 版本。它的 GC 比 Mono GC 性能要好很多，且提供了更多现代化的功能，例如 Span、Memory 这些为了提高性能而诞生的结构，提供了更多优化性能后的功能组件，支持最新的 C# 版本 (目前是 11)。但是，CoreCLR 目前仅支持以 P/Invoke 的形式进行代码绑定，所以对于内嵌到游戏引擎中而言更为复杂。我们需要在 C++ 层面加载 hostfxr，进而使得游戏引擎成为 CoreCLR 的宿主，这样可以调用 C# 托管代码。但是对于 C# 调用 C++ 代码的情况，我们还是得通过 P/Invoke 去实现。

[Write a custom .NET host (learn.microsoft.com)](https://learn.microsoft.com/en-us/dotnet/core/tutorials/netcore-hosting)

### Kytten Roadmap

在 Kytten 0.1.0 的 Roadmap 中，我们计划将 mono 嵌入到引擎中，作为脚本系统的底层核心之一，这样就可以最简单地实现 C# 脚本编程，不过支持的 C# 版本会相对低一些，性能也会差一些。

在未来，我们计划将 .NET 8.0 (LTS) 嵌入到引擎中，作为脚本系统的又一底层核心。.NET 的 CoreCLR 会给脚本系统带来巨大的性能提升以及最新 C# 语言版本带来的新特性。

> 如果 CoreCLR 未来提供内嵌 API，那么绑定就更加方便了，希望微软后面会提供这些 API。

如果 C# 脚本系统有两套不同的运行时方案，根据编译器宏参数进行开启和关闭，那么我们还需要编写绑定代码生成器，或者利用源生成器 (Source Generators)，根据选用的运行时 (Mono 或者 CoreCLR) 来生成相应的绑定代码 (使用 Internal Call 或者使用 DLLImport / LibraryImport)。

## 游戏引擎内嵌 Mono (以 Windows 为例)

在游戏引擎中内嵌 Mono 是比较轻松的，因为 Mono 已经为我们提供了内嵌 API，直接使用即可。在正式内嵌 Mono 之前，我们需要编译或者安装 Mono 以获得必要的文件。

编译 Mono 需要一定的时间，直接安装 Mono 一般而言是不错的选择。不过一旦你需要更改 Mono 中的部分逻辑以实现新功能，那就必须编译自己更改后的 Mono。

### 内嵌 Mono 的原理

简单描述，就是，C/C++ 中，托管了一个 Mono 运行时，在 Mono 运行时中初始化 AppDomain，加载程序集等等。

[Embedding Mono | Mono](https://www.mono-project.com/docs/advanced/embedding/#how-embedding-works)

### 编译 Mono 并获得必要文件

> 提示：需要科学上网环境，需要消耗较长时间。需要 Visual Studio 环境，并且安装了 C++ 桌面开发环境。

#### 开启 Windows 开发者模式

`设置→更新和安全→开发者选项→开发人员模式→开`

#### 下载 Cygwin 并安装依赖组件

点击 [下载](http://www.cygwin.com/setup-x86_64.exe)。

下载后，从 CMD 在下载目录执行以下命令进行安装：

```batch
setup-x86_64.exe -P autoconf,automake,bison,gcc-core,gcc-g++,mingw64-i686-runtime,mingw64-i686-binutils,mingw64-i686-gcc-core,mingw64-i686-gcc-g++,mingw64-i686-pthreads,mingw64-i686-w32api,mingw64-x86_64-runtime,mingw64-x86_64-binutils,mingw64-x86_64-gcc-core,mingw64-x86_64-gcc-g++,mingw64-x86_64-pthreads,mingw64-x86_64-w32api,libtool,make,python,gettext-devel,gettext,intltool,libiconv,pkg-config,git,curl,wget,libxslt,bc,patch,cmake,perl,yasm,unzip
```

> 如果遇到 libusb0 安装失败的问题，可以暂时忽略它，点击下一步即可。

#### 编译 Mono

打开 Cygwin 以后，会进入命令行窗口。

我们执行以下命令克隆 Mono 仓库，并切换到最新发布的 Tag，设置安装路径为 mono 源码根目录中的 install 文件夹：

```bash
cd ~
git clone https://github.com/mono/mono.git # Or your own mono git repo
cd mono
git checkout 73df89a # The latest released tag's commit hash
export PREFIX=~/mono/install
export PATH=$PREFIX/bin:$PATH
```

此时 mono 仓库已经克隆下来了，我们在文件资源浏览器中打开 `Cygwin根目录/home/[用户名]/mono`，进入 `msvc` 文件夹，双击打开 `mono.sln` 解决方案，然后编译解决方案。可以选择 Debug / Release + x64 / Win32，根据需求编译即可。此步的目的是获得 MSVC 支持的静态库文件。

> 可能会遇到 libtest 编译没有通过（常量中有换行符）的情况，没有关系，应该是测试用例或者代码页出现的编码问题，不影响其他核心库的编译即可。

编译并安装 64 位版本 Mono：

```bash
./autogen.sh --prefix=$PREFIX --host=x86_64-w64-mingw32 --disable-boehm
make get-monolite-latest
make -j8
make install
```

编译并安装 32 位版本 Mono：

```bash
./autogen.sh --prefix=$PREFIX --host=i686-w64-mingw32 --disable-boehm
make get-monolite-latest
make -j8
make install
```

#### 获得必要的文件

需要获得的文件包括：

- 静态库文件
- 头文件
- 配置文件
- 运行时 DLL 集合

静态库文件在 `msvc/build/` 中，例如，如果我在 `mono.sln` 中选择的编译配置为 Debug + x64，那么对应的需要获得的静态库文件为在 `msvc/build/sgen/x64/lib/Debug/` 中的 `libmono-static-sgen.lib`。

头文件在 `msvc/include/` 中，`mono` 文件夹中包含的就是我们所需要的所有头文件。

配置文件在 `install/etc/` 中，`mono` 文件夹中包含了我们所需要的所有配置文件。

运行时 DLL 集合则在 `install/lib/mono/` 中，通常而言，我们只需要其中的 `4.5` 文件夹，并且，该文件夹中我们只关心 .dll 后缀的程序集文件，其他文件我们不需要。

### 安装 Mono 并获得必要文件

#### 下载并安装 Mono

进入 [Mono 官网](https://www.mono-project.com/download/stable/)，下载最新稳定版，具体选择 32 位还是 64 位看需求。

下载后运行安装即可。

#### 获得必要的文件

需要获得的文件包括：

- 静态库文件
- 头文件
- 配置文件
- 运行时 DLL 集合

以 Mono 安装目录为准。Mono 64 位默认的安装目录为 `C:\Program Files\Mono`。后续 Mono 安装目录以 `%MONO_DIR%` 代替。

静态库文件为在 `%MONO_DIR%/lib/` 中的 `libmono-static-sgen.lib`。

头文件在 `%MONO_DIR%/include/mono-2.0/` 中，`mono` 文件夹中包含的就是我们所需要的所有头文件。

配置文件在 `%MONO_DIR%/etc/` 中，`mono` 文件夹中包含了我们所需要的所有配置文件。

运行时 DLL 集合则在 `%MONO_DIR%/lib/mono/` 中，通常而言，我们只需要其中的 `4.5` 文件夹，并且，该文件夹中我们只关心 .dll 后缀的程序集文件，其他文件我们不需要。

### 项目设置

#### 添加静态链接

根据你的引擎项目结构，链接 `libmono-static-sgen.lib`。在 Windows 下，直接链接它是存在链接错误的，还需要同时链接以下库：

- Mswsock.lib
- ws2_32.lib
- psapi.lib
- version.lib
- winmm.lib
- Bcrypt.lib

Kytten 目前基于 CMake 构建，以下是 Kytten 关于链接 mono 静态库的部分 CMake 代码，省略了 Linux 和 MacOS 的部分：

```cmake
# Link Mono
set(MONO_HEADER_FILES_DIR ${THIRD_PARTY_DIR}/mono)
if (PLATFORM_WINDOWS)
    set(MONO_ROOT_DIR ${PLATFORM_ROOT_DIR}/Windows/Binaries/Mono)
    set(MONO_LIB_DIR ${MONO_ROOT_DIR}/${ARCH}/lib/${CMAKE_BUILD_TYPE})
    target_link_libraries(${TARGET_NAME} PUBLIC ${MONO_LIB_DIR}/libmono-static-sgen.lib)
    target_include_directories(${TARGET_NAME} PUBLIC $<BUILD_INTERFACE:${MONO_HEADER_FILES_DIR}>)

    # Link mono dependencies on Windows
    target_link_libraries(${TARGET_NAME} PUBLIC "Mswsock.lib")
    target_link_libraries(${TARGET_NAME} PUBLIC "ws2_32.lib")
    target_link_libraries(${TARGET_NAME} PUBLIC "psapi.lib")
    target_link_libraries(${TARGET_NAME} PUBLIC "version.lib")
    target_link_libraries(${TARGET_NAME} PUBLIC "winmm.lib")
    target_link_libraries(${TARGET_NAME} PUBLIC "Bcrypt.lib")
elseif(PLATFORM_LINUX)
    # ...
elseif(PLATFORM_DARWIN)
    # ...
else()
    message(WARNING "Currently, Kytten Mono doesn't support this platform.")
endif()
```

### 关键步骤

#### 包含头文件

```cpp
#include <mono/jit/jit.h>
#include <mono/metadata/assembly.h>
#include <mono/metadata/mono-config.h>
```

#### 设置 Mono 的相关路径和配置

Mono 可以指定 .NET 运行库路径和配置路径。如果不指定，则会默认尝试从常用安装目录寻找，如果最终找不到，后续初始化 AppDomain 时则会报错。

```cpp
mono_set_dirs("lib/mono/lib", "lib/mono/etc");
```

除此之外，我们还需要解析 config 文件以初始化 DLL 映射，否则在 MacOS 和 Linux 上可能会出现找不到 DLL 的问题。

```cpp
mono_config_parse("lib/mono/etc/mono/config");
```

#### 初始化 AppDomain

AppDomain 主要用于隔离应用程序。一般，对于游戏引擎而言，我们创建一个 AppDomain 即可。

```cpp
MonoDomain* domain = mono_jit_init("KyttenEngineScripting");
```

上述代码创建了一个名为 "KyttenEngineScripting" 的 AppDomain。

#### 加载程序集

我们首先创建一个 .NET Framework 控制台程序，项目名为 MonoTest，编写 Program.cs：

```csharp
using System;

namespace MonoTest
{
    internal class Program
    {
        static int Main(string[] args)
        {
            Console.WriteLine("Hello, Mono!");
            return 0;
        }
    }
}
```

这个程序的主方法会打印一行 "Hello, Mono!"，返回 0。

由于仅仅是为了测试，我们生成程序集 (此处是 exe 文件)，并将程序集拷贝到合适的位置，以供后续加载。

然后我们在引擎内部尝试加载这个程序集。

我们在我们之前初始化的 AppDomain 中加载程序集：

```cpp
MonoAssembly* assembly = mono_domain_assembly_open(domain, "MonoTest.exe");
if (!assembly)
{
    // Handle error
}
```

#### 添加内部调用 (Internal Call)

接下来我们添加一个内部调用，以供后续 C# 层面绑定。

我们创建一个静态方法 Hello：

```cpp
// internal call test function
static void Hello(MonoString* name)
{
    std::cout << "Hello, " << mono_string_to_utf8(name) << "!" << std::endl;
}
```

然后添加内部调用：

```cpp
mono_add_internal_call("SomeNameSpace.SomeClass::Hello", reinterpret_cast<void*>(&Hello));
```

这样，C# 那边就可以声明一个外部方法来与之绑定了。

#### C# 调用 C++

我们需要根据内部调用所定义的命名空间名称、类型名称、方法名称来一一匹配，声明一个外部方法。我们在 MonoTest 项目中创建一个 InternalCall.cs：

```csharp
using System.Runtime.CompilerServices;

namespace SomeNameSpace
{
    class SomeClass
    {
        [MethodImpl(MethodImplOptions.InternalCall)]
        public static extern void Hello(string name);
    }
}
```

到这里，Hello 方法就完成了绑定。我们在 Main 方法中调用这个外部方法：

```csharp
using System;

namespace MonoTest
{
    internal class Program
    {
        static int Main(string[] args)
        {
            Console.WriteLine("Hello, Mono!");

            // Invoke an external method
            SomeNameSpace.SomeClass.Hello("Game Engine Developer");
            return 0;
        }
    }
}
```

#### C++ 调用 C#

当然，我们最后希望在 C++ 层面调用 Main 方法，我们可以这样实现：

```cpp
void*       args[1];
args[0]                  = mono_array_new(domain, mono_get_string_class(), 0);
MonoClass* programClass = mono_class_from_name(image, "MonoTest", "Program");
MonoMethod* mainMethod   = mono_class_get_method_from_name(programClass, "Main", 1);
MonoObject* result       = mono_runtime_invoke(mainMethod, nullptr, args, nullptr);
int         resultCode   = *static_cast<int*>(mono_object_unbox(result));
```

这个代码片段，首先使用 `mono_array_new` 定义了一个空字符串数组，作为 Main 方法的参数。

然后使用 `mono_class_from_name` 通过命名空间名称、类型名称找到对应的类型，在 Mono 中对应 MonoClass*。

然后使用 `mono_class_get_method_from_name` 根据方法名称和参数个数，找到对应的方法，在 Mono 中对应 MonoMethod*。

最后，使用 `mono_runtime_invoke` 调用找到的方法，传入之前创建的空字符串数组作为参数，返回一个 MonoObject*。如果该方法没有返回值，则此处返回 nullptr。

当然，我们实现的 Main 方法返回 0，我们需要对 MonoObject 进行拆箱，得到实际返回的 int 值。

这是一个比较典型的调用方法的例子。除了这种调用方式，Mono 还提供了其他非常多的方式，API 众多，这里不多提及。

最终执行效果：

```text
Hello, Mono!
Hello, Game Engine Developer!
```

### 引擎内部封装

由于 Mono 提供的是面向过程的 C API，接下来只需要根据引擎的项目结构，对 Mono 相关结构和函数进行基于 C++ 的 OOP 封装，自己设计并实现脚本的生命周期，实现事件/消息系统，实现一套运行时反射系统等等。

### 更多

MacOS 和 Linux 平台上 Mono 的内嵌步骤与 Windows 平台实际上大同小异。

下一篇脚本系统相关的内容应该就是在引擎中内嵌 .NET 8.0 (LTS) 了，请耐心等候。

## 相关引用

- Mono Embedding for Game Engines, Peter Nilsson, <http://nilssondev.com/mono-guide/book/>
- Compiling Mono on Windows, mono-project.com, <https://www.mono-project.com/docs/compiling-mono/windows/>
- Embedding Mono, mono-project.com, <https://www.mono-project.com/docs/advanced/embedding/>

## 扩展阅读

- [Porting the Unity Engine to .NET CoreCLR | xoofx](https://xoofx.com/blog/2018/04/06/porting-unity-to-coreclr/)
- [runtime/native-hosting.md at main · dotnet/runtime](https://github.com/dotnet/runtime/blob/main/docs/design/features/native-hosting.md)
- [Interop with Native Libraries | Mono](https://www.mono-project.com/docs/advanced/pinvoke/)
- [FlaxEngine/Source/Engine/Scripting at master · FlaxEngine/FlaxEngine](https://github.com/FlaxEngine/FlaxEngine/tree/master/Source/Engine/Scripting)
