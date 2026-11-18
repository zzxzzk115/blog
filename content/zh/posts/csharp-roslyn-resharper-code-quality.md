---
title: '游戏工业化探索 - 基于 Roslyn 和 Resharper 实现 C# 代码质量与规范一致性保证'
date: 2023-03-10T17:21:00
categories: [编程语言]
tags: [CSharp, Roslyn, ReSharper, 代码质量, CI]
toc: true
original: true
---

> 本文转载自我在 FlowUs 上的笔记（写于 2023-03-10），迁移时整理了格式。

目前，我们正处于游戏工业化时代，即整个游戏开发过程是一条具有严格规范的流水线，一个游戏从孵化到开发到上线再到维护，有各种工具和规范为我们的开发流程保驾护航，它们保证开发流程的规范化和一致性，保证交付产物的质量。这条流水线最终需要交付高质量的游戏产品。

<!--more-->

## 前言

每个公司内部都有自己的代码规范，包括命名规范、格式规范、语法规范等，但是大多数情况下我们并没有直接进行完整的代码分析和修正，在有效利用专业的工具之前，大多数情况下都是让 leader 进行代码 review，虽然这样可以保证大多数情况下的代码质量和规范的一致性，但是多少容易出现疏漏的情况，而且效率比较低。我们希望在代码编辑阶段就做出严格的规范限制，这在目前是可行的。

我们公司使用 Unity 作为核心游戏引擎，与此同时，我们最新的服务器框架也使用 .NET 6.0 开发。这意味着，客户端程序员和服务器程序员都使用 C# 作为主力编程语言。

近些年来，.NET 发展迅速，C# 语言的新特性层出不穷，这些特性中，有符合我们需求的，也有一些让人匪夷所思的。我们需要确定，哪些特性允许被使用，哪些特性被禁止使用。

我们的 CI 使用 Jenkins，我们可以编写 Groovy 脚本和其他平台特定的脚本（bat/Powershell 或者 sh/bash），高度定制 CI 管线的流程，我们的目标是将代码分析这个步骤加入到 Build 管线中。

我们需要统一我们的代码规范，对于不满足规范的代码，首先应该在 IDE 中提示警告和错误，其次，应该在 CI 流程的 Build 步骤时中断，统计并报告不符合规范的代码出处，反馈给相应程序员，这样可以最大程度地保证代码的质量和规范一致性。

最近这段时间，我和一位前辈对“C# 代码质量与规范一致性保证”这一板块进行了技术调研，目的是探求游戏工业化时代下，如何严格保证统一的代码编写规范、如何保证 C# 代码符合预期的质量以及如何将代码分析步骤整合到 CI 流程中。

我们最终的结论是：

1. 使用 Roslyn
2. 使用 Resharper 的命令行工具 InspectCode（已确定）和 CleanupCode（待讨论）
3. 编写命令行工具，在 Jenkins Build Pipeline 中加入代码分析流程

## Roslyn 简介

Roslyn 是微软推出的 C#、VB、F# 编译器的开源实现，是一个编译器的平台。它提供了 API 接口和 SDK，允许我们基于 Roslyn SDK 实现自己的代码分析器（`Code Analyzer`）。我们可以利用 Roslyn SDK 提供的代码分析与修正功能，来保证我们的代码质量和规范的一致性。

代码分析器生成后，我们可以得到一个 Nuget 包，项目安装该 Nuget 包后，Visual Studio 在编辑器运行时提供分析支持，同时也在编译期提供分析支持。除了得到 Nuget 包之外，我们还可以得到一个 VSIX 文件（Visual Studio 插件安装包），Visual Studio 安装该插件后，Visual Studio 在编辑器运行时提供分析支持，在编译期没有分析支持。分析器通过获得代码的语法树（`Syntax Tree`），进行语法分析、语义分析，检查是否不符合自己定制的一系列规范。如果不规范，会报告一个诊断。VS 收到 Roslyn 的诊断报告后，会查找同诊断 ID 对应的一个或多个代码修正提供器（`CodeFixProvider`），用户可以选择一个，执行相应的代码修正（`Code Fix`）逻辑，代码修正逻辑中进行语法转换。简单说就是在 Visual Studio 中产生警告或者错误（通常是蓝色或者红色的波浪线，附近还会出现一个灯泡），提示用户应用代码修正，用户点击对应修正选项后，会应用修正逻辑。

