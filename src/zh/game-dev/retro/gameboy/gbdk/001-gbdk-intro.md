---
title: GBDK 简介
author: Lazy_V
date: 2022-12-18 19:05:00
category:
  - 游戏开发
tag:
  - 游戏开发
  - 复古
  - GameBoy
  - GBDK
isOriginal: true
---

对于经典的 GB/GBC 开发，高手们习惯使用汇编。但是使用汇编需要我们首先对 GB/GBC 整个硬件原理和完整的指令集有了完整的了解后才合适，这样的成本太高了。

现代的 GB/GBC 开发，至少需要使用高级编程语言，例如 C 语言。我们可以利用 GBDK 和 C 语言，进行 GB/GBC 开发。

[GBDK](https://github.com/gbdk-2020/gbdk-2020) (GameBoy Development Kit) 即 GameBoy 开发工具包，主要包含一个 C 语言编译器： SDCC。它包括编译器、汇编器和链接器。GBDK 还提供面向受支持硬件的库。Game Boy 使用 Sharp SM83 CPU，其指令集与 Intel 8080、Z80 有渊源，但它并不是完整的 Z80，因此不能将 Z80 代码和库与 Game Boy 代码直接互换。

GBDK 包含了我们编译相关的所有内容，接下来我们开始进行环境搭建吧！