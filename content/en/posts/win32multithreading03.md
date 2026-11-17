---
title: 'Reading Notes on Multithreading Applications in Win32 (3)'
date: 2020-04-13T14:08:00
categories: [Systems Programming]
tags: [win32, multithreading, notes]
toc: true
original: true
cnblogs: 12691052
aiTranslated: true
---

> Reposted from my old cnblogs blog: [《Win32多线程程序设计》读书笔记（三）](https://www.cnblogs.com/lazy-v/p/12691052.html) (written 2020-04-13); formatting tidied during migration.

Chapter 3: busy waiting, the performance monitor, WaitForSingleObject and signaled objects.

<!--more-->

# Chapter 3

## Busy Waiting

Busy waiting here means calling **GetExitCodeThread** over and over until the result is no longer **STILL_ACTIVE**. It wastes a huge amount of CPU time.

The simplest example:

```cpp
...
GetExitCodeThread(hThrd, &exitCode)
while(STILL_ACTIVE == exitCode);
...
```

That's busy waiting.

While busy waiting, the main thread just sits in that **while** loop checking whether **exitCode** still equals **STILL_ACTIVE**, which is a total waste of time! Worse, this one program can starve other processes of resources and make other applications stutter. A disaster!

So never busy-wait.

## Performance Monitor

Windows 10 still has a system app with the performance-monitor features of good old NT and 95.

That's today's **Task Manager**, where you can watch each process's resource usage, performance and so on.

## Waiting for a thread to finish

Win32 provides a function called **WaitForSingleObject**, which can be used to wait until a thread finishes.

```cpp
DWORD WaitForSingleObject(
    HANDLE hHandle,
    DWORD dwMilliseconds
);
```

`dwMilliseconds` is the maximum time to wait; if it runs out before the handle becomes signaled, the function returns anyway. `0` means return immediately; **INFINITE** means wait forever.

If the function fails, it returns **WAIT_FAILED**, and **GetLastError** gives the error details.

On success, if the kernel object being waited on becomes signaled, it returns **WAIT_OBJECT_0**;

if the wait times out before the kernel object becomes signaled, it returns **WAIT_TIMEOUT**;

if a thread that owns a **mutex** ends without releasing it, it returns **WAIT_ABANDONED**.

With this function, the earlier code can be improved:

```cpp
WaitForSingleObject(hThrd, INFINITE);
```

## Signaled Objects

The kernel objects that **WaitForSingleObject** can wait on have two states: signaled and nonsignaled.

When a kernel object becomes signaled, **WaitForSingleObject** wakes up. The other **Wait** functions work the same way.

**While a thread is running, its thread object is nonsignaled; when the thread ends, the thread object becomes signaled.**
