# 进程 Process

>  进程实际是应用程序的实例要使用的资源的集合。 		——《CLR via C#》中文第四版 P592
>
> In [computing](https://en.wikipedia.org/wiki/Computing), a **process** is the [instance](https://en.wikipedia.org/wiki/Instance_(computer_science)) of a [computer program](https://en.wikipedia.org/wiki/Computer_program) that is being executed by one or many [threads](https://en.wikipedia.org/wiki/Thread_(computing)).					—— [维基百科](https://en.wikipedia.org/wiki/Process_(computing)#Representation)

## 进程的定义

进程(Process)是操作系统为正在运行的程序提供的一层抽象。在Windows层面，进程包含了内存和资源。内存不用多说，就目前的硬件水平而言一个进程可拥有的内存已经可达到GB级别。资源包括核心对象(Kernel Object，如文件句柄File Handle和线程Thread)、USER资源(如对话框和字符串)、GDI资源(如设备上下文Device Context和笔刷Brushes)。

每个进程都被赋予了一个虚拟地址空间，这确保了一个进程中的代码和数据无法被另一个进程访问，进而确保了应用程序实例的健壮性。

### Windows 进程的结构

每个Windows进程都是由一个执行体进程(EPROCESS)结构表示的。

执行体进程的结构如下图所示：

![EPROCESS](http://img.zhangkexuan.cn/markdown_20210519180604.png)

EPROCESS结构中除了包含许多与进程有关的属性有关外，还包含和指向了许多其他的相关数据结构。例如，每个进程都有一个或多个线程，这些线程由执行体线程(ETHREAD)结构来表示。

EPROCESS和相关数据结构位于系统空间中，但进程环境块(PEB)是个例外，它位于进程地址空间中，因为它包含一些需要由用户模式代码来修改的信息。





