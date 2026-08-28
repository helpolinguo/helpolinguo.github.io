#!/usr/bin/env python3
"""Generates the site's front-door files FOR MACHINES: robots, map, llms,
search.

WHY AT THE ROOT. The four sites share one origin — the home page is the
user site, the three books are project sites. But "/robots.txt" and
"/sitemap.xml" are only read at the ROOT of a domain: a robots.txt dropped
into /tabeli/ would be read by nobody. These four files can therefore only
live here, and they speak for all four sites.

WHAT EACH ONE DOES

  robots.txt      says yes to everyone, by name — including the language
                  models' crawlers, which many sites block and which, for
                  want of a mention, sometimes abstain of their own accord.
  sitemap.xml     lists the pages for search engines.
  llms.txt        the map, for the use of models: what the site holds, in
                  what form, AND AT WHAT PRICE. It is the stated weight
                  that counts: it allows a choice to be made BEFORE
                  downloading, and that, far more than compression, is
                  where the saving is.
  opensearch.xml  says that this domain HAS A SEARCH, and at what address.
                  Safari reads it, and macOS 26 hands what Safari has
                  learnt to Spotlight — see write_opensearch below.

THIS SCRIPT READS THE NEIGHBOURING REPOSITORIES. The three books are
separate repositories; the script expects their clones beside this one. It
therefore has to be re-run when a book changes, and the last line printed
says so.

    python3 tools/machine_files.py
"""

import datetime
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NEIGHBOURS = ROOT.parent
SITE = 'https://ido.help'


def weight_bytes(n: int) -> str:
    """A weight legible at a glance, so as to choose without arithmetic.

    In bytes and their multiples. This serves /llms.txt alone, which is in
    English: the pages themselves say « Ko » and « Mo », in Ido, and are
    not touched by it. It takes a COUNT and not a file, because the map
    prices one thing that is not a file — how far into the reading page a
    given article begins. See page_depth().
    """
    if n >= 1_048_576:
        return '%.1f MB' % (n / 1_048_576)
    if n >= 1024:
        return '%d kB' % (n / 1024)
    return '%d bytes' % n


def weight(p: Path) -> str:
    """The weight of a file that exists."""
    return weight_bytes(p.stat().st_size)


def found(book: str, *names):
    """A book's files that really exist, with their weight.

    We never DECLARE a file without having seen it: a map that announces
    what is not there is worse than no map at all.
    """
    base = NEIGHBOURS / book
    for n in names:
        f = base / n
        if f.exists():
            yield n, weight(f)


# --------------------------------------------------------------------------
# robots.txt
# --------------------------------------------------------------------------
# The language models' crawlers are named ONE BY ONE, and not covered by the
# star alone. The reason is practical: several of them look for their own name
# before falling back on the general rule, and some operators abstain when
# nothing addresses them. An explicit permission removes the doubt. Nor are
# they subject to any delay: the site is static and sits on GitHub Pages,
# which has no interest in the rate of visits.
ROBOTS = """# ido.help — three works of the international auxiliary language Ido.
#
# Everything is open, to everyone, without delay. The site is static: no
# rate of visits puts it under any strain.
#
# The MACHINE-READABLE versions are announced in /llms.txt — plain text
# and JSON, far cheaper than the pages themselves.

User-agent: *
Allow: /

# The language models' crawlers, named one by one: several look for their
# own name before the general rule, and abstain when nothing addresses
# them. Here, nothing stands in their way.
User-agent: ClaudeBot
Allow: /
User-agent: Claude-Web
Allow: /
User-agent: ClaudeBot-User
Allow: /
User-agent: GPTBot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: CCBot
Allow: /
User-agent: Applebot
Allow: /
User-agent: Applebot-Extended
Allow: /
User-agent: Bytespider
Allow: /
User-agent: Amazonbot
Allow: /
User-agent: meta-externalagent
Allow: /
User-agent: cohere-ai
Allow: /
User-agent: Diffbot
Allow: /
User-agent: omgili
Allow: /

Sitemap: {site}/sitemap.xml
"""


def write_robots():
    (ROOT / 'robots.txt').write_text(ROBOTS.format(site=SITE), encoding='utf-8')


