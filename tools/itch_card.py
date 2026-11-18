"""Fetch itch.io game details for the {{< itch >}} shortcode.

    python tools/itch_card.py https://lazy-v.itch.io/catmario-gb [more game URLs]

Writes data/itch.toml (title, author, description, cover; keyed by the game URL) and saves each
cover to static/img/itch/, so pages never load anything from itch.io. itch rate-limits bursts
(HTTP 429): the script waits between games and retries once. Edit data/itch.toml by hand to
override anything, e.g. `pixel = true` for pixel-art covers.

In a post:  {{< itch url="https://lazy-v.itch.io/catmario-gb" >}}   (desc="…" overrides the blurb, e.g. a translation)
"""
import json, re, sys, time, tomllib
from pathlib import Path
from urllib.parse import urljoin, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
from linkcard import Meta, clean, get  # same polite fetcher (User-Agent, delays, one retry on 429)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "itch.toml"
COVERS = ROOT / "static" / "img" / "itch"


def fetch(url):
    p = Meta(); p.feed(get(url, "en"))
    m = p.meta
    full = clean(m.get("og:title") or p.title, 120)                     # "CatMario-GB by Lazy_V"
    title, _, author = full.rpartition(" by ") if " by " in full else (full, "", "")
    game = {"title": title or full, "author": author or urlparse(url).netloc.split(".")[0],
            "desc": clean(m.get("og:description") or m.get("description"), 200)}
    img = m.get("og:image") or m.get("twitter:image")
    if img:
        data, ctype = get(urljoin(url, img), "en", binary=True)
        ext = {"image/png": ".png", "image/jpeg": ".jpg", "image/gif": ".gif", "image/webp": ".webp"}.get(ctype.split(";")[0].strip(), ".png")
        name = re.sub(r"[^a-z0-9]+", "-", (urlparse(url).netloc.split(".")[0] + urlparse(url).path).lower()).strip("-") + ext
        COVERS.mkdir(parents=True, exist_ok=True)
        (COVERS / name).write_bytes(data)
        game["cover"] = f"/img/itch/{name}"
    return game


def main():
    urls = [a.rstrip("/") for a in sys.argv[1:] if a.startswith("http")]
    if not urls:
        sys.exit(__doc__)
    games = tomllib.loads(DATA.read_text(encoding="utf-8")) if DATA.exists() else {}
    for i, url in enumerate(urls):
        if i: time.sleep(5)
        try:
            games[url] = {**games.get(url, {}), **fetch(url)}
            print(f"  {url}: {games[url]['title']} by {games[url]['author']}")
        except Exception as e:
            print(f"  {url}: failed ({e}); try again in a minute", file=sys.stderr)
    lines = ["# itch.io games for {{< itch >}}; written by tools/itch_card.py, safe to edit.", ""]
    for url, g in games.items():
        lines.append(f"[{json.dumps(url)}]")
        for k, v in g.items():
            lines.append(f"{k} = {json.dumps(v, ensure_ascii=False)}")
        lines.append("")
    DATA.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(f"wrote {DATA.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
