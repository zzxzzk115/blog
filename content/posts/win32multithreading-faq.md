---
title: 《Win32多线程程序设计》FAQ整理
date: 2021-05-26T17:55:30
categories: [Tech]
tags: [win32, multithreading, faq]
toc: true
---

# FAQ整理

## FAQ 01： 合作型(cooperative)多任务与抢占式(preemptive)多任务有何不同？

合作型(cooperative)多任务是指由程序员来控制程序如何分享CPU资源，多个程序之间需要适当分享CPU资源，一旦一个程序拒绝与其他程序共享资源而占用所有资源的话，其它程序则无法做任何事情。即可控权不在操作系统，而在程序。

> **提示**
>
> Windows 1、2、3为合作型多任务操作系统

抢占式(preemptive)多任务是指由操作系统来控制程序如何分享CPU资源，无需程序员操心CPU资源共享的问题。即可控权在操作系统而不在程序。

> **提示**
>
> Unix、VMS、AmigaDOS等为抢先式操作系统

## FAQ 02：我可以在Win32s中使用多个线程吗？

不可以。Win32s是Win32 API在Windows 3.1中的移植，但是不幸的是许多功能没有办法移植。Win32s既不支持抢先式多任务也不支持多线程。

> **提示**
>
> 在Windows NT及以后版本中可以使用多线程。

## FAQ 03：线程和进程有什么不同？

进程含有内存和资源，其中资源包括内核对象。线程是内核对象的一种，即进程包含线程。一个进程可以拥有多个线程。进程本身并不能够执行，它只提供一个安置内存和线程的地方。线程才是真正被操作系统调度的单元，它用来执行一段程序。

> **提示**
>
> 进程是资源分配的最小单位，线程是CPU调度的最小单位。

## FAQ 04：线程在操作系统中携带多少“行李”？

携带了在”任何时刻下的状态“，即线程上下文结构，定义在进程的某块内存或者CPU寄存器中。

## FAQ 05：Context Switch是怎样发生的？

当硬件计时器认为某个线程已经执行够久了，就会发出一个中断，于是CPU取得目前这个线程的当前状态，也就是把所有寄存器内容拷贝到堆栈之中，再把它从堆栈拷贝到一个CONTEXT结构，以备以后再用。

当切换线程时，Context Switch便发生，操作系统会切换当前线程所属进程的内存，恢复该线程放在CONTEXT结构中寄存器值。

## FAQ 06：为什么我应该调用CloseHandle()？

因为调用CloseHandle能避免内存泄漏。内核对象采用引用计数方式管理内存。当一个Handle引用到一个内核对象时，它的引用计数+1。当计数为0时，内核对象被销毁，内存被回收。CloseHandle让某Handle引用的内核对象引用计数减一。如果一个Handle的工作结束了，但不使用CloseHandle，会导致该Handle引用的内核对象引用计数始终不会为0，即发生了资源泄露(resource leaks)或内存泄漏(memory leaks)。

## FAQ 07：为什么可以在不结束线程的情况下关闭其handle？

因为CloseHandle的工作仅仅是将该Handle引用的内核对象引用计数减一，而并非清理内核对象。线程的Handle指向线程的内核对象，而不是线程本身。所以在不结束线程的情况下，可以关闭其handle。线程的内核对象当且仅当所有Handle被关闭且线程结束的时候，引用计数降为0，内核对象被清理。

> **提示**
>
> 当线程结束时，引用计数减一。

## FAQ 08：如果线程还在运行而我的程序结束了，会怎样？

程序结束即主线程结束，会导致其他所有线程被迫结束，并且没有机会做清理工作。

## FAQ 09：什么是MTVERIFY？

侯老自己写的宏，内部记录并解释了Win32GetLastError()的结果，如果Win32函数失败则该宏打印一段简短的文字说明。

## FAQ 10：我如何得知一个内核对象时否处于激发状态？

调用WaitForSingleObject函数，将dwMilliseconds参数设置为0。这样会立即返回内核对象的状态。

## FAQ 11：什么是一个被激发的对象？

内核对象默认是未激发的对象，当它的内部状态有所改变时，则变为一个被激发的对象。

例如线程正在执行的时候，线程的内核对象处于未激发状态，当线程结束时，线程的内核对象被激发，此时线程的内核对象就是被激发的对象。

不同种类的内核对象，是否激发的判断条件不同。

## FAQ 12：”激发“对于不同的内核对象有什么不同的意义？

