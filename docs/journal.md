# ido.help — the door page

A single page, which does not scroll, gathering the three transcribed books:

| button | repository | book |
|---|---|---|
| **Tabeli** | `helpolinguo/tabeli` | *Expliko-Libreto di la Delmas-Tabeli helpanta*, 1926 |
| **Dicionario** | `helpolinguo/dicionario` | *Dicionario de la 10.000 radiki*, 1934/1964 |
| **Gramatiko** | `helpolinguo/gramatiko` | *Kompleta Gramatiko Detaloza*, 1925 |

```
index.html              the whole page — structure, style and script
sw.js                   the service worker: offline for all four pages (§ 9)
manifest.webmanifest    the application's name and icons (§ 9)
shared.css              the back button of the three books (§ 8)
shared.js               the little behaviour that button needs (§ 8)
emblem.svg              the emblem alone (favicon) and the button's drawing
apple-touch-icon.png    the same, 180 × 180; icon-192/512.png for the manifest
og-image.png            1200 × 630, the sharing image
fonts/                  Jost* Bold and Medium, subset to this page
tools/emblem.py         reconstructs the logotype
tools/icons.py          rebuilds the images above
tools/machine_files.py  robots.txt, sitemap.xml, llms.txt (§ 10)
CNAME                   the domain, for GitHub Pages
```

---

## 1. Why this repository is named after the account

The name is not a preference: it is what holds the addresses together.

GitHub Pages serves two kinds of site, and only one of the two gives
`ido.help/tabeli`:

* the **user site**, served from the repository named exactly
  `<account>.github.io`, at the root;
* the **project sites**, one per repository, served under the repository's
  name.

When a custom domain is set **on the user site**, GitHub attaches the whole
tree to it — the root *and* every project site of the same account:

```
ido.help/              <- this repository
ido.help/tabeli/       <- the tabeli repository,      automatically
ido.help/dicionario/   <- the dicionario repository,  automatically
ido.help/gramatiko/    <- the gramatiko repository,   automatically
```

Set on a project repository, the domain would indeed serve this page at the
root, but `ido.help/tabeli` would answer 404. Hence the name, and hence the
fact that the repository's name no longer recalls the domain: the domain lives
in the `CNAME` file.

### How it came to this

The name was taken by the *Rare diseases* site of June 2021. Three constraints
dictated the order of operations, and are worth noting if the arrangement ever
has to be made again:

* **archiving does not free a name** — an account cannot have two repositories
  of the same name;
* **an archived repository is read-only**, hence impossible to rename without
  unarchiving, and impossible to push to;
* the redirect GitHub sets on every rename falls the moment another repository
  takes the old name.

The 2021 site was therefore first renamed `rare-diseases`, then archived — it
is still served, an archived repository keeping its pages, but under
`ido.help/rare-diseases/`. Its old addresses did not survive the move: there
was no way to keep them while putting something else at the root. The
`ido.help` repository, where this page was written, then took the freed name,
with its history and its pull requests.

### The settings that must stay in place

**Settings → Pages** on this repository:

* *Source*: `main`, folder `/`;
* *Custom domain*: `ido.help` — the `CNAME` file at the root carries it;
* *Enforce HTTPS*.

At the registrar for `ido.help`:

| type | name | value |
|---|---|---|
| A | `@` | `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153` |
| AAAA | `@` | `2606:50c0:8000::153`, `…8001::153`, `…8002::153`, `…8003::153` |
| CNAME | `www` | the user-site host, with a trailing dot |

### What must not be broken

* **None of the three book repositories may have its own custom domain.** They
  have none — no `CNAME` file — and that is precisely what allows them to be
  served under `ido.help/…`.
* **The `CNAME` file must not disappear.** Deleting it would detach the
  domain, and the three addresses with it.
* The three buttons' links are **absolute from the root** (`/tabeli/`). They
  therefore hold as well under the GitHub Pages host as under `ido.help/`:
  there is nothing to change should the domain lapse or come back.
* The `*.ido.li` subdomains are plain HTTP redirects at IONOS
  (`217.160.0.251`) to the user site's `/<repository>`. They keep working:
  GitHub redirects in turn to `ido.help/<repository>`. They can also be
  repointed directly, or kept as short addresses.

---

## 2. The logotype

The azure IDO is the one from the **title page** of the *Dicionario* (page 3
of `dicionario.pdf`, the one where the lettering is blue on white). It is not
reproduced as an image: it is **rebuilt in outlines**, identically, by
`tools/emblem.py`, from the measurements already recorded in
`dicionario/pocket/cover.tex`:

