"""Streamlined categories and tags for every article, in one place.

  python tools/taxonomy.py            write tools/taxonomy-plan.md (review: old -> new for every post)
  python tools/taxonomy.py --apply    rewrite categories/tags in content/zh and content/en, and data/terms.toml

Edit PLAN / CATEGORIES / TAGS below, re-run, review, then --apply.
Chinese names are the keys; the English site gets the paired names.
"""
import re, sys, collections
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# zh -> en
CATEGORIES = {
    "编程语言": "Programming Languages",
    "系统编程": "Systems Programming",
    "后端与网络": "Backend & Networking",
    "算法与数据结构": "Algorithms & Data Structures",
    "游戏开发": "Game Development",
    "游戏引擎": "Game Engines",
    "复古掌机": "Retro Handhelds",
    "机器学习": "Machine Learning",
    "随笔": "Jottings",
}

# zh -> en (same name when it is a proper noun)
TAGS = {
    # languages and runtimes
    "C": "C", "C++": "C++", "STL": "STL", "C#": "C#", ".NET": ".NET", "CLR": "CLR", "Python": "Python", "汇编": "Assembly",
    # systems
    "Win32": "Win32", "Windows": "Windows", "多线程": "Multithreading", "操作系统": "OS",
    # backend and networking
    "API": "API", "网络编程": "Network Programming", "TCP/IP": "TCP/IP", "MongoDB": "MongoDB", "Metasploit": "Metasploit",
    "Raspberry Pi": "Raspberry Pi", "Arduino": "Arduino",
    # algorithms
    "排序": "Sorting", "图论": "Graph Theory", "动态规划": "Dynamic Programming", "LeetCode": "LeetCode", "寻路": "Pathfinding",
    # games
    "Unity": "Unity", "Godot": "Godot", "Pilot": "Pilot", "GameBoy": "GameBoy", "GBDK": "GBDK", "像素艺术": "Pixel Art",
    "设计模式": "Design Patterns", "OpenXR": "OpenXR",
    # retro handhelds
    "PocketChip": "PocketChip", "GameShell": "GameShell", "DevTerm": "DevTerm",
    # machine learning
    "深度学习": "Deep Learning",
    # jottings
    "博客": "Blogging", "Hexo": "Hexo", "Hugo": "Hugo", "Git": "Git", "TVCG": "TVCG",
    # kept specific topics
    "线程池": "Thread Pool", "异步 I/O": "Async I/O", "AppDomain": "AppDomain", "异常处理": "Exception Handling",
    "匿名类型": "Anonymous Types", "内存布局": "Memory Layout", "DLL": "DLL", "Mono": "Mono", "CIL": "CIL", "跨平台": "Cross-Platform",
    "接口": "Interfaces", "内核对象": "Kernel Objects", "Socket": "Socket", "Unix": "Unix", "数据库": "Database",
    "安全": "Security", "BadUSB": "BadUSB", "造轮子": "Reinventing the Wheel", "bilibili": "bilibili", "GitHub": "GitHub",
    "最短路径": "Shortest Path", "DFS": "DFS", "BFS": "BFS", "并查集": "Union-Find", "A*": "A*", "GAMES104": "GAMES104",
    "动画": "Animation", "XR": "XR", "Love2D": "Love2D", "RetroArch": "RetroArch", "OpenGL": "OpenGL", "改装": "Modding",
    "ClockworkPi": "ClockworkPi", "神经网络": "Neural Networks", "逻辑回归": "Logistic Regression", "Shields.io": "Shields.io",
    "学术": "Academia",
}

# Names that can't be used as-is in a URL get a safe key in front matter; the real name is set as the
# title of content/shared/<taxonomy>/<key>/_index.md (both languages). Without this Hugo would turn
# "C#" and "C++" into /tags/c/ (the same page as C) and ".NET" into a hidden folder.
KEYS = {
    "C#": "CSharp", "C++": "CPP", ".NET": "DotNET", "TCP/IP": "TCP-IP", "A*": "AStar",
    "异步 I/O": "异步IO", "Async I/O": "AsyncIO",
    "Backend & Networking": "Backend-Networking", "Algorithms & Data Structures": "Algorithms-Data-Structures",
}

