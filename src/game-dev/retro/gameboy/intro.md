---
title: GB/GBC Game Development — Introduction
author: Lazy_V
date: 2022-12-18 19:00:00
category:
  - Game Development
tag:
  - Game Development
  - Retro
  - GameBoy
order: 99999
---

::: info Before we begin
Nintendo's Game Boy was popular around the world, but I never had one as a child. When I learned about it later, I became fascinated by it and wanted to make games that could run on the hardware.
:::

<!-- more -->

## How I got into GB/GBC development

In 2018, I discovered [GBDK](https://github.com/gbdk-2020/gbdk-2020). Using it and the C programming I already knew, I made a few small games and demos. They remained unfinished, so I do not plan to show them here.

In 2020, I learned about [GB Studio](https://github.com/chrismaltby/gb-studio), a tool that makes GB/GBC game development accessible without requiring programming experience.

In 2021, during the pandemic, I felt particularly motivated to create something. I used GB Studio to make my own GBC version of Cat Mario: [CatMario-GB](../../001-games-gallery.md#catmario-gb).

## Let's start developing for GB/GBC

I would like to share what I have learned in a series of tutorials on **modern** GB/GBC development.

I will start with the more code-oriented GBDK toolchain. GB Studio is easier to get started with, so I can cover it later.

Rather than beginning with a long explanation of all the hardware, I will introduce individual hardware features, their settings, and the underlying principles as we need them to produce something on screen.

Start here:

- [Developing with GBDK](./gbdk/001-gbdk-intro.md)
