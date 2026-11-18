---
title: 'Digging into the <Old Friend?> new Keyword (Updated)'
date: 2020-11-24T20:31:15
categories: [Programming Languages]
tags: [CSharp, CPP]
toc: true
aiTranslated: true
---

C++, C# and Java all have a new keyword. What are the differences between the three?

You use new all the time, so you probably think of it as an old friend.

But do you really **know** it?

<!--more-->

Everyone is surely familiar with the new keyword. Most people's understanding of new is probably: allocate memory, create an object, return a reference or pointer.

In reality, each language implements new differently, and even within a single language, new isn't implemented exactly the same way in every scenario.

# new in C++

As we all know, new in C++ is implemented on top of C's malloc, but what it does may go beyond just allocating memory.

We need to distinguish several cases depending on what new is applied to. Let's look at the disassembly and dig into the C++ source to see what new actually does in each case.

## Using new on primitive types

First, beyond any doubt, new returns a pointer, and the pointer's type is a pointer to whatever new is applied to.

```cpp
int *i = new int;
```

What goes on behind this one line of code?

Using Visual Studio, let's look at the disassembly (Debug, not Release):

```nasm
0029183E  push        4  						; an int takes 4 bytes
00291840  call        operator new (02912B7h)  	; call void* ::operator new(size_t size)
00291845  add         esp,4  					; balance the stack
00291848  mov         dword ptr [ebp-0D4h],eax  ; ---------
0029184E  mov         eax,dword ptr [ebp-0D4h]  ; assign the pointer to i
00291854  mov         dword ptr [i],eax			; ---------
```

We can see it calls a function named operator new, located at address 0x02912B7.

Let's look at the assembly at address 0x02912B7:

![](/img/markdown_20201124224401.png)

It jumps to 0x0291C50, which should be the source of operator new:

![](/img/markdown_20201124224653.png)

Sure enough.

Stripping out the assembly and tidying up the source:

```cpp
_CRT_SECURITYCRITICAL_ATTRIBUTE
void* __CRTDECL operator new(size_t const size)
{
    while(true)
    {
        if (void* const block = malloc(size))
        {
            while(true)
            {
                if (void* const block = malloc(size))
                    return block;
                if (_callnewh(size) == 0)
                    if (size == SIZE_MAX)
                        __scrt_throw_std_bad_array_new_length();
                    else
                        __scrt_throw_std_bad_alloc();
            }
        }
    }
}
```

Put simply, it uses malloc to allocate a memory block and returns the block's address, with exception handling included, of course. This is in fact the globally defined void* ::operator new (size_t size) function.

So for primitive types, new merely allocates a chunk of memory and returns the starting address of that memory.

## Using new on user-defined types

Using new on user-defined types also splits into two cases. As we know, types (classes and structs) can overload the operator new function too. In that case, when you new an object of that type, its own overloaded operator new is called instead of the global void* ::operator new (size_t size). When a type doesn't overload operator new, newing one of its objects calls the default global void* ::operator new (size_t size). Of course, for types, new actually does something else besides calling operator new; we'll get to that later.

### Classes and structs that don't overload operator new

Suppose we have a class and a struct, neither of which overloads operator new.

```cpp
class TestClass
{
private:
	int a;

public:
	TestClass():a(0){}
	TestClass(const int a):a(a){}
};

struct TestStruct
{
private:
	int a;
public:
	TestStruct():a(0){}
	TestStruct(const int a):a(a){}
};
```

The test code is:

```cpp
TestClass *tc0 = new TestClass();
```

Run it in Debug mode and look at the disassembly:

```nasm
00151B5D  push        4  
00151B5F  call        operator new (01512B7h)  
00151B64  add         esp,4  
00151B67  mov         dword ptr [ebp-0ECh],eax  
00151B6D  mov         dword ptr [ebp-4],0  
00151B74  cmp         dword ptr [ebp-0ECh],0  
00151B7B  je          main+70h (0151B90h)  
00151B7D  mov         ecx,dword ptr [ebp-0ECh]  
00151B83  call        TestClass::TestClass (015141Ah)  
00151B88  mov         dword ptr [ebp-0F4h],eax  
00151B8E  jmp         main+7Ah (0151B9Ah)  
00151B90  mov         dword ptr [ebp-0F4h],0  
00151B9A  mov         eax,dword ptr [ebp-0F4h]  
00151BA0  mov         dword ptr [ebp-0E0h],eax  
00151BA6  mov         dword ptr [ebp-4],0FFFFFFFFh  
00151BAD  mov         ecx,dword ptr [ebp-0E0h]  
00151BB3  mov         dword ptr [tc0],ecx
```

