---
title: 'Unity Online Game Development in Practice (2): Status Checking with Poll and Multiplexing with Select'
date: 2020-10-30T10:46:59
tags: [Unity, Network Programming]
categories: [Game Development]
toc: true
aiTranslated: true
---

This post shows you how to apply status checking with Poll and multiplexing with Select in Echo.

<!--more-->

> Besides async programs, what other ways are there to improve Echo's client and server?
>
> This blog series is based on the book *Unity3D Online Game Development in Practice*. If there are any mistakes, feel free to point them out in the comments.

# Status Checking with Poll

Can we use synchronous methods to optimize the client and server programs?

## What Is Poll

Microsoft provides a Poll instance method for the Socket class. Its prototype:

```csharp
public bool Poll (
    int  microSeconds,
    SelectMode mode
)
```

Parameter descriptions:

| Parameter    | Description                                                  |
| :----------- | ------------------------------------------------------------ |
| microSeconds | The time to wait for a response, in microseconds. If this parameter is -1, it waits indefinitely; if it's 0, it's non-blocking |
| mode         | There are 3 modes to choose from:<br />SelectRead: returns true if the Socket is readable (can receive data), otherwise false;<br />SelectWrite: returns true if the Socket is writable, otherwise false;<br />SelectError: returns true if the connection has failed, otherwise false |

The idea of Poll is to synchronously check the Socket's state (readable, writable, error) in a loop, and then run the corresponding logic.

## Poll Client

Make a few changes to Echo's synchronous client program EchoSync.cs: remove the Receive-related code in the Send method, and add a non-blocking Poll call in the Update method to check the Socket's readable state:

```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net.Sockets;
using UnityEngine.UI;

/// <summary>
/// Poll, client
/// </summary>
public class EchoPoll : MonoBehaviour
{
    /// <summary>
    /// Socket
    /// </summary>
    private Socket socket;

    /// <summary>
    /// Input field for sending messages
    /// </summary>
    public InputField input;

    /// <summary>
    /// Text box that displays content sent by the server
    /// </summary>
    public Text text;

    /// <summary>
    /// Connect to the server
    /// </summary>
    public void Connection()
    {
        //Define a Socket using IPv4, stream transport, and the TCP protocol
        socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);

        //Connect to the server; the server ip is the local machine ip, port 8888
        socket.Connect("127.0.0.1", 8888);
    }

    /// <summary>
    /// Send a message
    /// </summary>
    public void Send()
    {
        //----------------------
        //Send

        //Get the text string from the input field
        string sendStr = input.text;

        //Convert to a byte array
        byte[] sendBytes = System.Text.Encoding.UTF8.GetBytes(sendStr);

        //Send
        socket.Send(sendBytes);
		
        /*
        //----------------------
        //Receive

        //Receive buffer
        byte[] readBuffer = new byte[1024];

        //Receive and get the number of bytes
        int count = socket.Receive(readBuffer);

        //Build the string
        string receiveStr = System.Text.Encoding.UTF8.GetString(readBuffer, 0, count);

        //Display the string in UGUI
        text.text = receiveStr;

        //----------------------
        //Close

        //Close the socket
        socket.Close();
        */
    }
    
    private void Update() 
    {
        if(socket == null)
            return;
        //Non-blocking Poll to check the socket's readable state
        //If readable
        if(socket.Poll(0, SelectMode.SelectRead))
        {
            //Receive

        	//Receive buffer
        	byte[] readBuffer = new byte[1024];

        	//Receive and get the number of bytes
        	int count = socket.Receive(readBuffer);

        	//Build the string
        	string receiveStr = System.Text.Encoding.UTF8.GetString(readBuffer, 0, count);

        	//Display the string in UGUI
        	text.text = receiveStr;
        }
    }
}
```

## Poll Server

Make a few changes to Echo's asynchronous server program: remove the async methods and callback functions, use Poll in a loop to check the Socket's readable state, and then run the corresponding logic.

