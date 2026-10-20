# Structural-Systematic Philosophy — Premium Redesign

Static, responsive website for Alan White: seven main pages plus three complete original articles and a custom 404 page. The homepage includes research entry points, author biography, four-book showcase, TAPTOE feature, review and recent writing.

## Editing

- Page content lives in `src/pages/*.html`. Each file starts with a `<!-- title: … | desc: … -->` comment.
- The shared header, footer and `<head>` are in `tools/build.py`. The build also writes `sitemap.xml`, `robots.txt`, the 404 page and the JSON-LD structured data.
- Set the `SITE_URL` environment variable before building for a different domain; canonical, Open Graph and sitemap URLs follow it.
- After editing, run `python tools/build.py` to regenerate the root `*.html` files.
- Hero images are written as `<!--hero:NAME|alt text|page-hero-img-->`. The build expands this into a `<picture>` with WebP, a JPG fallback, and a mobile crop (`NAME-m`).
- Any `<img src="assets/img/X.jpg">` is wrapped in a `<picture>` with `X.webp` automatically when that file exists.
- Styles: `styles.css`. The site is light-only; colors are tokens at the top.
- Behaviour (menu, blog search, CV scrollspy, lightbox, reveal, parallax): `script.js`.
- Fonts (Cormorant Garamond, EB Garamond, latin subset) are self-hosted in `assets/fonts/`.

## Assets

- `assets/img/` holds the optimized images the site uses, each as WebP plus a JPG fallback.
- Heroes are 2000px wide for retina screens, with 900×760 mobile crops.
- The AI photos share one color grade: matte tone curve, warm split tone, soft vignette and fine grain. Real photos are left ungraded.
- Photos were AI-generated with Figma AI (gpt-image-2.5-sunburst; originals in `source-images/v2/`). Thumbnails and book-cover backgrounds are crops of those images.
- `og.jpg` (1200×630) is the social-share image.
- `alan-white.jpg`, `cover-taptoe.jpg`, `cover-taptoe-back.jpg` and `tolkien-letter.jpg` are real images from the source site.
- `geometry.svg` and `cover-structure.svg` are hand-made vector art.
- `source-images/` holds the full-size originals. It is not needed for deployment.

## Deploy

Run `python tools/build.py` and `python tools/check.py`. Upload the contents of `dist/` to a static host. The build includes aliases for original routes such as `/blog/` and full article URLs. Configure the host to serve `404.html` for missing pages. No installation or external font service is needed.

Original page and article content snapshots are in `tools/source-content/`. The three articles preserve source HTML, including footnotes and lists. All seven main pages, source resource links and original images have been retained; the original CV is also available locally. `CONTENT-AUDIT.json` records local link checks and source limitations. The old history PDF returns 404; its original link remains alongside the updated 2025 paper. Some Williams College PDF URLs return 403 to automated downloads and remain external. The source corrigenda contain replacement characters, preserved verbatim.
