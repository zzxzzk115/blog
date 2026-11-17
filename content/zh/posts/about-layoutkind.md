---
title: 关于 CLR 的 StructLayoutAttribute 控制类型的字段布局的探究
date: 2020-11-21T23:31:50
categories: [编程语言]
tags: [CLR, StructLayoutAttribute]
toc: true
---

《CLR via C#》的 p110 一整页都在叙述"CLR 如何控制类型中的字段布局"的问题。

让我们来仔细分析一下 StructLayoutAttribute 中 LayoutKind 的几种不同的选项的具体应用场景。

<!--more-->

# 类型字段布局 与 StructLayoutAttribute

类型的字段布局，也就是类型字段在内存中的排列方式。是让 C# 编译器自己采用最优化的布局，还是采用当前字段顺序的布局，还是自定义字段偏移量的布局？这些都可以由你来决定(当然 C# 也有默认选择)。根据不同的场景，需要选择不同的处理方式。如果选择的处理方式不恰当，可能就会出现"内存损耗高、性能较低"或者"内存分布和对齐不匹配导致平台调用失败"相关的问题。

你可以为自己定义的类或结构应用 C# 中 System.Runtime.InteropServices.StructLayoutAttribute 特性。

共有三种选项：

1. LayoutKind.Auto，编译器自动布局
2. LayoutKind.Sequential，按字段定义的顺序布局
3. LayoutKind.Explicit，自定义字段偏移量，设置布局

## LayoutKind.Auto：更好的性能

> 如果不与非托管代码交互，采用 LayoutKind.Auto 是不错的选择

来看个例子：

```csharp
[StructLayout(LayoutKind.Auto)]
struct StructAuto
{
    public int a;
    public bool b;
    public int c;
    public double d;
}

[StructLayout(LayoutKind.Sequential)]
struct StructSequential
{
    public int a;
    public bool b;
    public int c;
    public double d;
}
```

为了测试值类型变量的内存分配情况，需要开启/unsafe 开关，在 VS 里，打开项目设置，点击"生成"，勾选"运行不安全代码"：

![open_unsafe](/img/markdown_20201122210307.png)

通过 unsafe 块，得到内存地址：

```csharp
Console.WriteLine("size of bool : " + sizeof(bool) + "byte(s)");
Console.WriteLine("size of int : " + sizeof(int) + "byte(s)");
Console.WriteLine("size of double : " + sizeof(double) + "byte(s)");
unsafe
{
    Console.WriteLine("StructAuto:");
    StructAuto sa = new StructAuto();
    Console.WriteLine("address of a : 0x{0}", ((int)&sa.a).ToString("X"));
    Console.WriteLine("address of b : 0x{0}", ((int)&sa.b).ToString("X"));
    Console.WriteLine("address of c : 0x{0}", ((int)&sa.c).ToString("X"));
    Console.WriteLine("address of d : 0x{0}", ((int)&sa.d).ToString("X"));
    Console.WriteLine("StructSequential:");
    StructSequential ss = new StructSequential();
    Console.WriteLine("address of a : 0x{0}", ((int)&ss.a).ToString("X"));
    Console.WriteLine("address of b : 0x{0}", ((int)&ss.b).ToString("X"));
    Console.WriteLine("address of c : 0x{0}", ((int)&ss.c).ToString("X"));
    Console.WriteLine("address of d : 0x{0}", ((int)&ss.d).ToString("X"));
}
```

结果：

![result_layoutkind_auto_sequential](/img/markdown_20201123121552.png)

用内存图的形式表示一下这两个结构体变量的内存分配情况：

![data_image](/img/markdown_20201123141654.png)

可以看到，LayoutKind.Auto 会以一种最节约内存的形式对字段进行布局和内存对齐。这种布局是编译器自动提供的，是编译器自己找到的一种最优的字段布局方式，所以字段在内存中的排布顺序和定义字段时的顺序可能会不一样。

而 LayoutKind.Sequential 会按照你定义字段的顺序在内存中布局和内存对齐，并且和 C++ 结构的内存对齐方式一样，以字段中占最大字节数的倍数来进行对齐（这个例子中最大是 double 占用的 8Bytes，所以补齐后的字节数应该是 8 的倍数，这里是 24Bytes）。

一般情况下，如果不与非托管代码进行交互，使用 LayoutKind.Auto 更节约空间，性能更好。如果要和其他非托管代码（例如 C++）进行交互，例如使用到了非托管 C++ 编译的 DLL 中的某函数，需要传入一个结构体，那么，这个结构体，在 C# 这边声明时，就需要使用 LayoutKind.Sequential 来保持和 C++ 一样的布局和对齐方式，这样不会出现问题。当然，C# 编译器默认对 Struct 使用的就是 LayoutKind.Sequential 进行布局的，如果你刚好要和非托管 C++ 交互，那么刚好；如果你不用和非托管代码交互，想更加高效，那么 LayoutKind.Auto 是不错的选择。

## LayoutKind.Sequential ：与 非托管 C++ 交互

