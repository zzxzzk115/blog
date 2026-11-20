---
title: 画廊
article: false
url: /zh/gallery.html
aliases:
  - /game-dev/001-games-gallery.html
  - /porting/001-porting-gallery.html
  - /software/001-software-gallery.html
  - /graphics/001-graphics-gallery.html
  - /porting/
  - /software/
  - /graphics/
---

做过、参与过和移植过的东西，带截图、视频，有的能直接玩。每个项目的详细介绍在[项目](/projects/)页。

## 游戏 {#games}

> 以下是我做过或参与开发的游戏，欢迎游玩体验，也欢迎交流开发相关的内容。

### 分裂细胞 Cells of Division

俯视角弹幕 Roguelike：在免疫系统里与「过去几局的自己」的克隆体（最多 6 个）并肩作战，搭配约 100 种道具，挑战 50 多个 Boss，消灭病毒。由 High Path Games 开发，我是联合创始人和程序负责人，负责程序架构设计、核心子系统开发并带领程序团队。**已于 2026 年 11 月 10 日在 Steam 正式发售**（Windows、macOS、Linux），欢迎购买和评测！

<iframe src="https://store.steampowered.com/widget/3879680/?l=schinese" frameborder="0" width="646" height="190" style="max-width:100%" loading="lazy" title="Cells of Division on Steam"></iframe>

{{< gallery grid >}}
/img/games/cells-of-division/screenshot-1.jpg | 分裂细胞 截图 1
/img/games/cells-of-division/screenshot-2.jpg | 分裂细胞 截图 2
/img/games/cells-of-division/screenshot-3.jpg | 分裂细胞 截图 3
/img/games/cells-of-division/screenshot-4.jpg | 分裂细胞 截图 4
{{< /gallery >}}

