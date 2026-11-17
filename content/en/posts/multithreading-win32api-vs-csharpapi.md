---
title: 'Mapping Win32 Multithreading APIs to C# Multithreading APIs'
date: 2021-06-15T18:47:27
categories: [Systems Programming]
tags: [Win32, Multithreading, CSharp]
toc: true
aiTranslated: true
---

> In this post I summarize how the Win32 API and the C# API map to each other for multithreading. They're often similar, but there are some differences too.

# Threads

## Creating a thread

When you create a thread, you usually need to specify "what it does", i.e. supply a function pointer or a delegate.

Win32 uses the CreateThread function to create a thread:

```cpp
HANDLE CreateThread(
    PSECURITY_ATTRIBUTES pThreadAttributes,
    DWORD dwStackSize,
    PTHREAD_START_ROUTINE pStartAddress,
    PVOID pParameter,
    DWORD dwCreationFlags,
    PDWORD pdwThreadId
)
```

C# wraps threads up, and you create one with a statement like this:

```csharp
Thread t = new Thread(()=>{
    Console.WriteLine("Hello,Thread");
});
```

For the same task, the two implementations look different:

```cpp
#include <windows.h>

DWORD WINAPI ThreadFunc(LPVOID);

int main()
{
    HANDLE hThread;
    DWORD threadId;
    hThread = CreateThread(NULL, 0, ThreadFunc, 0, 0, &threadId);
    return 0;
}

DWORD WINAPI ThreadFunc(LPVOID p)
{
    int p0 = (int)p;
    printf("Parameter:%d\n", p0);
}
```

```csharp
using System;
using System.Threading;

public class Program{
    public static void Main(string[] args)
    {
        Thread t = new Thread(ThreadFunc);
        t.Start(0);
    }
    
    static void ThreadFunc(Object o)
    {
        int p0 = (int)o;
        Console.WriteLine($"Parameter:{p0}");
    }
}
```

## Forcibly terminating a thread

Every now and then we need to forcibly terminate a thread.

In Win32, a thread can call the ExitThread function to forcibly end the calling thread:

```cpp
VOID ExitThread(DWORD dwExitCode);
```

Win32 can also forcibly end the thread object a HANDLE points to by passing that HANDLE:

```cpp
BOOL TerminateThread(HANDLE hThread, DWORD dwExitCode);
```

C# also has several ways to end a thread:

- Thread's Abort instance method: `t.Abort();`, `Thread.CurrentThread.Abort();`
- `Application.ExitThread();`

## Suspend and Resume

Win32 uses the SuspendThread function to suspend a thread and the ResumeThread function to resume it:

```cpp
DWORD SuspendThread(HANDLE hThread);
DWORD ResumeThread(HANDLE hThread);
```

C# uses Thread's Suspend instance method to suspend a thread and the Resume method to resume it:

```csharp
t.Suspend();
t.Resume();
```

> Suspend and Resume are obsolete.

## Sleep

Win32 uses the Sleep function to put the calling thread to sleep:

```cpp
VOID Sleep(DWORD dwMilliseconds);

Sleep(100);
```

C# uses the Thread.Sleep method to put the calling thread to sleep:

```csharp
Thread.Sleep(100);
```

## Priority

Win32 uses the SetThreadPriority function to set a thread's priority:

```cpp
BOOL SetThreadPriority(
    HANDLE hThread,
    int nPriority
);

SetThreadPriority(THREAD_PRIORITY_ABOVE_NORMAL);
```

Win32 uses the GetThreadPriority function to get a thread's priority:

```cpp
int GetThreadPriority(
    HANDLE hThread
);
```

C# uses the Thread object's Priority property to set and get a thread's priority:

```csharp
t.Priority = ThreadPriority.AboveNormal;
int priority = t.Priority;
```

# Thread synchronization

Thread synchronization generally comes in two flavors: user-mode synchronization and kernel-mode synchronization.

User mode's selling point is speed, because it has nothing to do with the operating system; everything is done in hardware.

