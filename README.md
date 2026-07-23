# blueion0612.github.io

Personal portfolio of **Yuhyeon Lee** — Wearable Robotics & Exoskeleton Engineer.
Live at **[blueion0612.github.io](https://blueion0612.github.io)**.

Hand-written HTML + CSS, no frameworks, no build step — edit and push.

**Design**: "the engineer's dossier" — dark-only matte black, film grain,
angular tech display in caps (Chakra Petch), monospace readouts (IBM Plex Mono),
Archivo body, one phosphor-green accent, brass for stamps and the monogram.
When editing `assets/style.css`, bump the `?v=` query on its `<link>` in
`index.html` to bust the Pages CDN cache.

## Structure

```
index.html         # all content (one page) + small scroll-reveal script
assets/style.css   # all styling (dark only; print forces light)
assets/            # images go here (e.g. portrait.jpg)
```

## How to update

| What | Where |
|:--|:--|
| Photo | Save as `assets/portrait.jpg`, then in `index.html` replace `div.portrait-blank` with the `<img>` tag shown in the comment there |
| Publications | Add an `<li>` to the `.publications` list; paper links go in `.pub-links` (see inline comment); swap the `.stamp` text when status changes |
| Awards / Experience | Uncomment the `AWARDS & EXPERIENCE` section |
| LinkedIn · Scholar · ORCID | Uncomment the `FUTURE LINKS` buttons in the hero |
| New project | Copy a `.project-card` (featured) or `.project-list li` (compact) block |

