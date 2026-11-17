"""Bring back images from the old Qiniu image host (img.zhangkexuan.cn).

    python tools/import_images.py --list            # write tools/missing_images.md (what is still missing)
    python tools/import_images.py <folder> [...]    # copy found files into static/img/ and fix the links

Posts that still point at http://img.zhangkexuan.cn/<name> are rewritten to /img/<name> once
<name> is found in one of the given folders (searched recursively, matched by file name).
Safe to run again whenever you have downloaded more images.
"""
import re
import shutil
import sys
import urllib.parse
from collections import defaultdict
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
CONTENT = SITE / "content"
DEST = SITE / "static" / "img"
HOST = re.compile(r"https?://img\.zhangkexuan\.cn/([^\s)\"'<>]+)")


def missing():
    """{file name: set of content files that use it}"""
    out = defaultdict(set)
    for f in CONTENT.rglob("*.md"):
        for m in HOST.finditer(f.read_text(encoding="utf-8")):
            out[urllib.parse.unquote(m.group(1))].add(f.relative_to(SITE).as_posix())
    return out


def write_list():
    miss = missing()
    by_post = defaultdict(list)
    for name, files in miss.items():
        for f in files:
            by_post[f].append(name)
    lines = ["# Missing images", "",
             f"{len(miss)} images (from `http://img.zhangkexuan.cn/`) are not in `static/img/` yet.",
             "Download them (file names as listed), then run:", "",
             "```bash", "python tools/import_images.py <download folder>", "```", ""]
    for post in sorted(by_post):
        lines.append(f"## {post}")
        lines += [f"- `{n}`" for n in sorted(by_post[post])]
        lines.append("")
    out = SITE / "tools" / "missing_images.md"
    out.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(f"{len(miss)} missing images in {len(by_post)} files -> {out.relative_to(SITE)}")


def import_from(folders):
    found = {}
    for folder in folders:
        for p in Path(folder).rglob("*"):
            if p.is_file():
                found.setdefault(p.name, p)
    DEST.mkdir(parents=True, exist_ok=True)
    copied, links, files = set(), 0, 0
    for f in CONTENT.rglob("*.md"):
        t = f.read_text(encoding="utf-8")

        def rep(m):
            nonlocal links
            name = urllib.parse.unquote(m.group(1))
            src = found.get(name)
            if not src:
                return m.group(0)
            if name not in copied:
                shutil.copy2(src, DEST / name)
                copied.add(name)
            links += 1
            return "/img/" + urllib.parse.quote(name)

        t2 = HOST.sub(rep, t)
        if t2 != t:
            f.write_text(t2, encoding="utf-8", newline="\n")
            files += 1
    print(f"copied {len(copied)} images, rewrote {links} links in {files} files")
    write_list()


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args == ["--list"]:
        write_list()
    else:
        import_from(args)
