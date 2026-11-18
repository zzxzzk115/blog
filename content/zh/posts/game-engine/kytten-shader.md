---
title: 'KyttenShader：现代的跨平台 Shader 系统'
date: 2023-05-07T06:29:00
categories: [游戏引擎]
tags: [Kytten, Shader, Slang, SPIR-V, 跨平台]
toc: true
original: true
zhihu: 627321970
---

> 本文转载自我在知乎的专栏文章：[KyttenShader: 现代的跨平台 Shader 系统](https://zhuanlan.zhihu.com/p/627321970)（发布于 2023-05-07），迁移时整理了格式。

> [!NOTE]
> Kytten 引擎已经停止开发，但它确实存在过。它为后来的 [Snow Leopard Engine](https://github.com/SnowLeopardEngine/SnowLeopardEngine)（利兹大学硕士团队项目）以及 [libvultra](https://github.com/zzxzzk115/libvultra) 奠定了基础。文中的 Roadmap 和「后续会加入」的计划不再继续。

KyttenShader 是 Kytten Engine 中的现代的跨平台 Shader 系统，正在开发中。

<!--more-->

## 前置内容

### Shader 的反射

通过一些工具的 Shader 反射 (Reflection) 机制，我们可以获得 Shader 代码中定义的输入 (Inputs)、输出 (Outputs)、布局 (Layouts)、缓冲区 (Buffers) 等等。我们可以收集这些反射出来的信息，运用到材质 (Material) 系统中。

### Slang

Slang 是现代的 Shader 语言，它是对 HLSL 语法的扩展，具有更人性化的语法特性。

[Basic Convenience Features](https://shader-slang.com/slang/user-guide/03-convenience-features.html)

它兼容 HLSL，支持参数块 (Parameter Blocks)，支持接口 (Interfaces) 和泛型 (Generics)，支持模块系统 (Module System)，支持 Compute Shader、Rasterization Shader 以及 Ray-Tracing Shader，支持反射，最关键的是，它支持将 Slang 代码或者 HLSL 代码编译为 DXBC、DXIL、SPIR-V、HLSL、GLSL (有限支持 OpenGL，不支持 OpenGL ES)、CUDA 等等几乎所有主流的代码。

### SPIR-V Cross

SPIR-V 是 Khronos 组织提出的一套开源的标准可移植的中间语言模型，SPIR-V Cross 则可以将 SPIR-V 格式的二进制文件编译为 GLSL、HLSL、MSL，支持反射。也就是说，支持导出得到 OpenGL、OpenGL ES、Vulkan、DirectX11 以及 Metal 这些平台的 Shader 代码。

[GitHub - KhronosGroup/SPIRV-Cross](https://github.com/KhronosGroup/SPIRV-Cross)

### HJSON

HJSON 是对 JSON 的扩展，支持注释，支持行尾省略逗号，支持省略字符串的双引号，支持多行字符串块等等，比 JSON 更人性化，更易读。

[GitHub - hjson/hjson](https://github.com/hjson/hjson)

## KyttenShader 介绍

### 格式

KyttenShader 后缀为 .kshader，格式采用 HJSON。在 KyttenShader 中，具有以下术语：

**Stage**：即指定阶段，例如 vertex、pixel (fragment)、compute 等，Stage 内部包含 Slang 源码。

**RenderSetup**：渲染状态设置，例如剔除模式、混合模式等等。

**Tags**：用于配置一些与渲染引擎相关的配置选项。

**Pass**：描述一个渲染过程，本质上对应 Slang 的一个 Module。

**Shader**：描述整个着色器，包括所有的 Pass。

以下是一个合法的 KyttenShader：

```text
{
    Shader : {
        Name: Demo/DemoShader
        RenderSetup: {
            CullMode: Back
            ZTest: Always
        }
        Tags: {
            RenderType: Opaque
        }
        Passes: [
            {
                Name: BasePass
                RenderSetup: {
                    ZWrite: On
                    Blend: SrcFactor
                }
                Tags: {
                    DisableBatching: true
                }
                Stages: [
                    {
                        Name: Pixel
                        Profile: ps_6_0
                        EntryPoint: PSMain
                        Src: '''
                            struct PSInput
                            {
                                float4 color : COLOR;
                            };

                            float4 PSMain(PSInput input) : SV_TARGET
                            {
                                return input.color;
                            }
                        '''
                    }
                ]
            }
        ]
    }
}
```

### 编译流程

![KyttenShader 编译流程](/img/zhihu/kytten-shader-compile-flow.jpg)

- 将 kshader 文件反序列化为 KyttenShader 实例（使用 [hjson-cpp](https://github.com/hjson/hjson-cpp)）
- 根据 RenderSetup 和 Tags，设置渲染管线状态
- 遍历每一个 Pass
  - 根据 RenderSetup 和 Tags，设置渲染管线状态
  - 遍历每一个 Stage
    - 通过配置的 Profile、EntryPoint 和 Src，编译得到目标平台 Shader 代码
    - 获得反射信息，收集到 KyttenShaderReflectionInfo 结构中，后续材质系统会利用到。

      ```cpp
      slang::ShaderReflection* shaderReflection = slang::ShaderReflection::get(request);

      unsigned parameterCount = shaderReflection->getParameterCount();
      for(unsigned pp = 0; pp < parameterCount; pp++)
      {
          slang::VariableLayoutReflection* parameter =
              shaderReflection->getParameterByIndex(pp);
          // ...
      }
      ```
- 导出 Slang 模块，可供其他 KyttenShader 导入使用。

对于 DX11/DX12，此流程已经可以得到最终的 DXBC、HLSL 或者 DXIL，直接使用即可。

对于 Vulkan，此流程已经可以得到最终的 SPIR-V 二进制文件，直接使用即可。

对于 MetalSL，我们在得到 SPIR-V 二进制文件后，使用 SPIR-V Cross 进一步得到 MetalSL 代码。

对于 OpenGL，由于 Slang 编译得到的 GLSL 并不完美，存在部分问题，且缺乏 OpenGL ES 的支持，我们在得到 SPIR-V 二进制文件后，使用 SPIR-V Cross 进一步得到 OpenGL/OpenGL ES 的 GLSL 代码。

### 模块化与复用

与 Unity 的 cginc 类似，Kytten Engine 将会提供内置的 Slang 模块，在 Src 中手动 import 模块文件名称（不带后缀）即可。

[Basic Convenience Features: Modules](https://shader-slang.com/slang/user-guide/03-convenience-features.html#modules)

编译流程中，每一个 Stage 除了会被编译以外，还会默认导出 .slang 文件到指定的搜索位置。

例如之前的例子中，会导出一个名为 `Demo_DemoShader_BasePass_Pixel.slang` 的文件，命名规则为 `{ShaderName}_{PassName}_{StageName}.slang`。

这样，其他 Shader 的 Stage 如果想复用某个 Shader 的某个 Pass 中的某个 Stage 的代码，只需要 `import {ShaderName}_{PassName}_{StageName}`。我们在这个原理的基础上封装了一下，增加了 ImportModule 块：

```text
ImportModule: Demo/DemoShader/BasePass/Pixel
```

ImportModule 块会使得在当前 Stage 的 Src 最开始插入一行 import 语句：

```text
import Demo_DemoShader_BasePass_Pixel
```

当然，Pass 也可以被复用，对于 Pass 的复用，我们通过引用的形式完成。同样地，我们增加了 UsePass 块：

```text
UsePass: Demo/DemoShader/BasePass
```

本质上，编译时，它会检查被引用的 Pass 是否已经被编译完全，若没有，则先去编译被引用的 Pass，否则，直接跳过编译，使用已编译的目标文件。

> 目前，KyttenShader 还没有加入类似 Unity 中 GrabPass 的功能，后续会加入。

### 材质系统简述

KyttenMaterial 本质上引用了一个 KyttenShader，并通过收集 KyttenShader 的反射信息，持有其参数输入信息，在编辑器下提供相应的 UI 控件，方便开发者设置参数，并且可以被序列化成为一个预设。

## KyttenShader 与 Unity ShaderLab

Unity ShaderLab 采用 HLSLcc 将 HLSL 翻译为 GLSL、GLSL ES、GLSL Vulkan、MetalSL，虽然是可行的方案，但并不是大趋势下的实现方案。大趋势下，势必利用 DirectXShaderCompiler / Slang + SPIR-V Cross 这一强大的体系。当然，Unity 已经在着手接入 SPIR-V Cross，实现新的 Shader 编译系统了。

[Unity-Technologies/SPIRV-Cross](https://github.com/Unity-Technologies/SPIRV-Cross)

KyttenShader 采用现代的实现方案，由于 Slang 具有非常多的语言特性，使得写 Shader 更加方便、高效、高质量。同时，KyttenShader 有效利用了 SPIR-V Cross 的强大生态。

## KyttenShaderGraph 开发思路

KyttenShaderGraph 本质上是为 .kshader 提供的可视化编辑系统，通过实时的 DAG（有向无环图）+ 代码生成，得到最终的 .kshader 文件。KyttenEngine 0.1.0 版本的 Roadmap 中不包括 KyttenShaderGraph，预计在 0.2.0 版本中加入。

## 相关引用

Cross-Platform Shader Handling, Stephanheigl, <https://stephanheigl.github.io/posts/shader-compiler/>

## 扩展阅读

- [Slang API User's Guide](https://shader-slang.com/slang/api-users-guide.html)
- [Shader Playground](https://shader-playground.timjones.io/)
