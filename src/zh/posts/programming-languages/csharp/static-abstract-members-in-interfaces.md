---
lang: zh-CN
title: 深入探究 C# 11 的静态抽象接口方法
description: 静态抽象接口方法是 C# 11 (对应 .NET 7.0) 引入的新特性。本篇我们来探究一下为什么要有它、它是什么，以及怎么使用它。
author: Lazy_V
date: 2022-11-30
category:
  - 编程语言
tag:
  - 编程语言
  - C#
  - .NET
  - 接口
star: true
---

## 为什么要有静态抽象接口方法

回顾我们曾经的需求：

1. 我们希望在泛型中进行数学运算，但是编译器无法得知 `T` 的运行时类型，从而无法得知 `T` 是否支持诸如加减乘除的数学运算，故无法实现类似下面这样的代码：

   ```csharp
   public T Add<T>(T a, T b)
   {
       return a + b;
   }
   ```

2. 我们希望某些情况下，`T` 作为编译期能够确定的类型，能够调用 `T` 的公有静态方法。然而，接口中无法声明静态接口方法，来允许我们进行 `T.XXX()`; 的操作。要是能够让接口中声明静态接口方法就好了。我们曾经的幻想：

   ```csharp
   public interface ISomeInterface<T> where T : ISomeInterface<T>
   {
       static void SomeStaticMethod();
   }
   
   public void Test<T>() where T : ISomeInterface<T>
   {
       T.SomeStaticMethod();
   }
   ```

为了满足这些需求，微软携手社区开发者们，共同推出了静态抽象接口方法，大家以前的幻想现在已经得以实现。

## 什么是静态抽象接口方法

静态抽象接口方法是 C# 11 (对应 .NET 7.0) 引入的新特性。使用最新的 Visual Studio 2022 版本，安装过 .NET 7.0 运行时，即可尝鲜。

它支持在接口中声明 static abstract 方法 (官方说支持在接口中声明 static virtual 方法，但我开启了 preview 后依旧报错，暂时不知道 static virtual 如何使用)。

## 怎么样使用静态抽象接口方法

举个例子：

我们可以利用上述新特性，定义如下接口：

```csharp
public interface IGetNext<T> where T : IGetNext<T>
{
    static abstract T operator ++(T other);
}
```

>  许多运算符都强制要求其参数必须与类型匹配，或者是按照约束要实现包含类型的类型参数，所以这里，我们约束 `T` 必须实现 `IGetNext<T>`。

然后，定义一个 `RepeatSequence` 结构去实现上面的接口，该结构创建由 `‘A'` 组成的字符串，每个 `++` 操作都使得向字符串中添加一个 `'A'`。

```csharp
public struct RepeatSequence : IGetNext<RepeatSequence>
{
    private const char Ch = 'A';
    public string Text = new string(Ch, 1);

    public RepeatSequence() {}

    public static RepeatSequence operator ++(RepeatSequence other)
        => other with { Text = other.Text + Ch };

    public override string ToString() => Text;
}
```

然后我们可以编写测试代码，打印看看结果：

```csharp
var str = new RepeatSequence();

for (int i = 0; i < 10; i++)
    Console.WriteLine(str++);
```

得到输出：

```
A
AA
AAA
AAAA
AAAAA
AAAAAA
AAAAAAA
AAAAAAAA
AAAAAAAAA
AAAAAAAAAA
```

### Playground

<iframe style="width: 100%; height: 400px;" src="https://sharplab.io/#v2:EYLgtghglgdgNAFxAJwK7wCYgNQB8ACATAIwCwAUBfgMwAEsCApsgGYQDGjtAkgOKMIAcowAeCADwAVAHy0A7gAtmXSbRA9+Q0RJkUA3hVpHa+YgDZaEYAGcEyDglqqA9gAdmEBM+S1s2ABQuCErIAJQA3BQAvhRUdLZo7I4ASozungDKjACOqIwwnGoaAsJi4qnpCFm5+ZzS+obGrshQAG6eXOzOMLa07AoQPgDCCrQAvLQA5ACCk5HkxiZ0pgAMTtrjtDCMcibEK/4jcLTEEY1G50u0FYyZOXkFjP6htHoxlAvGNHsWN3c1j1obg8Xh8fn8fyq91qXGcwWYoUuizGsjhIXkUGCr3WYk2aOYADpJBtsLQRrQovNLt9nK1mC0MFxVk5nBk7LAAObPcayYliebvCgMZgwCAAGxMhD2AHYGp8jKYLPgACy0ACy0Bg/lWAG0ALqWZAc6yI+WvJHGdo+BKbba7SHVB6cZ5Us2LFjeWj+Bj0TYrcK+8Qnf30PymxYRr7EACc/gSYfmi3eUSAA"></iframe>

