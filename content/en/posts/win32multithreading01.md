---
title: 'Reading Notes on Multithreading Applications in Win32 (Part 1)'
date: 2020-03-29T13:42:00
categories: [Systems Programming]
tags: [win32, multithreading, notes]
toc: true
aiTranslated: true
cnblogs: 12591945
---

> Originally published on my old cnblogs blog: [《Win32多线程程序设计》读书笔记（一）](https://www.cnblogs.com/lazy-v/p/12591945.html) (written 2020-03-29).

# Chapter 1

## Definition of Multithreading

According to the book, the simple, big-picture definition is:



**Multithreading lets a program split up its work so that the pieces run independently without affecting each other.**





Wikipedia's definition is:



In [computer architecture](https://en.wikipedia.org/wiki/Computer_architecture), **multithreading** is the ability of a [central processing unit](https://en.wikipedia.org/wiki/Central_processing_unit) (CPU) (or a single core in a [multi-core processor](https://en.wikipedia.org/wiki/Multi-core_processor)) to provide multiple [threads of execution](https://en.wikipedia.org/wiki/Thread_(computer_science)) concurrently, supported by the [operating system](https://en.wikipedia.org/wiki/Operating_system).



In other words,

**Multithreading is the ability of multiprocessor machines and multi-core processors to run multiple threads in parallel, carried out by the operating system.**

<!--more-->

## Threads vs. Processes

A thread is the smallest unit the operating system schedules. A process, on the other hand, is one execution of a program, and it can own memory, handles, threads, and more. So in the OS, a thread is a smaller unit than a process; a process can own many threads, and those threads all get access to the shared resources of the process they belong to.



## Why Use Multithreading

A web server has thousands of clients accessing it at the same time. Without multithreading it couldn't respond in time, and for clients it would feel like waiting in line.

In an app that doesn't use multithreading, the UI (User Interface) and the logic all live on the main thread, so while your logic is hogging the main thread, the UI stops responding. An app like that is guaranteed to have a terrible user experience.



## Multithreading == Efficiency?

Not necessarily. Multithreading can also mean twice the effort for half the result. If threads are handled poorly, the experience can end up awful.



## Why Multiple Processes Don't Work

A process's window has a handle. You can think of a handle as an identifier for an instance within an application, kind of like a pointer. With multiple processes, you'd need to hand the current process's handle over to another process so they could access each other's resources. But that's impossible, because a handle is only meaningful within the pool it was born in (i.e. the process it belongs to). Sure, you can create a copy of a handle and share it with other processes, but that's actually very inefficient, so multiple processes don't work.



## Context Switch

In a preemptive multitasking system, the OS makes sure every thread gets a chance to run. So, using a hardware timer, if a thread has been running long enough, an interrupt is raised, making the CPU copy the thread's current state (the contents of its registers) onto the stack, and then copy it from the stack into a Context structure for later use.



To complete a thread switch, the OS first switches to the memory of the process the thread belongs to, and then restores the register values the thread saved in its context structure. That's a context switch.



## Race Conditions

In a preemptive multitasking system, control is forcibly transferred, so the order in which two threads execute is unpredictable, which gives rise to race conditions.

For example, client A is editing `a.cpp`

```c++
#include <iostream>
using namespace std;

int main()
{
    //Nothing written here
    return 0;
}
```



Meanwhile, client B is also editing the same `a.cpp`

```c++
#include <iostream>
using namespace std;

int main()
{
    cout << "Hello, world!" << endl;
    return 0;
}
```

A's content is shorter, so A finishes typing and saves first.

B finishes typing later and saves.

In the end, `a.cpp` contains B's edits, and A's content has been overwritten.

But if A and B swapped what they were typing, it would be B's content that gets overwritten instead.

You don't know how long A's and B's content is or how long it will take them, so the result is unpredictable.

That's a race condition.



## Atomic Operations

To avoid race conditions, we need an operation that completes without being interrupted: an atomic operation.

Here's an example function:

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

The rough idea of the code above is to have both threads check the value of flag when they run. If the other thread has set it to 1, let that thread run until flag goes back to 0, then run yourself. But setting flag is not actually an atomic operation, so this still runs into problems.

In hardware, we have Test and Set instructions for this kind of marking. The operating system provides higher-level mechanisms that let programs replace Test and Set. (My thought: you could solve this with a lock function in a high-level language, i.e. put a lock on the flag variable.)



____

That's what I personally consider the key content of Chapter 1. I may add more after reading it more carefully.