* the letters **ID** are the outlines of Jost\* Bold, advance widths included;
* the disc follows the D at 0.0045 × page width, that is 12.19 thousandths of
  an em, and its diameter is 1.0651 times the cap height;
* the **star** is regular and constructed, not traced: three long points on
  the circle, three short ones at half-radius, the base of a long point being
  a third of the side of the central triangle.

The total computed width — 1810.8 thousandths of an em — falls within a tenth
of the one measured in the PDF (208.389 pt at 115.083 pt).

The SVG's box is that of the **ink** and not of the advance widths: it begins
at the left side bearing of the I and ends at the edge of the disc, and
overshoots the cap height by 22.79 thousandths above and below, since the disc
is taller than the letters. That is what lets the motto be *exactly* as wide
as what one sees.

**The star turns.** A click on the mark pivots it by a third of a turn — and
it comes back onto itself, the figure being invariant under a rotation of 120
degrees. It is the page's one flourish, and it says something true about the
drawing.

---

## 3. The motto

"helpolinguo internaciona" is the width of the logotype **to the pixel, at any
size**. The text sits in an SVG of the same box, with `textLength` and
`lengthAdjust="spacing"`: it is the spacing between the letters that stretches,
never their drawing. The agreement therefore does not depend on which font
actually loaded — it holds even if Jost\* never arrives.

The type size, 132 thousandths, with the extreme side bearings taken off,
gives a letter-spacing of 0.102 em: enough for the line to breathe under a
mark of that size, not enough to break it apart.

---

## 4. The sky

"International auxiliary language" in **sixty national languages**, laid
behind the mark. The script places them on the real rectangles: two words
never overlap, and none comes near the central block. Each drifts at its own
pace; the whole layer shifts a few pixels under the pointer. Under a real
pointer, hovering a word shows the name of its language.

The draw is pseudo-random **from a fixed seed**: the layout is the same on
every visit for a given window. On a small window, where the central block
takes two thirds of the room, the gaps tighten and the attempts multiply —
without which only six or seven words would be left.

`prefers-reduced-motion` stops the drift and the parallax.

> **To be re-read.** The translations were written by hand. The ones I am
> least sure of, and which would gain from being checked by a speaker: Basque,
> Welsh, Irish, Filipino, Swahili, Mongolian, Kazakh, Tamil and Thai. They are
> all in the `WORDS` table at the top of the script, one line per language.

---

## 5. The entrance

On load, only the disc is visible at first: it comes in from the left,
**rolling**, and the two letters are drawn as it passes them. Then the motto,
the three doors and the foot rise by one notch. The whole lasts a second and a
half.

**The distance is not chosen by eye.** A rolling wheel turns through an angle
proportional to the distance covered: a third of a turn is exactly one radius
times 2π/3, that is 780.76 thousandths of an em. The journey is two of them —
1561.52 — and that number has two happy consequences:

1. the star being invariant under a third of a turn, it **arrives in its
   canonical position with no correction whatsoever**;
2. at the start, the right edge of the disc falls at 249.3, and the ink of the
   I ends at 246: the disc **covers the I exactly**, no more and no less.

The roll is therefore true, not mimed. It is the same figure that a click then
turns, by a third of a turn in its turn (§ 2).

**The letters are not animated: a curtain uncovers them.** They were at first
each clipped by their own animation, with their own delay — and the vertical
cut came away from the disc, which had already rolled further. One saw the
edge of the animation instead of seeing the wheel lay the letters down.

The curtain is a rectangle the colour of the paper, laid over the letters and
under the disc, whose left edge follows the centre of the disc exactly: same
duration, same delay, same easing curve, and a translation that is the *same
function of time*. The two can therefore no longer fall out of step — this is
not a setting, it is an identity.

**And the cut is invisible**, for the very reason you will notice on looking
at the mark: the disc is taller than the letters, 745.6 against 700 of cap
height. At the top of the capitals, where it is narrowest, it still extends
128.3 thousandths either side of its centre. The curtain's edge, which passes
through that centre, is therefore covered over the whole height at which it is
painted.

The curtain is confined to the box of the letters' ink, widened by three
thousandths on all four sides: without that margin its edge fell exactly on
the letters' edge and the two antialiasings did not quite overlap — a
one-pixel azure line was left on the baseline. The margin compromises nothing:
at y = −3 as at y = 703, the disc still extends 119.8 thousandths either side
of its centre. Outside that box the curtain erases itself — at the end of the
roll as at rest.

Three precautions:

* the `intro` class is set **in the HTML** and not by the script — otherwise
  the page would be painted once in its final state before the script ran, and
  the entrance would begin with a jolt;