```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net;
using System.Net.Sockets;

/// <summary>
/// Poll, server
/// </summary>
namespace Echo_Server_Poll
{
    /// <summary>
    /// Client state
    /// </summary>
    class ClientState
    {
        //Socket
        public Socket socket;

        //Receive buffer
        public byte[] readBuffer = new byte[1024];
    }

    class Program
    {
        //Listening Socket
        static Socket listenfd;

        //Client Sockets and their states
        static Dictionary<Socket, ClientState> clients = new Dictionary<Socket, ClientState>();

        static void Main(string[] args)
        {
            Console.WriteLine("Hello, World!");
            //Console.ReadKey();

            //Create the Socket
            listenfd = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);

            //Create the IPAddress
            IPAddress ipAddr = IPAddress.Parse("127.0.0.1");

            //Create the IPEndPoint
            IPEndPoint ipEp = new IPEndPoint(ipAddr, 8888);

            //Bind
            listenfd.Bind(ipEp);

            //Listen; 0 means no limit on the number of pending connections
            listenfd.Listen(0);

            Console.WriteLine("[Server] started successfully");
			
            //Main loop
            while(true)
            {
                //Check clientfd
                if(listenfd.Poll(0, SelectMode.SelectRead))
                {
                    ReadListenfd(listenfd);
                }
                //Check clientfd
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
                //Prevent excessively high CPU usage
                System.Threading.Thread.Sleep(1);
            }
        }
        
        /// <summary>
        /// ReadListenfd method, does something similar to AcceptCallback
        /// </summary>
        /// <param name="listenfd"></param>
        public static void ReadListenfd(Socket listenfd)
        {
            Console.WriteLine("[Server] Accept");
            Socket clientfd = listenfd.Accept();

            //clients list
            ClientState state = new ClientState();
            state.socket = clientfd;
            clients.Add(clientfd, state);
        }
        
        /// <summary>
        /// ReadClientfd method, does something similar to ReceiveCallback
        /// </summary>
        /// <param name="listenfd"></param>
        public static void ReadClientfd(Socket clientfd)
        {
            ClientState state = clients[clientfd];
            //Receive
            int count = 0;
            try
            {
                count = clientfd.Receive(state.readBuffer);
            }
            catch(SocketException ex)
            {
                clientfd.Close();
                clients.Remove(clientfd);
                Console.WriteLine("Socket receive failed " + ex.ToString());
                return false;
            }
            //Client closed
            if(count == 0)
            {
                clientfd.Close();
                clients.Remove(clientfd);
                Console.WriteLine("Socket closed");
                return false;
            }
			//Broadcast
            string recvStr = System.Text.Encoding.UTF8.GetString(state.readBuffer, 0, count);
            Console.WriteLine("[Server received]" + recvStr);
                
            byte[] sendBytes = System.Text.Encoding.UTF8.GetBytes("Echo " + recvStr);
     
            Console.WriteLine("[Server sent]" + "Echo " + recvStr);
            
			foreach(ClientState cs in clients.Values)
            {
                cs.socket.Send(sendBytes);
            }
            return true;
        }
    }
}
```

Poll's logic is very clear, but since it's constantly looping and checking, it still consumes CPU resources. Is there any way to further optimize performance?

# Multiplexing with Select

Is there a way to check a Socket's readable, writable, and error states all at once?

## What Is Multiplexing

Multiplexing means handling multiple signals at the same time, for example checking the states of multiple Sockets simultaneously.

For this, Microsoft provides the Socket class's static Select method. Its prototype:

```csharp
public static void Select(
	IList checkRead,
    IList checkWrite,
    IList checkError,
    int microSeconds
)
```

Parameter descriptions:

| Parameter    | Description                                                  |
| ------------ | :----------------------------------------------------------- |
| checkRead    | The list of Sockets to check for readability                |
| checkWrite   | The list of Sockets to check for writability                |
| checkError   | The list of Sockets to check for errors                     |
| microSeconds | The time to wait for a response, in microseconds. If this parameter is -1 it waits indefinitely; if it's 0 it's non-blocking |

Select can determine the state of one or more Sockets. After it's called, it modifies the IList lists you passed in, keeping only the sockets that meet the conditions. When no Socket meets the requirements, Select blocks the program without consuming CPU.

## Select Server

Make a few changes to the while loop in the Poll version of the Echo server, leaving everything else unchanged:

