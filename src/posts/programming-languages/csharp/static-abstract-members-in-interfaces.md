---
lang: en-US
title: Deeply dive into static abstract interface methods in C# 11
description: Static abstract interface method is a new feature in C# 11 (corresponding .NET 7.0). In this article, we are going to deeply dive into it, talk about why we need it, what it is and how to use it.
author: Lazy_V
date: 2022-11-30
category:
  - Programming Languages
tag:
  - Programming Languages
  - C#
  - .NET
  - Interfaces
star: true
---

## Why we need it

Let's recall our previous demands: 

1. We hope to perform mathematical operations in generics, but the compiler can't know the runtime type of `T`, so it can't know whether `T` supports mathematical operations such as addition, subtraction, multiplication and division, so it can't implement code like the following:

   ```csharp
   public T Add<T>(T a, T b)
   {
       return a + b;
   }
   ```

2. We hope that in some cases, `T`, as a type that can be determined at compile time, can call the public static method of `T`. However, the static interface method cannot be declared in the interface to allow us to operate `T.XXX()`; If only the static interface method could be declared in the interface. We used to dream about implementing code like the following：

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

In order to meet these needs, Microsoft and community developers jointly launched the static abstract interface method, and everyone's previous fantasy has now been realized.

## What is it

Static abstract interface method is a new feature in C# 11 (corresponding .NET 7.0). Using the latest version of Visual Studio 2022 and then when NET 7.0 runs, you can taste it fresh.

