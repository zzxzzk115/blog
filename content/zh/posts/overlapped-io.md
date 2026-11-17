---
title: 'Overlapped I/O：异步、非阻塞式 I/O 技术'
date: 2021-06-21T10:32:47
categories: [系统编程]
tags: [multithreading, win32, OverlappedI-O]
toc: true
---

# Overlapped I/O 简介

Overlapped I/O 是 Win32 的一项技术，你可以要求操作系统为你传送数据，并且在传送完毕时通知你。这项技术使你的程序在 I/O 进行过程中仍然能够继续处理事务。它又被称为非阻塞 I/O 或异步 I/O 。

假设一个线程向设备发出一个异步 I/O 请求。这个 I/O 请求被传给设备驱动程序，后者负责完成实际的 I/O 操作。当驱动程序在等待设备响应的时候，应用程序的线程并没有因为要等待 I/O 请求完成而被挂起，线程会继续运行并执行其它有用的任务。

它包含从简单到高级的四种异步 I/O 的方式：

- 激发的 File Handles
- 激发的 Event Objects
- 异步过程调用(Asynchronous Procedure Call, APC)
- I/O Completion Port (IOCP)

# 使用 Overlapped I/O 的前提

为了以异步的方式访问设备，我们需要调用 Win32 的 CreateFile 函数，并指定 dwFlagsAndAttributes 参数为 FILE_FLAG_OVERLAPPED 标志来打开设备。这个标志告诉操作系统，我们想以异步的方式来访问设备。

为了将 I/O 请求加入设备驱动程序的队列中，我们必须使用 Win32 的 ReadFile 和 WriteFile 函数。

## CreateFile 函数

不要被它的名称愚弄了，它不仅可以打开文件(File)，还可以打开更多其它设备。

```cpp
HANDLE CreateFile(
    PCTSTR pszName,
    DWORD dwDesiredAccess,
    DWORD dwShareMode,
    PSECURITY_ATTRIBUTES psa,
    DWORD dwCreationDisposition,
    DOWRD dwFlagsAndAttributes,
    HANDLE hFileTemplate
);
```

pszName 既表示设备类型，也表示该类设备的某个实例。

dwDesiredAccess 指定我们想以何种方式来和设备进行数据传输。

dwShareMode 指定设备共享特权。

psa 指定安全信息。

dwCreationDisposition 指定创建方式。

最关键的，dwFlagsAndAttributes 有两个用途：

- 可以设置一些标志来微调与设备间的通信
- 如果设备是一个文件，我们还能设置文件的属性

**如果设置 dwFlagsAndAttributes 为 FILE_FLAG_OVERLAPPED ，则表示希望通过异步方式访问设备。**

## ReadFile 函数 和 WriteFile 函数

Win32 分别提供了 ReadFile 函数和 WriteFile 函数来完成对设备的数据进行读/写操作。

```cpp
HANDLE ReadFile(
    HANDLE hFile,
    PVOID pvBuffer,
    DWORD nNumBytesToRead,
    PDWORD pdwNumBytes,
    OVERLAPPED* pOverlapped
);

HANDLE WriteFile(
    HANDLE hFile,
    CONST VOID *pvBuffer,
    DWORD nNumBytesToWrite,
    PDWORD pdwNumBytes,
    OVERLAPPED* pOverlapped
);
```

当调用这两个函数的任何一个时，函数会检查 hFile 参数标识的设备是否是用 FILE_FLAG_OVERLAPPED 标志打开的。如果打开设备时指定了这个标志，那么函数会执行异步 I/O。

## OVERLAPPED 结构

执行异步设备 I/O 的时候，必须在 pOverlapped 参数中传入一个已经初始化的 OVERLAPPED 结构。

```cpp
typedef struct _OVERLAPPED{    
    DWORD Internal;			// [out] Error code
    DWORD InternalHigh;		// [out] Number of bytes transferred
    DWORD Offset;			// [in]  Low 32-bit file offset
    DWORD OffsetHigh;		// [in]  High 32-bit file offset
    HANDLE hEvent;			// [in]  Event handle or data
} OVERLAPPED, *LPOVERLAPPED;
```

| 成员名称     | 说明                                                         |
| ------------ | ------------------------------------------------------------ |
| Internal     | 通常被保留。当 GetOverlappedResult() 传回 FALSE 并且 GetLastError() 并非传回 ERROR_IO_PENDING 时，此栏位将包含一个视系统而定的状态 |
| InternalHigh | 通常被保留。当 GetOverlappedResult() 传回 TRUE 时，此栏位将包含"被传输数据的长度" |
| Offset       | 文件之中开始读或者被写的偏移位置(从文件头开始)。非文件设备会忽略此栏位，如果向非文件设备发起异步 I/O 请求，则此处应该被初始化为 0，否则请求失败，GetLastError 会返回 ERROR_INVALID_PARAMETER |
| OffsetHigh   | 64 位文件偏移位置中的较高的 32 位。非文件设备会忽略此栏位，如果向非文件设备发起异步 I/O 请求，则此处应该被初始化为 0，否则请求失败，GetLastError 会返回 ERROR_INVALID_PARAMETER |
| hEvent       | 一个手动重置事件对象的句柄，当 Overlapped I/O 完成时，该事件被激发。ReadFileEx() 和 WriteFileEX() 会忽略此栏位，此时用户可以用此栏位来传递一个自定义的对象的指针 |

 