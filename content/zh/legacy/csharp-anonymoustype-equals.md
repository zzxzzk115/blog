---
title: C#匿名类型的同一性与相等性
date: 2021-01-14T16:57:59
categories: [Tech]
tags: [CLR, CSharp, AnonymousType]
toc: true
---

C#里，如何判断匿名类型是同一种类型？匿名类型的实例对象怎么判断相等？

<!--more-->

# C#匿名类型

看一段代码:

```csharp
var o = new { Name = "Jack", Age = 22};
```

o是什么类型？

o是 **匿名类型** 。

在new后面不指定类型名称，而使用 **对象初始化器** 语法来声明属性并初始化属性，这样，C#编译器会自动定义一种匿名类型。

我们编译以后查看IL反汇编就能得知了：

![](http://img.zhangkexuan.cn/markdown_20210114170834.png)

可以看到，这样一种匿名类型，里面有两个私有字段，分别叫`<Age>i__Field`和`<Name>i__Field`，还有对应属性生成的方法`get_Age`和`getName`，有重写过的`Equals`、`GetHashCode`、`ToString`，还有实例属性`Age`和`Name`。

## 同一性

```csharp
var o1 = new { Name = "Jack", Age = 22};
var o2 = new { Name = "Tony", Age = 21};
var o3 = new { Name = "Anonymous", Age = 99, Gender = "Male"};
var o4 = new { Namae = "Mitsuhashi", Sai = 20};
var o5 = new { Age = 30, Name = "?"};
```

哪些是同一个类型呢？

一切看IL来分析：

![](http://img.zhangkexuan.cn/markdown_20210114172906.png)

可见，C#编译器根据 **对象初始化器** 中的不同结构来生成不同的匿名类型。

如果对象的类型结构相同，即属性的名称、属性的类型、属性的指定顺序均相同，则属于同一种匿名类型。

所以，上面例子中，o1和o2是同一类型，其他o3、o4、o5各自属于不同的类型。

## 相等性

```csharp
var o1 = new { Name = "Jack", Age = 22 };
var o2 = new { Name = "Jack", Age = 22 };
Console.WriteLine(o1.Equals(o2));
```

结果会是True嘛？

来看看结果：

![](http://img.zhangkexuan.cn/markdown_20210114173253.png)

是True。说明匿名类型一定重写了Equals方法，并且实现了逐字段比较。

查看IL看看Equals是怎么实现的：

![](http://img.zhangkexuan.cn/markdown_20210114173423.png)

关键在于里里面的call和callvirt。

抽离出来就是:

```assembly
IL_000a:  call       class [mscorlib]System.Collections.Generic.EqualityComparer`1<!0> class [mscorlib]System.Collections.Generic.EqualityComparer`1<!'<Name>j__TPar'>::get_Default()

IL_001b:  callvirt   instance bool class [mscorlib]System.Collections.Generic.EqualityComparer`1<!'<Name>j__TPar'>::Equals(!0, !0)

IL_0022:  call       class [mscorlib]System.Collections.Generic.EqualityComparer`1<!0> class [mscorlib]System.Collections.Generic.EqualityComparer`1<!'<Age>j__TPar'>::get_Default()

IL_0033:  callvirt   instance bool class [mscorlib]System.Collections.Generic.EqualityComparer`1<!'<Age>j__TPar'>::Equals(!0, !0)
```

调用的方法有两个：

- `System.Collections.Generic.EqualityComparer<T>.Default`属性生成的方法get_Default。
- `System.Collections.Generic.EqualityComparer<T>.Equals`方法

### System.Collections.Generic.EqualityComparer\<T\>.Default

看看源码：

![](http://img.zhangkexuan.cn/markdown_20210114174343.png)

返回的是静态只读字段defaultComparer，该字段通过CreateComparer方法初始化。

再来看看CreateComparer方法：

![](http://img.zhangkexuan.cn/markdown_20210114174620.png)

简单看来，就是通过RuntimeType得到泛型参数T的运行时实际类型，如果然后返回一个对应的具体XXXEqualityComparer实例。这些XXXEqualityComparer都是EqualityComparer的派生类、具体实现类。

再来看看对应的API文档：

![](http://img.zhangkexuan.cn/markdown_20210114175119.png)

那我们得到的是什么类型的相等比较器呢？

得到的是GenericEqualityComparer，泛型类型相等比较器。因为我们泛型参数传入的是`!'<Name>j__TPar'`、`!'<Age>j__TPar'`这种。

再来看看泛型类型相等比较器的实现：

![](http://img.zhangkexuan.cn/markdown_20210114175812.png)

可以看到，它的确是EqualityComparer\<T\>的派生类。这就很好理解了。当我们在对象初始化器中声明属性并赋值的时候，就相当于GenericEqualityComparer\<T\>中将T指定为赋予值的类型。比如`Name = "Jack"`，就是指定T为String；`Age = 22`，就是指定T为Int32。

所以现在能够理解，以`Name = "Jack"`为例子，System.Collections.Generic.EqualityComparer\<T\>.Default得到的是一个GenericEqualityComparer\<String\>的实例，该实例实现了Equals、GetHashCode等方法。

### System.Collections.Generic.EqualityComparer\<T\>.Equals

来看源码：

![](http://img.zhangkexuan.cn/markdown_20210114180836.png)

抽象方法。已经很明显了。因为GenericEqualityComparer\<T\>是EqualityComparer\<T\>的派生类，所以我们以callvirt调用EqualityComparer\<T\>的Equals方法时，首先会判断当前对象的实际类型，判断出是之前得到的GenericEqualityComparer\<T\>，所以真正调用的方法是GenericEqualityComparer\<T\>实现的Equals:

![](http://img.zhangkexuan.cn/markdown_20210114181356.png)

### 联系起来

还记得之前Equals的IL嘛：

![](http://img.zhangkexuan.cn/markdown_20210114173423.png)

现在再来分析，那就是先通过调用get_Default方法得到一个EqualityComparer（GenericEqualityComparer\<T\>），再将两个匿名类型实例对象的字段放到栈上，最后调用EqualityComparer（GenericEqualityComparer\<T\>）的Equals方法，返回一个bool值，最后将所有bool值综合判断，如果每个字段都相等，则结果就是true，否则是false。

到这里，就分析结束了。

# 总结

C#匿名类型的同一性由C#编译器来完成，它根据不同的结构生成不同的匿名类型，相同结构的对象的匿名类型相同。

C#匿名类型的相等性由CLR在运行时完成，它通过利用GenericEqualityComparer\<T\>的Equals来实现。

