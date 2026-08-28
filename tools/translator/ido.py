"""IDO'S MORPHOLOGY, AS RULES. Analysis and generation, both exact.

WHY THIS IS NOT LEARNED. Ido's endings are unambiguous and exceptionless: a
word ending in `-o` is a noun, in `-a` an adjective, in `-e` an adverb, in
`-as` a present-tense verb. There is no irregular verb, no gender, no
declension, no stem change. A rule table therefore does not APPROXIMATE the
morphology -- it IS the morphology, and a statistical model trained on 251,467
tokens could at best rediscover part of it. That is why nothing below is
trained.

THE DIVISION OF LABOUR THE BOOKS ALREADY MAKE. The Dicionario carries roots --
9,473 of them, and it says so: `kovrilo`, `dometo`, `hundino` are not
headwords. The Gramatiko carries the 65 affixes that build the rest. So an
analyser that strips endings and affixes down to a root, and a generator that
puts them back, is the join the two books were printed to make.

WHAT IS DELIBERATELY NOT HERE. The accusative `-n` is stripped on analysis but
never generated: the Gramatiko makes it obligatory only where the word order
departs from subject-verb-object, and `temi/akuzativo.md` is 47 blocks on
when that is. Guessing it wrong is worse than leaving it off, which is
always grammatical in the plain order.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import corpus  # noqa: E402

# ---------------------------------------------------------------- the endings
# Longest first: `-as` must be tried before `-a`, or every verb becomes an
# adjective. The tuple is (ending, part of speech, features).

FINAL = [
    ('ar', 'verb', {'tense': 'infinitive'}),
    ('ir', 'verb', {'tense': 'infinitive-past'}),
    ('or', 'verb', {'tense': 'infinitive-future'}),
    ('as', 'verb', {'tense': 'present'}),
    ('is', 'verb', {'tense': 'past'}),
    ('os', 'verb', {'tense': 'future'}),
    ('us', 'verb', {'mood': 'conditional'}),
    ('ez', 'verb', {'mood': 'imperative'}),
    ('i',  'noun', {'number': 'plural'}),
    ('o',  'noun', {'number': 'singular'}),
    ('a',  'adjective', {}),
    ('e',  'adverb', {}),
]

# The participles, which take a nominal, adjectival or adverbial ending of
# their own: `skrib-ant-a`, `skrib-ant-o`, `skrib-int-e`.
PARTICIPLE = [
    ('ant', {'voice': 'active', 'time': 'present'}),
    ('int', {'voice': 'active', 'time': 'past'}),
    ('ont', {'voice': 'active', 'time': 'future'}),
    ('at',  {'voice': 'passive', 'time': 'present'}),
    ('it',  {'voice': 'passive', 'time': 'past'}),
    ('ot',  {'voice': 'passive', 'time': 'future'}),
]

# The closed classes. These are WORDS, not roots: no ending is stripped from
# them and none of them is a Dicionario headword, because the Dicionario is a
# dictionary of roots and these belong to the grammar. Taken from the
# Gramatiko's chapters on the pronoun, the article, the correlative, the
# numeral, the preposition and the conjunction.
#
# MEASURED, AND THIS IS WHY THE LIST IS HERE: without it the analyser misses
# `dil` 557 times, `ulu` 523 and `mea` 235 over the site's Ido -- all of them
# ordinary words, none of them findable in a book of roots.

PRONOUNS = {
    'me', 'tu', 'vu', 'il', 'ilu', 'el', 'elu', 'ol', 'olu', 'lu',
    'ni', 'vi', 'ili', 'eli', 'oli', 'li', 'su', 'onu', 'on', 'lo',
}

# Pronoun + `-a` is the possessive, and it is regular over the whole set.
POSSESSIVES = {
    'mea', 'tua', 'vua', 'ilua', 'elua', 'olua', 'lua', 'nia', 'via',
    'ilia', 'elia', 'olia', 'lia', 'sua', 'onua',
}

# The correlatives. A closed table in the Gramatiko, and closed here: the
# stems overlap real roots (`sam-`, `tal-`, `ul-`), so generating them by rule
# would invent words the book does not print.
CORRELATIVES = {
    'qua', 'quo', 'qui', 'quan', 'quon', 'quin', 'quala', 'quanta', 'quante',
    'ta', 'to', 'ti', 'tan', 'ton', 'ita', 'ito', 'iti', 'ica', 'ico', 'ici',
    'ca', 'co', 'ci', 'olta', 'olto', 'olti', 'olca', 'olco', 'olci',
    'ula', 'ulo', 'ulu', 'uli', 'nula', 'nulo', 'nulu', 'nuli',
    'irga', 'irgo', 'irgu', 'irgi', 'omna', 'omno', 'omnu', 'omni',
    'altra', 'altro', 'altru', 'altri', 'sama', 'samo', 'singla', 'singlu',
    'tala', 'tanta', 'tante', 'ilca', 'ilta',
    'kande', 'lore', 'ube', 'ibe', 'hike', 'ulloke', 'nulloke',
    'quale', 'tale', 'kad', 'ka',
}

# The article elides against four prepositions, and the elision is written.
# Each is one word in the text and two in the grammar.
ELISIONS = {
    'al': ('a', 'la'), 'dal': ('da', 'la'), 'del': ('de', 'la'),
    'dil': ('di', 'la'), 'l': ('la', None),
}

PARTICLES = {
    'la', 'e', 'ed', 'o', 'od', 'ma', 'nam', 'do', 'or', 'ke', 'se',
    'ne', 'nul', 'ya', 'yes', 'no', 'anke', 'nur', 'ja', 'ankore', 'ankor',
    'di', 'da', 'de', 'a', 'ad', 'en', 'sur', 'sub', 'kun', 'sen', 'per',
    'por', 'pri', 'pro', 'ek', 'til', 'ye', 'che', 'inter', 'kontre',
    'ultre', 'malgre', 'segun', 'vice', 'dum', 'pos', 'ante', 'cirkum',
    'aden', 'adsur', 'apud', 'avan', 'dop', 'exter', 'super', 'trans', 'tra',
    'kam', 'quik', 'olim', 'nun', 'hiere', 'hodie', 'morge', 'sempre',
    'nultempe', 'plu', 'min', 'tam', 'tre', 'tro', 'plus', 'pluse', 'pose',
    'ex', 'ipsa', 'mem', 'preske', 'apene', 'quaze', 'forsan', 'certe',
    'un', 'du', 'tri', 'quar', 'kin', 'sis', 'sep', 'ok', 'non', 'dek',
    'cent', 'mil', 'milion', 'miliardo', 'zero',
}

# The numeral suffixes. THE GRAMATIKO PUTS THESE IN ITS NUMERAL CHAPTER AND
# NOT AMONG THE 65 AFFIXES, so `afixi/` does not carry them and the analyser
# would miss `unesma` (185 times) and `duesma` (129) without them.
NUMERAL_SUFFIXES = ['esm', 'opl', 'im', 'on']

# The numerals are not headwords either -- `du` is not in the Dicionario --
# so they are stems here, and `duesma` and `duopla` are built on them.
NUMERAL_STEMS = {
    'un', 'du', 'tri', 'quar', 'kin', 'sis', 'sep', 'ok', 'non', 'dek',
    'cent', 'mil', 'milion', 'miliard', 'zer',
}

# A PREPOSITION MAY BE USED AS A PREFIX, and the Gramatiko says so in its
# chapter on composition: `de-prenar`, `ad-juntar`, `sur-metar`. These are not
# among the 65 affixes, because they are not affixes -- they are prepositions
# doing a second job.
PREPOSITION_PREFIXES = [
    'kontre', 'cirkum', 'super', 'trans', 'inter', 'avan', 'apud', 'exter',
    'aden', 'sur', 'sub', 'kun', 'sen', 'per', 'por', 'pri', 'pro', 'ante',
    'pos', 'dop', 'tra', 'ek', 'en', 'ad', 'de', 'da', 'di', 'a',
]

# ------------------------------------------------------------- the 65 affixes
# Read from `gramatiko/afixi/`, so the inventory is the book's and not a copy
# kept here that could drift from it.


def affixes():
    """(suffixes, prefixes), each a list of bare forms, longest first.

    The file names carry the hyphens the book prints -- `-il-`, `des-`,
    `mono-` -- and the hyphens say which side the affix attaches on.
    """
    suf, pre = [], []
    for name in corpus.afixi():
        bare = name.strip('-')
        if not bare:
            continue
        if name.startswith('-'):
            suf.append(bare)
        else:
            pre.append(bare)
    suf += NUMERAL_SUFFIXES
    pre += PREPOSITION_PREFIXES
    return (sorted(set(suf), key=len, reverse=True),
            sorted(set(pre), key=len, reverse=True))


# ------------------------------------------------------------------ the roots

def roots():
    """Bare stems of the Dicionario's headwords -> the headwords themselves.

    `hundo` gives `hund`, `skribar` gives `skrib`, `bona` gives `bon`. A
    headword that is not inflected at all -- `la`, `amen`, `a posteriori` --
    is kept whole and marked so.
    """
    out = {}
    for r in corpus.dicionario():
        h = r['v']
        clean = h.strip('*').strip('«»').replace('(', '').replace(')', '')
        clean = clean.strip('!').strip()
        if not clean or ' ' in clean:
            continue
        low = clean.lower()
        if low.startswith('-') or low.endswith('-'):
            continue                       # an affix, handled above
        stem, pos = None, None
        for end, p, _ in FINAL:
            if low.endswith(end) and len(low) > len(end):
                stem, pos = low[:-len(end)], p
                break
        if stem:
            out.setdefault(stem, []).append((h, pos))
        else:
            out.setdefault(low, []).append((h, 'invariable'))
    for n in NUMERAL_STEMS:
        out.setdefault(n, []).append((n, 'numeral'))
    return out


# ------------------------------------------------------------------ analysis

class Parse:
    __slots__ = ('root', 'headword', 'pos', 'features', 'prefixes',
                 'suffixes', 'accusative')

    def __init__(self, root, headword, pos, features, prefixes, suffixes,
                 accusative):
        self.root, self.headword, self.pos = root, headword, pos
        self.features, self.prefixes = features, prefixes
        self.suffixes, self.accusative = suffixes, accusative

    def __repr__(self):
        bits = [self.headword or self.root, self.pos]
        if self.prefixes:
            bits.append('pre=' + '+'.join(self.prefixes))
        if self.suffixes:
            bits.append('suf=' + '+'.join(self.suffixes))
        if self.accusative:
            bits.append('acc')
        f = ','.join('%s=%s' % kv for kv in sorted(self.features.items()))
        if f:
            bits.append(f)
        return '<%s>' % ' '.join(bits)

    CLOSED = ('elision', 'possessive', 'correlative', 'pronoun',
              'particle', 'invariable')

    def cost(self):
        """Fewer pieces is a better parse; a closed-class word beats any
        decomposition, because the closed classes are exhaustive lists and
        a decomposition of one of them is always an accident."""
        if self.pos in Parse.CLOSED:
            return -1
        return len(self.prefixes) + len(self.suffixes) + self.accusative


class Analyser:
    def __init__(self):
        self.roots = roots()
        self.suffixes, self.prefixes = affixes()
        self._affixset = set(self.suffixes) | set(self.prefixes)

    # -- one step: take the grammatical ending off ---------------------------
    def _endings(self, word):
        """Yield (stem, pos, features, accusative) for every reading."""
        for acc in ((False, True) if len(word) > 2 and word.endswith('n')
                    else (False,)):
            w = word[:-1] if acc else word
            for end, pos, feat in FINAL:
                if not (w.endswith(end) and len(w) > len(end)):
                    continue
                body = w[:-len(end)]
                # A participle sits between the root and the ending.
                for pmark, pfeat in PARTICIPLE:
                    if body.endswith(pmark) and len(body) > len(pmark):
                        f = dict(feat)
                        f.update(pfeat)
                        f['participle'] = True
                        yield body[:-len(pmark)], pos, f, acc
                yield body, pos, feat, acc

    # -- the affixes, peeled off until a root is reached ---------------------
    def _compound(self, stem):
        """Two roots welded together -- `ter` + `globo`, `skrib` + `mashino`.

        The Gramatiko's chapter on composition allows it and the Dicionario
        does not list the results, so without this `terglobo` (36 times) has
        no parse. BOUNDED TO TWO ROOTS AND TO PARTS OF THREE LETTERS OR MORE:
        unbounded, a 9,269-root lexicon will cut any string into something,
        and the parses stop meaning anything.
        """
        for i in range(3, len(stem) - 2):
            head, tail = stem[:i], stem[i:]
            if tail in self.roots and head in self.roots:
                yield head, tail

    def _peel(self, stem, pres, sufs, depth=0):
        """Yield (root, prefixes, suffixes) for every way `stem` decomposes.

        Bounded at four affixes: the Gramatiko's own longest examples stack
        three (`des-bel-eg-a`), and an unbounded search on a 9,473-root
        lexicon invents decompositions nobody wrote.
        """
        if stem in self.roots:
            yield stem, list(pres), list(sufs)
        if depth >= 4:
            return
        for s in self.suffixes:
            if stem.endswith(s) and len(stem) > len(s) + 1:
                yield from self._peel(stem[:-len(s)], pres, [s] + sufs,
                                      depth + 1)
        for p in self.prefixes:
            if stem.startswith(p) and len(stem) > len(p) + 1:
                yield from self._peel(stem[len(p):], pres + [p], sufs,
                                      depth + 1)

    def analyse(self, word):
        """Every reading of `word`, best (fewest pieces) first.

        The closed classes are tried before the roots, because several of them
        would otherwise get a spurious root parse: `mea` decomposes as a
        headword plus an ending if you let it, and it is a possessive.
        """
        w = word.lower().strip()
        out = []
        if w in ELISIONS:
            a, b = ELISIONS[w]
            out.append(Parse(w, w, 'elision', {'esas': (a, b)}, [], [], False))
        if w in POSSESSIVES:
            out.append(Parse(w, w, 'possessive', {}, [], [], False))
        if w in CORRELATIVES:
            out.append(Parse(w, w, 'correlative', {}, [], [], False))
        if w in PRONOUNS:
            out.append(Parse(w, w, 'pronoun', {}, [], [], False))
        if w in PARTICLES:
            out.append(Parse(w, w, 'particle', {}, [], [], False))
        if w in self.roots and any(p == 'invariable'
                                   for _, p in self.roots[w]):
            out.append(Parse(w, self.roots[w][0][0], 'invariable', {}, [], [],
                             False))
        for stem, pos, feat, acc in self._endings(w):
            # AN AFFIX MAY STAND AS A WORD OF ITS OWN. The Gramatiko is
            # explicit about it -- `igar`, `ajo`, `eso`, `ero` are the affix
            # used bare -- and it costs 345 misses on `igar` alone to ignore.
            if stem in self._affixset:
                out.append(Parse(stem, '-%s-' % stem, pos, feat, [], [], acc))
            got = False
            for root, pres, sufs in self._peel(stem, [], []):
                head = self.roots[root][0][0]
                out.append(Parse(root, head, pos, feat, pres, sufs, acc))
                got = True
            if not got:
                for a_, b_ in self._compound(stem):
                    out.append(Parse(b_, '%s+%s' % (
                        self.roots[a_][0][0], self.roots[b_][0][0]),
                        pos, feat, [a_], sufs if False else [], acc))
        seen, uniq = set(), []
        for p in sorted(out, key=Parse.cost):
            k = (p.root, p.pos, tuple(p.prefixes), tuple(p.suffixes),
                 tuple(sorted(p.features.items())), p.accusative)
            if k not in seen:
                seen.add(k)
                uniq.append(p)
        return uniq


# ---------------------------------------------------------------- generation

def generate(root, pos, number='singular', tense='present', mood=None,
             suffixes=(), prefixes=()):
    """Root plus affixes plus one ending. Exact, because the endings are.

    `root` is the bare stem -- `hund`, not `hundo`. The caller gets what the
    Gramatiko says it should get and nothing is guessed.
    """
    stem = ''.join(prefixes) + root + ''.join(suffixes)
    if pos == 'noun':
        return stem + ('i' if number == 'plural' else 'o')
    if pos == 'adjective':
        return stem + 'a'
    if pos == 'adverb':
        return stem + 'e'
    if pos == 'verb':
        if mood == 'imperative':
            return stem + 'ez'
        if mood == 'conditional':
            return stem + 'us'
        return stem + {'infinitive': 'ar', 'present': 'as', 'past': 'is',
                       'future': 'os'}.get(tense, 'as')
    return stem


def participle(root, time='present', voice='active', pos='adjective'):
    mark = {('present', 'active'): 'ant', ('past', 'active'): 'int',
            ('future', 'active'): 'ont', ('present', 'passive'): 'at',
            ('past', 'passive'): 'it', ('future', 'passive'): 'ot'}[
                (time, voice)]
    return root + mark + {'adjective': 'a', 'noun': 'o', 'adverb': 'e'}[pos]


if __name__ == '__main__':
    a = Analyser()
    print('roots %d   suffixes %d   prefixes %d'
          % (len(a.roots), len(a.suffixes), len(a.prefixes)))
    for w in ('hundo', 'hundini', 'kovrilo', 'dometo', 'skribilo',
              'desbeleg a'.replace(' ', ''), 'nekredebla', 'skribanta',
              'skribita', 'la', 'domon', 'reskribar'):
        print('%-14s %s' % (w, a.analyse(w)[:3] or 'NO PARSE'))
    print()
    print('generate:', generate('hund', 'noun', number='plural'),
          generate('skrib', 'verb', tense='past'),
          generate('dom', 'noun', suffixes=['et']),
          participle('skrib', 'past', 'passive'))