# Old tag -> where it went (only for the review document).
RENAMED = {
    "CSharp": "C#", "CPP": "C++", "DotNET": ".NET", "python": "Python", "win32": "Win32", "multithreading": "多线程",
    "Thread": "多线程", "ThreadPool": "线程池", "OverlappedI-O": "异步 I/O", "assembly": "汇编", "OS": "操作系统",
    "TCP-IP": "TCP/IP", "network": "网络编程", "Exception": "异常处理", "AnonymousType": "匿名类型",
    "StructLayoutAttribute": "内存布局", "Handles": "内核对象", "Objects": "内核对象", "crossplatform": "跨平台",
    "CLI": "CIL / .NET", "codefromscratch": "造轮子", "github": "GitHub", "git": "Git", "msf": "Metasploit", "badusb": "BadUSB",
    "internet-security": "安全", "AStar": "A*", "PathFinding": "寻路", "Union-Find-Sets": "并查集", "PixelArt": "像素艺术",
    "Animation": "动画", "design-pattern": "设计模式", "PilotEngine": "Pilot", "RaspberryPi": "Raspberry Pi",
    "Clockwork": "ClockworkPi", "MicroPC": "ClockworkPi", "LCD": "改装", "beautify": "Shields.io",
}

# path under content/<lang>/ -> (category, [tags])
PLAN = {
    # 编程语言
    "posts/about-layoutkind.md": ("编程语言", ["CLR", "C#", "内存布局"]),
    "posts/about-new.md": ("编程语言", ["C#", "C++"]),
    "posts/c-letter-case-swap.md": ("编程语言", ["C"]),
    "posts/clr-compute-bound-asynchronous-operations.md": ("编程语言", ["CLR", "C#", "多线程", "线程池"]),
    "posts/clr-critical-chapters.md": ("编程语言", ["CLR"]),
    "posts/clr-qa.md": ("编程语言", ["CLR"]),
    "posts/clr01-basic.md": ("编程语言", ["CLR", "C#"]),
    "posts/cpp-dll-and-assembly.md": ("编程语言", [".NET", "CLR", "DLL"]),
    "posts/csharp-anonymoustype-equals.md": ("编程语言", ["CLR", "C#", "匿名类型"]),
    "posts/csharp-exception.md": ("编程语言", ["CLR", "C#", "异常处理"]),
    "posts/how-app-monitors-unloading-of-appdomain.md": ("编程语言", ["CLR", "C#", "AppDomain"]),
    "posts/programming-languages/csharp/static-abstract-members-in-interfaces.md": ("编程语言", ["C#", ".NET", "接口"]),
    "posts/sharing-a-bloger-about-dotnet.md": ("编程语言", [".NET"]),
    "posts/stl-vector.md": ("编程语言", ["C++", "STL"]),
    "posts/trap-clr-constrained.md": ("编程语言", ["CLR", "C#"]),
    "posts/typeobj-and-typeinit.md": ("编程语言", ["CLR", "C#"]),
    "posts/vc6-basics.md": ("编程语言", ["C", "C++"]),
    # 系统编程
    "posts/handles-and-objects-on-windows.md": ("系统编程", ["Windows", "内核对象"]),
    "posts/make-os-in-30-days-01.md": ("系统编程", ["操作系统", "汇编"]),
    "posts/multithreading-win32api-vs-csharpapi.md": ("系统编程", ["Win32", "多线程", "C#"]),
    "posts/overlapped-io.md": ("系统编程", ["Win32", "多线程", "异步 I/O"]),
    "posts/win32multithreading-faq.md": ("系统编程", ["Win32", "多线程"]),
    "posts/win32multithreading01.md": ("系统编程", ["Win32", "多线程"]),
    "posts/win32multithreading02.md": ("系统编程", ["Win32", "多线程"]),
    "posts/win32multithreading03.md": ("系统编程", ["Win32", "多线程"]),
    "posts/windows-thread-internals.md": ("系统编程", ["Windows", "多线程"]),
    # 后端与网络
    "posts/about-python-api.md": ("后端与网络", ["Python", "API"]),
    "posts/api-fanscount-bilibili.md": ("后端与网络", ["Python", "API", "造轮子", "bilibili"]),
    "posts/api-fanscount-github.md": ("后端与网络", ["Python", "API", "造轮子", "GitHub"]),
    "posts/backend/mongodb/auto-increment-id-in-mongodb.md": ("后端与网络", ["MongoDB", "数据库"]),
    "posts/dorm-assistant.md": ("后端与网络", ["Raspberry Pi", "Arduino", "Python"]),
    "posts/tcpip-notes.md": ("后端与网络", ["TCP/IP", "网络编程"]),
    "posts/unix-socket-api.md": ("后端与网络", ["TCP/IP", "网络编程", "Socket", "Unix"]),
    "posts/msf01-windows-meterpreter-reverse-tcp.md": ("后端与网络", ["安全", "Metasploit", "BadUSB", "Windows"]),
    # 算法与数据结构
    "posts/algorithms/dynamic-programming/framework.md": ("算法与数据结构", ["动态规划"]),
    "posts/bubble-sort.md": ("算法与数据结构", ["排序"]),
    "posts/merge-sort.md": ("算法与数据结构", ["排序"]),
    "posts/quick-sort.md": ("算法与数据结构", ["排序"]),
    "posts/sort-three-numbers.md": ("算法与数据结构", ["排序", "C"]),
    "posts/dijkstra.md": ("算法与数据结构", ["图论", "最短路径"]),
    "posts/leetcode547.md": ("算法与数据结构", ["LeetCode", "图论", "DFS", "BFS", "并查集"]),
    "posts/data-structure-linear-list.md": ("算法与数据结构", ["C"]),
    "posts/data-structure-stack.md": ("算法与数据结构", ["C"]),
    # 游戏开发
    "posts/astar-in-unity.md": ("游戏开发", ["Unity", "寻路", "A*"]),
    "posts/command-pattern-in-unity.md": ("游戏开发", ["Unity", "设计模式"]),
    "posts/unity-netgame-001.md": ("游戏开发", ["Unity", "网络编程"]),
    "posts/unity-netgame-002.md": ("游戏开发", ["Unity", "网络编程"]),
    "posts/how-unity-crossplatform.md": ("游戏引擎", ["Unity", "跨平台", "Mono", "CIL", ".NET", "CLR"]),
    "posts/game-engine/godotsteam-macos-permission.md": ("游戏引擎", ["Godot"]),
    "posts/learn-from-pilot-01.md": ("游戏引擎", ["Pilot", "GAMES104"]),
    "posts/learn-from-pilot-02.md": ("游戏引擎", ["Pilot", "GAMES104"]),
    "posts/learn-from-pilot-03.md": ("游戏引擎", ["Pilot", "GAMES104"]),
    "posts/pixel-art-animation-001-shine.md": ("游戏开发", ["像素艺术", "动画"]),
    "posts/phd-life/openxr-simulator.md": ("游戏开发", ["OpenXR", "XR"]),
    "game-dev/retro/gameboy/intro.md": ("游戏开发", ["GameBoy"]),
    "game-dev/retro/gameboy/gbdk/001-gbdk-intro.md": ("游戏开发", ["GameBoy", "GBDK"]),
    "game-dev/retro/gameboy/gbdk/002-gbdk-preparation.md": ("游戏开发", ["GameBoy", "GBDK"]),
    "game-dev/retro/gameboy/gbdk/003-gbdk-simple-sprites.md": ("游戏开发", ["GameBoy", "GBDK"]),
    # 复古掌机
    "posts/gameshell-bigger-lcd.md": ("复古掌机", ["GameShell", "ClockworkPi", "改装"]),
    "posts/how-to-play-gameshell-01.md": ("复古掌机", ["GameShell", "ClockworkPi"]),
    "posts/run-godot-game-on-gameshell.md": ("复古掌机", ["GameShell", "ClockworkPi", "Godot"]),
    "posts/intro-devterm.md": ("复古掌机", ["DevTerm", "ClockworkPi"]),
    "posts/pocketchip-love2d.md": ("复古掌机", ["PocketChip", "Love2D"]),
    "posts/pocketchip-opengl-hardware-speedup.md": ("复古掌机", ["PocketChip", "OpenGL"]),
    "posts/pocketchip-retroarch.md": ("复古掌机", ["PocketChip", "RetroArch"]),
    "posts/pocketchip-stero-speaker.md": ("复古掌机", ["PocketChip", "改装"]),
    # 机器学习
    **{f"posts/{s}.md": ("机器学习", ["深度学习"]) for s in [
        "ml-notes-01-learning-system", "ml-notes-03-supervised-learning", "ml-notes-04-why-deep-learning",
        "ml-notes-05-binary-classification"]},
    "posts/ml-notes-02-neural-networks.md": ("机器学习", ["深度学习", "神经网络"]),
    "posts/ml-notes-06-logistic-regression.md": ("机器学习", ["深度学习", "逻辑回归"]),
    "posts/ml-notes-07-logistic-regression-cost.md": ("机器学习", ["深度学习", "逻辑回归"]),
    # 随笔
    "posts/git-badge-substats.md": ("随笔", ["Git", "Shields.io", "博客"]),
    "posts/hexo-aliyun.md": ("随笔", ["Hexo", "博客"]),
    "posts/hugo-blog-revival.md": ("随笔", ["Hugo", "博客"]),
    "posts/phd-life/ieee-tvcg-guidelines.md": ("随笔", ["TVCG", "学术"]),
}


