---
title: 'Unity 网游实战(1)：最简单的网络程序 Echo'
date: 2020-10-23T12:36:00
tags: [tutorial, network, Unity]
categories: [游戏开发]
toc: true
---

网游是怎么进行通信的？本文教你用最简单的 TCP/IP Socket 实现最简单的网络通信。

<!--more-->

> 初学者可能接触了 Unity 游戏引擎以后，会萌生做联机游戏的想法，我一开始也一样。我尝试过一些联机服务框架，比如 PUN2，最终游戏的确能玩，但这无法满足我的求知欲，我还是想自己实现服务器和客户端通信。相信读者也不希望只会用框架而不知道原理。
>
> 本系列博文参考自《Unity3D 网络游戏实战》一书。如有错误，欢迎评论区指正。

# 客户端、服务端、TCP

你手机运行的 App，电脑上玩的游戏，都算客户端程序。运行在运营商服务器上的程序，是服务端程序。

游戏中，客户端与服务端一般使用 TCP(Transfer Control Protocol，传输控制协议) 进行通信。TCP 是面向连接的、可靠的、基于字节流的传输层通信协议。简单理解为：需要建立连接，传输丢包率低，传输的数据是字节流。

客户端之间的消息通信利用服务端的消息转发来实现。

假设 Client A 和 Client B 都与 Server A 进行了 TCP 连接。

如果 Client A 位置变更，那么 Client B 怎么知道呢？由于 Client A 和 Client B 都与 Server A 进行了连接，Server A 可以把 Client A 位置变更的消息发送给 Client B，这样就完成了位置信息同步。

如果数以万计的客户端同时连接同一个服务端，不难想象，这个服务端可能会崩溃。所以，现在的网游多数都进行分区处理。分区实际上就是服务端采取分布式架构。这样，原本一个服务端要处理十万个客户端，现在 N 个服务端处理十万个客户端，崩溃的可能性小多了。

心细的读者会考虑到，那如果十万个客户端都选同一个区呢？哈哈哈，玩过 LOL 的朋友就最清楚了，以前每次有活动，艾欧尼亚都会“排队”！蜂拥而至的情况，服务端会处理的，排队就是处理方式之一。



# Socket

Socket，套接字，是网络连接的端点。网络上的两个程序进行双向通信时，通信的一端是 Socket。对于 Client A 和 Server A 而言，Client A 包含一个 Socket 实例，Server A 包含一个 Socket 实例。Socket 包含了网络通信的五种信息：

> Socket 包含的五种信息：
>
> 1. 协议：TCP
> 2. 本地 IP: 192.168.1.103
> 3. 本地端口: 65308
> 4. 远程 IP：192.168.1.105
> 5. 远程端口：8888

Socket 通信流程为：

> Socket 通信流程：
>
> 1. 服务端建立 Socket 对象，Bind（绑定）一个 IPEndPoint（就是 IP 和端口号所生成的对象）
> 2. 服务端开启 Listen（监听）
> 3. 客户端 Connect（连接）到服务端（三次握手）
> 4. 服务端 Accept（接受）连接
> 5. 客户端和服务端通过 Send（发送）和 Receive（接收）进行数据通信
> 6. 某一方 Close（关闭）连接（四次挥手）



# 开始网络编程：Echo

> 我会分为同步篇和异步篇来说明。
>
> 客户端采用 Unity3D 制作，服务端采用 C#.NET 制作控制台应用程序。
>
> Echo 的效果就是，客户端给服务端发送 InputField 输入框内的文本消息，服务端控制台打印日志，把接收到的消息发送回客户端，客户端的 Text 控件显示从服务端接收到的消息文本。

## 同步和异步的概念

同步是指：发送方发出数据后，等接收方发回响应以后才发下一个数据包的通讯方式。 

异步是指：发送方发出数据后，不等接收方发回响应，接着发送下个数据包的通讯方式。

同步往往不被采纳，因为会造成线程阻塞，影响程序性能。但是同步程序要好写很多，所以我先从最简单的同步程序讲起。

## 同步篇

场景搭建：

![EchoSyncScene](/img/markdown_20201029174457.png)

