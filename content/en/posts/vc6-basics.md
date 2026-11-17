---
title: '[Tutorial] Basic Usage of VC++6.0'
date: 2017-12-04T11:18:36
categories: [Programming Languages]
tags: [C, tutorial]
toc: true
original: true
csdn: 78707323
aiTranslated: true
---

> Reposted from my old CSDN blog: [[教程]VC++6.0 的简单使用](https://blog.csdn.net/zkx981105/article/details/78707323) (written 2017-12-04); formatting tidied during migration.

Since a lot of classmates can't get vc++6.0 to work properly, don't know how to create projects and files, and some run into compile problems, I'm putting together a little tutorial here

<!--more-->

## 1.Getting the Tools Ready

- First, here are the resources you need. There are just two files: one installer, and one MSDEV.exe used as a replacement. Link: https://pan.baidu.com/s/1nvqrePV  Password: wsvd

- Next, open vc6_cn_full.exe and install vc++6.0. After vc is installed, don't open it; opening it will only throw errors (it breaks on win8 and win10). Find the shortcut on the desktop, right-click it, click "Open file location", then drag the downloaded MSDEV.exe in. The computer will ask whether you want to replace the file; just click Yes.

- Right-click the desktop shortcut, click "Compatibility", check "Run this program as an administrator" at the bottom and apply. This avoids some errors later on.

- Finally, double-click the desktop shortcut and it should run normally.

## 2.Creating a Project and a File

- First, click File->New.

![Main window](/img/csdn/78707323-1.png)

![New](/img/csdn/78707323-2.png)

- Since early on we only need console applications, choose Win32 Console Application (a win32 console application, the "little black box")

![win32](/img/csdn/78707323-3.png)

- Choosing an empty project is better for learning things yourself

![Empty project](/img/csdn/78707323-4.png)

- Then create a new C++  Source File

![C++ Source File](/img/csdn/78707323-5.png)

- Type in your code

![Type in code](/img/csdn/78707323-6.png)

- Click the red exclamation mark or press the shortcut key to compile, link, and run in one go

![Red exclamation mark](/img/csdn/78707323-7.png)

- It runs successfully

![001](/img/csdn/78707323-8.png)

![00](/img/csdn/78707323-9.png)

## 3.Common Little Problems (Updated Occasionally)

- can not open file debug/*.exe

   Problem: an error occurs while running Link.exe; it's mainly because the computer doesn't have enough permissions.

   Solution: right-click the vc shortcut on the desktop, click "Compatibility", check "Run this program as an administrator" and apply

- If it won't run no matter what, then your workspace was created in vc's default MyProjects workspace, which causes lots of problems. So when you create a workspace, be sure to pick a folder of your own, preferably one without Chinese characters in the path.

## 4.Takeaways

- If it isn't a problem with your code, searching the error message on Baidu will usually solve it

- Honestly, I don't recommend vc. I'd recommend a good editor like Sublime Text 3 or Notepad++ paired with compilers like GCC and the JDK; it's lighter and faster than an IDE.
