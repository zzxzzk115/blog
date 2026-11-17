---
title: 'FAQ Notes for Multithreading Applications in Win32'
date: 2021-05-26T17:55:30
categories: [Systems Programming]
tags: [win32, multithreading, faq]
toc: true
aiTranslated: true
---

# FAQ notes

## FAQ 01: What's the difference between cooperative multitasking and preemptive multitasking?

Cooperative multitasking means the programmer controls how programs share the CPU. Multiple programs have to share the CPU appropriately, and once one program refuses to share and hogs everything, the other programs can't do anything. In other words, control lies with the programs, not the operating system.

> **Tip**
>
> Windows 1, 2 and 3 were cooperative multitasking operating systems.

Preemptive multitasking means the operating system controls how programs share the CPU, so programmers don't have to worry about sharing the CPU. In other words, control lies with the operating system, not the programs.

> **Tip**
>
> Unix, VMS, AmigaDOS and others are preemptive operating systems.

## FAQ 02: Can I use multiple threads in Win32s?

No. Win32s is a port of the Win32 API to Windows 3.1, but unfortunately a lot of functionality couldn't be ported. Win32s supports neither preemptive multitasking nor multithreading.

> **Tip**
>
> You can use multithreading in Windows NT and later.

## FAQ 03: What's the difference between a thread and a process?

A process contains memory and resources, and those resources include kernel objects. A thread is a kind of kernel object, i.e. processes contain threads. A process can have multiple threads. A process can't execute by itself; it just provides a place to hold memory and threads. The thread is the unit the operating system actually schedules, and it's what executes a piece of code.

> **Tip**
>
> The process is the smallest unit of resource allocation; the thread is the smallest unit of CPU scheduling.

## FAQ 04: How much "baggage" does a thread carry in the operating system?

It carries its "state at any given moment", i.e. the thread context structure, which lives in some block of the process's memory or in CPU registers.

## FAQ 05: How does a context switch happen?

When the hardware timer decides a thread has run long enough, it raises an interrupt. The CPU then captures the current state of the thread, i.e. it copies all the register contents onto the stack, and then copies them from the stack into a CONTEXT structure for later use.

A context switch happens when switching threads: the operating system switches to the memory of the process the new thread belongs to, and restores that thread's register values from its CONTEXT structure.

## FAQ 06: Why should I call CloseHandle()?

Because calling CloseHandle avoids memory leaks. Kernel objects manage their memory with reference counting. When a handle refers to a kernel object, its reference count goes up by one. When the count hits 0, the kernel object is destroyed and its memory reclaimed. CloseHandle decrements the reference count of the kernel object the handle refers to. If you're done with a handle but don't call CloseHandle, the reference count of the kernel object it refers to will never reach 0, i.e. you get a resource leak or memory leak.

## FAQ 07: Why can I close a thread's handle without ending the thread?

Because all CloseHandle does is decrement the reference count of the kernel object the handle refers to; it doesn't clean up the kernel object. A thread handle points to the thread's kernel object, not the thread itself. That's why you can close its handle without ending the thread. The thread's kernel object's reference count drops to 0, and the kernel object is cleaned up, if and only if all its handles have been closed and the thread has ended.

> **Tip**
>
> When a thread ends, the reference count goes down by one.

## FAQ 08: What happens if a thread is still running when my program ends?

The program ending means the primary thread ends, which forces all other threads to end, with no chance to do any cleanup.

## FAQ 09: What is MTVERIFY?

