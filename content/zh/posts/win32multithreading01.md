---
title: '《Win32 多线程程序设计》读书笔记（一）'
date: 2020-03-29T13:42:00
categories: [系统编程]
tags: [Win32, 多线程]
toc: true
cnblogs: 12591945
---

> 本文最初发表于我在博客园的旧博客：[《Win32 多线程程序设计》读书笔记（一）](https://www.cnblogs.com/lazy-v/p/12591945.html)（写于 2020-03-29）。

# 第一章

## 多线程的定义

根据书中的内容，宏观上的简单定义为：



**多线程，使程序得以将其工作分开，独立运作，不互相影响。**





维基百科中的定义为：



In [computer architecture](https://en.wikipedia.org/wiki/Computer_architecture), **multithreading** is the ability of a [central processing unit](https://en.wikipedia.org/wiki/Central_processing_unit) (CPU) (or a single core in a [multi-core processor](https://en.wikipedia.org/wiki/Multi-core_processor)) to provide multiple [threads of execution](https://en.wikipedia.org/wiki/Thread_(computer_science)) concurrently, supported by the [operating system](https://en.wikipedia.org/wiki/Operating_system).



也就是说，

**多线程是多处理机、多核处理器提供多个线程并行执行的能力，由操作系统来完成。**

<!--more-->

## 线程与进程

线程是操作系统调度的最小单位。而进程是程序的一次执行，它可以拥有内存、句柄、线程即更多内容。也就是说，线程在操作系统中是比进程要更小的单位，进程可以拥有很多个的线程，同时这些线程能够获得所属进程的共享资源。



## 为什么要用多线程

一个 Web 服务器，拥有成千上万的客户去同时访问。如果没有多线程，就做不到及时的响应，客户体验就好像在排队。

一个 App，如果不用多线程，UI (User Interface) 和逻辑都在主线程中，那么你的逻辑在占用主线程的时候，UI 会无响应。这样的 App，用户体验一定很差。



## 多线程 == 高效 ？

不一定，使用多线程也可能会事倍功半。如果对线程的操作不适当，可能会带来体验极差的效果。



## 多进程为什么行不通

进程的窗口拥有一个句柄(handle)，句柄实际上可以理解为应用程序中实例的标识符，类似指针。如果多进程，则需要将当前进程的 handle 交给另一个进程，这样才能互相访问资源。然而，这是不可能的，因为 handle 只在其诞生池（也就是所属进程）中才有意义。虽说可以创建 handle 副本分享给其他进程，但这样的效率实际上也是很低的，所以多进程行不通。



## 上下文切换(Context Switch)

在抢占式多任务的系统中，操作系统确保每个线程都有机会执行。所以通过硬件计时器，如果一个线程执行的时间够久，则发起一个中断(interrupt)，让 CPU 把线程的当前状态（寄存器的内容）拷贝到堆栈中，再把它从堆栈拷贝到一个上下文(Context) 结构中，以备后续再使用。



完成线程切换，操作系统首先要切换该线程所属进程的内存，然后恢复该线程放在上下文结构中的寄存器的值。这就是上下文切换。



## 竞争条件(Race Conditions)

在抢占式多任务系统中，控制权被强制移转，因此两个线程之间的执行次序不可预期，也就产生了竞争条件(race conditions)。

比如说，客户 A 在编辑一个 `a.cpp`

```c++
#include <iostream>
using namespace std;

int main()
{
    //啥也没写
    return 0;
}
```



同时，客户 B 也在编辑同一个 `a.cpp`

```c++
#include <iostream>
using namespace std;

int main()
{
    cout << "Hello, world!" << endl;
    return 0;
}
```

A 的文本内容短，A 先敲完保存了。

B 后敲完，保存了。

最后 `a.cpp` 的内容是 B 编辑的内容，而 A 的内容被覆盖了。

但如果 A 和 B 敲的内容互换，则又变成 B 的内容被覆盖了。

你不知道 A 和 B 要敲的内容多长，耗时多久，所以结果将会是不可预期。

这就产生了竞争条件。



## 原子操作(Atomic Operations)

为了避免竞争条件的产生，我们要使用一个不受中断而完成的操作：原子操作。

举个函数的例子：

```c
int flag = 0;
returnType functionName(parameters)
{
    while(flag != 0);
    flag = 1;
    /*
    	do something here
    */
    flag = 0;
}
```

上述代码，大致有一个思路，就是让两个线程在执行的时候考虑 flag 的值，如果另一个线程标记为了 1，则让它执行，直到 flag 变为 0，自己执行。但是 flag 的标记实际上不是一个原子操作，这样依旧会出现问题。

在硬件中，我们有 Test 指令和 Set 指令来进行标记。在操作系统中，提供了更高阶的机制可以让程序取代 Test 和 Set。（我的想法：可以用高级语言中的 lock 函数来解决这个问题，也就是给 flag 变量上锁）



____

以上就是第一章中个人认为比较重点的内容了，可能后续细读后还会添加新内容。