---
title: 'Key Chapters of CLR via C#'
date: 2020-12-15T19:17:24
categories: [Programming Languages]
tags: [CLR]
toc: true
aiTranslated: true
---

Key chapters of CLR via C#.

<!--more-->

The checked items are the important ones. The unchecked ones should be read through; don't just skip them. Items with page numbers or highlighting are must-reads.

# Chapter 1 The CLR's Execution Model

- [x] 1.1 Compiling Source Code into Managed Modules
  - [x] The parts of a managed module (p5)
  - [x] Overview of metadata (p5)
- [x] 1.2 Combining Managed Modules into Assemblies
  - [x] **The concept of an assembly** (p6-7)
- [x] 1.3 Loading the Common Language Runtime
- [x] 1.4 Executing Your Assembly's Code
  - [x] **What the JITCompiler function does** (p11)
  - [x] Overview of IL (p15)
- [ ] 1.5 The Native Code Generator Tool: NGen.exe
- [x] 1.6 The Framework Class Library
  - [x] General FCL namespaces (p21)
- [x] 1.7 The Common Type System
  - [x] Access modifiers (p23)
- [x] 1.8 The Common Language Specification
  - [x] The relationship between C#, the CLR/CTS and the CLS (p25)
  - [x] The Test class and its IL (p26-27)
- [ ] 1.9 Interoperability with Unmanaged Code

# Chapter 2 Building, Packaging, Deploying, and Administering Applications and Types

- [ ] 2.1 .NET Framework Deployment Goals
- [x] 2.2 Building Types into a Module (hands-on practice recommended)
- [x] 2.3 **A Brief Look at Metadata**
  - [x] The concept of metadata (p33)
  - [x] The metadata tables (p34-35)
  - [x] Viewing metadata with IL tools (p35-38, hands-on practice recommended)
- [x] 2.4 Combining Modules to Form an Assembly
  - [x] Assemblies and manifests (p39)
  - [x] Manifest metadata tables (p41)
  - [x] /addmodule and the structure of a multi-module assembly (p42-43, hands-on practice recommended)
  - [x] AL.exe (p45-47, hands-on practice recommended)
- [ ] 2.5 Assembly Version Resource Information
  - [x] Version number format (p50)
- [ ] 2.6 Culture
  - [x] The concept of satellite assemblies (p51)
- [ ] 2.7 Simple Application Deployment (Privately Deployed Assemblies)
- [ ] 2.8 Simple Administrative Control (Configuration)

# Chapter 3 Shared Assemblies and Strongly Named Assemblies

- [x] 3.1 Two Kinds of Assemblies, Two Kinds of Deployment
  - [x] The difference between weakly named and strongly named assemblies (p58)
- [x] 3.2 Giving an Assembly a Strong Name
  - [x] The structure of a strongly named assembly's string identity (p59)
  - [x] The concept and process of signing (p59-63)
- [ ] 3.3 The Global Assembly Cache
- [ ] 3.4 Building an Assembly That References a Strongly Named Assembly
- [ ] 3.5 Strongly Named Assemblies Are Tamper-Resistant
- [ ] 3.6 Delayed Signing
- [ ] 3.7 Privately Deploying Strongly Named Assemblies
- [x] 3.8  **How the Runtime Resolves Type References** (understand the process, using the diagram on p72)
- [ ] 3.9 Advanced Administrative Control (Configuration)

# Chapter 4 Type Fundamentals

- [x] 4.1 All Types Are Derived from System.Object
  - [x] The methods of System.Object (p81-82)
  - [x] What the new operator does (p82-83)
- [x] 4.2 Casting Between Types
  - [x] The concepts of is and as and how they differ
  - [x] Type-safety quiz (code on p85, table on p86, hands-on practice recommended)
- [x] 4.3 Namespaces and Assemblies
  - [x] The relationship between namespaces and assemblies (p89)
- [x] 4.4 **How Things Relate at Run Time** (all of it is gold)

# Chapter 5 Primitive, Reference, and Value Types

- [x] 5.1 Programming Language Primitive Types
  - [x] C# primitive types and their corresponding FCL types (table on p100)
  - [x] checked and unchecked (p102-105, hands-on practice recommended, look at the IL)
