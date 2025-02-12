---
title: Develop OpenXR native PC apps without a headset by using Meta XR Simulator
description: If you don't have an XR headset but you want to develop OpenXR apps, you can use Meta XR Simulator! It's great.
author: Lazy_V
date: 2025-02-11
category:
  - PhD-Life
tag:
  - OpenXR
sticky: true
star: true
isOriginal: true
---

If you don't have an XR headset but you want to develop OpenXR apps, you can use Meta XR Simulator! It's great.

## Download Meta XR Simulator

![Download Meta XR Simulator](/images/posts/phd-life/openxr-simulator/download_meta_xr_simulator.png)

Download it from [here](https://developers.meta.com/horizon/downloads/package/meta-xr-simulator)

You will get a compressed file, and you have to extract it and get the necessary files.

We only need the `MetaXRSimulator` folder. Copy it to somewhere on your machine, for example, `C:\MetaXRSimulator`.

## Configure Currently Active OpenXR Runtime & Run

There are two options to configure the currently active OpenXR runtime on Windows:
- Windows Registry
- Environment Variable

I recommend you to use an temporary environment variable (`XR_RUNTIME_JSON`) in the IDE or the terminal to set the currently active OpenXR runtime, which will not replace the system default OpenXR runtime.

::: tabs

@tab Powershell

```powershell
$Env:XR_RUNTIME_JSON = "C:\MetaXRSimulator\meta_openxr_simulator.json"
# then run your OpenXR apps
```

@tab CMD

```
set XR_RUNTIME_JSON="C:\MetaXRSimulator\meta_openxr_simulator.json"
:: then run your OpenXR apps
```

:::

After configuring the environment variable, just run your OpenXR apps in the same terminal!

Have fun!