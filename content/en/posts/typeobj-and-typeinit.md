---
title: 'How the Loading of Type Objects Relates to the Invocation of Type Initializers'
date: 2021-03-26T10:32:34
tags: [CLR, CSharp]
categories: [Programming Languages]
toc: true
aiTranslated: true
---

When does a type object get loaded onto the Loader heap? And when is the type initializer actually called?

<!--more-->

# Loading type objects and calling type initializers

Type objects are loaded at runtime, during JIT compilation. A type initializer is called if and only if the program accesses something in the type object for the first time.

## What the JIT compiler does before a method is called

Suppose we have a type like this:

```csharp
public class TestClass
{   
    static TestClass()
    {
        Console.WriteLine("Test cctor");
    }
    
    public void TestFunction()
    {
        Console.WriteLine("Test");
    }
}
```

So when does the type object for TestClass get loaded onto the Loader heap?

The answer: at JIT-compile time, before the first method that references the TestClass type is called.

For example, say there's a method like this that a thread is just about to execute:

```csharp
public void M1()
{
    TestClass tc = new TestClass();
}
```

When the JIT compiler converts M1's IL code into native CPU instructions, it notices all the types referenced inside M1 (here, just TestClass). The CLR has to make sure the assemblies defining those types are loaded, and then it uses the assemblies' metadata to extract information about those types and create some data structures (the type objects) to represent the types themselves.

> Note that M1 has not been called yet at this point.

In other words, if M1 is the first to reference the TestClass type, the TestClass type object is loaded onto the Loader heap **before M1 is called**.

Now someone might ask: does TestClass's type initializer get called at this point too?

## When the type initializer is called

Actually, if you think about it a bit, it's clear that TestClass's type initializer should be called when M1 reaches the line `TestClass tc = new TestClass();`. That's because the new operator has to initialize things like the type object pointer and the sync block index of the TestClass instance, and that touches TestClass's type object.
