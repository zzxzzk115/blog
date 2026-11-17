---
title: 'Unix Network Programming: The Sockets Networking API'
date: 2021-07-08T17:14:42
categories: [Backend]
tags: [TCP-IP, Unix, Socket, API]
toc: true
aiTranslated: true
---

# Introduction

## Overview

### Thinking about network program design

When designing a network program, the first thing to decide is the communication protocol, and at a high level you need to decide which program initiates the communication and when responses happen.

### Daemons

A long-running program is called a daemon. Generally speaking, a web server program is a kind of daemon.

### The client/server model

Most network applications are organized as a client and a server, i.e. the C/S model. The client and server communicate via an application protocol.

![](http://img.zhangkexuan.cn/markdown_20210708173859.png)

### How a web application communicates

When a web client application (a browser) makes a request to a web server, it typically communicates using HTTP/HTTPS at the application layer, which in turn uses TCP at the transport layer, IP at the network layer, and Ethernet at the link layer, and finally the bit stream is transmitted over the physical medium at the physical layer. Then the data goes back up layer by layer, from the physical layer to the application layer, and finally the server receives it. ![](http://img.zhangkexuan.cn/markdown_20210708173952.png)

### The OSI model

A common way to describe the protocol layers in a network is the Open Systems Interconnection (OSI) model for computer communications, developed by the International Organization for Standardization (ISO). The OSI model is a seven-layer network model.

![](http://img.zhangkexuan.cn/markdown_20210708174451.png)

In the figure above, the thick black line separates the top layers of the OSI model from the bottom four layers. There are two reasons for this:

- The top three layers handle all the details of the specific network application but know very little about the communication details. The bottom four layers know little about the specific network application but handle all the communication details.
- The top three layers are what user processes do. The bottom four layers are what the operating system kernel does.

### Unix standards

#### POSIX

POSIX stands for Portable Operating System Interface. It isn't a single standard, but a family of standards developed by the Institute for Electrical and Electronics Engineers, Inc., i.e. the IEEE.

# The transport layer: TCP, UDP and SCTP

## Overview

The transport layer usually uses TCP and UDP; SCTP (Stream Control Transmission Protocol) is a relatively new protocol.

UDP is a simple, unreliable datagram protocol; TCP is a complex, reliable byte-stream protocol. On top of what TCP offers, SCTP adds message boundaries, transport-level multihoming support, and a way to minimize head-of-line blocking.

## The big picture

Here's the overall picture of the TCP/IP protocol suite:

![](http://img.zhangkexuan.cn/markdown_20210708192122.png)

## User Datagram Protocol (UDP)

### Problems with UDP

It lacks reliability: it doesn't guarantee that a datagram will reach its final destination, that datagrams stay in order after crossing the network, or that each datagram arrives only once. If a datagram's checksum detects an error, or it gets dropped, it isn't retransmitted automatically either.

## Transmission Control Protocol (TCP)

Unlike UDP, TCP provides reliable transmission and is connection-oriented.

### Differences between TCP and UDP

- TCP is connection-oriented, while UDP is connectionless.

- TCP provides reliability: it has acknowledgments, sequence numbers, RTT estimation, timeouts and retransmission, none of which UDP provides.

- TCP provides flow control. TCP always tells its peer exactly how many bytes of data it's willing to accept from the peer at any one time; this is called the advertised window. The window size changes dynamically to whatever is appropriate.

- TCP is full-duplex. An application can send and receive data in both directions on a given connection at any time.

  > UDP can actually be full-duplex too.

## Stream Control Transmission Protocol (SCTP)

SCTP is mostly the same as TCP. The difference is that it's message-oriented, and it also provides multihoming, which lets a single SCTP endpoint support multiple IP addresses.

## TCP connection establishment and termination

### The three-way handshake

![](http://img.zhangkexuan.cn/markdown_20210708200352.png)

### Common TCP options

- The MSS option, i.e. Maximum Segment Size: the maximum amount of data the endpoint is willing to accept in each TCP segment on this connection.
- The window scale option.
- The timestamp option.

### The four-way handshake (connection termination)

![](http://img.zhangkexuan.cn/markdown_20210708200846.png)

### The TCP state transition diagram

![](http://img.zhangkexuan.cn/markdown_20210708200954.png)

### The TIME_WAIT state



## Port numbers

Port numbers are 16 bits.

Clients usually use ephemeral ports, which the client doesn't need to care about.

- Well-known ports: 0~1023
- Registered ports: 1024~49151
- Dynamic ports: 49152~65535

![](http://img.zhangkexuan.cn/markdown_20210708201913.png)

## Socket pairs

A socket is the two values (IP address and port number) that identify an endpoint.

A socket pair defines the four-tuple of a connection (local IP address, local TCP port, foreign IP address, foreign TCP port).

## TCP port numbers and concurrent servers

Concurrent servers on Linux are implemented by calling fork to create child processes.

![](http://img.zhangkexuan.cn/markdown_20210708204317.png)

![](http://img.zhangkexuan.cn/markdown_20210708204331.png)

![](http://img.zhangkexuan.cn/markdown_20210708204346.png)

# Introduction to socket programming

## IPv4 socket address structure

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