## 从代码角度分析

### 看看 IL

如下接口：

```csharp
public interface IDeepInSourceCode<T> where T : IDeepInSourceCode<T>
{
    void SomeMethod();
    static abstract void SomeStaticAbstractMethod();
}
```

它的 IL：

```csharp
// Type: StaticAbstractInterfaceMethods.IDeepInSourceCode`1 
// Assembly: StaticAbstractInterfaceMethods, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null
// MVID: 27A20D9E-C658-48F7-8AC2-47D46316D62D
// Location: F:\static_abstract\StaticAbstractInterfaceMethods\bin\Debug\net7.0\StaticAbstractInterfaceMethods.dll
// Sequence point data from f:\static_abstract\staticabstractinterfacemethods\bin\debug\net7.0\staticabstractinterfacemethods.pdb

.class interface public abstract auto ansi
  StaticAbstractInterfaceMethods.IDeepInSourceCode`1<(class StaticAbstractInterfaceMethods.IDeepInSourceCode`1<!0/*T*/>) T>
{
  .param constraint [1] /*T*/, class StaticAbstractInterfaceMethods.IDeepInSourceCode`1<!0/*T*/>
    .custom instance void System.Runtime.CompilerServices.NullableAttribute::.ctor([in] unsigned int8)
      = (01 00 01 00 00 ) // .....
      // unsigned int8(1) // 0x01

  .method public hidebysig virtual newslot abstract instance void
    SomeMethod() cil managed
  {
    // Can't find a body
  } // end of method IDeepInSourceCode`1::SomeMethod

  .method public hidebysig static virtual abstract void
    SomeStaticAbstractMethod() cil managed
  {
    // Can't find a body
  } // end of method IDeepInSourceCode`1::SomeStaticAbstractMethod
} // end of class StaticAbstractInterfaceMethods.IDeepInSourceCode`1
```

对比发现，实际上，static abstract 方法和普通接口方法的区别在于，`newslot` 和 `instance` 关键字变成了 `static`。

这意味着，实现 static abstract 接口方法的具体实现方法，必须是一个以 `public static 开头的方法。

### 试一试继承关系

接着上面的接口，我们定义两个类型：

```csharp
public class DeepInSourceCodeBase : IDeepInSourceCode<DeepInSourceCodeBase>
{
    public virtual void SomeMethod()
    {
        Console.WriteLine("SomeMethodBase is invoked.");
    }

    public static void SomeStaticAbstractMethod()
    {
        Console.WriteLine("SomeStaticAbstractMethodBase is invoked.");
    }
}

public class DeepInSourceCodeDerived : DeepInSourceCodeBase, IDeepInSourceCode<DeepInSourceCodeDerived>
{
    public override void SomeMethod()
    {
        Console.WriteLine("SomeMethodDerived is invoked.");
    }

    public new static void SomeStaticAbstractMethod()
    {
        Console.WriteLine("SomeStaticAbstractMethodDerived is invoked.");
    }
}
```

`DeepInSourceCodeBase` 实现了 `IDeepInSourceCode<DeepInSourceCodeBase>` 接口。

`DeepInSourceCodeDerived` 派生自 `DeepInSourceCodeBase`，重写了 `SomeMethod` 方法，覆盖了 `SomeStaticAbstractMethod` 方法。

写一个测试代码：

```csharp
public class DeepInSourceCodeTester
{
    public static void Test<T1, T2>() 
        where T1 : IDeepInSourceCode<T1>, new()
        where T2 : T1, new()
    {
        T1 t1 = new T1();
        T2 t2 = new T2();
        t1.SomeMethod();
        t2.SomeMethod();
        T1.SomeStaticAbstractMethod();
        T2.SomeStaticAbstractMethod();
    }
}
```

在 `Main` 方法中加入测试代码：

