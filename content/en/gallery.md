---
title: Gallery
article: false
url: /gallery.html
aliases:
  - /game-dev/001-games-gallery.html
  - /porting/001-porting-gallery.html
  - /software/001-software-gallery.html
  - /graphics/001-graphics-gallery.html
  - /porting/
  - /software/
  - /graphics/
---

Things I've made, worked on or ported, with screenshots and videos; some you can play right here. Each project's details are on the [Projects](/projects/) page.

## Games {#games}

> Games I've made or worked on. Have a go, and feel free to get in touch about game development.

### Cells of Division

A top-down bullet-hell roguelike: fight alongside clones of your past runs (up to 6 allies) inside the immune system, mix around 100 items and take down 50+ bosses to wipe out viruses. Developed by High Path Games, where I'm a co-founder and the programming lead: I design the program architecture, build core subsystems and lead the programming team. **Out now on Steam** (released 10 November 2026) for Windows, macOS and Linux. Reviews are very welcome!

<iframe src="https://store.steampowered.com/widget/3879680/?l=english" frameborder="0" width="646" height="190" style="max-width:100%" loading="lazy" title="Cells of Division on Steam"></iframe>

{{< gallery grid >}}
/img/games/cells-of-division/screenshot-1.jpg | Cells of Division screenshot 1
/img/games/cells-of-division/screenshot-2.jpg | Cells of Division screenshot 2
/img/games/cells-of-division/screenshot-3.jpg | Cells of Division screenshot 3
/img/games/cells-of-division/screenshot-4.jpg | Cells of Division screenshot 4
{{< /gallery >}}

