"""Create a new bilingual post: content/zh/<section>/<slug>.md and content/en/<section>/<slug>.md.

The two files share a path, so Hugo links them as translations. Both start as drafts
(`draft: true`), which `hugo server -D` shows and the real build skips.

usage:
  python tools/new_post.py <slug> [--zh 中文标题] [--en "English title"] [--section posts/game-engine]
                           [--tags "Unity, C#"] [--categories "游戏开发"] [--only zh|en] [--open]

  slug        file name and URL part: lowercase-words-with-dashes
  --section   folder under content/<lang>/ (default: posts)
  --tags / --categories   comma-separated, as you'd write them in the zh post; English names are
              looked up in data/terms.toml (Algorithms = 算法 ...), unknown names are copied as-is
  --only      create just one language
  --open      open the created files in VS Code
"""
import argparse, datetime, re, shutil, subprocess, sys, tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def zh_to_en_map():
    """data/terms.toml maps English -> zh; invert it per taxonomy."""
    path = ROOT / "data" / "terms.toml"
    if not path.exists():
        return {}, {}
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    inv = lambda tax: {v["zh"]: k for k, v in data.get(tax, {}).items() if "zh" in v}
    return inv("tags"), inv("categories")


def split(s):
    return [x.strip() for x in re.split(r"[,，]", s or "") if x.strip()]


def yaml_list(items):
    return "[" + ", ".join(f'"{x}"' if re.search(r"[:#\[\]{},&*!|>'\"%@`]", x) else x for x in items) + "]"


def front_matter(title, date, tags, cats, lang):
    note = {"zh": "这里写摘要，显示在首页列表里。", "en": "Summary shown in the post list goes here."}[lang]
    body = {"zh": "正文从这里开始。", "en": "The post starts here."}[lang]
    return (
        "---\n"
        f"title: '{title.replace(chr(39), chr(39) * 2)}'\n"
        f"date: {date}\n"
        f"tags: {yaml_list(tags)}\n"
        f"categories: {yaml_list(cats)}\n"
        "toc: true\n"
        "draft: true\n"
        "---\n\n"
        f"{note}\n\n<!--more-->\n\n{body}\n"
    )


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slug")
    ap.add_argument("--zh", default="")
    ap.add_argument("--en", default="")
    ap.add_argument("--section", default="posts")
    ap.add_argument("--tags", default="")
    ap.add_argument("--categories", default="")
    ap.add_argument("--only", choices=["zh", "en"])
    ap.add_argument("--open", action="store_true")
    a = ap.parse_args()

    slug = a.slug.strip().lower()
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug):
        sys.exit(f"slug should look like my-new-post (lowercase letters, digits, dashes), got: {a.slug}")
    section = a.section.strip("/\\ ").replace("\\", "/")
    date = datetime.datetime.now().replace(microsecond=0).isoformat()

    tag_map, cat_map = zh_to_en_map()
    tags_zh, cats_zh = split(a.tags), split(a.categories)
    tags_en = [tag_map.get(t, t) for t in tags_zh]
    cats_en = [cat_map.get(c, c) for c in cats_zh]

    langs = [a.only] if a.only else ["zh", "en"]
    made = []
    for lang in langs:
        path = ROOT / "content" / lang / section / f"{slug}.md"
        if path.exists():
            sys.exit(f"already exists: {path.relative_to(ROOT)}")
        title = (a.zh if lang == "zh" else a.en) or (a.en if lang == "zh" else a.zh) or slug.replace("-", " ").title()
        tags, cats = (tags_zh, cats_zh) if lang == "zh" else (tags_en, cats_en)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(front_matter(title, date, tags, cats, lang), encoding="utf-8", newline="\n")
        made.append(path)
        print("created", path.relative_to(ROOT).as_posix())

    print(f"images: put them in static/img/{slug}/ and write ![说明](/img/{slug}/xxx.png)")
    print("preview: hugo server -D   (drafts are shown; remove `draft: true` to publish)")

    if a.open:
        code = shutil.which("code") or shutil.which("code.cmd")
        if code:
            subprocess.run([code, *map(str, made)])


if __name__ == "__main__":
    main()