# --------------------------------------------------------------------------
# sitemap.xml
# --------------------------------------------------------------------------
def write_sitemap(today: str):
    urls = [(f'{SITE}/', '1.0'),
            (f'{SITE}/tabeli/', '0.9'),
            (f'{SITE}/dicionario/', '0.9'),
            (f'{SITE}/gramatiko/', '0.9'),
            (f'{SITE}/llms.txt', '0.5')]

    # The machine-readable derivatives go into the map: without that an engine
    # would find them only by the page's link, and a crawler not at all.
    for book, names in (('tabeli', ('tabeli.md', 'tabeli.json')),
                        ('dicionario', ('dicionario.md', 'dicionario.json',
                                        'dicionario.jsonl', 'dicionario.tsv',
                                        'vortlisto.md')),
                        ('gramatiko', ('gramatiko.md',))):
        for n, _ in found(book, *names):
            urls.append((f'{SITE}/{book}/{n}', '0.6'))

    chapters = NEIGHBOURS / 'gramatiko' / 'chapitri'
    if (chapters / 'index.md').exists():
        urls.append((f'{SITE}/gramatiko/chapitri/index.md', '0.6'))
        for f in sorted(chapters.glob('*.md')):
            if f.name != 'index.md':
                urls.append((f'{SITE}/gramatiko/chapitri/{f.name}', '0.4'))

    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, priority in urls:
        lines += ['  <url>', f'    <loc>{u}</loc>', f'    <lastmod>{today}</lastmod>',
                  f'    <priority>{priority}</priority>', '  </url>']
    lines.append('</urlset>')
    (ROOT / 'sitemap.xml').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return len(urls)


# --------------------------------------------------------------------------
# llms.txt
# --------------------------------------------------------------------------
# THE BODY BELOW IS IN ENGLISH, and it is the one published page that is.
# The three interfaces are in Ido because they are read by people who came
# for Ido; /llms.txt is read by crawlers and by whoever is wiring a program
# up to the site, and English is what serves them. The titles of the three
# works keep their own names, which are the works' names.
#
# A MODEL ASKED FOR A DEFINITION HAS TWO WAYS TO BE WRONG, AND THIS FILE IS
# WHAT STANDS BETWEEN THEM AND THE ANSWER. It can fetch THE WRONG ADDRESS —
# the reading page rather than the flat list — and be truncated before it
# reaches the word. Or it can read the dictionary AS BILINGUAL and answer
# from the English cognate of the headword instead of the Ido definition
# printed under it. Both were observed, in one exchange:
#
#   ASKED WHAT « propoziciono » MEANS ACCORDING TO ido.help, ChatGPT
#   ANSWERED WITH THE SENSES OF THE ENGLISH « proposition » — proposal,
#   offer, logical assertion — and credited the Gramatiko with a sentence
#   it does not contain. The article gives four senses and « offer » is
#   not among them: (logiko), (gram.), (geom.), (teol.). Told it was
#   wrong, it fetched the page, was truncated, and gave up.
#
# The map said nothing that would have stopped either move. It listed four
# files by weight and called the dictionary « searchable »; it never said
# THE DEFINITIONS ARE IN IDO, and it offered « the page, with its search »
# beside the flat files without saying that the search is run BY THE
# BROWSER. Hence the two sections that now precede the listing: what the
# dictionary is, with an example read out of the book itself, and which
# address to fetch, with the measurement that condemns the other one.
EXAMPLE = 'propoziciono'


def example_entry(word):
    """The article for `word`, READ OUT OF THE BOOK, not copied to here.

    A worked example is the part of a map that gets imitated, so it must
    not be able to go stale: it is lifted from the neighbouring
    dicionario.md and vortlisto.md as the file is written. Absent the
    clones, the section is dropped rather than guessed at — the same rule
    as found().
    """
    base = NEIGHBOURS / 'dicionario'
    full, brief = base / 'dicionario.md', base / 'vortlisto.md'
    if not (full.exists() and brief.exists()):
        return None, None
    block = []
    for line in full.read_text(encoding='utf-8').splitlines():
        if block:
            if line.startswith('## '):
                break
            block.append(line)
        elif line == '## ' + word or line.startswith('## %s *' % word):
            block.append(line)
    while block and not block[-1].strip():
        block.pop()
    one = next((l for l in brief.read_text(encoding='utf-8').splitlines()
                if l.startswith(word + ' — ')), None)
    return (block or None), one


def page_depth(word):
    """How far into /dicionario/ the article for `word` BEGINS.

    THE FIGURE IS THE WHOLE ARGUMENT. The reading page carries all the
    articles as one JSON block and filters them in the browser, so
    « ?q=propoziciono » is answered by the page and not by the server. A
    fetcher that truncates therefore reads the head of the alphabet and
    concludes the word is absent. Saying « large » would not carry; saying
    that the word starts at 73 % of 2.1 MB does.
    """
    p = NEIGHBOURS / 'dicionario' / 'index.html'
    if not p.exists():
        return None
    h = p.read_text(encoding='utf-8')
    i = h.find('"v":"%s"' % word)
    return None if i < 0 else (i, len(h), 100.0 * i / len(h))


