"""Migrate a VuePress (vuepress-theme-hope) `src/` directory into this Hugo site.

Usage:
    python tools/migrate_vuepress.py <vuepress-src-dir> [--zh-prefix zh]

Layout mapping:
  src/<path>.md          -> content/en/<path>.md
  src/zh/<path>.md       -> content/zh/<path>.md
  .../README.md          -> .../_index.md          (section page)
  src/README.md          -> skipped                (hope's hero home page; the theme has its own)
  src/.vuepress/public/* -> static/*

Every regular page gets `url:` set to its old VuePress URL (e.g. /posts/x/y.html), so links keep working.

Front matter:
  category / tag         -> categories / tags (with URL-safe names, see migrate_hexo.TERM_SLUGS)
  order                  -> weight (section pages only)
  sticky, star, article, description, author, date, title   kept
  icon, index, isOriginal, layout, home, hero*, footer, projects, bgImage, tagline   dropped
  math: true             added when the body contains $...$

Markdown (outside code fences):
  ::: tip|info|note|warning|danger|caution [Title]  ...  :::  -> {{< alert >}}
  ::: details [Title] ... :::                                  -> <details>
  ::: tabs / @tab Label / :::                                  -> {{< tabs >}} {{< tab >}}
  <FontIcon icon="x" />                                        -> {{< icon x >}}
  <FriendLinks :friends="[{name, link, desc, avatar}]" />      -> {{< friend >}} cards
  <!-- more -->                                                -> <!--more-->
"""
import argparse
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from migrate_hexo import RENAMED_TERMS, safe_term, write_renamed_terms  # noqa: E402

SITE = Path(__file__).resolve().parent.parent
DROP_KEYS = {"icon", "index", "isOriginal", "layout", "home", "heroImage", "heroText",
             "heroFullScreen", "footer", "projects", "bgImage", "tagline", "dir"}
ALERT_TYPES = {"tip": "success", "info": "info", "note": "info", "important": "info",
               "warning": "warning", "danger": "danger", "caution": "danger"}
FENCE_RE = re.compile(r"^(\s*)(`{3,}|~{3,})")
CONTAINER_OPEN_RE = re.compile(r"^(\s*):::+\s*([a-zA-Z-]+)\s*(.*?)\s*$")
CONTAINER_CLOSE_RE = re.compile(r"^(\s*):::+\s*$")


# ---------------------------------------------------------------- front matter
def parse_front_matter(text):
    """Tiny YAML subset: `key: value`, `key:` + `  - item` lists, comments ignored."""
    if not text.startswith("---"):
        return {}, [], text
    end = text.find("\n---", 3)
    fm_text, body = text[3:end], text[end + 4:].lstrip("\n")
    data, order, key = {}, [], None
    for line in fm_text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            order.append(key)
            data[key] = val if val else []
            continue
        m = re.match(r"^\s+-\s*(.*)$", line)
        if m and key and isinstance(data.get(key), list):
            data[key].append(m.group(1).strip().strip("'\""))
    return data, order, body