def split_fm(text):
    text = text.replace("\r\n", "\n")
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    return (m.group(1), text[m.end():]) if m else (None, text)


def get_list(fm, key):
    m = re.search(rf"^{key}:\s*\[(.*?)\]\s*$", fm, re.M)
    return [x.strip().strip("'\"") for x in m.group(1).split(",") if x.strip()] if m else []


def yaml_list(items):
    return "[" + ", ".join(f'"{x}"' if re.search(r"[:#\[\]{},&*!|>'\"%@`]", x) else x for x in items) + "]"


def set_list(fm, key, items):
    line = f"{key}: {yaml_list(items)}"
    if re.search(rf"^{key}:.*$", fm, re.M):
        return re.sub(rf"^{key}:.*$", lambda m: line, fm, count=1, flags=re.M)
    return fm + "\n" + line


def articles(lang):
    for p in sorted((ROOT / "content" / lang).rglob("*.md")):
        if p.name == "_index.md":
            continue
        fm, _ = split_fm(p.read_text(encoding="utf-8"))
        if fm is None or re.search(r"^(article:\s*false|layout:)", fm, re.M):
            continue
        yield p.relative_to(ROOT / "content" / lang).as_posix(), p, fm


def check():
    problems = []
    for rel, cat_tags in PLAN.items():
        cat, tags = cat_tags
        if cat not in CATEGORIES: problems.append(f"{rel}: unknown category {cat}")
        problems += [f"{rel}: unknown tag {t}" for t in tags if t not in TAGS]
    zh = {rel for rel, _, _ in articles("zh")}
    problems += [f"no plan for {rel}" for rel in sorted(zh - PLAN.keys())]
    problems += [f"plan for missing post {rel}" for rel in sorted(PLAN.keys() - zh)]
    return problems


