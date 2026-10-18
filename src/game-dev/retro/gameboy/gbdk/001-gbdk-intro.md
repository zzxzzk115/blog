---
title: An Introduction to GBDK
author: Lazy_V
date: 2022-12-18 19:05:00
category:
  - Game Development
tag:
  - Game Development
  - Retro
  - GameBoy
  - GBDK
isOriginal: true
---

Assembly language is a common choice for GB/GBC development. However, starting with it requires learning the hardware and instruction set together, which can be a substantial barrier for a beginner.

For this series, we will use a higher-level language: C. GBDK provides the tools and libraries needed to write C programs for the Game Boy and Game Boy Color.

[GBDK](https://github.com/gbdk-2020/gbdk-2020), the Game Boy Development Kit, includes a toolchain based on SDCC, together with an assembler, linker, and libraries for the supported hardware. The Game Boy CPU is the Sharp SM83, with an instruction set related to the Intel 8080 and Z80; it is not a full Z80, so Z80 code and libraries are not generally interchangeable with Game Boy code.

GBDK bundles the tools we need to build a ROM. Next, let's [set up the development environment](./002-gbdk-preparation.md).
