---
title: '《CLR via C#》 Q&A(已更新)'
date: 2020-12-03T11:55:37
categories: [编程语言]
tags: [Q-A, CLR]
toc: true
---

我收集了一下《CLR via C#》 中出现的问题，做成了 Q&A。

<!--more-->

# 第一部分

## 第一章 CLR 的执行模型

### Q. 托管模块有哪些部分？

PE32/PE32+ 头、CLR 头、元数据、IL 代码。

### Q. 程序集和托管模块的关系？CLR 直接管理的是程序集还是托管模块？

如果一个程序集只有一个托管模块并且没有资源文件，那么这个程序集可以说就是托管模块，否则不能说程序集就是托管模块。

CLR 直接管理的是程序集。

### Q. 方法首次调用和第二次调用时，JITCompiler 函数做的事情？

方法首次调用时，JITCompiler 会：

1. 在程序集元数据找到实现类型中被调用的方法
2. 从元数据中获取该方法的 IL
3. 分配内存块
4. 将 IL 编译为 Native Code，存到步骤 3 分配的内存中
5. 在 Type 表中修改与方法对应的条目，使之指向步骤 3 分配的内存块
6. 跳转到内存块中的 Native Code

方法第二次调用时，由于方法已经被验证和编译，会直接跳转到 Native Code 进而执行。JITCompiler 不会做任何事情。

### Q. IL 有哪些特点？优点在哪？

IL 基于栈 : 不提供寄存器操作，容易创建新的语言和编译器。

IL 指令是无类型的 ：操作数不区分 32 位和 64 位，使用方便。

IL 会提供名为“验证”的过程 ：确保代码是安全的，使程序具有健壮性和安全性。

### Q. NGen.exe 的优点和缺点？

优点：

1. 提高应用程序的启动速度（因为 NGen.exe 会一次性编译全部 IL 代码为本机代码，启动的时候不需要 JIT 编译了）
2. 减小应用程序的工作集（生成的代码可以通过内存映射的方式共享，节约了内存）
3. 拥有托管代码的所有好处（垃圾回收、验证、类型、类型安全等）
4. 没有托管代码（JIT 编译）的所有性能问题

缺点：

1. 没有知识产权保护（发布的时候必须同时发布包含 IL 和元数据的程序集）
2. 文件可能失去同步（特征不匹配导致生成的文件根本不能使用）
3. 较差的执行时性能（没有 JIT 的运行时假定，不能生成一些优化的代码、静态字段只能间接访问、会到处插入代码来调用类构造器）

### Q. 通用类型系统 CTS 指定的类型可见性规则是怎样的？

- private 

  成员只能由同一个类(class) 类型中的其他成员访问。

- family

  成员可由派生类型访问，不管那些类型是否在同一个程序集中。C# 用 protected 修饰。

- family and assembly

  成员可由派生类型访问，但这些派生类型必须在同一个程序集中定义。C# 没有提供这种访问控制。

- assembly

  成员可由同一个程序集中的任何代码访问。C# 用 internal 修饰。

- family or assembly

  成员可由任何程序集中的派生类型访问。成员也可由同一个程序集中的任何类型访问。C# 用 protected internal 修饰。

- public

  成员可由任何程序集中的任何代码访问。

## 第二章 生成、打包、部署和管理应用程序及类型

### Q. DLL 和程序集的区别？

程序集可以导出为.DLL 文件或.EXE 文件。程序集导出的.DLL 文件和 Win32 DLL 文件不同，它包含 IL、元数据、资源文件、清单文件等，它还拥有 CLR 头，这些都是 Win32 DLL 没有的。

### Q. 元数据是什么？

元数据(metadata) 简单说是一个数据表(data table) 的集合，是几个表构成的二进制数据块。有三种表：定义表(defination table)、引用表(reference table) 和清单表(manifest table)。

常用的定义表：ModuleDef、TypeDef、MethodDef、FieldDef、ParamDef、PropertyDef、EventDef。

常用的引用表：AssemblyRef、ModuleRef、TypeRef、MemberRef。

常用的清单表：AssemblyDef、FileDef、ManifestResourceDef、ExportedTypesDef。

### Q. 程序集链接器 AL.exe 的作用？

程序集链接器可以生成只含资源的程序集，也就是附属程序集。它还可以生成 EXE 文件和只含清单的 DLL PE 文件。

