---
title: 'CLR via C# Q&A (Updated)'
date: 2020-12-03T11:55:37
categories: [Programming Languages]
tags: [CLR]
toc: true
aiTranslated: true
---

I collected the questions that come up in *CLR via C#* and turned them into a Q&A.

<!--more-->

# Part 1

## Chapter 1 The CLR's Execution Model

### Q. What are the parts of a managed module?

The PE32/PE32+ header, the CLR header, metadata, and IL code.

### Q. What's the relationship between an assembly and a managed module? Does the CLR directly manage assemblies or managed modules?

If an assembly contains only one managed module and no resource files, you could say the assembly is the managed module; otherwise, you can't say the assembly is the managed module.

The CLR directly manages assemblies.

### Q. What does the JITCompiler function do when a method is called for the first time and the second time?

When a method is called for the first time, JITCompiler:

1. Finds, in the assembly's metadata, the called method within the implementing type
2. Gets the method's IL from the metadata
3. Allocates a block of memory
4. Compiles the IL into native code and stores it in the memory allocated in step 3
5. Modifies the method's entry in the type's table so that it points to the memory block allocated in step 3
6. Jumps to the native code in the memory block

When the method is called the second time, since it has already been verified and compiled, execution jumps straight to the native code. JITCompiler doesn't do anything at all.

### Q. What are the characteristics of IL? What are its advantages?

IL is stack-based: it doesn't provide register operations, which makes it easy to create new languages and compilers.

IL instructions are typeless: operands don't distinguish between 32-bit and 64-bit, which makes them convenient to use.

IL goes through a process called "verification": this ensures the code is safe, making programs robust and secure.

### Q. What are the pros and cons of NGen.exe?

Pros:

1. Improves an application's startup time (because NGen.exe compiles all the IL into native code in one go, no JIT compilation is needed at startup)
2. Reduces an application's working set (the generated code can be shared via memory mapping, saving memory)
3. Keeps all the benefits of managed code (garbage collection, verification, types, type safety, etc.)
4. Avoids all the performance issues of managed code (JIT compilation)

Cons:

1. No intellectual property protection (you must still ship the assemblies containing the IL and metadata)
2. Files can fall out of sync (mismatched characteristics can make the generated files completely unusable)
3. Inferior execution-time performance (without the JIT's runtime assumptions, some optimized code can't be generated, static fields can only be accessed indirectly, and code gets inserted all over the place to call class constructors)

### Q. What are the visibility rules for types specified by the Common Type System (CTS)?

- private

  The member is accessible only by other members in the same class type.

- family

  The member is accessible by derived types, regardless of whether they're in the same assembly. C# uses protected for this.

- family and assembly

  The member is accessible by derived types, but only if those derived types are defined in the same assembly. C# doesn't provide this access control.

- assembly

  The member is accessible by any code in the same assembly. C# uses internal for this.

- family or assembly

  The member is accessible by derived types in any assembly. The member is also accessible by any types in the same assembly. C# uses protected internal for this.

- public

  The member is accessible by any code in any assembly.

## Chapter 2 Building, Packaging, Deploying, and Administering Applications and Types

### Q. What's the difference between a DLL and an assembly?

An assembly can be emitted as a .DLL or .EXE file. The .DLL file an assembly produces is different from a Win32 DLL: it contains IL, metadata, resource files, a manifest and so on, and it also has a CLR header, none of which a Win32 DLL has.

### Q. What is metadata?

Simply put, metadata is a collection of data tables: a binary block of data made up of several tables. There are three kinds of tables: definition tables, reference tables, and manifest tables.

Common definition tables: ModuleDef, TypeDef, MethodDef, FieldDef, ParamDef, PropertyDef, EventDef.

Common reference tables: AssemblyRef, ModuleRef, TypeRef, MemberRef.

Common manifest tables: AssemblyDef, FileDef, ManifestResourceDef, ExportedTypesDef.

### Q. What does the Assembly Linker, AL.exe, do?

