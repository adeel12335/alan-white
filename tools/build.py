"""Build the static site: wraps each src/pages/*.html body in the shared layout,
then writes sitemap.xml and robots.txt.

Each page file starts with a front-matter comment:
<!-- title: Blog | desc: ... -->
Run:  python tools/build.py
"""
import json
import re
import os
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / "src" / "pages"
IMG = ROOT / "assets" / "img"

# Change this if the site is deployed on a different domain.
SITE_URL = os.environ.get("SITE_URL", "https://structural-systematic-philosophy-alan-white.thewikistudioltd.chatgpt.site").rstrip('/')

NAV = [
    ("index.html", "Home"),
    ("blog.html", "Blog"),
    ("cv.html", "CV"),
    ("extras.html", "Extras"),
    ("podcasts.html", "Podcasts"),
    ("publications.html", "Publications"),
    ("recent-posts.html", "Recent Posts"),
]
SUBTITLE = "Mark Hopkins Professor of Philosophy, Williams College"

ARROW_UP = ('<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="1.5" aria-hidden="true"><path d="M12 20V4M5 11l7-7 7 7"/></svg>')
LAYOUT = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
{base}<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Structural-Systematic Philosophy">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{site}/assets/img/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="color-scheme" content="light">
<meta name="theme-color" content="#f8f4ec">
<link rel="icon" href="assets/img/geometry.svg" type="image/svg+xml">
<link rel="preload" href="assets/fonts/cormorant.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/eb-garamond.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="styles.css">
{jsonld}</head>
<body id="top">
<div class="reading-progress" aria-hidden="true"></div>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap nav">
    <a class="brand" href="index.html"><strong>Alan White</strong><span>{subtitle}</span></a>
    <nav class="menu" aria-label="Main">{nav}<p class="menu-foot">{subtitle}</p></nav>
    <div class="nav-tools">
      <button class="mobile-toggle" type="button" aria-label="Menu" aria-expanded="false"><span></span><span></span></button>
    </div>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="footer">
  <div class="wrap">
    <div class="footer-top">
      <p class="footer-mark">Structural-Systematic <em>Philosophy</em></p>
      <a class="to-top" href="#top" aria-label="Back to top">{arrow}</a>
    </div>
    <div class="footer-grid">
      <a class="brand" href="index.html"><strong>Alan White</strong><span>{subtitle}</span></a>
      <nav class="footer-nav" aria-label="Footer">{footer_nav}</nav>
    </div>
    <p class="footer-credit">Original website by <a href="https://www.onebricktech.com" target="_blank" rel="noopener">One Brick Tech</a></p>
  </div>
