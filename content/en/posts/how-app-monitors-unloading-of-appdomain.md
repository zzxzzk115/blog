---
title: How a Program Can Monitor AppDomain Unloading
date: 2021-01-27T20:09:08
categories: [Programming Languages]
tags: [AppDomain, CLR, CSharp]
toc: true
aiTranslated: true
---

An AppDomain can be unloaded manually, and sometimes we may want our program to be notified when one or more AppDomains get unloaded.

So how can a program monitor the unloading of an AppDomain?

# Exploring All the Event Members of System.AppDomain

The first thing that came to mind was to check whether the AppDomain class exposes any public event members.

To quickly find out which events exist, I created an AppDomain instance with the static method CreateDomain, then used IntelliSense and filtered by the lightning bolt icon (which stands for events) to get the list right away:

![](/img/markdown_20210127201650.png)

![](/img/markdown_20210127201736.png)

As you can see, there are 9 public event members:

- DomainUnload : Occurs when an AppDomain is about to be unloaded
- AssemblyLoad : Occurs when an assembly is loaded
- AssemblyResolve : Occurs when the resolution of an assembly fails
- FirstChanceException : Occurs when an exception is thrown in managed code, before the runtime searches the call stack for an exception handler in the application domain
- ProcessExit : Occurs when the default application domain's parent process exits
- ReflectionOnlyAssemblyResolve : Occurs when the resolution of an assembly fails in the reflection-only context
- ResourceResolve : Occurs when the resolution of a resource fails because the resource is not a valid linked or embedded resource in the assembly
- TypeResolve : Occurs when the resolution of a type fails
- UnhandledException : Occurs when an exception is not caught

The very first one happens to be exactly the event I need: DomainUnload.

It fires when an AppDomain is about to be unloaded.

# Registering the DomainUnload Event

First, let's look at the delegate type of the DomainUnload event:

![](/img/markdown_20210127202702.png)

It's an EventHandler, so our listener method needs to have the signature `void 方法名(object, EventArgs)`.

I defined a static method as the listener (since the test code lives in a static method):

![](/img/markdown_20210127202945.png)

Then the test code is:

![](/img/markdown_20210127203020.png)

# Testing

The Main method:

![](/img/markdown_20210127203101.png)



Result:

![](/img/markdown_20210127203206.png)

# Analysis

The actual type of sender is AppDomain, so we can use the as operator to get the AppDomain instance and then retrieve more detailed information:

![](/img/markdown_20210127203504.png)

Result:

![](/img/markdown_20210127203615.png)



# Summary

System.AppDomain provides the DomainUnload event. By registering for this event, a program can monitor the unloading of an AppDomain.

