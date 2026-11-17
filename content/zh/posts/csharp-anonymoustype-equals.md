---
title: C# 匿名类型的同一性与相等性
date: 2021-01-14T16:57:59
categories: [编程语言]
tags: [CLR, CSharp, 匿名类型]
toc: true
---

C# 里，如何判断匿名类型是同一种类型？匿名类型的实例对象怎么判断相等？

<!--more-->

# C# 匿名类型

看一段代码:

```csharp
var o = new { Name = "Jack", Age = 22};
```

o 是什么类型？

o 是 **匿名类型** 。

在 new 后面不指定类型名称，而使用 **对象初始化器** 语法来声明属性并初始化属性，这样，C# 编译器会自动定义一种匿名类型。

我们编译以后查看 IL 反汇编就能得知了：

![](/img/markdown_20210114170834.png)

可以看到，这样一种匿名类型，里面有两个私有字段，分别叫 `<Age>i__Field` 和 `<Name>i__Field`，还有对应属性生成的方法 `get_Age` 和 `getName`，有重写过的 `Equals`、`GetHashCode`、`ToString`，还有实例属性 `Age` 和 `Name`。

## 同一性

```csharp
var o1 = new { Name = "Jack", Age = 22};
var o2 = new { Name = "Tony", Age = 21};
var o3 = new { Name = "Anonymous", Age = 99, Gender = "Male"};
var o4 = new { Namae = "Mitsuhashi", Sai = 20};
var o5 = new { Age = 30, Name = "?"};
```

哪些是同一个类型呢？

一切看 IL 来分析：

![](/img/markdown_20210114172906.png)

可见，C# 编译器根据 **对象初始化器** 中的不同结构来生成不同的匿名类型。

如果对象的类型结构相同，即属性的名称、属性的类型、属性的指定顺序均相同，则属于同一种匿名类型。

所以，上面例子中，o1 和 o2 是同一类型，其他 o3、o4、o5 各自属于不同的类型。

## 相等性

```csharp
var o1 = new { Name = "Jack", Age = 22 };
var o2 = new { Name = "Jack", Age = 22 };
Console.WriteLine(o1.Equals(o2));
```

结果会是 True 嘛？

来看看结果：

![](/img/markdown_20210114173253.png)

是 True。说明匿名类型一定重写了 Equals 方法，并且实现了逐字段比较。

查看 IL 看看 Equals 是怎么实现的：

![](/img/markdown_20210114173423.png)

关键在于里里面的 call 和 callvirt。

抽离出来就是:

```cil
IL_000a:  call       class [mscorlib]System.Collections.Generic.EqualityComparer`1<!0> class [mscorlib]System.Collections.Generic.EqualityComparer`1<!'<Name>j__TPar'>::get_Default()

IL_001b:  callvirt   instance bool class [mscorlib]System.Collections.Generic.EqualityComparer`1<!'<Name>j__TPar'>::Equals(!0, !0)

IL_0022:  call       class [mscorlib]System.Collections.Generic.EqualityComparer`1<!0> class [mscorlib]System.Collections.Generic.EqualityComparer`1<!'<Age>j__TPar'>::get_Default()

IL_0033:  callvirt   instance bool class [mscorlib]System.Collections.Generic.EqualityComparer`1<!'<Age>j__TPar'>::Equals(!0, !0)
```

调用的方法有两个：

- `System.Collections.Generic.EqualityComparer<T>.Default` 属性生成的方法 get_Default。
- `System.Collections.Generic.EqualityComparer<T>.Equals` 方法

### System.Collections.Generic.EqualityComparer\<T\>.Default

看看源码：

![](/img/markdown_20210114174343.png)

返回的是静态只读字段 defaultComparer，该字段通过 CreateComparer 方法初始化。

再来看看 CreateComparer 方法：

![](/img/markdown_20210114174620.png)

简单看来，就是通过 RuntimeType 得到泛型参数 T 的运行时实际类型，如果然后返回一个对应的具体 XXXEqualityComparer 实例。这些 XXXEqualityComparer 都是 EqualityComparer 的派生类、具体实现类。

再来看看对应的 API 文档：

![](/img/markdown_20210114175119.png)

那我们得到的是什么类型的相等比较器呢？

得到的是 GenericEqualityComparer，泛型类型相等比较器。因为我们泛型参数传入的是 `!'<Name>j__TPar'`、`!'<Age>j__TPar'` 这种。

再来看看泛型类型相等比较器的实现：

![](/img/markdown_20210114175812.png)

可以看到，它的确是 EqualityComparer\<T\>的派生类。这就很好理解了。当我们在对象初始化器中声明属性并赋值的时候，就相当于 GenericEqualityComparer\<T\>中将 T 指定为赋予值的类型。比如 `Name = "Jack"`，就是指定 T 为 String；`Age = 22`，就是指定 T 为 Int32。

所以现在能够理解，以 `Name = "Jack"` 为例子，System.Collections.Generic.EqualityComparer\<T\>.Default 得到的是一个 GenericEqualityComparer\<String\>的实例，该实例实现了 Equals、GetHashCode 等方法。

### System.Collections.Generic.EqualityComparer\<T\>.Equals

来看源码：

![](/img/markdown_20210114180836.png)

抽象方法。已经很明显了。因为 GenericEqualityComparer\<T\>是 EqualityComparer\<T\>的派生类，所以我们以 callvirt 调用 EqualityComparer\<T\>的 Equals 方法时，首先会判断当前对象的实际类型，判断出是之前得到的 GenericEqualityComparer\<T\>，所以真正调用的方法是 GenericEqualityComparer\<T\>实现的 Equals:

![](/img/markdown_20210114181356.png)

### 联系起来

还记得之前 Equals 的 IL 嘛：

![](/img/markdown_20210114173423.png)

现在再来分析，那就是先通过调用 get_Default 方法得到一个 EqualityComparer（GenericEqualityComparer\<T\>），再将两个匿名类型实例对象的字段放到栈上，最后调用 EqualityComparer（GenericEqualityComparer\<T\>）的 Equals 方法，返回一个 bool 值，最后将所有 bool 值综合判断，如果每个字段都相等，则结果就是 true，否则是 false。

到这里，就分析结束了。

# 总结

C# 匿名类型的同一性由 C# 编译器来完成，它根据不同的结构生成不同的匿名类型，相同结构的对象的匿名类型相同。

C# 匿名类型的相等性由 CLR 在运行时完成，它通过利用 GenericEqualityComparer\<T\>的 Equals 来实现。

