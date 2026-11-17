---
title: 'Unity网游实战(2)：状态检测Poll和多路复用Select'
date: 2020-10-30T10:46:59
tags: [tutorial, network, Unity]
categories: [Tech]
toc: true
---

本篇文章教你在Echo中应用状态监测Poll和多路复用Select。

<!--more-->

> 除了异步程序，还有什么方法可以改善Echo的客户端和服务端呢？
>
> 本系列博文参考自《Unity3D网络游戏实战》一书。如有错误，欢迎评论区指正。

# 状态检测Poll

可以用同步方法来优化客户端和服务端程序吗？

## 什么是Poll

Microsoft为Socket类提供了Poll实例方法，它的原型：

```csharp
public bool Poll (
    int  microSeconds,
    SelectMode mode
)
```

参数说明：

| 参数         | 说明                                                         |
| :----------- | ------------------------------------------------------------ |
| microSeconds | 等待回应的时间，以微秒为单位，如果该参数为-1，表示一直等待，如果为0，表示非阻塞 |
| mode         | 有3种可选的模式，如下：<br />SelectRead：如果Socket可读（可以接受数据），返回true，否则返回false；<br />SelectWrite：如果Socket可写，返回true，否则返回false；<br />SelectError：如果连接失败，返回true，否则返回false |

Poll的思想就是，循环中同步检测Socket的状态（可读、可写、错误），进而进行相应的逻辑。

## Poll客户端

将Echo的同步客户端程序EchoSync.cs稍作更改，将Send方法中Receive相关代码删除，在Update方法中加入非阻塞的Poll方法检测Socket的可读状态:

```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net.Sockets;
using UnityEngine.UI;

/// <summary>
/// Poll，客户端
/// </summary>
public class EchoPoll : MonoBehaviour
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
		
        /*
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
        */
    }
    
    private void Update() 
    {
        if(socket == null)
            return;
        //非阻塞Poll检测socket的可读状态
        //如果可读
        if(socket.Poll(0, SelectMode.SelectRead))
        {
            //接收

        	//接收缓冲
        	byte[] readBuffer = new byte[1024];

        	//接收并获得字节大小
        	int count = socket.Receive(readBuffer);

        	//生成字符串
        	string receiveStr = System.Text.Encoding.UTF8.GetString(readBuffer, 0, count);

        	//显示字符串到UGUI
        	text.text = receiveStr;
        }
    }
}
```

## Poll服务端

将Echo的异步服务端程序稍作修改，将异步方法和回调函数删除，循环中使用Poll检测Socket的可读状态，进而完成相应逻辑。

```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net;
using System.Net.Sockets;

/// <summary>
/// Poll，服务器
/// </summary>
namespace Echo_Server_Poll
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
			
            //主循环
            while(true)
            {
                //检查clientfd
                if(listenfd.Poll(0, SelectMode.SelectRead))
                {
                    ReadListenfd(listenfd);
                }
                //检查clientfd
                foreach(ClientState s in clients.Values)
                {
                    Socket clientfd = s.socket;
                    if(clientfd.Poll(0, SelectMode.SelectRead))
                    {
                        if(!ReadClientfd(clientfd))
                        {
                            break;
                        }
                    }
                }
                //防止CPU占用过高
                System.Threading.Thread.Sleep(1);
            }
        }
        
        /// <summary>
        /// ReadListenfd方法，与AcceptCallback做的事情类似
        /// </summary>
        /// <param name="listenfd"></param>
        public static void ReadListenfd(Socket listenfd)
        {
            Console.WriteLine("[服务器]Accept");
            Socket clientfd = listenfd.Accept();

            //clients列表
            ClientState state = new ClientState();
            state.socket = clientfd;
            clients.Add(clientfd, state);
        }
        
        /// <summary>
        /// ReadClientfd方法，与ReceiveCallback做的事情类似
        /// </summary>
        /// <param name="listenfd"></param>
        public static void ReadClientfd(Socket clientfd)
        {
            ClientState state = clients[clientfd];
            //接收
            int count = 0;
            try
            {
                count = clientfd.Receive(state.readBuffer);
            }
            catch(SocketException ex)
            {
                clientfd.Close();
                clients.Remove(clientfd);
                Console.WriteLine("Socket接收失败 " + ex.ToString());
                return false;
            }
            //客户端关闭
            if(count == 0)
            {
                clientfd.Close();
                clients.Remove(clientfd);
                Console.WriteLine("Socket关闭");
                return false;
            }
			//广播
            string recvStr = System.Text.Encoding.UTF8.GetString(state.readBuffer, 0, count);
            Console.WriteLine("[服务器接收]" + recvStr);
                
            byte[] sendBytes = System.Text.Encoding.UTF8.GetBytes("Echo " + recvStr);
     
            Console.WriteLine("[服务器发送]" + "Echo " + recvStr);
            
			foreach(ClientState cs in clients.Values)
            {
                cs.socket.Send(sendBytes);
            }
            return true;
        }
    }
}
```

Poll的逻辑很清晰，但是一直处于循环检测的状态，依旧耗费CPU资源，还有什么可以更加优化性能的方法呢？

