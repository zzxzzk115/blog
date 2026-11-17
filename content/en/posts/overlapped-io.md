---
title: 'Overlapped I/O: Asynchronous, Non-Blocking I/O'
date: 2021-06-21T10:32:47
categories: [Systems Programming]
tags: [multithreading, win32, OverlappedI-O]
toc: true
aiTranslated: true
---

# Introduction to Overlapped I/O

Overlapped I/O is a Win32 technique where you ask the operating system to transfer data for you and notify you when the transfer is done. It lets your program keep handling other work while I/O is in progress. It's also known as non-blocking I/O or asynchronous I/O.

Suppose a thread issues an asynchronous I/O request to a device. The request is handed to the device driver, which is responsible for carrying out the actual I/O operation. While the driver waits for the device to respond, the application's thread is not suspended waiting for the I/O request to complete; it keeps running and does other useful work.

It comes in four flavors of asynchronous I/O, ranging from simple to advanced:

- Signaled File Handles
- Signaled Event Objects
- Asynchronous Procedure Calls (APC)
- I/O Completion Port (IOCP)

# Prerequisites for Using Overlapped I/O

To access a device asynchronously, we need to call the Win32 CreateFile function and open the device with the FILE_FLAG_OVERLAPPED flag in the dwFlagsAndAttributes parameter. This flag tells the operating system that we want to access the device asynchronously.

To queue I/O requests to the device driver, we have to use the Win32 ReadFile and WriteFile functions.

## The CreateFile Function

Don't be fooled by its name: it can open not only files but many other kinds of devices as well.

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

pszName identifies both the device type and a specific instance of that type of device.

dwDesiredAccess specifies how we want to transfer data to and from the device.

dwShareMode specifies the device sharing privileges.

psa specifies the security information.

dwCreationDisposition specifies how the file is created.

Most importantly, dwFlagsAndAttributes serves two purposes:

- You can set flags to fine-tune communication with the device
- If the device is a file, you can also set the file's attributes

**Setting dwFlagsAndAttributes to FILE_FLAG_OVERLAPPED means you want to access the device asynchronously.**

## The ReadFile and WriteFile Functions

Win32 provides the ReadFile and WriteFile functions for reading data from and writing data to a device.

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

When you call either of these functions, it checks whether the device identified by hFile was opened with the FILE_FLAG_OVERLAPPED flag. If the flag was specified when the device was opened, the function performs asynchronous I/O.

## The OVERLAPPED Structure

When performing asynchronous device I/O, you must pass an initialized OVERLAPPED structure in the pOverlapped parameter.

```cpp
typedef struct _OVERLAPPED{    
    DWORD Internal;			// [out] Error code
    DWORD InternalHigh;		// [out] Number of bytes transferred
    DWORD Offset;			// [in]  Low 32-bit file offset
    DWORD OffsetHigh;		// [in]  High 32-bit file offset
    HANDLE hEvent;			// [in]  Event handle or data
} OVERLAPPED, *LPOVERLAPPED;
```

| Member       | Description                                                  |
| ------------ | ------------------------------------------------------------ |
| Internal     | Normally reserved. When GetOverlappedResult() returns FALSE and GetLastError() does not return ERROR_IO_PENDING, this field contains a system-dependent status |
| InternalHigh | Normally reserved. When GetOverlappedResult() returns TRUE, this field contains "the number of bytes transferred" |
| Offset       | The offset in the file (from the start of the file) at which to begin reading or writing. Non-file devices ignore this field; if you issue an async I/O request to a non-file device, it should be initialized to 0, otherwise the request fails and GetLastError returns ERROR_INVALID_PARAMETER |
| OffsetHigh   | The high 32 bits of the 64-bit file offset. Non-file devices ignore this field; if you issue an async I/O request to a non-file device, it should be initialized to 0, otherwise the request fails and GetLastError returns ERROR_INVALID_PARAMETER |
| hEvent       | A handle to a manual-reset event object that is signaled when the overlapped I/O completes. ReadFileEx() and WriteFileEx() ignore this field, in which case you can use it to pass a pointer to a custom object |

 