- [Steam store page](https://store.steampowered.com/app/3879680/Cells_of_Division/)

### Lazy-100

A Lua fantasy console with built-in code, sprite, map, sound and music editors, built on my [VRI](https://github.com/zzxzzk115/VRI) rendering interface; it runs on desktop and in the browser. Its games are examples made with the console's own tools.

![Lazy-100: the editors and games in action](/img/games/lazy-100/showcase.webp)

- [Play Breakout in your browser](https://zzxzzk115.github.io/Lazy-100/?cart=breakout) · [Browse cartridges (Breakout, Lazy Bird, Snake)](https://zzxzzk115.github.io/Lazy-100/carts/)
- [Source](https://github.com/zzxzzk115/Lazy-100) · [Cartridge catalog](https://github.com/zzxzzk115/Lazy-100-games)

### Planet Chaos 1 & 2

Team games I made with GeniusGameStudio in 2020: Worms-style multiplayer 2D artillery battles built in Unity. I worked on the core architecture and gameplay programming and coordinated the schedule. The sequel, Planet Chaos 2, moved to pixel art and Unity URP, with more weapons and gameplay systems.

{{< gallery grid >}}
/img/games/planet-chaos/main_menu.png | Planet Chaos main menu
/img/games/planet-chaos/gameplay001.jpg | Planet Chaos gameplay
/img/games/planet-chaos/gameplay003.jpg | Planet Chaos gameplay
/img/games/planet-chaos/gameplay005.jpg | Planet Chaos gameplay
{{< /gallery >}}

{{< gallery grid >}}
/img/games/planet-chaos-2/MainMenu.png | Planet Chaos 2 main menu
/img/games/planet-chaos-2/GamePlay1.jpg | Planet Chaos 2 gameplay
/img/games/planet-chaos-2/GamePlay3.jpg | Planet Chaos 2 gameplay
/img/games/planet-chaos-2/GamePlay5.jpg | Planet Chaos 2 gameplay
{{< /gallery >}}

- Planet Chaos: [source](https://github.com/GeniusGameStudio/PlanetChaos) · [download (GitHub releases)](https://github.com/GeniusGameStudio/PlanetChaos/releases)
- Planet Chaos 2: [source](https://github.com/GeniusGameStudio/PlanetChaos2) · [download (GitHub releases)](https://github.com/GeniusGameStudio/PlanetChaos2/releases)

### CatMario-GB

A Cat Mario demo for the Game Boy (GBC supported), made with GB Studio. The demo covers the basic game flow and mechanics.

{{< itch url="https://lazy-v.itch.io/catmario-gb" >}}

{{< gallery grid pixel >}}
/img/games/catmario-gb/title.png | Title screen
/img/games/catmario-gb/level1_1.png | Level 1-1
{{< /gallery >}}

- [Play in the browser on this site](/GameSrc/CatMarioGB/)
- [Download the ROM](/GameSrc/CatMarioGB/rom/game.gb) · [GitHub releases](https://github.com/zzxzzk115/CatMarioGB/releases) · [Source](https://github.com/zzxzzk115/CatMarioGB)

### GoldMiner-Rebirth

A remake of the classic Gold Miner, made with [LÖVE](https://love2d.org/) (Love2D). It started as "Gold Miner for GameShell", written for the [GameShell](https://www.clockworkpi.com/gameshell) handheld; it was later renamed GoldMiner-Rebirth, gained support for the Trimui series (Smart Pro, Brick), and is now included in [PortMaster](https://portmaster.games/detail.html?name=goldminer), so any handheld that runs PortMaster can play it.

{{< itch url="https://lazy-v.itch.io/goldminer-rebirth" >}}

{{< gallery grid >}}
/img/games/goldminer-rebirth/screenshots_01_main_menu.png | Main menu
/img/games/goldminer-rebirth/screenshots_03_level01.png | Level 1
/img/games/goldminer-rebirth/screenshots_04_shop.png | Shop
/img/games/goldminer-rebirth/photos_04_trimui_brick_red_01.jpg | Running on a Trimui Brick
{{< /gallery >}}

- [Download on itch.io](https://lazy-v.itch.io/goldminer-rebirth) · [GitHub releases](https://github.com/zzxzzk115/GoldMiner-Rebirth/releases) · [Source](https://github.com/zzxzzk115/GoldMiner-Rebirth)
- [Install via PortMaster](https://portmaster.games/detail.html?name=goldminer) (thanks to [JanTrueno](https://github.com/JanTrueno) for the port)
- Found a bug? [Open an issue](https://github.com/zzxzzk115/GoldMiner-Rebirth/issues).

## Porting {#porting}

> Games, emulators and software brought to retro handhelds: GameShell, PocketCHIP, H700 handhelds… More on my [GitHub](https://github.com/zzxzzk115).

{{< projects group="porting" >}}

### Related posts

{{< pagelist "/posts/how-to-play-gameshell-01, /posts/gameshell-bigger-lcd, /posts/run-godot-game-on-gameshell, /posts/pocketchip-love2d, /posts/pocketchip-retroarch, /posts/pocketchip-opengl-hardware-speedup, /posts/pocketchip-stero-speaker, /posts/intro-devterm" >}}

## Software {#software}

> Desktop apps, command-line tools, libraries and small web tools. More on my [GitHub](https://github.com/zzxzzk115).

{{< projects group="software" >}}

### Related posts

{{< pagelist "/posts/hugo-blog-revival, /posts/dorm-assistant, /posts/api-fanscount-github, /posts/api-fanscount-bilibili, /posts/about-python-api" >}}

## Graphics & Engines {#graphics}

> Game engines, a rendering interface, renderers and graphics libraries: from Snow Leopard Engine, our COMP5530M student group project at Leeds, to my current Vultra ecosystem. More on my [GitHub](https://github.com/zzxzzk115).

{{< projects group="graphics" >}}

### Related posts

{{< pagelist "/posts/game-engine/kytten-shader, /posts/game-engine/kytten-csharp-scripting-mono, /posts/learn-from-pilot-01, /posts/learn-from-pilot-02, /posts/learn-from-pilot-03, /posts/phd-life/openxr-simulator" >}}
