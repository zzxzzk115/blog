---
title: 'Installing RetroArch on the PocketChip'
date: 2022-05-12T19:47:41
tags: [PocketChip, RetroArch]
categories: [Retro Handhelds]
toc: true
aiTranslated: true
---

> RetroArch is an all-in-one emulator. By loading different emulator cores it can run games for all kinds of systems, and you can tweak all sorts of settings and add filters and shaders to give an ordinary screen that retro feel.

# Preparation

## 1. Install the dependencies

I won't go through them one by one this time; here's every dependency you need in one go!

```bash
sudo apt update
sudo apt install -y libsdl1.2-dev libsdl2-dev libboost-system-dev libboost-filesystem-dev libboost-date-time-dev libfreeimage-dev libfreetype6-dev libeigen3-dev libcurl4-openssl-dev libasound2-dev libgl1-mesa-dev cmake build-essential pkg-config
```

## 2. Get the RetroArch source code

```bash
git clone https://github.com/zzxzzk115/RetroArch.git
```

# Installing RetroArch

```bash
cd RetroArch
./configure --prefix=/home/chip/retroarch --enable-opengles --disable-oss --disable-sdl --disable-ffmpeg --disable-vg --disable-cg --enable-neon --enable-floathard --disable-wayland --disable-pulse --enable-dylib --enable-hid --enable-zlib --enable-7zip
make -j2
sudo make install
sudo chmod +x /home/chip/retroarch/bin/retroarch
sudo ln -s /home/chip/retroarch/bin/retroarch /usr/bin/retroarch
```

# Running it

`retroarch`

# Problems I ran into

At first some parts show up as black boxes. That's because the assets haven't been downloaded.

Choose `Online Updater->Update Assets` and wait for it to download and extract automatically.

Once that's done, the icons display properly, but the on-screen font becomes really blurry.

Next comes the configuration part:

# Configuring RetroArch

Press ESC to quit, then delete the default theme's font:

```bash
sudo rm ~/.config/retroarch/assets/xmb/monochrome/font.ttf
```

If you don't want the mouse cursor showing after launch, you need to enable fullscreen.

Open retroarch again.

Just turn on `Video->Start in FullScreen Mode` in the second column.

You'll probably want to bring up the quick menu while playing, so you need to rebind a hotkey:

In `Input->Input Hotkey Binds` in the second column, press Enter on Menu toggle, then press Backspace to finish the binding.

If you find the system notification font too large, you can edit the config:
`sudo nano .config/retroarch/retroarch.cfg`

Find video_font_size and change it from 32 to 16, or whatever size you like.

And that's basically it for configuration.

Of course, if you want things to run smoothly, you should read this first:

[Enabling OpenGL hardware acceleration on the PocketChip](/posts/pocketchip-opengl-hardware-speedup)

----

2022/05/12 Migrated here from cnblogs.