```csharp
internal class Program
{
    static void Main(string[] args)
    {
        DeepInSourceCodeTester.Test<DeepInSourceCodeBase, DeepInSourceCodeDerived>();
    }
}
```

先猜猜结果是什么？

```
SomeMethodBase is invoked.
SomeMethodDerived is invoked.
SomeStaticAbstractMethodBase is invoked.
SomeStaticAbstractMethodDerived is invoked.
```

你会猜测是这样的结果吗？

其实不是。

这里结果是：

```
SomeMethodBase is invoked.
SomeMethodDerived is invoked.
SomeStaticAbstractMethodBase is invoked.
SomeStaticAbstractMethodBase is invoked.
```

官方有专门的说明：https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/interface#static-abstract-and-virtual-members

当我们把 `where T2 : T1, new()` 改为 `where T2 : IDeepInSourceCode<T2>, new()` 结果就是我们猜测的那样了。

### Playground

<iframe style="width: 100%; height: 400px;" src="https://sharplab.io/#v2:EYLgtghglgdgNAFxAJwK7wCYgNQB8ACATAIwCwAUBfgMwAEsCApsgGYQDGjtAkgCKOMADtxgBlAPapknAMLiMjADwAVAHy0A7gAtmXZbRA9+QkRKmz5StRQDeFWg9r4ALLQlhGAWUYIt8gBQAlADc9o74xABstBDAAM4IyBwITq7ujKIIEAhQ7ACC8YnJ3r4BIRQAvhRUdES0xsJiktKMcgoAQhBxXIZ8Ao1mLW1KDabNFh1djKq2YQ40tABuUMgIqBAANqlu4h4lfhhBc7R25I7nTsQAnP4AROn78p3d9HH0MIviANaMGAB0t3KZ0cVUowPmtSi23SmWyuQKCSS7AQj0OgWOpwu4WudxhWRy+UKSJRPgOzy4UDesE+P3+gNC4NooNBNSchHq/TG5laln4yCgi1+Bg5Jia3OG5LgRk5YqGlkUo1lE0YfIFvxm5Ex4To4kFyH5Cmhuy8pLKGOO5wiN3uxtRqsFGFe7xpvwBQPOLMZCxgjA0l2iLh2HlhBIRRWRqKOjK1WKtuONIfhROKpow9qFlOd31d9OOzOq5AWdUVg2VykYCWYsy9kIDrnLCRUxClykIqiCtAtjm0uloymIwr6otLPIUTdUUp9GijWIcPeQenZhn7k99M8cMYu/doCAHAF5aFO+8QggzZ332Qh2Qej63T12HLu/g9U/fGecr8/ba/3bP+1/g3xJNERTUo0TPP9CAAjIgMJECIx/CCHHzMEGGYGBNjZS4AHZq0tKFA08aAYH8CIAAYAG0AF0YmQABzOJ0WjB8RQGcZR0YBsmGQP4uIVGURwlKYpRLdjhnTDB21/ZDKgoIA="></iframe>

## .NET 如何支持[泛型数学](https://learn.microsoft.com/zh-cn/dotnet/standard/generics/math)

为了支持泛型数学，**.NET 7.0 将所有的基元类型进行了重新实现**。

以 `Int32` 为例，它现在要实现更多的接口，这些接口就是为了进行一些泛型数学运算。

```csharp
public readonly struct Int32
        : IComparable,
          IConvertible,
          ISpanFormattable,
          IComparable<int>,
          IEquatable<int>,
          IBinaryInteger<int>,
          IMinMaxValue<int>,
          ISignedNumber<int>
```

`Int32` 除了之前实现的一些接口，目前还实现了以下新的接口：