## 第三章 共享程序集和强命名程序集

### Q. 强命名程序集和弱命名程序集在部署上有何区别？

弱命名程序集只能私有部署，强命名程序集既可以私有部署也可以全局部署。

### Q. 运行时如何解析类型引用？

运行程序，CLR 会加载并初始化自身，读取程序集的 CLR 头，查找标识了应用程序入口方法的 MethodDefToken，检索 MethodDef 元数据表找到方法的 IL 代码在文件中的偏移量，将 IL 代码 JIT 编译成 Native Code，最后执行 Native Code。CLR 会检测所有类型和成员引用，加载它们的定义程序集。解析引用的类型时，CLR 可能在三个地方找到：

1. 相同文件：编译时直接从文件加载，执行继续。
2. 不同文件，相同程序集：运行时确保引用的文件在当前程序集元数据的 FileDef 表中，检查加载程序集清单文件目录，加载被引用的文件，检查哈希值以确保文件完整性。发现类型的成员，执行继续。
3. 不同文件，不同程序集：运行时加载清单文件，如果需要的类型不在该文件中，就继续加载包含了类型的文件。发现类型的成员，执行继续。

解析类型引用如果有错误会抛出异常。

> 图见 P72。

## 第四章 类型基础

### Q. 所有类型都最终从 System.Object 派生吗？

除了接口类型比较特殊，其他类型最终都从 System.Object 派生。

### Q. System.Object 有哪些实例方法？哪些是虚方法？哪些是非虚方法？哪些是受保护的方法？

System.Object 有 Equals、GetHashCode、ToString、GetType、MemberwiseClone、Finalize 这些实例方法。

Equals、GetHashCode、ToString、Finalize 是虚方法。GetType 和 MemberwiseClone 是非虚方法。

MemberwiseClone 和 Finalize 是受保护的方法。

### Q. 创建对象时，new 操作符做了哪些事？

new 做了这些事：

1. 计算类型及其所有基类型（直到 System.Object）中定义的所有实例字段需要的字节数。堆上每个对象都需要一些额外的成员，包括类型对象指针和同步块索引。32 位程序，这两个字段各自需要 32 位，所以每个对象要增加 8 字节。对于 64 位程序，这两个字段各自需要 64 位，所以每个对象要增加 16 字节。
2. CLR 检查区域中是否有分配对象所需的字节数。如果托管堆有足够的可用空间，就在 NextObjPtr 指针指向的地址处放入对象，为对象分配的字节会被清零。接着调用类型的构造器（为 this 参数传递 NextObjPtr），调用基类的构造器直到 System.Object 的构造器（什么也不做，直接返回），new 操作符返回对象引用。返回引用前，NextObjPtr 指针的值会加上对象占用的字节数得到一个新值，即下一个对象放入托管堆时的地址。

> 结合 p82 和 p448

### Q. is 和 as 的功能？它们的区别？

is 判断对象是否兼容于指定类型，如果兼容，返回 true，否则返回 false。当然，如果对象本身为 null，is 直接返回 false。

as 判断对象是否兼容于指定类型，如果兼容，直接返回对同一对象的非 null 引用，否则返回 null。

对于转型而言，as 比 is 效率高，性能更好。as 和 is 都不会抛出异常。

### Q. 命名空间和程序集的关系

同一个命名空间的类型可能在不同程序集完成，例如 System.IO.FileStream 在 MSCorLib.dll 程序集中实现，System.IO.FileStreamWatcher 在 System.dll 程序集中实现。

同一个程序集也可能包含不同命名空间中的类型，例如 System.Int32 和 System.Text.StringBuilder 类型都在 MSCorLib.dll 中实现。

### Q. System.Type 类型对象的类型对象指针指向谁？

指向它自己，因为 System.Type 类型对象本身就是类型对象的一个实例。

## 第五章 基元类型、引用类型和值类型

### Q. 哪些 C# 基元类型不符合 CLS？

sbyte、ushort、uint、ulong。

### Q. checked 等价于在 IL 中的运算做出怎样的改变？

checked 将 IL 中原本应该是普通算术运算的 add、sub、mul、conv 转换为 add.ovf、sub.ovf、mul.ovf、conv.ovf。也就是带有溢出检查的运算指令，一旦检查出溢出，CLR 将会抛出 OverflowException 异常。