> 与非托管 C++ 交互时，LayoutKind.Sequential 是必要的。

新建一个 C++（非 CLI），DLL 项目：

![new_cpp(notcli)_dll](/img/markdown_20201123143252.png)

然后在 StructDLL.cpp 中添加结构体和需要导出的方法（使用 extern "C"的话，函数的入口就是函数名，否则是带有其它参数标记的一长串字符串，仅限用于没有重载函数的时候方便找到函数）：

![](/img/markdown_20201123152943.png)

上面的函数的作用是将传入的 Point 变量的 x, y, z 全部反转。

生成解决方案，得到 StructDLL.dll 文件，复制到 C# CLR 项目的 bin/Debug 目录中。

在 C# CLR 的项目中导入这个 DLL 中的 GetPointString 方法：

![import_dll](/img/markdown_20201123153111.png)

C++ 类型和 C# 类型对照参考：[https://www.cnblogs.com/zhangweizhong/p/8119395.html](https://www.cnblogs.com/zhangweizhong/p/8119395.html)

进行测试：

![Point 类型定义](/img/markdown_20201123153248.png)

![test](/img/markdown_20201123153133.png)

结果：

![result_sequential_dll](/img/markdown_20201123153309.png)

成功调用。

**假如** 对 Point 设置的布局采用 Layout.Auto 呢？看看效果：

![error1](/img/markdown_20201123153438.png)

抛出异常，说明是"无效的托管/非托管类型组合"。可以肯定的是，因为此时的内存布局和对齐与 C++ 不一致，导致不能成功传入符合要求的参数，导致调用失败，抛出异常。

## LayoutKind.Explicit : 更加灵活

> LayoutKind.Explicit 适用于一些对内存布局和偏移量有精确要求的场景

LayoutKind.Explicit 要求必须对每一个字段声明偏移量：

![error2](/img/markdown_20201123160711.png)

像这样是满足要求的：

![fieldoffset](/img/markdown_20201123160827.png)

测试一下：

```csharp
unsafe
{
    Console.WriteLine("StructExplicit:");
    StructExplicit se = new StructExplicit();
    Console.WriteLine("address of a : 0x{0}", ((int)&se.a).ToString("X"));
    Console.WriteLine("address of b : 0x{0}", ((int)&se.b).ToString("X"));
    Console.WriteLine("address of c : 0x{0}", ((int)&se.c).ToString("X"));
    Console.WriteLine("address of d : 0x{0}", ((int)&se.d).ToString("X"));
}
```

结果：

![result_explicit_1](/img/markdown_20201123161137.png)

可以发现，这样的结构，没有进行内存对齐，因为偏移量都是自己定义的。

那么理论上，使用这种方式对上面 LayoutKind.Sequential 例子中的 Point 结构控制布局，也能正常调用，来测试一下：

由于 float 占用 4 个字节，这里的字段的偏移量应该分别是是 0,4,8。

![explicit_point](/img/markdown_20201123165052.png)

结果：

![result_explicit](/img/markdown_20201123165217.png)

成功调用。

如果不按照 C++ 内存对齐方式来，我们定义为 0,5,10 的话呢？理论上是会报错的，测试一下：

![result_explicit_error](/img/markdown_20201123170011.png)

并没有报错。我们画内存图来分析一下：

![analysis](/img/markdown_20201123230956.png)

按照 C# 这边的内存布局，传送到 C++(DLL) 的数据是偏移量 0-11 的数据块，C++ 对偏移量为 0-3，4-7，8-11 的三个字段，进行取反（最高位从 0 变为 1，或者从 1 变为 0），改变好后，传送会 C# 这边，C# 这边按照自己的内存布局再进行解析，得到的数据就是错误的数据，但并没有报错，因为只是数据错了。（见上图）

有什么场景非常需要这样的功能呢？答案是 C/C++ 中的 union 联合体。

union 和 struct 不同，它的成员共享同一个内存地址。也就是说，字段的偏移量都是 0。

此时用

```csharp
[StructLayout(LayoutKind.Explicit)]
struct UnionSimulation
{
    [FieldOffset(0)]
    public int a;
    [FieldOffset(0)]
    public bool b;
    [FieldOffset(0)]
    public char c;
}
```

可以模拟 C/C++ 中的 union：

```cpp
union UnionData{
    int a;
    bool b;
    char c;
};
```

这样，如果非托管 C++ 编译的 DLL 中的函数需要 union 作为参数，我们就可以利用 LayoutKind.Explicit 来进行模拟，字段偏移量都设置为 0 即可。

----

参考：

[https://www.cnblogs.com/happyhippy/archive/2007/04/17/717028.html](https://www.cnblogs.com/happyhippy/archive/2007/04/17/717028.html)

[https://www.cnblogs.com/tuyile006/p/3804261.html](https://www.cnblogs.com/tuyile006/p/3804261.html)

[https://www.cnblogs.com/zhangweizhong/p/8119395.html](https://www.cnblogs.com/zhangweizhong/p/8119395.html)