def review():
    name = {v: k for k, v in KEYS.items()}.get  # front matter keys back to display names
    old = {rel: ([name(c, c) for c in get_list(fm, "categories")], [name(x, x) for x in get_list(fm, "tags")],
                 (re.search(r"^title:\s*(.*)$", fm, re.M) or [0, ""])[1].strip("'\""))
           for rel, _, fm in articles("zh")}
    ccount = collections.Counter(c for c, _ in PLAN.values())
    tcount = collections.Counter(t for _, ts in PLAN.values() for t in ts)
    old_tags = collections.Counter(t for _, ts, _ in old.values() for t in ts)
    old_cats = collections.Counter(c for cs, _, _ in old.values() for c in cs)
    out = ["# 分类与标签整理方案", "",
           f"共 {len(PLAN)} 篇文章。分类 {len(old_cats)} → {len(CATEGORIES)}，标签 {len(old_tags)} → {len(tcount)}。",
           "英文站使用右列的英文名。中英对应关系由三处共同保证，`--apply` 会一起生成：", "",
           "1. 文章 front matter：名字里有 `#`、`+`、`/`、`*`、`&`、开头是 `.` 的，写成 URL 安全的键（`C#` → `CSharp`，`C++` → `CPP`，`.NET` → `DotNET`，`TCP/IP` → `TCP-IP`，`A*` → `AStar`，`异步 I/O` → `异步IO`）。",
           "2. 这些键的显示名页面 `_index.md`：中英同名的放 `content/shared/`（两种语言共用），只有一种语言用的放 `content/zh/` 或 `content/en/`，其余旧的标签页全部删除，不留空标签页。",
           "3. `data/terms.toml`：中英不同名的成对登记（多线程 = Multithreading），相关文章按它跨语言匹配，标签页的语言切换也靠它找到对应页。", "",
           "试运行（应用 → 构建 → 恢复）的检查结果：174 个标签/分类页的语言切换全部指向对应语言的同名页，且两边文章一致；66 篇双语文章的相关文章仅 3 篇不同，均因《深入理解 Windows 线程》只有中文版。", "",
           "## 分类", "", "| 中文 | English | 篇数 |", "|---|---|---|"]
    out += [f"| {zh} | {en} | {ccount[zh]} |" for zh, en in CATEGORIES.items()]
    out += ["", "## 标签", "", "| 中文 | English | 篇数 |", "|---|---|---|"]
    out += [f"| {zh} | {en} | {tcount[zh]} |" for zh, en in sorted(TAGS.items(), key=lambda kv: (-tcount[kv[0]], kv[0].lower()))]
    gone = sorted(set(old_tags) - set(TAGS), key=str.lower)
    renamed = {t: RENAMED[t] for t in gone if t in RENAMED}
    removed = [t for t in gone if t not in RENAMED]
    if renamed:
        out += ["", "## 旧标签的去向", "", "改名或并入（内容保留，只是统一了写法）：", "",
                "| 旧 | 新 |", "|---|---|"] + [f"| {a} | {b} |" for a, b in renamed.items()]
    if removed:
        out += ["", "删除（文章类型、或与分类重复）：", "", "、".join(removed)]
    out += ["", "## 每篇文章（旧 → 新）", "", "| 文章 | 旧分类 | 新分类 | 旧标签 | 新标签 |", "|---|---|---|---|---|"]
    order = list(CATEGORIES)
    for rel, (cat, tags) in sorted(PLAN.items(), key=lambda kv: (order.index(kv[1][0]), kv[0])):
        oc, ot, title = old.get(rel, ([], [], rel))
        same_c = "" if oc == [cat] else "**"
        out.append(f"| {title} | {', '.join(oc)} | {same_c}{cat}{same_c} | {', '.join(ot)} | {', '.join(tags)} |")
    path = ROOT / "tools" / "taxonomy-plan.md"
    path.write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")
    print("wrote", path.relative_to(ROOT).as_posix(), f"({len(CATEGORIES)} categories, {len(tcount)} tags, {len(gone)} old tags dropped)")


