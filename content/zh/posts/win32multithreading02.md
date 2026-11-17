---
title: '《Win32 多线程程序设计》读书笔记（二）'
date: 2020-03-29T14:49:00
categories: [系统编程]
tags: [win32, multithreading, notes]
toc: true
cnblogs: 12592275
---

> 本文最初发表于我在博客园的旧博客：[《Win32 多线程程序设计》读书笔记（二）](https://www.cnblogs.com/lazy-v/p/12592275.html)（写于 2020-03-29）。

# 第二章

> 这章开始，正式进入 win32 多线程编程

<!--more-->

## 创建线程

我们看看以下代码

```c++
#include <stdio.h>
#include <Windows.h>

DWORD WINAPI ThreadFunc(LPVOID);

int main()
{
    HANDLE hThread;
    DWORD threadId;

    hThread = CreateThread(NULL,
        0,
        ThreadFunc,
        0,
        0,
        &threadId
    );

    printf("Thread is running...\n");
    for (int i = 0; i < 20; i++)
        printf("Main:%d\n", i + 1);
    return 0;
}

DWORD WINAPI ThreadFunc(LPVOID p)
{
    for (int i = 0; i < 20; i++)
        printf("Thread:%d\n", i+1);

    return 0;
}
```

其中，`DWORD` 表示一个 `双字(Double Word)`，而一个 `字(Word)` 代表两个 `字节(Byte)`，所以 **`DWORD` 表示 `4` 个字节，共 `32` 位(bit)。也就是 `unsigned long`。**你会发现原定义是 `typedef unsigned long DWORD;`。这里的 `DWORD` 是函数返回值类型。

`WINAPI` 实际上是 `_stdcall`，代表函数的调用形式。

`LPVOID` 实际上是 `void far*` 类型，是一种指针类型，而 far 类型和 near 类型实际上只在 `16` 位机上需要用到，far 原本的作用是让指针指向另一个段内地址。**在 `32` 位机中没有 far 和 near 的区别**。

`HANDLE` 表示句柄，即某个资源的标识符，此时用于标识线程，因为我们要创建线程。

**CreateThread** 的函数原型为:

```c++
HANDLE CreateThread(
	LPSECURITY_ATTRIBUTES lpThreadAttributes,
    DWORD dwStatckSize,
    LPTHREAD_START_ROUTINE lpStartAddress,
    LPVOID lpParameter,
    DWORD dwCreationFlags,
    LPDWORD lpThreadId
);
```

其中，`lpThreadAttributes` 描述线程的 **security** (安全) 属性，`NULL` 表示缺省。

`dwStatckSize` 描述线程堆栈的大小，`0` 表示缺省：`1`**MB**。

`lpStartAddress` 描述开始的起始地址，即**函数指针**。

`lpParameter` 作为参数，传入上面函数指针指定的函数中。

`dwCreationFlags` 运行线程暂时挂起，默认情况是立即执行。

`lpThreadId` 产生的**线程的 id** 会被传回到这里。



所以，最上面的代码，就是一个默认的开启线程，执行 **ThreadFunc** 函数的程序。



运行结果：

![单线程结果](/img/o_200329061400%E5%BC%80%E5%90%AF%E7%BA%BF%E7%A8%8B.png)



可以发现，主线程和新开启的线程之间的执行顺序是未知的，这是根据操作系统的分配策略而产生的结果。



## 创建多个线程

我们知道了 **CreateThread** 函数可以创建线程，返回一个句柄，那么我们就可以通过 `for` 循环来生成多个线程，并进行分析：

```c++
#include <stdio.h>
#include <Windows.h>

DWORD WINAPI MyThreadFunction(LPVOID);

int main()
{
    HANDLE hThread;
    DWORD threadId;

    for (int i = 0; i < 5; i++)
    {
        hThread = CreateThread(NULL,
            0,
            MyThreadFunction,
            (LPVOID)(i+1),
            0,
            &threadId
        );

        if (hThread)
        {
            printf("Thread%d launched...\n", i+1);
        }
    }

    Sleep(3000);
    return 0;
}

DWORD WINAPI MyThreadFunction(LPVOID p)
{
    for (int i = 0; i < 10; i++)
        printf("%d\n", (int)p);
    return 0;
}
```

之前提到 **CreateThread** 函数可以给要调用的函数传参数，这里用强制类型转换：`(LPVOID)(i+1)`，**如果不强转，是会报错的**。

`Sleep(3000);` 让主函数在结束前休止 3 秒钟，目的是等候所有线程均启动并执行完毕，否则可能有的线程还未启动或还未执行完毕主函数就返回了。

结果为:

![多线程结果](/img/o_200329114839%E5%BC%80%E5%90%AF%E5%A4%9A%E7%BA%BF%E7%A8%8B.png)

1 到 5 都无序地被打印了 10 次。虽然是 Thread1-5，但实际上第二次运行可能是 Thread1 2 4 3 5 也说不准。

如果我们 `printf("%d%d%d%d%d%d%d%d\n",(int)p,(int)p,(int)p,(int)p,(int)p,(int)p,(int)p,(int)p);`，那么可能还会出现 `333344444444` 或 `3333` 的情况，这就是**竞争条件**。

无序的原因，正是因为之前提到的：**无法预测**。

我们的任务就是学会从多线程程序中获得可预期的结果，这也是**《Win32 多线程程序设计》**这本书要教我们的内容。

上面的问题体现了目前**多线程程序的几个特点**：

1. 无法预期
2. 执行次序无法保证
3. Task Switches 可能随时随地发生
4. 线程对小的改变高度敏感
5. 线程并不总是立刻启动



## 核心对象 (Kernel Objects)

**CreateThread** 函数返回的变量是一个**句柄 **(Handle)，它还通过参数输出了一个**线程 id**(Thread ID)。

线程 id 可以**独一无二地表示**系统任意进程中的某个线程。

句柄被称为**核心对象** (Kernel Objects)，由 **KERNEL32.DLL** 管理。它其实是一个指针，指向操作系统内存空间中的某个东西，但你没有权限直接获取那个东西，这是出于维护操作系统的完整性和安全性。

### Win32 核心对象清单:

- 进程 (processes)
- 线程 (threads)
- 文件 (files)
- 事件 (events)
- 信号量 (semaphores)
- 互斥器 (mutexes)
- 管道 (pipes。分为 named 和 anonymous 两种)



### GDI 对象和核心对象的不同点

**GDI 对象**有单一拥有者，不是进程就是线程。

**核心对象**可以有一个以上的拥有者，可以跨进程。核心对象保持了一个**引用计数** (reference count) 来记录有多少 handles 对应到此对象，对象也同时记录哪一个进程或者线程是拥有者。调用类似 **CreateThread** 这种传回 handle 的函数，count 会加 1，调用 **CloseHandle** 函数，count 会减 1，一旦 count 为 0，核心对象即**销毁**。



### CloseHandle 的重要性

完成工作后，应该调用 **CloseHandle** 函数释放核心对象。

**CloseHandle** 的函数原型为:

```c++
BOOL CloseHandle(
	HANDLE hObject
);
```

`hObject` 代表一个已经打开的对象 handle。

如果成功，返回 `TRUE`，后则返回 `FALSE`，如果失败，可以调用 **GetLastError** 获取到失败的原因。

如果我们没有事后 **CloseHandle** 的习惯，虽然操作系统会自动把 count 减 1，但是我们自己的逻辑就会出问题。

如果一个进程频繁产生 **worker 线程**，我们总是不关闭线程的 handle，则会把它们全部堆给操作系统去“善后”，操作系统帮我们清理，这样则会出现**资源泄露** (resource leaks)。这不是我们期望的结果。

>**tips:**
>
>worker 线程：指完全不牵扯到**图形用户接口** (GUI)，**只做运算**的线程。



### 优化之前的代码

了解了 **CloseHandle** 的重要性，我们就要优化之前的代码，加入 **CloseHandle** 了。

```c++
#include <stdio.h>
#include <Windows.h>

DWORD WINAPI MyThreadFunction(LPVOID);

int main()
{
    HANDLE hThread;
    DWORD threadId;

    for (int i = 0; i < 5; i++)
    {
        hThread = CreateThread(NULL,
            0,
            MyThreadFunction,
            (LPVOID)(i+1),
            0,
            &threadId
        );

        if (hThread)
        {
            printf("Thread%d launched...\n", i+1);
            //call CloseHandle here.
            CloseHandle(hThread);
        }
    }

    Sleep(3000);
    return 0;
}

DWORD WINAPI MyThreadFunction(LPVOID p)
{
    for (int i = 0; i < 10; i++)
        printf("%d\n", (int)p);
    return 0;
}
```

这样的代码，才更加严谨。



### 线程核心对象和线程的区别

线程的 handle 指向 “线程核心对象” ，而不指向线程本身。所以，**可以在线程结束前关闭其 handle**，正如上面的代码中，我们实际在线程结束前就关闭了它的 handle。

线程对象的默认引用计数是 2，调用 **CloseHandle**，count 减 1，线程结束，count 减 1，**只有这两件事情都发生，这个线程对象才会被真正清除。**



## 线程结束代码 (Exit Code)

之前的代码用 **Sleep** 函数来等待线程执行完毕，但实际上，如果 CPU 忙碌，可能等待结束时线程还在执行。

所以我们有个新的函数 **GetExitCodeThread** 可以用：

```c++
BOOL GetExitCodeThread(
	HANDLE hThread,
    LPDWORD lpExitCode
);
```

其中，`hThread` 是要传入的线程的 handle。

`lpExitCode` 是一个指向 `DWORD` 的指针，用以接受**结束代码** (exit code)。

成功返回 `TRUE`，不成功返回 `FALSE` 并可用 **GetLastError** 获取错误信息。如果线程结束，则 `lpExitCode` 带回结束代码，否则带回 `STILL_ACTIVE`。

需要特别注意的是，不能通过 **GetExitCodeThread** 函数的返回值来判断一个线程是否结束，因为在一个线程还没有所谓的结束代码时，它就返回 `TRUE` 了。所以，**不能从它的返回值知道线程在运行，还是已经结束，但返回值是 `STILL_ACTIVE`。**



## 强制结束一个线程

如果想要暴力一点，可以用 **ExitThread** 函数，它的原型为：

```c++
VOID ExitThread(
	DWORD dwExitCode
);
```

`dwExitCode` 指定调用此函数的线程的结束代码。

也就是说，在一个线程调用的函数中，调用这个函数，假设 `ExitThread(6)`，那么，这个线程立即结束，并且结束代码为 6。

需要注意的是，**ExitThread** 函数从不返回任何值，也就是说，调用它以后的任何操作（同一作用域内）将无效。

如果在主线程中使用 **ExitThread** 函数，则会导致主线程结束但"worker 线程"继续存在，这样会跳过 `runtime library` 中的清理(cleanup) 函数，导致已开启的文件没有清理，这样不好。

如果**结束主线程**，则会导致**其他所有线程被强制结束**。

> 主线程(primary thread) ，负责 GUI 消息循环。它的结束会导致程序结束、其他线程被强制关闭，其他线程没有机会被清理。



## MTVERIFY 错误处理

**MTVERIFY** 是一个**宏**，适用于 GUI 程序也适用于 Console 程序。它实际上是记录并解释 **Win32 GetLastError()** 而获得描述。如果 Win32 函数失败，MTVERIFY 会打印出简短的文字说明。

使用方法，就是 MTVERIFY(`...`)，其中 `...` 是一个 Win32 函数。比如 `MTVERIFY(CloseHandle(hThrd));`



## 微软的多线程模型

线程分为 **GUI 线程**和 **worker 线程**两种。

GUI 线程负责建造窗口以及处理消息循环。

worker 线程负责执行纯粹运算工作。



## 多线程设计的成功关键

1. 各线程的数据要分离开，避免使用全局变量
2. 不要在线程之间共享 GDI 对象
3. 确定你知道你的线程状态，不要径自结束程序而不等待它们的结束
4. 让主线程处理用户界面(UI)
