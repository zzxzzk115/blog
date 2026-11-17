---
title: 程序如何监视 AppDomain 的卸载
date: 2021-01-27T20:09:08
categories: [编程语言]
tags: [CLR, CSharp, AppDomain]
toc: true
---

AppDomain 可以被手动卸载，有的时候我们可能需要程序能够监听到某个或某些 AppDomain 的卸载。

那么，程序如何监视 AppDomain 的卸载呢？

# 探索 System.AppDomain 提供的的所有事件成员

首先我想到的是查看 AppDomain 类是否提供了一些公开的事件成员。

为了快速找到有哪些事件成员，我通过 AppDomain 的静态方法 CreateDomain 创建一个 AppDomain 实例后，通过智能感知，勾选闪电图标（代表事件），来快速得到结果：

![](/img/markdown_20210127201650.png)

![](/img/markdown_20210127201736.png)

可以发现，提供了 9 种公开的事件成员:

- DomainUnload : 在即将卸载 AppDomain 时发生
- AssemblyLoad : 在加载程序集时发生
- AssemblyResolve : 在对程序集的解析失败时发生
- FirstChanceException : 当托管代码抛出异常时发生，在运行时在调用堆栈中搜索应用程序域中的异常处理程序之前
- ProcessExit : 当默认应用程序域的父进程存在时发生
- ReflectionOnlyAssemblyResolve : 当程序集的解析在仅限反射的上下文中失败时发生
- ResourceResolve : 当资源解析因资源不是程序集中的有效链接资源或嵌入资源而失败时发生
- TypeResolve : 在对类型的解析失败时发生
- UnhandledException : 当某个异常未被捕获时出现

第一个，恰好就是我需要的事件成员：DomainUnload。

它在即将卸载 AppDomain 时发生。

# 注册 DomainUnload 事件

先看看 DomainUnload 事件的委托类型：

![](/img/markdown_20210127202702.png)

是 EventHandler 类型，那么我们的监听方法需要的方法的结构为 `void 方法名(object, EventArgs)`

我定义一个静态方法去监听（因为测试代码在静态方法中）:

![](/img/markdown_20210127202945.png)

然后测试代码为：

![](/img/markdown_20210127203020.png)

# 测试

Main 方法：

![](/img/markdown_20210127203101.png)



结果：

![](/img/markdown_20210127203206.png)

# 分析

sender 的实际类型实际上是 AppDomain 类型，所以可以通过 as 操作得到 AppDomain 的实例，进而获得更加详尽的信息:

![](/img/markdown_20210127203504.png)

结果：

![](/img/markdown_20210127203615.png)



# 总结

System.AppDomain 提供了 DomainUnload 事件，注册该事件，程序就可以监视 AppDomain 的卸载。

