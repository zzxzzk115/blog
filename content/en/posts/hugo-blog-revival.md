---
title: Reviving My Old Blog with Hugo
date: 2026-11-17T20:00:00
tags: [Hugo, Blogging]
categories: [Jottings]
toc: true
---

After a long while, I recovered the content of my old blog and brought my favourite old theme back to life with Hugo. Here is a quick record of the current setup.

<!--more-->

## Recovering the old blog

The old blog lived on Coding, and luckily the repositories were still there: the Hexo sources and the generated site. The tricky part was the images: they were all on a Qiniu image host whose domain died long ago.

Thanks to Qiniu, the images in my old bucket could still be recovered. I downloaded them into the repository and pointed every post at the local copies, so a dead image-host domain is no longer a concern.

With that, the 2020–2022 posts moved in and were merged with the posts from the later VuePress blog.

Beyond those, I recovered a good deal more from other platforms:

- **CSDN**: 18 posts from 2017–2018, written when I was just starting to program: algorithms, data structures, C/C++, machine-learning notes and a small open-source project.
- **cnblogs**: 10 posts from 2020. Two were newly recovered; the other eight were already in the Hexo blog and now carry their original cnblogs dates.
- **Zhihu**: 2 column posts from 2023, on the Kytten engine's shader system and its C# scripting.
- **FlowUs**: 1 note from 2023, on keeping C# code quality and style consistent with Roslyn and ReSharper.

Each of these posts notes where and when it was first published.

## Bringing freemind.bithack back with Hugo

My favourite theme back then was Hexo's [freemind.bithack](https://github.com/Ares-X/hexo-theme-freemind.bithack) (itself based on freemind.386, and before that freemind). The original has a black background, green links, a DOS-style bitmap font (Fixedsys) for headings and Fira Code for body text and code: very much a terminal.

What I actually used, though, was my own modified version. Compared with the original, I had changed:

- **Colours**: the original is just black with green links. I added red: bold text in red and tables with solid red borders. That is where the later black-red-green look came from.
- **Chinese font**: the original falls back to SimHei for Chinese, so only Latin text is pixelated. I added the Founder Pixel 12 (方正像素 12) web font so Chinese was pixel art too.
- **Icons**: the original ships Font Awesome, but its menu icons are commented out. I turned them on and added an icomoon icon font for icons Font Awesome lacks, such as Bilibili.
- **Details**: a pixel-art icon for the collapsed menu button, Games, Friends and Wiki menu items, the slogan TALK IS CHEAP, SHOW ME THE CODE., and adjusted spacing for tables, images and code blocks.

This time I ported it to [Hugo](https://gohugo.io/) as [hugo-theme-freemind-bithack](https://github.com/zzxzzk115/hugo-theme-freemind-bithack) (MIT licensed, with a [live demo](https://zzxzzk115.github.io/hugo-theme-freemind-bithack/)). It recreates my modified version, not the original. Founder Pixel is a commercial font, so the Chinese pixel font is now the open-source [Fusion Pixel](https://github.com/TakWolf/fusion-pixel-font).

Why Hugo: it is a single executable. No Node, so none of the dependency-version trouble.

AI turned out to be really handy for this, since I'm not a front-end developer. The look stays as close to my old modified version as possible, while picking up what a blog should have these days: English and Chinese versions, site search, copy buttons on code, math, comments, a reader mode, and so on.

## The current setup

- **Generator**: Hugo, with the theme as a git submodule.
- **Content**: posts with the same file name under `content/zh` and `content/en` are translations of each other; the English versions of the old posts were translated with AI assistance.
- **Deployment**: pushing to GitHub triggers GitHub Actions, which builds the site and publishes it to GitHub Pages.
- **Comments**: giscus, backed by GitHub Discussions.

### Writing locally

Install Hugo:

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

The hugo in apt is usually far behind, so install the official extended `.deb` instead; on ARM, replace `amd64` with `arm64`.
{{< /tab >}}
{{< tab "Other Linux" >}}
```bash
VER=0.170.0
mkdir -p ~/.local/bin
curl -L https://github.com/gohugoio/hugo/releases/download/v${VER}/hugo_extended_${VER}_linux-amd64.tar.gz | tar -xz -C ~/.local/bin hugo
hugo version
```

Works on any distribution (Fedora, openSUSE, ...): the official extended binary, unpacked into `~/.local/bin` (make sure it is on your `PATH`). On ARM, replace `amd64` with `arm64`.
{{< /tab >}}
{{< /tabs >}}

Clone the blog repository with the theme submodule and start the local preview:

```bash
git clone --recurse-submodules https://github.com/zzxzzk115/blog.git
cd blog
hugo server
```

For a new post, a small script in the repo creates the Chinese and English files at once (same name means they are translations of each other), as drafts:

```bash
python tools/new_post.py my-new-post --zh "中文标题" --en "English title" --tags "算法" --categories "随笔"
```

In VS Code, `.vscode/` is already set up: run **Blog: new post** from the command palette and fill in the prompts, and **Blog: preview** starts a preview that includes drafts. In Markdown, type a prefix such as `alert`, `img`, `video` or `tabs` and press Tab to insert that component. When the post is done, remove `draft: true`, push to GitHub and let GitHub Actions do the rest.