### Q. 值类型和引用类型的区别？

值类型一般在栈上分配内存，而引用类型在堆上分配内存。

值类型一般不会被垃圾回收，离开作用域时自动被释放。引用类型会被垃圾回收。

值类型分为未装箱和已装箱，而引用类型都是已装箱的。

值类型的拷贝是深拷贝，引用类型的拷贝是浅拷贝。

值类型没有同步块索引和类型对象指针，不能多线程同步对值类型实例的访问。

> 值类型数组在托管堆上分配内存，数组元素是未装箱的值类型。

### Q. 值类型继承自哪个类型？

结构和枚举都是值类型。

结构(struct) 直接继承自 System.ValueType。System.ValueType 继承自 System.Object。

枚举(enum) 直接继承自 System.Enum，System.Enum 继承自 System.ValueType，但 System.Enum 比较特殊，它是引用类型，而枚举是值类型。

值类型都是隐式密封的。

### Q. 什么是装箱？什么是拆箱？它们的过程？

装箱是指将值类型转换成引用类型：

1. 在托管堆中分配内存，分配的内存量是值类型各字段所需的内存量加上类型对象指针和同步块索引所需的内存量。
2. 值类型的字段复制到新分配的堆内存。
3. 返回对象地址。

拆箱是指获取指向已装箱实例中未装箱部分的指针，这就是拆箱的过程。拆箱往往伴随着字段赋值，但字段赋值不属于拆箱的过程。

### Q. 值类型未实现 Object 的某个虚方法，调用这个虚方法，是否需要装箱？

需要。如果实现了则不需要。因为如果实现（重写）了 Object 的虚方法，则 CLR 以非虚的方式直接调用值类型实现的方法，不用装箱。如果没实现（重写），需要对值类型装箱，传递一个 this 指针，调用 Object 类型的方法。

### Q. Object 的 Equals 方法怎么实现的？它实现的是同一性还是相等性？

这样实现的:

```csharp
public class Object 
{
	public virtual Boolean Equals(Object obj)
    {
        if(this == obj) return true;
        return false;
    }
}
```

它实现的是同一性，因为它只是对引用做了比较。

### Q. ValueType 的 Equals 方法怎么实现的？它实现的是同一性还是相等性？

大致这样实现的：

1. 如果 obj 实参为 null，就返回 false。
2. 如果 this 和 obj 实参引用不同类型的对象，就返回 false。
3. 针对类型定义的每个实例字段，都将 this 对象中的值与 obj 对象中的值进行比较（通过调用字段的 Equals 方法）。任何字段不相等，就返回 false。
4. 返回 true。ValueType 的 Equals 方法不调用 Object 的 Equals 方法。

它实现的是相等性。

### Q. 自己重写的 Equals 要符合相等性的哪 4 个特征？

1. Equals 必须自反：x.Equals(x) 必须返回 true。
2. Equals 必须对称：x.Equals(y) 和 y.Equals(x) 必须返回相同的值。
3. Equals 必须可传递：x.Equals(y) 返回 true，y.Equals(z) 返回 true，则 x.Equals(z) 必须返回 true。
4. Equals 必须一致：比较的两个值不变，Equals 返回值也不能变。

### Q. 自己重写 Equals 除了考虑相等性特征，还需要做哪些事情？

1. 让类型实现 System.IEquatable\<T\>接口的 Equals 方法。
2. 重载==和!=操作符方法。
3. 重写 GetHashCode 方法，保证相等性算法和对象哈希码算法一致。

### Q. dynamic 的原理？

代码使用 dynamic 表达式/变量调用成员时，编译器生成 payload，可在运行时根据 dynamic 表达式/变量引用的对象的实际类型来决定具体执行的操作。

如果字段、方法参数或方法返回值的类型时 dynamic，编译器会将该类型转换为 System.Object，并在元数据中向字段、参数或返回类型应用 System.Runtime.CompilerServices.DynamicAttribute 的实例。

如果局部变量被指定为 dynamic，则变量也会成为 Object，但不会向局部变量应用 DynamicAttribute。

### Q. dynamic 和 var 的区别

dynamic 可以用于局部变量、字段和参数，而 var 只能在方法内部声明局部变量。