def yaml_scalar(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    s = str(v)
    if s in ("true", "false") or re.fullmatch(r"-?\d+(\.\d+)?", s) or re.fullmatch(r"\d{4}-\d{2}-\d{2}T[\d:]+", s):
        return s
    if s.startswith(("'", '"')):
        return s
    if re.search(r"[:#\[\]{}&*!|>%@`,]", s) or s != s.strip():
        return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return s


def norm_date(v):
    m = re.match(r"^(\d{4})-(\d{1,2})-(\d{1,2})(?:[ T](\d{1,2}):(\d{2})(?::(\d{2}))?)?$", str(v).strip("'\""))
    if not m:
        return v
    y, mo, d, h, mi, s = (int(x or 0) for x in m.groups())
    return f"{y:04d}-{mo:02d}-{d:02d}T{h:02d}:{mi:02d}:{s:02d}"


def as_list(v):
    if isinstance(v, list):
        return v
    v = str(v).strip()
    if v.startswith("["):
        return [x.strip().strip("'\"") for x in v.strip("[]").split(",") if x.strip()]
    return [v.strip("'\"")] if v else []


def build_front_matter(data, order, url, body):
    out = []
    for key in order:
        val = data[key]
        if key in DROP_KEYS:
            continue
        if key in ("category", "categories", "tag", "tags"):
            tax = "tags" if key.startswith("tag") else "categories"
            items = [safe_term(tax, x) for x in as_list(val)]
            if items:
                out.append(f"{tax}: [{', '.join(yaml_scalar(i) for i in items)}]")
            continue
        if key == "order":
            # hope uses `order` for sidebar position; only meaningful for section pages here.
            # On articles a weight would override date sorting everywhere in Hugo.
            if url is None:
                out.append(f"weight: {val}")
            continue
        if key == "date":
            out.append(f"date: {norm_date(val)}")
            continue
        if isinstance(val, list):
            if val:
                out.append(f"{key}: [{', '.join(yaml_scalar(i) for i in val)}]")
            continue
        out.append(f"{key}: {val}")
    if url:
        out.append(f"url: {url}")
    if "math" not in data and re.search(r"\$\$|(?<![\\$])\$[^$\s][^$\n]*\$", strip_code(body)):
        out.append("math: true")
    return "---\n" + "\n".join(out) + "\n---\n\n"


# ---------------------------------------------------------------- body
def strip_code(body):
    return re.sub(r"```.*?```", "", body, flags=re.S)


def parse_friends(attr):
    friends = []
    for obj in re.findall(r"\{(.*?)\}", attr, flags=re.S):
        f = dict(re.findall(r"(\w+)\s*:\s*'([^']*)'", obj))
        f.update(re.findall(r'(\w+)\s*:\s*"([^"]*)"', obj))
        if f:
            friends.append(f)
    return friends


def friend_shortcodes(m):
    lines = []
    for f in parse_friends(m.group(1)):
        args = " ".join(f'{k}="{f.get(src, "")}"' for k, src in
                        (("name", "name"), ("url", "link"), ("desc", "desc"), ("avatar", "avatar")))
        lines.append("{{< friend " + args + " >}}")
    return "\n".join(lines)


def convert_body(body):
    body = MORE.sub("<!--more-->", body)
    body = re.sub(r'<FriendLinks\s+:friends="(.*?)"\s*/>', friend_shortcodes, body, flags=re.S)

    out, stack, fence = [], [], None
    for line in body.split("\n"):
        fm = FENCE_RE.match(line)
        if fence:
            if fm and fm.group(2)[0] == fence[0] and len(fm.group(2)) >= len(fence):
                fence = None
            out.append(line)
            continue
        if fm:
            fence = fm.group(2)
            out.append(line)
            continue

        line = re.sub(r'<FontIcon\s+icon="([^"]+)"\s*/>', r'{{< icon "\1" >}}', line)

        mo = CONTAINER_OPEN_RE.match(line)
        if mo and not CONTAINER_CLOSE_RE.match(line):
            indent, kind, title = mo.groups()
            kind = kind.lower()
            if kind == "tabs":
                stack.append(("tabs", False))
                out.append(f"{indent}{{{{< tabs >}}}}")
                continue
            if kind == "details":
                stack.append(("details", None))
                out.append(f"{indent}<details><summary>{title or 'Details'}</summary>\n")
                continue
            if kind in ALERT_TYPES:
                stack.append(("alert", None))
                t = f' title="{title}"' if title else ""
                out.append(f'{indent}{{{{< alert type="{ALERT_TYPES[kind]}"{t} >}}}}')
                continue
        if CONTAINER_CLOSE_RE.match(line) and stack:
            indent = CONTAINER_CLOSE_RE.match(line).group(1)
            kind, tab_open = stack.pop()
            if kind == "tabs":
                if tab_open:
                    out.append(f"{indent}{{{{< /tab >}}}}")
                out.append(f"{indent}{{{{< /tabs >}}}}")
            elif kind == "details":
                out.append(f"\n{indent}</details>")
            else:
                out.append(f"{indent}{{{{< /alert >}}}}")
            continue
        mt = re.match(r"^(\s*)@tab(?::active)?\s+(.*)$", line)
        if mt and stack and stack[-1][0] == "tabs":
            indent, label = mt.groups()
            if stack[-1][1]:
                out.append(f"{indent}{{{{< /tab >}}}}")
            stack[-1] = ("tabs", True)
            label = label.strip().replace('"', '\\"')
            out.append(f'{indent}{{{{< tab "{label}" >}}}}')
            continue
        out.append(line)
    if stack:
        # markdown-it-container lets an unclosed container run to the end of the file; do the same.
        print(f"  warning: {len(stack)} unclosed ::: container(s), closed at end of file")
        for kind, tab_open in reversed(stack):
            if kind == "tabs":
                out.extend(["{{< /tab >}}"] if tab_open else [])
                out.append("{{< /tabs >}}")
            elif kind == "details":
                out.append("\n</details>")
            else:
                out.append("{{< /alert >}}")
    return "\n".join(out)


MORE = re.compile(r"<!--\s*more\s*-->")


# ---------------------------------------------------------------- main
def old_url(rel: Path, lang_prefix: str):
    parts = rel.with_suffix("").as_posix()
    return f"/{lang_prefix}{parts}.html"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source", type=Path, help="VuePress src/ directory")
    ap.add_argument("--zh-prefix", default="zh")
    args = ap.parse_args()
    src: Path = args.source
    if not (src / ".vuepress").is_dir():
        sys.exit(f"{src} does not look like a VuePress src dir (no .vuepress/)")

    files = {"en": [], "zh": []}
    for md in sorted(src.rglob("*.md")):
        rel = md.relative_to(src)
        if rel.parts[0] == ".vuepress":
            continue
        if rel.parts[0] == args.zh_prefix:
            files["zh"].append((md, Path(*rel.parts[1:])))
        else:
            files["en"].append((md, rel))

    for lang, items in files.items():
        for md, rel in items:
            migrate_page(md, rel, lang)
        print(f"pages: {lang}={len(items)}")
        write_renamed_terms(SITE / "content" / lang)

    pub = src / ".vuepress" / "public"
    if pub.is_dir():
        shutil.copytree(pub, SITE / "static", dirs_exist_ok=True)
        print("static: .vuepress/public/* -> static/")


def migrate_page(md: Path, rel: Path, lang: str):
        if rel.as_posix() == "README.md":
            return  # hero home page
        text = md.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
        data, order, body = parse_front_matter(text)
        is_index = rel.name == "README.md"
        dst_rel = rel.with_name("_index.md") if is_index else rel
        # A custom `url` is not prefixed with the language by Hugo, so add /zh/ ourselves.
        url = None if is_index else old_url(rel, "" if lang == "en" else f"{lang}/")
        out = build_front_matter(data, order, url, body) + convert_body(body)
        dst = SITE / "content" / lang / dst_rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(out, encoding="utf-8")


if __name__ == "__main__":
    main()
