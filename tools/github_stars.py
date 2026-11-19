"""Refresh data/github_stars.json: star counts for the GitHub repos of the blog's project cards.

    python tools/catalog.py && python tools/github_stars.py   # GITHUB_TOKEN raises the API rate limit (optional)

Reads the `repo` of each card in data/projects.json (generated from the project catalog by tools/catalog.py),
asks the GitHub API for stargazers_count and writes {"owner/repo": stars}. The deploy workflow runs it before
every build; a failed request keeps the previous count.
"""
import json, os, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "github_stars.json"


def main():
    cards = json.loads((ROOT / "data" / "projects.json").read_text(encoding="utf-8"))
    repos = sorted({c["repo"] for c in cards if c.get("repo")}, key=str.lower)
    old = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    headers = {"User-Agent": "blog-github-stars", "Accept": "application/vnd.github+json"}
    if os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    stars, failed = {}, 0
    for r in repos:
        try:
            req = urllib.request.Request(f"https://api.github.com/repos/{r}", headers=headers)
            with urllib.request.urlopen(req, timeout=20) as resp:
                stars[r] = json.load(resp)["stargazers_count"]
        except Exception as e:  # keep the last known count
            failed += 1
            print(f"  {r}: {e}", file=sys.stderr)
            if r in old:
                stars[r] = old[r]
    OUT.write_text(json.dumps(stars, indent=1, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {OUT.relative_to(ROOT)}: {len(stars)} repos, {failed} failed")


if __name__ == "__main__":
    main()