dynamic 可以接受表达式，var 不行。

dynamic 声明的变量无需初始化，而 var 必须要显示初始化变量。

## 第六章 类型和成员

### Q. 类型有哪些常见成员？

常量、字段、实例构造器、类型构造器、方法、操作符重载、转换操作符、属性、事件、类型。

### Q. call 和 callvirt 的区别

- call

  该指令可调用静态方法、实例方法和虚方法。用 call 指令调用静态方法，必须指定方法的定义类型。用 call 指令调用实例方法或者虚方法，必须指定引用了对象的变量。call 指令假定该变量不为 null。换言之，变量本身的类型指明了方法的定义类型。如果变量的类型没有定义该方法，就检查基类型来查找匹配方法。call 指令经常用于非虚方式调用虚方法。

- callvirt

  该 IL 指令可调用实例方法和虚方法，不能调用静态方法。用 callvirt 指令调用实例方法或者虚方法，必须指定引用了对象的变量。用 callvirt 指令调用非虚实例方法，变量的类型指明了方法的定义类型。用 callvirt 指令调用虚实例方法，CLR 调查发出调用的对象的实际类型，然后以多态方式调用方法。为了确定类型，发出调用的变量绝不能是 null。换言之，编译这个调用时，JIT 编译器会生成代码来验证变量的值是不是 null，如果是，callvirt 指令造成 CLR 抛出 NullReferenceException 异常。正式由于要进行这种额外的检查，所以 callvirt 指令的执行速度比 call 指令稍慢。注意，即使 callvirt 指令调用的是非虚实例方法，也要执行这种 null 检查。

## 第七章 常量和字段

### Q. 定义常量会分配内存吗？常量和静态字段的区别？

不会，常量会被嵌入到 IL 代码中。

常量的初始化在程序编译时，被嵌入 IL 代码中。静态字段在静态类型构造器中初始化，当类型对象被访问到的时候初始化。

常量的访问只能通过类型的实例对象进行访问，而静态字段可以直接通过类型进行访问。

### Q. 字段被标记 readonly，不可改变的是什么？

是引用，而不是字段引用的对象。

例如：

```csharp
public sealed class AType{
	public static readonly char[] InvalidChars = new char[] {'A', 'B', 'C'};    
}
```

这样是不会报错的：

```csharp
AType.InvalidChars[0] = 'X';
AType.InvalidChars[1] = 'Y';
AType.InvalidChars[2] = 'Z';
```

这样才是会报错的：

```csharp
AType.InvalidChars = new char[]{'X', 'Y', 'Z'};
```

## 第八章 方法

### Q. 值类型的实例构造器如何调用？

如果值类型只有无参实例构造器，则定义值类型的时候会隐式调用默认的无参实例构造器。

如果值类型定义了有参实例构造器，则需要显式调用有参实例构造器。

### Q. 值类型的类型构造器什么时候被调用？

值类型的类型构造器，仅在第一次访问到其类型对象的时候被调用。例如访问静态字段、调用实例方法和静态方法、显式调用有参实例构造器的时候。

> 注意，是第一次，类型构造器第一次调用后，不会再被调用。

### Q. 扩展方法如何定义？

先定义一个静态类，再在该静态类中定义扩展方法。扩展方法都是静态方法。

## 第九章 参数

### Q. ref 和 out 的区别与联系？

相同点：