* it is removed when the wheel stops, but also **on the first gesture**:
  whoever touches the page has better things to do than watch an animation.
  Removing it freezes everything in the final state, so the entrance can be
  cut short at any moment. A safety net removes it in any case after 3.2 s;
* `prefers-reduced-motion` suppresses it entirely: the page paints itself in
  its final state.

Without JavaScript the entrance runs all the same — it is CSS — and ends of
itself on the final state.

---

## 6. The page does not scroll

Not on a screen, not on a phone. The stage is fixed to the viewport
(`100dvh`, which follows the address bar as it retracts), and everything it
contains is measured in `svh` — the **smallest** height the browser can offer,
the one where the address bar is deployed. The block therefore fits in the
narrowest case, and nothing overflows in the others.

A single measure governs the page, `--width`:

```css
--width: min(74vw, 54svh, 560px)
```

That is the width of the logotype; the motto and the three buttons align to
it. Bounded at once by the viewport's width, by its height and by an absolute
maximum, it holds as well on a phone lying sideways (844 × 390) as on a large
screen. On a narrow phone held upright, the three buttons stack — three words
side by side become unreadable well before they run out of room.

Checked in Chromium at 1440 × 900, 820 × 1180, 390 × 844, 844 × 390 and
320 × 568, in light and dark themes: `scrollHeight` equals `clientHeight`
everywhere.

---

## 7. What the page asks of the network

Nothing outside itself — `sw.js` and `manifest.webmanifest` (§ 9) are served
by the site like the rest. The style and the script are in `index.html`; the
two fonts are served by the site (5.7 kB each, subset to the glyphs used); the
logotype is SVG. No request to any third party, hence no tracker. Without
JavaScript the page stays whole — mark, motto and three buttons; only the sky
is missing.

The colours are the five tokens of the three reading pages — paper `#fbfaf7`,
ink `#1a1a1a`, muted `#6b6560`, rule `#e2ddd5` — plus the book's azure,
`#007FFF`. The dark theme takes the same values as the three other pages; the
azure lightens there to `#4da3ff`, failing which it would not hold the
contrast on `#16161a`.

### The two corner discs

The page carries a global action in each of two opposite corners, and both
wear the same disc — 42 px, 38 below 560 px of width, 24 px from both edges.
It is the measure of the back button on the three books (§ 8), so that the
corner carries the same thing everywhere on the site.

**Bottom left, the download** (§ 9). **Top right, the source code**: a link to
the GitHub organisation that holds the four repositories. Neither carries a
word — the site addresses every language, and a label in Ido would say nothing
to a reader who does not read Ido. The accessible names, and the labels that
appear on hover, do stay in Ido: they are the interface, and the interface is
in Ido throughout.

The source disc's flourish is a rhyme rather than an ornament. On hover, a
thin azure ring draws itself all the way round, clockwise, in exactly the
stroke and circumference of the progress ring on the download disc opposite —
2π × 20 = 125.66, the same number in both files. One corner measures a fetch,
the other merely answers a glance, but the eye recognises the same gesture and
the two corners read as one pair. The GitHub octicon sits at the centre of the
same 44-unit box the ring lives in, 25 units wide: (44 − 25) / 2 = 9.5 of
inset and 25/16 of scale, so that ring and mark share one coordinate system
and no number has to be repeated.

Both discs are declared to the sky (§ 4) as keep-out rectangles, widened to
the left or the right by the 120 px their labels take, so that no word can
drift under either one.

---

## 8. The stylesheet shared by the three books

The three books carry, in the bottom left corner, the azure emblem in small: a
link to this page. **Its whole appearance lives in one file**, `shared.css`,
served from this root.

That is possible because the four sites are served from the **same origin** —
the whole point of § 1. A file placed here is readable by `ido.help/tabeli/`,
`…/dicionario/` and `…/gramatiko/`. Each of the three repositories therefore
carries three lines only, and they will not change again:

```html
<link rel="stylesheet" href="/shared.css">
<script src="/shared.js" defer></script>
<a class="ido-home" href="/">Ido</a>
```

The word "Ido" is in the link and not in the stylesheet: if the sheet fails to
load — a page opened outside the site, a file moved — a legible link is left
at the end of the document instead of an empty square.

**It is hidden by a null type size, and not by overflow.** It was at first
pushed out of the disc by `text-indent`, and it was `overflow: hidden` that
held it back — but the overflow has to be made visible on hover, or the label
could not leave the disc. The word therefore came out with it, and "Ido"
appeared twice: once as a label, once spelled out, in the font and colour of
links. A null type size depends on no overflow.

