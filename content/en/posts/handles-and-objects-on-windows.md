---
title: '[Translation] Handles and Objects on Windows'
date: 2021-01-22T15:23:47
categories: [Systems Programming]
tags: [Windows, Handles, Objects]
toc: true
aiTranslated: true
---

How should we understand the two concepts of Handles and Objects in Windows?

<!--more-->

# Handles and Objects

In Windows, **an object is a data structure that represents a system resource, such as a file, a thread, a graphic image, and so on...**

However, an application can't directly access an object's data or the system resource the object represents. Instead, the application has to obtain an object **handle**, which it can use to examine and modify the system resource.

Each handle has an entry in an internally maintained table. These entries contain the address of the resource and a means of identifying the resource type.

## Why Windows has these two concepts

The system uses objects and handles to regulate access to system resources for two main reasons. First, using objects ensures that Microsoft can update system functionality as long as the original object interface is maintained. When later versions of the system are released, we can use the updated objects without doing any extra work.

Second, using objects lets us take advantage of Windows security. Each object has its own access-control list (ACL) that specifies the actions processes can perform on the object. The system checks an object's ACL every time an application creates a handle to the object.

## Object Manager

An object consists of a standard header and object-specific attributes. Because all objects have the same structure, there's a single object manager in Windows that maintains all objects.

The object header includes items such as the object's name, so that other processes can refer to the object by name, and a security descriptor, so that the object manager can control which processes access the system resource.

The tasks performed by the object manager include:

- Creating objects
- Verifying that a process has the right to use an object
- Creating object handles and returning them to the caller
- Maintaining resource quotas
- Creating duplicate handles
- Closing handles to objects

## Object Interface

Windows provides functions that perform the following tasks:

- Create an object
- Get an object handle
- Get information about an object
- Set information about an object
- Close an object handle
- Destroy an object

Some of these tasks aren't necessary for every object, and some of them are combined for certain objects. For example, an application can create an event object. Other applications can open the event to get a unique handle to that event object. When each application is done with the event, it closes its handle to the object. When there are no open handles left to the event object, the system destroys it. By contrast, an application can get a handle to an existing window object. When the window object is no longer needed, the application has to destroy the object, which invalidates the window handle.

Sometimes an object stays in memory even after all its handles have been closed. For example, a thread can create an event object and wait on the event handle. While the thread is waiting, another thread can close the same event object handle. The event object stays in memory, without any event object handles, until it's set to the signaled state and the wait operation completes. At that point the system removes the object from memory.

Handles and objects consume memory. So to preserve system performance, you should close handles and destroy objects as soon as you no longer need them. If you don't, your application can hurt system performance through excessive use of the paging file.

When a process terminates, the system automatically closes the handles and deletes the objects the process created. However, when a thread terminates, the system generally doesn't close handles or delete objects. The only exceptions are window, hook, window position, and dynamic data exchange (DDE) conversation objects; these are destroyed when the thread that created them terminates.

## Handle Limitations

Some objects support only one handle at a time. The system provides the handle when the application creates the object, and invalidates the handle when the application destroys the object. Other objects support multiple handles to a single object. After the last handle to the object is closed, the operating system automatically removes the object from memory.

The total number of open handles in the system is limited only by the amount of available memory. Some object types support a limited number of handles per session or per process.

## Handle Inheritance

A child process can inherit handles from its parent process. An inherited handle is valid only in the context of the child process. To let a child process inherit open handles from its parent, use the following steps:

1. Create the handle with the **bInheritHandle** member set to TRUE.
2. Create the child process with the **CreateProcess** function, setting the **bInheritHandle** parameter to TRUE.

The DuplicateHandle function duplicates a handle to be used in the current process or in another process. If an application duplicates one of its handles for another process, the duplicated handle is valid only in the context of the other process.

A duplicated or inherited handle is a unique value, but it refers to the same object as the original handle. Processes can inherit or duplicate handles to the following types of objects:

- Access Token
- Communications device
- Console input
- Console screen buffer
- Desktop
- Directory
- Event
- File
- File mapping
- Job
- Mailslot
- Mutex
- Pipe
- Process
- Registry key
- Semaphore
- Socket
- Thread
- Timer
- Window station

