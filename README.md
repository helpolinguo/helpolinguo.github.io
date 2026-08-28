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
icon-1536.png           the same drawing, for the lock screen — see below
og-image.png            1200 × 630, the sharing image
robots.txt              }
sitemap.xml             }  generated — see tools/machine_files.py
sitemap-pages.xml       }  the pages; sitemap.xml indexes it
sitemap-vorti.xml       }  the 9461 articles, one address each
llms.txt                }
opensearch.xml          }
fonts/                  Jost* Bold and Medium, subset to this page
audio/la-skopo.mp3      the song behind the easter egg — see below
tools/                  the generators; nothing here is served
tools/tap.html          taps out the reel's line times — see below
docs/journal.md         why the page is built the way it is
CNAME                   the domain, for GitHub Pages
```

## Building

The page itself needs no build: it is one self-contained HTML file, served
statically. Three scripts regenerate what is not written by hand.

```sh
python3 tools/emblem.py         # the logotype, to be copied into index.html
python3 tools/icons.py          # emblem.svg, the icons, og-image.png
python3 tools/machine_files.py  # robots.txt, the three sitemaps, llms.txt,
                                # opensearch.xml
```

The first two need `fonttools` and `pymupdf`, and read the Jost\* TTFs from
the `dicionario` repository. The third reads the three book repositories, and
so expects their clones beside this one; re-run it whenever a book changes.

Files under `tools/` are **generators, not sources**: `robots.txt`,
`sitemap.xml` and its two children, `llms.txt` and `opensearch.xml` are
overwritten wholesale, so anything that must change is changed in
`tools/machine_files.py`.

## Searching the site from outside it

`opensearch.xml` declares that this domain has a search, and gives its
address: `https://ido.help/dicionario/?q=`. The dictionary's page reads that
`?q=` at load, so the address is a search one can copy, bookmark or send.

Safari reads the declaration on the first visit — the `<link rel="search">`
is on the home page and on the dictionary's — and files the site under
*Settings → Search → Manage Websites*. **macOS 26 hands that list to
Spotlight**: typing the site's name there and pressing Tab opens a field
whose result lands on the dictionary, the word already sought. The same
entry serves the address bar, where `ido.help` followed by a space does the
same thing.

Two limits worth knowing. Spotlight OPENS the page; it does not show the
definition inside its own window — only a native application, through App
Intents, can do that. And Safari has to have seen the site at least once:
the list is built from visits, not from a registry. Safari on iOS ignores
OpenSearch entirely.

## What a machine is told, and where it is sent

`llms.txt` is the map, and it grew two paths that were missing — the two a
model asked to **write** Ido needs, as against one asked to read it.

**Deriving a word.** The Dicionario carries the roots, so `kovrilo`,
`skribilo`, `dometo`, `hundino` are none of them headwords and no number of
articles will yield one. `gramatiko/afixi/` gives each of the **65 affixes**
its own file of about 2 kB, and the map now carries the whole inventory
inline, with the first example the book prints under each — so a reader of
`llms.txt` alone already holds the derivational system.

**Going from a meaning to an Ido word.** `tabeli/glosaro/` pairs the
Tabeli's bold terms with their equivalents in 56 languages — **1,897 pairs
in `en-GB`** — and is the only place the site answers *what is the Ido for
X*. The map said, until now, that no such index existed; it says instead
where it is, and that it is small and concrete, so that a model reaching
for an abstract word is sent back to the definitions rather than left to
invent one.

Both are read out of the neighbouring repositories, like everything else in
`machine_files.py`, and both **degrade silently**: run without those
directories, the map is 14 kB and mentions neither, and the sitemap drops
back from 364 addresses to 185.

## The song in the O

Seven clicks on the mark inside seven seconds, and the **O becomes a
player**: the star folds away, a ring takes the rim to measure the song,
and the disc is the play and pause button of *La Skopo* — Zamenhof's
*La Vojo* in de Beaufront's Ido. When the song ends the star comes back and
turns again as before; Escape leaves early.

