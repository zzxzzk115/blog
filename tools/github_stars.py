"""Refresh data/github_stars.json: star counts for the GitHub repos the project cards link to.

    python tools/github_stars.py          # GITHUB_TOKEN in the environment raises the API rate limit (optional)

Reads data/projects.json and data/projects_extra.json, takes each card's GitHub repo (its "Source" link, else the
first GitHub link, else `page`, else data/projects_repos.toml), asks the GitHub API for stargazers_count and
writes {"owner/repo": stars}.
The deploy workflow runs it before every build; a failed request keeps the previous count.
"""
import json, os, re, sys, tomllib, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "github_stars.json"
REPO = re.compile(r"^https?://github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)")


_over = ROOT / "data" / "projects_repos.toml"
OVERRIDES = tomllib.loads(_over.read_text(encoding="utf-8")) if _over.exists() else {}


def repo_of(p):
    links = [l.get("href", "") for l in p.get("links") or []]
    src = [l.get("href", "") for l in p.get("links") or [] if l.get("label") == "Source"]
    for href in src + links + [p.get("page", "")]:
        m = REPO.match(href or "")
        if m:
            return f"{m.group(1)}/{m.group(2).removesuffix('.git')}"
    return OVERRIDES.get(p.get("id"))


def main():
    projects = []
    for name in ("projects.json", "projects_extra.json"):
        f = ROOT / "data" / name
        if f.exists():
            projects += json.loads(f.read_text(encoding="utf-8"))
    repos = sorted({r for r in map(repo_of, projects) if r}, key=str.lower)
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
