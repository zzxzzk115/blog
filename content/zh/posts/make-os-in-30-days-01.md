---
title: '《30 天自制操作系统》Day01'
date: 2020-04-05T17:39:00
categories: [系统编程]
tags: [OS, assembly, notes]
toc: true
original: true
cnblogs: 12638174
---

> 本文转载自我在博客园的旧博客：[《30 天自制操作系统》Day01](https://www.cnblogs.com/lazy-v/p/12638174.html)（写于 2020-04-05），迁移时整理了格式。

> 我宣布，从今天开始，本懒狗正式踏入自制操作系统的大坑之中，内容将使用较现代的新工具和新思路来编写，会不定期更新（谁让我懒呢...）
>
> 当然，这个系列不会涉及太多理论，主要以我自己的实践过程为主，看理论请看书。

<!--more-->

可以在 GitHub 跟进我的学习实践进度...（原仓库 Use30DaysToMakeOS 已不存在，可查看 [Wayback Machine 存档](https://web.archive.org/web/20201016085805/https://github.com/zzxzzk115/Use30DaysToMakeOS)）

# 1. 工具准备

作者使用的工具，并不是我熟悉的，也不一定是最好的解决方案。

对于 **16 进制编辑器**，你可以选用 [WinHex](http://www.x-ways.net/winhex/)，我将采用开源免费的 [wxMEdit](http://wxmedit.github.io/zh_CN/)：

![wxMEdit](/img/cnblogs/12638174-1.png)

**文本编辑器** 我首选 [Visual Studio Code](https://code.visualstudio.com/)，你可以选择自己喜欢的文本编辑器。

**虚拟机** 的话，你可以使用 [Virtual Box](https://www.virtualbox.org/) 或者 [VMware](https://www.vmware.com/products/desktop-hypervisor/workstation-and-fusion)。我将使用 VMware Workstation 14，因为它更加强大。

**汇编** 的话，还是老老实实采用作者的 nask.exe（原下载链接随仓库失效，可在书附带的工具包中找到）吧，我们并不需要自己写一个汇编器。

我们还需要一个 **Bash 环境**，你可以选择 [Git](https://git-scm.com/downloads) 的 Bash，我这里使用 [Cmder](https://cmder.app/)。

# 2. 以 16 进制方式编辑 image 映像文件

## 2.1. Bash 环境，dd 命令，生成全 0 的 image 文件

软盘规定大小必须为 `1440` **KB**，也就是 `1474560` 字节（1440 * 1024 **Bytes**，1 **KB** = 1024 **Bytes**）。

我们要制作的 img 文件中，由于只显示 `hello,world`，所以很多空间中的值都是 `0`。

如果不用命令生成，你就慢慢敲吧，复制粘贴都能累死你。

我们使用 Bash 环境的 `dd` 命令来快速生成全 0 的文件：

```bash
dd if=/dev/zero of=helloos.img count=1474560 bs=1
```

说明一下，**dd** 命令用于读取、转换并输出数据。

**dd** 可从标准输入或文件中读取数据，根据指定的格式来转换数据，再输出到文件、设备或标准输出。

`if=文件名`，指定源文件，这里指定 `/dev/zero`，它是一个可以输出无穷无尽的 0 的设备，具体提供多少，你自己定。

`of=文件名`，指定输出文件，这里输出文件 `helloos.img`。

`count=blocks`，代表拷贝 blocks 个块，这里拷贝 `1474560` 个块。

`bs=bytes`，代表同时设置读入、输出的块大小为 bytes 个字节，这里为 1 字节。

所以，整个操作的含义就是 **生成一个 `1474560` bytes 大小的，内容全为 `0` 的名为 `helloos.img` 的文件**。

我在 `Day01->codes` 文件夹中，右键以 **Cmder** 打开，并执行这个指令：

![dd](/img/cnblogs/12638174-2.png)

可以看到，生成了一个名为 `helloos.img`、大小为 1440 **KB** 的映像文件，成功。

## 2.2. 使用 16 进制编辑器，编辑 helloos.img

用 16 进制编辑器打开刚刚生成的 `helloos.img`，然后进入漫长的对着敲环节，体会一下当年打孔编程的快感（打孔那就更累了，那是 2 进制，这里好歹是 16 进制）。

![hex01](/img/cnblogs/12638174-3.png)

注意 000001F0 的行末和 00000200 的行首：

![hex02](/img/cnblogs/12638174-4.png)

还有 00001400 的行首：

![hex03](/img/cnblogs/12638174-5.png)

到这里，img 文件编辑完成。

# 3. 使用虚拟机，以软盘方式启动

打开 VMware：

![vm01](/img/cnblogs/12638174-6.png)

点击“创建新的虚拟机”，选择自定义，然后下一步：

![vm02](/img/cnblogs/12638174-7.png)

到这一步时，选择“稍后安装操作系统”：

![vm04](/img/cnblogs/12638174-8.png)

然后这一步全选“其他”：

![vm05](/img/cnblogs/12638174-9.png)

然后其他的配置 **按你自己需求** 来，**一直下一步** 就行。

最后完成后，点击“编辑虚拟机设置”，我们要给虚拟机 **添加软盘驱动器**：

![vm14](/img/cnblogs/12638174-10.png)

点击“添加”：

![vm15](/img/cnblogs/12638174-11.png)

选择“软盘驱动器”：

![vm16](/img/cnblogs/12638174-12.png)

最后勾选“使用软盘映像文件”，点击“浏览”，选择我们刚刚编辑好的 `helloos.img`，确认。

然后可以运行，如果提示 **无法连接 ide1:0**，直接点是就行了，暂时不考虑硬盘的问题。

最后会显示 `hello, world`：

![vm19](/img/cnblogs/12638174-13.png)

# 4. 使用 Visual Studio Code 进行汇编代码的编写

手撸 16 进制，我反正是累死了，你们呢？

好在有汇编。汇编引入了助记符，我们不用写纯机器代码了，汇编器可以把我们的汇编源文件编译成机器代码。

打开 VS Code，可以装一个 x86 assembly 的插件用于高亮，但有没有都无所谓。

键入以下内容：

```nasm
; hello-os
; TAB=4

; 标准FAT-32软盘专用代码

    DB      0xeb, 0x4e, 0x90
    DB      "HELLOIPL"      ; 启动区的名称
    DW      512             ; 每个扇区的大小(字节)，必须512字节
    DB      1               ; 簇的大小(扇区)，必须1个扇区
    DW      1               ; FAT的起始位置，一般第一个扇区
    DB      2               ; FAT的个数，必须为2
    DW      224             ; 根目录的大小(项)，一般224项
    DW      2880            ; 该磁盘的大小(扇区)，必须2880扇区
    DB      0xf0            ; 磁盘的种类，必须是0xf0
    DW      9               ; FAT的长度(扇区)，必须是9扇区
    DW      18              ; 1个磁道有多少个扇区，必须是18
    DW      2               ; 磁头数，必须是2
    DD      0               ; 不使用分区，必须是0
    DD      2880            ; 重写一次磁盘大小
    DB      0, 0, 0x29      ; 固定
    DD      0xffffffff      ; 可能是卷标号码
    DB      "HELLO-OS   "   ; 磁盘的名称(11字节)
    DB      "FAT12   "      ; 磁盘格式名称(8字节)
    RESB    18              ; 空出18字节

; 程序主体

    DB      0xb8, 0x00, 0x00, 0x8e, 0xd0, 0xbc, 0x00, 0x7c
    DB      0x8e, 0xd8, 0x8e, 0xc0, 0xbe, 0x74, 0x7c, 0x8a
    DB      0x04, 0x83, 0xc6, 0x01, 0x3c, 0x00, 0x74, 0x09
    DB      0xb4, 0x0e, 0xbb, 0x0f, 0x00, 0xcd, 0x10, 0xeb
    DB      0xee, 0xf4, 0xeb, 0xfd

; 信息显示

    DB      0x0a, 0x0a          ; 两个换行
    DB      "hello, world"
    DB      0x0a                ; 换行
    DB      0

    RESB    0x1fe-$             ; 填写0x00,直到0x001fe
    DB      0x55, 0xaa          ; 启动标识55aa

; 启动区外的输出

    DB      0xf0, 0xff, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00
    RESB    4600
    DB      0xf0, 0xff, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00
    RESB    1469432
```

再用控制台，再用 `nask.exe` 去生成 img 文件。

格式为：

```bash
nask.exe ***.nas ***.img
```

先用 `tree /f` 命令看看目前的文件目录树及其中所有文件：

```text
E:.
│  LICENSE
│  README-en.md
│  README.md
│
├─Day01
│  │  README.md
│  │
│  └─codes
│          helloos.img
│          helloos.nas
│          helloos1.img
│
└─tools
        nask.exe
        README.md
```

我们在 `Day01->codes` 文件夹中新建一个批处理文件 `make.bat`：

```batch
..\..\tools\nask.exe helloos.nas helloos1.img
```

`..` 代表当前 bat 文件的上层目录，所以 `..\..` 实际代表 `Use30DaysToMakeOS`，也就是我的根目录，`..\..\tools` 就是 `Use30DaysToMakeOS\tools`。

这样一来，在 `codes` 文件夹运行这个 `make.bat`，则会在当前文件夹（codes 文件夹）生成 `helloos1.img`：

![vsc_assembly](/img/cnblogs/12638174-14.png)

最后，修改 VMware 里的 img 文件为 `helloos1.img`，进行测试运行：

![helloos1](/img/cnblogs/12638174-15.png)

还是一样的效果。

毕竟用汇编只是简化了流程，最后的字节码都是一样的。
