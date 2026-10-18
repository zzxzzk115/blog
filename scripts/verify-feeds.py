"""Validate the production feeds without requiring third-party Python packages."""

import json
from datetime import datetime
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree as ET

DIST = Path(__file__).resolve().parents[1] / "src/.vuepress/dist"
ORIGIN = "https://zzxzzk115.github.io"
ATOM = "{http://www.w3.org/2005/Atom}"


class FeedLinks(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.links = {}
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "link" and attrs.get("rel") == "alternate":
            self.links[attrs.get("type")] = attrs.get("href")


class ContentLinks(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        for name, url in attrs:
            if name in ("href", "src") and url:
                parsed = urlsplit(url)
                assert parsed.scheme, f"Relative URL in feed: {url}"
                if parsed.netloc == urlsplit(ORIGIN).netloc and parsed.path.startswith("/blog/"):
                    local_target(url)


def local_target(url):
    parsed = urlsplit(url)
    assert f"{parsed.scheme}://{parsed.netloc}" == ORIGIN, url
    assert parsed.path.startswith("/blog/"), url
    path = (DIST / unquote(parsed.path.removeprefix("/blog/"))).resolve()
    assert path.is_relative_to(DIST.resolve()), url
    if path.is_dir():
        path /= "index.html"
    assert path.is_file(), f"Missing output for {url}"
    return path


for locale, language in (("", "en-US"), ("zh/", "zh-CN")):
    root = DIST / locale
    base = f"{ORIGIN}/blog/{locale}"
    feed = json.loads((root / "feed.json").read_text())
    assert feed["version"] == "https://jsonfeed.org/version/1.1"
    assert feed["title"] and feed["home_page_url"] == base
    assert feed["feed_url"] == base + "feed.json"
    items = feed["items"]
    assert items, f"Empty feed: {locale}"
    ids = [item["id"] for item in items]
    assert len(ids) == len(set(ids)), "Duplicate feed IDs"
    dates = [datetime.fromisoformat(item["date_published"].replace("Z", "+00:00"))
             for item in items]
    assert dates == sorted(dates, reverse=True), "Feed must be newest first"

    rss = ET.parse(root / "rss.xml").getroot()
    channel = rss.find("channel")
    assert rss.tag == "rss" and rss.attrib["version"] == "2.0"
    assert channel.findtext("link") == base
    assert channel.findtext("language") == language
    assert channel.find(f"{ATOM}link").attrib["href"] == base + "rss.xml"
    rss_items = channel.findall("item")
    assert [item.findtext("guid") for item in rss_items] == ids
    assert [item.findtext("link") for item in rss_items] == [item["url"] for item in items]
    assert [parsedate_to_datetime(item.findtext("pubDate")) for item in rss_items] == dates

    atom = ET.parse(root / "atom.xml").getroot()
    assert atom.tag == ATOM + "feed" and atom.findtext(ATOM + "id") == base
    assert atom.find(f"{ATOM}link[@rel='self']").attrib["href"] == base + "atom.xml"
    assert [item.findtext(ATOM + "id") for item in atom.findall(ATOM + "entry")] == ids
    for stylesheet in ("rss.xsl", "atom.xsl"):
        ET.parse(root / stylesheet)

    for item in items:
        assert item["title"] and item["content_html"], item["id"]
        ContentLinks(item["content_html"])
        assert item["url"].startswith(base), item["url"]
        assert urlsplit(item["url"]).path.startswith("/blog/zh/") == bool(locale)
        html = local_target(item["url"]).read_text()
        links = FeedLinks(html).links
        for filename, mime in (("rss.xml", "application/rss+xml"),
                               ("atom.xml", "application/atom+xml"),
                               ("feed.json", "application/json")):
            assert links[mime] == base + filename, item["url"]
    home_links = FeedLinks((root / "index.html").read_text()).links
    assert home_links["application/rss+xml"] == base + "rss.xml"
    print(f"{language}: {len(items)} articles; JSON, RSS, Atom, discovery and links verified")
