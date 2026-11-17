---
title: '类型对象的加载时机和类型初始化器的调用时机之间的关系'
date: 2021-03-26T10:32:34
tags: [CLR, CSharp]
categories: [Tech]
toc: true
---

类型对象什么时候加载到Loader堆？类型初始化器又是什么时候被调用？

<!--more-->

# 类型对象的加载和类型初始化器的调用

类型对象的加载发生在运行时，JIT编译期间。类型初始化器当且仅当程序第一次访问到类型对象中的内容时被调用。

## 方法调用前，JIT编译器做的事情

假设目前有这样一个类型：

```csharp
public class TestClass
{   
    static TestClass()
    {
        Console.WriteLine("Test cctor");
    }
    
    public void TestFunction()
    {
        Console.WriteLine("Test");
    }
}
```

那么，TestClass类型的类型对象什么时候会被加载到Loader堆呢？

答案是：首次引用到了TestClass类型的方法被调用前，JIT编译时。

例如：现在有这样一个方法马上要被线程执行：

```csharp
public void M1()
{
    TestClass tc = new TestClass();
}
```

JIT编译器在将M1的IL代码转换成本机CPU指令的时候，会注意到M1内部引用的所有类型(目前只有TestClass)，CLR需要确定定义了这些类型的程序集都已被加载，然后利用程序集的元数据提取和这些类型有关的信息，创建一些数据结构(类型对象)来表示类型本身。

> 注意，此时还未调用M1方法。

也就是说，M1是首次引用TestClass类型的情况下， **调用M1之前** ，TestClass的类型对象会被加载到Loader堆上。

有人会有疑问，那TestClass的类型初始化器会被调用吗？

## 类型初始化器的调用时机

其实，仔细想想就能明白，TestClass的类型初始化器，应该在M1执行到`TestClass tc = new TestClass();`这一句的时候被调用。因为new操作符需要对TestClass实例对象的类型对象指针、同步块索引等进行初始化，这会访问到TestClass的类型对象。