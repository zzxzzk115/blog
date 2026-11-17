---
title: 用 Hugo 复活老博客
date: 2026-11-17T20:00:00
tags: [tutorial, record]
categories: [随笔]
toc: true
---

时隔多日，我找回了老博客的内容，还把曾经最喜欢的主题用 Hugo 复活了。顺手记录一下现在的环境。

<!--more-->

## 找回老博客

老博客当年放在 Coding 上，好在仓库还在：Hexo 的源码、生成好的站点都在里面。比较麻烦的是图片——文章里的图都放在七牛云图床上，原来的域名早就失效了。

感谢七牛云，我的老图床里的图片还能找回来。把图片下载回来之后放进仓库，再把文章里的链接统一换成站内路径，以后就不用再担心图床域名的问题了。

这样，2020–2022 年的文章都搬了进来，和后来 VuePress 博客上的文章合并到了一起。

## 用 Hugo 复活 freemind.bithack

我曾经最喜欢的主题是 Hexo 的 [freemind.bithack](https://github.com/Ares-X/hexo-theme-freemind.bithack)：黑底、像素字体、终端风格。这次我把它移植到了 [Hugo](https://gohugo.io/)，做成了 [hugo-theme-freemind-bithack](https://github.com/zzxzzk115/hugo-theme-freemind-bithack)（MIT 开源，有 [在线示例](https://zzxzzk115.github.io/hugo-theme-freemind-bithack/)）。

选 Hugo 的原因很简单：它就是一个可执行文件，不需要 Node，也就没有那些依赖版本的问题。

在这一点上，使用 AI 倒是挺方便的，毕竟我不是前端程序员。外观尽量保持原样，同时补上了这些年博客该有的东西：中英双语、站内搜索、代码复制、数学公式、评论、纯享阅读模式等等。

## 现在的环境

- **生成器**：Hugo，主题以 git submodule 的形式引入。
- **内容**：`content/zh` 和 `content/en` 下同名的文章互为翻译；旧文章的英文版是 AI 辅助翻译的。
- **部署**：推送到 GitHub 后，GitHub Actions 自动构建并发布到 GitHub Pages。
- **评论**：giscus，基于 GitHub Discussions。

### 本地写作

安装 Hugo（Windows 上用 winget，macOS 上用 Homebrew）：

```bash
winget install Hugo.Hugo.Extended
# macOS
brew install hugo
```

拉取博客仓库（带上主题子模块），然后启动本地预览：

```bash
git clone --recurse-submodules https://github.com/zzxzzk115/blog.git
cd blog
hugo server
```

写新文章时，在 `content/zh/posts/` 和 `content/en/posts/` 下各放一个同名的 Markdown 文件，就会自动成为中英文互译的两篇。写完推送到 GitHub，剩下的交给 GitHub Actions。
