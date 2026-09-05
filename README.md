# blueion0612.github.io

Personal portfolio of **Yuhyeon Lee**, Wearable Robotics & Exoskeleton Engineer.
Live at **[blueion0612.github.io](https://blueion0612.github.io)**.

Hand-written HTML and CSS. No frameworks, no build step: edit and push.

**Design**: a wanted poster. Besley carries the name, Rye the western bands and
section keys, IBM Plex Mono the readouts and Archivo the body text. One
phosphor-green accent, brass for the stamps and the monogram, brass tacks and a
vignette over the whole page. Night is matte black with film grain, day is
parchment; the toggle sits in the nav and remembers the choice.

When editing `assets/style.css`, bump the `?v=` query on its `<link>` in
`index.html` to bust the Pages CDN cache. It is currently at `v=22`.

## Structure

```
index.html         # all content (one page) + theme toggle and scroll-reveal script
assets/style.css   # all styling, both themes (print forces light)
assets/portrait.jpg
assets/og.png      # social preview card
```

Sections, in order: about, research, education, publications, awards, projects,
contact.

## How to update

| What | Where |
|:--|:--|
| Publications | Add an `<li>` to the `.publications` list; paper links go in `.pub-links` (see the inline comment); swap the `.stamp` text when the status changes |
| Awards and experience | Add an `<li>` to `.awards`; sub-points go in a nested `ul.award-points` inside the `div.award-body` |
| New project | Copy a `.project-card` (featured) or a `.project-list li` (compact) block |
| Google Scholar | Uncomment the `FUTURE LINKS` button in the hero once a paper is published |
| Photo | Replace `assets/portrait.jpg` |

Rules that keep the layout intact: scope any rule that styles a bare descendant
`li` to direct children (`.awards > li`) before nesting a list inside it, and
check the render at 1200 px and 500 px in **both** themes after a CSS change.
