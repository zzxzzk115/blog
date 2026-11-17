---
title: Identity and Equality of C# Anonymous Types
date: 2021-01-14T16:57:59
categories: [Programming Languages]
tags: [CLR, CSharp, Anonymous Types]
toc: true
aiTranslated: true
---

In C#, how do you tell whether two anonymous types are the same type? And how is equality determined between instances of anonymous types?

<!--more-->

# C# Anonymous Types

Take a look at this code:

```csharp
var o = new { Name = "Jack", Age = 22};
```

What type is o?

o is an **anonymous type**.

When you don't specify a type name after new and instead use the **object initializer** syntax to declare and initialize properties, the C# compiler automatically defines an anonymous type for you.

We can confirm this by compiling and looking at the IL disassembly:

![](/img/markdown_20210114170834.png)

As you can see, this anonymous type has two private fields named `<Age>i__Field` and `<Name>i__Field`, the methods `get_Age` and `getName` generated for the corresponding properties, overridden `Equals`, `GetHashCode` and `ToString`, plus the instance properties `Age` and `Name`.

## Identity

```csharp
var o1 = new { Name = "Jack", Age = 22};
var o2 = new { Name = "Tony", Age = 21};
var o3 = new { Name = "Anonymous", Age = 99, Gender = "Male"};
var o4 = new { Namae = "Mitsuhashi", Sai = 20};
var o5 = new { Age = 30, Name = "?"};
```

Which of these are the same type?

Let's let the IL do the talking:

![](/img/markdown_20210114172906.png)

So the C# compiler generates different anonymous types based on the different structures in the **object initializer**.

If the objects have the same type structure, i.e. the property names, property types and the order in which the properties are specified are all the same, they belong to the same anonymous type.

So in the example above, o1 and o2 are the same type, while o3, o4 and o5 each belong to a different type.

## Equality

```csharp
var o1 = new { Name = "Jack", Age = 22 };
var o2 = new { Name = "Jack", Age = 22 };
Console.WriteLine(o1.Equals(o2));
```

Will the result be True?

Let's look at the result:

![](/img/markdown_20210114173253.png)

It's True. That means the anonymous type must override the Equals method and implement field-by-field comparison.

Let's check the IL to see how Equals is implemented:

![](/img/markdown_20210114173423.png)

The key lies in the call and callvirt instructions inside.

Pulled out, they are:

```cil
IL_000a:  call       class [mscorlib]System.Collections.Generic.EqualityComparer`1<!0> class [mscorlib]System.Collections.Generic.EqualityComparer`1<!'<Name>j__TPar'>::get_Default()

IL_001b:  callvirt   instance bool class [mscorlib]System.Collections.Generic.EqualityComparer`1<!'<Name>j__TPar'>::Equals(!0, !0)

IL_0022:  call       class [mscorlib]System.Collections.Generic.EqualityComparer`1<!0> class [mscorlib]System.Collections.Generic.EqualityComparer`1<!'<Age>j__TPar'>::get_Default()

IL_0033:  callvirt   instance bool class [mscorlib]System.Collections.Generic.EqualityComparer`1<!'<Age>j__TPar'>::Equals(!0, !0)
```

Two methods are called:

- get_Default, the method generated for the `System.Collections.Generic.EqualityComparer<T>.Default` property.
- The `System.Collections.Generic.EqualityComparer<T>.Equals` method

### System.Collections.Generic.EqualityComparer\<T\>.Default

Let's look at the source:

![](/img/markdown_20210114174343.png)

It returns the static readonly field defaultComparer, which is initialized by the CreateComparer method.

Now let's look at the CreateComparer method:

![](/img/markdown_20210114174620.png)

Put simply, it uses RuntimeType to get the actual runtime type of the generic parameter T, and then returns a corresponding concrete XXXEqualityComparer instance. These XXXEqualityComparers are all derived classes, i.e. concrete implementations, of EqualityComparer.

Now let's look at the corresponding API docs:

![](/img/markdown_20210114175119.png)

So what kind of equality comparer do we get?

We get a GenericEqualityComparer, the generic equality comparer, because the generic arguments we pass in are things like `!'<Name>j__TPar'` and `!'<Age>j__TPar'`.

Now let's look at how the generic equality comparer is implemented:

![](/img/markdown_20210114175812.png)

As you can see, it is indeed a derived class of EqualityComparer\<T\>. That makes things easy to understand. When we declare a property and assign it a value in the object initializer, it's equivalent to specifying T in GenericEqualityComparer\<T\> as the type of the assigned value. For example, `Name = "Jack"` specifies T as String, and `Age = 22` specifies T as Int32.

So now it makes sense: taking `Name = "Jack"` as an example, System.Collections.Generic.EqualityComparer\<T\>.Default gives us an instance of GenericEqualityComparer\<String\>, which implements Equals, GetHashCode and so on.

### System.Collections.Generic.EqualityComparer\<T\>.Equals

Let's look at the source:

![](/img/markdown_20210114180836.png)

It's an abstract method, so it's pretty obvious now. Since GenericEqualityComparer\<T\> is a derived class of EqualityComparer\<T\>, when we call EqualityComparer\<T\>'s Equals method via callvirt, the runtime first checks the actual type of the current object, finds that it's the GenericEqualityComparer\<T\> we got earlier, and so the method actually invoked is the Equals implemented by GenericEqualityComparer\<T\>:

![](/img/markdown_20210114181356.png)

### Putting It Together

Remember the IL for Equals from earlier?

![](/img/markdown_20210114173423.png)

Analyzing it again now: it first calls get_Default to get an EqualityComparer (GenericEqualityComparer\<T\>), then pushes the fields of the two anonymous type instances onto the stack, and finally calls the Equals method of the EqualityComparer (GenericEqualityComparer\<T\>), which returns a bool. All the bools are then combined: if every field is equal, the result is true; otherwise it's false.

And that wraps up the analysis.

# Summary

The identity of C# anonymous types is handled by the C# compiler, which generates different anonymous types for different structures; objects with the same structure share the same anonymous type.

The equality of C# anonymous types is handled by the CLR at runtime, implemented using the Equals of GenericEqualityComparer\<T\>.

