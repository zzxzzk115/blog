"""Insert a space between CJK characters and Latin letters / digits in Markdown prose
("pangu" spacing):  使用Unity开发2D游戏  ->  使用 Unity 开发 2D 游戏

Usage:
    python tools/cjk_spacing.py [--check] [paths...]     (default: content/)

Only prose is changed. Untouched: fenced code blocks, inline `code`, link / image URLs,
raw URLs, $math$, HTML tags, Hugo shortcodes, and front matter (except title / description).
No space is added next to full-width punctuation (，。：（）…), only between CJK ideographs/kana
and ASCII letters, digits or inline elements (`code`, [links](…), $math$).
--check lists files that would change without writing them.
"""
import re
import sys
from pathlib import Path

CJK = r"⺀-⻿⼀-⿟぀-ゟ゠-ヿ㄀-ㄯ㈀-㋿㐀-䶿一-鿿豈-﫿"
CJK_CH = re.compile(f"[{CJK}]")
# Latin "word" characters that want a space next to CJK. Trailing # + % keep C# / C++ / 50% together.
LATIN_START = r"[A-Za-z0-9`\[$@]"
LATIN_END = r"(?:[A-Za-z0-9][#+%]*|[`\]\)$%])"
EMPH = r"(?:\*{1,3}|_{1,3}|~~)?"

# Protected inline spans: replaced by placeholders, then restored.
PROTECT = re.compile(
    r"(`+)(?:.+?)\1"                       # inline code
    r"|\{\{[<%].*?[%>]\}\}"                # shortcodes
    r"|<[A-Za-z/!][^>]*>"                  # html tags / comments / autolinks
    r"|!?\[(?:[^\]\\]|\\.)*\]\([^)\s]*(?:\s+\"[^\"]*\")?\)"   # links / images (text handled separately)
    r"|https?://[^\s<>()\[\]，。、；：！？]+"  # bare URLs
    r"|\$\$.+?\$\$|\$[^$\s][^$]*?\$"       # math
)


def space_text(s):
    s = re.sub(f"([{CJK}])({EMPH})(?={LATIN_START})", r"\1 \2", s)
    s = re.sub(f"({LATIN_END})({EMPH})(?=[{CJK}])", r"\1\2 ", s)
    return s


def space_line(line):
    spans = []

    def keep(m):
        tok = m.group(0)
        # links: also space the link text itself
        lm = re.match(r"(!?\[)((?:[^\]\\]|\\.)*)(\]\(.*)", tok, re.S)
        if lm:
            tok = lm.group(1) + space_text(lm.group(2)) + lm.group(3)
        kind = "tag" if tok.startswith("<") or tok.startswith("{{") else "latin"
        spans.append(tok)
        return f"\x00{kind}{len(spans) - 1}\x01"

    s = PROTECT.sub(keep, line)
    # inline elements behave like Latin words at their edges; tags/shortcodes are transparent
    s = re.sub(f"([{CJK}])({EMPH})(\x00latin)", r"\1 \2\3", s)
    s = re.sub(f"(latin\\d+\x01)({EMPH})(?=[{CJK}])", r"\1\2 ", s)
    s = space_text(s)
    return re.sub("\x00(?:tag|latin)(\\d+)\x01", lambda m: spans[int(m.group(1))], s)


def process(text):
    out, fence, front = [], None, False
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if i == 0 and line.strip() == "---":
            front = True
            out.append(line)
            continue
        if front:
            if line.strip() == "---":
                front = False
            elif re.match(r"^(title|description|summary):", line):
                k, v = line.split(":", 1)
                line = k + ":" + space_line(v)
            out.append(line)
            continue
        m = re.match(r"^\s*(`{3,}|~{3,})", line)
        if fence:
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence):
                fence = None
            out.append(line)
            continue
        if m:
            fence = m.group(1)
            out.append(line)
            continue
        out.append(space_line(line) if CJK_CH.search(line) else line)
    return "\n".join(out)


def main():
    args = [a for a in sys.argv[1:] if a != "--check"]
    check = "--check" in sys.argv
    roots = [Path(a) for a in args] or [Path(__file__).resolve().parent.parent / "content"]
    changed = 0
    for root in roots:
        files = [root] if root.is_file() else sorted(root.rglob("*.md"))
        for f in files:
            t = f.read_text(encoding="utf-8")
            n = process(t)
            if n != t:
                changed += 1
                if check:
                    print(f)
                else:
                    f.write_text(n, encoding="utf-8", newline=chr(10))
    print(f"{'would change' if check else 'changed'}: {changed} file(s)")


if __name__ == "__main__":
    main()
