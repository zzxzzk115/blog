"""Migrate a Hexo `source/` directory into this Hugo site.

Usage:
    python tools/migrate_hexo.py <hexo-source-dir> [--lang zh] [--section posts] [--pages games] [--static-dirs wiki,GameSrc,...]

What it does:
  * source/_posts/*.md          -> content/<lang>/<section>/*.md
      - `category: X`            -> `categories: [X]`
      - `<!-- more -->`          -> `<!--more-->` (Hugo summary divider)
      - `layout:` lines dropped (the theme decides layouts)
  * source/<page>/index.md      -> content/<lang>/<page>.md   (only pages listed in --pages)
  * --static-dirs               -> copied verbatim to static/ (hexo `skip_render` dirs)

Existing files in content/ are overwritten; nothing else is touched.
"""
import argparse
import re
import shutil
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
SKIP_LAYOUTS = {"categories", "tags"}
MORE_RE = re.compile(r"<!--\s*more\s*-->")


# Term names that cannot be used as URL path segments (`#`, `/`, `&`, `+`...).
# The post keeps a URL-safe name; content/<taxonomy>/<safe>/_index.md restores the display title.
TERM_SLUGS = {"C#": "CSharp", "C++": "CPP", ".NET": "DotNET"}
RENAMED_TERMS = {}  # (taxonomy, safe) -> original


def safe_term(taxonomy: str, name: str) -> str:
    safe = TERM_SLUGS.get(name) or re.sub(r"[^\w.\-]+", "-", name, flags=re.UNICODE).strip("-")
    if safe != name:
        RENAMED_TERMS[(taxonomy, safe)] = name
    return safe


def convert_terms(taxonomy: str, val: str) -> str:
    items = [v.strip().strip("'\"") for v in val.strip("[]").split(",") if v.strip()]
    return "[" + ", ".join(safe_term(taxonomy, i) for i in items) + "]"


def write_renamed_terms(content_dir: Path):
    """content/<lang>/<taxonomy>/<safe>/_index.md restores the display title of renamed terms."""
    for (tax, safe), original in sorted(RENAMED_TERMS.items()):
        idx = content_dir / tax / safe / "_index.md"
        idx.parent.mkdir(parents=True, exist_ok=True)
        title = original.replace('"', '\\"')
        idx.write_text(f'---\ntitle: "{title}"\n---\n', encoding="utf-8")
        print(f"term {content_dir.name}/{tax}/{safe} -> \"{original}\"")
    RENAMED_TERMS.clear()


def split_front_matter(text: str):
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end < 0:
        return None, text
    fm = text[3:end].strip("\r\n")
    body = text[end + 4:].lstrip("\r\n")
    return fm, body


def convert_front_matter(fm: str):
    out, layout = [], None
    for line in fm.splitlines():
        m = re.match(r"^(\w+):\s*(.*)$", line)
        key, val = (m.group(1), m.group(2).strip()) if m else (None, None)
        if key == "layout":
            layout = val
            continue
        if key in ("date", "updated"):
            d = re.match(r"^(\d{4})-(\d{1,2})-(\d{1,2})(?:[ T](\d{1,2}):(\d{2})(?::(\d{2}))?)?$", val.strip("'\""))
            if d:
                y, mo, da, h, mi, s = (int(x or 0) for x in d.groups())
                val = f"{y:04d}-{mo:02d}-{da:02d}T{h:02d}:{mi:02d}:{s:02d}"
            out.append(f"{'lastmod' if key == 'updated' else 'date'}: {val}")
            continue
        if key in ("category", "categories", "tags") and val:
            tax = "tags" if key == "tags" else "categories"
            out.append(f"{tax}: {convert_terms(tax, val)}")
            continue
        out.append(line)
    return "\n".join(out), layout


def convert_file(src: Path, dst: Path, extra_fm: str = ""):
    text = src.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    fm, body = split_front_matter(text)
    layout = None
    if fm is not None:
        fm, layout = convert_front_matter(fm)
    else:
        fm = f"title: {src.stem}"
    if layout in SKIP_LAYOUTS:
        return f"skip (layout: {layout})"
    if extra_fm:
        fm += "\n" + extra_fm
    body = MORE_RE.sub("<!--more-->", body)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(f"---\n{fm}\n---\n\n{body}", encoding="utf-8")
    return "ok"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source", type=Path, help="Hexo source/ directory")
    ap.add_argument("--lang", default="zh", help="content/<lang>/")
    ap.add_argument("--section", default="posts")
    ap.add_argument("--pages", default="games", help="comma separated source/<page>/index.md to import")
    ap.add_argument("--static-dirs", default="", help="comma separated dirs copied to static/")
    args = ap.parse_args()
    src: Path = args.source
    if not (src / "_posts").is_dir():
        sys.exit(f"{src} does not look like a Hexo source dir (no _posts/)")
    content = SITE / "content" / args.lang

    n = 0
    for p in sorted((src / "_posts").glob("*.md")):
        convert_file(p, content / args.section / p.name)
        n += 1
    print(f"posts: {n} -> content/{args.lang}/{args.section}/")
    write_renamed_terms(content)

    for name in [x for x in args.pages.split(",") if x]:
        idx = src / name / "index.md"
        if idx.is_file():
            print(f"page {name}: {convert_file(idx, content / f'{name}.md')}")
        else:
            print(f"page {name}: not found")

    for name in sorted(d for d in args.static_dirs.split(",") if d):
        s = src / name
        if s.is_dir():
            shutil.copytree(s, SITE / "static" / name, dirs_exist_ok=True)
            print(f"static: {name}/")
        else:
            print(f"static: {name} not found, skipped")


if __name__ == "__main__":
    main()