The Assembly Linker can produce assemblies that contain only resources, i.e. satellite assemblies. It can also produce EXE files and DLL PE files that contain only a manifest.

## Chapter 3 Shared Assemblies and Strongly Named Assemblies

### Q. How do strongly named and weakly named assemblies differ in deployment?

Weakly named assemblies can only be deployed privately, while strongly named assemblies can be deployed either privately or globally.

### Q. How does the runtime resolve type references?

When the program runs, the CLR loads and initializes itself, reads the assembly's CLR header, looks for the MethodDefToken identifying the application's entry point method, searches the MethodDef metadata table to find the offset of the method's IL code within the file, JIT-compiles the IL into native code, and finally executes the native code. The CLR detects all type and member references and loads their defining assemblies. When resolving a referenced type, the CLR may find it in one of three places:

1. Same file: loaded directly from the file at compile time, and execution continues.
2. Different file, same assembly: the runtime ensures the referenced file is in the FileDef table of the current assembly's metadata, checks the directory the assembly's manifest file was loaded from, loads the referenced file, and checks the hash value to ensure file integrity. The type's member is found and execution continues.
3. Different file, different assembly: the runtime loads the manifest file; if the needed type isn't in that file, it goes on to load the file containing the type. The type's member is found and execution continues.

If an error occurs while resolving a type reference, an exception is thrown.

> See the diagram on p72.

## Chapter 4 Type Fundamentals

### Q. Are all types ultimately derived from System.Object?

Apart from interface types, which are a special case, all types ultimately derive from System.Object.

### Q. What instance methods does System.Object have? Which are virtual? Which are non-virtual? Which are protected?

System.Object has the instance methods Equals, GetHashCode, ToString, GetType, MemberwiseClone and Finalize.

Equals, GetHashCode, ToString and Finalize are virtual. GetType and MemberwiseClone are non-virtual.

MemberwiseClone and Finalize are protected.

### Q. What does the new operator do when creating an object?

new does the following:

1. It calculates the number of bytes required by all instance fields defined in the type and all of its base types (up to System.Object). Every object on the heap also needs some additional members: the type object pointer and the sync block index. In a 32-bit program, these two fields need 32 bits each, so each object gets an extra 8 bytes. In a 64-bit program, they need 64 bits each, so each object gets an extra 16 bytes.
2. The CLR checks whether the region has the number of bytes needed to allocate the object. If the managed heap has enough free space, the object is placed at the address pointed to by the NextObjPtr pointer, and the bytes allocated for the object are zeroed. Then the type's constructor is called (passing NextObjPtr for the this parameter), which calls the base class constructors up to System.Object's constructor (which does nothing and simply returns), and the new operator returns a reference to the object. Before the reference is returned, the size of the object in bytes is added to NextObjPtr to get a new value, i.e. the address where the next object will be placed on the managed heap.

> Read p82 together with p448

### Q. What do is and as do? How do they differ?

is checks whether an object is compatible with a given type; if so it returns true, otherwise false. Of course, if the object itself is null, is just returns false.

as checks whether an object is compatible with a given type; if so it directly returns a non-null reference to the same object, otherwise it returns null.

For casting, as is more efficient and performs better than is. Neither as nor is ever throws an exception.

### Q. The relationship between namespaces and assemblies

Types in the same namespace may be implemented in different assemblies. For example, System.IO.FileStream is implemented in the MSCorLib.dll assembly, while System.IO.FileStreamWatcher is implemented in the System.dll assembly.

The same assembly may also contain types in different namespaces. For example, the System.Int32 and System.Text.StringBuilder types are both implemented in MSCorLib.dll.

### Q. What does the type object pointer of the System.Type type object point to?

It points to itself, because the System.Type type object is itself an instance of a type object.

## Chapter 5 Primitive, Reference, and Value Types

### Q. Which C# primitive types are not CLS-compliant?

sbyte, ushort, uint, ulong.