def articles():
    """The number of articles, counted rather than remembered."""
    import json
    p = NEIGHBOURS / 'dicionario' / 'dicionario.json'
    if not p.exists():
        return None
    return len(json.loads(p.read_text(encoding='utf-8')))


def write_llms():
    def listing(book, names, suffix=''):
        return [f'- [{n}]({SITE}/{book}/{n}) — {w}{suffix}'
                for n, w in found(book, *names)]

    n_art = articles()
    count = f'{n_art:,}' if n_art else '9,473'

    L = [
        '# ido.help',
        '',
        '> Three works of the international auxiliary language **Ido**, '
        'transcribed and exhaustively searchable: the Delmas-Tabeli (1926), '
        'the Dicionario de la 10.000 radiki (1934/1964), and the Kompleta '
        'Gramatiko Detaloza (1925). For the rights in each work, see the '
        "repository's page.",
        '',
        'Ido is an international auxiliary language, published in 1907 and '
        'derived from Esperanto. This site offers the three fundamental works '
        'in a form legible to people and to machines.',
        '',
        '## Read this before quoting a definition',
        '',
        '**The Dicionario defines Ido in Ido.** It is a MONOLINGUAL '
        'dictionary: the headword is Ido and so is the definition under it. '
        'There is no English column, here or anywhere on the site. An answer '
        "built from the English cognate of a headword is not this book's "
        'answer, and for most words it is not the same answer.',
        '',
        '**The languages listed against an article are not translations.** '
        'They are the languages in which the root is ATTESTED — the evidence '
        'on which Ido admitted it, printed `DEFIRS` in the book. `Angla` '
        'means the root has an English cognate. It does not mean the article '
        'gives an English gloss, and no article does.',
        '',
        '**Give the senses as they are numbered, with their fields.** Each '
        'sense carries the domain it belongs to — `(logiko)`, `(gram.)`, '
        '`(bot.)`, `(teol.)`. Quote them all, or say which one you are '
        'quoting.',
        '',
        '**A word may be absent, and that is an answer.** The %s articles '
        'are the ROOTS. A regularly derived form — `-eto`, `-ilo`, `-ero`, '
        '`-ala` — has no article of its own and is read off its root and the '
        "Gramatiko's affix chapters. If a headword is not in the list, say "
        'so; do not supply one from another dictionary.' % count,
        '',
        '**If the text could not be fetched, say that.** An article that was '
        'not read cannot be quoted, and the senses of the English cognate are '
        'not a substitute for it.',
        '',
    ]

    block, one = example_entry(EXAMPLE)
    if block:
        L += ['### A worked example — `%s`' % EXAMPLE, '',
              'In `dicionario.md`, the article stands under a `##` heading:',
              '']
        L += ['    ' + b for b in block]
        L += ['',
              'Four senses in four domains, every one of them defined in Ido; '
              'the trailing comment gives the page and line of the printing, '
              'then the attesting languages. The English word *proposition* '
              'would suggest an « offer » sense: the book has none.',
              '']
        if one:
            L += ['In `vortlisto.md` the same article is one line — headword, '
                  'then the first sense only:', '', '    ' + one, '']

    L += ['## Fetching one article without downloading the book', '']

    depth = page_depth(EXAMPLE)
    if depth:
        off, total, pct = depth
        L += ['**Do not fetch `%s/dicionario/?q=WORD` in order to READ a '
              'word.** The address is a real search and the page honours it, '
              'but the search is run BY THE BROWSER: the page carries every '
              'article as one JSON block and filters it after loading. The '
              'page weighs %s and the articles are in alphabetical order, so '
              '`%s` begins %s into it — %.0f %% of the way through. A fetcher '
              'that truncates before that point reads the letter A and '
              'reports the word missing. Use the address to send a PERSON to '
              'the word; do not use it to read the word.'
              % (SITE, weight(NEIGHBOURS / 'dicionario' / 'index.html'),
                 EXAMPLE, weight_bytes(off), pct),
              '']

    L += ['The files below are flat: no script runs, and one pass over any '
          'one of them finds any headword.',
          '',
          '- `vortlisto.md` — one line per article, `headword — first sense`. '
          'The cheapest whole dictionary there is, and enough to settle '
          'whether a word exists.',
          '- `dicionario.tsv` — one line per article, tab-separated, the '
          'senses joined by ` ¶ `. Columns: `vedetto fako senci nomi_latina '
          'simbolo_kemiala lingui kodo pagino ligno imago drapeli`.',
          '- `dicionario.md` — the complete articles, each under `## '
          'headword`.',
          '- `dicionario.json` — the same records, under SHORT keys; the '
          'table below reads them.',
          '- `dicionario.jsonl` — one record per line, under the long keys, '
          'and carrying `teksto`, the article as it stands in the printing.',
          '',
          '### The keys of `dicionario.json`',
          '',
          'They are short because the reading page carries this file inline, '
          "and its weight is the page's. `dicionario.jsonl` gives the same "
          'fields under the long names, which are the ones the project uses '
          'in prose.',
          '',
          '| key | long name | what it holds |',
          '| --- | --- | --- |',
          '| `v` | `vedetto` | the headword |',
          '| `f` | `fako` | the domain of the whole article, or `null` |',
          '| `b` | `senci` | the senses, in the order printed; each is '
          '`{"t": text, "u": sub-entries}` |',
          '| `u` | `sub` | phrases under a sense: `{"k": the phrase, '
          '"t": its definition}` |',
          '| `n` | `lingui` | the ATTESTING languages — not translations |',
          '| `p` | `pagino` | page of the 1964 printing |',
          '| `g` | `ligno` | line on that page |',
          '| `l` | `latina` | the Latin binomial, for plants and animals |',
          '| `y` | `simbolo` | the chemical symbol; present on 90 records |',
          '| `c` | `citita` | `1` where the headword is printed as a '
          'citation form (`amen`, `a posteriori`) |',
          '| `d` | `drapeli` | flags left by the transcription, for review |',
          '',
          '`y` and `c` are written only where they are set; the rest are on '
          'every record.',
          '',
          '## Where to start',
          '',
          'To **learn the grammar**, the chapters are the cheapest way in: '
          'each chapter is a separate file of some 10 kB. Do not download the '
          'whole book for one question.',
          '',
          '- [Table of the chapters](%s/gramatiko/chapitri/index.md) — the 49 '
          'chapters, with their sizes' % SITE,
          '',
          'To **look up a word**, the word list is short; the full entries '
          'are longer. Read the two sections above first.',
          '',
          '## Gramatiko — *Kompleta Gramatiko Detaloza*, L. de Beaufront, 1925',
          '']
    L += ['- [chapitri/index.md](%s/gramatiko/chapitri/index.md) — the table, '
          "with each chapter's size" % SITE]
    chapters = NEIGHBOURS / 'gramatiko' / 'chapitri'
    if chapters.exists():
        n = len([f for f in chapters.glob('*.md') if f.name != 'index.md'])
        L += ['- %d separate chapters, under `%s/gramatiko/chapitri/` — '
              'some 10 kB each' % (n, SITE)]
    L += listing('gramatiko', ('gramatiko.md',), ' — the whole book')
    L += ["- [gramatiko/](%s/gramatiko/) — the page, with its search "
          "(run in the browser, like the dictionary's)" % SITE, '']

    L += ['## Dicionario — *Dicionario de la 10.000 radiki*, M. Pesch, '
          '1934/1964',
          '',
          '%s articles. Ido defined in Ido — see above.' % count,
          '']
    L += listing('dicionario', ('vortlisto.md',),
                 ' — headword and first sense only')
    L += listing('dicionario', ('dicionario.md',), ' — the full articles')
    L += listing('dicionario', ('dicionario.tsv',),
                 ' — one line per article, tab-separated')
    L += listing('dicionario', ('dicionario.json',),
                 ' — the records, short keys')
    L += listing('dicionario', ('dicionario.jsonl',),
                 ' — one record per line, long keys, with the printed text')
    L += ['- [dicionario/](%s/dicionario/) — the page, for a PERSON to '
          'search' % SITE,
          '']

    L += ['## Tabeli — *Expliko-Libreto di la Delmas-Tabeli*, J. Guignon, 1926',
          '',
          'A table comparing **57 languages**. The keys of `tabeli.json` are '
          'those of `lingui/*.json`: to obtain any pair of languages, join '
          'them on the key.',
          '']
    L += listing('tabeli', ('tabeli.md',), ' — Ido and French side by side')
    L += listing('tabeli', ('tabeli.json',), ' — the keys and the two languages')
    L += listing('tabeli', ('lingui/index.json',),
                 ' — the 55 other languages offered')
    L += ['- [tabeli/](%s/tabeli/) — the page, with its search' % SITE, '']

    L += ['## Notes',
          '',
          '- The `.md`, `.json`, `.jsonl` and `.tsv` files are GENERATED from '
          'the pages. The source stays `index.html` in each repository.',
          '- The three works are transcriptions of printed books, and the '
          'transcription is the site\'s own work. Where an article is hard to '
          'read, `drapeli` says so rather than the text being mended.',
          '- No rate limit: the site is static.',
          '- Code and transcriptions: https://github.com/helpolinguo',
          '']
    (ROOT / 'llms.txt').write_text('\n'.join(L), encoding='utf-8')