**And the label does not count in the link's name.** The browser appends the
pseudo-element's content to the accessible name, which became "Ido Ido" — the
same duplication, but for whoever listens to the page. The syntax
`content: "Ido" / ""` gives it an empty alternative: it is seen, it is no
longer spoken. It sits under `@supports`, because a browser that ignores the
syntax would discard the whole declaration, and the label would not appear at
all. The drawing itself is `emblem.svg`, already served as this page's icon:
one file for all four.

Retouching the button — size, colour, position, label — is therefore done
**here only**, and the three books follow at the next refresh. GitHub Pages
serves its files with a ten-minute cache; that is the delay to reckon with.

Two things worth knowing:

* **The inset from the corner is 24 px, and it is not a matter of taste.** A
  phone screen has rounded corners, and the rounding eats into the viewport
  diagonally: a corner of radius *r* cuts off everything lying, on the
  diagonal, within *r*(√2−1) ≈ 0.414 *r* of the corner. The point of the disc
  nearest the corner lies √2(*m* + *R*) − (*R* + *h*) from it, where *m* is the
  inset, *R* the radius of the disc and *h* the halo. With the 12 px inset this
  button first had, that came to 20.8 px: the screen's corner radius had to be
  under 50 px for nothing to be clipped — and a recent iPhone is around 55 to
  62, so the button was being eaten. At 24 px the clearance rises to 37.8 px
  and holds up to a radius of 91. The number is isolated in the `--margin`
  variable at the top of `shared.css`.

  Notches are still accounted for on top, `max` keeping the larger of the two
  constraints — but `env(safe-area-inset-*)` only applies on a page declaring
  `viewport-fit=cover`, which the three books do not. It is therefore the
  literal inset that protects them.

* **On the two books with a side panel** — the *Gramatiko* and the *Tabeli* —
  the disc floats over the table of contents and covers the beginning of one
  line. The line stays clickable: the disc is 42 px on a 250 px column, and
  the link is reachable everywhere else. Reserving the corner would mean
  retouching each book's layout, which would lose the benefit of the single
  file.

* **The button is placed from the top, and not from the bottom.** On iPhone
  the address bar retracts as one scrolls down, and the bottom of the viewport
  then moves: a button placed by `bottom` followed that bottom and moved —
  whereas a landmark must not move. It is therefore placed from the top, an
  edge that never moves, at the height of the **smallest** viewport the
  browser can offer:

  ```css
  top: calc(100svh - var(--size) - max(var(--margin), env(safe-area-inset-bottom)))
  ```

  `svh` does not vary when the bars retract. The button therefore stays still
  whatever their state, and stays visible in every case since it fits inside
  the smallest viewport. The `bottom` declaration is left before it, as a
  fallback: a browser that ignores `svh` — Safari before 15.4 — discards the
  `top` and recovers the old behaviour; when both are understood it is `top`
  that wins, the height being fixed.

  The disc is moreover promoted to its own layer by a null three-dimensional
  transform. WebKit does not reposition fixed elements continuously during
  scroll inertia: they drift with the text, then snap back. This is the usual
  remedy, and it costs nothing for a 42 px disc.

* **The button passes under the panels** (`z-index: 12`). On a narrow screen
  the table of contents slides over the page behind a veil; the button has
  nothing to say while it is open.

### The cross that clears the search field

**First attempt, and why it could not have worked.** The cross was at first
asked back from the browser, by restoring the appearance of the
`::-webkit-search-cancel-button` pseudo-element — WebKit abandoning a control's
native rendering as soon as one gives it a border and a background, which the
three books do. On iPhone nothing appeared, and **nothing could**: WebKit
renders that pseudo-element only on macOS. On iOS it does not exist; a search
field there is an ordinary text field, and the custom is to clear it from the
keyboard. No CSS will change that.

The cross therefore has to be **drawn ourselves**. It is placed by
`shared.js`, companion to `shared.css` and served from the same root: each
book carries one more line of it. The native cross is discarded at the same
time — macOS drew one, and there would have been two. Measured in Chromium:
rule cancelled, two crosses; rule active, one only.

`color-scheme: light dark` stays. It no longer serves the cross, but it
matches the scrollbars and the language menu to the dark theme of the three
books, which it already did.

**Nothing breaks if the script fails to load.** Without it the three fields
are exactly what they were: you clear from the keyboard, as before.

#### The wrapper, and the one real trap

The cross is placed absolutely; it therefore needs a positioned parent that
hugs the field. The *Tabeli* already have one — the wrapper around their
magnifier — and the script uses it as it stands rather than stacking a second.
It recognises it by two conditions, both necessary: the parent is already
positioned, and the field is its **only child in the flow** (an icon placed
absolutely does not count). The bar of the other two books fails on both — it
is static, and carries the contents button; they therefore get a wrapper.

