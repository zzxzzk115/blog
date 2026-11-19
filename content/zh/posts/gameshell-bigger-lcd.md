---
title: 'GameShell 魔改大屏攻略'
date: 2020-04-09T15:56:00
tags: [GameShell, ClockworkPi, 改装]
categories: [复古掌机]
toc: true
cnblogs: 12667486
---

> 本文最初发表于我在博客园的旧博客：[GameShell 魔改大屏攻略](https://www.cnblogs.com/lazy-v/p/12667486.html)（写于 2020-04-09）。

> 目前已经有小伙伴成功魔改，他将过程分享到了 GitHub，这是他分享的仓库地址：https://github.com/Yvees/GameShellHacking

# 材料采购

我们需要的材料：

1. 一块 3.5 寸屏幕(320 x 240 或者 640 x 480)
2. 6cm 45pin 异面 FPC 线
3. PCB 转接板
4. FPC 座 * 2，分别是 0.3mm H1.0 45P 翻盖、0.5mm H2.0 54P 翻盖
5. 3D 打印前壳



屏幕大致有两个不错的选择，一是柯达科的 320 x 240，[tb 链接](<https://item.taobao.com/item.htm?ut_sk=1.WOMnj8sz1t0DAFrTn0PDtX4g_21380790_1586412009068.Copy.1&id=594337582777&sourceType=item&price=15-72.9&suid=521C3937-9B73-4FE5-B065-ECE8247FC3B2&un=9394a44ddf9a362f&share_crt_v=1&spm=a2159r.13376460.0.0&sp_tk=JElVYnMxUXpnRjFEJA==&cpp=1&shareurl=true&short_name=h.VhiOBnH&sm=2da0f8&tdsourcetag=s_pctim_aiomsg&app=chrome>)

二是辰宸科技的这款 640 x 480，[tb 链接](<https://item.taobao.com/item.htm?spm=a1z10.1-c-s.w4004-21816738571.7.196c4ab6nmfeKM&id=603271622592>)

具体看个人需求。**一定要和店家说要串联 18V 的!主要是要串联！**



FPC 线的 [tb 链接](<https://item.taobao.com/item.htm?spm=a1z10.3-c.w4002-16327681171.37.d71171d3Vm6TDU&id=565842370557>)



PCB 转接板和 FPC 座需要定制+焊接，当然懂焊接的可以都买了自己焊接。

PCB 推荐 [这家]()，FPC 座的两款的链接：[(1)](<https://item.taobao.com/item.htm?spm=a1z10.3-c.w4002-22306881049.11.681e2eeciI7LO7&id=574405341541>) [(2)](<https://item.taobao.com/item.htm?spm=a1z10.3-c.w4002-22306881049.9.5d582eecjOhlZJ&id=574402496160>)



3D 打印的话，有一家学生优惠的，可以试试，[tb 链接](<https://item.taobao.com/item.htm?spm=a1z10.3-c.w4002-21947488495.12.475c45caiJFXOj&id=609901366662>)



# 魔改流程

材料都拿到手后，参考以下流程：

1. 先把原屏幕和 lcd 背板分离：

   ![](/img/markdown_20220512181634.webp)

2. 准备前盖、转接板、6cm 异面 45pinFPC 线：

   ![](/img/markdown_20220512181652.webp)

3. 连接排线：

   ![](/img/markdown_20220512181708.webp)

   ![](/img/markdown_20220512181727.webp)

   ![](/img/markdown_20220512181745.webp)

4. 替换内核文件 [待更新内容]：

5. 组装前壳，搞定！

如果用 240p 的屏幕，还需要打个 lcd 的 patch。

3D 前壳的 STL 文件，PCB 文件以及内核文件均在我们的 GameShell 分享群的群文件里，欢迎 GameShell 爱好者加入。

群号: 1041399424

图源群中 梦中大佬，官方论坛和闲鱼(非卖) 改大屏的就是他，此教程也是他分享的魔改过程，非常感谢他！

----

2022/05/12 从博客园迁移至此。