**It plays in the background, and the lock screen shows it.** The song is a
plain `<audio>` element, so iOS puts it in its Now Playing panel by itself
and the controls there work without anything being asked of them. What that
panel *shows*, left to itself, is the page's title and the largest icon the
manifest offers — and 512 px, blown up to the 1111 the panel draws on an
iPhone 16 Pro, came out with the star's edges stepped. So the page names
the song itself, through the Media Session API, with `icon-1536.png` for
artwork. Setting that metadata is all or nothing — an unset field is empty,
not inherited — which is why the panel now reads *La Skopo* and its authors
rather than the site's name.

**The words follow, under the three doors.** The whole poem stands in the
page, in order; the panel is a window on it, moved so the line being sung is
at the middle while the rest blur and fade in proportion to their distance.
The five credits ride at the end of the reel, the way a karaoke roll ends on
them — so the foot keeps its own line while the poem is up, and takes the
credits back only where the window has no room and stands down.

The panel hangs below the block and is out of its flow, so the mark, the
motto and the doors do not move by a pixel when the song starts, and the
resting page is unchanged. Its height is measured, not declared: the room
between the doors and the foot runs from 94 px at 320 × 568 to 359 px at
820 × 1180, and the script subtracts rather than guessing at it with media
queries — five lines where there is room, three where there is less, none
below that.

**The times are the weakest number on the page.** Each line carries a
`data-t`, the second it begins at, and following the voice automatically does
not work here — because the accompaniment is a *choir*, so the lead singer is
neither the only harmonic thing in the mix nor the only thing in the centre
of it. Centre extraction, harmonic salience, chroma self-similarity, a search
for the four repeats, and forced alignment against the one offline acoustic
model available were all tried; `docs/journal.md` § 15 keeps the ledger.

What the recording does give up is where the singing stops, once the right
thing is measured. An instrumental passage here is not *quieter* — the choir
sees to that — but it lacks the 3–8 Hz **wobble of syllables**. Measuring the
modulation of the presence band (700–3200 Hz) about its own 0.9 s mean finds
three quiet stretches, stable as the threshold moves from the 25th percentile
to the 43rd:

| | |
|---|---|
| 0.0 – 27.1 s | the instrumental introduction |
| 108.2 – 119.2 s | **one break, in the middle, 11.0 s** |
| 200.5 – 216.4 s | the closing tag |

So there is no interlude between the first stanza and the second, nor between
the third and the fourth: the song runs two stanzas, breaks once, and runs two
more. The reason to believe it is that the two halves this implies are
**81.1 s and 81.3 s** long — 0.20 s apart in 81, sixteen lines each.

**The 32 sung lines are now tapped, not estimated.** `tools/tap.html` struck
each one by hand against the recording, and the estimate turns out to have
had the shape right and every boundary about five seconds late — the lag of a
detector that smooths over two seconds before it will call a stretch quiet.
The tapped gaps run from 4.02 s to 5.54 s: a poem in a strict metre is still
not sung in one, and no estimate could have known that.

The tool remains the way to redo them: serve the repository root, open it,
and tap the space bar on each line as it begins. The right arrow skips a
line and lets it be worked out from the taps either side. It prints the block
of `<p class="line">` back ready to replace the one in `index.html`, and
reads the poem from `index.html` rather than keeping a copy, so it cannot go
stale against it.

The recording is `audio/la-skopo.mp3`, 4.9 MB for 3 min 36 s. It carries
`preload="none"`, so **nobody who never finds the egg ever fetches it**,
and it is not in the offline plan the download button follows: played once
online, the service worker keeps it like any other asset. The credits stand
in the foot while it sounds, in Ido like the rest of the interface:

| | |
|---|---|
| Poemo «&#8239;La Vojo&#8239;» | L. L. Zamenhof |
| Tradukuro «&#8239;La Skopo&#8239;» | L. de Beaufront |
| Melodio | René Deshays |
| Akompano por koro | Félicien Menu de Ménil |
| Enrejistruro | Lucas Costa, per SUNO |

The recording was made by Lucas Costa with SUNO and contributed to this
project; the poem, its Ido translation, the melody and the choral setting
are the work of the four authors named above. The MIT licence at the foot
of this file covers **the code**, not the recording.

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