### Q. What change does checked make to arithmetic operations in the IL?

checked converts the IL instructions add, sub, mul and conv, which would otherwise be ordinary arithmetic operations, into add.ovf, sub.ovf, mul.ovf and conv.ovf. In other words, arithmetic instructions with overflow checking; as soon as an overflow is detected, the CLR throws an OverflowException.

### Q. What's the difference between value types and reference types?

Value types are generally allocated on the stack, while reference types are allocated on the heap.

Value types generally aren't garbage collected; they're freed automatically when they go out of scope. Reference types are garbage collected.

Value types come in unboxed and boxed forms, while reference types are always in boxed form.

Copying a value type is a deep copy; copying a reference type is a shallow copy.

Value types have no sync block index or type object pointer, so access to a value type instance can't be synchronized across threads.

> Arrays of value types are allocated on the managed heap, and the array elements are unboxed value types.

### Q. What type do value types inherit from?

Structs and enums are both value types.

A struct inherits directly from System.ValueType. System.ValueType inherits from System.Object.

An enum inherits directly from System.Enum, and System.Enum inherits from System.ValueType. But System.Enum is a special case: it's a reference type, while enums are value types.

All value types are implicitly sealed.

### Q. What are boxing and unboxing? What do the processes look like?

Boxing means converting a value type into a reference type:

1. Memory is allocated on the managed heap. The amount allocated is the memory required by the value type's fields plus the memory required for the type object pointer and the sync block index.
2. The value type's fields are copied to the newly allocated heap memory.
3. The address of the object is returned.

Unboxing means getting a pointer to the unboxed part of a boxed instance; that's all the unboxing process is. Unboxing is usually followed by copying the fields, but copying the fields isn't part of the unboxing process.

### Q. If a value type doesn't implement one of Object's virtual methods, does calling that virtual method require boxing?

Yes. If it does implement it, no boxing is needed. That's because if the value type implements (overrides) Object's virtual method, the CLR calls the value type's implementation directly in a non-virtual way, with no boxing. If it doesn't implement (override) it, the value type has to be boxed so a this pointer can be passed to call the Object type's method.

### Q. How is Object's Equals method implemented? Does it implement identity or equality?

It's implemented like this:

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

It implements identity, because it only compares references.

### Q. How is ValueType's Equals method implemented? Does it implement identity or equality?

It's implemented roughly like this:

