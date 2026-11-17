---
title: 对于《CLR via C#》中异常部分的整理
date: 2021-01-09T13:12:18
categories: [编程语言]
tags: [CLR, CSharp, Exception]
toc: true
---

> 什么是异常？如何捕获异常？如果定义异常类？如何抛出异常？如何得到异常的属性？这次我来总结一下《CLR via C#》异常机制相关的内容。

<!--more-->

# 对于《CLR via C#》中异常部分的整理

## 异常是什么

我对异常的理解是：一个方法如果不能正常完成它应该完成的任务，则应该抛出一个异常（Exception）。

注意，是不能正常完成任务。意思就是方法要做的事情可能做到一半，由于可能发生的种种错误，导致后面要做的事情无法继续完成了。这个时候，理应提示程序出错，以及出错的位置，然后想办法解决错误，恢复程序。

所以，多数高级语言都提供了异常处理机制，来帮助程序猿们完成对异常的处理，让程序更健壮。

## 怎么处理异常

C# 提供了对异常的处理机制。Microsoft 为 C# 的异常处理机制专门提供了四个关键字：`try`、`catch`、`finally` 和 `throw`。

通常而言，异常处理机制的标准使用如下：

```csharp
private void SomeMethod()
{
    try
    {
        // 需要得体地进行恢复和/或清理的代码放在这里
    }
    catch (InvalidOperationException)
    {
        // 从InvalidOperationExciption恢复的代码放在这里
    }
    catch (IOException)
    {
        // 从IOException恢复的代码放在这里
    }
    catch
    {
        // 从除了上述异常之外的其他所有异常恢复的代码放在这里
        ...
        // 如果什么异常都捕捉，通常要重新抛出异常。
        throw;
    }
    finally
    {
        // 这里的代码对始于try块的任何操作进行清理
        // 这里的代码总是执行，不管是不是抛出了异常
    }
    // 如果try块没有抛出异常，或者某个catch块捕获到异常，
    // 但没有抛出或重新抛出异常，就执行下面的代码
    ...
}
```

### try、catch、finally 的关系

一个 try 块必须匹配关联 catch 块或者 finally 块，单独的 try 块是没有意义的，C# 也不允许这么做。

例如

```csharp
try
{
    //...
}
catch
{
    //...
}
```

和

```csharp
try
{
    //...
}
finally
{
    //...
}
```

都是允许的。

而

```csharp
try
{
    //...
}
```

这样单独的 try 是不允许的。

一个 try 块可以关联 0 到多个 catch 块，如果 try 块代码没有抛出异常，那么 CLR 会跳过它匹配关联的所有 catch 块，此时如果有 finally 块，会直接执行 finally 块，然后执行 finally 块后面的语句。

CLR 会自上而下搜索 try 块匹配的 catch 块，所以我们在写代码的时候，从上往下定义 catch 时，catch 里的异常类型的是从具体到抽象。如果不这样写，C# 编译器会报错，因为如果具体的 catch 块放在底部，则这个 catch 块根本是不可达的。

如果 try 对应匹配的 catch 块都没有捕捉类型与抛出的异常类型相同，则 CLR 将会调用栈更高的一层继续搜索。

> 调用栈：方法调用栈，处理方法之间的调用和返回的顺序。越上层，方法越先被调用，越靠后返回。

如果直到调用栈的顶部，都没找到匹配的 catch 块，则发生了未处理的异常。

如果找到了匹配的 catch 块，待该 catch 块执行结束后，就会执行从抛出异常的 try 块开始到匹配异常的 catch 块之间（之间：不包含匹配异常的 catch 块后面的 finally 块）的所有 finally 块中的代码。

所有内层的 finally 块执行完后，再执行匹配异常的那个 catch 块中的代码，最后执行 catch 块后的 finally 块中的代码。

catch 中有三种常用操作：

- 重抛异常
- 抛新异常
- 退出当前 catch 块，进入 finally 块（如果有的话）

对于上面调用栈的问题，来看个小例子：

