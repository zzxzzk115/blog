# 线程 Thread

> 进程是资源分配的最小单位，线程是CPU调度的最小单位。
>
> 作为一个Windows概念，线程的职责是对CPU进行虚拟化。			——《CLR via C#》中文第四版 P592
>
> In [computer science](https://en.wikipedia.org/wiki/Computer_science), a **thread** of [execution](https://en.wikipedia.org/wiki/Execution_(computing)) is the smallest sequence of programmed instructions that can be managed independently by a [scheduler](https://en.wikipedia.org/wiki/Scheduling_(computing)), which is typically a part of the [operating system](https://en.wikipedia.org/wiki/Operating_system).						——[维基百科](https://en.wikipedia.org/wiki/Thread_(computing))

![](http://img.zhangkexuan.cn/markdown_20210520112206.png)

上图名为"Concepts-_Program_vs._Process_vs._Thread"，源自维基百科。里面涉及了程序(Program)、进程(Process)、线程(Thread)的概念，也涉及了调度(Scheduling)、抢占(Preemption)、上下文切换(Context Switching)等概念。从图中可以理解一个多线程程序从内存到CPU执行指令的过程。

## 线程的定义

线程(Thread)是允许应用程序并发执行多个任务的一种机制。一个进程可以包含多个线程。同一程序中的所有线程均会独立执行相同程序，且共享同一份全局内存区域，其中包括初始化数据段(initialized data)、未初始化数据段(uninitialized data)以及堆内存段(heap segment)。

!> 传统UNIX进程只是多线程程序的特例，该进程只包含一个线程。

![同时执行4个线程的进程（Linux/x86-32）](http://img.zhangkexuan.cn/markdown_20210520104518.png)

同一进程中的多个线程可以并发执行。在多处理器环境下，多个线程可以同时并行。如果一线程因等待I/O操作而遭阻塞，那么其他线程依然可以继续运行。

## Windows 线程的开销

和一切虚拟化机制一样，线程有空间(内存耗用)和时间(运行时的执行性能)上的开销。

每个线程都有以下要素：

- 线程内核对象(thread kernel object)
- 线程环境块(thread environment block, TEB)
- 用户模式栈(user-mode stack)
- 内核模式栈(kernel-mode stack)
- DLL线程连接(attach)与线程分离(detach)通知

## 上下文切换(Context Switching)

在一个抢占式多任务系统中，操作系统小心地确保每一个线程都有机会执行。它依赖硬件的协助以及许多的簿记工作。当硬件计时器认为某个线程已经执行够久了，就会发出一个中断（interrupt），于是 CPU 取得目前这个线程的当前状态，也就是把所有寄存器内容拷贝到堆栈之中，再把它从堆栈拷贝到一个 CONTEXT 结构（这样便储存了线程的状态）中，以备以后再用。 

要切换不同的线程，操作系统应先切换该线程所属进程的内存，然后恢复该线程放在 CONTEXT 结构中的寄存器值。这整个过程便称为context switching。 

## 线程与进程的区别与联系

对于线程与进程之间的区别与联系，它的书面描述有点抽象，我找到了一个形象易懂的说法。

以下是知乎答主biaodianfu的[回答](https://www.zhihu.com/question/25532384/answer/411179772)：

做个简单的比喻：进程=火车，线程=车厢

- 线程在进程下行进（单纯的车厢无法运行）
- 一个进程可以包含多个线程（一辆火车可以有多个车厢）
- 不同进程间数据很难共享（一辆火车上的乘客很难换到另外一辆火车，比如站点换乘）
- 同一进程下不同线程间数据很易共享（A车厢换到B车厢很容易）
- 进程要比线程消耗更多的计算机资源（采用多列火车相比多个车厢更耗资源）
- 进程间不会相互影响，一个线程挂掉，多数情况将导致整个进程挂掉（一列火车不会影响到另外一列火车，但是如果一列火车上中间的一节车厢着火了，将影响到所有车厢）
- 进程可以拓展到多机，线程最多扩展到多核CPU，而不能扩展到多机（不同火车可以开在多个轨道上，同一火车的车厢不能行进在不同的轨道上）
- 进程使用的内存地址可以上锁，即一个线程使用某些共享内存时，其他线程必须等它结束，才能使用这一块内存。（比如火车上的洗手间）－"互斥锁"
- 进程使用的内存地址可以限定使用量（比如火车上的餐厅，最多只允许多少人进入，如果满了需要在门口等，等有人出来了才能进去）－“信号量”

当然，以上描述是经过改动的。原描述可能存在部分问题。

## Windows 线程深入

请看此篇[深入理解Windows线程](http://blog.zhangkexuan.cn/2021/01/24/windows-thread-internals/)

