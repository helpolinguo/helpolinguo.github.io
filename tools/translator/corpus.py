"""The Ido text on ido.help, gathered into one place, and the books' tables.

READS THE THREE BOOK REPOSITORIES BESIDE THIS ONE, like machine_files.py, and
degrades the same way: a missing book is a missing section, not a crash. Every
count this package prints comes from here, so that no number in the README is
a supposition.

The three books hold three different KINDS of Ido, and the difference matters
more than the total:

    Dicionario  11,690 senses     definitions, written in Ido about Ido
    Gramatiko    ~900 paragraphs  prose about grammar, thick with cited forms
    Tabeli          672 segments  ordinary descriptive prose, the only running
                                  text of the three, and the only one aligned
                                  against another language
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
BOOKS = ROOT.parent

DICIONARIO = BOOKS / 'dicionario'
GRAMATIKO = BOOKS / 'gramatiko'
TABELI = BOOKS / 'tabeli'

# Ido is written in plain ASCII; the accented letters below turn up only in
# proper names and in the French of the Tabeli's left column.
WORD = re.compile(r"[a-zàâäçéèêëîïôöùûüÿ]+", re.I)


def tokens(text):
    return WORD.findall(text.lower())


# ---------------------------------------------------------------- the books

def dicionario():
    """The 9,473 articles, under the short keys llms.txt documents."""
    p = DICIONARIO / 'dicionario.json'
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else []


def verbi():
    """2,020 verbs marked transitive or not, and the 396 governing a
    preposition. The mark stands on the SENSE for 31 of them."""
    p = DICIONARIO / 'verbi.json'
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}


def tabeli():
    """672 segments, Ido and French, keyed."""
    p = TABELI / 'tabeli.json'
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}


def teksti(code):
    """One of the 55 other languages, `{key: text}` on the same 672 keys."""
    p = TABELI / 'teksti' / ('%s.json' % code)
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}


def glosaro(code='en-GB'):
    """The glossary's Ido -> other pairs, as (ido, other, [segment keys]).

    The JSON is read rather than the .md because it keeps the segment each
    pair was lifted from; the .md is the same pairs with that provenance
    dropped. `vorti` is the Ido -> other half and `inversa` the same pairs
    reversed, so only `vorti` is read here.

    NOT TRANSLATIONS COMPOSED BY ANYONE: each pair is the n-th bold run of a
    segment set against the n-th of the same segment in the other book.
    """
    p = TABELI / 'glosaro' / ('%s.json' % code)
    if not p.exists():
        return []
    raw = json.loads(p.read_text(encoding='utf-8'))
    out = []
    for ido, senses in (raw.get('vorti') or {}).items():
        for s in senses:
            out.append((ido, s['t'], s.get('k') or []))
    return out


def glosaro_languages():
    """The 56 codes the glossary is built for."""
    d = TABELI / 'glosaro'
    if not d.is_dir():
        return []
    return sorted(p.stem for p in d.glob('*.json'))


def gramatiko_text():
    p = GRAMATIKO / 'gramatiko.md'
    if not p.exists():
        return ''
    return re.sub(r'<!--.*?-->', ' ', p.read_text(encoding='utf-8'), flags=re.S)


def afixi():
    """The 65 affix files, `{affix: the book's own paragraphs}`."""
    d = GRAMATIKO / 'afixi'
    if not d.exists():
        return {}
    return {p.stem: p.read_text(encoding='utf-8')
            for p in sorted(d.glob('*.md')) if p.stem != 'index'}


# ------------------------------------------------------------- the corpora

def ido_documents():
    """Every passage of Ido on the site, as token lists, tagged by book.

    Returns (tag, tokens) pairs. The tag is what lets an experiment ask
    whether a result comes from the running text or only from the citations.
    """
    docs = []
    for r in dicionario():
        for s in r.get('b') or []:
            t = tokens(s.get('t') or '')
            if t:
                docs.append(('dicionario', t))
            for sub in s.get('u') or []:
                t = tokens('%s %s' % (sub.get('k') or '', sub.get('t') or ''))
                if t:
                    docs.append(('dicionario', t))
    for para in re.split(r'\n\s*\n', gramatiko_text()):
        t = tokens(para)
        if t:
            docs.append(('gramatiko', t))
    for v in tabeli().values():
        t = tokens(v.get('io') or '')
        if t:
            docs.append(('tabeli', t))
    return docs


def have_books():
    return {'dicionario': DICIONARIO.is_dir(),
            'gramatiko': GRAMATIKO.is_dir(),
            'tabeli': TABELI.is_dir()}


if __name__ == '__main__':
    import collections
    print('books beside this one:', have_books())
    docs = ido_documents()
    freq = collections.Counter(w for _, d in docs for w in d)
    n = sum(len(d) for _, d in docs)
    per = collections.Counter(tag for tag, _ in docs)
    print('documents %d  tokens %d  types %d' % (len(docs), n, len(freq)))
    for tag in ('dicionario', 'gramatiko', 'tabeli'):
        t = sum(len(d) for g, d in docs if g == tag)
        print('  %-11s %5d documents %7d tokens' % (tag, per[tag], t))
    print('hapax %d (%.1f%% of types)' % (
        sum(1 for c in freq.values() if c == 1),
        100 * sum(1 for c in freq.values() if c == 1) / len(freq)))
