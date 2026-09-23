"""Build the project pages and the tile grid from projects/projects.json.

    python tools/build_projects.py

Writes projects/<slug>/index.html for every project, rewrites the block between
<!-- projects:tiles --> and <!-- /projects:tiles --> in index.html, and writes
sitemap.xml. Run it after editing projects.json; the generated pages are committed.
"""
import datetime
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "projects", "projects.json")
CSS_VERSION = "26"

NAV_LINKS = ["about", "research", "education", "publications", "awards", "projects", "contact"]


def e(s):
    return html.escape(s, quote=True)


def chips(p, with_lang=True):
    out = []
    for label, cls in p["kinds"]:
        out.append(f'<span class="chip {cls}">{e(label)}</span>')
    for label, cls in p["mods"]:
        out.append(f'<span class="chip chip-mod {cls}">{e(label)}</span>')
    if with_lang:
        for label, cls in p["langs"]:
            out.append(f'<span class="chip {cls}">{e(label)}</span>')
    return "".join(out)


def tile(p, prefix=""):
    vis_cls = "vis-public" if p["visibility"] == "Public" else "vis-private"
    name = e(p["name"]) + (f' <span class="tile-sub">{e(p["subtitle"])}</span>' if p.get("subtitle") else "")
    return f"""      <li>
        <a class="tile" href="{prefix}projects/{p['slug']}/">
          {thumb_html(p['slug'], prefix)}
          <div class="tile-body">
            <h3 class="tile-title">{name}</h3>
            <p class="tile-blurb">{e(p['blurb'])}</p>
            <div class="tile-meta">
              <span class="tag {vis_cls}">{e(p['visibility'])}</span>
              <span class="project-year">{e(p['year'])}</span>
            </div>
            <div class="chips">{chips(p)}</div>
          </div>
        </a>
      </li>"""


def tiles_block(data):
    parts = []
    for g in data["groups"]:
        group = [p for p in data["projects"] if p["group"] == g["key"]]
        parts.append(f'    <h3 class="more-heading">{e(g["label"])}</h3>\n    <ul class="tiles">\n'
                     + "\n".join(tile(p) for p in group) + "\n    </ul>")
    return "\n".join(parts)


def dims(name):
    """width and height attributes for an image under assets/projects, read from the file."""
    from PIL import Image
    with Image.open(os.path.join(ROOT, "assets", "projects", name)) as im:
        return f'width="{im.width}" height="{im.height}"'


# Rendered widths, measured at every breakpoint: below 761 px a figure spans the page
# less 66 px of frame and padding; up to 992 px the hero spans it less 138 px and a
# gallery figure takes half of that; past 992 px both stop growing.
HERO_SIZES = "(max-width: 760px) calc(100vw - 66px), (max-width: 992px) calc(100vw - 138px), 854px"
GRID_SIZES = "(max-width: 760px) calc(100vw - 66px), (max-width: 992px) calc(50vw - 76px), 420px"


def srcset(stem, prefix):
    """srcset over <stem>.webp and the narrower copies site_thumbs.py wrote beside it."""
    from PIL import Image
    out = []
    for name in (f"{stem}-700.webp", f"{stem}-1000.webp", f"{stem}.webp"):
        path = os.path.join(ROOT, "assets", "projects", name)
        if os.path.exists(path):
            with Image.open(path) as im:
                out.append(f"{prefix}assets/projects/{name} {im.width}w")
    return ", ".join(out)


def picture(light, dark, prefix, attrs, sizes=None):
    """An image in the palette on screen, fetched once.

    `light` and `dark` are file stems under assets/projects; `dark` may be None. With
    `sizes`, each palette gets a srcset of its widths; without, the file is used as is.
    The dark <source> matches a dark system, which is exactly when the site starts in
    night, and site.js pins it to the theme actually shown, so the other palette's file
    is never requested unless the reader switches themes."""
    def files(stem):
        if sizes:
            return f'srcset="{srcset(stem, prefix)}" sizes="{sizes}"'
        return f'srcset="{prefix}assets/projects/{stem}.webp"'
    img_files = f' srcset="{srcset(light, prefix)}" sizes="{sizes}"' if sizes else ""
    img = f'<img src="{prefix}assets/projects/{light}.webp"{img_files} {attrs}>'
    if not dark:
        return img
    return f'<picture><source media="(prefers-color-scheme: dark)" {files(dark)} data-dark>{img}</picture>'


