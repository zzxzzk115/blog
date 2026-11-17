---
title: 'DevTerm，一款开源复古便携终端设备'
date: 2020-11-24T14:04:19
categories: [复古掌机]
tags: [DevTerm, ClockworkPi]
toc: true
---

![devterm_main_picture](/img/markdown_20201124140839.png)

DevTerm 是一种后现代的、数字的、简约的生活方式。A5 印刷纸的尺寸，将完整的 PC 功能与复古主义结合，配备了 6.8 英寸的超宽屏，经典 QWERTY 键盘，必要的接口，达到高速无限连接，具有较长的电池寿命，甚至包括实用的热敏打印机。

目前 DevTerm 在 [Clockwork 官网](https://www.clockworkpi.com/) 已经开启预售，预计 2021 年 4 月前开始发货。

<!--more-->

# 简介

第一眼看到它（DevTerm），我已经决定好了奖学金的去向。正如上次一眼看到 GameShell 就立马花钱购入一样，我对 DevTerm 同样一见钟情。Clockwork 推出的产品每次都能给我惊喜。

它的设计灵感我想多半来自于 TRS-80 Model100 和 NEC PC8200、8300 等，一部分来自于其他类似的机器（见图）：

**TRS-80 Model 100**

![trs-80 model 100](/img/markdown_20201125150156.png)

**NEC PC-8300**

![nec_pc_8300](/img/markdown_20201125145618.png)

**上世纪的一些 MiniPC**

![](/img/markdown_20201125133248.png)

对于 TRS-80 Model100，比尔盖茨说：“这应该是由我亲自参与写了大量代码的最后一台机器”，可见比尔盖茨对它的喜爱。

关于 TRS-80 Model100 的更多细节，可以看看这篇：[世界第一台笔记本](https://www.sohu.com/a/23818304_105527)

我觉得 DevTerm 也许受到了树莓派论坛一篇帖子的激发:[https://www.raspberrypi.org/forums/viewtopic.php?t=188635](https://www.raspberrypi.org/forums/viewtopic.php?t=188635)

帖主用 TRS-80 Model100 + 树莓派 3 + 宽屏 DIY 了一台真正可以敲的 MiniPC:

![trs-80 model 100 + rpi3](/img/markdown_20201125150611.png)

好了，回归正题。

![devterm_bottom_picture](/img/markdown_20201124141951.png)

可以看到，这次推出的新设备 DevTerm 与 GameShell 也有几分相似，却又有很多新的功能和玩法。

首先是它的 CPU 改为了 64 位 ARM CPU，这让更多软件得以运行。

然后是 16:6（1280\*480) 的宽屏相当于两个 4:3（640\*480) 的复古屏幕横向排列，这样既复古，也能显示更多内容，也让 NDS 模拟器可以有更好的显示效果。

它让我觉得惊喜的是采用了类似 ThinkPad 的 TrackPoint（小红帽）的设计，让鼠标操作也变得简单和人性化，不用再用 USB 连接鼠标，也不用难用和占体积的触摸板。

它继承了 GameShell 的特性，配备了十字方向键和 ABXY 按钮，这让它依旧可以成为复古游戏设备。

5G 的 WIFI 模块，比 GameShell 的 2.4G WIFI 模块强了太多，蓝牙 5.0，也让蓝牙设备的通信变得简单高速。

TF 卡、3.5mm 音频接口、立体扬声器这些都是标配。

唯一不太相同的是，它采用了两节 18650 锂电池供电的方式。不知道为什么要这样设计，致敬 TRS-80 Model100？？？也可能是为了方便上飞机？？？不过这些不重要。两节 18650 能带来大约最大 7000mAh 的容量，加上电池容易携带多节，它的续航时间可以说是非常可观。

这次的充电口不再是 Micro-USB 了，这次采用了 USB-C 进行充电，这样，也方便大家只用带一根线，不用每次都带 TypeC 和 Micro-USB 两根线。

有 3 个 USB-A 接口可供其他 USB 连接，可以很方便地连接许多 USB 设备。

Micro-HDMI 接口，也让它可以将屏幕内容输出到显示器上。

最让人感到惊喜的是，它拥有一个小型的热敏打印机（右上角），可以进行简单的打印。这一点倒是挺有那么一种复古感的，哈哈。

# 玩法

玩法自然是 ARM Linux PC 能做的，它基本都能做。

![devterm_function](/img/markdown_20201124145122.png)

![tech_support](/img/markdown_20201124145351.png)

可运行的操作系统目前有 clockworkOS、debian、ubuntu、Raspberry Pi 等。

然后，原本 GameShell 支持的开源游戏平台，它也都支持，不仅如此，它还支持更多桌面 PC 应用，你可以用它上网、敲代码、写文档、看视频等等。

![assembly](/img/markdown_20201124145501.png)

它同样采用模块化设计，这使得你可以方便地更改和替换模块、进行 DIY。

# 硬件

## 主板（MainBoard）

![mainboard](/img/markdown_20201124145825.png)

新的主板，支持你插入不同的核心模块进行工作。比如插入树莓派 CM3 模块，或者 clockwork 推出的 A04、A06 模块。

主板的参数在图中说明的很清楚，WIFI 和蓝牙都是板载的。

新的主板的集成度很高，该有的接口都有，真正做到了小体积，大功能。

## 核心模块（Core Module）

![core_module](/img/markdown_20201124150447.png)

所有核心模块的配置，一眼可见。

A-0401 和 A-0402 型号仅 RAM 的存储空间有不同，一个是 1GB，另一个是 2GB。A-04 系列和树莓派 CM3 的性能都属于较低（相对 A-06 而言较低，实际已经还不错了）的一个级别。

A-0602 和 A-0604 型号也仅 RAM 的存储空间不同，一个是 2GB，另一个是 4GB。A-06 系列采用 ARM 的大小核技术（big.LITTLE），旨在为适当的作业分配恰当的处理器。也就是说，操作系统会自动判断采用哪个核心来完成作业。例如你游玩 3D 游戏，那么操作系统使用 Cortex-A72 来负载，一些其他的不是很繁重的作业，将由 Cortex-A53 来处理。

当然，高配置的 A-06 自然也贵一些。

## 扩展模块（Ext. Module）

![ext_module](/img/markdown_20201124151415.png)

扩展模块进行了接口的扩展以及安装了风扇模块。

如你所见，扩展模块拥有 2 个 USB-A 接口、UART 串口调试接口、热敏打印机接口以及 MIPI-CSI 摄像头接口。

(看到这里我有个点子：在扩展的摄像头接口安装摄像头模块，拍照，用热敏打印机打印，hhh。)

官方对所有硬件都是开源的，所以说，扩展板的潜能无穷。大神没准搞个 4G/5G 模块，搞一些其他的模块，重新打样 PCB。那样 DevTerm 的玩法估计只会是你想不到的玩法。

## 键盘（Keyboard）

![keyboard](/img/markdown_20201124152007.png)

65% 的 QWERTY 键盘，配备了十字键和 ABXY，外加 TrackBall 和三个鼠标按键，这使得 DevTerm 可以进行正常的 PC 软件的使用。

它同样是基于 Arduino 开发的，你可以使用 ArduinoIDE 对它进行映射修改或者更多功能，你要是觉得不满足，你可以自己做一套键盘。毕竟 3D 打印的资料以及所有硬件电路图都是开源的。

## 模块化

![module_design](/img/markdown_20201124152341.png)

DevTerm 的模块化设计和资料几乎完全开源，让它变成了一个易于扩展、易于 DIY 的设备。它面向的并非普通用户，它主要面向的是极客、设计师、玩家、复古爱好者等。

# 价格

![price](/img/markdown_20201124152938.png)

价格还算能够接受，大概 2000 左右买顶配。

如果不是真的喜欢，谁又会剁手呢？

# 总结

DevTerm 是一款极具潜力的开源设备，它是真正具有开源精神的产品。它也算是对上世纪 MiniPC 的致敬，使用了类似 TRS-80 Model100 或者是 NEC PC-8300 的外形，却拥有着现代的 ARM Linux PC 的强大配置。可能设计团队真的很喜欢 TRS-80 Model100 或者 NEC PC-8300 吧，也可能正是 Clockwork 的这种怀旧感，这种开源精神打动了我，打动了其他人。

它并不面向普通用户，它更多地面向我这种折腾专业户，如果你也喜欢折腾，你也喜欢 linux，你也喜欢 DIY，建议你关注一下它。如果你单纯想玩游戏，建议还是不要考虑，毕竟价格也不低。

小道消息说过不久 KS 会发起众筹，一起期待吧！













