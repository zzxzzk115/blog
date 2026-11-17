---
title: '《Win32 多线程程序设计》读书笔记（三）'
date: 2020-04-13T14:08:00
categories: [系统编程]
tags: [win32, multithreading, notes]
toc: true
original: true
cnblogs: 12691052
---

> 本文转载自我在博客园的旧博客：[《Win32 多线程程序设计》读书笔记（三）](https://www.cnblogs.com/lazy-v/p/12691052.html)（写于 2020-04-13），迁移时整理了格式。

第三章：忙等、性能监视器、WaitForSingleObject 与被激发的对象。

<!--more-->

# 第三章

## 忙等 Busy Waiting

忙等，在这里就是不断调用 **GetExitCodeThread** 函数，直到结果不再是 **STILL_ACTIVE**，它十分浪费 CPU 时间。

举个最简单的例子：

```cpp
...
GetExitCodeThread(hThrd, &exitCode)
while(STILL_ACTIVE == exitCode);
...
```

这就是忙等。

处于忙等会让主线程一直处于这个 **while** 循环中去判断 **exitCode** 的值是否等于 **STILL_ACTIVE**，这实在是太浪费时间了！不仅如此，你可能由于这一个程序，导致其他进程资源被抢占，也就是其他应用卡顿，这简直是灾难！

所以千万不要用忙等。

## 性能监视器 (Performance Monitor)

在现在的 Windows 10 系统中依旧有原来老 NT 老 95 的性能监视器的功能的系统应用。

也就是现在的 **任务管理器 (Task Manager)**，里面可以监视各个进程占用资源情况，性能情况等。

## 等待一个线程的结束

Win32 提供了一个名为 **WaitForSingleObject** 的函数，能够在某个线程结束时被调用。

```cpp
DWORD WaitForSingleObject(
    HANDLE hHandle,
    DWORD dwMilliseconds
);
```

`dwMilliseconds` 指等待的最长时间，如果到了最长时间，handle 尚未成为激发状态，则还是要返回。指定 `0`，表示立即返回；指定 **INFINITE** 表示无穷等待。

如果函数失败，返回 **WAIT_FAILED**，可以用 **GetLastError** 获取错误信息。

函数成功时，如果等待的目标核心对象变成激发状态，返回 **WAIT_OBJECT_0**；

如果等待的核心对象变成激发态之前，等待时间过了，则返回 **WAIT_TIMEOUT**；

如果一个拥有 **mutex（互斥器）** 的线程结束前没有释放 mutex，则传回 **WAIT_ABANDONED**。

通过这个函数，就可以改良之前的代码：

```cpp
WaitForSingleObject(hThrd, INFINITE);
```

## 被激发的对象 (Signaled Objects)

可被 **WaitForSingleObject** 使用的核心对象有两种状态：激发与未激发。

当核心对象被激发时，会导致 **WaitForSingleObject** 醒来。**Wait** 也是如此。

**线程执行时，线程对象处于未激发状态；线程结束时，线程对象就被激发。**
