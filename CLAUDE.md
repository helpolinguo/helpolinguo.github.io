# Working notes

This file says how we work on this repository. The *what* is in
`README.md`, which is the project's documentation; we do not repeat it
here, we point at it.

## Branches and pull requests

**The project lives on `main`**, which is the default branch, and
GitHub Pages serves it at `ido.help`. A push to `main` is a deployment.

We never write to `main` directly. We work on a branch, and bring it in
through a **pull request whose base is `main`**, opened as a draft. A
branch always starts again from the current `main`:

    git fetch origin main
    git checkout -B <branch> origin/main

**A branch is named after its subject**, in English, in lower case, the
words joined by hyphens: `claude/working-notes`,
`claude/source-link-corner`, `claude/llms-in-english`. No session
identifier, no random suffix — a name like that says nothing six months
later, and it lies the moment the branch serves something other than
what it was opened for. The `claude/` prefix stays: it says who held the
pen.

A merged pull request is finished: it cannot carry a sequel. The next
piece of work starts again from `main`, and it is a new pull request.

## THIS REPOSITORY IS THE SITE'S ROOT, AND THREE OTHERS DEPEND ON IT

`shared.css`, `shared.js`, `emblem.svg`, `llms.txt` and `opensearch.xml`
are served from here and read by `tabeli`, `gramatiko` and `dicionario`,
which reference them as `/shared.css`, `/shared.js`, `/llms.txt` and
`/opensearch.xml`. **A rename here breaks all three**, and nothing inside
this repository can tell: there is no root to 404 against when you serve
this folder alone.

The same goes for the class names those pages carry — `.ido-home`,
`.ido-clear`, `.ido-search-shell`, `.ido-filled`. They are defined here
and written into each book's generated page.

So: **when an asset or a class changes name here, the four deployments
land together**, or a book is unstyled for as long as GitHub Pages
caches. This has been paid for: `dicionario` was left behind on a
rename, and its page would have gone out asking for a stylesheet that no
longer existed, and lost the round azure home button with it.

The way to catch it is to serve one book's page **with this root beside
it** and watch what the browser asks for:

    mkdir /tmp/site && cp ../tabeli/index.html /tmp/site/
    cp shared.css shared.js emblem.svg llms.txt /tmp/site/
    cd /tmp/site && python3 -m http.server

Then check that no request to a **root** address fails, and that
`.ido-home` computes to `width: 42px`, `border-radius: 50%`,
`position: fixed` — the round button. The book's own assets (its plates,
its language files) are not in that folder and will 404: those are the
copy's doing, not the site's.

## What we check before pushing

The page needs no build; three generators produce what is not written by
hand:

    python3 tools/emblem.py         # the logotype, to be copied into index.html
    python3 tools/icons.py          # emblem.svg, the icons, og-image.png
    python3 tools/machine_files.py  # robots.txt, sitemap.xml, llms.txt,
                                    # opensearch.xml

`machine_files.py` reads the three book repositories and expects their
clones **beside this one**; re-run it whenever a book changes. It stamps
today's date into `sitemap.xml`, so that file will always show in a
diff — pass `DATE=` to reproduce an earlier run byte for byte.

And the page itself: no console error, and no horizontal scroll at
1440×900, at 390×844, or in the dark theme
(`scrollHeight == clientHeight`).

## Three rules that are not negotiable

**A PRODUCED FILE IS NOT A PLACE WHERE ONE WRITES.** `robots.txt`,
`sitemap.xml`, `llms.txt`, `opensearch.xml`, `emblem.svg`, the icons and
`og-image.png` are overwritten wholesale. What must change is changed in
`tools/`.

`machine_files.py` is the one to watch: **run without the three books
beside it, it empties `sitemap.xml` of them and shortens `llms.txt`** —
265 lines went out of the map that way here, and were put back by hand.
`opensearch.xml` alone does not depend on them.

**THE SERVICE WORKER'S CACHE NAME STAYS `ido-2`.** Changing `CACHE`
purges everything at activation, and a reader who had taken the whole
site offline would lose sixty-nine megabytes to a rename. Stale shell
entries are harmless: the erase button keeps only what is in `SHELL`.
And `VERSIONED` must stay **directory-agnostic** — it matches any
relative address bearing a `?v=`, so that a book moving its plates does
not cost its readers their offline copy.

**THE INTERFACE IS IN IDO.** Page text, accessible names, tooltips, the
labels on hover, and the URLs of the three books. `/llms.txt` is the one
published page in English, and `README.md` says why. Nothing else a
visitor can see changes because the source changed.

## Writing

Commit messages and code comments **in English**, in the house style: the
finding at the head and in capitals, measurements rather than
suppositions, the approaches tried and then abandoned recorded, and an
earlier assertion that has become false corrected **where it is
written**.

`docs/journal.md` is in French. It is the record of how the page was
built, written as it was built; it is not translated, and a new entry is
written in English at the end.
