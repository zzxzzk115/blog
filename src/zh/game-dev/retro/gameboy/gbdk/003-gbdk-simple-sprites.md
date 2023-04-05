---
title: 使用 GBDK 绘制简单的精灵
author: Lazy_V
date: 2022-12-20
category:
  - 游戏开发
tag:
  - 游戏开发
  - 复古
  - GameBoy
  - GBDK
isOriginal: true
---

GameBoy 屏幕分辨率为 160*144，对于现在而言，这是非常低的，但是这个分辨率对于那个像素时代而言，却已经足以显示一个个生动活泼的角色了。

[精灵 (Sprite)](https://en.wikipedia.org/wiki/Sprite_(computer_graphics))，在计算机图形学中指 2D 的位图，并经常使用于 2D 游戏中。

举个例子，超级马里奥中，马里奥对应的位图就是精灵。

我们如何使用 GBDK 将一个精灵绘制到 GameBoy 的屏幕中呢？

<!-- more -->

答案是，使用工具，设计好我们的精灵，最后将精灵数据导出为 C 数组。

这里，我们使用最为流行的 GBTD。

::: info 如果你想造轮子
当然，自己写一个工具也是可以的，只要自己写的工具最后导出的 C 数组符合 GBDK 需要的 C 数组格式就行。
:::

## GBTD 简介

在 GameBoy 的世界中，地图多半是由瓦块所组成的瓦块地图 (Tile Map)，精灵实际上也是由一些小小的瓦块组成的。

GBTD, GameBoy Tile Designer，主要用于设计瓦块 (Tile)，并最终导出兼容 GBDK 的 C 数组。

它的界面是这样的：

![GBTD 的界面](/images/game-dev/retro/gameboy/gbdk/gbtd_interface_01.png)

::: tip 关于 MacOS/Linux 运行 GBTD 和 GBMB
如果没有搭建好环境，请参考上一篇文章，先搭建好环境。

环境搭建好后，且跟着教程一起配置了 alias 后，可以直接使用别名打开：

```bash
# 打开 GBTD
gbtd

# 打开 GBMB
gbmb
```

:::

## 绘制第一个简单的精灵

接下来，我们绘制一个 `8*8` 的笑脸，并显示在靠近屏幕中央的位置。

::: info 为什么是 8*8
GameBoy 中，精灵的渲染有两种模式（二选一）：

- `8*8`
- `8*16`

每个瓦块的尺寸最小为 `8*8`，所以最简单的精灵都是用一个瓦块，这里我们希望精灵不要过于迷你，所以还是选择 `8*8` 的尺寸，实际上，`1*1` 都是可以的，只是依旧还是需要一个 `8*8` 的瓦块来表达。复杂一点的精灵，可能会使用 `8*16` 模式。更复杂一点的精灵，甚至可能是多个 `8*8` 的瓦片组合而成的。
:::

GBTD 的最下方有一个颜色选择器。

左侧 L R 显示的是鼠标左键和鼠标右键对应要在画布上绘制的颜色索引。

右侧的四个色块代表 0 到 3 四个索引色，每个索引对应的颜色是我们自己通过调色板进行配置的，默认调色板是从白到黑的渐变的四个颜色。

![GBTD 颜色选择器](/images/game-dev/retro/gameboy/gbdk/gbtd_color_picker.png)

GBTD 的左侧工具栏，默认选择了画笔工具，画笔底下是油漆桶工具。往下四个是移动工具，可以自行试试效果。再往下是垂直翻转、水平翻转、旋转以及自动更新。

![GBTD 左侧工具栏](/images/game-dev/retro/gameboy/gbdk/gbtd_left_toolbar.png)

::: info GBTD 不存在橡皮擦工具
GBTD 不存在橡皮擦工具，这是因为 GameBoy 的颜色模式是索引色模式，而非 RGBA 模式。

如果需要擦除某个画错的部分，你要做的就是使用另一个索引色来填充画错的部分。
:::

当我们在颜色选择器的右侧色块区域使用鼠标左键点击其中一个色块，则鼠标左键即将绘制的颜色索引会变成你点击的那个色块的索引值，简而言之就是接下来你的鼠标左键在画布上绘制的时候画笔（或油漆桶）的颜色变成了你所选色块的颜色。鼠标右键也是一样的逻辑。这样方便我们鼠标左右两个键在画布上绘制图形。

我们首先选择画笔工具，使用鼠标左键点击颜色选择器右侧的索引值为 3 的黑色色块，然后在画布上绘制一个笑脸，当然，你也可以按照自己的想法绘制，只要是 `8*8` 及以内的就行。

然后选择油漆桶工具，选择索引值为 1 的浅灰色色块，然后填充笑脸。

画好后大致长这样（没认真画，教程嘛，意思意思）：

![第一个精灵：笑脸](/images/game-dev/retro/gameboy/gbdk/first_sprite_smile_face.png)

绘制好了，我们就可以开始导出成 GBDK 兼容的 C 数组了。

当然，为了备份，你应该先保存一下。保存后，你将得到一个以 `.gbr` 后缀的文件，下次再用 GBTD 打开它就能继续编辑。

## 导出绘制的精灵

最上面主菜单点击 `Files/ExportTo`，然后配置如下：

![导出笑脸为 GBDK 支持的 C 数组](/images/game-dev/retro/gameboy/gbdk/export_smile_face_as_gbdk_c_array.png)

::: info 关键参数介绍
Filename - 导出文件的名称，这里我们填入 `Smile.c`

Type - 导出数据的类型，这里我们选择 `GBDK C file`，代表导出文件中包含的数据是兼容 GBDK 的 C 数组

Label - 导出 C 数组的名称，我们在代码中会用到，这里我们命名为 `Smile`

Format - 颜色格式，这里我们选择 `Gameboy 4 color`
:::

点击 `OK` 即可导出。导出成功后，会在 `.gbr` 所在同级目录下得到 `Smile.h` 和 `Smile.c` 文件。

`.h` 文件中是数组相关的声明，而 `.c` 文件中是具体定义，存放了实际的精灵数据。

下面，我们就可以利用 C 数组，开始编写程序，绘制精灵了。

## 开始编程吧！

### 使用 Visual Studio Code + Makefile 进行项目搭建

::: info 
之前的 helloworld 程序由于是单文件，过于简单，所以没有提到 Visual Studio Code 的配置以及使用 Makefile。

后面的项目中，我们都会使用 Visual Studio Code + Makefile 的模式来进行开发。
:::

我们创建一个 `gb-dev` 目录，并在它下面创建一个 `first-sprite` 目录。

然后使用 Visual Studio Code 打开 `gb-dev` 目录。

首先配置 `includePath`，让我们可以拥有智能提示。在 `gb-dev` 目录下创建一个 `.vscode` 文件夹，在该文件夹下创建一个名为 `c_cpp_properties.json` 的配置文件：

```json
{
    "configurations": [
        {
            "name": "GBDK_VSC",
            "includePath": [
                "${GBDKDIR}/include/**"
            ],
            "defines": [],
            "macFrameworkPath": [],
            "compilerPath": "${GBDKDIR}/bin/lcc",
            "cStandard": "gnu99"
        }
    ],
    "version": 4
}
```

这样，我们以后的代码就拥有智能提示了。

然后我们将之前导出的 `Smile.h` 和 `Smile.c` 拷贝到 `first-sprite` 目录下。

接着我们就可以在 `first-sprite` 目录下，开始编写主程序 `FirstSprite.c` 了：

```c
#include <gb/gb.h>
#include <stdio.h>
#include "Smile.h"

void main()
{
    // 设置精灵数据
    // 从第 0 号位的 Tile 开始，设置 No.0 的瓦块的数据
    // 数据来源于 Smile 数组
    set_sprite_data(0, 0, Smile);
    
    // 设置精灵使用哪个瓦块的数据
    // 这里是 No.0 精灵使用 No.0 瓦块数据
    set_sprite_tile(0, 0);

    // 一个宏，内部设置 LCDC 寄存器的第 1 位为 1，
    // 目的是开启精灵层，代表显示所有精灵
    SHOW_SPRITES;

    // 将精灵 No.0 移动到 (84, 78) 的位置，即屏幕中央附近
    move_sprite(0, 84, 78);
}
```

随后，我们编写一个叫做 `Makefile` 的文件。实际上，Makefile 是 make 的配置文件，make 可以方便我们设定编译参数以及具体每个模块的编译流程。这些模块的编译流程大多是重复的，所以使用 make 这套规则去编译，节约了我们的时间，也让编译流程更加清晰。

我们的 `Makefile` 如下：

```makefile
# 设置 LCC 编译器执行路径
CC  = $(GBDKDIR)/bin/lcc

# 设置 SameBoy 执行路径
EMU = /Applications/SameBoy.app/Contents/MacOS/SameBoy

# 默认行为，编译各个编译单元，最后链接得到 FirstSprite.gb
all:
	$(CC) -Wa-l -Wl-m -Wl-j -o FirstSprite.gb Smile.c FirstSprite.c

# 编译得到 FirstSprite.gb 后，使用 SameBoy 启动
run: all
	$(EMU) FirstSprite.gb

# 清理，删除中间文件和目标文件
clean:
	rm -f *.o *.lst *.map *.gb *.ihx *.sym *.cdb *.adb *.asm *.noi
```

现在，make 支持几种不同的命令参数：

- 无，即默认行为，默认为 Makefile 中第一个出现的目标，在我们的设置中，为 all
- all，编译链接最终得到 `FirstSprite.gb` ，即 ROM 文件
- run，编译得到 ROM 后，使用 SameBoy 模拟器运行该 ROM 文件
- clean，清理，删除中间文件和目标文件

我们可以直接使用 `make run` 来编译、链接并运行。

最后的效果如下：

![成功在屏幕中显示第一个精灵](/images/game-dev/retro/gameboy/gbdk/successfully_showed_first_sprite.png)

最后还可以使用 `make clean` 来删除中间文件和目标文件，回到只有源码和 Makefile 等文件的状态。

::: tip
`gb-dev` 源码[看这里](https://github.com/zzxzzk115/blog/tree/master/src/.vuepress/public/src/gb-dev/)
:::