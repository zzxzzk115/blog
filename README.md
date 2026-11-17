# new-blog

Lazy_V's Blog 2.0：Hugo + [freemind-bithack](themes/freemind-bithack/README.md) 主题，中英双语。
合并了现在的 VuePress 博客（zzxzzk115/blog）和 2020–2022 的 Hexo 旧博客（MyBlog）。

## 本地运行

只需要 [Hugo](https://gohugo.io/installation/)（Windows：`winget install Hugo.Hugo.Extended`），不需要 Node。

```bash
hugo server
```

英文版 <http://localhost:1313/>，中文版 <http://localhost:1313/zh/>。构建：`hugo --gc --minify`，输出在 `public/`。

## 目录结构

```
config/_default/
  hugo.toml          站点全局（语言默认值、URL 规则、输出格式）
  languages.toml     en / zh 的标题、描述
  module.toml        content/en、content/zh、content/shared 分别挂载到哪种语言
  menus.en.toml      英文导航
  menus.zh.toml      中文导航
  params.toml        主题参数（mainSections、侧边栏、链接、评论）
  markup.toml        Markdown / 代码高亮 / 数学公式
content/
  en/                英文，站点根路径 /
    posts/ game-dev/ hpg-notes/     文章（按主题分目录，目录的 _index.md 即栏目页）
    intro.md friends.md archives.md
  zh/                中文，/zh/
    posts/ game-dev/ hpg-notes/     与 en 一一对应的译文（同路径 = 互为翻译）
    intro.md friends.md archives.md
  shared/            同时挂载到两种语言（config/_default/module.toml）
    posts/           2020–2022 的 Hexo 文章（中文），URL：/2021/01/10/slug/ 与 /zh/2021/01/10/slug/
    games.md tags/
static/
  images/ src/ logo.png bg.png favicon.ico    来自 VuePress .vuepress/public
  wiki/ GameSrc/ GameAssets/ devterm/         来自 Hexo（原样的静态页面 / 网页游戏）
themes/freemind-bithack/   主题（可独立成仓库）
tools/                     迁移脚本
```

**写新文章**：在 `content/en/<栏目>/` 和 `content/zh/<栏目>/` 下放同名文件，两篇自动互为翻译。只写一种语言也可以。

## URL 兼容

- VuePress 页面：`url:` front matter 保留原地址（`/posts/phd-life/openxr-simulator.html`、`/zh/...`）。部署到 `https://zzxzzk115.github.io/blog/` 时把 `baseURL` 改成该地址即可，路径会自动加 `/blog`。
- RSS 仍是 `/rss.xml`、`/zh/rss.xml`；另有 `atom.xml`。
- Hexo 时期的文章：英文侧 `/2021/01/10/astar-in-unity/`（与原 Hexo 地址一致），中文侧 `/zh/2021/01/10/astar-in-unity/`。没有写 `url` 的新文章也用这个格式。
- 分类 / 标签页地址变了：VuePress 的 `/category/xxx/` 改为 `/categories/xxx/`。

## 迁移脚本

```bash
python tools/migrate_vuepress.py <blog 仓库>/src
python tools/migrate_hexo.py <MyBlog hexo 分支>/hexo/source --static-dirs wiki,GameSrc,GameAssets,devterm
```

会覆盖 `content/` 中的同名文件。转换细节见脚本开头的说明。迁移后的 `content/` 就是新的源文件，以后直接在这里改，不必再重新跑脚本。

迁移后手工修过的地方：

- `content/zh/game-dev/retro/gameboy/gbdk/002-gbdk-preparation.md`：原文 `::: tip`（"MacOS 和 Linux 需要准备 Wine 环境"）缺少结束的 `:::`，已补上（英文版本来就是闭合的）。

## 待办

- [ ] `img.zhangkexuan.cn`（七牛云）图片约 295 处失效，需要下载原图后替换链接
- [ ] 评论系统选型（giscus？）
- [ ] 部署：GitHub Actions 构建 → GitHub Pages，替换 zzxzzk115/blog