</footer>
<a class="float-top" href="#top" aria-label="Back to top">{arrow}</a>
<script src="script.js"></script>
</body>
</html>
"""

PERSON = {
    "@type": "Person",
    "@id": f"{SITE_URL}/#alan-white",
    "name": "Alan White",
    "jobTitle": "Mark Hopkins Professor of Philosophy",
    "affiliation": {"@type": "CollegeOrUniversity", "name": "Williams College"},
    "url": f"{SITE_URL}/",
    "image": f"{SITE_URL}/assets/img/alan-white.jpg",
    "sameAs": ["http://sites.williams.edu/awhite/"],
}


def book(name, year, publisher=None, author=None):
    b = {"@type": "Book", "name": name, "datePublished": str(year),
         "author": author or {"@id": PERSON["@id"]}}
    if publisher:
        b["publisher"] = {"@type": "Organization", "name": publisher}
    return b


JSONLD = {
    "index.html": [
        {"@type": "WebSite", "name": "Structural-Systematic Philosophy", "url": f"{SITE_URL}/"},
        PERSON,
    ],
    "publications.html": [
        PERSON,
        book("Toward a Philosophical Theory of Everything. Contributions to the Structural-Systematic Philosophy",
             2014, "Bloomsbury"),
        book("Within Nietzsche’s Labyrinth", 1990, "Routledge"),
        book("Absolute Knowledge. Hegel and the Problem of Metaphysics", 1983, "Ohio University Press"),
        book("Schelling. An Introduction to the System of Freedom", 1983, "Yale University Press"),
        book("Nothing Matters. A Philosophical Romance", 2011),
        book("Revenge", 2011),
    ],
    "cv.html": [PERSON],
}


def hero_picture(m):
    """<!--hero:NAME|alt|class--> -> responsive <picture> with WebP and a mobile crop."""
    name, alt, cls = m.group(1), m.group(2), m.group(3)
    return (f'<picture class="{cls}">'
            f'<source media="(max-width:900px)" srcset="assets/img/{name}-m.webp" type="image/webp">'
            f'<source media="(max-width:900px)" srcset="assets/img/{name}-m.jpg">'
            f'<source srcset="assets/img/{name}.webp" type="image/webp">'
            f'<img src="assets/img/{name}.jpg" alt="{alt}" fetchpriority="high" decoding="async"></picture>')


def webp_img(m):
    """Wrap <img src="assets/img/X.jpg"> in <picture> when X.webp exists."""
    tag, name = m.group(0), m.group(1)
    if not (IMG / f"{name}.webp").exists():
        return tag
    return f'<picture><source srcset="assets/img/{name}.webp" type="image/webp">{tag}</picture>'


def webp_bg(m):
    name = m.group(1)
    if not (IMG / f"{name}.webp").exists():
        return m.group(0)
    return (f'background-image:url(assets/img/{name}.jpg);'
            f'background-image:image-set(url(assets/img/{name}.webp) type("image/webp"),url(assets/img/{name}.jpg) type("image/jpeg"))')


def page_url(out):
    return f"{SITE_URL}/" if out == "index.html" else f"{SITE_URL}/{out}"


def build():
    built = []
    for src in sorted(PAGES.glob("*.html")):
        text = src.read_text(encoding="utf-8")
        m = re.match(r"\s*<!--\s*title:\s*(.*?)\s*\|\s*desc:\s*(.*?)\s*-->\s*", text, re.S)
        if not m:
            raise SystemExit(f"{src.name}: missing front-matter comment")
        title, desc, body = m.group(1), m.group(2), text[m.end():]
        out = src.name
        body = re.sub(r'<img src="assets/img/([\w-]+)\.jpg"[^>]*>', webp_img, body)
        body = re.sub(r"<!--hero:([\w-]+)\|(.*?)\|([\w -]+)-->", hero_picture, body)
        body = re.sub(r"background-image:url\(assets/img/([\w-]+)\.jpg\)", webp_bg, body)
        nav = "".join(
            f'<a href="{href}"{" class=\"active\" aria-current=\"page\"" if href == out else ""}>{label}</a>'
            for href, label in NAV
        )
        footer_nav = "".join(f'<a href="{href}">{label}</a>' for href, label in NAV)
        graph = JSONLD.get(out)
        jsonld = ('<script type="application/ld+json">'
                  + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
                  + "</script>\n") if graph else ""
        is404 = out == "404.html"
        html = LAYOUT.format(
            title=title, desc=desc, subtitle=SUBTITLE, nav=nav, footer_nav=footer_nav,
            body=body.rstrip(), url=page_url(out), site=SITE_URL, jsonld=jsonld,
            arrow=ARROW_UP,
            # the 404 page is served from any path, so resolve its links from the site root
            base='<base href="/">\n<meta name="robots" content="noindex">\n' if is404 else "",
        )
        (ROOT / out).write_text(html, encoding="utf-8")
        if not is404:
            built.append(out)
        print("built", out)

    today = date.today().isoformat()
    urls = "".join(f"  <url><loc>{page_url(o)}</loc><lastmod>{today}</lastmod></url>\n"
                   for o in sorted(built, key=lambda o: (o != "index.html", o)))
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n",
        encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n",
                                     encoding="utf-8")
    print("built sitemap.xml, robots.txt")
    dist = ROOT / 'dist'
    dist.mkdir(exist_ok=True)
    for name in [*built, '404.html', 'styles.css', 'script.js', 'sitemap.xml', 'robots.txt']:
        shutil.copy2(ROOT / name, dist / name)
    shutil.copytree(ROOT / 'assets', dist / 'assets', dirs_exist_ok=True)
    # Retain original WordPress-style routes when hosted on a static server.
    for name in built:
        if name == 'index.html':
            continue
        alias = dist / Path(name).stem
        alias.mkdir(exist_ok=True)
        (alias / 'index.html').write_text((ROOT / name).read_text(encoding='utf-8').replace('<head>', '<head>\n<base href="/">', 1), encoding='utf-8')
    (dist / '_headers').write_text('/assets/*\n  Cache-Control: public, max-age=31536000\n/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  X-Frame-Options: SAMEORIGIN\n', encoding='utf-8')
    print('Packaged production files in dist/')


if __name__ == "__main__":
    build()