And there is the trap. A wrapper stands between the bar and the field: it is
the wrapper, now, that the bar lays out. The measurements that decide the
field's place must therefore pass from one to the other. This is not a
precaution on principle:

```css
/* gramatiko, below 900 px */
input[type=search]{flex:1 1 120px;min-width:0}
```

The author says why in so many words — at a 260 px basis the field would drop
below the contents button. A wrapper taking its basis from its content would
measure wider, and the field would wrap again. Which is exactly what happened,
at a 340 px viewport.

**The measurements are therefore re-read, not copied once.** They change with
the screen width, each book having its own; a copy taken at load would be
wrong from the phone's first rotation. At every real change of viewport the
script clears its overrides, re-reads what the book says about the field *at
that width*, and sets them again. Checked by comparing the field's box, before
and after, at eighteen widths from 1280 to 300 px on all three books:
identical everywhere, to two hundredths of a pixel.

On the rest of the header, with an empty field: no difference on the *Tabeli*,
which have no wrapper; fifteen to twenty-five pixels on the other two, of a
maximum amplitude of 2 out of 255, all on the rounded edge of the field. That
is aliasing, not displacement.

#### A few choices that cannot be guessed

* **It appears only if the field holds something**, and the 34 px indent that
  makes room for it arrives with it. An empty field has nothing to clear, and
  the cross would eat into the placeholder — already truncated on a phone. The
  indent arrives with the first letter typed: by then the placeholder has gone
  and the field holds a single character, so that nothing moves under the eye.

* **The finger's press must not scare the keyboard away.** Pressing a button
  takes the caret out of the field, and on iPhone the keyboard folds away at
  once only to reopen just after: the page jumps twice. Refusing the press's
  default action leaves the caret where it is, and the click follows all the
  same.

* **The caret is only given back to the field if it was there.** Clearing from
  a page already scrolled — keyboard folded away, a result under the eye —
  must not bring the keyboard back up over what was being read.

* **The `input` event is emitted by hand.** The three books filter on it, and
  assigning `value` directly emits none: without this the field would be empty
  and the list still filtered.

* **The cross is not a tab stop**, like the native macOS cross. It inserts
  itself between the field and the next control; making it a stop would add
  one where there was none, for a service the keyboard already renders. Screen
  readers reach it nonetheless, the button remaining in the document and named
  — "Efacar la sercho", in Ido like the rest of the three interfaces.

* **The touch target is 34 px over the full height of the field**, for a 15 px
  stroke: a finger does not aim at a stroke.

This section is why `shared.css` is no longer only the back button but **the
shared stylesheet**: whatever has to be uniform across the three books and
cannot be made so otherwise now has its place there — the appearance in the
stylesheet, the little behaviour needed in `shared.js`, beside it.

---

## 9. Offline, and the application's name

### The name

The tab's title stays **"Ido — helpolinguo internaciona"**. Under an icon, a
name has room for two words at most: the manifest and Apple's meta tag
therefore give **"Ido"** alone.

```html
<link rel="manifest" href="manifest.webmanifest">
<meta name="apple-mobile-web-app-title" content="Ido">
```

`manifest.webmanifest` also carries `short_name`, the icons (`icon-192.png`,
`icon-512.png`, rebuilt by `tools/icons.py`) and three shortcuts to the books.

**The window bar's colour.** The browser keeps **the first** `theme-color`
whose `media` matches. The unconditional one used to come first: it always
matched, and the dark-theme one was never reached — hence a white bar in dark
mode in the Dock application, while the three books followed the theme,
declaring none and letting Safari deduce the colour from the ground actually
painted.

Both therefore carry their condition, and **the light one comes first**: a
browser that ignored the `media` attribute would take the first, and light is
the page's default.

```html
<meta name="theme-color" media="(prefers-color-scheme:light)" content="#fbfaf7">
<meta name="theme-color" media="(prefers-color-scheme:dark)"  content="#16161a">
```

The manifest **no longer declares a `theme_color`**: it was a second source,
static and light, which could not have followed the theme. Without it only the
two meta tags are left — and if a browser ignored them, it would do as it does
for the three books, which have none and are fine. `:root` further declares
`color-scheme: light dark`, so that the browser matches its own surfaces.

> **A choice worth knowing about.** The manifest declares
> `"display": "standalone"`, and the `apple-mobile-web-app-capable` tag
> accompanies it for iOS before 16.4: the saved application therefore opens
> **without Safari's chrome**. That is what "web app" implies, but it is a
> visible change. One word to change to go back.

