# new-blog

Lazy_V's Blog 2.0：Hugo + [freemind-bithack](themes/freemind-bithack/README.md) 主题，中英双语。
合并了此前的 VuePress 博客、2020–2022 的 Hexo 旧博客（MyBlog），以及更早的 CSDN、博客园文章。
VuePress 版本完整归档在 [zzxzzk115/vuepress-hope-blog](https://github.com/zzxzzk115/vuepress-hope-blog)（私有、只读）。

## 本地运行

只需要 [Hugo](https://gohugo.io/installation/)（Windows：`winget install Hugo.Hugo.Extended`），不需要 Node。

```bash
git submodule update --init
hugo server
```

英文版 <http://localhost:1313/>，中文版 <http://localhost:1313/zh/>。构建：`hugo --gc --minify`，输出在 `public/`。

手机预览（同一 Wi-Fi）：`python tools/serve_lan.py`（参数同 `hugo server`，如 `-D`），在电脑上打开它打印的局域网地址，点右下角“手机阅读”扫码。第一次运行 Windows 可能询问是否允许 Hugo 接受连接，在“专用网络”上允许即可。

## 写作

新建一篇（中英两份同时生成，`draft: true`，标签/分类的英文名按 `data/terms.toml` 自动对应）：

```bash
python tools/new_post.py my-new-post --zh "中文标题" --en "English title" --tags "算法, Unity" --categories "随笔" --open
```

- `--section posts/game-engine` 放到子目录；`--only zh` 只建一种语言。
- 已有的分类与标签（中英对照、篇数）见 `tools/taxonomy-plan.md`，尽量复用。全站整理改 `tools/taxonomy.py` 里的表，再 `python tools/taxonomy.py --apply`：它会一起改文章 front matter、`C#`/`C++` 这类名字的 URL 安全键与显示名页面，以及 `data/terms.toml` 的中英配对。
- 图片放 `static/img/<slug>/`，文中写 `![说明](/img/<slug>/xxx.png)`。
- 预览含草稿：`hugo server -D`；写完删掉 `draft: true` 再推送。
- 链接卡片：`python tools/linkcard.py <网址>` 抓取标题、描述和预览图（图片存到 `static/img/linkcards/`）并输出 `{{< linkcard … >}}`；`--replace 文章.md` 会把只含一个链接的行整体换成卡片，打不开的死链会保留原样并提示。
- 音乐播放器：`python tools/netease_music.py <网易云歌曲ID…>` 把标题、歌手、封面、歌词写进 `data/music.toml`，文中写 `{{< music ids="ID1, ID2" >}}`；`--all` 刷新已有的歌。
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
    tags/            名字含特殊字符的标签的显示名（C#、C++、.NET、TCP/IP、A*）
  en|zh/tags/ en|zh/categories/   只有一种语言用到的此类名字（Async I/O、Backend & Networking…）
                     这些都由 tools/taxonomy.py 生成
static/
  images/ src/ favicon.ico                   来自 VuePress .vuepress/public
  img/                                        文章图片：七牛云图床恢复的 /img/<文件名>，CSDN /img/csdn/，博客园 /img/cnblogs/ 等
  video/                                      本地托管的视频（原优酷）
  GameSrc/ GameAssets/ devterm/               来自 Hexo（网页游戏等，原样保留）
  avatar.png                                  侧边栏作者卡片的 1-bit 头像（GitHub 头像原图）
themes/freemind-bithack/   主题，git submodule（独立仓库 hugo-theme-freemind-bithack）
.github/workflows/deploy.yml  push 后用 Hugo 构建并发布到 GitHub Pages
tools/                     写作（new_post.py）、分类标签（taxonomy.py）和迁移脚本
```

**写新文章**：在 `content/en/<栏目>/` 和 `content/zh/<栏目>/` 下放同名文件，两篇自动互为翻译。只写一种语言也可以。

## URL 兼容

- VuePress 页面：`url:` front matter 保留原地址（`/posts/phd-life/openxr-simulator.html`、`/zh/...`）。部署到 `https://zzxzzk115.github.io/blog/` 时把 `baseURL` 改成该地址即可，路径会自动加 `/blog`。
- RSS 仍是 `/rss.xml`、`/zh/rss.xml`；另有 `atom.xml`。
- Hexo 时期的文章：英文译文 `/2021/01/10/astar-in-unity/`（与原 Hexo 地址一致），中文原文 `/zh/2021/01/10/astar-in-unity/`。没有写 `url` 的新文章也用这个格式。
- 分类与标签已统一整理（9 个分类、78 个标签，中英对照见 `tools/taxonomy-plan.md`）。
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

所有文章图片都在本仓库里，不依赖外部图床：

- 七牛云图床（`img.zhangkexuan.cn`）的图片已全部恢复到 `static/img/`，链接是 `/img/<文件名>`。
- CSDN 和博客园文章的图片下载到 `static/img/csdn/`、`static/img/cnblogs/`。
- 已失效外站的图片从 Wayback Machine 找回（`static/img/xuefei/`、`static/img/msf/`）。
- 原来在优酷上的寝室助手开门视频在 `static/video/dorm/`。

死链的处理：能找到替代的换成新链接或 Wayback Machine 存档，找不到的去掉链接、改成文字说明。

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

- 无。
