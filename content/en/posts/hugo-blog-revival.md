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

## Bringing freemind.bithack back with Hugo

My favourite theme back then was Hexo's [freemind.bithack](https://github.com/Ares-X/hexo-theme-freemind.bithack): black background, pixel fonts, terminal style. This time I ported it to [Hugo](https://gohugo.io/) as [hugo-theme-freemind-bithack](https://github.com/zzxzzk115/hugo-theme-freemind-bithack) (MIT licensed, with a [live demo](https://zzxzzk115.github.io/hugo-theme-freemind-bithack/)).

Why Hugo: it is a single executable. No Node, so none of the dependency-version trouble.

AI turned out to be really handy for this, since I'm not a front-end developer. The look stays as close to the original as possible, while picking up what a blog should have these days: English and Chinese versions, site search, copy buttons on code, math, comments, a reader mode, and so on.

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