> 说明：Unity 场景中空物体 EchoSync 绑定客户端脚本 EchoSync.cs，有一个 ConnectButton 按钮，绑定客户端脚本的 Connection 方法，有一个 Send 按钮，绑定客户端脚本的 Send 方法，有一个 InputField 对应输入框，有一个 Text 对应服务端发回来的信息显示，InputField 和 Text 通过 public 绑定。这里设计好服务端 IP 为 localhost(127.0.0.1)，端口号 8888。

客户端代码：

```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net.Sockets;
using UnityEngine.UI;

/// <summary>
/// 同步，客户端
/// </summary>
public class EchoSync : MonoBehaviour
{
    /// <summary>
    /// 套接字
    /// </summary>
    private Socket socket;

    /// <summary>
    /// 发送信息的输入框
    /// </summary>
    public InputField input;

    /// <summary>
    /// 显示服务端发送内容的文本框
    /// </summary>
    public Text text;

    /// <summary>
    /// 连接服务器
    /// </summary>
    public void Connection()
    {
        //定义使用IPv4,流式传输,TCP协议的一个Socket
        socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);

        //连接服务器,服务器ip为本机ip,端口号8888
        socket.Connect("127.0.0.1", 8888);
    }

    /// <summary>
    /// 发送消息
    /// </summary>
    public void Send()
    {
        //----------------------
        //发送

        //获取输入框文本字符串
        string sendStr = input.text;

        //转换为字节数组
        byte[] sendBytes = System.Text.Encoding.UTF8.GetBytes(sendStr);

        //发送
        socket.Send(sendBytes);

        //----------------------
        //接收

        //接收缓冲
        byte[] readBuffer = new byte[1024];

        //接收并获得字节大小
        int count = socket.Receive(readBuffer);

        //生成字符串
        string receiveStr = System.Text.Encoding.UTF8.GetString(readBuffer, 0, count);

        //显示字符串到UGUI
        text.text = receiveStr;

        //----------------------
        //关闭

        //关闭socket
        socket.Close();
    }
}
```

服务端代码：

```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net;
using System.Net.Sockets;

/// <summary>
/// 同步，服务器，缺点：阻塞，CPU占用高。
/// </summary>
namespace Echo_Server_Sync
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Hello, World!");
            //Console.ReadKey();

            //创建Socket
            Socket listenfd = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);

            //创建IPAddress
            IPAddress ipAddr = IPAddress.Parse("127.0.0.1");

            //创建IPEndPoint
            IPEndPoint ipEp = new IPEndPoint(ipAddr, 8888);

            //绑定(Bind)
            listenfd.Bind(ipEp);

            //监听,0代表等待连接数不受限制
            listenfd.Listen(0);

            Console.WriteLine("[服务器]启动成功");

            while (true)
            {
                //Accept
                Socket connfd = listenfd.Accept();
                Console.WriteLine("[服务器]Accept");

                //Receive
                byte[] readBuffer = new byte[1024];
                int count = connfd.Receive(readBuffer);
                string receiveStr = System.Text.Encoding.UTF8.GetString(readBuffer, 0, count);
                Console.WriteLine("[服务器接收]" + receiveStr);

                //Send
                byte[] sendBytes = System.Text.Encoding.UTF8.GetBytes(receiveStr);
                connfd.Send(sendBytes);
            }

        }
    }
}
```

这样的客户端和服务器程序，写起来简单，用起来可能会造成卡顿，因为 Connect、Accept、Receive、Send 都是阻塞方法。不仅如此，目前的同步程序，只能是 1 对 1 的关系，服务端不能处理多个客户端的连接。



## 异步篇

异步程序中，对应的 API 发生了变换。Connect 变为 BeginConnect，Accept 变为 BeginAccept，Receive 变为 BeginReceive，Send 变为 BeginSend。改变后的方法均需要传入 void Callback(IAsyncResult ar) 类型的委托作为回调，均返回一个 IAsyncResult 接口类型的对象。相应需要结束，就有 EndConnect、EndAccept、EndReceive、EndSend 等方法，需要传入一个 IAsyncResult 类型的对象作为参数。

