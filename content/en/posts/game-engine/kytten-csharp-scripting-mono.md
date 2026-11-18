---
title: "Kytten's C# Scripting System: Mono"
date: 2023-05-17T15:45:00
categories: [Game Engines]
tags: [Kytten, Scripting, Mono, CSharp, DotNET]
toc: true
original: true
zhihu: 630199985
aiTranslated: true
---

> Reposted from my Zhihu column: [Kytten 的 C# 脚本系统：Mono 篇](https://zhuanlan.zhihu.com/p/630199985) (published 2023-05-17); formatting tidied during migration.

> [!NOTE]
> The Kytten engine is no longer being developed, but it did exist. It laid the groundwork for the later [Snow Leopard Engine](https://github.com/SnowLeopardEngine/SnowLeopardEngine) (a Leeds MSc team project) and [libvultra](https://github.com/zzxzzk115/libvultra). The roadmap and the "coming later" plans in this post won't be continued.

Kytten's C# scripting system is under development, and some of the technology is still being researched and tested.

<!--more-->

## C# Scripting System Overview

### What Is a C# Scripting System?

A C# scripting system means embedding a managed C# runtime inside the engine's unmanaged layer, so that unmanaged code and managed C# code can call each other.

### Why Do Game Engines Usually Need a C# Scripting System?

Because C# is easier to learn and understand than lower-level languages (C/C++/Rust). If developers write scripts in C#, it's easier to get started, the learning cost is lower, and development is more efficient.

Another reason is that C# has a better ecosystem. Behind C# is .NET, and .NET has a huge ecosystem. In the future, .NET will become a truly unified platform, and at that point C# will be the greatest of all time.

## Mono VS CoreCLR

### Mono

Mono is an open-source project started by Xamarin. Since .NET Framework only supported Windows, Mono was created to fill the gap. Its goal is to provide a cross-platform runtime that implements the same ECMA specifications as .NET Framework and is compatible with most .NET Framework code, so that C# can be used to write applications and libraries for mainstream desktop and mobile platforms. Microsoft later acquired Xamarin. Today there are two versions of Mono: one is still maintained by the original Mono team, and the other is maintained by Microsoft itself. Their features differ. The former is more general-purpose and is a commonly used third-party library for game engine scripting systems; the latter has mainly been made more compatible with and optimized for Microsoft's own products, and isn't a good fit for embedding in a game engine.

{{< linkcard url="https://github.com/mono/mono" title="GitHub - mono/mono: Mono open source ECMA CLI, C# and .NET implementation." desc="Mono open source ECMA CLI, C# and .NET implementation. - mono/mono" site="GitHub" image="/img/linkcards/github-com-mono-mono-e59a5f.png" >}}

{{< linkcard url="https://github.com/dotnet/runtime/tree/main/src/mono" title="runtime/src/mono at main · dotnet/runtime" desc=".NET is a cross-platform runtime for cloud, mobile, desktop, and IoT apps. - dotnet/runtime" site="GitHub" image="/img/linkcards/github-com-dotnet-runtime-tree-main-src-mono-b10440.png" >}}

### CoreCLR

CoreCLR is also an open-source project, started by Microsoft. Given that .NET Framework was not cross-platform, not open source and couldn't benefit from community support, Microsoft decided to develop a brand-new, open-source, cross-platform common language runtime — CoreCLR. It is based on the .NET Framework CLR, but its platform-specific implementation was rewritten, the GC was upgraded and optimized, and the performance of core features such as multithreading and tasks was improved. Most importantly, it is cross-platform. For now, though, CoreCLR only supports mainstream desktop platforms; for mobile platforms, Microsoft is still using Mono for the time being.

{{< linkcard url="https://github.com/dotnet/runtime" title="GitHub - dotnet/runtime: .NET is a cross-platform runtime for cloud, mobile, desktop, and IoT apps." desc=".NET is a cross-platform runtime for cloud, mobile, desktop, and IoT apps. - dotnet/runtime" site="GitHub" image="/img/linkcards/github-com-dotnet-runtime-d8611a.png" >}}

### Pros and Cons of Mono and CoreCLR

Mono's advantages are that it supports more platforms than CoreCLR and is easier to embed. Why easier? Because its binding mechanisms are more flexible. It supports two binding mechanisms:

- P/Invoke (Platform Invoke)
- The Mono embedding API

P/Invoke involves a lot more around the DLLImport attribute (the newest is the [LibraryImport attribute](https://learn.microsoft.com/en-us/dotnet/standard/native-interop/pinvoke-source-generation)), calling conventions and marshaling. It's comparatively more complex and error-prone — if anything goes wrong in any one of those pieces, the binding fails. If we use Mono, we usually don't use P/Invoke for embedding.

The Mono embedding API, on the other hand, lets you add an internal call on the C++ side and then declare it as an external method on the C# side; as long as the namespace, class name and method name all match, the binding is done. Marshaling is also more convenient. Take strings as an example: with P/Invoke you need to specify how the string is marshaled, its encoding and so on. With the Mono embedding API, MonoString solves string marshaling nicely, and Mono provides plenty of convenient APIs for it.

| C Type | Mono Type | C to Mono | Mono to C |
|---|---|---|---|
| strings, char * | MonoString * | mono_string_new, mono_string_new_len, mono_string_new_wrapper, mono_string_new_utf16 | mono_string_to_utf8, mono_string_to_utf16 |

CoreCLR's advantages are higher performance and a newer C# version. Its GC performs much better than Mono's GC, and it offers more modern features, such as Span and Memory — structures created to improve performance — along with more performance-optimized components, and it supports the latest C# version (currently 11). However, CoreCLR currently only supports binding code via P/Invoke, which makes embedding it in a game engine more complicated. We need to load hostfxr on the C++ side so that the game engine becomes CoreCLR's host, which lets us call managed C# code. But for C# calling C++ code, we still have to go through P/Invoke.

{{< linkcard url="https://learn.microsoft.com/en-us/dotnet/core/tutorials/netcore-hosting" title="Write a custom .NET runtime host - .NET" desc="Learn to host the .NET runtime from native code to support advanced scenarios that require controlling how the .NET runtime works." image="/img/linkcards/learn-microsoft-com-en-us-dotnet-core-tutorials--442310.png" >}}

### Kytten Roadmap

On the Kytten 0.1.0 roadmap, we plan to embed Mono in the engine as one of the core foundations of the scripting system. That's the simplest way to get C# scripting working, though the supported C# version will be somewhat older and performance will be somewhat worse.

In the future, we plan to embed .NET 8.0 (LTS) in the engine as another core foundation of the scripting system. .NET's CoreCLR will bring a huge performance boost to the scripting system, along with the new features of the latest C# language version.

> If CoreCLR provides an embedding API in the future, binding will become much more convenient. I hope Microsoft will offer these APIs down the line.

If the C# scripting system has two different runtime options, switched on and off via compiler macros, then we'll also need to write a binding code generator, or use Source Generators, to generate the appropriate binding code (using Internal Calls or using DLLImport / LibraryImport) depending on the chosen runtime (Mono or CoreCLR).

## Embedding Mono in a Game Engine (Windows as an Example)

Embedding Mono in a game engine is fairly easy, because Mono already provides an embedding API that we can use directly. Before actually embedding Mono, we need to build or install Mono to get the necessary files.

Building Mono takes a while, so simply installing it is generally a good choice. However, once you need to change some of Mono's logic to implement new features, you'll have to build your own modified Mono.

### How Embedding Mono Works

Put simply, the C/C++ side hosts a Mono runtime, and within that runtime we initialize an AppDomain, load assemblies and so on.

{{< linkcard url="https://www.mono-project.com/docs/advanced/embedding/#how-embedding-works" title="Embedding Mono | Mono" >}}

### Building Mono and Getting the Necessary Files

> Tip: depending on your network (e.g. in mainland China), you may need a VPN or proxy to reach GitHub and other sites, and the process takes quite a long time. You need a Visual Studio environment with the Desktop development with C++ workload installed.

#### Enable Windows Developer Mode

`Settings → Update & Security → For developers → Developer Mode → On`

#### Download Cygwin and Install the Dependencies

Click [here to download](http://www.cygwin.com/setup-x86_64.exe).

After downloading, run the following command from CMD in the download directory to install:

```batch
setup-x86_64.exe -P autoconf,automake,bison,gcc-core,gcc-g++,mingw64-i686-runtime,mingw64-i686-binutils,mingw64-i686-gcc-core,mingw64-i686-gcc-g++,mingw64-i686-pthreads,mingw64-i686-w32api,mingw64-x86_64-runtime,mingw64-x86_64-binutils,mingw64-x86_64-gcc-core,mingw64-x86_64-gcc-g++,mingw64-x86_64-pthreads,mingw64-x86_64-w32api,libtool,make,python,gettext-devel,gettext,intltool,libiconv,pkg-config,git,curl,wget,libxslt,bc,patch,cmake,perl,yasm,unzip
```

> If libusb0 fails to install, you can ignore it for now and just click Next.

#### Build Mono

Opening Cygwin drops you into a command-line window.

Run the following commands to clone the Mono repository, check out the latest release tag, and set the install path to the install folder in the Mono source root:

```bash
cd ~
git clone https://github.com/mono/mono.git # Or your own mono git repo
cd mono
git checkout 73df89a # The latest released tag's commit hash
export PREFIX=~/mono/install
export PATH=$PREFIX/bin:$PATH
```

The mono repository is now cloned. In File Explorer, open `<Cygwin root>/home/[username]/mono`, go into the `msvc` folder, double-click `mono.sln` to open the solution, and build it. You can choose Debug / Release + x64 / Win32 and build whichever you need. The purpose of this step is to get static library files that MSVC supports.

> libtest may fail to build (newline in constant). That's fine — it's probably an encoding issue in the test cases or the code page, and as long as it doesn't affect the other core libraries, it doesn't matter.

Build and install the 64-bit version of Mono:

```bash
./autogen.sh --prefix=$PREFIX --host=x86_64-w64-mingw32 --disable-boehm
make get-monolite-latest
make -j8
make install
```

Build and install the 32-bit version of Mono:

```bash
./autogen.sh --prefix=$PREFIX --host=i686-w64-mingw32 --disable-boehm
make get-monolite-latest
make -j8
make install
```

#### Get the Necessary Files

The files we need are:

- Static library files
- Header files
- Configuration files
- The runtime DLL set

The static library files are in `msvc/build/`. For example, if I chose Debug + x64 as the build configuration in `mono.sln`, then the static library I need is `libmono-static-sgen.lib` in `msvc/build/sgen/x64/lib/Debug/`.

The header files are in `msvc/include/`; the `mono` folder contains all the headers we need.

The configuration files are in `install/etc/`; the `mono` folder contains all the configuration files we need.

The runtime DLL set is in `install/lib/mono/`. Usually we only need the `4.5` folder from it, and within that folder we only care about the assembly files with the .dll extension; we don't need the other files.

### Installing Mono and Getting the Necessary Files

#### Download and Install Mono

Go to the [official Mono website](https://www.mono-project.com/download/stable/) and download the latest stable release, choosing 32-bit or 64-bit as needed.

After downloading, just run the installer.

#### Get the Necessary Files

The files we need are:

- Static library files
- Header files
- Configuration files
- The runtime DLL set

Everything is relative to the Mono installation directory. The default installation directory for 64-bit Mono is `C:\Program Files\Mono`. From here on, the Mono installation directory is referred to as `%MONO_DIR%`.

The static library file is `libmono-static-sgen.lib` in `%MONO_DIR%/lib/`.

The header files are in `%MONO_DIR%/include/mono-2.0/`; the `mono` folder contains all the headers we need.

The configuration files are in `%MONO_DIR%/etc/`; the `mono` folder contains all the configuration files we need.

The runtime DLL set is in `%MONO_DIR%/lib/mono/`. Usually we only need the `4.5` folder from it, and within that folder we only care about the assembly files with the .dll extension; we don't need the other files.

### Project Setup

#### Add Static Linking

Link `libmono-static-sgen.lib` according to your engine's project structure. On Windows, linking it alone produces link errors; you also need to link the following libraries:

- Mswsock.lib
- ws2_32.lib
- psapi.lib
- version.lib
- winmm.lib
- Bcrypt.lib

Kytten is currently built with CMake. Below is part of Kytten's CMake code for linking the Mono static library, with the Linux and MacOS parts omitted:

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

### Key Steps

#### Include the Headers

```cpp
#include <mono/jit/jit.h>
#include <mono/metadata/assembly.h>
#include <mono/metadata/mono-config.h>
```

#### Set Mono's Paths and Configuration

Mono lets you specify the .NET runtime library path and the configuration path. If you don't, it will try to find them in the common installation directories by default; if it ultimately can't find them, initializing the AppDomain later will fail with an error.

```cpp
mono_set_dirs("lib/mono/lib", "lib/mono/etc");
```

In addition, we need to parse the config file to initialize the DLL mappings; otherwise DLLs may not be found on MacOS and Linux.

```cpp
mono_config_parse("lib/mono/etc/mono/config");
```

#### Initialize the AppDomain

An AppDomain is mainly used to isolate applications. For a game engine, creating a single AppDomain is generally enough.

```cpp
MonoDomain* domain = mono_jit_init("KyttenEngineScripting");
```

The code above creates an AppDomain named "KyttenEngineScripting".

#### Load an Assembly

First, we create a .NET Framework console application named MonoTest and write Program.cs:

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

This program's Main method prints "Hello, Mono!" and returns 0.

Since this is just a test, we build the assembly (an exe file in this case) and copy it to a suitable location so it can be loaded later.

Then we try to load this assembly from inside the engine.

We load the assembly in the AppDomain we initialized earlier:

```cpp
MonoAssembly* assembly = mono_domain_assembly_open(domain, "MonoTest.exe");
if (!assembly)
{
    // Handle error
}
```

#### Add an Internal Call

Next, we add an internal call for the C# side to bind to later.

We create a static method Hello:

```cpp
// internal call test function
static void Hello(MonoString* name)
{
    std::cout << "Hello, " << mono_string_to_utf8(name) << "!" << std::endl;
}
```

Then we add the internal call:

```cpp
mono_add_internal_call("SomeNameSpace.SomeClass::Hello", reinterpret_cast<void*>(&Hello));
```

Now the C# side can declare an external method to bind to it.

#### Calling C++ from C#

We need to declare an external method whose namespace name, type name and method name match those defined for the internal call. We create InternalCall.cs in the MonoTest project:

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

At this point, the Hello method is bound. We call this external method from Main:

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

#### Calling C# from C++

Of course, in the end we want to call the Main method from the C++ side. We can do it like this:

```cpp
void*       args[1];
args[0]                  = mono_array_new(domain, mono_get_string_class(), 0);
MonoClass* programClass = mono_class_from_name(image, "MonoTest", "Program");
MonoMethod* mainMethod   = mono_class_get_method_from_name(programClass, "Main", 1);
MonoObject* result       = mono_runtime_invoke(mainMethod, nullptr, args, nullptr);
int         resultCode   = *static_cast<int*>(mono_object_unbox(result));
```

This snippet first uses `mono_array_new` to define an empty string array as the argument to Main.

It then uses `mono_class_from_name` to find the type by namespace name and type name, which corresponds to a MonoClass* in Mono.

Next, it uses `mono_class_get_method_from_name` to find the method by method name and parameter count, which corresponds to a MonoMethod* in Mono.

Finally, it uses `mono_runtime_invoke` to call the method it found, passing in the empty string array created earlier as the argument, and gets back a MonoObject*. If the method has no return value, this returns nullptr.

Our Main method returns 0, of course, so we need to unbox the MonoObject to get the actual int value returned.

This is a fairly typical example of invoking a method. Besides this approach, Mono provides many other ways to do it with a large number of APIs, which I won't go into here.

Final output:

```text
Hello, Mono!
Hello, Game Engine Developer!
```

### Wrapping It Inside the Engine

Since Mono provides a procedural C API, what's left is to wrap Mono's structures and functions in a C++ OOP layer according to the engine's project structure, design and implement the script lifecycle yourself, implement an event/messaging system, implement a runtime reflection system and so on.

### More

The steps for embedding Mono on MacOS and Linux are actually much the same as on Windows.

The next post on the scripting system should be about embedding .NET 8.0 (LTS) in the engine — stay tuned.

## References

- Mono Embedding for Game Engines, Peter Nilsson, <http://nilssondev.com/mono-guide/book/>
- Compiling Mono on Windows, mono-project.com, <https://www.mono-project.com/docs/compiling-mono/windows/>
- Embedding Mono, mono-project.com, <https://www.mono-project.com/docs/advanced/embedding/>

## Further Reading

{{< linkcard url="https://xoofx.com/blog/2018/04/06/porting-unity-to-coreclr/" title="Porting the Unity Engine to .NET CoreCLR | xoofx" >}}

{{< linkcard url="https://github.com/dotnet/runtime/blob/main/docs/design/features/native-hosting.md" title="runtime/docs/design/features/native-hosting.md at main · dotnet/runtime" desc=".NET is a cross-platform runtime for cloud, mobile, desktop, and IoT apps. - dotnet/runtime" site="GitHub" image="/img/linkcards/github-com-dotnet-runtime-blob-main-docs-design--c7b068.png" >}}

{{< linkcard url="https://www.mono-project.com/docs/advanced/pinvoke/" title="Interop with Native Libraries | Mono" >}}

{{< linkcard url="https://github.com/FlaxEngine/FlaxEngine/tree/master/Source/Engine/Scripting" title="FlaxEngine/Source/Engine/Scripting at master · FlaxEngine/FlaxEngine" desc="Flax Engine – multi-platform 3D game engine. Contribute to FlaxEngine/FlaxEngine development by creating an account on GitHub." site="GitHub" image="/img/linkcards/github-com-flaxengine-flaxengine-tree-master-sou-80b01a.png" >}}