Kernel mode relies on the operating system. It's a lot slower than user mode but more capable: with the various kernel objects, we can solve some synchronization problems that user mode can't.

Generally speaking, when solving a thread synchronization problem with the best performance in mind, you should consider user-mode synchronization first, and only turn to kernel-mode synchronization if that doesn't meet your needs.

> C# provides hybrid thread synchronization, which combines user-mode and kernel-mode synchronization, takes the best of both, and also solves some performance problems.
>
> When using C#, if the problem is fairly complex and performance matters, you can use hybrid thread synchronization.

## Thread synchronization in User Mode

### Atomic Access

Atomic access means that while a thread is accessing a resource, it's guaranteed that no other thread accesses the same resource at the same moment.

Win32 provides the Interlocked family of functions to guarantee atomic increment, decrement and exchange operations on variables:

```cpp
LONG InterlockedIncrement(PLONG plAddend);

LONG InterlockeDecrement(PLONG plAddend);

LONG InterlockedExchangeAdd(
    PLONG volatile plAddend,
    LONG lIncrement
);

LONGLONG InterlockedExchangeAdd64(
    PLONGLONG volatile pllAddend,
    LONGLONG llIncrement
);

LONG InterlockedExchange(
    PLONG volatile plTarget,
    LONG lValue
);

LONGLONG InterlockedExchange64(
    PLONGLONG volatile plTarget,
    LONGLONG lValue
);

PVOID InterlockedExchangePointer(
    PVOID* volatile ppvTarget,
    PVOID pvValue
);

PLONG InterlockedCompareExchange(
    PLONG plDestination,
    LONG lExchange,
    LONG lComparand
);

PLONG InterlockedCompareExchange64(
    PLONGLONG pllDestination,
    LONGLONG llExchange,
    LONGLONG llComparand
);

LONG InterlockedCompareExchangePointer(
    PVOID* ppvDestination,
    PVOID pvExchange,
    PVOID pvComparand
);
```

C# wraps this up in the Volatile and Interlocked classes. There are a lot of methods, so check the docs for details:

