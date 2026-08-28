"""WHAT THE RULES REACH, COUNTED OVER THE SITE'S OWN IDO.

The claim being tested is that the Dicionario's roots plus the Gramatiko's 65
affixes plus the regular endings ACCOUNT FOR RUNNING IDO -- that the two books
together are a lexicon, not merely two books. If they do, a rule-based
translator has a lexicon; if they do not, it has a hole that no amount of
grammar will fill.

Counted two ways, because they answer different questions:

  BY TOKEN, which says how much of a page a reader gets through.
  BY TYPE,  which says how much of the vocabulary is reached at all, and is
            always the harsher of the two.

The Tabeli is reported apart from the rest, and it is the number that matters:
it is the only ORDINARY PROSE of the three. The Dicionario's definitions and
the Gramatiko's paragraphs are both metalinguistic, and both cite forms that
the language does not otherwise use.

Run: python3 tools/translator/coverage.py
"""

import collections
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import corpus  # noqa: E402
import ido     # noqa: E402


def main():
    docs = corpus.ido_documents()
    if not docs:
        sys.exit('The three books are not beside this repository; see CLAUDE.md.')
    a = ido.Analyser()
    print('lexicon: %d roots, %d suffixes, %d prefixes'
          % (len(a.roots), len(a.suffixes), len(a.prefixes)))

    tok_hit = collections.Counter()
    tok_all = collections.Counter()
    types = collections.defaultdict(collections.Counter)
    cache = {}
    misses = collections.Counter()

    for tag, d in docs:
        for w in d:
            if w not in cache:
                cache[w] = bool(a.analyse(w))
            tok_all[tag] += 1
            types[tag][w] += 1
            if cache[w]:
                tok_hit[tag] += 1
            else:
                misses[w] += 1

    print()
    print('%-12s %>9s %8s   %9s %8s'.replace('>', '')
          % ('book', 'tokens', 'covered', 'types', 'covered'))
    for tag in ('tabeli', 'dicionario', 'gramatiko'):
        ts = types[tag]
        th = sum(1 for w in ts if cache[w])
        print('%-12s %9d %7.1f%%   %9d %7.1f%%'
              % (tag, tok_all[tag], 100 * tok_hit[tag] / max(1, tok_all[tag]),
                 len(ts), 100 * th / max(1, len(ts))))
    allt = sum(tok_all.values())
    allh = sum(tok_hit.values())
    alltypes = set(cache)
    print('%-12s %9d %7.1f%%   %9d %7.1f%%'
          % ('ALL', allt, 100 * allh / allt, len(alltypes),
             100 * sum(1 for w in alltypes if cache[w]) / len(alltypes)))

    # ---- WHAT IS LEFT, SORTED INTO WHAT IT ACTUALLY IS ------------------
    # A raw miss list flatters nobody and informs nobody: most of what the
    # analyser cannot parse is not Ido. The Gramatiko quotes bare endings as
    # text (`la finalo -n`), and the Dicionario prints its subject fields
    # abbreviated (`metaf.`, `geom.`). Both fall into the token stream and
    # neither is a word the language uses. They are separated here so that
    # the number left over is the one that means something: VOCABULARY THE
    # TWO BOOKS TOGETHER DO NOT REACH.
    import json
    abbrev = set()
    fp = corpus.DICIONARIO / 'faki.json'
    if fp.exists():
        for k in (json.loads(fp.read_text(encoding='utf-8')).get('faki') or {}):
            abbrev.add(k.strip('*.-').lower().split()[0] if k.strip() else '')
    affix = set(a.suffixes) | set(a.prefixes) | {e for e, _, _ in ido.FINAL}

    kinds = collections.Counter()
    bucket = collections.defaultdict(collections.Counter)
    for w, n in misses.items():
        if len(w) <= 2 or w in affix:
            k = 'a fragment the Gramatiko quotes (an ending, an affix)'
        elif w in abbrev:
            k = "the Dicionario's own abbreviated subject field"
        else:
            k = 'VOCABULARY THE BOOKS DO NOT REACH'
        kinds[k] += n
        bucket[k][w] += n

    print()
    print('WHAT IS NOT REACHED, sorted into what it is')
    print('(%d tokens in all, %.1f%% of the corpus)'
          % (sum(misses.values()), 100 * sum(misses.values()) / allt))
    for k, n in kinds.most_common():
        print('\n  %-52s %6d  %4.1f%%' % (k, n, 100 * n / allt))
        print('    ' + ', '.join(w for w, _ in bucket[k].most_common(14)))

    real = kinds['VOCABULARY THE BOOKS DO NOT REACH']
    print()
    print('SO THE HONEST FIGURE IS THIS: %.1f%% of the site\'s Ido is real'
          % (100 * real / allt))
    print('vocabulary the two books together cannot account for. The rest of')
    print('the miss is the books talking about the language rather than in it.')

    # How much of the work the affixes are doing: a token covered only
    # BECAUSE an affix was stripped is one the Dicionario alone would miss.
    bare = plain = 0
    for w, n in ((w, sum(types[t][w] for t in types)) for w in alltypes):
        if not cache[w]:
            continue
        p = a.analyse(w)[0]
        if p.prefixes or p.suffixes:
            bare += n
        else:
            plain += n
    print()
    print('of the covered tokens, %d (%.1f%%) needed an affix stripped:'
          % (bare, 100 * bare / max(1, bare + plain)))
    print('THE DICIONARIO ALONE WOULD MISS THOSE. The affix chapters are not')
    print('an ornament on the dictionary; they are part of its lexicon.')


if __name__ == '__main__':
    main()