这个场景想必大家都不陌生，因为微软本身已经基于 Roslyn 编写了 C# 语言的基本分析器，我们平时编写的项目在创建时已经默认引用并加载了这些分析器，所以我们经常会在开发中看到一些小灯泡，考虑是否根据它的提示来修改代码，选择其中一个修正选项后，我们的代码会得到相应的改良或修正。

举个实际点的例子，Unity 其实就实现了自己的代码分析器，当 Unity 游戏开发者使用 Visual Studio 进行了一些不符合 Unity 开发规范或者编写了不被推荐的代码时（例如 `var component = new MonoBehaviour();` 或者创建了一个空的 Update 方法），VS 会提示开发者应用代码修正。开发者的 IDE 中会出现警告或错误，将鼠标悬停在上面，会提示诊断信息，包含可供采取的代码修正方案，选择修正方案，代码就会被修正。

Unity 的代码分析器仓库在这里：

{{< linkcard url="https://github.com/microsoft/Microsoft.Unity.Analyzers" title="GitHub - microsoft/Microsoft.Unity.Analyzers: Roslyn analyzers for Unity game developers" desc="Roslyn analyzers for Unity game developers. Contribute to microsoft/Microsoft.Unity.Analyzers development by creating an account on GitHub." site="GitHub" image="/img/linkcards/github-com-microsoft-microsoft-unity-analyzers-3e031a.png" >}}

此外，Resharper 的命令行工具 InspectCode 和 CleanupCode 的工作内容是类似的，即代码的分析与清理。为什么已经存在 Roslyn，还需要使用 Resharper 呢？原因后面会展开描述。

## 使用 Roslyn 实现代码的分析与修正

环境前置依赖：

- Visual Studio 2022（推荐）或 Visual Studio 2019（16.8 或更高版本，不推荐，已过时）
- .NET Framework 4.6 及以上，建议 .NET Framework 4.8
- .NET SDK 6.0 及以上，建议 6.0 和 7.0 都安装
- Roslyn SDK

关于 Roslyn SDK 的安装，在 Visual Studio Installer 中下载单个组件即可：

![在 Visual Studio Installer 中安装 .NET Compiler Platform SDK](/img/flowus/roslyn/01.png)

### 创建 Analyzer with Code Fix 项目

首先通过模板创建一个 `Analyzer with Code Fix` 项目，它将生成代码分析器（Nuget 包或者 VSIX 插件）。

> 当然，Roslyn SDK 也支持创建独立的代码分析命令行工具和代码重构插件，这里我就不展开描述了，后面有机会再写新的文章。

![Analyzer with Code Fix 项目模板](/img/flowus/roslyn/02.png)

这里，我将解决方案项目取名为 `HelloRoslyn`：

![创建 HelloRoslyn 解决方案](/img/flowus/roslyn/03.png)

创建后，整个解决方案由以下项目组成：

- HelloRoslyn
- HelloRoslyn.CodeFixes
- HelloRoslyn.Package
- HelloRoslyn.Test
- HelloRoslyn.Vsix

### HelloRoslyn 项目

此项目包含了代码分析器。

在 Roslyn 中，分析器是通过反射收集的，它收集满足以下条件的所有类型：

- 派生自 `DiagnosticAnalyzer` 类型
- 被 `DiagnosticAnalyzer` 特性所标记

> 如果不同时满足这两个条件，则不会被收集，即不会生效，需要注意。

在此模板项目的 `HelloRoslynAnalyzer.cs` 中，我们的 `HelloRoslynAnalyzer` 派生自 `DiagnosticAnalyzer`，被 `DiagnosticAnalyzer` 特性标记，它会被反射收集到一个分析器集合中，最终，Roslyn 会执行分析器集合中的所有分析器。

![HelloRoslynAnalyzer 的声明](/img/flowus/roslyn/04.png)

`DiagnosticAnalyzer` 特性用于描述分析的语言，可选的语言有：`CSharp`（C#）、`VisualBasic`（VB）以及 `FSharp`（F#），都是微软自家的语言。我们针对 C# 进行代码分析，故传入 `LanguageNames.CSharp` 即可。

