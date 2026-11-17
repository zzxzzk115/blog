---
title: GodotSteam 等自编译版本在 macOS 上反复弹窗确认权限？几行命令就够了
author: Lazy_V
date: 2026-04-12T00:00:00
categories: [游戏引擎]
tags: [Godot]
star: true
url: /zh/posts/game-engine/godotsteam-macos-permission.html
original: true
---

在 macOS 上使用本地安装的 GodotSteam 时反复弹窗确认权限，我是这样解决的。

首先，重置相关的隐私权限。这里要用你的版本对应的 bundle identifier，下面的命令用的是 Godot 的：

```bash
tccutil reset All org.godotengine.godot
```

然后打开 **系统设置 → 隐私与安全性 → 完全磁盘访问权限**，点击 **+**，加入 GodotSteam（或其他自编译的 Godot 版本）。

最后，对应用包做 ad-hoc 重新签名。路径换成你的应用所在位置，我的放在 `/Applications` 里：

```bash
codesign --force --deep --sign - /Applications/GodotSteam.app
```