- IBinaryInterger\<int\>

  ```csharp
  public interface IBinaryInteger<TSelf>
          : IBinaryNumber<TSelf>,
            IShiftOperators<TSelf, int, TSelf>
          where TSelf : IBinaryInteger<TSelf>?
  ```

  - IBinaryNumber\<int\>

    ```csharp
    public interface IBinaryNumber<TSelf>
            : IBitwiseOperators<TSelf, TSelf, TSelf>,
              INumber<TSelf>
            where TSelf : IBinaryNumber<TSelf>?
    ```

    - IBitwiseOperators\<int, int, int\>

      声明了重载 `&`、`|`、`~`、`!`  四个运算符的 static abstract 方法

    - INumber\<int\>

      ```csharp
      public interface INumber<TSelf>
              : IComparable,
                IComparable<TSelf>,
                IComparisonOperators<TSelf, TSelf, bool>,
                IModulusOperators<TSelf, TSelf, TSelf>,
                INumberBase<TSelf>
              where TSelf : INumber<TSelf>?
      ```

      - IComparisonOperators\<int, int, int\>

        声明了重载 `>`、`<`、`>=`、`<=` 四个运算符的 static abstract 方法

      - IModulusOperators\<int, int, int>

        声明了重载 `%` 运算符的  static abstract 方法

      - INumberBase\<int\>

        ```csharp
        public interface INumberBase<TSelf>
                : IAdditionOperators<TSelf, TSelf, TSelf>,
                  IAdditiveIdentity<TSelf, TSelf>,
                  IDecrementOperators<TSelf>,
                  IDivisionOperators<TSelf, TSelf, TSelf>,
                  IEquatable<TSelf>,
                  IEqualityOperators<TSelf, TSelf, bool>,
                  IIncrementOperators<TSelf>,
                  IMultiplicativeIdentity<TSelf, TSelf>,
                  IMultiplyOperators<TSelf, TSelf, TSelf>,
                  ISpanFormattable,
                  ISpanParsable<TSelf>,
                  ISubtractionOperators<TSelf, TSelf, TSelf>,
                  IUnaryPlusOperators<TSelf, TSelf>,
                  IUnaryNegationOperators<TSelf, TSelf>
                where TSelf : INumberBase<TSelf>?
        ```

        简述：主要声明了四则运算相关运算符的重载 static abstract 方法。

  - IShiftOperators\<int, int, int\>

    声明了重载 `<<`、`>>`、`>>>` 三个移位运算符的 static abstract 方法

- IMinMaxValue\<int\>

  声明了 `MinValue`、`MaxValue` 两个 static abstract 属性，表示具有最大最小值属性。

- ISignedNumber\<int\>

  声明了 `NegativeOne` static abstract 属性，表示具有 -1 属性。

如此一来，`Int32` 可以作为泛型数学的泛型参数。

除了 `Int32`，其他诸如 `Single`、`Double`、`Byte` 这些基元类型也都实现了很多这种用于泛型数学运算的接口。

举一个简单的例子：

```csharp
public static void MultiplyAndSub<T>(T t1, T t2, T t3)
    where T : IMultiplyOperators<T, T, T>, ISubtractionOperators<T, T, T>
{
    Console.WriteLine(t1 * t2 - t3);
}
```

上述方法约束 `T` 类型支持乘法和减法运算。

可以这样调用上述方法：

```csharp
MultiplyAndSub(1, 2, 3);
MultiplyAndSub(0.1f, 0.2f, 0.3f);
MultiplyAndSub(0.1d, 0.2d, 0.3d);
```

当然，我们也可以自己定义一个类型，然后实现 乘法、减法 相关的接口：

```csharp
public struct MultiplyAndSubCustomStruct : 
    IMultiplyOperators<MultiplyAndSubCustomStruct, MultiplyAndSubCustomStruct, MultiplyAndSubCustomStruct>,
    ISubtractionOperators<MultiplyAndSubCustomStruct, MultiplyAndSubCustomStruct, MultiplyAndSubCustomStruct>
{
    public MultiplyAndSubCustomStruct(int value)
    {
        Value = value;
    }

    public int Value;

    public static MultiplyAndSubCustomStruct operator *(MultiplyAndSubCustomStruct left, MultiplyAndSubCustomStruct right)
    {
        return new MultiplyAndSubCustomStruct(left.Value * right.Value);
    }

    public static MultiplyAndSubCustomStruct operator -(MultiplyAndSubCustomStruct left, MultiplyAndSubCustomStruct right)
    {
        return new MultiplyAndSubCustomStruct(left.Value - right.Value);
    }

    public string ToString(string? format, IFormatProvider? formatProvider)
    {
        return Value.ToString(format, formatProvider);
    }
}
```

然后也可以调用 `MultiplyAndSub`：

```csharp
MultiplyAndSub(new MultiplyAndSubCustomStruct(1), new MultiplyAndSubCustomStruct(2), new MultiplyAndSubCustomStruct(3));
```

结果是 `-1`，符合预期。