def apply():
    # 1. front matter: URL-safe keys (C# -> CSharp ...), the display name comes from the shared page
    for lang in ("zh", "en"):
        for rel, p, fm in articles(lang):
            if rel not in PLAN:
                continue
            cat, tags = PLAN[rel]
            if lang == "en":
                cat, tags = CATEGORIES[cat], [TAGS[t] for t in tags]
            text = p.read_text(encoding="utf-8").replace("\r\n", "\n")
            fm2, body = split_fm(text)
            fm2 = set_list(set_list(fm2, "categories", [KEYS.get(cat, cat)]), "tags", [KEYS.get(t, t) for t in tags])
            p.write_text(f"---\n{fm2}\n---\n{body}", encoding="utf-8", newline="\n")
    # 2. Display-name pages for keyed terms, placed by which language uses the name:
    #    both -> content/shared/<tax>/<key>/ (mounted for both), one -> content/<lang>/<tax>/<key>/.
    #    Any other term page under these folders is removed, so no term page exists without posts.
    names = {"tags": (set(TAGS), set(TAGS.values())), "categories": (set(CATEGORIES), set(CATEGORIES.values()))}
    for tax, (zh_names, en_names) in names.items():
        want = {}
        for name in (zh_names | en_names):
            if name in KEYS:
                where = "shared" if (name in zh_names and name in en_names) else ("zh" if name in zh_names else "en")
                want[(where, KEYS[name])] = name
        for where in ("shared", "zh", "en"):
            base = ROOT / "content" / where / tax
            if not base.exists():
                continue
            for d in base.iterdir():
                if d.is_dir() and (where, d.name) not in want:
                    for f in d.iterdir(): f.unlink()
                    d.rmdir()
        for (where, key), name in want.items():
            d = ROOT / "content" / where / tax / key
            d.mkdir(parents=True, exist_ok=True)
            (d / "_index.md").write_text(f'---\ntitle: "{name}"\n---\n', encoding="utf-8", newline="\n")
    # 3. data/terms.toml: pairs of display names, for related posts and the language switch on term pages
    lines = ["# Links tags / categories that are spelled differently in each language.",
             "# Generated by tools/taxonomy.py (edit the lists there, then run it with --apply).",
             "#", "#   [<taxonomy>.\"<English name>\"]", "#   zh = \"<中文名>\"", ""]
    for zh, en in sorted(TAGS.items(), key=lambda kv: kv[1].lower()):
        if zh != en: lines += [f'[tags."{en}"]', f'zh = "{zh}"']
    lines.append("")
    for zh, en in CATEGORIES.items():
        if zh != en: lines += [f'[categories."{en}"]', f'zh = "{zh}"']
    (ROOT / "data" / "terms.toml").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print("applied to content/zh, content/en and data/terms.toml")


if __name__ == "__main__":
    probs = check()
    if probs:
        print("\n".join(probs)); sys.exit(1)
    apply() if "--apply" in sys.argv else review()
