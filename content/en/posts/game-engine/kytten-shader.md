---
title: 'KyttenShader: A Modern Cross-Platform Shader System'
date: 2023-05-07T06:29:00
categories: [Game Engines]
tags: [Kytten, Shader, Slang, SPIR-V, Cross-Platform]
toc: true
original: true
zhihu: 627321970
aiTranslated: true
---

> Reposted from my Zhihu column: [KyttenShader: 现代的跨平台 Shader 系统](https://zhuanlan.zhihu.com/p/627321970) (published 2023-05-07); formatting tidied during migration.

> [!NOTE]
> The Kytten engine is no longer being developed, but it did exist. It laid the groundwork for the later [Snow Leopard Engine](https://github.com/SnowLeopardEngine/SnowLeopardEngine) (a Leeds MSc team project) and [libvultra](https://github.com/zzxzzk115/libvultra). The roadmap and the "coming later" plans in this post won't be continued.

KyttenShader is the modern cross-platform shader system in Kytten Engine, currently under development.

<!--more-->

## Background

### Shader Reflection

Through the shader reflection mechanisms provided by certain tools, we can obtain the inputs, outputs, layouts, buffers and so on defined in shader code. We can collect this reflected information and put it to use in the material system.

### Slang

Slang is a modern shading language. It extends HLSL syntax with more developer-friendly language features.

{{< linkcard url="https://shader-slang.org/slang/user-guide/convenience-features.html" title="Basic Convenience Features" desc="Making it easier to work with shaders" site="slang" >}}

It is compatible with HLSL; supports parameter blocks, interfaces and generics, and a module system; supports compute shaders, rasterization shaders and ray-tracing shaders; and supports reflection. Most importantly, it can compile Slang or HLSL code to DXBC, DXIL, SPIR-V, HLSL, GLSL (limited OpenGL support, no OpenGL ES), CUDA and more — practically every mainstream target.

### SPIR-V Cross

SPIR-V is an open, standard, portable intermediate language model proposed by the Khronos Group. SPIR-V Cross can compile SPIR-V binaries to GLSL, HLSL and MSL, and supports reflection. In other words, it can export shader code for OpenGL, OpenGL ES, Vulkan, DirectX 11 and Metal.

{{< linkcard url="https://github.com/KhronosGroup/SPIRV-Cross" title="GitHub - KhronosGroup/SPIRV-Cross: SPIRV-Cross is a practical tool and library for performing reflection on SPIR-V and…" desc="SPIRV-Cross is a practical tool and library for performing reflection on SPIR-V and disassembling SPIR-V back to high level languages. - KhronosGroup/SPIRV-Cross" site="GitHub" image="/img/linkcards/github-com-khronosgroup-spirv-cross-66790a.png" >}}

### HJSON

HJSON is an extension of JSON. It supports comments, lets you omit trailing commas at the end of lines, lets you omit double quotes around strings, supports multi-line string blocks and so on, making it friendlier and more readable than JSON.

{{< linkcard url="https://github.com/hjson/hjson" title="GitHub - hjson/hjson: Hjson, a user interface for JSON" desc="Hjson, a user interface for JSON. Contribute to hjson/hjson development by creating an account on GitHub." site="GitHub" image="/img/linkcards/github-com-hjson-hjson-45de6e.png" >}}

## Introducing KyttenShader

### Format

KyttenShader files use the .kshader extension and are written in HJSON. KyttenShader uses the following terms:

**Stage**: a specific stage, such as vertex, pixel (fragment) or compute. A Stage contains Slang source code.

**RenderSetup**: render state settings, such as cull mode, blend mode and so on.

**Tags**: configuration options related to the rendering engine.

**Pass**: describes a single render pass; essentially it corresponds to one Slang module.

**Shader**: describes the whole shader, including all of its Passes.

Here is a valid KyttenShader:

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

### Compilation Pipeline

![KyttenShader compilation pipeline](/img/zhihu/kytten-shader-compile-flow.jpg)

- Deserialize the kshader file into a KyttenShader instance (using [hjson-cpp](https://github.com/hjson/hjson-cpp))
- Set the render pipeline state based on RenderSetup and Tags
- Iterate over each Pass
  - Set the render pipeline state based on RenderSetup and Tags
  - Iterate over each Stage
    - Compile the target platform's shader code using the configured Profile, EntryPoint and Src
    - Obtain the reflection information and collect it into a KyttenShaderReflectionInfo structure, which the material system will use later.

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
- Export Slang modules that other KyttenShaders can import.

For DX11/DX12, this pipeline already produces the final DXBC, HLSL or DXIL, which can be used directly.

For Vulkan, this pipeline already produces the final SPIR-V binary, which can be used directly.

For MetalSL, once we have the SPIR-V binary, we use SPIR-V Cross to go one step further and get MetalSL code.

For OpenGL, since the GLSL that Slang generates isn't perfect — it has some issues — and lacks OpenGL ES support, once we have the SPIR-V binary we use SPIR-V Cross to go one step further and get GLSL code for OpenGL/OpenGL ES.

### Modularity and Reuse

Similar to Unity's cginc, Kytten Engine will provide built-in Slang modules; you just manually import the module file name (without the extension) in Src.

{{< linkcard url="https://shader-slang.org/slang/user-guide/modules.html" title="Modules and Access Control" desc="Making it easier to work with shaders" site="slang" >}}

During compilation, besides being compiled, each Stage also exports a .slang file to a designated search location by default.

For example, the earlier example exports a file named `Demo_DemoShader_BasePass_Pixel.slang`; the naming rule is `{ShaderName}_{PassName}_{StageName}.slang`.

This way, if a Stage in another shader wants to reuse the code of a particular Stage in a particular Pass of some shader, it only needs `import {ShaderName}_{PassName}_{StageName}`. We built a small wrapper on top of this mechanism by adding an ImportModule block:

```text
ImportModule: Demo/DemoShader/BasePass/Pixel
```

The ImportModule block inserts an import statement at the very beginning of the current Stage's Src:

```text
import Demo_DemoShader_BasePass_Pixel
```

Of course, Passes can be reused too. We handle Pass reuse by reference. Likewise, we added a UsePass block:

```text
UsePass: Demo/DemoShader/BasePass
```

Essentially, at compile time it checks whether the referenced Pass has already been fully compiled. If not, it compiles the referenced Pass first; otherwise it skips compilation and uses the already-compiled target files.

> KyttenShader doesn't have a feature like Unity's GrabPass yet; it will be added later.

### A Brief Look at the Material System

A KyttenMaterial essentially references a KyttenShader. By collecting the KyttenShader's reflection information, it holds the shader's parameter input information, provides corresponding UI controls in the editor so developers can conveniently set parameters, and can be serialized into a preset.

## KyttenShader vs. Unity ShaderLab

Unity ShaderLab uses HLSLcc to translate HLSL into GLSL, GLSL ES, GLSL Vulkan and MetalSL. It's a workable approach, but it isn't where the industry is heading. The trend is clearly toward the powerful DirectXShaderCompiler / Slang + SPIR-V Cross toolchain. In fact, Unity has already started integrating SPIR-V Cross to build a new shader compilation system.

Unity's SPIRV-Cross fork (`Unity-Technologies/SPIRV-Cross`; the repository no longer exists)

KyttenShader takes the modern approach. Because Slang has so many language features, writing shaders becomes more convenient and efficient, and the results are of higher quality. At the same time, KyttenShader makes effective use of SPIR-V Cross's powerful ecosystem.

## Plans for KyttenShaderGraph

KyttenShaderGraph is essentially a visual editing system for .kshader files. It produces the final .kshader file through a real-time DAG (directed acyclic graph) plus code generation. KyttenShaderGraph is not on the KyttenEngine 0.1.0 roadmap; it is expected to land in version 0.2.0.

## References

Cross-Platform Shader Handling, Stephanheigl, <https://stephanheigl.github.io/posts/shader-compiler/>

## Further Reading

{{< linkcard url="https://shader-slang.org/slang/user-guide/compiling.html" title="Compiling Code with Slang" desc="Making it easier to work with shaders" site="slang" >}}

{{< linkcard url="https://web.archive.org/web/20260416215429/https://shader-playground.timjones.io/" title="Shader Playground" >}}