| 对象                | 说明                                                         |
| ------------------- | ------------------------------------------------------------ |
| Thread*（线程）     | 当线程结束时，线程对象即被激发。当线程还在进行时，则对象处于未激发状态。线程对象系由CreateThread() 或 CreateRemoteThread() 产生 |
| Process*（进程）    | 当进程结束时，进程对象即被激发。当进程还在进行时，则对象处于未激发状态。 CreateProcess() 或OpenProcess() 会传回一个进程对象的 handle |
| Change Notification | 当一个特定的磁盘子目录中发生一件特别的变化时，此对象即被激发。此对象系由 FindFirstChangeNotification()产生 |
| Console Input*      | 当 console 窗口的输入缓冲区中有数据可用时，此对象将处于激发状态。CreateFile() 和 GetStdFile() 两函数可以获得 console handle |
| Event*              | Event 对象的状态直接受控于应用程序所使用的三个Win32 函数：SetEvent()、PulseEvent()、ResetEvent()。CreateEvent() 和 OpenEvent() 都可以传回一个 event object handle 。Event 对象的状态也可以被操作系统设定——如果使用于“overlapped”操作时 |
| Mutex*              | 如果 mutex 没有被任何线程拥有，它就是处于激发状态。一旦一个等待 mut ex 的函数返回了，mutex 也就自动重置为未激发状态。CreateMutex() 和 OpenMutex()都可以获得一个 mutex handle |
| Semaphore*          | Semaphore 有点像 mutex，但它有个计数器，可以约束其拥有者（线程）的个数。当计数器内容大于0时，semaphore 处于激发状态，当计数器内容等于0时，semaphore 处于未激发状态。 CreateSemaphore() 和OpenSemaphore() 可以传回一个 semaphore handle |

## FAQ 13：我如何在主线程中等待一个handle？

使用MsgWaitForMultiObjects修改主消息循环。

## FAQ 14：如果线程在critical sections中停很久，会怎样？

不会怎样，操作系统不会当掉。用户不会获得任何错误信息。最坏你情况是主线程需要使用这被锁定的资源时，程序会挂在那儿，动也不动。

## FAQ 15：如果线程在critical sections中结束，会怎样？

临界段资源一直不能被释放，可能出现死锁。

## FAQ 16：我如何避免死锁？

采用一次等两个资源的办法（即要不统统获得，要不统统没有）。

## FAQ 17：我能够等待一个以上的critical sections吗？

不能！

## FAQ 18：谁才拥有semaphore？

semaphore没有拥有权的观念。如果锁定成功，你也不会收到semaphore的拥有权。因为可以有一个以上的线程同时锁定一个semaphore，所以谈semaphore的拥有权并没有多少意义，即semaphore没有所谓的“独占锁定”，没有拥有权的观念。

## FAQ 19：Event Object有什么用途？

Event Object大有用途，因为它们的状态完全由程序控制，不会像mutex和semaphore那样因为WaitForSingleObject()之类的函数调用而变化状态。你可以精确告诉Event对象做什么事，什么时候去做。

Event Object被运用在多种高级I/O操作中。

## FAQ 20：如果我对着一个event对象调用PulseEvent()并且没有线程正在等待，会怎样？

该event对象会被遗失。也可能引起死锁。

## FAQ 21：什么是overlapped I/O？

overlapped I/O是Win32的一项技术，你可以要求操作系统为你传送数据，并且在传送完毕时通知你。这项技术使你的程序在I/O进行过程中仍然能继续处理事务。

## FAQ 22：Overlapped I/O在Windows 95上有什么限制？

只适用于named pipes，mailslots，serial I/O，以及socket()或accept（）传回来的sockets，它并不支持磁盘或光盘中的文件操作。

## FAQ 23：我能够以C runtime library使用overlapped I/O吗？

你将不可能藉由C runtime library中的stdio.h函数而使用overlappedI/O。例如你不可能使用fwrite，而只能使用WriteFile实现overlapped I/O。

## FAQ 24：Overlapped I/O总是异步地(asynchronously)执行吗？

不总是。如果数据被已经被放进cache中，或者如果操作系统认为它可以很快地取得那份数据，那么文件操作就会在ReadFile()返回之前完成，而ReadFile将传回TRUE。这种情况下，文件handle处于激发状态，而对文件的操作可以被视为就像overlapped一样。

## FAQ 25：我应该如何为overlapped I/O产生一个event对象？

必须创建手动重置(ManualReset)事件的对象，如果是自动重置(AutoReset)事件的对象，可能会产生Race Condition，因为系统内核可能在你有机会等待该event对象之前先激发它，它的激发状态将会遗失，Wait...()函数永不返回。但是手动重置的事件对象，一旦激发，就一直处于激发状态，等候你手动重置它为未激发状态。