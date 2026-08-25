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

    The units are the ones the page itself uses, in Ido: "o" for octets,
    "Ko" and "Mo" for their multiples. They are published text, not code,
    and they stay as they are.
    """
    n = p.stat().st_size
    if n >= 1_048_576:
        return '%.1f Mo' % (n / 1_048_576)
    if n >= 1024:
        return '%d Ko' % (n / 1024)
    return '%d o' % n


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
ROBOTS = """# ido.help — tri verki dil helpolinguo internaciona Ido.
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
# The body below is IN IDO, like the three interfaces: it is published text,
# addressed to whoever reads the site, and it is not translated with the rest
# of the source.
def write_llms():
    def listing(book, names, suffix=''):
        return [f'- [{n}]({SITE}/{book}/{n}) — {w}{suffix}'
                for n, w in found(book, *names)]

    L = [
        '# ido.help',
        '',
        '> Tri verki dil helpolinguo internaciona **Ido**, transskribita ed '
        'exhaustive serchebla : la Delmas-Tabeli (1926), la Dicionario de la '
        '10.000 radiki (1934/1964), e la Kompleta Gramatiko Detaloza (1925). '
        'Pri la yuri di singla verko, videz la pagino di la deposito.',
        '',
        'Ido esas helpolinguo internaciona, publikigita en 1907, derivita de '
        'Esperanto. Ca sito ofras la tri verki fundamentala en formo lektebla '
        'da homi ed da mashini.',
        '',
        '## Por komencar',
        '',
        'Se vu volas **lernar la gramatiko**, la chapitri esas la maxim '
        'ekonomiala voyo : singla chapitro esas apartra dosiero de cirkum '
        '10 Ko. Ne deskargez la tota libro por un questiono.',
        '',
        '- [Tabelo dil chapitri](%s/gramatiko/chapitri/index.md) — la 49 '
        'chapitri, kun lia grandeso' % SITE,
        '',
        'Se vu volas **serchar vorto**, la vortlisto esas kurta ; la kompleta '
        'artikli esas plu longa.',
        '',
        '## Gramatiko — *Kompleta Gramatiko Detaloza*, L. de Beaufront, 1925',
        '',
    ]
    L += ['- [chapitri/index.md](%s/gramatiko/chapitri/index.md) — la tabelo, '
          'kun la grandeso di singla chapitro' % SITE]
    chapters = NEIGHBOURS / 'gramatiko' / 'chapitri'
    if chapters.exists():
        n = len([f for f in chapters.glob('*.md') if f.name != 'index.md'])
        L += ['- %d chapitri apartra, en `%s/gramatiko/chapitri/` — '
              'cirkum 10 Ko singla' % (n, SITE)]
    L += listing('gramatiko', ('gramatiko.md',), ' — la tota libro')
    L += ['- [gramatiko/](%s/gramatiko/) — la pagino, kun sercho' % SITE, '']

    L += ['## Dicionario — *Dicionario de la 10.000 radiki*, M. Pesch, 1934/1964',
          '']
    L += listing('dicionario', ('vortlisto.md',), ' — vedvorto e unesma senco nur')
    L += listing('dicionario', ('dicionario.md',), ' — la kompleta artikli')
    L += listing('dicionario', ('dicionario.json',), ' — la datumi, por interogar')
    L += ['- [dicionario/](%s/dicionario/) — la pagino, kun sercho' % SITE, '']

    L += ['## Tabeli — *Expliko-Libreto di la Delmas-Tabeli*, J. Guignon, 1926',
          '',
          'Tabelo komparanta en **57 lingui**. La klefi di `tabeli.json` esas '
          'ti di `lingui/*.json` : por obtenar irga paro di lingui, junktez li '
          'per la klefo.',
          '']
    L += listing('tabeli', ('tabeli.md',), ' — Ido e Franca en regardo')
    L += listing('tabeli', ('tabeli.json',), ' — la klefi e la du lingui')
    L += listing('tabeli', ('lingui/index.json',), ' — la 55 altra lingui ofrata')
    L += ['- [tabeli/](%s/tabeli/) — la pagino, kun sercho' % SITE, '']

    L += ['## Noti',
          '',
          '- La `.md` e `.json` esas ENGENDRATA de la pagini. La fonto restas '
          '`index.html` en singla deposito.',
          '- Nula limito di frequeso : la sito esas statika.',
          '- Kodexo e transskribi : https://github.com/helpolinguo',
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