- [Steam 商店页面](https://store.steampowered.com/app/3879680/Cells_of_Division/)

### Lazy-100

用 Lua 编程的幻想主机，自带代码、精灵、地图、音效和音乐编辑器，基于我的 [VRI](https://github.com/zzxzzk115/VRI) 渲染接口，桌面和浏览器都能运行。主机里的游戏本身就是用这些编辑器做出来的示例。

![Lazy-100：编辑器与游戏演示](/img/games/lazy-100/showcase.webp)

- [在浏览器里直接玩 Breakout](https://zzxzzk115.github.io/Lazy-100/?cart=breakout) · [浏览卡带（Breakout、Lazy Bird、Snake）](https://zzxzzk115.github.io/Lazy-100/carts/)
- [源码](https://github.com/zzxzzk115/Lazy-100) · [卡带目录](https://github.com/zzxzzk115/Lazy-100-games)

### Planet Chaos 1 & 2

2020 年和 GeniusGameStudio 的伙伴们一起做的团队游戏：类似《百战天虫》的多人 2D 炮击对战，用 Unity 制作，我负责核心架构与玩法程序，并协调开发进度。续作 Planet Chaos 2 换成了像素美术和 Unity URP，加入了更多武器和玩法系统。

{{< gallery grid >}}
/img/games/planet-chaos/main_menu.png | Planet Chaos 主菜单
/img/games/planet-chaos/gameplay001.jpg | Planet Chaos 游戏画面
/img/games/planet-chaos/gameplay003.jpg | Planet Chaos 游戏画面
/img/games/planet-chaos/gameplay005.jpg | Planet Chaos 游戏画面
{{< /gallery >}}

{{< gallery grid >}}
/img/games/planet-chaos-2/MainMenu.png | Planet Chaos 2 主菜单
/img/games/planet-chaos-2/GamePlay1.jpg | Planet Chaos 2 游戏画面
/img/games/planet-chaos-2/GamePlay3.jpg | Planet Chaos 2 游戏画面
/img/games/planet-chaos-2/GamePlay5.jpg | Planet Chaos 2 游戏画面
{{< /gallery >}}

- Planet Chaos：[源码](https://github.com/GeniusGameStudio/PlanetChaos) · [下载（GitHub Release）](https://github.com/GeniusGameStudio/PlanetChaos/releases)
- Planet Chaos 2：[源码](https://github.com/GeniusGameStudio/PlanetChaos2) · [下载（GitHub Release）](https://github.com/GeniusGameStudio/PlanetChaos2/releases)

### CatMario-GB

猫里奥 Game Boy 版（支持 GBC），用 GB Studio 制作。目前为 DEMO，包含游戏的基本流程和玩法。

{{< itch url="https://lazy-v.itch.io/catmario-gb" desc="猫里奥的 Game Boy 版。" >}}

{{< gallery grid pixel >}}
/img/games/catmario-gb/title.png | 标题画面
/img/games/catmario-gb/level1_1.png | 1-1 关
{{< /gallery >}}

- [在本站直接游玩](/GameSrc/CatMarioGB/)
- [下载 ROM](/GameSrc/CatMarioGB/rom/game.gb) · [GitHub Release](https://github.com/zzxzzk115/CatMarioGB/releases) · [源码](https://github.com/zzxzzk115/CatMarioGB)

### GoldMiner-Rebirth

经典黄金矿工的重制版，用 [LÖVE](https://love2d.org/)（Love2D）制作。最初是为 [GameShell](https://www.clockworkpi.com/gameshell) 掌机写的「黄金矿工 GameShell 版」，后来改名 GoldMiner-Rebirth，加入了 Trimui 系列（Smart Pro、Brick）的支持，并被收录进 [PortMaster](https://portmaster.games/detail.html?name=goldminer)，支持 PortMaster 的掌机都能玩。

{{< itch url="https://lazy-v.itch.io/goldminer-rebirth" desc="经典游戏重制，为兼容 LÖVE（Love2D）的掌机打造。" >}}

{{< gallery grid >}}
/img/games/goldminer-rebirth/screenshots_01_main_menu.png | 主菜单
/img/games/goldminer-rebirth/screenshots_03_level01.png | 第一关
/img/games/goldminer-rebirth/screenshots_04_shop.png | 商店
/img/games/goldminer-rebirth/photos_04_trimui_brick_red_01.jpg | 在 Trimui Brick 上运行
{{< /gallery >}}

- [从 itch.io 下载](https://lazy-v.itch.io/goldminer-rebirth) · [GitHub Release](https://github.com/zzxzzk115/GoldMiner-Rebirth/releases) · [源码](https://github.com/zzxzzk115/GoldMiner-Rebirth)
- [在 PortMaster 中安装](https://portmaster.games/detail.html?name=goldminer)（感谢 [JanTrueno](https://github.com/JanTrueno) 的移植）
- 遇到 bug 欢迎到 GitHub [提 issue](https://github.com/zzxzzk115/GoldMiner-Rebirth/issues)。

## 移植 {#porting}

> 把游戏、模拟器和软件搬到复古掌机上：GameShell、PocketCHIP、H700 掌机……更多在我的 [GitHub](https://github.com/zzxzzk115)。

{{< projects group="porting" >}}

### 相关文章

{{< pagelist "/posts/how-to-play-gameshell-01, /posts/gameshell-bigger-lcd, /posts/run-godot-game-on-gameshell, /posts/pocketchip-love2d, /posts/pocketchip-retroarch, /posts/pocketchip-opengl-hardware-speedup, /posts/pocketchip-stero-speaker, /posts/intro-devterm" >}}

## 软件 {#software}

> 桌面应用、命令行工具、库和网页小工具。更多在我的 [GitHub](https://github.com/zzxzzk115)。

{{< projects group="software" >}}

### 相关文章

{{< pagelist "/posts/hugo-blog-revival, /posts/dorm-assistant, /posts/api-fanscount-github, /posts/api-fanscount-bilibili, /posts/about-python-api" >}}

## 图形学与引擎 {#graphics}

> 游戏引擎、渲染接口、渲染器和图形库：从利兹大学 COMP5530M 课程的学生小组项目 Snow Leopard Engine，到我现在的 Vultra 生态。更多在我的 [GitHub](https://github.com/zzxzzk115)。

{{< projects group="graphics" >}}

### 相关文章

{{< pagelist "/posts/game-engine/kytten-shader, /posts/game-engine/kytten-csharp-scripting-mono, /posts/learn-from-pilot-01, /posts/learn-from-pilot-02, /posts/learn-from-pilot-03, /posts/phd-life/openxr-simulator" >}}