new does two main things:

1. Calls the operator new function to allocate memory
2. Calls the TestClass constructor on the allocated memory

Let's look at 0x01512B7:

![](/img/markdown_20201125102455.png)

It jumps to 0x0151C50:

![](/img/markdown_20201125102657.png)

Same as before: the global void* ::operator new(size_t size) function.

So what does the constructor do?

![](/img/markdown_20201125102828.png)

It jumps to 0x0151910:

![](/img/markdown_20201125103055.png)

It doesn't call any other functions or return any value; it just builds the object in the previously allocated memory, initializing the fields' default values, the this pointer and so on.

Changing the test statement to:

```cpp
TestStruct *ts0 = new TestStruct();
```

turns out to be the same for the struct type.

So, using new on a class or struct that doesn't overload operator new:

1. Calls the global void* ::operator new(size_t size) function, which allocates memory and returns a void* pointer.
2. Calls the type's constructor on the allocated memory, building the object, initializing the fields' default values, the this pointer and so on.

### Classes and structs that overload operator new

Now we have a class and a struct that both overload operator new:

```cpp
class TestClassWithNew
{
private:
	int a;

public:
	TestClassWithNew():a(0) {}
	TestClassWithNew(const int a) :a(a) {}
	void* operator new(size_t size){
		return malloc(size);
	}
};

struct TestStructWithNew
{
private:
	int a;

public:
	TestStructWithNew():a(0) {}
	TestStructWithNew(const int a) :a(a) {}
	void* operator new(size_t size) {
		return malloc(size);
	}
};
```

Test code:

```cpp
TestClassWithNew *tcn = new TestClassWithNew();
```

Look at the disassembly:

![](/img/markdown_20201127232230.png)

We can see it calls the operator new function and also the class's constructor.

The operator new function being called is at 0x011912C1:

![](/img/markdown_20201127232333.png)

It jumps to 0x01191740:

![](/img/markdown_20201127232415.png)

Yep, this time it's the overloaded operator new function being called.

Same goes for the struct.

So, using new on a class or struct that overloads operator new:

1. Calls the overloaded void* ::operator new(size_t size) function, which allocates memory and returns a void* pointer.
2. Calls the type's constructor on the allocated memory, building the object, initializing the fields' default values, the this pointer and so on.

## Allocating arrays with new[]

Using new[] is similar to the cases above. The only difference is that arrays don't call the operator new function, but the operator new[] function.

It also comes in global and overloaded flavors. There's a global `void* operator new[](size_t size)` function, and user-defined types can overload it with their own logic.

Below I only test the primitive-type case.

