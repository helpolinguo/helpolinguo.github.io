#!/usr/bin/env python3
"""Generates the site's front-door files FOR MACHINES: robots, map, llms,
search.

WHY AT THE ROOT. The four sites share one origin — the home page is the
user site, the three books are project sites. But "/robots.txt" and
"/sitemap.xml" are only read at the ROOT of a domain: a robots.txt dropped
into /tabeli/ would be read by nobody. These files can therefore only live
here, and they speak for all four sites.

WHAT EACH ONE DOES

  robots.txt      says yes to everyone, by name — including the language
                  models' crawlers, which many sites block and which, for
                  want of a mention, sometimes abstain of their own accord.
  sitemap.xml     a <sitemapindex> over the two below. robots.txt points
                  at this one address, and it does not move.
  sitemap-pages   the site's pages and the whole-book files — 9 kB.
  sitemap-vorti   one address per article, 9461 of them — 1.3 MB. Kept
                  apart so an engine re-reading the pages does not pay
                  for the dictionary every time.
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
import re
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
# A SITEMAP HOLDS 50 000 ADDRESSES AND 50 MB, AND ONE FILE PER WORD WOULD
# NOT BREACH EITHER — 9461 articles come to 1.2 MB. It would still be the
# wrong shape. The pages of this site and the articles of one book change on
# different days and for different reasons, and a crawler re-reading a single
# 1.2 MB map to learn that the home page moved is paying for the book every
# time. An INDEX lets it fetch the 9 kB half and leave the rest alone.
#
# So /sitemap.xml is now a <sitemapindex> naming two children, and it is the
# index that robots.txt points at — one address, unchanged, which is what
# every engine already has on file.
def xml_(t: str) -> str:
    """An address, safe to put between XML tags.

    The slugs under vorti/ are [a-z0-9-] and the chapters' are no wider, so
    today this changes nothing and is verified to. It is here because a
    generator that emits XML without escaping is one odd filename away from
    emitting a broken map, and the map is the thing nobody reads until it
    has already failed.
    """
    return (t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
             .replace('"', '&quot;').replace("'", '&apos;'))


def urlset(urls, today: str) -> str:
    """One <urlset>: the addresses, each with the day and its priority."""
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, priority in urls:
        lines += ['  <url>', f'    <loc>{xml_(u)}</loc>',
                  f'    <lastmod>{today}</lastmod>',
                  f'    <priority>{priority}</priority>', '  </url>']
    lines.append('</urlset>')
    return '\n'.join(lines) + '\n'


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

    vorti = NEIGHBOURS / 'dicionario' / 'vorti'
    if (vorti / 'index.md').exists():
        urls.append((f'{SITE}/dicionario/vorti/index.md', '0.6'))

    # temi/ is ten files, not 9461: they go in beside the pages rather
    # than into a child of their own.
    # The 55 language files are the Tabeli's other half, and the map named
    # only their index.
    clean = NEIGHBOURS / 'tabeli' / 'teksti'
    if (clean / 'index.json').exists():
        for f in sorted(clean.glob('*.json')):
            urls.append((f'{SITE}/tabeli/teksti/{f.name}', '0.5'))

    lingui = NEIGHBOURS / 'tabeli' / 'lingui'
    if (lingui / 'index.json').exists():
        for f in sorted(lingui.glob('*.json')):
            if f.name != 'index.json':
                urls.append((f'{SITE}/tabeli/lingui/{f.name}', '0.5'))

    temi = NEIGHBOURS / 'gramatiko' / 'temi'
    if (temi / 'index.md').exists():
        urls.append((f'{SITE}/gramatiko/temi/index.md', '0.6'))
        for f in sorted(temi.glob('*.md')):
            if f.name != 'index.md':
                urls.append((f'{SITE}/gramatiko/temi/{f.name}', '0.5'))

    chapters = NEIGHBOURS / 'gramatiko' / 'chapitri'
    if (chapters / 'index.md').exists():
        urls.append((f'{SITE}/gramatiko/chapitri/index.md', '0.6'))
        for f in sorted(chapters.glob('*.md')):
            if f.name != 'index.md':
                urls.append((f'{SITE}/gramatiko/chapitri/{f.name}', '0.4'))

    (ROOT / 'sitemap-pages.xml').write_text(urlset(urls, today),
                                            encoding='utf-8')

    # THE ARTICLES, one address each. They are sorted so the file is stable
    # between runs: a map that reshuffles itself is a diff nobody can read.
    articles = sorted(f.name[:-3] for f in vorti.glob('*.md')
                      if f.name != 'index.md') if vorti.is_dir() else []
    child = ROOT / 'sitemap-vorti.xml'
    if articles:
        child.write_text(
            urlset([(f'{SITE}/dicionario/vorti/{a}.md', '0.3')
                    for a in articles], today), encoding='utf-8')
    elif child.exists():
        # A CHILD LEFT BEHIND IS A MAP OF FILES THAT MAY NO LONGER BE THERE,
        # and it would go on being served and crawled. vorti/ is emptied at
        # every run in the other repository for the same reason.
        child.unlink()

    children = ['sitemap-pages.xml'] + (['sitemap-vorti.xml'] if articles
                                        else [])
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for c in children:
        lines += ['  <sitemap>', f'    <loc>{SITE}/{c}</loc>',
                  f'    <lastmod>{today}</lastmod>', '  </sitemap>']
    lines.append('</sitemapindex>')
    (ROOT / 'sitemap.xml').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return len(urls), len(articles)



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

# The examples are the rule. Naming the operations would want words that are
# not in the book — see the note in dicionario's machine_readable.py — and a
# headword beside its real address says the same thing in no language at all.
# Every pair is CHECKED AGAINST THE DIRECTORY before it is printed.
SHOWN = ('propoziciono', '-a', 'a(d)', 'a posteriori', '*golfo', 'ah!',
         'ampère', '«brokoli»-kaulo')


def per_word():
    """vorti/ — how many files, how big, and a few real addresses.

    Returns None when the directory is not there, so the section is left out
    rather than promised: an address announced and not served is worse than
    one not announced.
    """
    import unicodedata
    out = NEIGHBOURS / 'dicionario' / 'vorti'
    if not (out / 'index.md').exists():
        return None

    def slug(v):
        t = unicodedata.normalize('NFD', v.lower())
        t = ''.join(c for c in t if unicodedata.category(c) != 'Mn')
        t = re.sub(r'[^a-z0-9-]', '', t.replace(' ', '-'))
        return re.sub(r'-{2,}', '-', t)

    files = [f for f in out.glob('*.md') if f.name != 'index.md']
    if not files:
        return None
    rows = [(v, slug(v)) for v in SHOWN if (out / (slug(v) + '.md')).exists()]
    total = sum(f.stat().st_size for f in files)
    return len(files), total // len(files), rows, weight(out / 'index.md')


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



def per_topic():
    """temi/ — the topics that cross the chapters, with their weights.

    Same rule as per_word(): None when the directory is not beside this
    repository, so the section falls out rather than promising an address
    nothing serves. The titles are READ OUT OF temi/index.md and never
    listed here, so a topic added or renamed there needs no edit in this
    file.
    """
    out = NEIGHBOURS / 'gramatiko' / 'temi'
    idx = out / 'index.md'
    if not idx.exists():
        return None
    rows = re.findall(r'^\| (.+?) \| +(\d+) \| \[([^\]]+)\]',
                      idx.read_text(encoding='utf-8'), re.M)
    files = [f for f in out.glob('*.md') if f.name != 'index.md']
    if not (rows and files):
        return None
    return (rows, len(files), weight(idx),
            weight_bytes(sum(f.stat().st_size for f in files)),
            numbering(idx.read_text(encoding='utf-8')))


# THE FIGURES ARE READ, NOT RESTATED. They were written out here by hand
# once — « 138 paragraphs carry a number », « § 32 cannot be found by
# number » — and helpolinguo/gramatiko#14 falsified both in one commit: it
# repaired § 32, which the site then went on asserting was unreachable.
# temi/index.md is generated from the chapters at every build, so it is the
# one place the numbers can be true, and it is where they are now taken
# from. A figure this file cannot read, it does not print.
NUMBERING = re.compile(
    r'numerizas (\d+) paragrafi, de § (\d+) a § (\d+).*?'
    r'([\d\u202f,]+) bloki, ([\d\u202f,]+) okteti, ne portas numero, '
    r'e (\d+) chapitri', re.S)


def numbering(idx: str):
    """How the book numbers itself, out of temi/index.md.

    Returns None when the shape of that file has moved under us — better a
    section that says less than a section that says something false, which
    is the whole reason this function exists.
    """
    m = NUMBERING.search(idx)
    if not m:
        return None
    n = lambda t: int(re.sub(r'[^0-9]', '', t))
    quirks = re.findall(r'^- \*\*§ (\d+)', idx, re.M)
    return {'numbered': n(m.group(1)), 'first': n(m.group(2)),
            'last': n(m.group(3)), 'blocks_un': n(m.group(4)),
            'bytes_un': n(m.group(5)), 'chapters_un': n(m.group(6)),
            'quirks': quirks}



# THE ONE PLACE ON THIS SITE WHERE IDO STANDS BESIDE ANOTHER LANGUAGE. The
# Dicionario defines Ido in Ido and the Gramatiko is in Ido throughout, so a
# reader who wants « what is the Ido for X » has, in those two, nothing to
# go on. The Tabeli has: 672 segments, aligned on one key, in 57 languages,
# English among them. The map said « 57 languages » and « join them on the
# key » and named not one of them, so nothing in it revealed that an
# attested Ido–English pair was there to be had.
PARALLEL_EXAMPLE = 't01-01-1'


def parallel():
    """The Tabeli as a parallel text: how many segments, which languages,
    and one real pair.

    The alignment is CHECKED here, not asserted: every language file must
    carry exactly the keys tabeli.json carries, or the claim that a join
    cannot miss is not made. None when the book is not beside us.
    """
    import json
    base = NEIGHBOURS / 'tabeli'
    main, idx = base / 'tabeli.json', base / 'lingui' / 'index.json'
    if not (main.exists() and idx.exists()):
        return None
    t = json.loads(main.read_text(encoding='utf-8'))
    codes = [l['kodexo'] for l in
             json.loads(idx.read_text(encoding='utf-8'))['lingui']]

    aligned, shapes = 0, set()
    for c in codes:
        f = base / 'lingui' / (c + '.json')
        if not f.exists():
            continue
        d = json.loads(f.read_text(encoding='utf-8'))
        shapes.add(tuple(sorted(d)))
        if set(d.get('k', {})) == set(t):
            aligned += 1
    if not aligned:
        return None

    pair = None
    en = base / 'lingui' / 'en-GB.json'
    if en.exists() and PARALLEL_EXAMPLE in t:
        k = json.loads(en.read_text(encoding='utf-8')).get('k', {})
        if PARALLEL_EXAMPLE in k:
            pair = (t[PARALLEL_EXAMPLE]['io'], k[PARALLEL_EXAMPLE])
    # THE TWO SIDES ARE NOT IN THE SAME FORMAT, and a reader told to join
    # them has to be told that too: tabeli.json is Markdown, the language
    # files are the page's own HTML, furniture included.
    # helpolinguo/tabeli#15 added teksti/: the same 55 languages through the
    # same cleaner that makes tabeli.json. lingui/ stays what it always was,
    # the browser's payload — so the map must now send a READER to teksti/
    # and stop telling them to strip tags they need never see.
    clean = base / 'teksti'
    cl = sorted(f.name[:-5] for f in clean.glob('*.json')
                if f.name != 'index.json') if clean.is_dir() else []
    cl_pair, cl_weight, cl_aligned = None, None, 0
    if cl:
        for c in cl:
            d = json.loads((clean / (c + '.json')).read_text(encoding='utf-8'))
            if set(d) == set(t):
                cl_aligned += 1
        f = clean / 'en-GB.json'
        if f.exists():
            k = json.loads(f.read_text(encoding='utf-8'))
            cl_weight = weight(f)
            if PARALLEL_EXAMPLE in k and PARALLEL_EXAMPLE in t:
                cl_pair = (t[PARALLEL_EXAMPLE]['io'], k[PARALLEL_EXAMPLE])

    md = sum(v['io'].count('**') for v in t.values())
    tags = butt = 0
    if en.exists():
        k = json.loads(en.read_text(encoding='utf-8')).get('k', {})
        tags = sum(len(re.findall(r'<[a-z][^>]*>', v)) for v in k.values())
        butt = sum(len(re.findall(r'<button', v)) for v in k.values())
    return {'segments': len(t), 'codes': codes, 'aligned': aligned,
            'shapes': sorted('/'.join(x) for x in shapes), 'pair': pair,
            'md': md, 'tags': tags, 'buttons': butt,
            'clean': cl, 'clean_pair': cl_pair, 'clean_weight': cl_weight,
            'clean_aligned': cl_aligned,
            'weight': weight(en) if en.exists() else None}


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
        '**To go the other way — from a meaning to an Ido word — search the '
        'DEFINITIONS.** The book has no index in any other language, but its '
        'definitions are text: `fugar` is reached by looking through '
        '`vortlisto.md` for « forirar » or « evitar », not by looking up '
        '*flee*. And for a concrete word there is the Tabeli below, which is '
        'a parallel text in 57 languages and the one place on this site where '
        'Ido stands beside English.',
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

    pw = per_word()
    if pw:
        n_files, avg, rows, idx_w = pw
        L += ['**One word is one file, and you can WORK OUT its address** — '
              'nothing to search, and no index to fetch first:',
              '',
              '    %s/dicionario/vorti/%s.md' % (SITE, EXAMPLE),
              '',
              'That is %d bytes. The rule is four steps: lower case, fold the '
              'accent, a space becomes a hyphen, drop anything else. Ido is '
              'written in plain ASCII, so it changes almost nothing.'
              % avg,
              '']
        if rows:
            L += ['| headword | address |', '| --- | --- |']
            L += ['| `%s` | `%s/dicionario/vorti/%s.md` |' % (v, SITE, sl)
                  for v, sl in rows]
            L += ['']
        L += ['The four marks dropped there carry sense in the book and none '
              'of them survives a URL: the asterisk of the word NOT OFFICIAL, '
              'the exclamation of the interjections, the parentheses of '
              '`a(d)`, the guillemets of `«brokoli»-kaulo`. They are gone from '
              'the ADDRESS only — each file prints its headword as the book '
              'sets it.',
              '',
              '%s articles sit at %s addresses. Twelve addresses hold two '
              'articles apiece, and serve both, so the rule never needs a '
              'suffix. **A 404 means the word is not a headword** — most '
              'often because it is a regular derivation, which this book '
              'leaves to its root.'
              % (count, f'{n_files:,}'),
              '',
              '- [vorti/index.md](%s/dicionario/vorti/index.md) — %s — every '
              'address, for a crawler. A reader who knows the word does not '
              'need it.' % (SITE, idx_w),
              '']

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

    L += ['### The whole book, when one word is not what is wanted',
          '',
          'These are flat: no script runs, and one pass over any one of them '
          'finds any headword.',
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
          'whole book for one question.'
          + (' For a rule that no chapter is about — the `-n` ending, the '
             'participle, the passive — fetch its topic file under '
             '`%s/gramatiko/temi/` instead.' % SITE if per_topic() else ''),
          '',
          '- [Table of the chapters](%s/gramatiko/chapitri/index.md) — the 49 '
          'chapters, with their sizes' % SITE,
          '',
          ('To **look up a word**, fetch it on its own — '
           '`%s/dicionario/vorti/WORD.md`, some 600 bytes. Read the two '
           'sections above first: the address rule is four steps, and the '
           'definitions are in Ido.' % SITE) if per_word() else
          ('To **look up a word**, the word list is short; the full entries '
           'are longer. Read the two sections above first.'),
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
    pt = per_topic()
    if pt:
        rows, n_files, idx_w, total_w, num = pt
        L += ['- [temi/index.md](%s/gramatiko/temi/index.md) — %s — %d TOPICS '
              'THAT CROSS THE CHAPTERS, %s in all'
              % (SITE, idx_w, n_files, total_w)]
    L += listing('gramatiko', ('gramatiko.md',), ' — the whole book')
    L += ["- [gramatiko/](%s/gramatiko/) — the page, with its search "
          "(run in the browser, like the dictionary's)" % SITE, '']

    if pt:
        rows, n_files, idx_w, total_w, num = pt
        L += ['### A rule that has no chapter', '',
              'The book is split by chapter, which answers *how is the plural '
              'formed* — there is a chapter called LA PLURALO EN IDO. It does '
              'not answer *what does this grammar say about the `-n` ending*, '
              'because no chapter is about it: that discussion is spread over '
              'SINTAXO, VORTORDINO, ADVERBI and four more. `temi/` collects '
              'each such topic into one file.',
              '',
              '| topic | blocks | address |', '| --- | ---: | --- |']
        L += ['| %s | %s | `%s/gramatiko/temi/%s` |' % (t, n, SITE, f)
              for t, n, f in rows]
        L += ['',
              '**Each file is the book quoted, not grammar rewritten.** Every '
              'block in it is lifted verbatim from the chapters; the one '
              'editorial act is the choice of search terms, and each file '
              'prints the terms that built it. Nothing there is a rule '
              'composed by this site.',
              '',
              ('**Citations use the numbers the book prints** — `§ 126` — '
               'but BEAUFRONT NUMBERED LESS THAN HALF HIS OWN BOOK: %d '
               'paragraphs carry a number, § %d to § %d, and %s blocks carry '
               'none, %d of the 49 chapters having no number anywhere. A '
               'block in an unnumbered chapter is therefore cited by its '
               'chapter and its rank.'
               % (num['numbered'], num['first'], num['last'],
                  f"{num['blocks_un']:,}", num['chapters_un'])
               if num else
               '**Citations use the numbers the book prints** — `§ 126` — '
               'but the book does not number all of itself: a block in an '
               'unnumbered chapter is cited by its chapter and its rank.'),
              '']
        if num and num['quirks']:
            L += ['%s also %s not behave — %s — and `temi/index.md` says how, '
                  'because a citation by number needs it.'
                  % ('One number' if len(num['quirks']) == 1
                     else '%d numbers' % len(num['quirks']),
                     'does' if len(num['quirks']) == 1 else 'do',
                     ', '.join('§ ' + q for q in num['quirks'])),
                  '']
    L += ['## Dicionario — *Dicionario de la 10.000 radiki*, M. Pesch, '
          '1934/1964',
          '',
          '%s articles. Ido defined in Ido — see above.' % count,
          '']
    if per_word():
        L += ['- [vorti/%s.md](%s/dicionario/vorti/%s.md) — ~600 bytes — '
              'ONE FILE PER WORD, and the address is the headword: any '
              'other one is reached the same way'
              % (EXAMPLE, SITE, EXAMPLE)]
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
          '']
    pl = parallel()
    if pl:
        L += ['**A PARALLEL TEXT IN 57 LANGUAGES.** %s segments, each aligned '
              'on one key, in Ido, French and %d more — `en-GB` and `en-US` '
              'among them.' % (f"{pl['segments']:,}", len(pl['codes'])),
              '',
              '**THIS IS THE ONLY PLACE ON THE SITE WHERE IDO STANDS BESIDE '
              'ANOTHER LANGUAGE.** The Dicionario defines Ido in Ido and the '
              'Gramatiko is in Ido throughout, so neither can answer *what is '
              'the Ido for X*. This can, from an attested text rather than '
              'from invention.',
              '']
    else:
        L += ['A table comparing **57 languages**. The keys of `tabeli.json` '
              'are those of `lingui/*.json`: to obtain any pair of languages, '
              'join them on the key.',
              '']
    L += listing('tabeli', ('tabeli.md',), ' — Ido and French side by side')
    L += listing('tabeli', ('tabeli.json',), ' — the keys and the two languages')
    L += listing('tabeli', ('lingui/index.json',),
                 ' — the 55 other languages offered')
    if pl and pl['clean']:
        L += ['- `%s/tabeli/teksti/<code>.json` — one per language, %s each — '
              '`{key: text}`, CLEAN: the same Markdown as `tabeli.json`, '
              'nothing to strip' % (SITE, pl['clean_weight'] or '~140 kB')]
    if pl:
        L += ['- `%s/tabeli/lingui/<code>.json` — the same languages as the '
              "PAGE eats them, %s each — HTML with the reading page's "
              'furniture in it. Not for text.'
              % (SITE, pl['weight'] or '~450 kB')]
    L += ['- [tabeli/](%s/tabeli/) — the page, with its search' % SITE, '']
    if pl:
        L += ['Codes: %s.' % ', '.join('`%s`' % c for c in pl['codes']),
              '', '### Joining two languages', '']
        def clip(t, n=140):
            return t if len(t) <= n else t[:t.rfind(' ', 0, n)] + ' …'
        pair = pl['clean_pair'] or pl['pair']
        src = 'teksti' if pl['clean_pair'] else 'lingui'
        if pair:
            io, en = (clip(t) for t in pair)
            left = '%s/en-GB.json' % src
            w = max(len('tabeli.json'), len(left))
            L += ['    %-*s  %s  io  %s' % (w, 'tabeli.json',
                                            PARALLEL_EXAMPLE, io),
                  '    %-*s  %s      %s' % (w, left, PARALLEL_EXAMPLE, en),
                  '']
        L += [('MEASURED: all %d files under `teksti/` carry EXACTLY the %s '
               'keys of `tabeli.json`, and so do all %d under `lingui/`. A '
               'join on the key cannot miss.'
               % (pl['clean_aligned'], f"{pl['segments']:,}", pl['aligned'])
               if pl['clean'] else
               'MEASURED: all %d language files carry EXACTLY the %s keys of '
               '`tabeli.json`, and all have the same shape (%s). A join on '
               'the key cannot miss.'
               % (pl['aligned'], f"{pl['segments']:,}",
                  ', '.join(pl['shapes']))),
              '',
              ('**TWO DIRECTORIES, AND ONLY ONE OF THEM IS TEXT.** '
               '`teksti/` is the clean half: the same Markdown as '
               '`tabeli.json` — %s `**` marks in the Ido, and nothing to '
               'strip on either side. `lingui/` is what the PAGE eats, and '
               'carries its furniture: %s tags in `en-GB`, of which %s are '
               '`<button>` — the magnifier that reveals a plate reference, '
               'not text. Use `teksti/` for reading and quoting; `lingui/` '
               'only if you are rebuilding the page.'
               % (f"{pl['md']:,}", f"{pl['tags']:,}", f"{pl['buttons']:,}")
               if pl['clean'] else
               '**THE TWO SIDES ARE NOT IN THE SAME FORMAT.** `tabeli.json` '
               'is Markdown — %s `**` marks in the Ido and no HTML at all. '
               "The language files are the reading page's own HTML: %s tags "
               'in `en-GB`, of which %s are `<button>`. STRIP THE TAGS '
               'BEFORE QUOTING.'
               % (f"{pl['md']:,}", f"{pl['tags']:,}", f"{pl['buttons']:,}")),
              '',
              '**What it is and is not.** %s segments of concrete vocabulary — '
              'a schoolroom, a house, trades, games — in whole sentences, '
              'which is what makes it usable for WRITING Ido and not only for '
              'reading it. It is one book and one register: no abstract '
              'vocabulary, and not a dictionary. For a word, the Dicionario; '
              'for a rule, the Gramatiko.' % f"{pl['segments']:,}",
              '']

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
    n, n_vorti = write_sitemap(today)
    write_llms()
    write_opensearch()
    for f in ('robots.txt', 'sitemap.xml', 'sitemap-pages.xml',
              'sitemap-vorti.xml', 'llms.txt', 'opensearch.xml'):
        if (ROOT / f).exists():
            print('  %-18s %8s' % (f, weight(ROOT / f)))
    print('  %d addresses in sitemap-pages, %d in sitemap-vorti'
          % (n, n_vorti))
    print('  (re-run when a book changes: the script reads the neighbouring repositories)')


if __name__ == '__main__':
    main()