# --------------------------------------------------------------------------
# opensearch.xml
# --------------------------------------------------------------------------
# WHAT THIS BUYS: "ido.help" + Tab, IN SPOTLIGHT. macOS 26 lets one type a
# site's name into Spotlight and press Tab to search INSIDE that site. It
# invents nothing: it hands over the list Safari keeps under Settings →
# Search → Manage Websites, and Safari fills that list from two sources —
# an OpenSearch description document, which Apple has read since Safari 8
# and calls the recommended way, or, failing that, a guess made from the
# metadata of a search form. We declare it rather than let it be guessed.
#
# THE DOCUMENT DESCRIBES ONE SEARCH, AND IT IS THE DICTIONARY'S. A domain
# gets one entry in that list, so the address below has to be the one worth
# reaching by a word: /dicionario/?q=. The Tabeli and the Gramatiko are
# searched from their own pages.
#
# THE TEMPLATE ONLY WORKS BECAUSE THE PAGE ANSWERS IT. /dicionario/ reads
# "?q=" at load and applies it to its search field — that came in with this
# file. An OpenSearch document pointing at an address that ignores its own
# query is a promise the site does not keep.
#
# THE TEXT IS IN IDO because it is shown: Safari prints ShortName and
# Description in the Manage Websites panel, and Spotlight prints the name
# beside the field. Sixteen characters is the limit OpenSearch sets on
# ShortName; « Ido » is the name the icon already carries.
#
# NOT DONE: the suggestions endpoint. OpenSearch allows a second address
# that returns completions as JSON as one types; it takes the typed word as
# a query parameter, which a static site on GitHub Pages cannot answer. The
# page's own search, once reached, does the rest.
OPENSEARCH = """<?xml version="1.0" encoding="UTF-8"?>
<OpenSearchDescription xmlns="http://a9.com/-/spec/opensearch/1.1/">
  <ShortName>Ido</ShortName>
  <Description>Serchez vorto en la Dicionario de la 10.000 radiki</Description>
  <Language>io</Language>
  <InputEncoding>UTF-8</InputEncoding>
  <Image width="192" height="192" type="image/png">{site}/icon-192.png</Image>
  <Url type="text/html" method="get"
       template="{site}/dicionario/?q={{searchTerms}}"/>
</OpenSearchDescription>
"""


