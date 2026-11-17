---
title: '对<老熟人?>new 关键字的探究(已更新)'
date: 2020-11-24T20:31:15
categories: [编程语言]
tags: [CSharp, CPP]
toc: true
---

C++ 和 C# 还有 Java 都有 new 关键字，三者之间的区别在哪？

你经常用到 new，可能你觉得它是老熟人。

你真的 **熟** 吗？

<!--more-->

对于 new 关键字，大家一定并不陌生。多数人对 new 的理解应该是：分配内存，创建对象，返回引用或指针。

实际上，各个语言，对于 new 的实现并不相同，单个语言中不同场景 new 的实现也并不完全相同。

# C++ 中的 new

众所周知，C++ 中的 new 是基于 C 的 malloc 实现的，但它做的事情可能不光内存的分配。

要根据 new 的操作对象来区分几种情况，我们通过查看反汇编和查询 C++ 源码的方式来看看 new 在不同情况下到底做了什么。

## 对基本类型使用 new

首先，毋庸置疑，new 会返回一个指针，指针的类型就是 new 后面的操作对象的指针类型。

```cpp
int *i = new int;
```

这样一行代码，背后做了什么事呢？

利用 Visual Studio，查看反汇编(Debug，不是 Release)：

```nasm
0029183E  push        4  						; int占4字节
00291840  call        operator new (02912B7h)  	; 调用void* ::operator new(size_t size)
00291845  add         esp,4  					; 平衡栈
00291848  mov         dword ptr [ebp-0D4h],eax  ; ---------
0029184E  mov         eax,dword ptr [ebp-0D4h]  ; 指针赋值给i
00291854  mov         dword ptr [i],eax			; ---------
```

可以发现，调用了一个叫做 operator new 的函数，它在地址 0x02912B7。

查看地址 0x02912B7 处的汇编代码：

![](/img/markdown_20201124224401.png)

跳转到了 0x0291C50，应该是 operator new 的源码：

![](/img/markdown_20201124224653.png)

果不其然。

去掉汇编代码，整理一下源码：

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

简单看就是，使用 malloc 分配一个内存块 block，返回 block 的地址，当然，也包括异常处理。这实际上就是全局定义的 void* ::operator new (size_t size) 函数。

所以，对于基本类型而言，new 仅仅是分配了一块内存，返回了一个这块内存的起始地址。

## 对自定义类型使用 new

对自定义类型使用 new，也分两种情况。我们知道，类型(class 和 struct) 也可以重载 operator new 函数，这样，在 new 这种类型的对象时，会调用它自身重载的 operator new 函数，而不是全局的 void* ::operator new (size_t size)。类型没有重载 operator new 函数的时候，new 它的对象的时候会调用默认的全局 void* ::operator new (size_t size)。当然，对于类型而言，new 除了调用 operator new 函数，实际上还做了别的事儿，我们后面再谈。

### 没有重载 operator new 的 class 和 struct

假定现在有一个类，一个结构体，均没有重载 operator new 函数。

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

测试代码为：

```cpp
TestClass *tc0 = new TestClass();
```

Debug 模式运行，查看反汇编：

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

new 主要做了两件事：

1. 调用 operator new 函数分配内存
2. 再分配的内存处调用 TestClass 类的构造函数

我们查看 0x01512B7 处:

![](/img/markdown_20201125102455.png)

跳转到了 0x0151C50:

![](/img/markdown_20201125102657.png)

还是一样的，之前的全局 void* ::operator new(size_t size) 函数。

那么构造函数做了什么事呢？

![](/img/markdown_20201125102828.png)

跳转到 0x0151910：

![](/img/markdown_20201125103055.png)

没有调用其他函数，也没有返回任何值，仅仅是在之前分配的内存中生成对象，初始化字段默认值，初始化 this 指针等等。

测试语句更改为：

```cpp
TestStruct *ts0 = new TestStruct();
```

发现结构体类型也是一样。

所以，对没有重载 operator new 的类或结构使用 new：

1. 调用全局的 void* ::operator new(size_t size) 函数，分配内存，返回 void* 指针。
2. 在分配的内存上调用类型的构造函数，生成对象，初始化字段默认值，初始化 this 指针等等。

### 重载了 operator new 的 class 和 struct

现在有一个类，一个结构体，它们都重载了 operator new 函数：

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

测试代码:

```cpp
TestClassWithNew *tcn = new TestClassWithNew();
```

查看反汇编：

![](/img/markdown_20201127232230.png)

可以看出调用了 operator new 函数，也调用了类的构造函数。

调用的 operator new 函数位于 0x011912C1 处：

![](/img/markdown_20201127232333.png)

跳转至 0x01191740 处：

![](/img/markdown_20201127232415.png)

嗯，调用的就是重载后的 operator new 函数了。

struct 也是一样。

所以，对重载了 operator new 的类或结构使用 new：

1. 调用重载后的 void* ::operator new(size_t size) 函数，分配内存，返回 void* 指针。
2. 在分配的内存上调用类型的构造函数，生成对象，初始化字段默认值，初始化 this 指针等等。

## 使用 new[] 申请数组

使用 new[]，和上面的几种情况类似。唯一的不同是，数组调用的不是 operator new 函数，而是 operator new[] 函数。

它也分全局和重载。全局存在一个 void* operator new[]\(size_t size\) 函数，自定义类型可以重载，自己实现逻辑。

以下只测试基本类型的情况。

