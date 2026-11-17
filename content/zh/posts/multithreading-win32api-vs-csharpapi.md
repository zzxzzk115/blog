---
title: 'Win32 多线程 API 和 C# 多线程 API 的对应关系'
date: 2021-06-15T18:47:27
categories: [系统编程]
tags: [Win32, 多线程, CSharp]
toc: true
---

> 本篇文章总结一下多线程中，Win32 API 和 C# API 的对应关系，它们时常是类似的，但也存在一些区别。

# 线程

## 创建线程

创建线程，一般要指定线程要“做什么”，即指定一个函数指针或者委托。

Win32 使用 CreateThread 函数来创建线程：

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

C# 对线程进行了封装，使用以下语句创建线程：

```csharp
Thread t = new Thread(()=>{
    Console.WriteLine("Hello,Thread");
});
```

对于同一件事情，两者的实现会不一样：

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

## 强制结束线程

我们偶尔需要强制结束某线程。

Win32 可以通过在线程中调用 ExitThread 函数来强制结束主调线程：

```cpp
VOID ExitThread(DWORD dwExitCode);
```

Win32 也可以通过传递 HANDLE 参数来强制结束 HANDLE 所指向的线程对象：

```cpp
BOOL TerminateThread(HANDLE hThread, DWORD dwExitCode);
```

C# 也有多种方式结束线程：

- Thread 的 Abort 实例方法。`t.Abort();`、`Thread.CurrentThread.Abort();`
- `Application.ExitThread();`

## 挂起(Suspend) 和恢复(Resume)

Win32 使用 SuspendThread 函数来挂起线程，使用 ResumeThread 函数来恢复线程：

```cpp
DWORD SuspendThread(HANDLE hThread);
DWORD ResumeThread(HANDLE hThread);
```

C# 使用 Thread 的实例方法 Suspend 来挂起线程，使用 Resume 方法来恢复线程：

```csharp
t.Suspend();
t.Resume();
```

> Suspend 和 Resume 已过时。

## 睡眠(Sleep)

Win32 使用 Sleep 函数来睡眠主调线程：

```cpp
VOID Sleep(DWORD dwMilliseconds);

Sleep(100);
```

C# 使用 Thread.Sleep 方法来睡眠主调线程：

```csharp
Thread.Sleep(100);
```

## 优先级(Priority)

Win32 使用 SetThreadPriority 函数来设置线程的优先级：

```cpp
BOOL SetThreadPriority(
    HANDLE hThread,
    int nPriority
);

SetThreadPriority(THREAD_PRIORITY_ABOVE_NORMAL);
```

Win32 使用 GetThreadPriority 函数来获得线程的优先级：

```cpp
int GetThreadPriority(
    HANDLE hThread
);
```

C# 使用 Thread 对象的 Priority 属性来设置和获得线程的优先级：

```csharp
t.Priority = ThreadPriority.AboveNormal;
int priority = t.Priority;
```

# 线程同步机制

线程同步一般分为两种：用户模式下的线程同步和内核模式下的线程同步。

用户模式，特点是快，因为它与操作系统是无关的，所有操作基于硬件来完成。

内核模式基于操作系统，它慢于用户模式很多，但功能更全面，通过各种内核对象，我们能解决一些用户模式不能解决的线程同步问题。

一般而言，解决线程同步的问题时，如果要考虑最佳性能，要先考虑使用用户模式下的线程同步，如果不能满足要求，再考虑使用内核模式下的线程同步。

> C# 提供了混合模式线程同步，它合并使用用户模式和内核模式的线程同步，综合了两者的优点，也解决了一些性能问题。
>
> 使用 C# 时，如果问题比较复杂，又要考虑性能，可以使用混合线程同步。

## 用户模式(User Mode) 下的线程同步

### 原子访问(Atomic Access)

原子访问指的是一个线程在访问某个资源的同时保证没有其它线程会在同一时刻访问同一资源。

Win32 提供了 Interlocked 系列函数来保证对变量进行原子级别的增、减、交换操作：

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

C# 封装了 Volatile 类、Interlocked 类，方法甚多，详情请看文档：

