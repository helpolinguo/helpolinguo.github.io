#!/usr/bin/env python3
"""Generates the site's front-door files FOR MACHINES: robots, map, llms.

WHY AT THE ROOT. The four sites share one origin — the home page is the
user site, the three books are project sites. But "/robots.txt" and
"/sitemap.xml" are only read at the ROOT of a domain: a robots.txt dropped
into /tabeli/ would be read by nobody. These three files can therefore only
live here, and they speak for all four.

WHAT EACH ONE DOES

  robots.txt   says yes to everyone, by name — including the language
               models' crawlers, which many sites block and which, for want
               of a mention, sometimes abstain of their own accord.
  sitemap.xml  lists the pages for search engines.
  llms.txt     the map, for the use of models: what the site holds, in what
               form, AND AT WHAT PRICE. It is the stated weight that
               counts: it allows a choice to be made BEFORE downloading,
               and that, far more than compression, is where the saving is.

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


def weight(p: Path) -> str:
    """A weight legible at a glance, so as to choose without arithmetic.

    In bytes and their multiples. This function serves /llms.txt alone,
    which is in English: the pages themselves say « Ko » and « Mo », in
    Ido, and are not touched by it.
    """
    n = p.stat().st_size
    if n >= 1_048_576:
        return '%.1f MB' % (n / 1_048_576)
    if n >= 1024:
        return '%d kB' % (n / 1024)
    return '%d bytes' % n


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
def write_llms():
    def listing(book, names, suffix=''):
        return [f'- [{n}]({SITE}/{book}/{n}) — {w}{suffix}'
                for n, w in found(book, *names)]

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
        '## Where to start',
        '',
        'To **learn the grammar**, the chapters are the cheapest way in: each '
        'chapter is a separate file of some 10 kB. Do not download the whole '
        'book for one question.',
        '',
        '- [Table of the chapters](%s/gramatiko/chapitri/index.md) — the 49 '
        'chapters, with their sizes' % SITE,
        '',
        'To **look up a word**, the word list is short; the full entries are '
        'longer.',
        '',
        '## Gramatiko — *Kompleta Gramatiko Detaloza*, L. de Beaufront, 1925',
        '',
    ]
    L += ['- [chapitri/index.md](%s/gramatiko/chapitri/index.md) — the table, '
          "with each chapter's size" % SITE]
    chapters = NEIGHBOURS / 'gramatiko' / 'chapitri'
    if chapters.exists():
        n = len([f for f in chapters.glob('*.md') if f.name != 'index.md'])
        L += ['- %d separate chapters, under `%s/gramatiko/chapitri/` — '
              'some 10 kB each' % (n, SITE)]
    L += listing('gramatiko', ('gramatiko.md',), ' — the whole book')
    L += ['- [gramatiko/](%s/gramatiko/) — the page, with its search' % SITE, '']

    L += ['## Dicionario — *Dicionario de la 10.000 radiki*, M. Pesch, 1934/1964',
          '']
    L += listing('dicionario', ('vortlisto.md',),
                 ' — headword and first sense only')
    L += listing('dicionario', ('dicionario.md',), ' — the full entries')
    L += listing('dicionario', ('dicionario.json',),
                 ' — the data, to be queried')
    L += ['- [dicionario/](%s/dicionario/) — the page, with its search' % SITE,
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
          '- The `.md` and `.json` files are GENERATED from the pages. The '
          'source stays `index.html` in each repository.',
          '- No rate limit: the site is static.',
          '- Code and transcriptions: https://github.com/helpolinguo',
          '']
    (ROOT / 'llms.txt').write_text('\n'.join(L), encoding='utf-8')


def main():
    today = os.environ.get('DATE') or datetime.date.today().isoformat()
    write_robots()
    n = write_sitemap(today)
    write_llms()
    for f in ('robots.txt', 'sitemap.xml', 'llms.txt'):
        print('  %-14s %8s' % (f, weight(ROOT / f)))
    print('  %d addresses in the sitemap' % n)
    print('  (re-run when a book changes: the script reads the neighbouring repositories)')


if __name__ == '__main__':
    main()