It supports declaring the static abstract method in the interface (officially, it supports declaring the static virtual method in the interface, but I still report an error after opening the language preview, and I don't know how to use static virtual for the time being).

## How to use it

For an instance, we can use the feature mentioned above to declare the following interface: 

```csharp
public interface IGetNext<T> where T : IGetNext<T>
{
    static abstract T operator ++(T other);
}
```

>  Many operators force their parameters to match the type, or implement the type parameters containing the type according to the constraints. So, in this case we constrain `T` implement `IGetNext<T>`.

Then, define a structure named `RepeatSequence` to implement the above interface, which creates a string composed of `'A'`, and each `++` operation allows an `'A'` to be added to the string.

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

Then we can write some testing codes, let them print to screen and we look at the output.

```csharp
var str = new RepeatSequence();

for (int i = 0; i < 10; i++)
    Console.WriteLine(str++);
```

Output:

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

## Analysing from code aspect

### Let's look at IL codes

Suppose that we have declared the following interface:

```csharp
public interface IDeepInSourceCode<T> where T : IDeepInSourceCode<T>
{
    void SomeMethod();
    static abstract void SomeStaticAbstractMethod();
}
```

The IL codes of it:

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

It is found that in fact, the difference between the static abstract method and the ordinary interface method is that the `newslot` and `instance` keywords become `static`.

It means that the specific implementation method of implementing the static abstract interface method must be a method starting with `public static`.

### Let's try the inheritance relationship

We define two types implementing the interface above:

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

`DeepInSourceCodeBase` implementes `IDeepInSourceCode<DeepInSourceCodeBase>`.

`DeepInSourceCodeDerived` derives from `DeepInSourceCodeBase`, overrides `SomeMethod` method, and covers `SomeStaticAbstractMethod` method.

Let's write some testing code:

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

Add testing codes to `Main`:

```csharp
internal class Program
{
    static void Main(string[] args)
    {
        DeepInSourceCodeTester.Test<DeepInSourceCodeBase, DeepInSourceCodeDerived>();
    }
}
```

Guess what the result is first?

```
SomeMethodBase is invoked.
SomeMethodDerived is invoked.
SomeStaticAbstractMethodBase is invoked.
SomeStaticAbstractMethodDerived is invoked.
```

Would you guess the result like this?

Actually, the result is not like this, it's:

```
SomeMethodBase is invoked.
SomeMethodDerived is invoked.
SomeStaticAbstractMethodBase is invoked.
SomeStaticAbstractMethodBase is invoked.
```

Here is the official explanation: https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/interface#static-abstract-and-virtual-members

When we change `where T2 : T1, new()` to `where T2 : IDeepInSourceCode<T2>, new()`, the result is what we expect.

### Playground

<iframe style="width: 100%; height: 400px;" src="https://sharplab.io/#v2:EYLgtghglgdgNAFxAJwK7wCYgNQB8ACATAIwCwAUBfgMwAEsCApsgGYQDGjtAkgCKOMADtxgBlAPapknAMLiMjADwAVAHy0A7gAtmXZbRA9+QkRKmz5StRQDeFWg9r4ALLQlhGAWUYIt8gBQAlADc9o74xABstBDAAM4IyBwITq7ujKIIEAhQ7ACC8YnJ3r4BIRQAvhRUdES0xsJiktKMcgoAQhBxXIZ8Ao1mLW1KDabNFh1djKq2YQ40tABuUMgIqBAANqlu4h4lfhhBc7R25I7nTsQAnP4AROn78p3d9HH0MIviANaMGAB0t3KZ0cVUowPmtSi23SmWyuQKCSS7AQj0OgWOpwu4WudxhWRy+UKSJRPgOzy4UDesE+P3+gNC4NooNBNSchHq/TG5laln4yCgi1+Bg5Jia3OG5LgRk5YqGlkUo1lE0YfIFvxm5Ex4To4kFyH5Cmhuy8pLKGOO5wiN3uxtRqsFGFe7xpvwBQPOLMZCxgjA0l2iLh2HlhBIRRWRqKOjK1WKtuONIfhROKpow9qFlOd31d9OOzOq5AWdUVg2VykYCWYsy9kIDrnLCRUxClykIqiCtAtjm0uloymIwr6otLPIUTdUUp9GijWIcPeQenZhn7k99M8cMYu/doCAHAF5aFO+8QggzZ332Qh2Qej63T12HLu/g9U/fGecr8/ba/3bP+1/g3xJNERTUo0TPP9CAAjIgMJECIx/CCHHzMEGGYGBNjZS4AHZq0tKFA08aAYH8CIAAYAG0AF0YmQABzOJ0WjB8RQGcZR0YBsmGQP4uIVGURwlKYpRLdjhnTDB21/ZDKgoIA="></iframe>

## How does .NET support [Generic Math](https://learn.microsoft.com/en-us/dotnet/standard/generics/math)? 

In order to support generic math, **. NET 7.0 has reimplemented all the base element types**.

Take `Int32` as an example, it now wants to implement more interfaces to perform some generic mathematical operations:

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

In addition to some previously implemented interfaces, the following new interfaces have been implemented by `Int32`:

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

      Declared the static abstract methods for overloading four operators: `&`, `|`, `~` and `!`.

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

        Declared the static abstract methods for overloading four operators: `>`, `<`, `>=` and `<=`.

      - IModulusOperators\<int, int, int>

        Declared the static abstract method for overloading the operator: `%`.

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

        Mainly declared the static abstract methods for overloading four operators: `+`, `-`, `*`, `/`.

  - IShiftOperators\<int, int, int\>

    Declared the static abstract methods for overloading three operators: `<<`, `>>`, and `>>>`.

- IMinMaxValue\<int\>

  Declared two static abstract properties: `MinValue` and `MaxValue`.

- ISignedNumber\<int\>

  Declared a static abstract property: `NegativeOne`.

In this way, `Int32` can be used as a generic parameter for generic math.

In addition to `Int32`, other element types such as `Single`, `Double` and `Byte` also implement many of these interfaces for generic mathematical operations.

Take a simple example:

```csharp
public static void MultiplyAndSub<T>(T t1, T t2, T t3)
    where T : IMultiplyOperators<T, T, T>, ISubtractionOperators<T, T, T>
{
    Console.WriteLine(t1 * t2 - t3);
}
```

The above method constraints `T` support multiplication and subtraction operations.

The above method can be called like this:

```csharp
MultiplyAndSub(1, 2, 3);
MultiplyAndSub(0.1f, 0.2f, 0.3f);
MultiplyAndSub(0.1d, 0.2d, 0.3d);
```

Of course, we can also define a type by ourselves, and then implement the interface related to multiplication and subtraction:

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

You can then call `MultiplyAndSub`:

```csharp
MultiplyAndSub(new MultiplyAndSubCustomStruct(1), new MultiplyAndSubCustomStruct(2), new MultiplyAndSubCustomStruct(3));
```

The result is `-1`, which meets expectations.