测试代码（申请一个数组，用于存放 3 个 int 变量，返回数组的首地址）：

```cpp
int *arr0 = new int[3];
```

查看反汇编：

![](/img/markdown_20201127232839.png)

经过两次查询地址后，得到 operator new[] 的源码：

![](/img/markdown_20201127232957.png)

本质上还是调用的 operator new 函数。回过头来分析反汇编的第一句：

```nasm
00E9180E  push        0Ch
```

0x0C 是十进制的 12，也就是 3 * sizeof(int)，3*4。所以，new[]，也就是得到需要分配的总字节数，然后分配这么多字节的一个内存块，返回的是内存块的首地址，也就是数组的首地址。

## 略谈 delete 和 delete[]

对于自定义的类型，delete 和 new 类似不过调用函数的顺序不同：delete 先调用类型的析构函数，再调用 operator delete 函数。

delete[] 先遍历调用析构函数，再调用 operator delete[] 函数。

# C# 中的 new

C# 中的 new 主要区分是对引用类型使用还是对值类型使用。

## 对引用类型使用 new

假定有一个测试用的引用类型：

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

测试代码：

```csharp
TestClass tc0 = new TestClass();
TestClass tc1 = new TestClass(3, false);
```

查看 IL 反汇编：

```cil
IL_0001: newobj       instance void TestCLR.TestClass::.ctor()
IL_0006: stloc.0      // tc0

IL_0007: ldc.i4.3
IL_0008: ldc.i4.0
IL_0009: newobj       instance void TestCLR.TestClass::.ctor(int32, bool)
IL_000e: stloc.1      // tc1
```

可以看到，执行的是 newobj 指令，参数是引用类型的实例构造器在元数据中的表达，调用无参或者有参实例构造器根据你的具体调用是否有参来定。

查询 [官方 OpCodes 的 newobj 指令的说明](https://docs.microsoft.com/en-us/dotnet/api/system.reflection.emit.opcodes.newobj?view=netframework-4.8)：

![](/img/markdown_20201128002256.png)

关键点是：

- newobj 分配内存，创建一个带有实例构造器的新实例，初始化所有实例字段为默认值（0 或者 null），调用实例构造器（默认是无参的，如果有参就把参数传入，调用有参实例构造器），将新创建的实例的引用推到栈上。

可以看到 newobj 主要是调用了引用类型的实例构造器的，那引用类型的实例构造器又做了什么事呢？

![](/img/markdown_20201128003025.png)

可以看到，如果调用的是无参实例构造器，则会仅调用父类的实例构造器；如果调用的是有参实例构造器，会先调用父类的实例构造器，再根据传入的参数列表来对字段进行初始化。

> 注意，图中显示的虽然是调用的 System.Object 的实例构造器，但我用''父类''来形容，是因为如果 TestClass 继承自 TestClassBase，则 TestClass 的实例构造器会调用 TestClassBase 的实例构造器，TestClassBase 的实例构造器会调用它父类的实例构造器，依次类推，直到调用 System.Object 的实例构造器。

关于 Object 的实例构造器，它实际上什么事都没做：

![](/img/markdown_20201128004254.png)

这也在《CLR via C#》的 p162 有相关的说明。Object 的实例构造器直接返回。

所以说，实例构造器做什么其实由你来决定，一般用于实例字段的赋值。对引用类型用 new 的时候，并不是实例构造器完成了字段的初始化，而是 newobj 指令完成的。《CLR via C#》一书的 p161 实际上也说的很明白了：

创建引用类型的实例时，首先为实例的数据字段分配内存，然后初始化对象的附加字段（类型对象指针和同步块索引）， **最后调用类型的实例构造器来设置对象的初始状态** 。

初始状态和初始化还是有区别的。

对比 newobj 指令，我觉得上面那句话的附加字段还是要改成所有实例字段和附加字段。因为官方给出的说明是（虽然我觉得官方也没说得很清楚...）：

![](/img/markdown_20201128010914.png)

《CLR via C#》p82-p83 也专门对 new 进行了描述，我简化并总结了一下：

1. 计算类型及其所有基类型（一直到 Object）中定义的所有实例字段和附加字段需要的字节数（包括类型对象指针和同步块索引需要的字节数）。
2. 托管堆中分配要求的字节数，初始化所有实例字段和附加字段。
3. 调用类型的实例构造器，传递实参，调用基类的实例构造器，直到调用 Object 的实例构造器。
4. 返回新建对象的引用（推到栈上）

由于无法更近一步对 newobj 进行分析，只能结合书籍和 OpCode 文档进行如上的总结了。

## 对值类型使用 new

假定有一个测试用的值类型：

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

测试代码：

```csharp
TestStruct ts0 = new TestStruct();
TestStruct ts1 = new TestStruct(1, 2);
```

查看 IL 反汇编:

```cil
IL_0001: ldloca.s     ts0
IL_0003: initobj      CLR_Test.Program/TestStruct

IL_0001: ldloca.s     ts1
IL_0003: ldc.i4.1
IL_0004: ldc.i4.2
IL_0005: call         instance void CLR_Test.Program/TestStruct::.ctor(int32, int32)
```

如果不向构造器中传入参数，则执行的是 initobj 指令，它用于将值类型的每个字段初始化为 0，而不调用实例构造器。

如果向构造器中传入参数，则直接将参数入栈，并通过 call 指令调用实例构造器。

# Java 中的 new