- ref 和 out 都能返回多个返回值
- 若要使用 ref 和 out 参数，则方法定义和调用方法都必须显式使用 ref 和 out 关键字。在方法中对参数的设置和改变将会直接影响函数调用之处(参数的初始值）。
- 它们生成的 IL 相同。

不同点：

- ref 指定的参数在函数调用时候必须初始化，不能为空的引用。而 out 指定的参数在函数调用时候可以不初始化；
- out 指定的参数在进入函数时会清空自己，必须在函数内部赋初值。而 ref 指定的参数不需要。
- 它们生成的元数据中的记录有一个 bit 不同，该 bit 位用于记录声明方法时指定的是 ref 还是 out。

ref 有进有出，out 只出不进。

### Q. 参数和返回类型的设计规范是什么？

声明方法的参数类型时，尽量指定最弱的类型。声明方法的返回类型时，尽量指定最强的类型。

## 第十章 属性

### Q. 定义属性的本质是什么？

定义非自动实现的属性，本质上编译器会生成 get_XXX 方法和 set_XXX 方法。定义自动实现的属性，本质上编译器会生成 get_XXX 方法和 set_XXX 方法和一个私有字段，get_XXX 和 set_XXX 方法都是编译器自动帮你实现，分别返回私有字段的值和设置私有字段的值。

### Q. 匿名类型如何判断同一性？

如果匿名类型的结构相同（属性名称和类型相同，属性的指定顺序也相同），编译器会视为同一种类型。

### Q. 有参属性如何设置访问器方法名称？

使用 IndexerName 特性来定义。

> 注意，如果要用 IndexerName 特性定义某个访问器方法，那么所有的有参属性都需要用这个特性定义。C# 不支持一个类内定义多个名称不同的访问器方法，但可以定义同名称、不同参数集的访问器方法。

## 第十一章 事件

### Q. 事件和委托的关系？

事件模型以委托为基础。在类内定义事件的时候，编译器会在类内隐式定义一个私有委托字段，一个 add_XXX 方法（用于注册事件），一个 remove_XXX 方法，（用于注销事件）。add_XXX 和 remove_XXX 方法都是基于线程安全的方法，主要利用 Interlocked.CompareExchange\<T\>来完成线程安全。

### Q. 如何以线程安全的方式引发事件？

可以使用 Volatile.Read 方法。

## 第十二章 泛型

### Q. 泛型的优势？

- 源代码保护
- 类型安全
- 代码清晰
- 性能好

### Q. 什么是开放类型？什么是封闭类型？

开放类型：具有泛型参数的类型。

封闭类型：为所有类型参数都传递了实际的数据类型的类型。

### Q. 什么是代码爆炸？CLR 如何解决代码爆炸？

CLR 要为每种不同的方法/类型组合生成本机代码。这称为代码爆炸。

CLR 这样解决代码爆炸：

- 假如为特定的类型实参调用了一个方法，以后再用相同的类型实参调用这个方法，CLR 只会为这个方法/类型组合编译一次代码。举例：一个程序集使用 List\<DateTime\>，一个完全不同的程序集(加载到同一 AppDomain 中) 也使用 List\<DateTime\>，CLR 只为 List\<DateTime\>编译一次方法。
- CLR 认为所有引用类型实参都完全相同，所以代码可以共享（因为引用类型的实参或变量实际只是指向堆上对象的指针，所有指针都以相同方式操纵）。例如为 List\<DateTime\>的方法编译的代码可以直接用于 List\<Stream\>的方法，因为 String 和 Stream 都是引用类型。注意：类型实参是值类型的值类型无法共享代码。

### Q. 逆变量和协变量的关系与区别？

关系：逆变量和协变量都是对于类型转换而言的。

区别：逆变量是指泛型类型参数可以从一个类更改为它的某个派生类，C# 用 in 关键字标记。协变量是指泛型类型参数可以从一个类更改为它的某个基类，C# 用 out 关键字标记。

### Q. 主要约束、次要约束、构造器约束的概念？

主要约束：类型参数指定一个约束类型，指定的类型实参的类型要么是指定的约束类型，要么是指定的约束类型派生的类型。（特殊：class 和 struct）

```csharp
internal sealed class PrimaryConstraintOfStream<T> where T : Stream 
{
	public void M(T stream)
    {
        stream.Close();
    }
}
```

次要约束：接口约束或类型参数约束。接口约束是对接口的类型参数的约束。类型参数约束是指，指定的类型的实参要么就是约束的类型，要么是约束类型的派生类型。

```csharp
//接口约束
private static Int32 M<T>(T t) where T : IComparable, IConvertible
{
    ...
}
//类型参数约束
private static List<TBase> ConvertIList<T, TBase>(IList<T> list) where T : TBase
{
    List<TBase> baseList = new List<TBase>(list.Count);
    for(int i = 0; i < list.Count; i++)
    {
        baseList.Add(list[index]);
    }
    return baseList;
}
```

构造器约束：指定构造器约束，则指定的类型实参是实现了公共无参构造器的非抽象类型。

```csharp
internal sealed class ConstructorConstraint<T> where T : new()
{
    public static T Factory()
    {
        return new T();
    }
}
```