`DiagnosticAnalyzer` 提供了代码分析的基本功能，并提供了一些虚方法供我们重写，例如 [DiagnosticAnalyzer.Initialize(AnalysisContext)](https://learn.microsoft.com/zh-cn/dotnet/api/microsoft.codeanalysis.diagnostics.diagnosticanalyzer.initialize#microsoft-codeanalysis-diagnostics-diagnosticanalyzer-initialize(microsoft-codeanalysis-diagnostics-analysiscontext)) 方法，在这个方法中，我们可以注册分析器回调。即当 Visual Studio 检测到匹配的注册操作的代码编辑时，我们注册的回调方法会被调用。在回调方法中，我们会在满足发起诊断条件的情况下，创建一个诊断对象，Visual Studio 利用这个诊断对象来通知用户警告或者错误描述。

本例中，注册了一个符号行为（`Symbol Action`）回调方法 `AnalyzeSymbol`，并且待分析的符号属于具名类型（`SymbolKind.NamedType`）。

**HelloRoslynAnalyzer-注册流程**

```csharp
        public override void Initialize(AnalysisContext context)
        {
            context.ConfigureGeneratedCodeAnalysis(GeneratedCodeAnalysisFlags.None);
            context.EnableConcurrentExecution();

            // TODO: Consider registering other actions that act on syntax instead of or in addition to symbols
            // See https://github.com/dotnet/roslyn/blob/main/docs/analyzers/Analyzer%20Actions%20Semantics.md for more information
            context.RegisterSymbolAction(AnalyzeSymbol, SymbolKind.NamedType);
        }

        private static void AnalyzeSymbol(SymbolAnalysisContext context)
        {
            // TODO: Replace the following code with your own analysis, generating Diagnostic objects for any issues you find
            var namedTypeSymbol = (INamedTypeSymbol)context.Symbol;

            // Find just those named type symbols with names containing lowercase letters.
            if (namedTypeSymbol.Name.ToCharArray().Any(char.IsLower))
            {
                // For all such symbols, produce a diagnostic.
                var diagnostic = Diagnostic.Create(Rule, namedTypeSymbol.Locations[0], namedTypeSymbol.Name);

                context.ReportDiagnostic(diagnostic);
            }
        }
```

在 `AnalyzeSymbol` 方法中，我们能够通过参数获得当前的符号分析上下文（`SymbolAnalysisContext`），这个上下文是 Roslyn 分析了代码的语法树后，筛选出来的符合要求的一个单个符号对应的上下文。实际上，对于每个符合要求的符号，都会执行这个回调方法。我们可以通过这个上下文，拿到符号的名称。本例中，我们判断符号名称中是否具有小写字符，如果存在小写字符，我们就生成一个诊断对象，并通过上下文，报告这个诊断。此诊断会被 Visual Studio 收集，最终会在 IDE 中显示波浪线，提示用户相关诊断信息。

“创建诊断信息”这一行为对应的规则是我们自己创建的，它是 `DiagnosticDescriptor` 类型的对象。

我们通常会在一个具体 `Analyzer` 类型中创建静态只读的 `DiagnosticDescriptor` 类型的字段。

`DiagnosticDescriptor` 的构造通常需要以下关键内容：

- 诊断 ID（唯一标识诊断对象，一个全局唯一的字符串，例如 `"HELLO_ROSLYN_0001"`）
- 诊断标题（描述诊断的标题，支持使用 `Resources.resx` 配置的本地化字符串）
- 诊断的消息格式字符串（描述诊断具体内容的格式字符串，例如 `"Type name '{0}' contains lowercase letters"`，即支持占位符替换的格式化字符串，支持使用 `Resources.resx` 配置的本地化字符串）
- 诊断类别（描述诊断的类别，例如 `"Design"`、`"Naming"`，用于分类，命名没有硬性要求）
- 诊断级别（描述诊断的级别，包括 `Hidden`、`Info`、`Warning` 和 `Error`，最终会对应 IDE 中隐藏、提示、警告和错误，我们一般选择 `Warning` 和 `Error`。）
- 诊断描述（描述诊断的详细信息，告诉用户出现诊断的原因，例如 `"Type names should be all uppercase."`，支持使用 `Resources.resx` 配置的本地化字符串）

除了注册符号行为外，还有很多其他的行为可供注册，例如代码块行为、编译行为、操作行为、语法节点行为等等：

![AnalysisContext 可注册的各种行为](/img/flowus/roslyn/05.png)

API 文档地址：

{{< linkcard url="https://learn.microsoft.com/zh-cn/dotnet/api/microsoft.codeanalysis.diagnostics.analysiscontext?view=roslyn-dotnet-4.3.0" title="AnalysisContext 类 (Microsoft.CodeAnalysis.Diagnostics)" desc="用于初始化分析器的上下文。 分析器初始化可以使用 AnalysisContext 来注册在以下任意位置执行的操作： 编译开始，编译结束，完成分析代码文档，完成代码文档的语义分析，完成符号的语义分析，开始对方法主体或出现在方法主体外部的表达式进行语义分析，完成方法主体或显示在方法主体外部的表达式的语义分析，或者完成语法节点的语义分析。" image="/img/linkcards/learn-microsoft-com-zh-cn-dotnet-api-microsoft-c-34581f.png" >}}

我们可以按需注册对应的行为回调，完成诊断对象的创建，并在诊断条件满足的情况下报告诊断。这样，VS 就可以显示对应的警告或者错误提示了。

### HelloRoslyn.CodeFixes 项目

此项目包含了代码修正提供器，只提供了一个代码修正提供器，实际上，我们可以针对一个代码分析器提供一个或多个代码修正提供器。

当诊断报告被 Roslyn 收集并提交给 VS 后，VS 会尝试获得与这个诊断报告诊断 ID 匹配的代码修正提供器，进而用户可以选择提供器提供的修正选项，进行代码修正。如果 VS 找不到对应的代码修正提供器，则会在诊断提示信息中提示错误。

在 Roslyn 中，代码修正提供器也是通过反射收集的，它收集满足以下条件的所有类型：

- 派生自 `CodeFixProvider` 类型
- 被 `ExportCodeFixProvider` 特性所标记

> 同样地，如果不同时满足这两个条件，则不会被收集，即不会生效，需要注意。

在此模板项目的 `HelloRoslynCodeFixProvider.cs` 中，我们的 `HelloRoslynCodeFixProvider` 派生自 `CodeFixProvider`，被 `ExportCodeFixProvider` 特性标记，它会被反射收集到一个代码修正提供器集合中，最终，VS 针对诊断报告，找到对应的所有代码修正提供器，供用户选择使用，表现为灯泡按钮被点击后的一个或多个修复选项，用户点击具体选项后，Roslyn 就会执行对应的代码修正提供器的代码修正回调逻辑。

![HelloRoslynCodeFixProvider 的声明](/img/flowus/roslyn/06.png)

`ExportCodeFixProvider` 特性用于描述分析的语言并指定对应代码提供器的名称，同样地，可选的语言有：`CSharp`（C#）、`VisualBasic`（VB）以及 `FSharp`（F#）。我们针对 C# 进行代码分析，故传入 `LanguageNames.CSharp` 即可。例子中，我们指定代码提供器的名称为 `HelloRoslynCodeFixProvider`。

`CodeFixProvider` 则是提供了代码修正的基本功能，并提供了一些虚方法供我们重写，例如 [CodeFixProvider.RegisterCodeFixesAsync(CodeFixContext)](https://learn.microsoft.com/zh-cn/dotnet/api/microsoft.codeanalysis.codefixes.codefixprovider.registercodefixesasync#microsoft-codeanalysis-codefixes-codefixprovider-registercodefixesasync(microsoft-codeanalysis-codefixes-codefixcontext)) 方法，在这个方法中，我们可以注册修正器回调。即当用户点击修正选项后，我们注册的回调方法会被调用。这个回调是一个异步过程。在回调方法中，我们会获得代码的文档对象和语法结构。此时我们有多个选择。

1. 我们可以选择创建一个新的解决方案（`Microsoft.CodeAnalysis.Solution` 类型）对象并返回。即用户点击修正选项后，整个解决方案的相应代码被修正（覆盖）。
2. 我们可以选择创建一个新的文档（`Microsoft.CodeAnalysis.Document` 类型）对象并返回。即用户点击修正选项后，当前正编辑中文档的代码被修正（覆盖）。

本例中，注册了一个修改解决方案的回调方法 `MakeUppercaseAsync`，从参数获取到代码文档、类型定义语法结构以及一个 `CancellationToken` 对象用于异步取消操作。该方法通过获得之前分析器收集的具有小写字符的类型，将该类型的 Token 的文本属性（`Text`）更改为全大写，并获得文档对应的语义模型，进而获得类型对应的符号，然后创建一个新的解决方案对象，在这个解决方案中应用符号改名（通过调用 `Renamer.RenameSymbolAsync` 方法），并返回新的解决方案对象。

**HelloRoslynCodeFixProvider 注册流程**

```csharp
        private async Task<Solution> MakeUppercaseAsync(Document document, TypeDeclarationSyntax typeDecl, CancellationToken cancellationToken)
        {
            // Compute new uppercase name.
            var identifierToken = typeDecl.Identifier;
            var newName = identifierToken.Text.ToUpperInvariant();

            // Get the symbol representing the type to be renamed.
            var semanticModel = await document.GetSemanticModelAsync(cancellationToken);
            var typeSymbol = semanticModel.GetDeclaredSymbol(typeDecl, cancellationToken);

            // Produce a new solution that has all references to that type renamed, including the declaration.
            var originalSolution = document.Project.Solution;
            var optionSet = originalSolution.Workspace.Options;
            var newSolution = await Renamer.RenameSymbolAsync(document.Project.Solution, typeSymbol, newName, optionSet, cancellationToken).ConfigureAwait(false);
            // Return the new solution with the now-uppercase type name.
            return newSolution;
        }
```

这样，当用户命名了带有小写字符的类型，编辑器出现提示后，点击修正选项，则会将整个解决方案中的具有小写字符命名的类型全部覆盖为全大写字符命名。

### HelloRoslyn.Package 项目

此项目基本不用改动，它已经包含了 Nuget 包的安装脚本和卸载脚本，这些脚本都是 PowerShell 脚本。如果有特定的需求，才需要改动脚本内容。

生成此项目，会生成 Nuget 包文件，该文件可以添加到支持 .NET Standard 2.0 的项目中作为分析器。

> .NET Framework 较新版本和 .NET Core 较新版本均实现了 .NET Standard 2.0，所以这个 Nuget 包，对于现代的 .NET Framework 和 .NET 版本而言，都可以使用。

### HelloRoslyn.Test 项目

此项目用于写一些测试用例。我们可以硬编码一些字符串，用于模拟代码文档以及创建期待的结果，然后测试我们的分析器和修正提供器。

Verifiers 文件夹中的验证器内容我们基本不需要更改，是直接可用的。当然我们也可以进行扩展。

样例中，我们的 `TestMethod1` 显示测试模式，确保分析器在不应报告诊断的情况下不会执行此操作。

`TestMethod2` 方法，通过 `VerifyCS.Diagnostic` 方法，尝试诊断，诊断 ID 为 `"HelloRoslyn"`，并在 `0` 位置插入参数，该参数填入到 `test` 字符串的 `0` 位置，即类名为 `TypeName`。我们知道，当类名中存在任意一个小写字符时，都会触发诊断，故此处会触发诊断。接着，通过 `VerifyCS.VerifyCodeFixAsync` 方法，把我们的原始代码文档内容、期望修改后的代码文档内容以及修改后的代码文档内容进行比对验证。

**HelloRoslynUnitTests.cs**

```csharp
using Microsoft.VisualStudio.TestTools.UnitTesting;
using System.Threading.Tasks;
using VerifyCS = HelloRoslyn.Test.CSharpCodeFixVerifier<
    HelloRoslyn.HelloRoslynAnalyzer,
    HelloRoslyn.HelloRoslynCodeFixProvider>;

namespace HelloRoslyn.Test
{
    [TestClass]
    public class HelloRoslynUnitTest
    {
        //No diagnostics expected to show up
        [TestMethod]
        public async Task TestMethod1()
        {
            var test = @"";

            await VerifyCS.VerifyAnalyzerAsync(test);
        }

        //Diagnostic and CodeFix both triggered and checked for
        [TestMethod]
        public async Task TestMethod2()
        {
            var test = @"
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;
    using System.Diagnostics;

    namespace ConsoleApplication1
    {
        class {|#0:TypeName|}
        {   
        }
    }";

            var fixtest = @"
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;
    using System.Diagnostics;

    namespace ConsoleApplication1
    {
        class TYPENAME
        {   
        }
    }";

            var expected = VerifyCS.Diagnostic("HelloRoslyn").WithLocation(0).WithArguments("TypeName");
            await VerifyCS.VerifyCodeFixAsync(test, expected, fixtest);
        }
    }
}
```

右键项目→运行测试，即可看到测试结果：

![单元测试结果](/img/flowus/roslyn/07.png)

我们在正式的开发中，当然不会引用一个项目，然后写一些代码，来进行测试。这样需要反复安装 Nuget 包，且会干扰和影响正式项目的编辑和编译，效率很低，效果不佳。所以，每当我们写了一个 Analyzer 和对应的所有 CodeFixProvider 后，都要写测试用例，进行全面的单元测试。

### HelloRoslyn.Vsix 项目

该项目将会生成 VS 插件安装文件（以 .vsix 为后缀），双击后，会出现安装插件的窗口。

> 需要注意，插件仅在 IDE 运行时，即编辑时进行代码分析，并不会在编译期生效。如果需要在编译期进行代码分析，则需要通过 Nuget 包的形式，加入到待分析的项目的引用中。

### 创建沙盒项目测试 Nuget 包

首先，我们将 HelloRoslyn.Package 生成得到的 Nuget 包文件拷贝到一个目录下。这个目录将作为我们的 Nuget 源。例如：

![作为本地 Nuget 源的目录](/img/flowus/roslyn/08.png)

然后，我们在 Visual Studio 中，添加 Nuget 本地源：

![打开 Nuget 包源设置](/img/flowus/roslyn/09.png)

![添加本地 Nuget 源](/img/flowus/roslyn/10.png)

记得输入名称和源后要点击更新按钮。

随后，我们就可以对沙盒 C# 控制台项目添加 Nuget 包引用了（即添加分析器）。

然后我们随便创建一个带有小写字符的类型，错误列表中就会出现警告：

![错误列表中的警告](/img/flowus/roslyn/11.png)

没有蓝色波浪线应该是我家里的电脑没有配置警告的显示。

鼠标悬停在类名上，我们也会发现诊断信息：

![悬停显示的诊断信息](/img/flowus/roslyn/12.png)

点击“显示可以修补的程序”，或者使用快捷键 `Ctrl` + `.`，则会出现代码修正选项：

![代码修正选项](/img/flowus/roslyn/13.png)

选择 `Make uppercase` 后，我们的类名就变成了全大写。这说明我们的代码分析器和代码修正提供器的功能在正式使用中是没有问题的。

### 分析器开发流程

基本的流程为：

1. 确定诊断 ID、诊断级别及其他关键诊断参数
2. 确定语法分析流程
3. 确定语义分析流程
4. 确定诊断报告条件

#### 语法分析

开发中，我们需要借助语法树视图来快速获得代码的语法树结构，进而思考如何编写分析器。

点击 视图→其他窗口→Syntax Visualizer 即可打开语法树可视化工具：

![Syntax Visualizer](/img/flowus/roslyn/14.png)

我们可以看到代码文档对应的语法树结构，可以获得所有 Token 以及相应描述信息。

后续开发可以参考以下教程：

{{< linkcard url="https://learn.microsoft.com/zh-cn/dotnet/csharp/roslyn-sdk/get-started/syntax-analysis" title="语法分析入门（Roslyn API） - C#" desc="遍历、查询和遍步语法树简介。" image="/img/linkcards/learn-microsoft-com-zh-cn-dotnet-csharp-roslyn-s-7b20d8.png" >}}

#### 语义分析

进行语法分析后，我们可以进而进行语义分析。

{{< linkcard url="https://learn.microsoft.com/zh-cn/dotnet/csharp/roslyn-sdk/get-started/semantic-analysis" title="语义分析入门 - C#" desc="本教程概述了如何使用 .NET 编译器 SDK 进行语义分析。" image="/img/linkcards/learn-microsoft-com-zh-cn-dotnet-csharp-roslyn-s-16dea4.png" >}}

### 修正提供器开发流程

进而我们可以进行修正提供器的编写。

基本流程就一步：确定语法转换流程。

#### 语法转换

修正提供器的修正逻辑本质上是进行语法转换，即创建新的语法结构，覆盖原本的文档或者原本的整个解决方案。

> 这里要注意，并不是直接修改原本的文档和解决方案。.NET 编译器平台具有不可变性的基本原则，适用于语法树、编译、符号、语义模型等。所以我们是对文档或解决方案进行覆盖，而不是修改。

{{< linkcard url="https://learn.microsoft.com/zh-cn/dotnet/csharp/roslyn-sdk/get-started/syntax-transformation" title="语法转换入门 （Roslyn API） - C#" desc="有关创建和转换语法树的简介。" image="/img/linkcards/learn-microsoft-com-zh-cn-dotnet-csharp-roslyn-s-75bbb5.png" >}}

### 整合到 CI 流程中

实际上，使用 Nuget 包形式将分析器添加到各个待分析的项目中，即可在编译期进行代码分析。如果代码不符合规范，且是 error，则会被视为编译失败。

我们服务器的 CI 流程中，通过使用 MSBuild 来编译整个解决方案，它可以同时指定输出 warning 级别的内容和 error 级别的内容到不同的两个文件中。我们可以将不满足规范的代码分析级别定为 Error，这样，我们可以写一个命令行工具，读取 error 级别的输出文件，一旦存在内容，即存在不满足规范的代码，并且这个命令行工具可以以正则或者其他形式筛选出具体项目、具体文件、具体行号等信息，最终会出现在 CI 的输出日志中，这样就可以告诉对应程序员，请进行代码的修正。（存在程序员不打开 VS 编辑代码文件并提交的情况，例如 SVN 修改冲突、使用 Visual Studio Code 或者 Notepad++ 进行快速编辑时）

## 使用 Resharper 命令行工具

Resharper 的 dotSettings 配置文件包含了代码样式相关的配置，它实际上可以实现部分代码分析逻辑，主要是进行一些预设的命名、格式、语法上的代码分析，当不满足配置的规范时，可以配置不同的警告级别，如忽略、提示、建议、警告或者报错。

![Resharper 的代码检查严重级别设置](/img/flowus/roslyn/15.png)

预设代表有限支持，这是它的痛点所在，如果需要高度定制代码分析，必然需要使用 Roslyn。那么，我们为什么还要用 Resharper 呢？

原因如下：

1. 我们公司从初期到现在已经传承下来了 dotSettings 配置文件，对于一些命名、格式、语法上的规范，已经确定好了，可以直接使用。我们不希望为了这些规范，再重新用 Roslyn 来实现一遍，这其实是很浪费时间的一件事情，虽然可以做，但是成本比较高。所以，我们还是会保留 Resharper 的这部分代码分析工作。我们在 .NET 6.0 项目中，将 dotSettings 导出为 editorConfig，并将 IDE 类别的诊断信息升级为编译期类别，这样除了 IDE 运行期，在编译期也能进行相应代码的分析与诊断。
2. 公司部分项目的服务器项目并未升级到 .NET 6.0，依旧使用 .NET Framework 4.6。考虑到这些暂时不会升级到 .NET 6.0 的项目，我们必须尽可能地为它们也提供代码分析流程。

在 .NET 5.0 及以后的项目中，我们可以配置项目的 editorConfig，将一些 IDE 警告或错误升级为编译警告或错误，最终在 MSBuild 的 warning 或 error 输出文件中可以找到对应的条目。这意味着对于使用 .NET 6.0 的项目而言，我们仅仅通过 MSBuild 就可以满足需求了。

{{< linkcard url="https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/overview?tabs=net-6#enable-on-build" title="Code analysis in .NET" desc="Learn about source code analysis in the .NET SDK." image="/img/linkcards/learn-microsoft-com-en-us-dotnet-fundamentals-co-2e78c0.png" >}}

但在 .NET Framework 中，这个方案是行不通的。我们的 CI 使用 MSBuild 编译解决方案，我们配置的一些 IDE 代码规范，并不会在编译期间得到分析，因为它们属于 IDE 类别，而非编译类别，也就是说，无法将它们升级，它们不会出现在输出文件中，这不是我们期望的结果。

此时 Resharper 的 InspectCode 就发挥作用了，它可以不依赖于 MSBuild 直接进行代码的分析，并且可以输出分析结果，这个结果同样可以作为 CI 是否继续的指标。

### 使用 InspectCode 实现代码分析

InspectCode 是 Resharper 命令行工具中包含的代码审查工具，它会对代码进行语法树分析，然后审查是否存在不符合规范的代码，如果存在，则会生成一个 Issue。最终，它的统计结果可以通过指定输出文件的形式，默认以 XML 格式输出。我们可以写一个命令行工具，解析该 XML 文件，根据其中是否存在 Issue 节点，来判断是否存在不符合规范的代码，进而可以成为中断 CI 流程的指标。

它支持 dotSettings 配置、editorConfig 配置以及命令行参数。

我们最关键的命令行参数为：使用 `--no-build` 跳过 MSBuild 流程，使用 `-job=8` 开启 8 核心并行分析，使用 `-e=ERROR` 设置最小诊断级别（只收集报告错误诊断）。

具体的配置及命令行参数详见官网，这里不过多展开。

{{< linkcard url="https://www.jetbrains.com/help/resharper/InspectCode.html" title="InspectCode Command-Line Tool | ReSharper" site="ReSharper Help" image="/img/linkcards/www-jetbrains-com-help-resharper-inspectcode-htm-747b16.jpg" >}}

### 使用 CleanupCode 实现代码清理

CleanupCode 是 Resharper 命令行工具中包含的代码清理工具，它支持修正代码格式，应用语法样式，移除冗余代码等功能。

它支持 dotSettings 配置、editorConfig 配置以及命令行参数。

具体的配置及命令行参数详见官网，这里不过多展开。

{{< linkcard url="https://www.jetbrains.com/help/resharper/CleanupCode.html" title="CleanupCode Command-Line Tool | ReSharper" site="ReSharper Help" image="/img/linkcards/www-jetbrains-com-help-resharper-cleanupcode-htm-02ad44.jpg" >}}

我们可以考虑在 CI 流程中，首先应用一遍 CleanupCode，进而再进行一次 InspectCode，不过目前这个方案还没有经过讨论。我个人认为，我们不应该依赖于工具在 CI 流程里进行自动化代码修正，而要把代码的修正工作彻底落实到写具体代码的程序员身上，否则很容易出现一些“无所谓，CI 总是会帮我处理好并提交到 Git/SVN”的懒惰想法，我认为这是不可取的，属于负优化，也违背了我们的初衷。当然，这是我个人的想法，具体是否采纳这个方案，还有待讨论。

## 总结

游戏工业化时代下的我们，应该注重游戏开发流程上的各种规范的一致性，并且保证交付质量，这样，我们的游戏产品才会茁壮成长，最终，我们才能够有机会将一个个高质量的游戏产品展现给大家。

感谢 Roslyn 和 Resharper，它们让我们能够尽可能地保证代码的质量和规范一致性。

一些可供参考的链接：

{{< linkcard url="https://mp.weixin.qq.com/s/62UMgI7q1diJp9JRjzQ4RA" title="紫龙上海CTO王琦：我们对游戏工业化的探索" site="微信公众平台" image="/img/linkcards/mp-weixin-qq-com-s-62umgi7q1dijp9jrjzq4ra-4a9141.jpg" >}}

{{< linkcard url="https://github.com/dotnet/roslyn" title="GitHub - dotnet/roslyn: The Roslyn .NET compiler provides C# and Visual Basic languages with rich code analysis APIs." desc="The Roslyn .NET compiler provides C# and Visual Basic languages with rich code analysis APIs. - dotnet/roslyn" site="GitHub" image="/img/linkcards/github-com-dotnet-roslyn-fc7711.png" >}}

{{< linkcard url="https://learn.microsoft.com/zh-cn/dotnet/csharp/roslyn-sdk/" title=".NET Compiler Platform SDK (Roslyn API) - C#" desc="了解如何使用 .NET 编译器平台 SDK（也称为 Roslyn API）来了解 .NET 代码、发现错误并修复这些错误。" image="/img/linkcards/learn-microsoft-com-zh-cn-dotnet-csharp-roslyn-s-a05600.png" >}}

{{< linkcard url="https://learn.microsoft.com/zh-cn/dotnet/csharp/roslyn-sdk/tutorials/how-to-write-csharp-analyzer-code-fix" title="教程：编写第一个分析器和代码修复 - C#" desc="本教程提供了使用 .NET 编译器 SDK（Roslyn API）生成分析器和代码修复的分步说明。" image="/img/linkcards/learn-microsoft-com-zh-cn-dotnet-csharp-roslyn-s-9d33d8.png" >}}

{{< linkcard url="https://www.jetbrains.com/help/resharper/ReSharper_Command_Line_Tools.html" title="ReSharper command line tools | ReSharper" site="ReSharper Help" image="/img/linkcards/www-jetbrains-com-help-resharper-resharper-comma-ccaca9.jpg" >}}
