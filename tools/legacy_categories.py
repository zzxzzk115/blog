"""Category / tag remap for the 2020–2022 (hexo) posts, used once when merging them into the
active blog's taxonomy. Kept for reference; `python tools/legacy_categories.py` is idempotent.

Moves content/shared/posts/*.md -> content/zh/posts/ (the English versions live in content/en/posts/).
"""
import pathlib
import re

SITE = pathlib.Path(__file__).resolve().parent.parent

# (en, zh)
PL = ("Programming Languages", "编程语言")
SYS = ("Systems Programming", "系统编程")
BE = ("Backend", "后端")
GD = ("Game Development", "游戏开发")
GE = ("Game Engines", "游戏引擎")
RH = ("Retro Handhelds", "复古掌机")
ALG = ("Algorithms", "算法")
JOT = ("Jottings", "随笔")
SEC = ("Security", "安全")

CATEGORY = {
    "about-layoutkind": PL, "about-new": PL, "clr-compute-bound-asynchronous-operations": PL,
    "clr-critical-chapters": PL, "clr-qa": PL, "clr01-basic": PL, "cpp-dll-and-assembly": PL,
    "csharp-anonymoustype-equals": PL, "csharp-exception": PL, "how-app-monitors-unloading-of-appdomain": PL,
    "sharing-a-bloger-about-dotnet": PL, "trap-clr-constrained": PL, "typeobj-and-typeinit": PL,
    "handles-and-objects-on-windows": SYS, "multithreading-win32api-vs-csharpapi": SYS, "overlapped-io": SYS,
    "win32multithreading-faq": SYS, "win32multithreading01": SYS, "win32multithreading02": SYS,
    "windows-thread-internals": SYS,
    "about-python-api": BE, "api-fanscount-bilibili": BE, "api-fanscount-github": BE, "tcpip-notes": BE,
    "unix-socket-api": BE,
    "command-pattern-in-unity": GD, "unity-netgame-001": GD, "unity-netgame-002": GD, "astar-in-unity": GD,
    "pixel-art-animation-001-shine": GD,
    "how-unity-crossplatform": GE, "learn-from-pilot-01": GE, "learn-from-pilot-02": GE, "learn-from-pilot-03": GE,
    "gameshell-bigger-lcd": RH, "how-to-play-gameshell-01": RH, "intro-devterm": RH, "pocketchip-love2d": RH,
    "pocketchip-opengl-hardware-speedup": RH, "pocketchip-retroarch": RH, "pocketchip-stero-speaker": RH,
    "run-godot-game-on-gameshell": RH,
    "leetcode547": ALG,
    "git-badge-substats": JOT, "hexo-aliyun": JOT,
    "msf01-windows-meterpreter-reverse-tcp": SEC,
}
TAG_MERGE = {"Algorithm": "Algorithms", "api": "API"}


def retag(text):
    m = re.search(r"^tags:\s*\[(.*?)\]", text, re.M)
    if not m:
        return text
    tags = []
    for t in (x.strip() for x in m.group(1).split(",") if x.strip()):
        t = TAG_MERGE.get(t, t)
        if t not in tags:
            tags.append(t)
    return text[:m.start()] + f"tags: [{', '.join(tags)}]" + text[m.end():]


def set_category(text, name):
    return re.sub(r"^categories:\s*\[.*?\]", f"categories: [{name}]", text, count=1, flags=re.M)


def main():
    src = SITE / "content" / "shared" / "posts"
    dst = SITE / "content" / "zh" / "posts"
    files = sorted(src.glob("*.md")) if src.is_dir() else sorted(p for p in dst.glob("*.md") if p.stem in CATEGORY)
    for f in files:
        en, zh = CATEGORY[f.stem]
        t = retag(set_category(f.read_text(encoding="utf-8"), zh))
        (dst / f.name).write_text(t, encoding="utf-8")
        if f.parent == src:
            f.unlink()
    # same tag merges for every other page
    for f in (SITE / "content").rglob("*.md"):
        t = f.read_text(encoding="utf-8")
        t2 = retag(t)
        if t2 != t:
            f.write_text(t2, encoding="utf-8")
    print(f"{len(files)} posts -> content/zh/posts/")


if __name__ == "__main__":
    main()