### Offline

`sw.js`, placed at the root, has the **whole site for its scope**: the door
and the three books, which are served from the same origin. The three
repositories therefore carry nothing — they are taken care of as soon as the
home page has been opened once. It is the same benefit as for `shared.css`
(§ 8).

**Freshness comes before speed**, since the texts are corrected often:

| what is requested | how | why |
|---|---|---|
| a **page** | network first, copy as backup | online, one always reads the latest version |
| **everything else** — stylesheet, fonts, images, PDFs | copy first, revalidation behind | these files change rarely, the wait would not be justified |

Network requests carry `cache: 'reload'`: without it the browser's HTTP cache
would hand back a copy ten minutes old — the lifetime GitHub Pages announces.

**When the connection returns**, the page tells the worker, which fetches
*everything it holds* afresh. That is what answers "as soon as possible".

### The full download

The whole site — the three texts, the PDFs, the 52 languages and the 38
engraved plates in **both** of their resolutions — weighs **69 MB**, or 106
files.

* **Installed**, the application fetches it of its own accord, four seconds
  after opening. That is what one expects of an application, and it is the
  closest moment to "added to the home screen" that a site can observe: iOS
  does not announce that addition, unlike Android.
* **In a tab**, nothing is fetched unasked: a passing visitor should not pay
  69 MB. A disc in the bottom left corner offers it.

**The disc carries no word**, and that is deliberate: the site addresses every
language, and "Deskargar" said nothing to a reader who does not read Ido. It
occupies, on the door, the place the back button occupies on the three books —
same corner, same size, same inset — so that the corner always carries "the
global action": going back when reading, downloading when standing at the
door.

| state | glyph | ring |
|---|---|---|
| at rest | an arrow pointing down | empty |
| during | the arrow | it goes round as it goes |
| finished | a tick | full, azure |
| armed for erasure | a bin | full, sienna |

The count of megabytes appears to the right of the disc during the fetch, and
only then: "18 MB" reads everywhere, which a sentence does not. It states what
has **come down**, with no denominator — it is the ring that says what share
is done, and a total announced in advance would rest on an estimate,
unversioned files not announcing their size.

**A click on the "finished" state does not erase**: it arms. The glyph becomes
a bin for four seconds, and one has to click a second time. Erasing 69 MB by
mistake would be painful, and a confirmation spelled out in words would amount
to putting the text back. Erasure keeps the shell: without it, one could no
longer ask for the download again offline.

The accessible name, for its part, stays in Ido and follows the state — screen
readers need words, eyes do not.

The state shown is not a marker set after the fact: the worker really counts
what it holds of the plan. If the browser emptied the cache, the button would
offer itself again of its own accord.

**The weight is known without a single request**, because the `?v=` of each
address **is** the file's size in bytes — checked on all 90 versioned
addresses. The plan itself is read from the *Tabeli*'s page, never written in
the source.

**A fallback for the magnifier.** The plates exist as "vido" (200 kB) and as
"detalo" (1.8 MB). If the large one is missing offline — download interrupted,
partial cache — the worker serves the small one: a blurred magnifier, but an
image, instead of an empty frame.

### And on Android?

Yes, and better than elsewhere. Service worker, cache and manifest are the
standard ones; Chrome on Android moreover knows how to offer installation
(`beforeinstallprompt`), announces the installation done (`appinstalled`), and
honours `navigator.storage.persist()`, which keeps the cache from being
evicted when space runs short. The `(display-mode: standalone)` test that
triggers the automatic download holds on both systems.

On iOS, persistence is granted outright to home-screen applications; it is in
a plain Safari tab that the cache may be cleared after seven days without a
visit.

### What is fetched, and when

| | weight | when |
|---|---|---|
| the shell — door, stylesheet, script, fonts, icons | 0.09 MB | at install, for every visitor |
| the three texts and the four PDFs | ≈ 12 MB | **only as an installed application**, four seconds after opening |
| the *Tabeli*'s 52 languages | 24.5 MB | next, in the order the page cites them |
| the 38 engraved plates, two resolutions | 32 MB | with the rest |

That is **69 MB**, the figure the disc shows at the end and which
`navigator.storage.estimate()` confirms.

**Why the languages.** The *Tabeli*'s page is bilingual: Ido on the left,
another language on the right. That other language is not in the page — it is
fetched at the moment it is chosen, one file per language. Offline, a language
never opened was therefore missing, and the selector had no effect.

**The list is not written in `sw.js`.** It is read from the page itself,
already cached: a copied list would go stale at the first change of address.
The languages are fetched in the order the page cites them, so that an
interrupted fetch covers the commonest first.