客户端代码：

```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net.Sockets;
using UnityEngine.UI;
using System;

/// <summary>
/// 异步，客户端
/// </summary>
public class EchoAsync : MonoBehaviour
{
    /// <summary>
    /// 套接字
    /// </summary>
    private Socket socket;

    /// <summary>
    /// 发送信息的输入框
    /// </summary>
    public InputField input;

    /// <summary>
    /// 显示服务端发送内容的文本框
    /// </summary>
    public Text text;

    /// <summary>
    /// 接收缓冲区
    /// </summary>
    private byte[] readBuffer = new byte[1024];

    /// <summary>
    /// 接收文本
    /// </summary>
    private string recvStr = "";

    /// <summary>
    /// 连接服务器
    /// </summary>
    public void Connection()
    {
        //定义使用IPv4,流式传输,TCP协议的一个Socket
        socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);

        //开始异步连接服务器,服务器ip为本机ip,端口号8888,回调函数为ConnectCallback,回调参数socket
        socket.BeginConnect("127.0.0.1", 8888, ConnectCallback, socket);
    }

    /// <summary>
    /// 异步连接的回调
    /// </summary>
    /// <param name="ar"></param>
    public void ConnectCallback(IAsyncResult ar)
    {
        try
        {
            //通过ar的异步状态获取到socket对象
            Socket socket = (Socket)ar.AsyncState;

            //结束异步连接
            socket.EndConnect(ar);

            Debug.Log("Socket连接成功");

            //开始异步接收
            socket.BeginReceive(readBuffer, 0, 1024, 0, ReceiveCallback, socket);
        }
        catch(SocketException ex)
        {
            Debug.LogError("Socket连接失败: " + ex.ToString());
        }
    }

    /// <summary>
    /// 异步接收的回调
    /// </summary>
    /// <param name="ar"></param>
    public void ReceiveCallback(IAsyncResult ar)
    {
        try
        {
            Socket socket = (Socket)ar.AsyncState;

            //结束异步接收，返回接收信息的字节个数
            int count = socket.EndReceive(ar);

            recvStr = System.Text.Encoding.UTF8.GetString(readBuffer, 0, count);

            //继续开始异步接收，形成循环
            socket.BeginReceive(readBuffer, 0, 1024, 0, ReceiveCallback, socket);
        }
        catch(SocketException ex)
        {
            Debug.LogError("Socket接收失败: " + ex.ToString());
        }
    }

    /// <summary>
    /// 异步发送消息
    /// </summary>
    public void Send()
    {
        //----------------------
        //发送

        //获取输入框文本字符串
        string sendStr = input.text;

        //转换为字节数组
        byte[] sendBytes = System.Text.Encoding.UTF8.GetBytes(sendStr);

        //发送
        socket.BeginSend(sendBytes, 0, sendBytes.Length, 0, SendCallback, socket);
    }

    /// <summary>
    /// 异步发送消息的回调
    /// </summary>
    /// <param name="ar"></param>
    public void SendCallback(IAsyncResult ar)
    {
        try
        {
            Socket socket = (Socket)ar.AsyncState;
            int count = socket.EndSend(ar);
            Debug.Log("Socket发送成功，发送字节数:" + count);
        }
        catch(SocketException ex)
        {
            Debug.LogError("Socket发送失败" + ex.ToString());
        }
    }

    private void Update()
    {
        text.text = recvStr;
    }
}
```

> 需要注意的是：
>
> 1. 采用异步以后，不能在回调里直接对 Unity 的控件（例如 Text）进行更新，因为异步程序新开了线程，非主线程无法对 Unity 控件进行任何操作，所以只能改变一个字符串的值，在 Update 方法中循环赋值为那个字符串。
> 2. 回调里继续调用 BeginXXX 方法，BeginXXX 方法里再传入这个回调，可以形成一个循环。
> 3. 异步程序可能会抛出 SocketException 异常，所以需要使用 try/catch 结构进行异常捕获。

服务端代码：