1. If the obj argument is null, return false.
2. If this and the obj argument refer to objects of different types, return false.
3. For each instance field defined by the type, compare the value in the this object with the value in the obj object (by calling the field's Equals method). If any field isn't equal, return false.
4. Return true. ValueType's Equals method doesn't call Object's Equals method.

It implements equality.

### Q. What 4 properties of equality must your own Equals override satisfy?

1. Equals must be reflexive: x.Equals(x) must return true.
2. Equals must be symmetric: x.Equals(y) and y.Equals(x) must return the same value.
3. Equals must be transitive: if x.Equals(y) returns true and y.Equals(z) returns true, then x.Equals(z) must return true.
4. Equals must be consistent: as long as the two values being compared don't change, the return value of Equals mustn't change either.

### Q. Besides the properties of equality, what else do you need to do when overriding Equals yourself?

1. Have the type implement the Equals method of the System.IEquatable\<T\> interface.
2. Overload the == and != operator methods.
3. Override the GetHashCode method so that the equality algorithm and the object hash code algorithm are consistent.

### Q. How does dynamic work?

When code uses a dynamic expression/variable to invoke a member, the compiler generates a payload that, at runtime, decides the actual operation to perform based on the actual type of the object referenced by the dynamic expression/variable.

If the type of a field, method parameter or method return value is dynamic, the compiler converts that type to System.Object and applies an instance of System.Runtime.CompilerServices.DynamicAttribute to the field, parameter or return type in the metadata.

If a local variable is specified as dynamic, the variable also becomes an Object, but DynamicAttribute isn't applied to the local variable.

### Q. The difference between dynamic and var

dynamic can be used for local variables, fields and parameters, while var can only be used to declare local variables inside a method.

dynamic can accept expressions; var can't.

Variables declared with dynamic don't need to be initialized, while var requires the variable to be explicitly initialized.

## Chapter 6 Types and Members

### Q. What are the common members of a type?

Constants, fields, instance constructors, type constructors, methods, operator overloads, conversion operators, properties, events, and types.

### Q. The difference between call and callvirt

- call

  This instruction can call static methods, instance methods and virtual methods. When call is used to call a static method, you must specify the type that defines the method. When call is used to call an instance or virtual method, you must specify a variable that refers to an object. The call instruction assumes this variable is not null. In other words, the type of the variable itself indicates which type defines the method. If the variable's type doesn't define the method, the base types are checked for a matching method. The call instruction is frequently used to call a virtual method non-virtually.

- callvirt

  This IL instruction can call instance methods and virtual methods, but not static methods. When callvirt is used to call an instance or virtual method, you must specify a variable that refers to an object. When callvirt is used to call a non-virtual instance method, the type of the variable indicates which type defines the method. When callvirt is used to call a virtual instance method, the CLR discovers the actual type of the object being used to make the call and then calls the method polymorphically. To determine the type, the variable used to make the call must never be null. In other words, when compiling this call, the JIT compiler generates code that verifies the variable's value isn't null; if it is, the callvirt instruction causes the CLR to throw a NullReferenceException. Precisely because of this extra check, the callvirt instruction executes slightly slower than the call instruction. Note that this null check is performed even when callvirt calls a non-virtual instance method.

## Chapter 7 Constants and Fields

### Q. Does defining a constant allocate memory? What's the difference between constants and static fields?

No, constants are embedded into the IL code.

Constants are initialized at compile time and embedded into the IL code. Static fields are initialized in the static type constructor, when the type object is first accessed.

Constants can only be accessed through instance objects of the type, while static fields can be accessed directly through the type.

### Q. When a field is marked readonly, what is it that can't change?

The reference, not the object the field refers to.

For example:

```csharp
public sealed class AType{
	public static readonly char[] InvalidChars = new char[] {'A', 'B', 'C'};    
}
```

This won't cause an error:

```csharp
AType.InvalidChars[0] = 'X';
AType.InvalidChars[1] = 'Y';
AType.InvalidChars[2] = 'Z';
```

This is what causes an error:

```csharp
AType.InvalidChars = new char[]{'X', 'Y', 'Z'};
```

## Chapter 8 Methods

### Q. How are a value type's instance constructors called?

If the value type only has a parameterless instance constructor, the default parameterless instance constructor is called implicitly when the value type is defined.

If the value type defines a parameterful instance constructor, the parameterful instance constructor has to be called explicitly.

### Q. When is a value type's type constructor called?

A value type's type constructor is called only the first time its type object is accessed, for example when accessing a static field, calling an instance or static method, or explicitly calling a parameterful instance constructor.

> Note: it's only the first time. After the type constructor has been called once, it won't be called again.

### Q. How do you define an extension method?

First define a static class, then define the extension method in that static class. Extension methods are always static methods.

## Chapter 9 Parameters

### Q. The differences and similarities between ref and out?

Similarities:

- Both ref and out can be used to return multiple values
- To use ref and out parameters, both the method definition and the calling code must explicitly use the ref and out keywords. Setting and changing the parameter inside the method directly affects the caller (the parameter's initial value).
- They generate the same IL.

Differences:

- A parameter marked ref must be initialized when the function is called and can't be an empty reference, whereas a parameter marked out doesn't need to be initialized when the function is called;
- A parameter marked out is cleared when entering the function and must be assigned an initial value inside the function. A parameter marked ref doesn't need this.
- Their records in the generated metadata differ by one bit, which records whether ref or out was specified when the method was declared.

ref goes both in and out; out only goes out, never in.

### Q. What are the design guidelines for parameters and return types?

When declaring a method's parameter types, specify the weakest type possible. When declaring a method's return type, specify the strongest type possible.

## Chapter 10 Properties

### Q. What does defining a property really amount to?

When you define a property that isn't auto-implemented, the compiler essentially generates a get_XXX method and a set_XXX method. When you define an auto-implemented property, the compiler essentially generates a get_XXX method, a set_XXX method and a private field; the get_XXX and set_XXX methods are implemented automatically by the compiler for you, returning the private field's value and setting the private field's value, respectively.

### Q. How is identity determined for anonymous types?

If anonymous types have the same structure (the same property names and types, specified in the same order), the compiler treats them as the same type.

### Q. How do you set the accessor method names for a parameterful property?

Define them with the IndexerName attribute.

> Note: if you use the IndexerName attribute to define one accessor method, then all parameterful properties need to be defined with this attribute. C# doesn't support defining multiple accessor methods with different names within a single class, but you can define accessor methods with the same name and different parameter sets.

## Chapter 11 Events

### Q. The relationship between events and delegates?

The event model is built on delegates. When you define an event in a class, the compiler implicitly defines a private delegate field, an add_XXX method (to register for the event) and a remove_XXX method (to unregister from the event) in that class. The add_XXX and remove_XXX methods are both thread-safe, mainly using Interlocked.CompareExchange\<T\> to achieve thread safety.

### Q. How do you raise an event in a thread-safe way?

You can use the Volatile.Read method.

## Chapter 12 Generics

### Q. What are the advantages of generics?

- Source code protection
- Type safety
- Cleaner code
- Better performance

### Q. What is an open type? What is a closed type?

Open type: a type that has generic type parameters.

Closed type: a type for which actual data types have been passed for all type parameters.

### Q. What is code explosion? How does the CLR deal with it?

The CLR has to generate native code for every distinct method/type combination. This is called code explosion.

The CLR deals with code explosion like this:

- If a method is called for a particular type argument, and later called again with the same type argument, the CLR compiles the code for that method/type combination only once. For example: if one assembly uses List\<DateTime\> and a completely different assembly (loaded into the same AppDomain) also uses List\<DateTime\>, the CLR compiles the methods for List\<DateTime\> only once.
- The CLR considers all reference type arguments to be identical, so the code can be shared (because a reference type argument or variable is really just a pointer to an object on the heap, and all pointers are manipulated the same way). For example, the code compiled for List\<DateTime\>'s methods can be used directly for List\<Stream\>'s methods, since String and Stream are both reference types. Note: code can't be shared for value type arguments.

### Q. The relationship and difference between contravariance and covariance?

Relationship: both contravariance and covariance are about type conversion.

Difference: contravariance means a generic type parameter can change from a class to one of its derived classes; C# marks it with the in keyword. Covariance means a generic type parameter can change from a class to one of its base classes; C# marks it with the out keyword.

### Q. The concepts of primary constraints, secondary constraints and constructor constraints?

Primary constraint: a type parameter specifies a constraint type, and the type argument specified must be either that constraint type or a type derived from it. (Special cases: class and struct)

```csharp
internal sealed class PrimaryConstraintOfStream<T> where T : Stream 
{
	public void M(T stream)
    {
        stream.Close();
    }
}
```

Secondary constraint: an interface constraint or a type parameter constraint. An interface constraint constrains a type parameter to interfaces. A type parameter constraint means the specified type argument must be either the constraining type or a type derived from it.

```csharp
//Interface constraint
private static Int32 M<T>(T t) where T : IComparable, IConvertible
{
    ...
}
//Type parameter constraint
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

Constructor constraint: if a constructor constraint is specified, the specified type argument must be a non-abstract type that implements a public parameterless constructor.

```csharp
internal sealed class ConstructorConstraint<T> where T : new()
{
    public static T Factory()
    {
        return new T();
    }
}
```