[C# .NET 5 Document: Volatile](https://docs.microsoft.com/zh-cn/dotnet/api/system.threading.volatile?view=net-5.0)

[C# .NET 5 Document: Interlocked](https://docs.microsoft.com/zh-cn/dotnet/api/system.threading.interlocked?view=net-5.0)

Volatile 类基于易变构造，提供了原子级别的读(Read)/写(Write) 操作。

Interlocked 类基于互锁构造，提供了原子级别的加(Add 正数, Increment)/减(Add 负数, Decrement)/交换(Exchange, CompareExchange) 操作，目前版本的.NET 还加入了位运算(Add, Or, Xor) 等操作，更加人性化。

用原子访问的方式去实现自旋锁(Spin Lock)，即可完成线程同步，但是自旋锁是一种忙等(Busy Loop)，最好避免使用这种方式完成线程同步。

Win32 可以这样实现自旋锁：

```cpp
BOOL globalResourceInUse = FALSE;
void Func1() {
    // 等待访问公共资源
    while(InterlockedExchange(&globalResourceInUse, TRUE) == TRUE)
        Sleep(0);
    
    // 获得到了公共资源，开始处理相应逻辑
    // ......
    
    // 逻辑做完了，要归还公共资源
    InterlockedExchange(&globalResourceInUse, FALSE);
}
```

C# 可以这样实现自旋锁：

```csharp
internal struct SimpleSpinLock
{
    // 0代表false，1代表true
    private int m_globalResourceInUse = 0;
    
    public void Enter()
    {
        while(true)
        {
            if(Interlocked.Exchange(ref m_globalResourceInUse, 1) == 0)
                return;
            
            // 额外逻辑，黑科技
        }
    }
    
    public void Leave()
    {
        Volatile.Write(ref m_globalResourceInUse, 0);
        // 也可以使用Interlocked.Exchange(ref m_globalResourceInUse, 0);
    }
}
```

 ### 临界区/关键段(Critical Section)

临界区是用户模式下的一种线程同步机制。相比原子访问，它可以不仅仅是对某一个变量进行值的更改，它可以做一系列更多的逻辑。同一时间只能有一个线程进入某临界区，完成相应逻辑，待该线程退出临界区后，其它线程才能有机会进入该临界区。

Win32 提供了四个函数，分别初始化、销毁、进入、离开临界区：

- 初始化使用 InitializeCriticalSection 函数

  ```cpp
  VOID InitializeCriticalSection(
      PCRITICAL_SECTION pCriticalSection
  );
  ```

- 销毁使用 DeleteCriticalSection 函数：

  ```cpp
  VOID DeleteCriticalSection(
      PCRITICAL_SECTION pCriticalSection
  );
  ```

- 进入使用 EnterCriticalSection 函数：

  ```cpp
  VOID EnterCriticalSection(
      PCRITICAL_SECTION pCriticalSection
  );
  ```

- 离开使用 LeaveCriticalSection 函数：

  ```cpp
  VOID LeaveCriticalSection(
      PCRITICAL_SECTION pCriticalSection
  );
  ```

C# 使用 Monitor.Enter 方法进入临界区：

```csharp
public static class Monitor 
{
    // ..........
    public static extern void Enter(Object obj);
    // ..........
}

// Monitor.Enter用法
int criticalSectionValue;
Monitor.Enter(criticalSectionValue);
```

C# 使用 Monitor.Exit 方法退出临界区：

```csharp
public static class Monitor 
{
    // ..........
    public static extern void Exit(Object obj);
    // ..........
}

// Monitor.Exit用法
int criticalSectionValue;
Monitor.Exit(criticalSectionValue);
```

> Win32 的临界区和 C# Monitor 实现的临界区只是功能类似，但内部实现方式并不相同。
>
> Win32 API 提供的临界区是 Windows 非托管代码实现的，内部使用自旋锁来提升性能。
>
> C# 的 Monitor 提供的临界区是托管的，基于同步块来设计实现的，并且，**Monitor 其实并不属于用户模式下的线程同步，它属于混合模式下的线程同步。**

## 内核模式(Kernel Mode) 下的线程同步

### 等待内核对象激发

常用内核对象包括：

- 进程(Process)
- 线程(Thread)
- 文件(File)
- 事件(Event)
- 信号量(Semaphore)
- 互斥器(Mutex)
- 管道(Pipe)

它们都有两种状态：未激发状态和激发状态。激发意味着它们的内部状态发生了变化，对于线程而言，激发指线程结束。

Win32 使用 WaitForSingleObject 函数来等待单个内核对象被激发：

```cpp
DWORD WaitForSingleObject(
    HANDLE hHandle,
    DWORD dwMilliseconds
);
```

Win32 使用 WaitForMultipleObjects 函数来等待多个内核对象被激发：

```cpp
DWORD WaitForMultipleObjects(
    DWORD dwCount,
    CONST HANDLE *pHandles,
    BOOL bWaitAll,
    DWORD dwMilliseconds
);
```

C# 提供了抽象类 WaitHandle，里面的 WaitOne 方法本质上会调用 Win32 的 WaitForSingleObject 函数，WaitAll 和 WaitAny 方法本质上会调用 Win32 的 WaitForMultipleObjects 函数：

```csharp
public abstract class WaitHandle : MarshalByRefObject, IDisposable{
    // 内部调用Win32 WaitForSingleObject函数
    public virtual bool WaitOne();
    public virtual bool WaitOne(int millisecondsTimeout);
    public virtual bool WaitOne(TimeSpan timeout);
    
    // 内部调用Win32 WaitForMultipleObjects函数
    public static bool WaitAll(WaitHandle[] waitHandles);
    public static bool WaitAll(WaitHandle[] waitHandles, int millisecondsTimeout);
    public static bool WaitAll(WaitHandles[] waitHandles, TimeSpan timeout);
    
    // 内部调用Win32 WaitForMultipleObjects函数
    public static bool WaitAny(WaitHandles[] waitHandles);
    public static bool WaitAny(WaitHandle[] waitHandles, int millisecondsTimeout);
    public static bool WaitAny(WaitHandles[] waitHandles, TimeSpan timeout);
    
    // 超时就从WaitAny返回这个
    public const int WaitTimeout = 258;
    
    // 内部调用Win32 CloseHandle函数
    public void Dispose();
}
```

> 注意：
>
> WaitHandle 是静态抽象类。
>
> FCL 中 WaitHandle 的类层次结构：
>
> - WaitHandle
>   - EventWaitHandle
>     - AutoResetEvent
>     - ManualResetEvent
>   - Semaphore
>   - Mutex
>
> 所以，**AutoResetEvent、ManualResetEvent、Semaphore、Mutex 的实例对象都可以调用 WaitOne 方法来等待内核对象被激发**，也可以直接调用 WaitHandle 的公有静态方法 WaitAll 和 WaitAny 来处理等待多个内核对象的情况。

### 互斥器(Mutex)

互斥器与临界区类似，同一时间，只能有一个线程对某些资源做某些操作。但互斥器是内核模式(kernel-mode) 下的一种线程同步机制，它比临界区要花费几乎 100 倍的时间。优点是它支持跨进程使用，而临界区不支持；它能指定等待时间，而临界区不能。

Win32 使用 CreateMutex 函数来创建互斥器：

```cpp
HANDLE CreateMutex(
    PSECURITY_ATTRIBUTES pMutexAttributes,
    BOOL bInitialOwner,
    PCTSTR pName
);
```

Win32 使用 OpenMutex 函数来得到一个已经存在的互斥器的句柄：

```cpp
HANDLE OpenMutex(
    DWORD dwDesiredAccess,
    BOOL bInheritHandle,
    PCTSTR pName
);
```

Win32 使用 ReleaseMutex 函数来释放一个互斥器：

```cpp
BOOL ReleaseMutex(
    HANDLE hMutex
);
```

C# 封装了 Mutex 类，通过新建 Mutex 对象来创建互斥器；通过调用静态方法 OpenExisting 来获得一个已经存在的互斥器对象；通过调用 ReleaseMutex 方法来释放互斥器：

```csharp
public sealed class Mutex : WaitHandle
{
    // 内部调用Win32 CreateMutex函数
    public Mutex();
    public Mutex (bool initiallyOwned);
    public Mutex (bool initiallyOwned, string name);
    public Mutex (bool initiallyOwned, string name, out bool createdNew);
    
    // 内部调用Win32 OpenMutex函数
    public static Mutex OpenExisting (string name);
    
    // 内部调用Win32 ReleaseMutex函数
   	public void ReleaseMutex();
}
```

临界区与互斥器在使用上是差不多的：

初始化临界区 <-> 创建互斥器

进入临界区     <-> 等待互斥器内核对象被激发(被释放)

离开临界区     <-> 释放互斥器

销毁临界区     <-> 调用 CloseHandle

互斥器是有拥有者(owner) 的概念的，一旦互斥器被某线程拥有，则只有该线程能够释放它。

> 注意：
>
> 如果互斥器的拥有者线程在互斥器释放前终止了，则互斥器被遗弃(abandoned)，将互斥器对象的线程 ID 设为 0，递归计数设为 0。系统接下来判断还有没有等待该互斥量的线程，如果有，会公平地选择正在等待该互斥量的线程，把对象内部的线程 ID 设为等待线程的 ID，并把递归计数设为 1。

### 信号量(Semaphore)

信号量也是内核模式下的一种线程同步机制，它可以很好地解决生产者/消费者问题。它可以被不同线程获得(锁住)n 次，也可以由任意线程释放。互斥器可以草率理解为特殊的信号量：n 为 1 的信号量，但是事实并非如此，因为信号量是不存在拥有者的概念的，而互斥器存在拥有者的概念。因为信号量不存在拥有者，所以任何线程都可以尝试获得(锁住) 和释放信号量。

Win32 使用 CreateSemaphore 函数来创建信号量：

```cpp
HANDLE CreateSemaphore(
    PSECURITY_ATTRIBUTES pAttributes,
    LONG lInitialCount,
    LONG lMaximumCount,
    PCTSTR pName
);
```

Win32 使用 OpenSemaphore 函数来得到一个已经存在的信号量的句柄：

```cpp
HANDLE OpenSemaphore(
    DWORD dwDesiredAccess,
    BOOL bInheritHandle,
    PCTSTR pName
);
```

Win32 使用 ReleaseSemaphore 函数来释放信号量：

```cpp
BOOL ReleaseSemaphore(
    HANDLE hSemaphore,
    LONG lReleaseCount,
    PLONG pPreviousCount
);
```

C# 封装了 Semaphore 类，通过新建 Semaphore 对象来初始化和创建信号量对象；通过调用 Release 方法来释放信号量对象；通过调用静态方法 OpenExisting 来获得一个已经存在的信号量对象：

```csharp
public sealed class Semaphore : WaitHandle
{
    // 内部调用Win32 CreateSemaphore函数
    public Semaphore(int initialCount, int maximumCount);
    public Semaphore (int initialCount, int maximumCount, string name);
    public Semaphore (int initialCount, int maximumCount, string name, out bool createdNew);
    
    // 内部调用Win32 OpenSemaphore函数
    public static Semaphore OpenExisting (string name);
    
    // 内部调用Win32 ReleaseSemaphore函数
    public int Release();
    public int Release(int releaseCount);
}
```

### 事件(Event)

事件也是内核模式下的一种线程同步机制，它实际上是内核维护的一个 bool 变量。事件为 false(未激发)，在事件上等待的线程就阻塞；事件为 true(激发)，就解除阻塞。事件分为两种：自动重置事件和手动重置事件。当一个自动重置事件为 true 时，它只唤醒一个阻塞的线程，然后内核将该事件自动重置(auto-reset) 为 false，其它等待线程继续阻塞。当一个手动重置事件为 true 时，它解除所有等待线程的阻塞，必须由你自己重新设置(reset) 它为 false。

Win32 使用 CreateEvent 函数来创建事件对象：

```cpp
HANDLE CreateEvent(
    PSECURITY_ATTRIBUTES pEventAttributes,
    BOOL bManualReset,
    BOOL bInitialState,
    PCTSTR pName
);
```

Win32 使用 OpenEvent 函数来获得一个已经创建的事件对象的句柄：

```cpp
HANDLE OpenEvent(
    DWORD dwDesiredAccess,
    BOOL bInherit,
    PCTSTR pName
);
```

Win32 使用 SetEvent 来设置事件为 true，使用 ResetEvent 来重新设置事件为 false，使用 PulseEvent 来先设置事件为 true，再立即将事件设置为 false(SetEvent 以后立即 ResetEvent)：

```cpp
BOOL SetEvent(HANDLE hEvent);

BOOL ResetEvent(HANDLE hEvent);

BOOL PulseEvent(HANDLE hEvent);
```

> 自动重置事件通常不需要调用 ResetEvent 函数，因为当自动重置事件被 Set 为 true(激发状态) 以后，内核会自动重设该事件为 false(未激发状态)。

C# 封装了 EventWaitHandle 类型，并派生了 AutoResetEvent 类型和 ManualResetEvent 类型：

```csharp
public class EventWaitHandle : WaitHandle
{
    // 内部调用Win32 CreateEvent函数
    public EventWaitHandle (bool initialState, EventResetMode mode);
    public EventWaitHandle (bool initialState, EventResetMode mode, string name);
    public EventWaitHandle (bool initialState, EventResetMode mode, string name, out bool createdNew);
    
    // 内部调用Win32 SetEvent函数，将事件设置为true，总是返回true
    public bool Set();     
    
    // 内部调用Win32 OpenEvent函数，打开一个已经存在的事件
    public static EventWaitHandle OpenExisting (string name);
    
    // 内部调用Win32 ResetEvent函数，将事件设为false，总是返回false
    public bool Reset();
}

// 单纯只是帮你设置了EventResetMode为AutoReset
public sealed class AutoResetEvent : EventWaitHandle
{
    public AutoResetEvent(bool initialState): base(initialState,EventResetMode.AutoReset){}
}

// 单纯只是帮你设置了EventResetMode为ManualReset
public sealed class ManualResetEvent : EventWaitHandle
{
    public ManualResetEvent(bool initialState) : base(initialState,EventResetMode.ManualReset){}
}
```

由于 PulseEvent 仅仅相当于调用 SetEvent 后立即调用 ResetEvent，用处并不大，所以 C# EventWaitHandle 类型中并没有提供与之对应的 Pulse 方法。

> 注意：
>
> 如果需要跨线程、进程获得事件对象，需要创建 EventWaitHandle 对象，需要在其构造方法中指定名称，否则是无法获得到的。