```csharp
class Program
{
    static void Method1()
    {
        try
        {
            Console.WriteLine("Method1 Try");
            Method2();
        }
        catch (DivideByZeroException e)
        {
            Console.WriteLine("[Method1 Catch]: " + e.ToString());
        }
        finally
        {
            Console.WriteLine("Method1 Finally");
        }
    }
    
    static void Method2()
    {
        try
        {
            Console.WriteLine("Method2 Try");
            Method3();
        }
        catch (IOException e)
        {
            Console.WriteLine("[Method2 Catch]: " + e.ToString());
        }
        finally
        {
            Console.WriteLine("Method2 Finally");
        }
    }

    static void Method3()
    {
        try
        {
            Console.WriteLine("Method3 Try");
            int a = 1;
            int b = a / 0;
        }
        catch (ArgumentException e)
        {
            Console.WriteLine("[Method3 Catch]: " + e.ToString());
        }
        finally
        {
            Console.WriteLine("Method3 Finally");
        }
    }

    static void Main(string[] args)
    {
        Method1();
        Console.ReadKey();
    }

}
```

结果为：

![](/img/markdown_20210109203152.png)

例子中，Method3 中的 `int b = a / 0;` 这句会导致抛出 System.DivideByZeroException 的异常。但是 Method3 中并没有 catch 到，所以它会去调用它的上层方法 Method2 中寻找有没有匹配 DivideByZeroException 的 catch，发现还是没有，再去调用 Method2 的 Method1 中寻找，好的，最后找到了。然后就是从内而外执行 finally 块中的内容，但是捕获到异常的那一层特殊一点，它会先执行匹配到的 catch 块中的内容（这里是打印了 e.ToString()），再执行该 catch 块后面的 finally 块的内容。

> 如果没有匹配到 catch 块，会发生未处理的异常，线程会被终止。

然后谈谈 finally。一个 finally 肯定是对应一个 try 的，这个毋庸置疑。一个 try 也最多对应一个 finally。那么，finally 里的代码一定会被执行吗？这要分情况讨论。

### finally 是否被执行的问题

先看看 finally 的一些特性。

#### finally 的一些特性

- 使用 lock 语句时，锁在 finally 块中释放。
- 使用 using 语句时，在 finally 块中调用方法的 Dispose 方法。
- 使用 foreach 语句时，在 finally 块中调用 IEnumerator 对象的 Dispose 方法
- 定义终结器方法时，在 finally 块中调用基类的 Finalize 方法

再回到 finally 是否被执行的问题，大致分三种情况：

- 如果是一般情况的线程终止、卸载 AppDomain，则 finally 块中的内容一定被保证执行。

  我们来看看发生未处理的异常的情况（发生未处理的异常会抛出 ThreadAbortException，中断线程）：

  我们把上面例子的代码的 Method1 改为不捕获 DivideByZeroException，然后在每个 finally 块中使用 File.Create 创建文件（之所以不用 Console，是因为线程终止的时候 Console 的 Handle 已经被杀或者依然被占用，无法完成测试比对结果）：

  ```csharp
  class Program
  {
      static void Method1()
      {
          try
          {
              Console.WriteLine("Method1 Try");
              Method2();
          }
          catch (IOException e)
          {
              Console.WriteLine("[Method1 Catch]: " + e.ToString());
          }
          finally
          {
              File.Create("Method1Finally.txt");
              Console.WriteLine("Method1 Finally");
          }
      }
      
      static void Method2()
      {
          try
          {
              Console.WriteLine("Method2 Try");
              Method3();
          }
          catch (IOException e)
          {
              
              Console.WriteLine("[Method2 Catch]: " + e.ToString());
          }
          finally
          {
              File.Create("Method2Finally.txt");
              Console.WriteLine("Method2 Finally");
          }
      }
  
      static void Method3()
      {
          try
          {
              Console.WriteLine("Method3 Try");
              int a = 1;
              int b = a / 0;
          }
          catch (ArgumentException e)
          {
              Console.WriteLine("[Method3 Catch]: " + e.ToString());
          }
          finally
          {
              File.Create("Method3Finally.txt");
              Console.WriteLine("Method3 Finally");
          }
      }
  
      static void Main(string[] args)
      {
          Method1();
          Console.ReadKey();
      }
  
  }
  ```

  切换到 Release，重新生成解决方案，以 Release 方式运行。运行前的文件夹内容：

  ![](/img/markdown_20210109205908.png)

  运行结果及运行后文件夹内容：

  ![](/img/markdown_20210109205949.png)

  ![](/img/markdown_20210109210002.png)

  即使线程终止了，但 finally 块的内容还是被执行了。