Test code (allocate an array to hold 3 int variables and return the array's starting address):

```cpp
int *arr0 = new int[3];
```

Look at the disassembly:

![](/img/markdown_20201127232839.png)

After following the address twice, we get the source of operator new[]:

![](/img/markdown_20201127232957.png)

Under the hood it still calls the operator new function. Going back and analyzing the first line of the disassembly:

```nasm
00E9180E  push        0Ch
```

0x0C is 12 in decimal, i.e. 3 * sizeof(int), 3*4. So new[] works out the total number of bytes it needs to allocate, allocates a memory block of that many bytes, and returns the starting address of the block, which is the starting address of the array.

## A few words on delete and delete[]

For user-defined types, delete is similar to new, but the functions are called in a different order: delete first calls the type's destructor, then calls the operator delete function.

delete[] first iterates over the elements calling the destructor, then calls the operator delete[] function.

# new in C#

For new in C#, the main distinction is whether it's used on a reference type or a value type.

## Using new on reference types

Suppose we have a reference type for testing:

```csharp
class TestClass
{
    public readonly int a;
    public readonly bool b;
    public TestClass(){}
    public TestClass(int a, bool b)
    {
        this.a = a;
        this.b = b;
    }
}
```

Test code:

```csharp
TestClass tc0 = new TestClass();
TestClass tc1 = new TestClass(3, false);
```

Look at the IL disassembly:

```cil
IL_0001: newobj       instance void TestCLR.TestClass::.ctor()
IL_0006: stloc.0      // tc0

IL_0007: ldc.i4.3
IL_0008: ldc.i4.0
IL_0009: newobj       instance void TestCLR.TestClass::.ctor(int32, bool)
IL_000e: stloc.1      // tc1
```

We can see it executes the newobj instruction, whose operand is the metadata representation of the reference type's instance constructor. Whether the parameterless or parameterized instance constructor gets called depends on whether your call passes arguments.

Checking the [official OpCodes documentation for the newobj instruction](https://docs.microsoft.com/en-us/dotnet/api/system.reflection.emit.opcodes.newobj?view=netframework-4.8):

![](/img/markdown_20201128002256.png)

The key points are:

- newobj allocates memory, creates a new instance with an instance constructor, initializes all instance fields to their default values (0 or null), calls the instance constructor (the parameterless one by default; if there are arguments, it passes them in and calls the parameterized instance constructor), and pushes a reference to the newly created instance onto the stack.

We can see newobj mainly calls the reference type's instance constructor. So what does the reference type's instance constructor do?

![](/img/markdown_20201128003025.png)

We can see that if the parameterless instance constructor is called, it only calls the parent class's instance constructor; if the parameterized one is called, it first calls the parent class's instance constructor and then initializes the fields based on the argument list passed in.

> Note: although the figure shows a call to System.Object's instance constructor, I say "parent class" because if TestClass inherited from TestClassBase, TestClass's instance constructor would call TestClassBase's instance constructor, which would call its own parent's instance constructor, and so on, until System.Object's instance constructor is called.

As for Object's instance constructor, it actually does nothing at all:

![](/img/markdown_20201128004254.png)

This is also explained on p162 of *CLR via C#*: Object's instance constructor simply returns.

So what the instance constructor does is really up to you; it's generally used to assign instance fields. When you use new on a reference type, it isn't the instance constructor that initializes the fields; it's the newobj instruction. Page 161 of *CLR via C#* actually spells this out pretty clearly:

When creating an instance of a reference type, memory is first allocated for the instance's data fields, then the object's overhead fields (the type object pointer and the sync block index) are initialized, and **finally the type's instance constructor is called to set the object's initial state**.

Setting the initial state is not the same thing as initialization.

Compared with the newobj instruction, I think "overhead fields" in the sentence above should really be "all instance fields and overhead fields", because the official description says (though I don't think the official docs are all that clear either...):

![](/img/markdown_20201128010914.png)

Pages 82-83 of *CLR via C#* also describe new specifically. I've simplified and summarized it:

1. Calculate the number of bytes required by all instance fields and overhead fields defined in the type and all of its base types (all the way up to Object), including the bytes needed for the type object pointer and the sync block index.
2. Allocate the required number of bytes on the managed heap, and initialize all instance fields and overhead fields.
3. Call the type's instance constructor, passing the arguments, which calls the base class's instance constructor, and so on until Object's instance constructor is called.
4. Return a reference to the new object (pushed onto the stack).

Since there's no way to analyze newobj any further, the best I can do is the summary above, based on the book and the OpCode documentation.

## Using new on value types

Suppose we have a value type for testing:

```csharp
struct TestStruct
{
    private int m_X;
    private int m_Y;
    public TestStruct(int x, int y)
    {
        this.m_X = x;
        this.m_Y = y;
    }
    public override string ToString()
    {
        return "(" + m_X + "," + m_Y + ")";
    }
}
```

Test code:

```csharp
TestStruct ts0 = new TestStruct();
TestStruct ts1 = new TestStruct(1, 2);
```

Look at the IL disassembly:

```cil
IL_0001: ldloca.s     ts0
IL_0003: initobj      CLR_Test.Program/TestStruct

IL_0001: ldloca.s     ts1
IL_0003: ldc.i4.1
IL_0004: ldc.i4.2
IL_0005: call         instance void CLR_Test.Program/TestStruct::.ctor(int32, int32)
```

If no arguments are passed to the constructor, the initobj instruction is executed, which initializes every field of the value type to 0 without calling the instance constructor.

If arguments are passed to the constructor, they're pushed directly onto the stack and the instance constructor is called via the call instruction.

# new in Java

