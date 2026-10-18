
# MyBlog

My personal blog, based on VuePress theme Hope.

## Getting Started

### 1. Install dependencies

CI uses Node 24 and `npm ci` with the committed `package-lock.json`. Use the
same command for a reproducible local installation; commit lockfile updates
when changing dependencies.

```bash
npm ci
# or
yarn install
# or
pnpm install
```

### 2. Start local development

```bash
pnpm docs:dev
# or
yarn docs:dev
# or
npm run docs:dev
```

### 3. Build static site

```bash
pnpm docs:build
# or
yarn docs:build
# or
npm run docs:build
```

### 4. Clean cache (if needed)

```bash
pnpm docs:clean-dev
# or
yarn docs:clean-dev
# or
npm run docs:clean-dev
```

### 5. Update theme & dependencies

```bash
pnpm docs:update-package
# or
yarn docs:update-package
# or
npm run docs:update-package
```

## Publishing

Pull requests build the site and validate its feeds. Pushes to `master` also
deploy the built artifact through GitHub Pages using the workflow's short-lived
`GITHUB_TOKEN` and OIDC identity. No personal access token is required.

In repository Settings → Pages, choose **GitHub Actions** as the publishing
source. The `github-pages` environment must allow deployments from `master`.

## Feeds

English feeds are published under `/blog/`, and Chinese feeds under `/blog/zh/`.
Each locale provides `rss.xml`, `atom.xml`, and `feed.json`; pages advertise
their locale's feeds to readers. The navigation also links to RSS.

Feeds include article pages, excluding home pages and pages marked
`article: false`, `feed: false`, or `draft: true`. Articles are ordered by their frontmatter
`date`, falling back to git creation time. Translations keep the original
publication date; git modification times record subsequent updates.
Feed content uses absolute article and image URLs, including the `/blog/` base,
so readers can load embedded images independently of the website.

After a production build, run `python3 scripts/verify-feeds.py` to check both
locales, feed formats, publication dates, discovery links, and article targets.
The portfolio consumes the English JSON Feed; its saved fallback is maintained
in the separate portfolio repository.