- 如果用一些手动强制性终止线程的方法（例如 System.Environment.FailFast 方法）的话，在该强制结束语句后本该执行的 finally 块的内容都不会被执行。

  ```csharp
  class Program
  {
      static void Method1()
      {
          try
          {
              Console.WriteLine("Method1 Try");
              Method2();
          }
          catch (DivideByZeroException e)
          {
              Console.WriteLine("[Method1 Catch]: " + e.ToString());
              System.Environment.FailFast("Method1让后面的finally都无法执行");
          }
          finally
          {
              File.Create("Method1Finally.txt");
              Console.WriteLine("Method1 Finally");
          }
      }
      
      static void Method2()
      {
          try
          {
              Console.WriteLine("Method2 Try");
              Method3();
          }
          catch (IOException e)
          {
              
              Console.WriteLine("[Method2 Catch]: " + e.ToString());
          }
          finally
          {
              File.Create("Method2Finally.txt");
              Console.WriteLine("Method2 Finally");
          }
      }
  
      static void Method3()
      {
          try
          {
              Console.WriteLine("Method3 Try");
              int a = 1;
              int b = a / 0;
          }
          catch (ArgumentException e)
          {
              Console.WriteLine("[Method3 Catch]: " + e.ToString());
          }
          finally
          {
              File.Create("Method3Finally.txt");
              Console.WriteLine("Method3 Finally");
          }
      }
  
      static void Main(string[] args)
      {
          Method1();
          Console.ReadKey();
      }
  
  }
  ```

  上面的代码，在 Method1 的 catch 执行完后，对应的 finally 块本应被执行，但是 catch 中使用了 System.Environment.FailFast 方法，会导致对应的 finally 块不会被执行。但是，Method2 和 Method3 的 finally 块会被执行，因为他们在执行 FailFast 方法前就被执行了。

  结果为：

  ![](/img/markdown_20210109210921.png)

  ![](/img/markdown_20210109210933.png)

  可以看到，并没有 Method1Finally.txt。
  
- 如果 try 和 catch 里有 return，依旧是先执行 finally 的内容，再 return。
## System.Exception 类

System.Exception 是 C# 的大部分异常类的基类（有些特例没有遵守）。继承自 System.Exception 的类都被认为是 CLS 相容的。

它有一些关键属性：

| 属性名称       | 访问  | 类型        | 说明                                                         |
| :------------- | :---- | :---------- | :----------------------------------------------------------- |
| Message        | 只读  | String      | 包含辅助性文字说明，指出抛出异常的原因。如果抛出的异常未处理，该消息通常被写入日志。由于最终用户一般不看这种消息，所以消息应提供尽可能多的技术细节，方便开发人员在生成新版本程序集时，利用消息所提供的信息来修正代码。 |
| Data           | 只读  | IDictionary | 引用一个“键/值对”集合。通常，代码在抛出异常前在该集合中添加记录项；捕捉异常的代码可在异常恢复过程中查询记录项并利用其中的信息 |
| Source         | 读/写 | String      | 包含生成异常的程序集的名称                                   |
| StackTrace     | 只读  | String      | 包含抛出异常之前调用过的所有方法的名称和签名，该属性对调试很有用 |
| TargetSite     | 只读  | MethodBase  | 包含抛出异常的方法                                           |
| HelpLink       | 只读  | String      | 包含帮助用户理解异常的一个文档的 URL。但要注意，键全的编程和安全实践阻止用户查看原始的未处理的异常。因此，除非希望将信息传达给其他程序员，否则不要使用该属性 |
| InnerException | 只读  | Exception   | 如果当前异常是在处理一个异常时抛出的，该属性就指出上一个异常是什么。这个只读属性通常为 null。Exception 类型还提供了公共方法 GetBaseException 来遍历由内层异常构成的链表，并返回最初抛出的异常 |
| HResult        | 读/写 | Int32       | 跨越托管和本机代码边界使用的一个 32 位值。例如，当 COM API 返回代表失败的 HRESULT 值，CLR 抛出一个 Exception 派生对象，并通过该属性来维护 HRESULT 值 |

 我们经常用到 Message 或者 Exception 的 ToString() 实例方法的形式来输出错误信息。

