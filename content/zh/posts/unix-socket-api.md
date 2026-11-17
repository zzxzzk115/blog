---
title: 'Unix 网络编程：套接字联网 API'
date: 2021-07-08T17:14:42
categories: [后端]
tags: [TCP-IP, Unix, Socket, API]
toc: true
---

# 简介

## 概述

### 网络程序设计思想

设计网络程序，首先要确定通信协议(protocol)，要在高层决断通信由哪个程序发起以及响应在何时发生。

### 守护程序

一个长时间运行的程序，即守护程序(daemon)。一般而言 Web 服务器程序是一种守护程序。

### C/S 模式

大多数网络应用按照划分成客户端(client) 和服务器(server) 来组织的，即 C/S 模式。客户端和服务器间通过应用协议来通信。

![](http://img.zhangkexuan.cn/markdown_20210708173859.png)

### Web 应用的通信过程

Web 客户端应用(浏览器) 对 Web 服务器发起请求时，在应用层一般使用 HTTP/HTTPS 协议进行通信，进而在传输层使用 TCP 协议进行通信，进而在网络层使用 IP 协议进行通信，进而在链路层使用以太网协议进行通信，最后在物理层通过传输介质传输比特流。然后反向再从物理层到应用层一层一层通信，最后服务端收到数据。![](http://img.zhangkexuan.cn/markdown_20210708173952.png)

### OSI 模型

描述网络中各个协议层的常用方法是使用国际标准化组织(International Organization for Standardization, ISO) 提出的计算机通信开放系统互联(Open Systems Interconnection, OSI) 模型。OSI 模型是七层网络模型。

![](http://img.zhangkexuan.cn/markdown_20210708174451.png)

上图，黑色加粗的线将 OSI 模型的顶上层和底下四层分开。之所以这样，有两个原因：

- 顶上三层处理具体网络应用的所有细节，但对通信细节了解很少。底下四层对具体网络应用了解不多，但处理了所有的通信细节。
- 顶上三层属于用户进程的行为。底下四层属于操作系统内核的行为。

### Unix 标准

#### POSIX

POSIX(Portable Operating System Interface)，即可移植操作系统接口。它并不是单个标准，而是由电气与电子工程师学会(the Institute for Electrical and Electronics Engineers, Inc.) 即 IEEE 开发的一系列标准。

# 传输层：TCP、UDP 和 SCTP

## 概述

传输层通常使用 TCP、UDP，SCTP(Stream Control Transmission Protocol，流控制传输协议) 是比较新的协议。

UDP 是一个简单的、不可靠的数据报协议；TCP 是一个复杂、可靠的字节流协议。SCTP 比 TCP 还多了消息边界、传输级别多宿(multihoming) 支持以及将头端阻塞(head-of-line blocking) 减少到最小的一种方法。

## 总图

TCP/IP 协议族总图如下：

![](http://img.zhangkexuan.cn/markdown_20210708192122.png)

## 用户数据报协议(UDP)

### UDP 的问题

缺乏可靠性，它不保证数据报会到达最终目的地，不保证各个数据报的先后顺序跨网络后不变，也不保证每个数据报只到达一次；数据报校验和检测出错，或者被丢弃，也不会被自动重传。

## 传输控制协议(TCP)

TCP 与 UDP 不同，它提供可靠传输，它是面向连接的。

### TCP 与 UDP 的区别

- TCP 面向连接，而 UDP 是无连接(connectionless) 的。

- TCP 提供了可靠性(reliability)，它提供确认、序列号、RTT 估算、超时和重传等机制，而这些机制 UDP 一个也没有提供。

- TCP 提供了流量控制(flow control)。TCP 总是告知对端在任何时刻它一次能够从对端接收多少字节的数据，这称为通告窗口(advertised window)。窗口大小会动态更改至合适。

- TCP 是全双工的(full-duplex)。在一个给定的连接上应用可以在任何时刻在进出两个方向上既发送数据又接收数据。

  > UDP 其实也可以是全双工的。

## 流控制传输协议(SCTP)

SCTP 与 TCP 大多相同，不同的是，它是面向消息(message-oriented) 的，它还提供了多宿特性，使得单个 SCTP 端点能够支持多个 IP 地址。

## TCP 连接的建立和终止

### 三次握手

![](http://img.zhangkexuan.cn/markdown_20210708200352.png)

### TCP 常用选项

- MSS 选项。即最大段大小(Maximum Segment Size)，也就是它在本连接的每个 TCP 段中愿意接收的最大数据量。
- 窗口大小选项。
- 时间戳选项。

### 四次挥手

![](http://img.zhangkexuan.cn/markdown_20210708200846.png)

### TCP 状态图

![](http://img.zhangkexuan.cn/markdown_20210708200954.png)

### TIME_WAIT 状态



## 端口号

端口号 16 位。

客户端常常使用临时端口(ephemeral port)，客户端无需关心。

- 熟知端口号：0~1023
- 注册端口号：1024~49151
- 动态端口号：49152~65535

![](http://img.zhangkexuan.cn/markdown_20210708201913.png)

## 套接字对

套接字是标识端点的两个值(IP 和端口号)。

一个套接字对则定义了一个连接的四元组(本地 IP 地址、本地 TCP 端口号、目标 IP 地址、目标 TCP 端口号)。

## TCP 端口号与并发服务器

Linux 的并发服务器采用 fork 函数生成子进程的方式来实现。

![](http://img.zhangkexuan.cn/markdown_20210708204317.png)

![](http://img.zhangkexuan.cn/markdown_20210708204331.png)

![](http://img.zhangkexuan.cn/markdown_20210708204346.png)

# 套接字编程简介

## IPv4 套接字地址结构

```c
struct in_addr {
    in_addr_t s_addr;				/* 32-bit IPv4 address */
    								/* network byte ordered */
}

struct sockaddr_in {
    uint8_t			sin_len;		/* length of structure (16) */
    sa_family_t		sin_family;		/* AF_INET */
    in_port_t 		sin_port;		/* 16-bit TCP or UDP port number */
    								/* network byte ordered */
    struct in_addr	sin_addr;		/* 32-bit IPv4 address */
    								/* network byte ordered */
    char			sin_zero[8];	/* unused */
}
```