**The versioned addresses are immutable.** Languages and plates all carry a
`?v=`: a correction changes the address, and the page — always fetched from
the network — cites the new one. Two consequences: they are never revalidated
when the connection returns, which would mean fetching 24 MB for nothing; and
the ones the page no longer cites are purged, failing which the old ones would
stay indefinitely.

Since the 2026 renaming, the pattern that finds them in the page **names no
directory**: any relative address bearing a `?v=` is a versioned asset, which
is all `sw.js` needs to know. It used to name `lingui` and `gravuri` one by
one, and a directory renamed on the *Tabeli*'s side would have silently
emptied the plan. Checked against the page as published: the two patterns find
exactly the same 93 addresses.

### Two points of safety

* **`addAll` is not used.** It is atomic: a single missing file, or a single
  request that fails, and nothing is cached — the whole shell lost over a
  detail. Each file is fetched separately.
* **A faulty deployment cannot get stuck**, since pages are fetched from the
  network first. And to purge everything: change `CACHE` at the top of
  `sw.js`; the old cache is deleted on activation.

  It was deliberately **not** changed for the 2026 renaming, although several
  shell files changed name. Bumping it would have cost every reader who had
  taken the whole site offline their 69 MB. The few stale entries left behind
  are harmless, and the erase button sweeps them, since it keeps only what is
  in `SHELL`.

### Checked in Chromium

Served locally in the real tree, with the network cut:

* the shell is fetched at install — 10 entries; the body on demand — 7
  entries, 16 in all;
* **offline**, the door, the three books and the PDFs all answer, without any
  book having been opened beforehand;
* a published correction is visible **at the next reload** as long as one is
  online, and is then found offline;
* a correction published *during* an outage is picked up **half a second
  after** the network returns;
* the 52 languages are fetched, and **offline the selector works** — French,
  German and Japanese fill their 672 blocks without the *Tabeli* having been
  opened beforehand;
* a versioned entry gone stale is **purged** on the next pass;
* the full download carries the **106 files** to their end, and **offline all
  106 answer, 0 failing**, for 69 MB restored;
* the plates appear offline without the *Tabeli* having been opened;
* with the large resolution deleted, the offline request receives the small one
  — 218 kB instead of 1.8 MB;
* the state is recognised on reload: the button says "Senrete disponebla";
* the disc passes through its four states, arms itself, disarms itself alone
  after four seconds, and erasure leaves only the shell's files;
* no word of the sky falls under either corner disc, at the six formats tried
  and over six spaced measurements — the reserve allows for the drift of the
  words, which is thirteen pixels at most;
* the entrance, the click on the star and the absence of scrolling are intact.

---

## 10. The site, for machines

The site addresses the eye first. This section describes what was added for
what has no eyes: search engines, crawlers, and the language models that go
looking for an address.

### The real problem was not the weight

One assumes at first that the difficulty is the number of tokens. Measured, it
was elsewhere:

| page | weight | visible text without JavaScript |
| --- | ---: | ---: |
| `/dicionario/` | 2.1 MB | **213 characters** |
| `/tabeli/` | 3.3 MB | 257 kB |
| `/gramatiko/` | 1.2 MB | 467 kB |

The Dicionario is built by JavaScript: its 9473 entries live in an array the
browser unrolls at load. Excellent for instant search, disastrous for anything
that does not run a script. The page moreover renders only 400 entries at a
time, even with JavaScript. An indexing robot without a JS engine saw nothing
there, and nothing told it so.

### The generated files

Each book now carries a `tools/machine_readable.py` which draws
machine-readable versions from its page. **They are generated, never edited by
hand**; the source stays `index.html`.

| book | files | contents |
| --- | --- | --- |
| Dicionario | `dicionario.json` | the 9473 entries, bare data |
| | `dicionario.md` | the book laid flat |
| | `vortlisto.md` | headword and first sense only |
| Gramatiko | `chapitri/*.md` | **one file per chapter**, ~10 kB |
| | `chapitri/index.md` | the table, with each one's size |
| | `gramatiko.md` | the whole book |
| Tabeli | `tabeli.json` | the 672 keys, Ido and French |
| | `tabeli.md` | the table laid flat |
| | `lingui/index.json` | the 55 other languages offered |

### Splitting beats compressing

That is the point to keep. A grammar is not read end to end: one looks up a
point in it. Whoever wants to know how the plural is formed does not have to
load 1.2 MB — they load a 10 kB chapter. The gain is not a few per cent, it is
two orders of magnitude, and it owes nothing to any compression: it rests on
the text being **split and labelled**, and on the sizes being announced in
advance so that one can choose before downloading.