def write_opensearch():
    (ROOT / 'opensearch.xml').write_text(OPENSEARCH.format(site=SITE),
                                         encoding='utf-8')


def main():
    # A MISSING CLONE DOES NOT FAIL, IT QUIETLY SHORTENS. found() declares
    # only what it has seen, so a run without the books beside this one
    # writes a valid map of almost nothing — 265 addresses went out of
    # sitemap.xml that way once, and were put back by hand. The absence is
    # therefore said aloud, BEFORE the files are written, and named.
    absent = [b for b in ('tabeli', 'dicionario', 'gramatiko')
              if not (NEIGHBOURS / b).is_dir()]
    if absent:
        print('  WARNING: %s not beside this repository (%s).'
              % (', '.join(absent), NEIGHBOURS))
        print('  sitemap.xml and llms.txt WILL BE WRITTEN SHORT. Clone the')
        print('  missing books and run again before committing.')

    today = os.environ.get('DATE') or datetime.date.today().isoformat()
    write_robots()
    n = write_sitemap(today)
    write_llms()
    write_opensearch()
    for f in ('robots.txt', 'sitemap.xml', 'llms.txt', 'opensearch.xml'):
        print('  %-14s %8s' % (f, weight(ROOT / f)))
    print('  %d addresses in the sitemap' % n)
    print('  (re-run when a book changes: the script reads the neighbouring repositories)')


if __name__ == '__main__':
    main()
