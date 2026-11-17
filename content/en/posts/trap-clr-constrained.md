---
title: "I Got Careless: Does Calling Equals on a Value Type Box in the CLR?"
date: 2020-11-20T17:32:27
categories: [Programming Languages]
tags: [CLR, CSharp]
toc: true
aiTranslated: true
---

Imagine you've defined your own Point struct:

```csharp
public struct Point
{
    private readonly float m_x;
    private readonly float m_y;
    private readonly float m_z;
    //Equals is not overridden
}
```

How many boxing operations happen in the following code?

```csharp
var p1 = new Point();
var p2 = new Point();
if (p1.Equals(p2))
{
   Console.WriteLine("-------"); 
}
```

Now take a look at the IL:

![il_point](/img/markdown_20201120174752.png)

So how many boxings do you think there are? One? Two? Something else?

<!--more-->

# I Was Too Naive

Naive me naively thought it was one, because I only saw a single box instruction. If you, like me, thought it was one because you only spotted one box instruction, then congratulations: we both fell for it.

Actually, if I hadn't looked at the IL and just reasoned it through the usual way, I would have said two. The custom Point type inherits from System.ValueType, and Equals is a virtual method that System.ValueType overrides from System.Object. If Point doesn't override Equals, then calling the base ValueType's Equals requires boxing, because the runtime needs to know the object's type to locate the type's method table and find that method. So when p1 calls Equals, p1 has to be boxed. And when p2 is passed in as the argument, p2 has to be boxed too (because Equals takes an Object parameter).

But when I looked at the IL and saw only one box instruction, I figured maybe I'd got it wrong and it really was just one...

It's actually still two. That's because the box is followed by a `constrained.` prefix, which I completely ignored... It was only after a classmate posted the definition of `constrained.` that I learned it can also perform boxing.

## The constrained. Instruction

So what does the constrained. instruction do?

[Click here for the documentation](https://docs.microsoft.com/en-us/dotnet/api/system.reflection.emit.opcodes.constrained?view=net-5.0)

According to the definition in the docs:

![constrained.](/img/markdown_20201120180905.png)

The key points are:

- If the type is a reference type, the managed pointer ptr is dereferenced and passed as the this pointer to the callvirt method.
- If the type is a value type and it implements (overrides) the virtual method, ptr is passed unmodified as the this pointer to a call method, directly invoking that type's implementation of the method.
- If the type is a value type but does not implement (override) the virtual method, ptr is dereferenced, boxed, and passed as the this pointer to the callvirt method.

## The Correct Answer to "How Many Boxings When Point Calls Equals"

For our problem, the Point struct doesn't override ValueType's Equals, so when p1 calls Equals we're in the third case. Clearly, the value type gets boxed. Add the boxing of p2 when it's passed into Equals(Object), and that's 2 boxings in total.

## If Point Overrides Equals

If Point overrides Equals, we're in the second case above: when p1 calls Equals, Point's own Equals instance method is called directly. But passing p2 as the argument to Equals(Object) still causes one boxing. In this case there's 1 boxing in total.

# Reflection

I was too naive. I fell into the trap this time because I wasn't careful and didn't think it through. I shouldn't jump to conclusions from surface appearances; I need to reason from the problem itself. Sometimes you really can't just look at the surface, and even when you do look at the surface, you can't settle for half an understanding. `constrained.` is exactly that kind of thing: if you leave it alone, you'll make the same mistake I did; once you understand what it does, the answer becomes obvious.

Falling into traps is fine; not falling into any might actually be the problem. From now on, *I Got Careless* will be a series dedicated to the traps I fall into plus the solutions / correct answers.
