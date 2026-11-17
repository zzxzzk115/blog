---
title: 程序如何监视AppDomain的卸载
date: 2021-01-27T20:09:08
categories: [Tech]
tags: [AppDomain, CLR, CSharp]
toc: true
---

AppDomain可以被手动卸载，有的时候我们可能需要程序能够监听到某个或某些AppDomain的卸载。

那么，程序如何监视AppDomain的卸载呢？

# 探索System.AppDomain提供的的所有事件成员

首先我想到的是查看AppDomain类是否提供了一些公开的事件成员。

为了快速找到有哪些事件成员，我通过AppDomain的静态方法CreateDomain创建一个AppDomain实例后，通过智能感知，勾选闪电图标（代表事件），来快速得到结果：

![](/img/markdown_20210127201650.png)

![](/img/markdown_20210127201736.png)

可以发现，提供了9种公开的事件成员:

- DomainUnload : 在即将卸载AppDomain时发生
- AssemblyLoad : 在加载程序集时发生
- AssemblyResolve : 在对程序集的解析失败时发生
- FirstChanceException : 当托管代码抛出异常时发生，在运行时在调用堆栈中搜索应用程序域中的异常处理程序之前
- ProcessExit : 当默认应用程序域的父进程存在时发生
- ReflectionOnlyAssemblyResolve : 当程序集的解析在仅限反射的上下文中失败时发生
- ResourceResolve : 当资源解析因资源不是程序集中的有效链接资源或嵌入资源而失败时发生
- TypeResolve : 在对类型的解析失败时发生
- UnhandledException : 当某个异常未被捕获时出现

第一个，恰好就是我需要的事件成员：DomainUnload。

它在即将卸载AppDomain时发生。

# 注册DomainUnload事件

先看看DomainUnload事件的委托类型：

![](/img/markdown_20210127202702.png)

是EventHandler类型，那么我们的监听方法需要的方法的结构为`void 方法名(object, EventArgs)`

我定义一个静态方法去监听（因为测试代码在静态方法中）:

![](/img/markdown_20210127202945.png)

然后测试代码为：

![](/img/markdown_20210127203020.png)

# 测试

Main方法：

![](/img/markdown_20210127203101.png)



结果：

![](/img/markdown_20210127203206.png)

# 分析

sender的实际类型实际上是AppDomain类型，所以可以通过as操作得到AppDomain的实例，进而获得更加详尽的信息:

![](/img/markdown_20210127203504.png)

结果：

![](/img/markdown_20210127203615.png)



# 总结

System.AppDomain提供了DomainUnload事件，注册该事件，程序就可以监视AppDomain的卸载。

