---
title: 'CLR: Compute-Bound Asynchronous Operations'
date: 2021-06-17T14:07:57
categories: [Programming Languages]
tags: [CLR, CSharp, Multithreading, Thread Pool]
toc: true
aiTranslated: true
---

# The CLR thread pool

There is one thread pool per CLR, and it's shared by all the AppDomains that CLR controls. If a process loads multiple CLRs, each CLR has its own separate thread pool.

When the CLR initializes, the thread pool has no threads in it. Internally, the thread pool maintains a queue of operation requests. When your application wants to perform an asynchronous operation, you call some method that appends an entry to the thread pool's queue. The thread pool's code extracts entries from this queue and dispatches each entry to a thread pool thread. If there are no threads in the pool, a new one is created. When a thread pool thread finishes its task, it isn't destroyed; instead it returns to the pool, goes idle and waits to be assigned a new task.

The thread pool is heuristic: it automatically adjusts how it works based on the current application load and the hardware's capabilities.

# The ThreadPool class

The ThreadPool class provides the QueueUserWorkItem method for adding an asynchronous compute-bound operation to the thread pool's queue:

```csharp
public static bool  QueueUserWorkItem(WaitCallback callBack);

public static bool QueueUserWorkItem(WaitCallback callBack, Object state);
```

The WaitCallback delegate:

```csharp
delegate void WaitCallback(object state);
```

# Execution contexts and the ExecutionContext class

Every thread has an execution context data structure associated with it. The execution context includes things like security settings, host settings and logical call context data.

By default, the CLR automatically makes the initiating thread's execution context flow to any helper threads. This passes the context information on to the helper threads, but it costs some performance, because an execution context contains a lot of information, and gathering it all up and copying it to the helper thread takes a fair amount of time. If the helper thread in turn uses more helper threads, even more execution context data structures have to be created and initialized.

The ExecutionContext class lets you control how an execution context flows from one thread to another.

```csharp
public sealed class ExecutionContext : IDisposable, ISerializable
{
    [SecurityCritical]
    public static AsyncFlowControl SuppressFlow();
    
    public static void RestoreFlow();
    
    public static bool IsFlowSuppressed();
}
```

Using the ExecutionContext class to stop the execution context from flowing can improve your application's performance. The gain is significant on servers, but not so much on clients. Also, since the SuppressFlow method is marked with the [SecurityCritical] attribute, some clients can't call it at all.

# Cooperative cancellation and timeouts

Compute-bound asynchronous operations should be cancelable.

1. First, create a CancellationTokenSource object. CancellationTokenSource's public bool property IsCancellationRequested indicates whether a cancellation request has been received. Its Token property, of type CancellationToken, can be passed as an argument to the work item. CancellationTokenSource also provides a Cancel method for issuing a cancellation request.
2. Inside the loop of the asynchronous operation, check IsCancellationRequested. If it's true, a cancellation has been requested, and that's usually when you stop the asynchronous operation.

CancellationToken's Register method lets you register a delegate that's called when the token is canceled. You can call Register multiple times to register multiple delegates.

If you want a CancellationTokenSource to cancel itself automatically after a certain amount of time, you can call its CancelAfter method:

```csharp
public void CancelAfter(int millisecondsDelay);

public void CancelAfter(TimeSpan delay);
```

# Tasks and the Task class

The biggest problem with ThreadPool's QueueUserWorkItem method is that there's no built-in way to know when the operation has completed, and no way to get a return value back when it does. Tasks are the concept that came along to solve exactly this problem.

Anything QueueUserWorkItem can do, Task can do too:

```csharp
ThreadPool.QueueUserWorkItem(ComputeBoundOp, 5);
new Task(ComputeBoundOp, 5).Start();
Task.Run(() => ComputeBoundOp(5) );
```

A Task can also be given a CancellationTokenSource object to support cancellation.

## Canceling a task

You can wait for a Task to complete and get its return value. Use Task\<TResult\> or call Task.Run\<TResult\> to handle operations that return a value.

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

// Create the task
Task<int> t = new Task<int>(n = > Sum((int)n), 1000000000);

// Start the task
t.Start();

// Wait for the task to complete
t.Wait();

// Print the task's result
Console.WriteLine(t.Result);
```

Besides the Wait method, Task also provides WaitAny and WaitAll, which wait for any one Task to complete and for all Tasks to complete, respectively.

## Starting a new task when a task completes

Task provides the ContinueWith method for starting a new Task once a given Task completes. ContinueWith returns a reference to the new Task.

## Tasks can start child tasks

A Task can also start child tasks: inside the Task's delegate, create a new Task object with TaskCreationOptions set to AttachedToParent and start it. That way, the parent task isn't considered complete until all of its child tasks have completed.

## Inside a task