def figure_html(fig, prefix, cls="project-figure", hero=False):
    # the hero is the largest thing above the fold, so it loads eagerly and first;
    # every other figure waits until it is near the viewport
    load = 'fetchpriority="high" decoding="async"' if hero else 'loading="lazy" decoding="async"'
    light = fig["light"][:-len(".webp")]
    dark = fig["dark"][:-len(".webp")] if fig.get("dark") else None
    attrs = f'alt="{e(fig["alt"])}" {dims(fig["light"])} {load}'
    img = picture(light, dark, prefix, attrs, HERO_SIZES if hero else GRID_SIZES)
    return f'<figure class="{cls}">{img}<figcaption>{e(fig["caption"])}</figcaption></figure>'


def thumb_html(slug, prefix, load='loading="lazy" decoding="async"', cls="tile-thumb"):
    """The 800 x 500 thumbnail, night plate by night and parchment plate by day."""
    cls_attr = f'class="{cls}" ' if cls else ""
    return picture(f"{slug}-day", slug, prefix, f'{cls_attr}width="800" height="500" {load} alt=""')


def head(title, description, canonical, image, prefix):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{e(title)}</title>
  <meta name="description" content="{e(description)}">
  <meta name="author" content="Yuhyeon Lee">
  <meta name="theme-color" content="#0c0d0b">
  <link rel="canonical" href="{canonical}">

  <meta property="og:type" content="article">
  <meta property="og:site_name" content="Yuhyeon Lee">
  <meta property="og:locale" content="en_US">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(description)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{image}">
  <meta property="og:image:width" content="800">
  <meta property="og:image:height" content="500">
  <meta name="twitter:card" content="summary_large_image">

  <link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="{prefix}favicon.ico" sizes="16x16 32x32 48x48">
  <link rel="apple-touch-icon" href="{prefix}assets/apple-touch-icon.png">

  <link rel="preload" href="{prefix}assets/fonts/besley-core.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="{prefix}assets/fonts/ibmplexmono-400.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="{prefix}assets/fonts/archivo-core.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="{prefix}assets/style.css?v={CSS_VERSION}">
  <script>
    try {{
      var t = localStorage.getItem('theme');
      if (t === 'day' || (!t && window.matchMedia('(prefers-color-scheme: light)').matches)) {{
        document.documentElement.setAttribute('data-theme', 'day');
      }}
    }} catch (e) {{}}
  </script>
</head>
"""


def nav(prefix):
    links = "\n".join(f'      <a href="{prefix}#{k}">{k.capitalize()}</a>' for k in NAV_LINKS)
    home = prefix if prefix else "./"
    return f"""<a class="skip-link" href="#top">Skip to content</a>
<div class="grain" aria-hidden="true"></div>

<nav class="nav" aria-label="Primary">
  <div class="nav-inner">
    <a class="nav-brand" href="{home}">
      <span class="mark" aria-hidden="true"><span>YL</span></span>
      <span class="nav-name">Yuhyeon Lee</span>
    </a>
    <div class="nav-links">
{links}
    </div>
    <button class="theme-toggle" type="button" aria-label="Switch to day mode">&#9728;</button>
  </div>
</nav>
"""


def footer(prefix):
    return f"""<footer>
  <div class="footer-inner">
    <span class="mark mark-footer" aria-hidden="true"><span>YL</span></span>
    <span class="footer-line">&copy; MMXXVI &middot; Yuhyeon Lee &middot; Seoul</span>
    <a class="footer-src" href="https://github.com/blueion0612/blueion0612.github.io" target="_blank" rel="noopener">Source</a>
  </div>
</footer>

<script src="{prefix}assets/site.js" defer></script>

