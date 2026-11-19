"""Pull the project catalog (github.com/zzxzzk115/featured-projects) and turn it into the blog's project data.

    python tools/catalog.py              # clone or pull into .catalog/, then generate
    python tools/catalog.py --no-pull    # use .catalog/ as it is
    CATALOG_DIR=../featured-projects python tools/catalog.py   # use a local checkout instead

Writes (all generated, git-ignored):
  data/projects.json      cards for the theme's {{< projects >}} shortcode (English)
  data/projects_zh.json   Chinese text, link labels and Chinese link targets, keyed by project id
  static/img/catalog/<id>/  the projects' images
Groups on each card: "about" (the About page's full list) and the blog columns it is in ("porting", ...), with its
position in each column in `groupOrder`.
"""
import json, os, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REMOTE = "https://github.com/zzxzzk115/featured-projects.git"
HOMEPAGE = "https://zzxzzk115.github.io"
BLOG = HOMEPAGE + "/blog"
IMG_URL = "/img/catalog"


def catalog_dir():
    if os.environ.get("CATALOG_DIR"):
        return Path(os.environ["CATALOG_DIR"]).resolve()
    d = ROOT / ".catalog"
    if "--no-pull" not in sys.argv:
        if (d / ".git").exists():
            subprocess.run(["git", "-C", str(d), "pull", "--ff-only", "-q"], check=True)
        else:
            subprocess.run(["git", "clone", "-q", "--depth", "1", REMOTE, str(d)], check=True)
    return d


def pick(v, lang):
    """A {en, zh} text or href in one language (Chinese falls back to English)."""
    if isinstance(v, dict):
        return v.get(lang) or v.get("en")
    return v


def local(href):
    """Links into this blog become site paths (they open here, not in a new tab); homepage paths ("/assets/...",
    written for the homepage) become full homepage addresses."""
    if isinstance(href, str) and href.startswith(BLOG + "/"):
        return href[len(BLOG):]
    if isinstance(href, str) and href.startswith("/") and not href.startswith("//"):
        return HOMEPAGE + href
    return href


def main():
    src = catalog_dir()
    cat = json.loads((src / "catalog.json").read_text(encoding="utf-8"))
    img_root = ROOT / "static" / IMG_URL.strip("/")
    if img_root.exists():
        shutil.rmtree(img_root)
    cards, zh, labels = [], {}, {}
    for p in cat["projects"]:
        pid, blog = p["id"], p.get("blog") or {}
        groups = (["about"] if blog.get("about") else []) + list((blog.get("columns") or {}).keys())
        if not groups:
            continue
        hp = p.get("homepage")
        orders = []
        if hp and isinstance(hp.get("home"), dict):
            orders = [v.get("order", 100) for v in hp["home"].values() if isinstance(v, dict)]
        first_link = p["links"][0]["href"] if p.get("links") else ""
        page = p.get("url") or (HOMEPAGE + hp["path"] if hp else first_link)
        image = ""
        if p.get("image"):
            f = src / p["image"]["src"]
            dest = img_root / pid / f.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, dest)
            image = f"{IMG_URL}/{pid}/{f.name}"
        cards.append({
            "id": pid, "title": p["title"]["en"], "desc": p["description"]["en"],
            "category": p.get("category", ""), "tags": p.get("tags", []),
            "status": pick(p.get("status"), "en") or "", "order": p.get("order", 999),
            "featured": min(orders) if orders else None,
            "image": image, "imageFit": (p.get("image") or {}).get("fit", "cover"),
            "page": local(pick(page, "en")), "repo": p.get("repo", ""),
            "links": [{"label": l["label"]["en"], "href": local(pick(l["href"], "en"))} for l in p.get("links", [])],
            "groups": groups, "groupOrder": blog.get("columns") or {},
        })
        t = {k: pick(p[f], "zh") for k, f in (("title", "title"), ("desc", "description"), ("status", "status"))
             if p.get(f) and p[f].get("zh")}
        zh_links = [local(pick(l["href"], "zh")) for l in p.get("links", [])]
        if zh_links != [c["href"] for c in cards[-1]["links"]]:
            t["hrefs"] = zh_links
        zh_page = local(pick(page, "zh"))
        if zh_page != cards[-1]["page"]:
            t["page"] = zh_page
        if t:
            zh[pid] = t
        for l in p.get("links", []):
            if l["label"].get("zh"):
                labels[l["label"]["en"]] = l["label"]["zh"]
    zh["labels"] = labels
    (ROOT / "data" / "projects.json").write_text(json.dumps(cards, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    (ROOT / "data" / "projects_zh.json").write_text(json.dumps(zh, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(f"catalog {src}: {len(cards)} projects for the blog")


if __name__ == "__main__":
    main()
