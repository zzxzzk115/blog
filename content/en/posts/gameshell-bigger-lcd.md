---
title: 'A Guide to Modding a Bigger Screen into the GameShell'
date: 2022-05-12T19:47:41
tags: [GameShell, LCD]
categories: [Retro Handhelds]
toc: true
aiTranslated: true
---

> Someone has already pulled off this mod and shared the process on GitHub. Here's the repo: https://github.com/Yvees/GameShellHacking

# Sourcing the parts

Here's what we need:

1. A 3.5-inch screen (320 x 240 or 640 x 480)
2. A 6cm 45-pin opposite-side FPC cable
3. A PCB adapter board
4. FPC connectors * 2: a 0.3mm H1.0 45P flip-lock and a 0.5mm H2.0 54P flip-lock
5. A 3D-printed front shell



There are roughly two good choices for the screen. One is Kedake's 320 x 240, [Taobao link](<https://item.taobao.com/item.htm?ut_sk=1.WOMnj8sz1t0DAFrTn0PDtX4g_21380790_1586412009068.Copy.1&id=594337582777&sourceType=item&price=15-72.9&suid=521C3937-9B73-4FE5-B065-ECE8247FC3B2&un=9394a44ddf9a362f&share_crt_v=1&spm=a2159r.13376460.0.0&sp_tk=JElVYnMxUXpnRjFEJA==&cpp=1&shareurl=true&short_name=h.VhiOBnH&sm=2da0f8&tdsourcetag=s_pctim_aiomsg&app=chrome>)

The other is this 640 x 480 from Chenchen Technology, [Taobao link](<https://item.taobao.com/item.htm?spm=a1z10.1-c-s.w4004-21816738571.7.196c4ab6nmfeKM&id=603271622592>)

Pick whichever suits you. **Make sure you tell the seller you want the 18V series version! The key word is series!**



The FPC cable: [Taobao link](<https://item.taobao.com/item.htm?spm=a1z10.3-c.w4002-16327681171.37.d71171d3Vm6TDU&id=565842370557>)



The PCB adapter board and FPC connectors need to be custom-made and soldered; of course, if you know how to solder, you can buy everything and solder it yourself.

For the PCB I recommend [this shop](), and here are the links for the two FPC connectors: [(1)](<https://item.taobao.com/item.htm?spm=a1z10.3-c.w4002-22306881049.11.681e2eeciI7LO7&id=574405341541>) [(2)](<https://item.taobao.com/item.htm?spm=a1z10.3-c.w4002-22306881049.9.5d582eecjOhlZJ&id=574402496160>)



For 3D printing, there's a shop with a student discount you could try, [Taobao link](<https://item.taobao.com/item.htm?spm=a1z10.3-c.w4002-21947488495.12.475c45caiJFXOj&id=609901366662>)



# The modding process

Once you have all the parts, follow these steps:

1. First, separate the original screen from the LCD backboard:

   ![](http://img.zhangkexuan.cn/markdown_20220512181634.png)

2. Get the front cover, the adapter board and the 6cm opposite-side 45-pin FPC cable ready:

   ![](http://img.zhangkexuan.cn/markdown_20220512181652.png)

3. Connect the ribbon cables:

   ![](http://img.zhangkexuan.cn/markdown_20220512181708.png)

   ![](http://img.zhangkexuan.cn/markdown_20220512181727.png)

   ![](http://img.zhangkexuan.cn/markdown_20220512181745.png)

4. Replace the kernel files [to be updated]:

5. Assemble the front shell, and you're done!

If you're using the 240p screen, you'll also need to apply an LCD patch.

The STL file for the 3D front shell, the PCB files and the kernel files are all in the group files of our GameShell sharing group. GameShell fans are welcome to join.

Group number: 1041399424

Photos courtesy of 梦中 (Mengzhong), a pro in our group. He's the one who did the big-screen mod you may have seen on the official forum and Xianyu (not for sale), and this tutorial is the modding process he shared. Huge thanks to him!

----

2022/05/12 Migrated here from cnblogs.
