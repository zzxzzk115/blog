# new-blog

Lazy_V's Blog 的 Hugo 版本，主题见 [themes/freemind-bithack](themes/freemind-bithack/README.md)。

## 本地运行

只需要 [Hugo](https://gohugo.io/installation/)（Windows：`winget install Hugo.Hugo.Extended`）。

```bash
hugo server
```

打开 <http://localhost:1313>。构建静态文件：`hugo --gc --minify`，输出在 `public/`。

## 内容来源

| 目录 | 来源 |
| --- | --- |
| `content/posts/` | oldblog-MyBlog `hexo` 分支 `hexo/source/_posts`（46 篇） |
| `content/{about,friends,games}.md` | 同上 `hexo/source/<page>/index.md` |
| `static/{wiki,GameSrc,GameAssets,devterm,test}` | 同上，hexo `skip_render` 的目录原样拷贝 |

重新导入（会覆盖 `content/` 中的同名文件）：

```bash
python tools/migrate_hexo.py <hexo 的 source 目录> --static-dirs wiki,test,GameSrc,GameAssets,devterm
```

导入时做的转换：`category:` → `categories:`；日期规范化；`<!-- more -->` → `<!--more-->`；含 `# / & +` 的标签改成 URL 安全名（如 `C#` → `/tags/CSharp/`），显示名用 `content/tags/<名字>/_index.md` 保留。

## 待办

- [ ] `img.zhangkexuan.cn`（七牛云）图片约 295 处失效，需要下载原图后替换链接
- [ ] 合并 oldblog-zzxzzk115（8 篇）和 zzxzzk115/blog（VuePress，约 125 个 md）
- [ ] 评论系统选型（Valine/LeanCloud 已不推荐，可换 giscus）
