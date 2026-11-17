# new-blog

Lazy_V's Blog 2.0：Hugo + [freemind-bithack](themes/freemind-bithack/README.md) 主题，中英双语。
合并了现在的 VuePress 博客（zzxzzk115/blog）和 2020–2022 的 Hexo 旧博客（MyBlog）。

## 本地运行

只需要 [Hugo](https://gohugo.io/installation/)（Windows：`winget install Hugo.Hugo.Extended`），不需要 Node。

```bash
git submodule update --init
hugo server
```

英文版 <http://localhost:1313/>，中文版 <http://localhost:1313/zh/>。构建：`hugo --gc --minify`，输出在 `public/`。

## 写作

新建一篇（中英两份同时生成，`draft: true`，标签/分类的英文名按 `data/terms.toml` 自动对应）：

```bash
python tools/new_post.py my-new-post --zh "中文标题" --en "English title" --tags "算法, Unity" --categories "随笔" --open
```

- `--section posts/game-engine` 放到子目录；`--only zh` 只建一种语言。
- 图片放 `static/img/<slug>/`，文中写 `![说明](/img/<slug>/xxx.png)`。
- 预览含草稿：`hugo server -D`；写完删掉 `draft: true` 再推送。
- 只建一个文件也可以用 Hugo 自带的：`hugo new content content/zh/posts/xxx.md`（模板在 `archetypes/default.md`）。

VS Code（`.vscode/` 已配好，无需插件）：

- `Ctrl+Shift+P` → `Tasks: Run Task` → **Blog: new post**（依次填 slug、标题、目录、标签）、**Blog: preview (with drafts)**（也是 `Ctrl+Shift+B`）、**Blog: build**。
- Markdown 里输入前缀按 Tab：`more` `alert` `img` `code` `video` `bilibili` `gallery` `tabs` `badge` `pdf` `math` `mermaid` `friend`。

## 目录结构

```
config/_default/
  hugo.toml          站点全局（语言默认值、URL 规则、输出格式）
  languages.toml     en / zh 的标题、描述
  module.toml        content/en、content/zh、content/shared 分别挂载到哪种语言
  menus.en.toml      英文导航
  menus.zh.toml      中文导航
  params.toml        主题参数（mainSections、侧边栏、作者卡片、社交链接、评论、编辑链接）
  markup.toml        Markdown / 代码高亮 / 数学公式 / ==mark== 等扩展
content/
  en/                英文，站点根路径 /
    posts/ game-dev/ hpg-notes/     文章（按主题分目录，目录的 _index.md 即栏目页）
                     posts/*.md 根目录：2020–2022 的 Hexo 文章（AI 翻译，aiTranslated: true）
    intro.md friends.md archives.md
  zh/                中文，/zh/
    posts/ game-dev/ hpg-notes/     与 en 一一对应的译文（同路径 = 互为翻译）
                     posts/*.md 根目录：2020–2022 的 Hexo 文章原文，URL /zh/2021/01/10/slug/
    intro.md friends.md archives.md
  shared/            同时挂载到两种语言（config/_default/module.toml）
    tags/            含特殊字符的标签显示名（C#、TCP/IP…）
static/
  images/ src/ logo.png bg.png favicon.ico    来自 VuePress .vuepress/public
  img/                                        七牛云图床（img.zhangkexuan.cn）恢复的图片，文章里是 /img/<文件名>
  GameSrc/ GameAssets/ devterm/               来自 Hexo（网页游戏等，原样保留）
  avatar.png                                  侧边栏作者卡片的 1-bit 头像（GitHub 头像原图）
themes/freemind-bithack/   主题，git submodule（独立仓库 hugo-theme-freemind-bithack）
.github/workflows/deploy.yml  push 后用 Hugo 构建并发布到 GitHub Pages
tools/                     迁移脚本
```

**写新文章**：在 `content/en/<栏目>/` 和 `content/zh/<栏目>/` 下放同名文件，两篇自动互为翻译。只写一种语言也可以。

## URL 兼容

- VuePress 页面：`url:` front matter 保留原地址（`/posts/phd-life/openxr-simulator.html`、`/zh/...`）。部署到 `https://zzxzzk115.github.io/blog/` 时把 `baseURL` 改成该地址即可，路径会自动加 `/blog`。
- RSS 仍是 `/rss.xml`、`/zh/rss.xml`；另有 `atom.xml`。
- Hexo 时期的文章：英文译文 `/2021/01/10/astar-in-unity/`（与原 Hexo 地址一致），中文原文 `/zh/2021/01/10/astar-in-unity/`。没有写 `url` 的新文章也用这个格式。
- 分类按现在博客的体系重新归类，另加 Systems Programming / 系统编程、Retro Handhelds / 复古掌机、Security / 安全（映射见 `tools/legacy_categories.py`）。
- 分类 / 标签页地址变了：VuePress 的 `/category/xxx/` 改为 `/categories/xxx/`。

## 迁移脚本

```bash
python tools/migrate_vuepress.py <blog 仓库>/src
python tools/migrate_hexo.py <MyBlog hexo 分支>/hexo/source --static-dirs wiki,GameSrc,GameAssets,devterm
```

会覆盖 `content/` 中的同名文件。转换细节见脚本开头的说明。迁移后的 `content/` 就是新的源文件，以后直接在这里改，不必再重新跑脚本。

迁移后手工修过的地方：

- `content/zh/game-dev/retro/gameboy/gbdk/002-gbdk-preparation.md`：原文 `::: tip`（"MacOS 和 Linux 需要准备 Wine 环境"）缺少结束的 `:::`，已补上（英文版本来就是闭合的）。

## 图片

七牛云备份中找到的 190 张已放进 `static/img/`，文章链接改成 `/img/<文件名>`。备份只到 2021-02，
以下文章的 110 张图片（2021-07 ~ 2022-05 上传）不在备份里，仍是原来的 `http://img.zhangkexuan.cn/...` 地址：
games、gameshell-bigger-lcd、how-to-play-gameshell-01、learn-from-pilot-01/02/03、pocketchip-love2d、
pocketchip-stero-speaker、run-godot-game-on-gameshell（41 张）、tcpip-notes、unix-socket-api、win32multithreading02。
找到后放进 `static/img/` 并把链接改成 `/img/<文件名>` 即可：

```bash
grep -rl "img.zhangkexuan.cn" content
```

## 已合并 / 移除

- 友链：新旧合并为一页（去掉已失效的站点）。
- 游戏：旧"在线游玩"页并入 Games Gallery（本站可直接玩 CatMarioGB）。
- 侧边栏：链接挂件并入作者卡片（GitHub、B 站、itch.io、个人主页、QQ、邮箱、微信、RSS）。
- About：只保留现在的 intro。
- Wiki：已移除。

## 评论

沿用 VuePress 博客的 giscus（`zzxzzk115/blog` 的 Announcements 分类，按 pathname 匹配）。
部署到 `https://zzxzzk115.github.io/blog/` 后页面路径与原来一致，已有评论会自动对上。

## 部署

1. 仓库 Settings → Pages → Source 选 **GitHub Actions**。
2. push 到 `master`（或 `main`），`deploy.yml` 会安装 Hugo、拉取主题 submodule、按 Pages 地址设置 `baseURL` 构建并发布。

## 待办

- [ ] 找回 2021-07 之后的图床图片（见上）
