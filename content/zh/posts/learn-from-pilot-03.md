---
title: '从 Pilot 引擎学知识(3)-CMake 在 Pilot 中的作用(上)'
date: 2022-05-12T19:47:40
tags: [Pilot, GAMES104]
categories: [游戏引擎]
toc: true
---

![](/img/markdown_20220512101936.png)

接下来分析一下 CMake 在 Pilot 引擎中的作用。

<!--more-->

# CMake 在 Pilot 中的作用(上)

为什么过了这么久我才更新呢，因为最近 Pilot 更新得比较频繁，一开始的 CMakeLists.txt 也过于繁琐，不够直观。目前版本的 CMakeLists.txt 经过多次修改后，已经很简单很直观了，让我们开始分析吧！

> 写博客时，采用的 Pilot 版本为：https://github.com/BoomingTech/Pilot/commit/83db9024c13a1882f95370d87ddda0a6063b643a

## 什么是 CMake？

大家可能或多或少了解过 make 以及 Makefile。Makefile 可以描述编译所使用的编译器、链接库、链接规则、编译标志、编译依赖规则等等。make 程序则是根据 makefile 的描述，执行命令，完成编译工作。

CMake 则是根据 CMakeLists.txt 文件中描述的内容，生成项目文件，包括但不限于 Visual Studio 项目文件、Ninja 项目文件、Unix Makefiles 项目文件、MinGW Makefiles 项目文件等等。具体生成什么项目文件，可以通过命令行参数(-G) 指定，即指定 CMake 使用的 Generator(生成器)：

![](/img/markdown_20220512104932.png)

也就是说，CMake 实际上是一个<项目文件生成工具>，CMakeLists.txt 是一个项目生成规则描述文件(配置文件)，CMake 通过 CMakeLists.txt 的描述来生成项目文件。

## 逐语句分析 Pilot 根目录的 CMakeLists.txt

![](/img/markdown_20220512101936.png)

蓝色高亮的内容叫做 CMake 命令，小括号里面的内容叫做命令参数。我们一句一句来分析命令及参数的含义。

```cmake
cmake_minimum_required(VERSION 3.19 FATAL_ERROR)
```