A macro written by Mr. Hou (the book's Chinese translator) himself. Internally it records and interprets the result of Win32 GetLastError(), and if a Win32 function fails, the macro prints a short text explanation.

## FAQ 10: How do I find out whether a kernel object is signaled?

Call WaitForSingleObject with the dwMilliseconds parameter set to 0. It returns the kernel object's state immediately.

## FAQ 11: What is a signaled object?

Kernel objects are nonsignaled by default; when their internal state changes, they become signaled objects.

For example, while a thread is running, its kernel object is nonsignaled; when the thread ends, the thread's kernel object becomes signaled, and at that point it's a signaled object.

Different kinds of kernel objects have different conditions for whether they're signaled.

## FAQ 12: What does "signaled" mean for different kernel objects?

| Object              | Description                                                  |
| ------------------- | ------------------------------------------------------------ |
| Thread*             | A thread object becomes signaled when the thread ends. While the thread is still running, the object is nonsignaled. Thread objects are created by CreateThread() or CreateRemoteThread() |
| Process*            | A process object becomes signaled when the process ends. While the process is still running, the object is nonsignaled. CreateProcess() or OpenProcess() returns a handle to a process object |
| Change Notification | This object becomes signaled when a particular kind of change happens in a specific disk directory. It's created by FindFirstChangeNotification() |
| Console Input*      | This object is signaled when there's data available in the console window's input buffer. The CreateFile() and GetStdFile() functions can get a console handle |
| Event*              | An Event object's state is directly controlled by the application through three Win32 functions: SetEvent(), PulseEvent() and ResetEvent(). CreateEvent() and OpenEvent() can both return an event object handle. An Event object's state can also be set by the operating system, when it's used for "overlapped" operations |
| Mutex*              | A mutex is signaled if it isn't owned by any thread. As soon as a function waiting on the mutex returns, the mutex is automatically reset to nonsignaled. CreateMutex() and OpenMutex() can both get a mutex handle |
| Semaphore*          | A semaphore is a bit like a mutex, but it has a counter that limits the number of its owners (threads). When the counter is greater than 0, the semaphore is signaled; when the counter equals 0, the semaphore is nonsignaled. CreateSemaphore() and OpenSemaphore() can return a semaphore handle |

## FAQ 13: How do I wait on a handle in the primary thread?

Use MsgWaitForMultiObjects to modify the main message loop.

## FAQ 14: What happens if a thread stays in a critical section for a long time?

Nothing much: the operating system won't crash, and the user won't get any error message. The worst case is that when the primary thread needs the locked resource, the program just hangs there, completely frozen.

## FAQ 15: What happens if a thread ends inside a critical section?

The critical section's resource can never be released, which may lead to deadlock.

## FAQ 16: How do I avoid deadlock?

Wait for both resources at once (i.e. either get them all or get none of them).

## FAQ 17: Can I wait on more than one critical section?

No!

## FAQ 18: Who owns a semaphore?

Semaphores have no notion of ownership. Even if you lock one successfully, you don't receive ownership of the semaphore. Since more than one thread can lock a semaphore at the same time, talking about semaphore ownership doesn't mean much; that is, there's no such thing as an "exclusive lock" on a semaphore, and no notion of ownership.

## FAQ 19: What are Event Objects good for?

Event Objects are very useful, because their state is entirely controlled by the program. Unlike mutexes and semaphores, their state doesn't change because of calls to functions like WaitForSingleObject(). You can tell an Event object exactly what to do and when to do it.

Event Objects are used in many kinds of advanced I/O operations.

## FAQ 20: What happens if I call PulseEvent() on an event object and no threads are waiting?

The event gets lost. It may also cause a deadlock.

## FAQ 21: What is overlapped I/O?

Overlapped I/O is a Win32 technique where you ask the operating system to transfer data for you and notify you when the transfer is done. It lets your program keep doing work while the I/O is in progress.

## FAQ 22: What are the limitations of overlapped I/O on Windows 95?

It only works with named pipes, mailslots, serial I/O, and sockets returned by socket() or accept(); it doesn't support file operations on disks or CD-ROMs.

## FAQ 23: Can I use overlapped I/O with the C runtime library?

You can't use overlapped I/O through the stdio.h functions in the C runtime library. For example, you can't use fwrite; you can only use WriteFile to do overlapped I/O.

## FAQ 24: Is overlapped I/O always performed asynchronously?

Not always. If the data is already in the cache, or if the operating system thinks it can get that data very quickly, the file operation will complete before ReadFile() returns, and ReadFile will return TRUE. In that case the file handle is signaled, and the operation on the file can be treated just as if it were overlapped.

## FAQ 25: How should I create an event object for overlapped I/O?

You must create a manual-reset event object. With an auto-reset event object you can get a race condition: the system kernel may signal it before you've had a chance to wait on the event object, its signaled state gets lost, and the Wait...() function never returns. A manual-reset event object, on the other hand, stays signaled once it's signaled, until you manually reset it to nonsignaled.
