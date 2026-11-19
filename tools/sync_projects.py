"""Sync the project gallery from the personal homepage (github.com/zzxzzk115/zzxzzk115.github.io).

    python tools/sync_projects.py            # needs PyYAML: pip install pyyaml

Reads content/projects/*.md (front matter: title, description, category, tags, links, image, order, home)
and writes data/projects.json for the {{< projects >}} shortcode; images are saved to static/img/projects/.
Chinese text lives in data/projects_zh.toml (hand-written, keyed by project id; never touched by this script).
"""
import json, re, sys, time, urllib.request
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is needed: pip install pyyaml")

REPO = "zzxzzk115/zzxzzk115.github.io"
RAW = f"https://raw.githubusercontent.com/{REPO}/main/"
SITE = "https://zzxzzk115.github.io"
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "projects.json"
IMG = ROOT / "static" / "img" / "projects"
UA = {"User-Agent": "Mozilla/5.0 (blog project sync)"}


def get(url, binary=False):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        data = r.read()
        return data if binary else data.decode("utf-8")


def absolute(href):
    """Homepage-relative links ("/assets/...") would resolve under the blog's domain root by luck; make them full."""
    return SITE + href if href.startswith("/") and not href.startswith("//") else href


def main():
    tree = json.loads(get(f"https://api.github.com/repos/{REPO}/git/trees/main?recursive=1"))
    files = sorted(t["path"] for t in tree["tree"] if re.fullmatch(r"content/projects/[^/]+\.md", t["path"]))
    IMG.mkdir(parents=True, exist_ok=True)
    projects = []
    for path in files:
        text = get(RAW + path)
        m = re.match(r"---\s*\n(.*?)\n---", text, re.S)
        if not m:
            continue
        fm = yaml.safe_load(m.group(1)) or {}
        pid = str(fm.get("id") or Path(path).stem)
        home = fm.get("home") or {}
        featured = None  # lowest homepage order across modes = featured on the homepage
        if isinstance(home, dict):
            orders = [v.get("order") for v in home.values() if isinstance(v, dict) and v.get("order") is not None]
            featured = min(orders) if orders else None
        image = ""
        if fm.get("image"):
            src = fm["image"] if fm["image"].startswith("http") else SITE + fm["image"]
            ext = Path(src.split("?")[0]).suffix.lower() or ".jpg"
            dest = IMG / f"{pid}{ext}"
            if (IMG / f"{pid}.webp").exists():  # a local WebP copy (converted to save space) wins
                dest = IMG / f"{pid}.webp"
            elif not dest.exists():
                time.sleep(0.3)
                dest.write_bytes(get(src, binary=True))
            image = f"/img/projects/{dest.name}"
        projects.append({
            "id": pid,
            "title": fm.get("title", pid),
            "desc": " ".join(str(fm.get("description", "")).split()),
            "category": fm.get("category", ""),
            "tags": [str(t) for t in fm.get("tags") or []],
            "status": fm.get("status", ""),
            "order": fm.get("order", 999),
            "featured": featured,
            "image": image,
            "imageFit": fm.get("imageFit", "cover"),
            "page": SITE + (fm.get("legacyPath") or f"/projects/{pid}/"),
            "links": [{"label": l.get("label", ""), "href": absolute(l.get("href", ""))} for l in fm.get("links") or [] if l.get("href")],
        })
        print(f"  {pid}: {projects[-1]['title']}{'  (featured ' + str(featured) + ')' if featured is not None else ''}")
    projects.sort(key=lambda p: (p["order"], p["title"].lower()))
    OUT.write_text(json.dumps(projects, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(projects)} projects)")


if __name__ == "__main__":
    main()