这一句的含义是：指定运行时 cmake 的最小版本需求为 3.19，否则会报错。关于 cmake_minimum_required 命令，[点我了解更多](https://cmake.org/cmake/help/latest/command/cmake_minimum_required.html)

```cmake
project(Pilot VERSION 0.1.0)
```

这一句的含义是：指定项目名称为 Pilot，版本号为 0.1.0。关于 project 命令，[点我了解更多](https://cmake.org/cmake/help/latest/command/project.html)

```cmake
set(CMAKE_CXX_STANDARD 17)
```

这一句的含义是：指定项目采用的 C++ 标准为 C++17。

`set` 命令用于设置变量(包括普通变量、缓存变量、环境变量)，`CMAKE_CXX_STANDARD` 则是 CMake 内建变量。关于 set 命令，[点我了解更多](https://cmake.org/cmake/help/latest/command/set.html)

```cmake
set(CMAKE_CXX_STANDARD_REQUIRED ON)
```

这一句的含义是：指定项目需要指定 C++ 标准。

```cmake
set(BUILD_SHARED_LIBS OFF)
```

这一句的含义是：指定 `BUILD_SHARED_LIBS` 变量为 OFF，这个变量并不是 CMake 内建变量，所以是 CMake 子目录中的 CMakeLists.txt 中需要的变量，后面会提及。

```cmake
include(CMakeDependentOption)
```

这一句的含义是：包含 CMake 内建的 cmake_dependent_option 函数，这个函数后面会使用到，[点我了解更多](https://cmake.org/cmake/help/latest/module/CMakeDependentOption.html)

```cmake
# ---- Include guards ----
if(PROJECT_SOURCE_DIR STREQUAL PROJECT_BINARY_DIR)
  message(
    FATAL_ERROR
      "In-source builds not allowed. Please make a new directory (called a build directory) and run CMake from there."
  )
endif()
```

这一段的含义是：如果项目的源目录和项目的二进制目录相同(字符串相等)，则发送一条报错消息，提示你不允许在 source 里 build，你需要创建一个新的文件夹例如 build 文件夹，在里面运行 cmake 指令。需要注意的是，CMake 中，if 需要和 endif 相匹配，有始有终。STREQUAL 用于比较两边的字符串是否相等。

```cmake
set(PILOT_ROOT_DIR "${CMAKE_CURRENT_SOURCE_DIR}")
```

这一句的含义是：设置 `PILOT_ROOT_DIR` 变量的值为 `CMAKE_CURRENT_SOURCE_DIR` 的值。${变量名}即为取变量的值。`CMAKE_CURRENT_SOURCE_DIR` 为 CMake 内建变量，指当前 CMakeLists.txt 所在目录，所以这里是设置 Pilot 的根目录为当前 CMakeLists.txt 所在目录。

```cmake
set(CMAKE_INSTALL_PREFIX "${PILOT_ROOT_DIR}/bin")
```

这一句的含义是：设置 `CMAKE_INSTALL_PREFIX` 变量的值为当前根目录下的 bin 目录。`CMAKE_INSTALL_PREFIX` 变量为 CMake 内建变量，指项目的安装路径前缀，即最后的二进制文件要安装到的位置，这里设置为了 Pilot 根目录下的 bin 目录。

```cmake
set(BINARY_ROOT_DIR "${CMAKE_INSTALL_PREFIX}/")
```

这一句的含义是：设置 `BINARY_ROOT_DIR` 变量的值为 `CMAKE_INSTALL_PREFIX` 的值加一个路径分隔符。实际上就是设置二进制文件的根目录为安装路径前缀对应的目录，默认设置是 Pilot 根目录下的 bin 目录。

```cmake
add_subdirectory(engine)
```

这一句的含义是：添加一个子目录，目录名为 engine。注意，cmake 会进入添加的子目录(这里是 engine 目录) 继续寻找 CMakeLists.txt 并执行。所以我们接下来分析 engine 目录下的 CMakeLists.txt

## 逐语句分析 engine 目录的 CMakeLists.txt

![](/img/markdown_20220512144653.png)

```cmake
set(ENGINE_ROOT_DIR "${PILOT_ROOT_DIR}/engine")
```

这一句的含义是：设置 `ENGINE_ROOT_DIR` 变量的值为 `PILOT_ROOT_DIR` 的值加上 `/engine`，实际上就是将<引擎根目录>设置为根目录下的 engine 目录。

```cmake
set(THIRD_PARTY_DIR "${ENGINE_ROOT_DIR}/3rdparty")
```

这一句的含义是：设置 `THIRD_PARTY_DIR` 变量的值为 `ENGINE_ROOT_DIR` 的值加上 `/3rdparty`，实际上就是将<第三方库目录>设置为<引擎根目录>下的 3rdparty 目录。

```cmake
set(ENGINE_ASSET_DIR "/asset")
```

这一句的含义是：设置 `ENGINE_ASSET_DIR` 变量的值为相对路径 `/asset`。实际上，我觉得如果要统一规范的话，这一句应该改为：`set(ENGINE_ASSET_DIR "${ENGINE_ROOT_DIR}/asset")`。实际上就是将<引擎资产目录>设置为<引擎根目录>下的 asset 目录。

```cmake
set(ENGINE_SCHEMA_DIR "/schema")
```

这一句的含义是：设置 `ENGINE_SCHEMA_DIR` 变量的值为相对路径 `/schema`。实际上，我觉得如果要统一规范的话，这一句应该改为：`set(ENGINE_SCHEMA_DIR"${ENGINE_ROOT_DIR}/schema")`。实际上就是将<引擎架构目录>设置为<引擎根目录>下的 schema 目录。

```cmake
if(MSVC)
    add_compile_options("/MP")
    set_property(DIRECTORY ${CMAKE_SOURCE_DIR} PROPERTY VS_STARTUP_PROJECT PilotEditor)
endif()
```

这一段的含义是：如果采用微软的 MSVC 编译器(使用 Visual Studio 编译)，则添加编译选项 `/MP`，并且设置 VS 的启动项目为 PilotEditor。`/MP` 代表使用多进程生成，[点我了解更多](https://docs.microsoft.com/zh-cn/cpp/build/reference/mp-build-with-multiple-processes?view=msvc-170)

```cmake
set(vulkan_include ${THIRD_PARTY_DIR}/VulkanSDK/include)
```

这一句的含义是：设置 `vulkan_include` 变量的值为 `THIRD_PARTY_DIR` 的值加上 `/VulkanSDK/include`，实际上就是将<Vulkan的包含目录>设置为<第三方库目录>/VulkanSDK/include。

```cmake
if(WIN32)
    set(vulkan_lib ${THIRD_PARTY_DIR}/VulkanSDK/lib/Win32/vulkan-1.lib)
    set(glslangValidator_executable ${THIRD_PARTY_DIR}/VulkanSDK/bin/Win32/glslangValidator.exe)
    add_compile_definitions("PILOT_VK_LAYER_PATH=${THIRD_PARTY_DIR}/VulkanSDK/bin/Win32")
elseif(UNIX)
    if(APPLE)
      set(vulkan_lib ${THIRD_PARTY_DIR}/VulkanSDK/lib/MacOS/libvulkan.1.dylib)
      set(glslangValidator_executable ${THIRD_PARTY_DIR}/VulkanSDK/bin/MacOS/glslangValidator)
      add_compile_definitions("PILOT_VK_LAYER_PATH=${THIRD_PARTY_DIR}/VulkanSDK/bin/MacOS")
      add_compile_definitions("PILOT_VK_ICD_FILENAMES=${THIRD_PARTY_DIR}/VulkanSDK/bin/MacOS/MoltenVK_icd.json")
    else()
      set(vulkan_lib ${THIRD_PARTY_DIR}/VulkanSDK/lib/Linux/libvulkan.so.1)
      set(glslangValidator_executable ${THIRD_PARTY_DIR}/VulkanSDK/bin/Linux/glslangValidator)
      add_compile_definitions("PILOT_VK_LAYER_PATH=${THIRD_PARTY_DIR}/VulkanSDK/bin/Linux")
    endif()
else()
  message(FATAL_ERROR "Unknown Platform")
endif()
```

这一段很长，我们详细分析一下：

如果运行 cmake 时，使用的是 Windows 环境，那么：

- 设置 `vulkan_lib` 变量的值为 `THIRD_PARTY_DIR` 的值加上 `/VulkanSDK/lib/Win32/vulkan-1.lib`。实际上就是将<Vulkan的库路径>设置为<第三方库目录>/VulkanSDK/lib/Win32/vulkan-1.lib。
- 设置 `glslangValidator_executable` 变量的值为 `THIRD_PARTY_DIR` 的值加上 `/VulkanSDK/bin/Win32/glslangValidator.exe`。实际上就是将<GLSL语言验证器可执行程序路径>设置为<第三方库目录>/VulkanSDK/bin/Win32/glslangValidator.exe。

否则，如果使用的是 Unix 环境，那么：

- 如果使用的是苹果系统(MacOS)：

  - 设置 `vulkan_lib` 变量的值为 `THIRD_PARTY_DIR` 的值加上 `/VulkanSDK/lib/MacOS/libvulkan.1.dylib`。实际上就是将<Vulkan的库路径>设置为<第三方库目录>/VulkanSDK/lib/MacOS/libvulkan.1.dylib。
  - 设置 `glslangValidator_executable` 变量的值为 `THIRD_PARTY_DIR` 的值加上 `/VulkanSDK/bin/MacOS/glslangValidator`。实际上就是将<GLSL语言验证器可执行程序路径>设置为<第三方库目录>/VulkanSDK/bin/MacOS/glslangValidator。
  - 添加编译定义：`PILOT_VK_LAYER_PATH=${THIRD_PARTY_DIR}/VulkanSDK/bin/MacOS`
  - 添加编译定义：`PILOT_VK_ICD_FILENAMES=${THIRD_PARTY_DIR}/VulkanSDK/bin/MacOS/MoltenVK_icd.json`
- 否则(其他 Unix/Linux 系统)：
  - 设置 `vulkan_lib` 变量的值为 `THIRD_PARTY_DIR` 的值加上 `/VulkanSDK/lib/Linux/libvulkan.so.1`。实际上就是将<Vulkan的库路径>设置为<第三方库目录>/VulkanSDK/lib/Linux/libvulkan.so.1。
  - 设置 `glslangValidator_executable` 变量的值为 `THIRD_PARTY_DIR` 的值加上 `/VulkanSDK/bin/Linux/glslangValidator`。实际上就是将<GLSL语言验证器可执行程序路径>设置为<第三方库目录>/VulkanSDK/bin/Linux/glslangValidator。
  - 添加编译定义：`PILOT_VK_LAYER_PATH=${THIRD_PARTY_DIR}/VulkanSDK/bin/Linux`

否则，运行的是不支持的平台，打印报错。

```cmake
set(SHADER_COMPILE_TARGET PilotShaderCompile)
```

这一句的含义是：设置 `SHADER_COMPILE_TARGET` 变量的值为 `PilotShaderCompile`，这个值代表 Target 的名字，后面会用到。

```cmake
add_subdirectory(shader)
add_subdirectory(3rdparty)
add_subdirectory(source/runtime)
add_subdirectory(source/editor)
```

然后接下来四句都是添加子目录。添加了 shader、3rdparty、source/runtime、source/editor 四个子目录，我们下次还要分析一下它们。

```cmake
set(CODEGEN_TARGET "PilotPreCompile")
include(source/precompile/precompile.cmake)
set_target_properties("${CODEGEN_TARGET}" PROPERTIES FOLDER "Engine" )
add_dependencies(PilotRuntime "${CODEGEN_TARGET}")
```

最后四句，设置 `CODEGEN_TARGET` 变量为 `PilotPreCompile`；包含 source/precompile/precompile.cmake 文件，这样就可以使用该文件中定义的函数；设置目标 `CODEGEN_TARGET`(即 PilotPreCompile) 的属性，文件夹为 `Engine`；添加依赖：PilotRuntime 依赖于 `CODEGEN_TARGET`(PilotPreCompile)。

## 小结

在 Pilot 中，CMake 实现了跨平台的项目文件生成，方便大家在不同的平台，使用 CMake 得到自己想要的项目文件，进而调试、编译、发布。

下一次，我们继续分析 shader、3rdparty、source/runtime、source/editor 四个子目录中的 CMakeLists.txt，看看 Pilot 是如果利用 CMake 完成项目文件生成的。



