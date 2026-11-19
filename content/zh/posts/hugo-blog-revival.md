---
title: 用 Hugo 复活老博客
date: 2026-11-17T20:00:00
tags: [Hugo, 博客]
categories: [随笔]
toc: true
---

时隔多日，我找回了老博客的内容，还把曾经最喜欢的主题用 Hugo 复活了。顺手记录一下现在的环境。

<!--more-->

## 找回老博客

老博客当年放在 Coding 上，好在仓库还在：Hexo 的源码、生成好的站点都在里面。比较麻烦的是图片——文章里的图都放在七牛云图床上，原来的域名早就失效了。

感谢七牛云，我的老图床里的图片还能找回来。把图片下载回来之后放进仓库，再把文章里的链接统一换成站内路径，以后就不用再担心图床域名的问题了。

这样，2020–2022 年的文章都搬了进来，和后来 VuePress 博客上的文章合并到了一起。

除了 2020 年以后的这些，我还从别的平台找回了不少内容：

- **CSDN**：2017–2018 年刚学编程时写的 18 篇，算法、数据结构、C/C++、机器学习笔记，还有一个开源小项目；
- **博客园**：2020 年的 10 篇，其中 2 篇是新找回的，另外 8 篇本来就在 Hexo 博客里，这次按博客园上的发布时间校正了日期；
- **知乎**：2023 年专栏里的 2 篇，讲 Kytten 引擎的 Shader 系统和 C# 脚本系统；
- **FlowUs**：2023 年的 1 篇笔记，用 Roslyn 和 ReSharper 保证 C# 代码质量与规范一致。

这些文章开头都注明了原始出处和写作时间。

## 用 Hugo 复活 freemind.bithack

我曾经最喜欢的主题是 Hexo 的 [freemind.bithack](https://github.com/Ares-X/hexo-theme-freemind.bithack)（它改自 freemind.386，再往上是 freemind）。原版是黑底、绿色链接，标题等处用 DOS 风格的点阵字体（Fixedsys），正文和代码用 Fira Code，终端味十足。

不过我当年用的并不是原版，而是自己魔改过的版本。和原版对比，主要改了这些：

- **配色**：原版只有黑底和绿色链接。我加了红色：加粗文字改成红色，表格改成红色实线边框，于是才有了后来“黑、红、绿”的样子。
- **中文字体**：原版的中文落回黑体，只有英文是点阵字。我接入了方正像素 12 的网络字体，让中文也成了像素风。
- **图标**：原版自带 Font Awesome，但菜单图标默认是注释掉的。我把菜单图标都打开了，又引入了一套 icomoon 图标字体，补上 Font Awesome 里没有的 B 站等图标。
- **其他细节**：导航栏的折叠按钮换成了像素风图标，菜单加了 Games、Friends、Wiki，slogan 改成 TALK IS CHEAP, SHOW ME THE CODE.，表格、图片和代码块的间距也调过。

这次我把它移植到了 [Hugo](https://gohugo.io/)，做成了 [hugo-theme-freemind-bithack](https://github.com/zzxzzk115/hugo-theme-freemind-bithack)（MIT 开源，有 [在线示例](https://zzxzzk115.github.io/hugo-theme-freemind-bithack/)）。复刻的是我魔改后的样子，而不是原版；方正像素是商业字体，中文像素字体换成了开源的 [Fusion Pixel](https://github.com/TakWolf/fusion-pixel-font)。

后来又发现一个问题：Fixedsys 并不是真正对齐像素网格的字体，方正像素和 Fusion Pixel 也只有在 12px 的整数倍下才清晰，在高分屏或 Windows 缩放下文字边缘都会发虚。所以这个博客现在全站换成了 [Zpix（最像素）](https://github.com/SolidZORO/zpix-pixel-font)：中英文、正文、标题、代码块都是同一套 12px 像素字形，按 16 / 24 / 32 / 40px 几档字号显示，在 150% 缩放和手机上完全像素对齐，其他缩放下也只是轻微柔化。Zpix 对个人项目免费，但不允许修改、拆分或随意分发，所以它只放在这个博客里；主题本身只提供一个通用的「站点像素字体」选项，默认仍然是开源字体。

选 Hugo 的原因很简单：它就是一个可执行文件，不需要 Node，也就没有那些依赖版本的问题。

在这一点上，使用 AI 倒是挺方便的，毕竟我不是前端程序员。外观尽量保持当年魔改版的样子，同时补上了这些年博客该有的东西：中英双语、站内搜索、代码复制、数学公式、评论、纯享阅读模式等等。

## 现在的环境

- **生成器**：Hugo，主题以 git submodule 的形式引入。
- **内容**：`content/zh` 和 `content/en` 下同名的文章互为翻译；旧文章的英文版是 AI 辅助翻译的。
- **部署**：推送到 GitHub 后，GitHub Actions 自动构建并发布到 GitHub Pages。
- **评论**：giscus，基于 GitHub Discussions。

### 本地写作

安装 Hugo：

{{< tabs >}}
{{< tab "Windows" >}}
```powershell
winget install Hugo.Hugo.Extended
```
{{< /tab >}}
{{< tab "macOS" >}}
```bash
brew install hugo
```
{{< /tab >}}
{{< tab "Arch" >}}
```bash
sudo pacman -S hugo
```
{{< /tab >}}
{{< tab "Debian / Ubuntu" >}}
```bash
VER=0.170.0
wget https://github.com/gohugoio/hugo/releases/download/v${VER}/hugo_extended_${VER}_linux-amd64.deb
sudo dpkg -i hugo_extended_${VER}_linux-amd64.deb
```

apt 源里的 hugo 往往旧很多，直接装官方的 extended 版 `.deb`；ARM 机器把 `amd64` 换成 `arm64`。
{{< /tab >}}
{{< tab "其他 Linux" >}}
```bash
VER=0.170.0
mkdir -p ~/.local/bin
curl -L https://github.com/gohugoio/hugo/releases/download/v${VER}/hugo_extended_${VER}_linux-amd64.tar.gz | tar -xz -C ~/.local/bin hugo
hugo version
```

适用于任何发行版（Fedora、openSUSE 等）：官方的 extended 版二进制，解压到 `~/.local/bin`（确保它在 `PATH` 里）。ARM 机器把 `amd64` 换成 `arm64`。
{{< /tab >}}
{{< /tabs >}}

拉取博客仓库（带上主题子模块），然后启动本地预览：

```bash
git clone --recurse-submodules https://github.com/zzxzzk115/blog.git
cd blog
hugo server
```

写新文章用仓库里的小脚本，一次生成中英两份同名文件（同名即互为译文），默认是草稿：

```bash
python tools/new_post.py my-new-post --zh "中文标题" --en "English title" --tags "算法" --categories "随笔"
```

用 VS Code 的话，仓库里的 `.vscode/` 已经配好了：命令面板里运行 **Blog: new post** 按提示填写即可，**Blog: preview** 启动带草稿的预览；Markdown 里输入 `alert`、`img`、`video`、`tabs` 等前缀按 Tab 就能插入对应组件。写完删掉 `draft: true`，推送到 GitHub，剩下的交给 GitHub Actions。