其实 Exception 的 ToString() 内部实现是这样的：

![](/img/markdown_20210109214228.png)

![](/img/markdown_20210109214057.png)

Exception 的 ToString 里面用到了 Message 属性来获取错误信息，用到了 GetStackTrace 方法来获取栈追踪信息。

也就是说，ToString 默认需要 Message 信息，需要栈追踪信息。

而这个 GetStackTrace，正是 StackTrace 属性中使用的方法：

![](/img/markdown_20210109215247.png)

和 StackTrace 相关的有两个私有字段：`_stackTraceString` 和 `_remoteStackTraceString`。

`_stackTraceString` 在 Exception 新建实例的时候被赋值为 null:

![](/img/markdown_20210109222718.png)

`_remoteStackTraceString` 是 Exception 类的实例被反序列化时设置的：

![](/img/markdown_20210109235104.png)

可以看到，它获得序列化信息中存储的 RemoteStackTraceString 信息，然后+=序列化信息中存储的 StackTraceString 信息。这样它不会像 `_stackTraceString` 每次在构造器中被赋值为 null，它会在多次序列化反序列化的操作中保存所有的栈追踪信息。

我们知道，在跨 AppDomain 封送对象的时候，对象会进行序列化和反序列化的操作，所以，跨 AppDomain 抛出/捕获一个异常的时候，上面的 Exception 的特殊的构造器会被调用。

 ## 如何抛出异常

C# 提供了 throw 关键字来抛出异常。

```csharp
throw;

throw e;

throw new IOException();
```

直接 throw 和 throw 一个 Exception 实例的区别是：前者不会被认为是异常的起点，后者会被认为是异常的起点。

至于抛出什么异常，在哪里抛出异常，抛出异常里传递什么字符串参数，就是值得进一步思考的问题了。这里我就不细说，毕竟要视具体情况而论。

## 自定义异常类

以 GameFramework 中的 GameFrameworkException 的实现为例子：

![](/img/markdown_20210110001827.png)

自定义的异常类至少要实现四个构造器，还需要被 Serializable 特性标记。

  当然，Exception 类中的一些虚属性（例如 Message）和虚方法（例如 Equals、ToString 等）都可以按你的想法来重写。

你也可以像《CLR via C#》的例子一样定义一个泛型异常类。参考 P413。

## 一些特殊情况

### 多线程抛出异常的异常处理问题

在线程中抛出的异常，是只能该线程它自己捕获到，还是其他线程也可以捕获到呢？

```csharp
class Program
{
    static void TestThreadMethod()
    {
        try
        {
            Console.WriteLine("Thread Try");
            int a = 1;
            int b = a / 0;
        }
        catch (IOException e)
        {
            Console.WriteLine("[Thread Catch]: " + e.ToString());
        }
        finally
        {
            File.Create("ThreadFinally.txt");
            Console.WriteLine("ThreadFinally Finally");
        }
    }

    static void Main(string[] args)
    {
        try
        {
            Thread t = new Thread(TestThreadMethod);
            t.Start();
        }
        catch (DivideByZeroException e)
        {
            Console.WriteLine(e.ToString());
        }
        Console.ReadKey();
    }

}
```

Main 方法中的 catch 会不会捕获到 t 线程中抛出的异常呢？

结果：

![](/img/markdown_20210110004028.png)

直接抛出未处理的异常。

所以，多线程异常处理时，一个线程里面抛出的异常，一般是该线程自己处理。因为其他线程也不知道该线程抛出异常的具体时机。