```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net;
using System.Net.Sockets;

/// <summary>
/// 异步，服务器
/// </summary>
namespace Echo_Server_Async
{
    /// <summary>
    /// 客户端状态
    /// </summary>
    class ClientState
    {
        //套接字
        public Socket socket;

        //接收缓冲区
        public byte[] readBuffer = new byte[1024];
    }

    class Program
    {
        //监听Socket
        static Socket listenfd;

        //客户端Socket及状态
        static Dictionary<Socket, ClientState> clients = new Dictionary<Socket, ClientState>();

        static void Main(string[] args)
        {
            Console.WriteLine("Hello, World!");
            //Console.ReadKey();

            //创建Socket
            listenfd = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);

            //创建IPAddress
            IPAddress ipAddr = IPAddress.Parse("127.0.0.1");

            //创建IPEndPoint
            IPEndPoint ipEp = new IPEndPoint(ipAddr, 8888);

            //绑定(Bind)
            listenfd.Bind(ipEp);

            //监听,0代表等待连接数不受限制
            listenfd.Listen(0);

            Console.WriteLine("[服务器]启动成功");

            //开始异步Accept
            listenfd.BeginAccept(AcceptCallback, listenfd);

            Console.ReadLine();
        }

        /// <summary>
        /// 异步Accept的回调
        /// </summary>
        /// <param name="ar"></param>
        public static void AcceptCallback(IAsyncResult ar)
        {
            try
            {
                Console.WriteLine("[服务器]Accept");
                Socket listenfd = (Socket)ar.AsyncState;
                Socket clientfd = listenfd.EndAccept(ar);

                //clients列表
                ClientState state = new ClientState();
                state.socket = clientfd;
                clients.Add(clientfd, state);

                //开始异步接收数据
                clientfd.BeginReceive(state.readBuffer, 0, 1024, 0, ReceiveCallback, state);

                //继续异步Accept
                listenfd.BeginAccept(AcceptCallback, listenfd);
            }
            catch(SocketException ex)
            {
                Console.WriteLine("Socket Accept失败" + ex.ToString());
            }
        }

        /// <summary>
        /// 异步接收的回调
        /// </summary>
        /// <param name="ar"></param>
        public static void ReceiveCallback(IAsyncResult ar)
        {
            try
            {
                ClientState state = (ClientState)ar.AsyncState;
                Socket clientfd = state.socket;
                int count = clientfd.EndReceive(ar);

                //客户端关闭
                if(count == 0)
                {
                    clientfd.Close();
                    clients.Remove(clientfd);
                    Console.WriteLine("Socket关闭");
                    return;
                }

                string recvStr = System.Text.Encoding.UTF8.GetString(state.readBuffer, 0, count);
                Console.WriteLine("[服务器接收]" + recvStr);
                
                byte[] sendBytes = System.Text.Encoding.UTF8.GetBytes("Echo " + recvStr);
                clientfd.Send(sendBytes);
                Console.WriteLine("[服务器发送]" + "Echo " + recvStr);

                //继续开始异步接收
                clientfd.BeginReceive(state.readBuffer, 0, 1024, 0, ReceiveCallback, state);
            }
            catch(SocketException ex)
            {
                Console.WriteLine("Socket接收失败" + ex.ToString());
            }
        }
    }
}
```

> 需要注意的是：
>
> 1. 服务端使用了 Dictionary<Socket, ClientState>存储了客户端字典集合。
> 2. ClientState 存储了 Socket 对应连接的 Socket 对象和缓冲区。
> 3. EndReceive 返回客户端传送的字节数，字节数为 0 代表该客户端断开了连接。
> 4. 为了减少代码量，服务端的 Send 没有采用异步，但读者可以用异步实现，效果会更好。

这样的程序，效率高，CPU 占用相对较低，不会阻塞，一个服务端可以处理多个客户端的连接。

关于程序中的 API，详见 [微软官方 C# API 文档](https://docs.microsoft.com/zh-cn/dotnet/csharp/)。

## 运行效果

以异步为例:

![EchoAsyncShowcase](/img/markdown_20201031112712.png)

## 总结

同步方法好写但阻塞，可能影响程序的效率。

异步方法效率高性能好，但是写起来相对复杂。

对于游戏而言，性能很关键，所以我们一般不会使用同步方法。