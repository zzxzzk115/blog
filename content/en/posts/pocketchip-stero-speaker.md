---
title: 'Modding the PocketChip with Stereo Speakers'
date: 2020-04-16T22:04:00
tags: [PocketChip]
categories: [Retro Handhelds]
toc: true
aiTranslated: true
cnblogs: 12716175
---

> Originally published on my old cnblogs blog: [Pocketchip魔改加双扬声器](https://www.cnblogs.com/lazy-v/p/12716175.html) (written 2020-04-16).

> The PocketChip doesn't have a built-in speaker; it only gives you a 3.5mm headphone jack.
>
> Sometimes you don't feel like carrying headphones around and just want sound out loud. What then?
>
> Since the PocketChip exposes its GPIO, we can solder one in ourselves!
>
> This mod is cheap, and anyone with a pair of hands can do it.

# 0. Buy the Parts

No parts, no mod.

- 8Ω 23mm mini speaker * 2 [Recommended link](https://m.tb.cn/h.Vhm6Jfh?sm=915842)
- Mini Class D amplifier board * 1 [Recommended link](https://m.tb.cn/h.V7fuAky?sm=7d460f)
- Soldering iron * 1
- Rosin * 1
- Solder wire * 1
- Hot glue gun * 1
- Hot glue sticks * 1
- Some 30AWG wire
- Heat-resistant insulating tape * 1
- Someone who can solder * 1
- One PocketChip (I assume everyone reading this has one)

![](/img/markdown_20220512181827.png)

(I forgot to include the hot glue and the glue gun in the photo above.)

# 1. Unplug the Power Connector

Before soldering, you must unplug the power connector, otherwise it isn't safe.

![](/img/markdown_20220512181852.png)

# 2. Mount the Class D Amplifier Board

Before mounting it, cover the chip with heat-resistant tape to protect it.

![](/img/markdown_20220512181918.png)

![](/img/markdown_20220512181934.png)



Then fix the amp board in place with the hot glue gun:

![](/img/markdown_20220512181952.png)



![](/img/markdown_20220512182007.png)

# 3. Start Soldering

First solder the amp board's `-` to the `GND` pin, i.e. the negative goes to ground.

![](/img/markdown_20220512182023.png)



Then connect +5V (positive) to `VCC-5V`:

![](/img/markdown_20220512182038.png)



Then solder according to the following rules:

`L`->`HPL`

`⊥`->`HPCOM`

`R`->`HPR`

![](/img/markdown_20220512182056.png)



Next, fix the left and right speakers in place with the hot glue gun:

![](/img/markdown_20220512182111.png)



Then connect the right speaker's (the one on the left as you look at it) `-` to the `-` of R on the amp board, and its other lead to R's `+`.

Do the same for the left speaker, matching its positive and negative to L's positive and negative.

![](/img/markdown_20220512182133.png)



And that's the soldering done! Plug the battery connector back in, put everything back together, and power it on. Open a game or app with sound effects and give it a test.

This saves you the hassle of always having to bring headphones. That said, if I want the speakers to mute automatically when headphones are plugged in, I'll still need to look into it some more.

----

2022/05/12 Migrated here from cnblogs.
