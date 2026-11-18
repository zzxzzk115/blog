"""Make a {{< linkcard >}} for a URL: reads the page's title, description and preview image
(Open Graph / Twitter tags), saves the image to static/img/linkcards/ and prints the shortcode.

  python tools/linkcard.py <url> [<url> ...] [--lang zh-CN] [--no-image]
  python tools/linkcard.py --replace content/zh/posts/xxx.md content/en/posts/xxx.md

The image is stored in the blog so the card doesn't depend on the other site later.
Pages that block scripts (or have no preview tags) still get a card with whatever was found;
edit the printed line by hand if needed.
"""
import argparse, hashlib, html, re, shutil, subprocess, sys, time, urllib.error, urllib.request
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "static" / "img" / "linkcards"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"


class Meta(HTMLParser):
    def __init__(self):
        super().__init__(); self.meta = {}; self.title = ""; self._in_title = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "meta":
            key = (a.get("property") or a.get("name") or "").lower()
            if key and a.get("content") and key not in self.meta:
                self.meta[key] = a["content"].strip()
        elif tag == "title":
            self._in_title = True

    def handle_endtag(self, tag):
        if tag == "title": self._in_title = False

    def handle_data(self, data):
        if self._in_title: self.title += data


class Dead(Exception):
    """The page is gone (404/410) or its domain no longer resolves."""


def get(url, lang, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": lang})
    for attempt in range(2):
        time.sleep(1.0)                      # be polite; GitHub rate-limits bursts
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = r.read(4_000_000)
                return (data, r.headers.get("Content-Type", "")) if binary else data.decode(r.headers.get_content_charset() or "utf-8", "ignore")
        except urllib.error.HTTPError as e:
            if e.code in (404, 410): raise Dead(f"HTTP {e.code}")
            if e.code in (429, 503) and attempt == 0: time.sleep(8); continue
            raise
        except urllib.error.URLError as e:
            if "getaddrinfo" in str(e.reason) or "Name or service not known" in str(e.reason): raise Dead("domain does not resolve")
            raise


def ffmpeg():
    exe = shutil.which("ffmpeg")
    if exe: return exe
    for p in Path.home().glob("AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg*/*/bin/ffmpeg.exe"):
        return str(p)
    return None


def shrink(path):
    """Card images are small: re-encode anything over 120 KB as a JPEG at most 640 px wide (needs ffmpeg)."""
    exe = ffmpeg()
    if not exe or path.suffix in (".svg", ".gif") or path.stat().st_size < 120_000:
        return path.name
    out = path.with_suffix(".jpg") if path.suffix != ".jpg" else path.with_name(path.stem + ".tmp.jpg")
    r = subprocess.run([exe, "-hide_banner", "-loglevel", "error", "-y", "-i", str(path), "-vf", "scale='min(640,iw)':-2", "-q:v", "4", str(out)])
    if r.returncode != 0 or not out.exists():
        return path.name
    if out.name.endswith(".tmp.jpg"):
        out.replace(path); return path.name
    path.unlink(); return out.name


def clean(s, limit):
    s = re.sub(r"\s+", " ", html.unescape(s or "")).strip()
    return s if len(s) <= limit else s[:limit - 1].rstrip() + "…"


def attr(s):
    return s.replace('"', "&quot;")


def card(url, lang, want_image=True, fallback_title=""):
    """The shortcode for url, or None if the page is dead (keep the plain link and fix it by hand)."""
    try:
        page = get(url, lang)
    except Dead as e:
        print(f"# DEAD {url}: {e}", file=sys.stderr); return None
    except Exception as e:
        print(f"# could not fetch {url}: {e} (using the link text)", file=sys.stderr); page = ""
    p = Meta(); p.feed(page)
    m = p.meta
    title = clean(m.get("og:title") or m.get("twitter:title") or p.title or fallback_title, 120)
    desc = clean(m.get("og:description") or m.get("twitter:description") or m.get("description"), 200)
    site = clean(m.get("og:site_name"), 60)
    img_url = m.get("og:image") or m.get("og:image:url") or m.get("twitter:image")
    image = ""
    if want_image and img_url:
        img_url = urljoin(url, html.unescape(img_url))
        try:
            data, ctype = get(img_url, lang, binary=True)
            ext = {"image/png": ".png", "image/jpeg": ".jpg", "image/webp": ".webp", "image/gif": ".gif", "image/svg+xml": ".svg"}.get(ctype.split(";")[0].strip())
            ext = ext or (Path(urlparse(img_url).path).suffix.lower() if Path(urlparse(img_url).path).suffix.lower() in (".png", ".jpg", ".jpeg", ".webp", ".gif") else ".jpg")
            name = re.sub(r"[^a-z0-9]+", "-", (urlparse(url).netloc + urlparse(url).path).lower()).strip("-")[:48]
            name = f"{name}-{hashlib.sha1(url.encode()).hexdigest()[:6]}{ext}"
            OUT.mkdir(parents=True, exist_ok=True)
            (OUT / name).write_bytes(data)
            name = shrink(OUT / name)
            image = f"/img/linkcards/{name}"
        except Exception as e:
            print(f"# image failed for {url}: {e}", file=sys.stderr)
    parts = [f'url="{attr(url)}"']
    if title: parts.append(f'title="{attr(title)}"')
    if desc: parts.append(f'desc="{attr(desc)}"')
    if site: parts.append(f'site="{attr(site)}"')
    if image: parts.append(f'image="{image}"')
    return "{{< linkcard " + " ".join(parts) + " >}}"


LINK_LINE = re.compile(r"^(?:- )?(?:\[(?P<text>[^\]]+)\]\((?P<url1>https?://[^)\s]+)\)|<(?P<url2>https?://[^>\s]+)>)\s*$")


def replace_in(path, want_image=True):
    """Turn every line that is just one link (a list item or a paragraph) into a card, outside code blocks."""
    p = Path(path); lines = p.read_text(encoding="utf-8").split("\n")
    lang = "zh-CN,zh;q=0.9" if "/zh/" in p.as_posix() else "en-US,en;q=0.8"
    fence, n = False, 0
    for i, line in enumerate(lines):
        if line.lstrip().startswith("```"): fence = not fence; continue
        m = None if fence else LINK_LINE.match(line)
        if m:
            c = card(m.group("url1") or m.group("url2"), lang, want_image, fallback_title=m.group("text") or "")
            if c:
                lines[i] = c; n += 1
                print(f"  {c[:110]}…")
    # cards are blocks: separate consecutive ones by a blank line
    text = re.sub(r"(\{\{< linkcard [^\n]*>\}\})\n(?=\{\{< linkcard)", r"\1\n\n", "\n".join(lines))
    p.write_text(text, encoding="utf-8", newline="\n")
    print(f"{p}: {n} link(s) turned into cards")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("urls", nargs="*")
    ap.add_argument("--lang", default="en-US,en;q=0.8")
    ap.add_argument("--no-image", action="store_true")
    ap.add_argument("--replace", nargs="+", metavar="FILE", help="turn single-link list lines in these posts into cards")
    a = ap.parse_args()
    for f in a.replace or []:
        replace_in(f, not a.no_image)
    for u in a.urls:
        print(card(u, a.lang, not a.no_image) or f"# {u} is dead; no card")