- [x] 5.2 **Reference Types and Value Types**
  - [x] The concepts of and differences between reference types and value types (p106-109)
  - [x] How the CLR controls the layout of a type's fields (p110)
- [x] 5.3 **Boxing and Unboxing Value Types**
  - [x] The concept of boxing (p111)
  - [x] The concept of unboxing (p112)
  - [x] Some examples (p113-123, hands-on practice recommended, look at the IL)
  - [x] Equals and identity (p123-126)
- [x] 5.4 Object Hash Codes
- [x] 5.5 The dynamic Primitive Type
  - [x] The concept and features of dynamic
  - [x] The difference between dynamic and var (p130)
  - [ ] dynamic and reflection

# Chapter 6 Type and Member Basics

- [x] 6.1 **The Different Kinds of Type Members**
- [x] 6.2 Type Visibility
- [x] 6.3 Member Accessibility
- [x] 6.4 **Static Classes**
- [x] 6.5 Partial Classes, Structures, and Interfaces
- [x] 6.6 Components, Polymorphism, and Versioning
  - [x] How C# keywords affect versioning (table on p144)
  - [x] How the CLR calls virtual methods, properties, and events
    - [x] **The difference between call and callvirt** (p145-147)

# Chapter 7 Constants and Fields

- [x] 7.1 Constants
- [x] 7.2 Fields

# Chapter 8 Methods

- [x] 8.1 Instance Constructors and Classes (Reference Types)
- [x] 8.2 Instance Constructors and Structures (Value Types)
- [x] 8.3 Type Constructors
  - [x] **When does a value type's type constructor get called?** (think about it; hands-on practice strongly recommended)
- [ ] 8.4 Operator Overload Methods
- [ ] 8.5 Conversion Operator Methods
- [x] 8.6 Extension Methods (hands-on practice recommended)
- [x] 8.7 Partial Methods (hands-on practice recommended)

# Chapter 9 Parameters

- [x] 9.1 Optional and Named Parameters (hands-on practice recommended)
- [x] 9.2 Implicitly Typed Local Variables (hands-on practice recommended)
- [x] 9.3 Passing Parameters by Reference to a Method
  - [x] **The differences and similarities between out and ref** (p190-195, hands-on practice strongly recommended, look at the IL)
- [x] 9.4 Passing a Variable Number of Arguments to a Method
  - [x] The Concat method and params (p197)
- [x] 9.5 Parameter and Return Type Guidelines
- [x] 9.6 Const-ness
  - [x] **What does immutable mean?** (think about it)

# Chapter 10 Properties

- [x] 10.1 Parameterless Properties
  - [x] **What properties really are** (p203-p205)
  - [x] Object and collection initializers (p208)
  - [x] Anonymous types (p209)
  - [ ] The Tuple type
- [x] 10.2 Parameterful Properties
  - [x] The concept of parameterful properties (p214-217)
  - [x] The IndexerName attribute (p217-218)
- [ ] 10.3 The Performance of Calling Property Accessor Methods
- [ ] 10.4 Property Accessor Accessibility
- [ ] 10.5 Generic Property Accessor Methods

# Chapter 11 Events

- [x] 11.1 Designing a Type That Exposes an Event
  - [x] The steps to define an event (p222-226, hands-on practice recommended)
  - [x] **How to raise an event in a thread-safe way** (p225)
- [x] 11.2 How the Compiler Implements an Event
  - [x] **What events really are, how events relate to delegates, and how events achieve thread safety** (p227-228)
- [x] 11.3 Designing a Type That Listens for an Event (hands-on practice recommended)
- [x] 11.4 Explicitly Implementing an Event (hands-on practice recommended)

# Chapter 12 Generics

- [x] 12.1 Generics in the Framework Class Library
- [x] 12.2 Generics Infrastructure
  - [x] **Open and closed types** (p239-240, hands-on practice recommended)
  - [x] Generic types and inheritance (p240, hands-on practice recommended)
  - [x] Generic type identity (p242)
  - [x] Code explosion (p243)
