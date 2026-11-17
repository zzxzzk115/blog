---
title: 'Learning from the Pilot Engine (3): The Role of CMake in Pilot (Part 1)'
date: 2022-05-12T19:47:40
tags: [Pilot, GAMES104]
categories: [Game Engines]
toc: true
aiTranslated: true
---

![](/img/markdown_20220512101936.png)

Next, let's analyze the role CMake plays in the Pilot engine.

<!--more-->

# The Role of CMake in Pilot (Part 1)

Why did it take me so long to post this? Because Pilot has been updated pretty frequently lately, and the original CMakeLists.txt was too convoluted and not very intuitive. After many revisions, the current CMakeLists.txt is now very simple and intuitive, so let's start analyzing it!

> Pilot version used while writing this post: https://github.com/BoomingTech/Pilot/commit/83db9024c13a1882f95370d87ddda0a6063b643a

## What Is CMake?

You've probably heard of make and Makefiles to some extent. A Makefile can describe the compiler used for the build, the libraries to link, the linking rules, compile flags, build dependency rules, and so on. The make program then runs commands according to the Makefile's description to carry out the build.

CMake, on the other hand, generates project files based on what's described in CMakeLists.txt, including but not limited to Visual Studio project files, Ninja project files, Unix Makefiles project files, MinGW Makefiles project files, and so on. Which kind of project file it generates can be specified with a command-line argument (-G), i.e. specifying the Generator CMake uses:

![](/img/markdown_20220512104932.png)

In other words, CMake is really a <project file generation tool>, and CMakeLists.txt is a file describing the project generation rules (a config file). CMake generates project files from the description in CMakeLists.txt.

## Line-by-Line Analysis of Pilot's Root CMakeLists.txt

![](/img/markdown_20220512101936.png)

The parts highlighted in blue are called CMake commands, and what's inside the parentheses are the command arguments. Let's go through the meaning of each command and its arguments one by one.

```cmake
cmake_minimum_required(VERSION 3.19 FATAL_ERROR)
```

