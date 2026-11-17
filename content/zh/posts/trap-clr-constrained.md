---
title: 《我大意了啊》之 CLR 中值类型调用 Equals 是否装箱的问题
date: 2020-11-20T17:32:27
categories: [编程语言]
tags: [trap, CLR]
toc: true
---

试想一下，你自定义了一个 Point 结构：

```csharp
public struct Point
{
    private readonly float m_x;
    private readonly float m_y;
    private readonly float m_z;
    //没有重写Equals方法
}
```

下面这样一段代码，共发生了几次装箱？

```csharp
var p1 = new Point();
var p2 = new Point();
if (p1.Equals(p2))
{
   Console.WriteLine("-------"); 
}
```

再看看 IL 代码：

![il_point](/img/markdown_20201120174752.png)

你觉得共发生了几次装箱呢？1 次？2 次？还是其他？

<!--more-->

# 我太天真了

天真的我，天真地觉得是 1 次。因为我就看到了一个 box 指令。如果你和我一样因为只看到了一个 box 指令而觉得是 1 次，那么恭喜，我俩都中招了。

其实如果不看 IL，按照一般的思路去想的话，我会觉得是 2 次。因为自定义的 Point 类型继承自 System.ValueType，Equals 方法是 System.ValueType 重写自 System.Object 的虚方法。Point 结构没有重写 Equals 方法的话，想要调用父类 ValueType 的 Equals 方法，就需要装箱，因为需要判断对象的类型来定位类型的方法表，才能找到该方法。所以，p1 调用 Equals 的时候，p1 要装箱。p2 作为参数传入的时候，p2 要装箱（因为 Equals 的参数要求是 Object)。

但是看到 IL，我只看到一个 box 指令，我会觉得可能是我想错了，可能就是 1 次吧。。。

其实还是 2 次。因为 box 底下跟着一个 constrained. 被我忽略了。。。后来还是一位同学发了关于 constrained. 的定义我才知道，它也可能会做装箱的操作。

## constrained. 指令

constrained. 指令有什么作用呢？

[点击查看文档](https://docs.microsoft.com/en-us/dotnet/api/system.reflection.emit.opcodes.constrained?view=net-5.0)

根据文档中的定义：

![constrained.](/img/markdown_20201120180905.png)

关键部分是：

- 如果类型是引用类型，那么托管指针 ptr 解引用并且作为 this 指针传入 callvirt 方法。
- 如果类型是值类型，并且实现（重写）了虚方法，那么 ptr 不会修改，作为 this 指针 传入 call 方法，直接调用该类型实现的这个方法。
- 如果类型是值类型，但是没有实现（重写）虚方法，那么 ptr 解引用，装箱，作为 this 指针传入 callvirt 方法。

## "Point 调用 Equals 发生几次装箱"的正确结果

对于我们的问题，Point 结构没有重写 ValueType 的 Equals 方法，p1 调用 Equals 方法的时候，处于第三种情况。很明显可以知道，发生了值类型装箱。加上 p2 作为参数传入 Equals(Object) 发生的一次装箱，一共是 2 次装箱。

## 如果 Point 重写了 Equals 方法

如果 Point 重写了 Equals 方法，则处于上面的第二种情况，p1 调用 Equals 方法时，是直接调用 Point 实现的 Equals 实例方法。但是 p2 作为参数传入 Equals(Object) 会发生一次装箱。这样的情况，一共 1 次装箱。

# 反思

我太天真了。这次我踩坑了，我还是不细心，没有仔细思考。不应该通过所谓的表象去直接得出结论，还是要从问题本身去思考。有些时候看问题确实不能只看表面，而且看表面也不能看个一知半解。constrained. 就是这样一个东西，你要是放着没管，你就和我一样犯错了，你如果搞懂了它的作用，答案也就很明显了。

踩坑，没关系，不踩坑反而可能出问题。以后《我大意了啊》会作为一个系列出现，专门讲述踩坑+解决方案/正确答案。