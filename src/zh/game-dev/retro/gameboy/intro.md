---
title: GB/GBC 游戏开发：简介
author: Lazy_V
date: 2022-12-18 19:00:00
category:
  - 游戏开发
tag:
  - 游戏开发
  - 复古
  - GameBoy
order: 99999
---

::: info 前言
任天堂 GameBoy 曾是风靡全球的掌机，不过很可惜，我小时候并没有接触过它。当我长大后了解它以后，对它产生了浓厚的兴趣。我希望我可以开发一些可以在 GameBoy 上运行的游戏。
:::

<!-- more -->

## 我与 GB/GBC 游戏开发的故事

2018 年，我了解到 [GBDK](https://github.com/gbdk-2020/gbdk-2020) 这个开发工具，并利用它，和我当时已掌握的 C 语言，写过一些小游戏和 DEMO。不过那些都是半成品，就不打算展示了。

2020 年，我了解到 [GB-Studio](https://github.com/chrismaltby/gb-studio) 这个让人人都能进行 GB/GBC 游戏开发的神奇工具。你并不需要编程相关的知识就可以使用它开始进行游戏创作。

2021 年，疫情期间我的创作欲比较强烈，成功使用 GB-Studio 制作了一款属于 GBC 的猫里奥：[传送门](../../001-games-gallery.md#catmario-gb)

## 开启 GB/GBC 的开发之旅吧

现在，我想分享一些 GB/GBC 游戏开发相关的知识，给大家带来**现代**的 GB/GBC 游戏开发教程系列。

对于开发工具，我打算先从比较硬核的 GBDK 开始，毕竟 GB-Studio 上手比较简单，可以放后面讲。

我并不打算先讲 GB/GBC 的硬件原理，这样过于枯燥。我会在讲开发细节的时候，介绍 GB/GBC 某个硬件模块的参数和设置，在实现效果的前提下，解释原理。

接下来你可以选择的教程：

- [使用 GBDK 开发](./gbdk/001-gbdk-intro.md)