# ido.help

The front door of [**ido.help**](https://ido.help/) — a single page, which
does not scroll, gathering three foundational books of **Ido**, the
international auxiliary language published in 1907.

Each book lives in its own repository and is served from this one's domain:

| | repository | book |
|---|---|---|
| [**Tabeli**](https://ido.help/tabeli/) | [helpolinguo/tabeli](https://github.com/helpolinguo/tabeli) | *Expliko-Libreto di la Delmas-Tabeli helpanta* — J. Guignon, 1926 |
| [**Dicionario**](https://ido.help/dicionario/) | [helpolinguo/dicionario](https://github.com/helpolinguo/dicionario) | *Dicionario de la 10.000 radiki di la linguo universala Ido* — M. Pesch, 1934/1964 |
| [**Gramatiko**](https://ido.help/gramatiko/) | [helpolinguo/gramatiko](https://github.com/helpolinguo/gramatiko) | *Kompleta Gramatiko Detaloza di la Linguo Internaciona Ido* — L. de Beaufront, 1925 |

All four are served from one origin, so this repository can carry what the
other three would otherwise each have to repeat: the shared stylesheet, the
service worker, and the files search engines only read at a domain's root.

## Layout

```
index.html              the whole page — structure, style and script
sw.js                   the service worker: offline for all four pages
manifest.webmanifest    the application's name and icons
shared.css              the three books' back button, and the search-field cross
shared.js               the little behaviour that cross needs
emblem.svg              the emblem alone: favicon, and the button's drawing
apple-touch-icon.png    the same, 180 × 180
icon-192.png            }  the manifest's icons
icon-512.png            }
og-image.png            1200 × 630, the sharing image
robots.txt              }
sitemap.xml             }  generated — see tools/machine_files.py
llms.txt                }
fonts/                  Jost* Bold and Medium, subset to this page
tools/                  the generators; nothing here is served
docs/journal.md         why the page is built the way it is
CNAME                   the domain, for GitHub Pages
```

## Building

The page itself needs no build: it is one self-contained HTML file, served
statically. Three scripts regenerate what is not written by hand.

```sh
python3 tools/emblem.py         # the logotype, to be copied into index.html
python3 tools/icons.py          # emblem.svg, the icons, og-image.png
python3 tools/machine_files.py  # robots.txt, sitemap.xml, llms.txt
```

The first two need `fonttools` and `pymupdf`, and read the Jost\* TTFs from
the `dicionario` repository. The third reads the three book repositories, and
so expects their clones beside this one; re-run it whenever a book changes.

Files under `tools/` are **generators, not sources**: `robots.txt`,
`sitemap.xml` and `llms.txt` are overwritten wholesale, so anything that must
change is changed in `tools/machine_files.py`.

## A note on language

The source is in English — comments, identifiers, filenames and commits. **The
interface is in Ido** and stays so: page text, accessible names, tooltips and
the labels on hover are all Ido, as are the URLs of the three books.
Translating the source changed nothing a visitor can see.

**`/llms.txt` is the one published page in English.** The interfaces are in
Ido because they are read by people who came for Ido; `/llms.txt` is read by
crawlers and by whoever is wiring a program up to the site, and English is
what serves them. The three works keep their own titles, which are their
names.

## Licence

The code in this repository is under the **MIT Licence** — see
[`LICENSE`](LICENSE). Copyright © 2026 Gilles-Philippe Morin.

The **three works presented on the site are in the public domain in Canada**,
where this project is maintained, their authors having died more than fifty
years before Canada's 2022 term extension, which did not restore expired
copyrights. Copyright terms differ from country to country: readers elsewhere
should satisfy themselves of the position under their own law. The
transcription, the typesetting and the reading pages are this project's own
work, and are covered by the licence above.

Jost\* is under the **SIL Open Font License 1.1** — see
[`fonts/OFL.txt`](fonts/OFL.txt).
