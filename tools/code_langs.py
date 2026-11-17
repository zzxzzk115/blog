"""Find fenced code blocks without a language and suggest one from their content.

    python tools/code_langs.py          # report
    python tools/code_langs.py --apply  # write the suggested language into the fences

Blocks the heuristics can't place are left alone (reported as "?").
"""
import re
import sys
from pathlib import Path

CONTENT = Path(__file__).resolve().parent.parent / "content"
FENCE = re.compile(r"^(\s*)(`{3,}|~{3,})\s*([\w#+.-]*)\s*(\{.*\})?\s*$")
UNTYPED = {"", "text", "txt", "plain", "plaintext"}

RULES = [  # (language, regex) — first match wins, most specific first
    ("csharp", r"\busing System\b|\bnamespace\s+[\w.]+\s*[{;]|\bConsole\.Write|\bpublic (static |sealed |abstract |partial )*(class|struct|interface|enum|record)\b|\b(get|set);|\bvar \w+ = new\b|\bstring\[\]|\bMonoBehaviour\b|\[DllImport|\bIntPtr\b|=>\s*\w|\bforeach\s*\(|\bThread\.|\bTask<|\basync Task\b|\bstatic void Main\b"),
    ("cpp", r"#include\s*[<\"]|\bstd::|\bcout\s*<<|\btemplate\s*<|\b(unsigned|signed)\s+(int|char|long)\b|::\w+\(|\bnullptr\b|\bvirtual\b.*\)\s*(=\s*0)?;|\b__declspec\b|\bHANDLE\b|\bDWORD\b|\bLPVOID\b|\bWINAPI\b|\bmain\s*\(\s*(int|void)?"),
    ("c", r"\bprintf\s*\(|\bmalloc\s*\(|\bstruct\s+\w+\s*\{|\bint\s+\w+\s*\([^)]*\)\s*\{"),
    ("python", r"^\s*(def|class) \w+.*:\s*$|^\s*(from \w+ )?import \w+|\bprint\(|\bself\.\w+|__name__"),
    ("cmake", r"\b(cmake_minimum_required|add_executable|add_library|target_link_libraries|set\(CMAKE_)\b"),
    ("makefile", r"^\w[\w.-]*\s*:.*$\n\t|\$\(\w+\)|^\.PHONY"),
    ("powershell", r"^\s*\$env:\w+|\bSet-\w+\b|\bGet-\w+\b"),
    ("batch", r"^\s*(set \w+=|@echo off|call \w+)"),
    ("bash", r"^\s*(sudo|apt(-get)?|brew|cd|ls|mkdir|git|pip3?|npm|wget|curl|chmod|chown|export|echo|cp|mv|rm|tar|unzip|make|cmake|ssh|scp|systemctl|service|source|alias|nano|vim?)\b|^\s*\$ "),
    ("json", r"^\s*[\[{]\s*$[\s\S]*\"\w+\"\s*:"),
    ("ini", r"^\s*#?\s*\[?\w[\w ]*\]?\s*$[\s\S]*^\s*#?\s*\w+\s*=|^\s*#?Section\b"),
    ("xml", r"^\s*<\?xml|^\s*<(\w+)[^>]*>[\s\S]*</\1>"),
    ("sql", r"\b(SELECT|INSERT INTO|CREATE TABLE|UPDATE \w+ SET)\b"),
]


def guess(code):
    for lang, rx in RULES:
        if re.search(rx, code, re.M):
            return lang
    return None


def blocks(text):
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        m = FENCE.match(lines[i])
        if m:
            indent, fence, lang, attrs = m.groups()
            j = i + 1
            while j < len(lines) and not re.match(rf"^\s*{re.escape(fence[0])}{{{len(fence)},}}\s*$", lines[j]):
                j += 1
            yield i, j, indent, fence, lang, attrs or "", "\n".join(lines[i + 1:j])
            i = j + 1
        else:
            i += 1


def main():
    apply = "--apply" in sys.argv
    total = changed = 0
    for f in sorted(CONTENT.rglob("*.md")):
        text = f.read_text(encoding="utf-8")
        lines = text.split("\n")
        edits = []
        for start, end, indent, fence, lang, attrs, code in blocks(text):
            if lang.lower() not in UNTYPED or lang.lower() in {"mermaid", "chart"}:
                continue
            total += 1
            g = guess(code)
            first = next((l.strip() for l in code.splitlines() if l.strip()), "")[:70]
            print(f"{'?' if not g else g:10} {f.relative_to(CONTENT).as_posix()}:{start + 1}  | {first}")
            if g:
                edits.append((start, f"{indent}{fence}{g}{(' ' + attrs) if attrs else ''}"))
        if apply and edits:
            for start, new in edits:
                lines[start] = new
            f.write_text("\n".join(lines), encoding="utf-8", newline="\n")
            changed += len(edits)
    print(f"untyped blocks: {total}" + (f", labelled: {changed}" if apply else ""))


if __name__ == "__main__":
    main()
