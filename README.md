# Structural-Systematic Philosophy — Premium Redesign

Static, responsive website for Alan White: seven main pages plus three complete original articles and a custom 404 page. The homepage includes research entry points, author biography, four-book showcase, TAPTOE feature, review and recent writing.

## Editing

- Page content lives in `src/pages/*.html`. Each file starts with a `<!-- title: … | desc: … -->` comment.
- The shared header, footer and `<head>` are in `tools/build.py`. The build also writes `sitemap.xml`, `robots.txt`, the 404 page and the JSON-LD structured data.
- Set the `SITE_URL` environment variable before building for a different domain; canonical, Open Graph and sitemap URLs follow it.
- After editing, run `python tools/build.py` to regenerate the root `*.html` files.
- Hero images are written as `<!--hero:NAME|alt text|page-hero-img-->`. The build expands this into a `<picture>` with WebP, a JPG fallback, and a mobile crop (`NAME-m`).
- Any `<img src="assets/img/X.jpg">` is wrapped in a `<picture>` with `X.webp` automatically when that file exists.
- Styles: `styles.css` is the base; `premium.css` contains the editorial design and responsive layouts; `showcase.css` styles the cinematic home slider and the image-led discovery cards.
- Behaviour (accessible menu, combined blog search and topic filters, CV scrollspy, image preview, reading progress and printing): `script.js`. The three-slide homepage carousel lives in `showcase.js`, with 7.5 second rotation, pause/play, previous/next, numbered controls, keyboard arrows and swipe. Rotation pauses on hover, keyboard focus, when offscreen or when the tab is hidden. Reduced-motion visitors start with autoplay off.
- Google Sans is the single site-wide typeface, loaded from the supplied Google Fonts URL. The shared `--font-site` token controls headings, body, labels and form controls. System sans-serif fonts are the fallback when offline.

## Assets

- Discovery carousel: Swiper 14.3.0, with two complete cards on desktop and one on narrower screens, drag/swipe, navigation, numbered pagination and pause/play. GSAP 3.13.0 with ScrollTrigger handles card transitions, scroll reveals and hover motion. Bundles are stored locally in `assets/vendor/` and retain their copyright/license headers. The integration is in `motion.js` and `motion.css`; reduced-motion preferences are respected. Run `node tools/check-motion.cjs` for controller checks. When scripts are unavailable, all three cards remain in a static grid.

- `assets/img/` holds the optimized images the site uses, each as WebP plus a JPG fallback.
- Active heroes and cards use photographic library, writing, book and podcast scenes. Three refined panoramic scenes are 1881×836; the publications scene is 1536×1024. CSS frames the subject for each viewport.
- Current imagery was created/edited with the built-in image-generation tool. Exact prompts, edit references and provenance are in `IMAGE-PROMPTS.md`; original PNGs are preserved under `source-images/generated/`.
- The social-share image uses `library-v2.jpg`.
- `alan-white.jpg`, `cover-taptoe.jpg`, `cover-taptoe-back.jpg` and `tolkien-letter.jpg` are real images from the source site.
- `geometry.svg` and `cover-structure.svg` are hand-made vector art.
- `source-images/` holds the full-size originals. It is not needed for deployment.

## Deploy

Run `python tools/build.py`, `python tools/check.py` and `node tools/check-interactions.cjs`. Upload the contents of `dist/` to a static host. The build includes aliases for original routes such as `/blog/` and full article URLs. Configure the host to serve `404.html` for missing pages. No installation is needed. Google Sans loads through Google Fonts; an offline system sans-serif fallback is provided.

Original page and article content snapshots are in `tools/source-content/`. The three articles preserve source HTML, including footnotes and lists. All seven main pages, source resource links and original images have been retained; the original CV is also available locally. `CONTENT-AUDIT.json` records local link checks and source limitations. The old history PDF returns 404; its original link remains alongside the updated 2025 paper. Some Williams College PDF URLs return 403 to automated downloads and remain external. The source corrigenda contain replacement characters, preserved verbatim.

Discovery layout fix: centered coverflow and looping were replaced with a standard slide transition and rewind. Desktop slides use a fixed-height image/text layout; mobile slides stack the image and text. Overflow is contained so adjacent cards cannot spill outside the section.

Inner-page refinement: `inner-pages.css` unifies all interior heroes, the even three-column blog catalogue, grouped CV timelines and book records, and a link-led podcast feature with a responsive platform grid. The unavailable Spotify iframe was removed; its original show URL is retained as an external button. External show/feed availability is controlled by the original providers.

New active imagery: four matching library, writing, publications and podcast scenes were generated with the built-in image-generation tool. Optimized exports are `assets/img/generated-*.webp` and `.jpg`. Complete prompts and provenance are in `IMAGE-PROMPTS.md`. Original PNGs are preserved in `source-images/generated/`; the original author portrait, TAPTOE covers and Tolkien letter remain unchanged.

Imagery refinement (20 October 2026): `library-v2`, `research-v2` and `podcast-v2` replace the earlier scenes with wider, more realistic compositions. Homepage hero slides and discovery cards now use contextual photography; the original Alan White portrait remains in About and the genuine TAPTOE covers remain in the book showcase. Blog corrigenda no longer use a microphone image; listening-platform thumbnails consistently use the recording setup. Exports retain the complete generated composition. Written page content and original resource links are unchanged.
