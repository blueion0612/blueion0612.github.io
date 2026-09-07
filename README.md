# blueion0612.github.io

Personal portfolio of **Yuhyeon Lee**, Wearable Robotics & Exoskeleton Engineer.
Live at **[blueion0612.github.io](https://blueion0612.github.io)**.

Hand-written HTML and CSS, no frameworks. The one generated part is the Projects
tab: `tools/build_projects.py` reads `projects/projects.json` and writes the tile
grid into `index.html`, one page per project under `projects/<slug>/`, and
`sitemap.xml`. Everything else is edited in place and pushed.

**Design**: a wanted poster. Besley carries the name, Rye the western bands and
section keys, IBM Plex Mono the readouts and Archivo the body text. One
phosphor-green accent, brass for the stamps and the monogram, brass tacks and a
vignette over the whole page. Night is matte black with film grain, day is
parchment. First visit follows the OS color scheme; the toggle in the nav overrides
it and remembers the choice. Fonts are self-hosted under `assets/fonts/` (SIL OFL).

When editing `assets/style.css`, bump the `?v=` query on its `<link>` in
`index.html`, `404.html` and `CSS_VERSION` in `tools/build_projects.py`, then
rebuild, to bust the Pages CDN cache. It is currently at `v=24`.

## Structure

```
index.html              # the front page; the Projects tab is generated between markers
404.html                # not-found page in the same shell
projects/projects.json  # every project: tile text, detail sections, facts, figures, links
projects/<slug>/        # one generated page per project
tools/build_projects.py # generator for the tiles, the pages and sitemap.xml
assets/style.css        # all styling, both themes (print forces light)
assets/site.js          # the theme toggle
assets/fonts/           # Besley, Archivo, IBM Plex Mono, Rye as woff2, with licenses
assets/projects/        # thumbnails (800 x 500 WebP) and detail figures, built by
                        # _standards/site_thumbs.py from each repository's README figures
assets/portrait.jpg
assets/og.png           # social preview card
robots.txt, sitemap.xml, favicon.ico, assets/favicon.svg, assets/apple-touch-icon.png
```

Sections, in order: about, research, education, publications, awards, projects,
contact.

## How to update

| What | Where |
|:--|:--|
| Publications | Add an `<li>` to the `.publications` list; a paper link is a `<p class="pub-links">` with an `<a>`; swap the `.stamp` text when the status changes |
| Awards and experience | Add an `<li>` to `.awards`; sub-points go in a nested `ul.award-points` inside the `div.award-body` |
| New project | Add an entry to `projects/projects.json`, add its images to `_standards/site_thumbs.py` and run it, then run `python tools/build_projects.py` |
| Project links | `github`, `project_page` and `paper` in the JSON; a null is simply not rendered, so a dedicated project page or a paper appears as soon as its URL is filled in |
| Google Scholar | Add a `.btn` to the hero links once a paper is published |
| Photo | Replace `assets/portrait.jpg` |

Rules that keep the layout intact: scope any rule that styles a bare descendant
`li` to direct children (`.awards > li`) before nesting a list inside it, and
check the render at 1200 px and 500 px in **both** themes after a CSS change.
Day-theme chip inks are tuned to 4.6:1 on the darkest day surface; keep them there.
There is no scroll-reveal effect and none should be added: the old
IntersectionObserver used a 0.12 threshold, which a section taller than about
eight viewports can never reach, so the Projects section stayed invisible on
phones.