```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net;
using System.Net.Sockets;

/// <summary>
/// Select, server
/// </summary>
namespace Echo_Server_Select
{
    /// <summary>
    /// Client state
    /// </summary>
    class ClientState
    {
        //Socket
        public Socket socket;

        //Receive buffer
        public byte[] readBuffer = new byte[1024];
    }

    class Program
    {
        //Listening Socket
        static Socket listenfd;

        //Client Sockets and their states
        static Dictionary<Socket, ClientState> clients = new Dictionary<Socket, ClientState>();

        static void Main(string[] args)
        {
            Console.WriteLine("Hello, World!");
            //Console.ReadKey();

            //Create the Socket
            listenfd = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);

            //Create the IPAddress
            IPAddress ipAddr = IPAddress.Parse("127.0.0.1");

            //Create the IPEndPoint
            IPEndPoint ipEp = new IPEndPoint(ipAddr, 8888);

            //Bind
            listenfd.Bind(ipEp);

            //Listen; 0 means no limit on the number of pending connections
            listenfd.Listen(0);

            Console.WriteLine("[Server] started successfully");
			
            //Initialize checkRead
            List<Socket> checkRead = new List<Socket>();
            
            //Main loop
            while(true)
            {
                //Fill the checkRead list
                checkRead.Clear();
                checkRead.Add(listenfd);
                foreach(ClientState s in clients.Values)
                {
                    checkRead.Add(s.socket);
                }
                //select, with a 1-millisecond timeout; if no socket qualifies, it blocks without consuming CPU
                Socket.Select(checkRead, null, null, 1000);
                //Check the readable objects
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
        /// ReadListenfd method, does something similar to AcceptCallback
        /// </summary>
        /// <param name="listenfd"></param>
        public static void ReadListenfd(Socket listenfd)
        {
            Console.WriteLine("[Server] Accept");
            Socket clientfd = listenfd.Accept();

            //clients list
            ClientState state = new ClientState();
            state.socket = clientfd;
            clients.Add(clientfd, state);
        }
        
        /// <summary>
        /// ReadClientfd method, does something similar to ReceiveCallback
        /// </summary>
        /// <param name="listenfd"></param>
        public static bool ReadClientfd(Socket clientfd)
        {
            ClientState state = clients[clientfd];
            //Receive
            int count = 0;
            try
            {
                count = clientfd.Receive(state.readBuffer);
            }
            catch(SocketException ex)
            {
                clientfd.Close();
                clients.Remove(clientfd);
                Console.WriteLine("Socket receive failed " + ex.ToString());
                return false;
            }
            //Client closed
            if(count == 0)
            {
                clientfd.Close();
                clients.Remove(clientfd);
                Console.WriteLine("Socket closed");
                return false;
            }
			//Broadcast
            string recvStr = System.Text.Encoding.UTF8.GetString(state.readBuffer, 0, count);
            Console.WriteLine("[Server received]" + recvStr);
                
            byte[] sendBytes = System.Text.Encoding.UTF8.GetBytes("Echo " + recvStr);
     
            Console.WriteLine("[Server sent]" + "Echo " + recvStr);
            
			foreach(ClientState cs in clients.Values)
            {
                cs.socket.Send(sendBytes);
            }
            return true;
        }
    }
}
```

## Select Client

Make a few changes to the client implemented with Poll: add a checkRead list object and modify the Update logic:

```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net.Sockets;
using UnityEngine.UI;

/// <summary>
/// Select, client
/// </summary>
public class EchoSelect : MonoBehaviour
{
    /// <summary>
    /// Socket
    /// </summary>
    private Socket socket;

    /// <summary>
    /// Input field for sending messages
    /// </summary>
    public InputField input;

    /// <summary>
    /// Text box that displays content sent by the server
    /// </summary>
    public Text text;
    
    /// <summary>
    /// checkRead list
    /// </summary>
    public List<Socket> checkRead = new List<Socket>();

    /// <summary>
    /// Connect to the server
    /// </summary>
    public void Connection()
    {
        //Define a Socket using IPv4, stream transport, and the TCP protocol
        socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);

        //Connect to the server; the server ip is the local machine ip, port 8888
        socket.Connect("127.0.0.1", 8888);
    }

    /// <summary>
    /// Send a message
    /// </summary>
    public void Send()
    {
        //----------------------
        //Send

        //Get the text string from the input field
        string sendStr = input.text;

        //Convert to a byte array
        byte[] sendBytes = System.Text.Encoding.UTF8.GetBytes(sendStr);

        //Send
        socket.Send(sendBytes);
    }
    
    private void Update() 
    {
        if(socket == null)
            return;
        
        //Fill the checkRead list
        checkRead.Clear();
        checkRead.Add(socket);
        
        //select
        Socket.Select(checkRead, null, null, 0);
        
        //check
        foreach(Socket s in checkRead)
        {
            //Receive
        	//Receive buffer
        	byte[] readBuffer = new byte[1024];
            
        	//Receive and get the number of bytes
        	int count = socket.Receive(readBuffer);
            
        	//Build the string
        	string receiveStr = System.Text.Encoding.UTF8.GetString(readBuffer, 0, count);
        	//Display the string in UGUI
        	text.text = receiveStr;
        }
    }
}
```

The Select client's performance is still fairly poor, because Update keeps checking non-stop. So in commercial settings an asynchronous client is generally used.

# Summary

Both Poll and Select are simpler to write than async, and Select outperforms Poll.

For the server, Select is a decent approach; for the client, it's still best to use the asynchronous approach.
