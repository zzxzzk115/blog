---
title: GodotSteam 等自编译版本在 macOS 上反复弹窗确认权限？几行命令就够了
author: Lazy_V
date: 2026-04-12
category:
  - 游戏引擎
tag:
  - Godot
sticky: true
star: true
isOriginal: true
---

很简单，先重制相关权限

```bash
tccutil reset All org.godotengine.godot
```

然后 `Settings -> Privacy & Security -> Full Disk Access` 栏目点 `+` 加入 GodotSteam (或其他自编译版本)

最后，强制重新签名：

```bash
# 路径填具体对应的，这里我把 GodotSteam 放到 /Applications 里了
codesign --force --deep --sign - /Applications/GodotSteam.app 
```