### The Tabeli's hinge

The rows' keys (`data-cle`) are exactly those of the `lingui/*.json` files.
Publishing the Ido/French pairs under those same keys therefore makes the
whole corpus of 57 languages joinable by program: whoever wants the
Ido–Japanese pair joins `tabeli.json` and `lingui/ja.json` on the key, without
opening the page or running its JavaScript. The 672 keys correspond 100 %.

### At the root, and why only there

`robots.txt` and `sitemap.xml` are only read at the ROOT of a domain: dropped
into `/tabeli/`, nobody would read them. Like the shared stylesheet and the
service worker, they can only live here, and they speak for all four pages.
`tools/machine_files.py` generates them — it reads the neighbouring
repositories, and must therefore be re-run when a book changes.

* **`robots.txt`** says yes to everyone, and names the language models'
  crawlers one by one. This is not redundant with the star: several look for
  their own name before the general rule, and some operators abstain when
  nothing addresses them.
* **`sitemap.xml`** lists the pages AND the generated files. Without that an
  engine would find them only by the page's link, and a crawler not at all.
* **`llms.txt`** is the map: what the site holds, in what form, and at what
  weight. It is the last column that counts.

### What each page carries

A description, a canonical link — the site also answers under its GitHub Pages
host, and without that line an engine may treat the two as two sites — an
`alternate` link to the Markdown version, and a JSON-LD block saying what the
document IS: a book, its author, its date, its language.

The Dicionario carries in addition a `<noscript>` which does not try to render
the dictionary in HTML, but says where it is. Without JavaScript the page
offered 213 characters and no way out; it offers 465 and three paths to the
text.

**No licence statement was written into the structured data.** The structured
data could carry a `license` field, and it was deliberately left empty: the
three works do not share one status — 1925 and 1926 on one side, a second
edition of 1964 on the other — and that decision belongs to the site's author,
not to its tooling. The repositories state their position in prose, in each
`README.md`.

## 11. Rebuilding the images

```sh
python3 tools/emblem.py   # the logotype, to be copied into index.html
python3 tools/icons.py    # emblem.svg, apple-touch-icon.png, og-image.png
```

Both scripts read `Jost-Bold.ttf` and `Jost-Medium.ttf` from
`dicionario/pocket/fonts/`; they require `fonttools` and `pymupdf`.

Jost\* is under the SIL OFL 1.1 — see `fonts/OFL.txt` and `fonts/README.md`.


## 12. Spotlight, and the search from outside the site

macOS 26 lets one type a site's name into Spotlight and press **Tab** to
search inside that site. It invents nothing: it hands over the list Safari
keeps under *Settings → Search → Manage Websites*, and Safari fills that
list from an **OpenSearch description document** — read since Safari 8, and
the way Apple recommends — or, failing one, from a guess made on the
metadata of a search form. Adding the site to the Dock as a web application
has nothing to do with it: that gives an icon and a name in Spotlight's
list of applications, not a search.

So `/opensearch.xml`, written by `tools/machine_files.py` like the three
other files for machines, and declared by a `<link rel="search">` on the
home page and on the dictionary's. It lives at the root for the reason the
other three do: **Safari keeps one entry per domain**, and the four sites
share this one.

That entry has to name an address that works. It names
`https://ido.help/dicionario/?q=` — the dictionary is the book one reaches
by a word — and the dictionary's page did not read `?q=` at all: its search
was a field and nothing else, and no search in it had an address. Reading
the parameter, and writing it back at each keystroke, is the other half of
this work; it was done in the `dicionario` repository, and its page's
comments say how.

**What the service worker was doing with it.** Pages are cached under the
address asked for. Measured, before the change: one search from Spotlight
laid a *second* copy of the dictionary in the cache — 2.1 MB — and every
distinct word would have laid another. A static host cannot vary by query,
so the copy is now filed under the address without its query, and one
search leaves one entry.

**What was expected and did not happen.** That the same rule should have
made a search address, offline, fall back on `/` — the home page — for want
of a hit. With the server stopped, Chromium answered the navigation all the
same, from its own store: the fault was never visible. The fallback was
corrected all the same, being the other half of the filing rule.

**Not done: the suggestions endpoint.** OpenSearch allows a second address
returning completions as JSON while one types. It takes the typed word as a
query parameter, which GitHub Pages cannot answer. Spotlight opens the page;
the page's own search does the rest — and it is worth saying plainly that
Spotlight will not show a definition inside its own window. Only a native
application, through App Intents, can do that.
