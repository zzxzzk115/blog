---
title: 'CLR：计算限制的异步操作'
date: 2021-06-17T14:07:57
categories: [编程语言]
tags: [CLR, CSharp, 多线程, 线程池]
toc: true
---

# CLR 线程池

每个 CLR 一个线程池，该线程池由 CLR 控制的所有 AppDomain 共享。如果一个进程加载了多个 CLR，则每个 CLR 都有它自己单独的线程池。

CLR 初始化时，线程池内没有线程。线程池内部维护了一个操作请求队列。应用程序执行一个异步操作时，就调用某个方法，将一个记录项(entry) 追加到线程池的操作请求队列中。线程池的代码从这个队列中提取记录项，将这个记录项派发(dispatch) 给一个线程池线程。如果线程池中没有线程，就创建一个新线程。当线程池线程完成任务后，不会被销毁，而是返回线程池，进入空闲状态，等待分配新任务。

线程池是启发式的，能够根据当前应用程序负载和硬件能力来自动调节工作模式。

# ThreadPool 类

ThreadPool 类提供了 QueueUserWorkItem 方法来将一个异步的计算限制操作添加到线程池的队列中：

```csharp
public static bool  QueueUserWorkItem(WaitCallback callBack);

public static bool QueueUserWorkItem(WaitCallback callBack, Object state);
```

WaitCallback 委托：

```csharp
delegate void WaitCallback(object state);
```

# 执行上下文与 ExecutionContext 类

每个线程都关联了一个执行上下文结构。执行上下文包括的东西有安全设置、宿主设置以及逻辑调用上下文数据。

默认情况下，CLR 自动造成初始线程的执行上下文流向任何辅助线程。这造成将上下文信息传给辅助线程，但这会性能造成一定影响，因为执行上下文中包含大量信息，而收集这些信息，再把它们复制到辅助线程，要耗费不少时间。如果辅助线程又采用了更多的辅助线程，还必须创建和初始化更多的执行上下文数据结构。

ExecutionContext 类允许你控制执行上下文如何从一个线程流向另一个。

```csharp
public sealed class ExecutionContext : IDisposable, ISerializable
{
    [SecurityCritical]
    public static AsyncFlowControl SuppressFlow();
    
    public static void RestoreFlow();
    
    public static bool IsFlowSuppressed();
}
```

用 ExecutionContext 类来阻止执行上下文流动可以提升应用程序的性能，服务器性能提升显著，但客户端不能提升多少性能。并且由于 SuppressFlow 方法用 [SecurityCritical] 特性标识，所以某些客户端并不能调用该方法。

# 协作式取消和超时

计算限制的异步操作应该能够取消。

1. 首先创建一个 CancellationTokenSource 对象。CancellationTokenSource 的公有 bool 类型属性 IsCancellationRequested 指出是否收到了取消的请求，CancellationTokenSource 的 CancellationToken 类型 Token 属性可以作为变量传入工作项的参数中，CancellationTokenSource 提供了 Cancel 方法，可以发起取消请求。
2. 在异步操作中的循环中判断 IsCancellationRequested，如果为 true，代表发起了取消的请求，一般在此时停止异步操作。

CancellationToken 的 Register 方法可以注册一个委托，在当前 Token 被取消时被调用。Register 方法可以多次调用，注册多个委托。

要想 CancellationTokenSource 在一段时间内被自动取消，可以调用它的 CancelAfter 方法：

```csharp
public void CancelAfter(int millisecondsDelay);

public void CancelAfter(TimeSpan delay);
```

# 任务与 Task 类

ThreadPool 的 QueueUserWorkItem 方法最大的问题就是没有内建机制让你知道操作在什么时候完成，也没有机制在操作完成时获得返回值。而任务(Task) 就是解决这个问题而出现的概念。

QueueUserWorkItem 做的事情，Task 也能做：

```csharp
ThreadPool.QueueUserWorkItem(ComputeBoundOp, 5);
new Task(ComputeBoundOp, 5).Start();
Task.Run(() => ComputeBoundOp(5) );
```

Task 也能传入一个 CancellationTokenSource 对象来完成取消操作。

## 取消任务

你可以等待 Task 的完成，并获得返回值。使用 Task\<TResult\>或者调用 Task.Run\<TResult\>来处理带有返回值的操作。

```csharp
private static int Sum(int n)
{
    int sum = 0;
    for(; n >0; n--)
    {
        checked{sum += n;}
    }
    return sum;
}

// 创建任务
Task<int> t = new Task<int>(n = > Sum((int)n), 1000000000);

// 开始任务
t.Start();

// 等待任务完成
t.Wait();

// 打印任务结果
Console.WriteLine(t.Result);
```

Task 除了 Wait 方法，也提供了 WaitAny、WaitAll 方法，来分别等待任意 Task 完成、等待所有 Task 完成。

## 任务完成时启动新任务

Task 提供了 ContinueWith 方法来某 Task 完成后启动一个新的 Task。ContinueWith 返回新的 Task 的引用。

## 任务可以启动子任务

Task 还可以启动子任务，即在 Task 的委托中新建 Task 对象将 TaskCreationOptions 设置为 AttachedToParent 并启动。这样，只有所有子任务都完成，父任务才被认为完成。

## 任务内部揭秘





