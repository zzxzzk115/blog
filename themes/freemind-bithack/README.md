# freemind.bithack for Hugo

[hexo-theme-freemind.bithack](https://github.com/Ares-X/hexo-theme-freemind.bithack) 的 Hugo 移植版：外观保持原样（暗色终端风、Bootstrap 3、像素字体），构建换成 Hugo 单文件，不需要 Node。

需要 Hugo ≥ 0.146（标准版即可，无需 extended）。

## 功能

| 功能 | 实现 |
| --- | --- |
| 文章范围 | `params.mainSections` 中的栏目 |
| 首页分页、摘要 | `<!--more-->` 手动分割，否则自动摘要（`params.autoExcerpt`） |
| 归档 / 分类 / 标签 | `/archives/`（`layout: archives`）、Hugo taxonomy |
| 侧边栏 | `params.widgets` 按名字渲染 `_partials/widgets/<name>.html` |
| 站内搜索 | 生成与 hexo-generator-search 相同格式的 `search.xml`，沿用原 `search.js` |
| RSS | `rss.xml` + `atom.xml`（每种语言各一份） |
| 代码高亮 | Hugo 内置 Chroma，配色沿用原主题 |
| 数学公式 | `$…$` / `$$…$$`，构建时 KaTeX 渲染（默认 MathML，无需 JS/CSS） |
| Mermaid | ` ```mermaid ` 代码块，仅在用到的页面加载 mermaid |
| 提示框 | GitHub 风格 `> [!TIP]` / `> [!WARNING]` → Bootstrap alert |
| 图片灯箱 | 原主题 fancybox / gallery.js |
| 外链新标签页 | `params.externalLinksNewTab` |
| 评论 | `params.comments.provider = "giscus" \| "valine"` |
| 目录 | 文章 front matter `toc: true` |
| 多语言 | 导航栏语言切换（有译文跳译文，没有跳该语言首页），i18n：`en` / `zh` |
| 置顶 | `sticky: true` 的文章在首页置顶并显示 Pinned 标记 |
| 非文章页 | `article: false` 的页面不进首页、归档、RSS、最新文章 |
| 下拉菜单 | 菜单项设置 `parent` 即成为下拉子项 |
| 栏目页 | 目录的 `_index.md`：显示简介、子栏目和其下全部文章 |

## 使用

```toml
# hugo.toml
theme = "freemind-bithack"

[outputs]                       # Hugo 不会从主题合并以下三段，需要写在站点配置里
  home = ["html", "rss", "atom", "searchxml"]
[pagination]
  pagerSize = 10
[markup.goldmark.renderer]
  unsafe = true
[markup.goldmark.extensions.passthrough]
  enable = true
  [markup.goldmark.extensions.passthrough.delimiters]
    block = [["$$", "$$"]]
    inline = [["$", "$"]]
[markup.highlight]
  noClasses = false
  lineNos = true
  lineNumbersInTable = true
```

菜单用 `[[menus.main]]`，图标写在 `params.icon`（Font Awesome 4 类名）。完整示例见上层站点的 `hugo.toml`。

## 自定义组件

所有扩展都放在**站点**目录里，不需要改主题本身：

- **短代码**（在 Markdown 里用）：主题自带下面这些；在站点 `layouts/_shortcodes/xxx.html` 新建文件就能加新的短代码，同名文件会覆盖主题自带的。
  - `{{< bilibili BV1554y1D7a1 >}}`：B 站视频
  - `{{< embed src="/GameSrc/CatMarioGB/" ratio="4:3" >}}`：iframe，可嵌网页游戏
  - `{{< alert type="warning" title="注意" >}}**Markdown**{{< /alert >}}`：提示框
  - `{{< gallery >}}` 每行一个图片路径 `{{< /gallery >}}`：轮播图
  - `{{< friend name="…" url="…" desc="…" avatar="…" >}}`：友链卡片
  - `{{< tabs >}}{{< tab "macOS" >}}…{{< /tab >}}{{< tab "Linux" >}}…{{< /tab >}}{{< /tabs >}}`：标签页
  - `{{< icon folder >}}`：行内 Font Awesome 4 图标
- **侧边栏挂件**：新建 `layouts/_partials/widgets/<name>.html`，再把 `<name>` 加进 `params.widgets`。
- **渲染钩子**：`layouts/_markup/render-{link,image,blockquote,passthrough,codeblock-<lang>}.html`。比如想让 ` ```chart ` 代码块输出图表，就新建 `render-codeblock-chart.html`。
- **插入点**：`layouts/_partials/hooks/{head-end,footer-end,body-end}.html`，用来加统计脚本、自定义 JS 等。
- **样式**：站点 `assets/css/custom.css` 会自动打包进主题样式表的末尾。
