---
title: Repeated macOS Permission Prompts with GodotSteam or a Custom Godot Build
author: Lazy_V
date: 2026-04-12
category:
  - Game Engines
tag:
  - Godot
sticky: true
star: true
isOriginal: true
---

These are the steps I used for repeated permission prompts with a locally installed GodotSteam build on macOS.

First, reset the relevant privacy permissions. Use the bundle identifier of your build; the command below uses Godot's identifier:

```bash
tccutil reset All org.godotengine.godot
```

Then open **System Settings → Privacy & Security → Full Disk Access**, click **+**, and add GodotSteam (or your custom Godot build).

Finally, apply an ad-hoc signature to the app bundle. Replace the path with the location of your app; mine is in `/Applications`:

```bash
codesign --force --deep --sign - /Applications/GodotSteam.app
```