# 多路复用Select

有没有可以同时对Socket的可读、可写、错误状态进行检测的方法呢？

## 什么是多路复用

多路复用，就是同时处理多路信号，比如同时检测多个Socket的状态。

微软为此提供了Socket类的Select静态方法，它的原型：

```csharp
public static void Select(
	IList checkRead,
    IList checkWrite,
    IList checkError,
    int microSeconds
)
```

参数说明：

| 参数         | 说明                                                         |
| ------------ | :----------------------------------------------------------- |
| checkRead    | 检测是否有可读的Socket列表                                   |
| checkWrite   | 检测是否有可写的Socket列表                                   |
| checkError   | 检测是否有出错的Socket列表                                   |
| microSeconds | 等待回应的时间，以微秒为单位，如果该参数为-1表示一直等待，为0表示非阻塞 |

Select可以确定一个或多个Socket的状态，调用后，会修改传入的IList列表，仅保留满足条件的套接字。当没有任何满足要求的Socket时，Select将程序阻塞，不占用CPU。

## Select服务端

对Poll方法的Echo服务端中的while循环稍作修改，其他不变：

```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net;
using System.Net.Sockets;

/// <summary>
/// Select，服务器
/// </summary>
namespace Echo_Server_Select
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
			
            //checkRead初始化
            List<Socket> checkRead = new List<Socket>();
            
            //主循环
            while(true)
            {
                //填充checkRead列表
                checkRead.Clear();
                checkRead.Add(listenfd);
                foreach(ClientState s in clients.Values)
                {
                    checkRead.Add(s.socket);
                }
                //select，超时时间1毫秒，如果没有满足的socket，会阻塞，不会占用CPU
                Socket.Select(checkRead, null, null, 1000);
                //检查可读对象
                foreach(Socket s in checkRead)
                {
                    if(s == listenfd)
                    {
                        ReadListenfd(s);
                    }
                    else
                    {
                        ReadClientfd(s);
                    }
                }
            }
        }
        
        /// <summary>
        /// ReadListenfd方法，与AcceptCallback做的事情类似
        /// </summary>
        /// <param name="listenfd"></param>
        public static void ReadListenfd(Socket listenfd)
        {
            Console.WriteLine("[服务器]Accept");
            Socket clientfd = listenfd.Accept();

            //clients列表
            ClientState state = new ClientState();
            state.socket = clientfd;
            clients.Add(clientfd, state);
        }
        
        /// <summary>
        /// ReadClientfd方法，与ReceiveCallback做的事情类似
        /// </summary>
        /// <param name="listenfd"></param>
        public static bool ReadClientfd(Socket clientfd)
        {
            ClientState state = clients[clientfd];
            //接收
            int count = 0;
            try
            {
                count = clientfd.Receive(state.readBuffer);
            }
            catch(SocketException ex)
            {
                clientfd.Close();
                clients.Remove(clientfd);
                Console.WriteLine("Socket接收失败 " + ex.ToString());
                return false;
            }
            //客户端关闭
            if(count == 0)
            {
                clientfd.Close();
                clients.Remove(clientfd);
                Console.WriteLine("Socket关闭");
                return false;
            }
			//广播
            string recvStr = System.Text.Encoding.UTF8.GetString(state.readBuffer, 0, count);
            Console.WriteLine("[服务器接收]" + recvStr);
                
            byte[] sendBytes = System.Text.Encoding.UTF8.GetBytes("Echo " + recvStr);
     
            Console.WriteLine("[服务器发送]" + "Echo " + recvStr);
            
			foreach(ClientState cs in clients.Values)
            {
                cs.socket.Send(sendBytes);
            }
            return true;
        }
    }
}
```

## Select客户端

对Poll方法实现的客户端稍作修改，加入checkRead列表对象，修改Update逻辑：

```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net.Sockets;
using UnityEngine.UI;

/// <summary>
/// Select，客户端
/// </summary>
public class EchoSelect : MonoBehaviour
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
    /// checkRead列表
    /// </summary>
    public List<Socket> checkRead = new List<Socket>();

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
    }
    
    private void Update() 
    {
        if(socket == null)
            return;
        
        //填充checkRead列表
        checkRead.Clear();
        checkRead.Add(socket);
        
        //select
        Socket.Select(checkRead, null, null, 0);
        
        //check
        foreach(Socket s in checkRead)
        {
            //接收
        	//接收缓冲
        	byte[] readBuffer = new byte[1024];
            
        	//接收并获得字节大小
        	int count = socket.Receive(readBuffer);
            
        	//生成字符串
        	string receiveStr = System.Text.Encoding.UTF8.GetString(readBuffer, 0, count);
        	//显示字符串到UGUI
        	text.text = receiveStr;
        }
    }
}
```

Select客户端的性能还是较差，因为Update不停检测。所以商业上一般采用异步客户端。

# 总结

Poll和Select写起来都比异步要简单，Select的性能优于Poll。

对于服务端而言，Select是一种不错的实现方式；对于客户端而言，最好还是使用异步方式。