All other objects are private to the process that created them; their object handles can't be duplicated or inherited.

## Object Categories

Objects fall into these categories:

- User Objects
- GDI Objects (graphics device interface objects)
- Kernel Objects

User objects support window management, GDI objects support graphics, and kernel objects support memory management, process execution, and interprocess communication (IPC).

### User Objects

User objects support only one handle per object. Processes can't inherit or duplicate handles to user objects. Processes in one session can't reference a user handle in another session.

There's a theoretical limit of 65,536 user handles per session. However, the maximum number of user handles that can be opened per session is usually lower, since it's affected by available memory. There's also a default per-process limit of user handles. To change this limit, set the following registry value:

`HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Windows\USERProcessHandleQuota`

This value can be set to a number between 200 and 18,000.

#### Handles to User Objects

Handles to user objects are public to all processes. That is, any process can use a user object handle, provided the process has security access to the object.

In the following illustration, an application creates a window object. The CreateWindow function creates the window object and returns an object handle:

![](/img/markdown_20210122165016.png)

After creating the window object, the application can use the window handle to display or change the window. The handle remains valid until the window object is destroyed.

In the next example, the application destroys the window object. The DestroyWindow function removes the window object from memory, which invalidates the window handle:

![](/img/markdown_20210122165311.png)

### GDI Objects

GDI objects support only one handle per object. Handles to GDI objects are private to a process. That is, only the process that created the GDI object can use the GDI object handle.

There's a theoretical limit of 65,536 GDI handles per session. However, the maximum number of GDI handles that can be opened per session is usually lower, since it's affected by available memory.

There's also a default per-process limit for GDI handles. To change this limit, set the following registry value:

`HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Windows\GDIProcessHandleQuota`

This value can be set to a number between 256 and 65,536.

### Kernel Objects

Kernel object handles are process-specific. That is, a process must either create the object or open an existing object to get a kernel object handle. The per-process limit on kernel handles is 2 to the 24th power. However, handles are stored in the paged pool, so the actual number of handles you can create depends on available memory. The number of handles you can create on 32-bit Windows is significantly lower than 2 to the 24th power.

Any process can create a new handle to an existing kernel object (even one created by another process), provided the process knows the object's name and has security access to the object. Kernel object handles include access rights that indicate which actions can be granted or denied to a process. An application specifies the access rights when it creates an object or gets a handle to an existing one. Each type of kernel object supports its own set of access rights. For example, event handles can have set or wait access (or both), file handles can have read or write access (or both), and so on.

In the following illustration, an application creates an event object. The CreateEvent function creates the event object and returns an object handle:

![](/img/markdown_20210122170731.png)

After creating the event object, the application can use the event handle to set or wait on the event. The handle remains valid until the application closes it or terminates.

Most kernel objects support multiple handles to a single object. For example, the application in the previous illustration could get additional event object handles by using the OpenEvent function, as shown in the following illustration:

![](/img/markdown_20210122170822.png)

This approach lets an application have handles with different access rights. For example, Handle 1 might have set and wait access to the event, while Handle 2 might have only wait access.

If another process knows the event name and has security access to the object, it can use OpenEvent to create its own event object handle. The creating application could also use the DuplicateHandle function to duplicate one of its handles into the same process or into another process.

An object remains in memory as long as at least one object handle exists. In the following illustration, the applications use the CloseHandle function to close their event object handles. When there are no event handles left, the system removes the object from memory, as shown in the following illustration:

![](/img/markdown_20210122171155.png)

The system manages file objects a bit differently from other kernel objects. File objects contain the file pointer, the pointer to the next byte to be read or written in the file. Whenever an application creates a new file handle, the system creates a new file object. So more than one file object can refer to a single file on disk, as shown in the following illustration:

![](/img/markdown_20210122171322.png)

Multiple file handles can refer to the same file object only through duplication or inheritance, as shown in the following illustration:

![](/img/markdown_20210122171926.png)



____

Translated from [https://docs.microsoft.com/en-us/windows/win32/sysinfo/handles-and-objects](https://docs.microsoft.com/en-us/windows/win32/sysinfo/handles-and-objects)