</body>
</html>
"""


def project_page(p, data, by_slug):
    prefix = "../../"
    base = data["base"]
    canonical = f"{base}/projects/{p['slug']}/"
    title = f"{p['name']} — Yuhyeon Lee"
    image = f"{base}/assets/projects/{p['slug']}.webp"
    group_label = next(g["label"] for g in data["groups"] if g["key"] == p["group"])
    vis_cls = "vis-public" if p["visibility"] == "Public" else "vis-private"

    links = []
    if p.get("github"):
        links.append(f'<a class="btn btn-primary" href="{p["github"]}" target="_blank" rel="noopener">GitHub</a>')
    if p.get("project_page"):
        links.append(f'<a class="btn" href="{p["project_page"]}" target="_blank" rel="noopener">Project page</a>')
    if p.get("paper"):
        links.append(f'<a class="btn" href="{p["paper"]}" target="_blank" rel="noopener">Paper</a>')
    links.append(f'<a class="btn" href="{prefix}#projects">All projects</a>')

    if p.get("hero"):
        hero = figure_html(p["hero"], prefix, cls="project-figure project-figure-hero", hero=True)
    else:
        plate = thumb_html(p["slug"], prefix, load='fetchpriority="high" decoding="async"', cls=None)
        hero = (f'<figure class="project-figure project-figure-hero">{plate}'
                f'<figcaption>Private repository. The code and the results stay with the sponsor.</figcaption></figure>')

    sections = []
    for s in p["sections"]:
        items = "\n".join(f"        <li>{e(i)}</li>" for i in s["items"])
        sections.append(f"""  <section class="detail">
    <div class="section-head"><h2>{e(s['title'])}</h2></div>
    <ul class="project-points">
{items}
    </ul>
  </section>""")

    facts = "\n".join(f'      <div class="fact"><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k, v in p["facts"])
    facts_html = f"""  <section class="detail">
    <div class="section-head"><h2>Facts</h2></div>
    <dl class="facts">
{facts}
    </dl>
  </section>"""

    figures_html = ""
    if p.get("figures"):
        figs = "\n".join("      " + figure_html(f, prefix) for f in p["figures"])
        figures_html = f"""  <section class="detail">
    <div class="section-head"><h2>Figures</h2></div>
    <div class="figure-grid">
{figs}
    </div>
  </section>"""

    related_html = ""
    rel = [by_slug[s] for s in p.get("related", []) if s in by_slug]
    if rel:
        items = "\n".join(
            f'      <li><a class="tile tile-small" href="{prefix}projects/{r["slug"]}/">'
            f'{thumb_html(r["slug"], prefix)}'
            f'<div class="tile-body"><h3 class="tile-title">{e(r["name"])}</h3>'
            f'<div class="tile-meta"><span class="project-year">{e(r["year"])}</span></div></div></a></li>'
            for r in rel)
        related_html = f"""  <section class="detail">
    <div class="section-head"><h2>Related</h2></div>
    <ul class="tiles tiles-small">
{items}
    </ul>
  </section>"""

    subtitle = f'\n    <p class="project-subtitle">{e(p["subtitle"])}</p>' if p.get("subtitle") else ""
    sections_html = "\n\n".join(sections)
    body = f"""<body>

{nav(prefix)}
<main id="top" class="project-page">

  <div class="frame-tacks" aria-hidden="true"><span>&#10022;</span><span>&#10022;</span><span>&#10022;</span><span>&#10022;</span></div>

  <header class="project-hero">
    <p class="hero-kicker">{e(group_label)} &middot; {e(p['year'])}</p>
    <h1>{e(p['name'])}</h1>{subtitle}
    <p class="project-lede">{e(p['lede'])}</p>
    <div class="tile-meta project-hero-meta">
      <span class="tag {vis_cls}">{e(p['visibility'])}</span>
    </div>
    <div class="chips project-hero-chips">{chips(p)}</div>
    <div class="hero-links">
      {' '.join(links)}
    </div>
  </header>

  {hero}

{sections_html}

{facts_html}

{figures_html}

{related_html}

</main>

{footer(prefix)}"""
    return head(title, p["blurb"], canonical, image, prefix) + body


def main():
    data = json.load(open(DATA, encoding="utf-8"))
    by_slug = {p["slug"]: p for p in data["projects"]}
    for p in data["projects"]:
        d = os.path.join(ROOT, "projects", p["slug"])
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8", newline="\n") as f:
            f.write(project_page(p, data, by_slug))
    idx = os.path.join(ROOT, "index.html")
    src = open(idx, encoding="utf-8", newline="").read()
    open_mark, close_mark = "<!-- projects:tiles -->", "<!-- /projects:tiles -->"
    if open_mark not in src or close_mark not in src:
        raise SystemExit("index.html has no projects:tiles markers")
    pre, rest = src.split(open_mark, 1)
    _, post = rest.split(close_mark, 1)
    new = pre + open_mark + "\n" + tiles_block(data) + "\n    " + close_mark + post
    open(idx, "w", encoding="utf-8", newline="").write(new)
    today = datetime.date.today().isoformat()
    urls = [f"{data['base']}/"] + [f"{data['base']}/projects/{p['slug']}/" for p in data["projects"]]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append(f"  <url><loc>{u}</loc><lastmod>{today}</lastmod></url>")
    sm.append("</urlset>")
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8", newline="\n").write("\n".join(sm) + "\n")
    print(f"{len(data['projects'])} project pages, tiles rewritten, sitemap with {len(urls)} URLs")


if __name__ == "__main__":
    main()