This line means: the minimum required cmake version at runtime is 3.19, otherwise an error is raised. For more on the cmake_minimum_required command, [click here](https://cmake.org/cmake/help/latest/command/cmake_minimum_required.html)

```cmake
project(Pilot VERSION 0.1.0)
```

This line means: the project name is Pilot and the version is 0.1.0. For more on the project command, [click here](https://cmake.org/cmake/help/latest/command/project.html)

```cmake
set(CMAKE_CXX_STANDARD 17)
```

This line means: the project uses the C++17 standard.

The `set` command sets variables (including normal variables, cache variables and environment variables), and `CMAKE_CXX_STANDARD` is a built-in CMake variable. For more on the set command, [click here](https://cmake.org/cmake/help/latest/command/set.html)

```cmake
set(CMAKE_CXX_STANDARD_REQUIRED ON)
```

This line means: the project requires the specified C++ standard.

```cmake
set(BUILD_SHARED_LIBS OFF)
```

This line means: set the `BUILD_SHARED_LIBS` variable to OFF. This isn't a built-in CMake variable, so it's a variable needed by the CMakeLists.txt in a CMake subdirectory; more on that later.

```cmake
include(CMakeDependentOption)
```

This line means: include CMake's built-in cmake_dependent_option function, which will be used later. [Click here to learn more](https://cmake.org/cmake/help/latest/module/CMakeDependentOption.html)

```cmake
# ---- Include guards ----
if(PROJECT_SOURCE_DIR STREQUAL PROJECT_BINARY_DIR)
  message(
    FATAL_ERROR
      "In-source builds not allowed. Please make a new directory (called a build directory) and run CMake from there."
  )
endif()
```

This block means: if the project's source directory and binary directory are the same (the strings are equal), emit an error message telling you in-source builds aren't allowed, and that you need to create a new folder, e.g. a build folder, and run cmake from inside it. Note that in CMake, every if must be matched by an endif — what's opened must be closed. STREQUAL compares whether the strings on both sides are equal.

```cmake
set(PILOT_ROOT_DIR "${CMAKE_CURRENT_SOURCE_DIR}")
```

This line means: set the value of `PILOT_ROOT_DIR` to the value of `CMAKE_CURRENT_SOURCE_DIR`. ${variable name} gets a variable's value. `CMAKE_CURRENT_SOURCE_DIR` is a built-in CMake variable referring to the directory containing the current CMakeLists.txt, so this sets Pilot's root directory to the directory of the current CMakeLists.txt.

```cmake
set(CMAKE_INSTALL_PREFIX "${PILOT_ROOT_DIR}/bin")
```

This line means: set the value of `CMAKE_INSTALL_PREFIX` to the bin directory under the current root directory. `CMAKE_INSTALL_PREFIX` is a built-in CMake variable for the project's install path prefix, i.e. where the final binaries get installed; here it's set to the bin directory under Pilot's root.

```cmake
set(BINARY_ROOT_DIR "${CMAKE_INSTALL_PREFIX}/")
```

This line means: set the value of `BINARY_ROOT_DIR` to the value of `CMAKE_INSTALL_PREFIX` plus a path separator. Effectively, this sets the binaries' root directory to the directory of the install path prefix, which by default is the bin directory under Pilot's root.

```cmake
add_subdirectory(engine)
```

This line means: add a subdirectory named engine. Note that cmake will go into the added subdirectory (here, engine), look for a CMakeLists.txt there, and run it. So next we'll analyze the CMakeLists.txt in the engine directory.

## Line-by-Line Analysis of the engine Directory's CMakeLists.txt

![](/img/markdown_20220512144653.png)

```cmake
set(ENGINE_ROOT_DIR "${PILOT_ROOT_DIR}/engine")
```

This line means: set the value of `ENGINE_ROOT_DIR` to the value of `PILOT_ROOT_DIR` plus `/engine`. Effectively, this sets the <engine root directory> to the engine directory under the root.

```cmake
set(THIRD_PARTY_DIR "${ENGINE_ROOT_DIR}/3rdparty")
```

This line means: set the value of `THIRD_PARTY_DIR` to the value of `ENGINE_ROOT_DIR` plus `/3rdparty`. Effectively, this sets the <third-party library directory> to the 3rdparty directory under the <engine root directory>.

```cmake
set(ENGINE_ASSET_DIR "/asset")
```

This line means: set the value of `ENGINE_ASSET_DIR` to the relative path `/asset`. Actually, I think that for consistency this line should be changed to: `set(ENGINE_ASSET_DIR "${ENGINE_ROOT_DIR}/asset")`. Effectively, this sets the <engine asset directory> to the asset directory under the <engine root directory>.

```cmake
set(ENGINE_SCHEMA_DIR "/schema")
```

This line means: set the value of `ENGINE_SCHEMA_DIR` to the relative path `/schema`. Actually, I think that for consistency this line should be changed to: `set(ENGINE_SCHEMA_DIR"${ENGINE_ROOT_DIR}/schema")`. Effectively, this sets the <engine schema directory> to the schema directory under the <engine root directory>.

```cmake
if(MSVC)
    add_compile_options("/MP")
    set_property(DIRECTORY ${CMAKE_SOURCE_DIR} PROPERTY VS_STARTUP_PROJECT PilotEditor)
endif()
```

This block means: if Microsoft's MSVC compiler is used (building with Visual Studio), add the compile option `/MP` and set the VS startup project to PilotEditor. `/MP` means build with multiple processes. [Click here to learn more](https://docs.microsoft.com/zh-cn/cpp/build/reference/mp-build-with-multiple-processes?view=msvc-170)

```cmake
set(vulkan_include ${THIRD_PARTY_DIR}/VulkanSDK/include)
```

This line means: set the value of `vulkan_include` to the value of `THIRD_PARTY_DIR` plus `/VulkanSDK/include`. Effectively, this sets the <Vulkan include directory> to <third-party library directory>/VulkanSDK/include.

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

This block is long, so let's analyze it in detail:

If cmake is run in a Windows environment, then:

- Set the value of `vulkan_lib` to the value of `THIRD_PARTY_DIR` plus `/VulkanSDK/lib/Win32/vulkan-1.lib`. Effectively, this sets the <Vulkan library path> to <third-party library directory>/VulkanSDK/lib/Win32/vulkan-1.lib.
- Set the value of `glslangValidator_executable` to the value of `THIRD_PARTY_DIR` plus `/VulkanSDK/bin/Win32/glslangValidator.exe`. Effectively, this sets the <GLSL validator executable path> to <third-party library directory>/VulkanSDK/bin/Win32/glslangValidator.exe.

Otherwise, if it's a Unix environment, then:

- If it's Apple's system (MacOS):

  - Set the value of `vulkan_lib` to the value of `THIRD_PARTY_DIR` plus `/VulkanSDK/lib/MacOS/libvulkan.1.dylib`. Effectively, this sets the <Vulkan library path> to <third-party library directory>/VulkanSDK/lib/MacOS/libvulkan.1.dylib.
  - Set the value of `glslangValidator_executable` to the value of `THIRD_PARTY_DIR` plus `/VulkanSDK/bin/MacOS/glslangValidator`. Effectively, this sets the <GLSL validator executable path> to <third-party library directory>/VulkanSDK/bin/MacOS/glslangValidator.
  - Add the compile definition: `PILOT_VK_LAYER_PATH=${THIRD_PARTY_DIR}/VulkanSDK/bin/MacOS`
  - Add the compile definition: `PILOT_VK_ICD_FILENAMES=${THIRD_PARTY_DIR}/VulkanSDK/bin/MacOS/MoltenVK_icd.json`
- Otherwise (other Unix/Linux systems):
  - Set the value of `vulkan_lib` to the value of `THIRD_PARTY_DIR` plus `/VulkanSDK/lib/Linux/libvulkan.so.1`. Effectively, this sets the <Vulkan library path> to <third-party library directory>/VulkanSDK/lib/Linux/libvulkan.so.1.
  - Set the value of `glslangValidator_executable` to the value of `THIRD_PARTY_DIR` plus `/VulkanSDK/bin/Linux/glslangValidator`. Effectively, this sets the <GLSL validator executable path> to <third-party library directory>/VulkanSDK/bin/Linux/glslangValidator.
  - Add the compile definition: `PILOT_VK_LAYER_PATH=${THIRD_PARTY_DIR}/VulkanSDK/bin/Linux`

Otherwise, it's running on an unsupported platform, and an error is printed.

```cmake
set(SHADER_COMPILE_TARGET PilotShaderCompile)
```

This line means: set the value of `SHADER_COMPILE_TARGET` to `PilotShaderCompile`. This value is the name of a Target, which will be used later.

```cmake
add_subdirectory(shader)
add_subdirectory(3rdparty)
add_subdirectory(source/runtime)
add_subdirectory(source/editor)
```

The next four lines all add subdirectories: shader, 3rdparty, source/runtime and source/editor. We'll analyze them next time.

```cmake
set(CODEGEN_TARGET "PilotPreCompile")
include(source/precompile/precompile.cmake)
set_target_properties("${CODEGEN_TARGET}" PROPERTIES FOLDER "Engine" )
add_dependencies(PilotRuntime "${CODEGEN_TARGET}")
```

The last four lines: set the `CODEGEN_TARGET` variable to `PilotPreCompile`; include the source/precompile/precompile.cmake file so the functions defined in it can be used; set a property on the target `CODEGEN_TARGET` (i.e. PilotPreCompile), with its folder set to `Engine`; and add a dependency: PilotRuntime depends on `CODEGEN_TARGET` (PilotPreCompile).

## Summary

In Pilot, CMake provides cross-platform project file generation, so that everyone can use CMake on different platforms to get the project files they want, and then debug, build and release.

Next time, we'll continue with the CMakeLists.txt files in the four subdirectories shader, 3rdparty, source/runtime and source/editor, and see how Pilot uses CMake to generate its project files.
