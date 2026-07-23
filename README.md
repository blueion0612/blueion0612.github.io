# blueion0612.github.io

Personal portfolio of **Yuhyeon Lee** — Wearable Robotics & Exoskeleton Engineer.
Live at **[blueion0612.github.io](https://blueion0612.github.io)**.

Hand-written HTML + CSS. No frameworks, no build step — edit and push.

## Structure

```
index.html         # all content (one page)
assets/style.css   # all styling (light/dark via prefers-color-scheme)
assets/            # images go here (e.g. portrait.jpg)
```

## How to update

| What | Where |
|:--|:--|
| Photo | Save as `assets/portrait.jpg`, then in `index.html` replace the `<span>YL</span>` inside `.portrait` with the `<img>` tag shown in the comment there |
| Publications | Uncomment the `PUBLICATIONS` section in `index.html`, fill in the entry, add a nav link |
| Awards / Experience | Uncomment the `AWARDS & EXPERIENCE` section |
| LinkedIn · Scholar · ORCID | Uncomment the `FUTURE LINKS` buttons in the hero |
| New project | Copy a `.project-card` (featured) or `.project-list li` (compact) block |

Section numbers (`01`–`05`) are manual — renumber after adding a section.