- [x] 12.3 Generic Interfaces
- [x] 12.4 Generic Delegates
- [x] 12.5 **Delegate and Interface Contra-variant and Covariant Generic Type Arguments**
- [x] 12.6 Generic Methods
- [x] 12.7 Generics and Other Members
- [x] 12.8 **Verifiability and Constraints**
  - [x] Primary constraints (p252)
  - [x] Secondary constraints (p253)
  - [x] Constructor constraints (p254)
  - [x] Other verifiability issues (p254-257)

# Chapter 13 Interfaces

- [x] 13.1 Class and Interface Inheritance
- [x] 13.2 Defining an Interface
- [x] 13.3 Inheriting an Interface
- [x] 13.4 More About Calling Interface Methods
- [x] 13.5 **Implicit and Explicit Interface Method Implementations (What's Happening Behind the Scenes)**
- [x] 13.6 Generic Interfaces
- [x] 13.7 Generics and Interface Constraints
- [x] 13.8 **Implementing Multiple Interfaces That Have the Same Method Name and Signature**
- [x] 13.9 Improving Compile-Time Type Safety with Explicit Interface Method Implementations
- [x] 13.10 Be Careful with Explicit Interface Method Implementations
- [ ] 13.11 Design: Base Class or Interface?

# Chapter 14 Chars, Strings, and Working with Text

- [x] 14.1 Characters
- [x] 14.2 The System.String Type
  - [x] **Strings are immutable** (p284)
  - [x] Comparing strings
  - [ ] Language and culture
  - [x] **String interning** (p290-292)
  - [x] **String pooling** (p293)
  - [ ] Examining a string's characters and text elements
  - [ ] Other string operations
- [x] 14.3 Constructing a String Efficiently
  - [x] Constructing a StringBuilder object (p296)
  - [x] StringBuilder members (p297-298)
- [ ] 14.4 Obtaining a String Representation of an Object: ToString
- [ ] 14.5 Parsing a String to Obtain an Object: Parse
- [x] 14.6 **Encodings: Converting Between Characters and Bytes**
  - [x] The differences between encodings such as UTF-8, UTF-16 and UTF-32 (p309)
  - [x] Encoding and decoding (p309-315)
- [ ] 14.7 Secure Strings

# Chapter 15 Enumerated Types and Bit Flags

- [x] 15.1 Enumerated Types
  - [x] **What enumerated types really are** (p320)
  - [x] How to change an enumerated type's underlying type (p321)
  - [x] **Is an enumerated type a reference type or a value type? Is System.Enum a reference type or a value type?** (think about it)
- [x] 15.2 Bit Flags
- [x] 15.3 Adding Methods to Enumerated Types

# Chapter 16 Arrays

- [x] 16.0 Overview of arrays (it has no heading, but it's very important)
  - [x] **Arrays are reference types** (p329)
  - [x] **The memory layout of arrays** (p330)
  - [x] **Concepts of single-dimensional, multi-dimensional, zero-based and non-zero-based arrays** (p330-331)
- [x] 16.1 Initializing Array Elements
- [x] 16.2 Casting Arrays
  - [x] **What the Array.Copy method does** (p334)
- [x] 16.3 All Arrays Are Implicitly Derived from System.Array
- [x] 16.4 All Arrays Implicitly Implement IEnumerable, ICollection, and IList
- [x] 16.5 Passing and Returning Arrays
- [x] 16.6 Creating Non-Zero Lower Bound Arrays
- [x] 16.7 **Array Internals**
- [x] 16.8 Unsafe Array Access and Fixed-Size Arrays

# Chapter 17 Delegates

- [x] 17.1 A First Look at Delegates
- [x] 17.2 Using Delegates to Call Back Static Methods
- [x] 17.3 Using Delegates to Call Back Instance Methods
- [x] 17.4 **Demystifying Delegates**
- [x] 17.5 **Using Delegates to Call Back Many Methods (Chaining)**
  - [x] **Are delegates immutable?** (think about it)
- [x] 17.6 Enough with the Delegate Definitions Already (Generic Delegates)
- [x] 17.7 C#'s Syntactical Sugar for Delegates
  - [x] Syntactical shortcut #1: no need to construct a delegate object (p360)
  - [x] **Syntactical shortcut #2: no need to define a callback method (lambda expressions)**  (p361)
  - [x] **Syntactical shortcut #3: no need to manually wrap local variables in a class to pass them to a callback method** (p364)
- [x] 17.8 Delegates and Reflection

# Chapter 18 Custom Attributes

- [x] 18.1 Using Custom Attributes
- [x] 18.2 **Defining Your Own Attribute Class**
- [x] 18.3 Attribute Constructor and Field/Property Data Types
- [x] 18.4 Detecting the Use of a Custom Attribute
  - [x] **IsDefined, GetCustomAttribute, GetCustomAttributes** (p379-382)
- [x] 18.5 Matching Two Attribute Instances Against Each Other
- [ ] 18.6 Detecting the Use of a Custom Attribute Without Creating Attribute-Derived Objects
- [ ] 18.7 Conditional Attribute Classes

# Chapter 19 Nullable Value Types

- [x] 19.0 **System.Nullable\<T\>**
- [x] 19.1 C#'s Support for Nullable Value Types
- [x] 19.2 C#'s Null-Coalescing Operator
- [x] 19.3 **The CLR Has Special Support for Nullable Value Types**
  - [x] Boxing nullable value types (p394)
  - [x] Unboxing nullable value types (p395)
  - [x] Calling GetType via a nullable value type
  - [x] Calling interface methods via a nullable value type

# Chapter 20 Exceptions and State Management

- [x] 20.1 Defining "Exception"
- [x] 20.2 Exception-Handling Mechanics
  - [x] The try block (p402)
  - [x] **The catch block** (p402-403)
  - [x] **The finally block** (p404-406)
- [x] 20.3 The System.Exception Class
  - [x] **Public properties of System.Exception** (p407)
- [ ] 20.4 FCL-Defined Exception Classes
- [ ] 20.5 Throwing an Exception
- [x] 20.6 Defining Your Own Exception Class
- [ ] 20.7 Trading Reliability for Productivity
- [x] 20.8 Guidelines and Best Practices
- [x] 20.9 Unhandled Exceptions
- [ ] 20.10 Debugging Exceptions
- [ ] 20.11 Exception-Handling Performance Considerations
- [x] 20.12 Constrained Execution Regions (CERs)
- [ ] 20.13 Code Contracts

# Chapter 21 The Managed Heap and Garbage Collection (all of it is gold)

- [x] 21.1 **Managed Heap Basics**
- [x] 21.2 **Generations: Improving Performance**
  - [x] **Generations 0, 1 and 2** (p454-457)
  - [x] Garbage collection triggers (p458-459)
  - [x] Large objects (p459)
  - [x] **Garbage collection modes** (p459-462)
  - [x] Forcing garbage collections (p462-463)
  - [ ] Monitoring your application's memory usage
- [x] 21.3 **Working with Types Requiring Special Cleanup**
  - [x] **SafeHandle, CriticalFinalizerObject** (p467)
  - [x] **IDisposable, Dispose** (p471)
  - [x] **Other GC features for use with native resources** (p475-479, hands-on practice strongly recommended)
  - [x] **Finalization internals** (p479-481)
  - [x] **Monitoring and controlling the lifetime of objects manually** (p481-487)

# Chapter 22 CLR Hosting and AppDomains

- [x] 22.1 CLR Hosting
- [x] 22.2 **AppDomains**
  - [x] Diagram of AppDomain hosting structure (p493)
  - [x] **Accessing objects across AppDomain boundaries** (p494-504)
- [x] 22.3 AppDomain Unloading
- [ ] 22.4 AppDomain Monitoring
- [ ] 22.5 AppDomain First-Chance Exception Notifications
- [ ] 22.6 How Hosts Use AppDomains
- [ ] 22.7 Advanced Host Control

# Chapter 23 Assembly Loading and Reflection

- [x] 23.1 **Assembly Loading**
  - [x] **Load, LoadFrom and other methods**(p516-519)
- [ ] 23.2 Using Reflection to Build a Dynamically Extensible Application
- [x] 23.3 Reflection Performance
- [ ] 23.4 Designing an Application That Supports Add-Ins
- [x] 23.5 **Using Reflection to Discover a Type's Members**

# Chapter 24 Runtime Serialization