[C# .NET 5 Document: Volatile](https://docs.microsoft.com/zh-cn/dotnet/api/system.threading.volatile?view=net-5.0)

[C# .NET 5 Document: Interlocked](https://docs.microsoft.com/zh-cn/dotnet/api/system.threading.interlocked?view=net-5.0)

The Volatile class is based on volatile constructs and provides atomic Read/Write operations.

The Interlocked class is based on interlocked constructs and provides atomic add (Add with a positive number, Increment), subtract (Add with a negative number, Decrement) and exchange (Exchange, CompareExchange) operations. Current versions of .NET have also added bitwise operations (Add, Or, Xor) and so on, which makes it even more convenient.

You can implement a Spin Lock with atomic access to achieve thread synchronization, but a spin lock is a Busy Loop, so it's best to avoid synchronizing threads this way.

In Win32 you can implement a spin lock like this:

```cpp
BOOL globalResourceInUse = FALSE;
void Func1() {
    // Wait to access the shared resource
    while(InterlockedExchange(&globalResourceInUse, TRUE) == TRUE)
        Sleep(0);
    
    // Got the shared resource, now run the corresponding logic
    // ......
    
    // Logic's done, give the shared resource back
    InterlockedExchange(&globalResourceInUse, FALSE);
}
```

In C# you can implement a spin lock like this:

```csharp
internal struct SimpleSpinLock
{
    // 0 means false, 1 means true
    private int m_globalResourceInUse = 0;
    
    public void Enter()
    {
        while(true)
        {
            if(Interlocked.Exchange(ref m_globalResourceInUse, 1) == 0)
                return;
            
            // Extra logic, black magic
        }
    }
    
    public void Leave()
    {
        Volatile.Write(ref m_globalResourceInUse, 0);
        // You could also use Interlocked.Exchange(ref m_globalResourceInUse, 0);
    }
}
```

 ### Critical Section

A critical section is a user-mode thread synchronization mechanism. Compared with atomic access, it's not limited to changing the value of a single variable; it can run a whole series of logic. Only one thread at a time can enter a given critical section and run the corresponding logic, and only after that thread leaves the critical section do other threads get a chance to enter it.

Win32 provides four functions to initialize, destroy, enter and leave a critical section respectively:

- Initialize with the InitializeCriticalSection function:

  ```cpp
  VOID InitializeCriticalSection(
      PCRITICAL_SECTION pCriticalSection
  );
  ```

- Destroy with the DeleteCriticalSection function:

  ```cpp
  VOID DeleteCriticalSection(
      PCRITICAL_SECTION pCriticalSection
  );
  ```

- Enter with the EnterCriticalSection function:

  ```cpp
  VOID EnterCriticalSection(
      PCRITICAL_SECTION pCriticalSection
  );
  ```

- Leave with the LeaveCriticalSection function:

  ```cpp
  VOID LeaveCriticalSection(
      PCRITICAL_SECTION pCriticalSection
  );
  ```

C# uses the Monitor.Enter method to enter a critical section:

```csharp
public static class Monitor 
{
    // ..........
    public static extern void Enter(Object obj);
    // ..........
}

// Monitor.Enter usage
int criticalSectionValue;
Monitor.Enter(criticalSectionValue);
```

C# uses the Monitor.Exit method to exit a critical section:

```csharp
public static class Monitor 
{
    // ..........
    public static extern void Exit(Object obj);
    // ..........
}

// Monitor.Exit usage
int criticalSectionValue;
Monitor.Exit(criticalSectionValue);
```

> Win32 critical sections and the critical sections implemented by C#'s Monitor are only similar in functionality; internally they're implemented differently.
>
> The critical sections provided by the Win32 API are implemented in unmanaged Windows code and use a spin lock internally to improve performance.
>
> The critical sections provided by C#'s Monitor are managed and designed around sync blocks. What's more, **Monitor doesn't actually belong to user-mode thread synchronization; it belongs to hybrid thread synchronization.**

## Thread synchronization in Kernel Mode

### Waiting for kernel objects to be signaled

Common kernel objects include:

- Process
- Thread
- File
- Event
- Semaphore
- Mutex
- Pipe

They all have two states: nonsignaled and signaled. Being signaled means their internal state has changed; for a thread, signaled means the thread has ended.

Win32 uses the WaitForSingleObject function to wait for a single kernel object to be signaled:

```cpp
DWORD WaitForSingleObject(
    HANDLE hHandle,
    DWORD dwMilliseconds
);
```

Win32 uses the WaitForMultipleObjects function to wait for multiple kernel objects to be signaled:

```cpp
DWORD WaitForMultipleObjects(
    DWORD dwCount,
    CONST HANDLE *pHandles,
    BOOL bWaitAll,
    DWORD dwMilliseconds
);
```

C# provides the abstract class WaitHandle. Its WaitOne method essentially calls Win32's WaitForSingleObject function, and its WaitAll and WaitAny methods essentially call Win32's WaitForMultipleObjects function:

```csharp
public abstract class WaitHandle : MarshalByRefObject, IDisposable{
    // Internally calls the Win32 WaitForSingleObject function
    public virtual bool WaitOne();
    public virtual bool WaitOne(int millisecondsTimeout);
    public virtual bool WaitOne(TimeSpan timeout);
    
    // Internally calls the Win32 WaitForMultipleObjects function
    public static bool WaitAll(WaitHandle[] waitHandles);
    public static bool WaitAll(WaitHandle[] waitHandles, int millisecondsTimeout);
    public static bool WaitAll(WaitHandles[] waitHandles, TimeSpan timeout);
    
    // Internally calls the Win32 WaitForMultipleObjects function
    public static bool WaitAny(WaitHandles[] waitHandles);
    public static bool WaitAny(WaitHandle[] waitHandles, int millisecondsTimeout);
    public static bool WaitAny(WaitHandles[] waitHandles, TimeSpan timeout);
    
    // WaitAny returns this on timeout
    public const int WaitTimeout = 258;
    
    // Internally calls the Win32 CloseHandle function
    public void Dispose();
}
```

> Note:
>
> WaitHandle is a static abstract class.
>
> The class hierarchy of WaitHandle in the FCL:
>
> - WaitHandle
>   - EventWaitHandle
>     - AutoResetEvent
>     - ManualResetEvent
>   - Semaphore
>   - Mutex
>
> So **instances of AutoResetEvent, ManualResetEvent, Semaphore and Mutex can all call the WaitOne method to wait for the kernel object to be signaled**, and you can also call WaitHandle's public static methods WaitAll and WaitAny directly to handle waiting on multiple kernel objects.

### Mutex

A mutex is similar to a critical section: only one thread at a time can perform certain operations on certain resources. But a mutex is a kernel-mode thread synchronization mechanism, and it takes almost 100 times longer than a critical section. Its advantages are that it can be used across processes, which critical sections can't, and that it lets you specify a wait timeout, which critical sections don't.

Win32 uses the CreateMutex function to create a mutex:

```cpp
HANDLE CreateMutex(
    PSECURITY_ATTRIBUTES pMutexAttributes,
    BOOL bInitialOwner,
    PCTSTR pName
);
```

Win32 uses the OpenMutex function to get a handle to an existing mutex:

```cpp
HANDLE OpenMutex(
    DWORD dwDesiredAccess,
    BOOL bInheritHandle,
    PCTSTR pName
);
```

Win32 uses the ReleaseMutex function to release a mutex:

```cpp
BOOL ReleaseMutex(
    HANDLE hMutex
);
```

C# wraps this in the Mutex class: you create a mutex by constructing a new Mutex object, get an existing mutex object by calling the static OpenExisting method, and release the mutex by calling the ReleaseMutex method:

```csharp
public sealed class Mutex : WaitHandle
{
    // Internally calls the Win32 CreateMutex function
    public Mutex();
    public Mutex (bool initiallyOwned);
    public Mutex (bool initiallyOwned, string name);
    public Mutex (bool initiallyOwned, string name, out bool createdNew);
    
    // Internally calls the Win32 OpenMutex function
    public static Mutex OpenExisting (string name);
    
    // Internally calls the Win32 ReleaseMutex function
   	public void ReleaseMutex();
}
```

Critical sections and mutexes are used in much the same way:

Initialize critical section <-> Create mutex

Enter critical section     <-> Wait for the mutex kernel object to be signaled (released)

Leave critical section     <-> Release mutex

Destroy critical section     <-> Call CloseHandle

Mutexes have the concept of an owner: once a mutex is owned by a thread, only that thread can release it.

> Note:
>
> If the thread that owns a mutex terminates before releasing it, the mutex is abandoned: the mutex object's thread ID is set to 0 and its recursion count is set to 0. The system then checks whether any threads are waiting on the mutex. If there are, it fairly picks one of the waiting threads, sets the object's internal thread ID to that waiting thread's ID, and sets the recursion count to 1.

### Semaphore

A semaphore is also a kernel-mode thread synchronization mechanism, and it's a great fit for the producer/consumer problem. It can be acquired (locked) n times by different threads and released by any thread. You could loosely think of a mutex as a special semaphore with n equal to 1, but that's not really the case, because semaphores have no concept of an owner while mutexes do. Since a semaphore has no owner, any thread can try to acquire (lock) and release it.

Win32 uses the CreateSemaphore function to create a semaphore:

```cpp
HANDLE CreateSemaphore(
    PSECURITY_ATTRIBUTES pAttributes,
    LONG lInitialCount,
    LONG lMaximumCount,
    PCTSTR pName
);
```

Win32 uses the OpenSemaphore function to get a handle to an existing semaphore:

```cpp
HANDLE OpenSemaphore(
    DWORD dwDesiredAccess,
    BOOL bInheritHandle,
    PCTSTR pName
);
```

Win32 uses the ReleaseSemaphore function to release a semaphore:

```cpp
BOOL ReleaseSemaphore(
    HANDLE hSemaphore,
    LONG lReleaseCount,
    PLONG pPreviousCount
);
```

C# wraps this in the Semaphore class: you initialize and create a semaphore object by constructing a new Semaphore object, release it by calling the Release method, and get an existing semaphore object by calling the static OpenExisting method:

```csharp
public sealed class Semaphore : WaitHandle
{
    // Internally calls the Win32 CreateSemaphore function
    public Semaphore(int initialCount, int maximumCount);
    public Semaphore (int initialCount, int maximumCount, string name);
    public Semaphore (int initialCount, int maximumCount, string name, out bool createdNew);
    
    // Internally calls the Win32 OpenSemaphore function
    public static Semaphore OpenExisting (string name);
    
    // Internally calls the Win32 ReleaseSemaphore function
    public int Release();
    public int Release(int releaseCount);
}
```

### Event

An event is also a kernel-mode thread synchronization mechanism; it's really just a bool variable maintained by the kernel. When the event is false (nonsignaled), threads waiting on it block; when it's true (signaled), they're unblocked. There are two kinds of events: auto-reset events and manual-reset events. When an auto-reset event becomes true, it wakes up only one blocked thread, and then the kernel automatically resets (auto-reset) the event to false, so the other waiting threads stay blocked. When a manual-reset event becomes true, it unblocks all waiting threads, and you have to reset it to false yourself.

Win32 uses the CreateEvent function to create an event object:

```cpp
HANDLE CreateEvent(
    PSECURITY_ATTRIBUTES pEventAttributes,
    BOOL bManualReset,
    BOOL bInitialState,
    PCTSTR pName
);
```

Win32 uses the OpenEvent function to get a handle to an already-created event object:

```cpp
HANDLE OpenEvent(
    DWORD dwDesiredAccess,
    BOOL bInherit,
    PCTSTR pName
);
```

Win32 uses SetEvent to set the event to true, ResetEvent to reset it to false, and PulseEvent to set the event to true and then immediately set it back to false (ResetEvent right after SetEvent):

```cpp
BOOL SetEvent(HANDLE hEvent);

BOOL ResetEvent(HANDLE hEvent);

BOOL PulseEvent(HANDLE hEvent);
```

> You usually don't need to call ResetEvent on an auto-reset event, because once an auto-reset event is Set to true (signaled), the kernel automatically resets it to false (nonsignaled).

C# wraps this in the EventWaitHandle type, from which the AutoResetEvent and ManualResetEvent types are derived:

```csharp
public class EventWaitHandle : WaitHandle
{
    // Internally calls the Win32 CreateEvent function
    public EventWaitHandle (bool initialState, EventResetMode mode);
    public EventWaitHandle (bool initialState, EventResetMode mode, string name);
    public EventWaitHandle (bool initialState, EventResetMode mode, string name, out bool createdNew);
    
    // Internally calls the Win32 SetEvent function to set the event to true; always returns true
    public bool Set();     
    
    // Internally calls the Win32 OpenEvent function to open an existing event
    public static EventWaitHandle OpenExisting (string name);
    
    // Internally calls the Win32 ResetEvent function to set the event to false; always returns false
    public bool Reset();
}

// Simply sets EventResetMode to AutoReset for you
public sealed class AutoResetEvent : EventWaitHandle
{
    public AutoResetEvent(bool initialState): base(initialState,EventResetMode.AutoReset){}
}

// Simply sets EventResetMode to ManualReset for you
public sealed class ManualResetEvent : EventWaitHandle
{
    public ManualResetEvent(bool initialState) : base(initialState,EventResetMode.ManualReset){}
}
```

Since PulseEvent is just equivalent to calling SetEvent followed immediately by ResetEvent and isn't very useful, C#'s EventWaitHandle type doesn't provide a corresponding Pulse method.

> Note:
>
> If you need to get an event object across threads or processes, you need to create an EventWaitHandle object and give it a name in its constructor; otherwise there's no way to get hold of it.

