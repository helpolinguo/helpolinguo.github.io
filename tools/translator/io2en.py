"""IDO -> ENGLISH, WHICH IS THE DIRECTION THAT WORKS.

THE ASYMMETRY IS THE WHOLE FINDING. Going English -> Ido you must CHOOSE a
word, and choosing needs a lexicon: the site has 1,897 attested pairs covering
12.3 % of the Dicionario's roots, and `evaluate.py` measures what that ceiling
does to a translator. Going Ido -> English you need only RECOGNISE one, and
recognition has three sources here where choice had one:

  the glossary   1,897 pairs, attested, from a printed parallel text
  the cognate    3,700-odd roots the Dicionario marks as attested in English,
                 recovered by `cognates.py` -- INDUCED, NOT THE BOOK'S ANSWER
  the definition the Dicionario defines every one of its 9,473 roots in Ido,
                 and with the two above most of that Ido is now legible

So an unknown word is not a dead end in this direction: it has an article, and
the article can be read. That is why this file produces something for text the
other direction cannot touch.

WHAT IT DOES NOT DO. It does not claim the cognate is a translation. A word
glossed from a cognate is marked `~`, and a word glossed from its definition
is given AS a definition, in braces. `llms.txt` is explicit that the English
cognate of a headword is not the book's answer, and this keeps the two apart
on the page instead of blending them into a confident-looking sentence.
"""

import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cognates   # noqa: E402
import corpus     # noqa: E402
import ido        # noqa: E402
import translate  # noqa: E402

# The function words, taken back the other way from translate.FUNCTION.
IO2EN_FUNCTION = {}
for _en, _io in translate.FUNCTION.items():
    if _io:
        IO2EN_FUNCTION.setdefault(_io, _en)
IO2EN_FUNCTION.update({
    'la': 'the', 'esas': 'is', 'esis': 'was', 'esos': 'will be',
    'esar': 'to be', 'e': 'and', 'ed': 'and', 'di': 'of', 'da': 'by',
    'de': 'from', 'en': 'in', 'sur': 'on', 'kun': 'with', 'ne': 'not',
    'ica': 'this', 'ici': 'these', 'ita': 'that', 'qua': 'which',
    'quo': 'what', 'qui': 'who', 'ube': 'where', 'kande': 'when',
    'omna': 'every', 'ula': 'some', 'nula': 'no', 'anke': 'also',
    'nur': 'only', 'tre': 'very', 'plu': 'more', 'min': 'less',
    'me': 'I', 'tu': 'you', 'vu': 'you', 'il': 'he', 'el': 'she',
    'ol': 'it', 'ni': 'we', 'vi': 'you', 'ili': 'they', 'onu': 'one',
    'lua': 'his', 'elua': 'her', 'mea': 'my', 'nia': 'our', 'vua': 'your',
    'sua': 'their own', 'lia': 'their',
})


def english_plural(w):
    if re.search(r'(s|x|z|ch|sh)$', w):
        return w + 'es'
    if re.search(r'[^aeiou]y$', w):
        return w[:-1] + 'ies'
    return w + 's'


def english_past(w):
    if w.endswith('e'):
        return w + 'd'
    if re.search(r'[^aeiou]y$', w):
        return w[:-1] + 'ied'
    return w + 'ed'


class Reader:
    """Renders Ido into English, and says where each word came from."""

    def __init__(self, english=None, keys=None, use_cognates=True,
                 use_definitions=False):
        # DEFINITIONS DEFAULT OFF, AND THE NUMBER IS WHY. Reading an unknown
        # word out of its own article glosses 93.5 % of tokens instead of
        # 76.7 %, and takes precision from 20.8 % to 4.9 % -- F1 halves, from
        # 17.9 % to 7.6 %. The extra 17 points of coverage are noise wearing a
        # sentence's clothes: `mezo` comes out `{part which dictate dee
        # horsemen extreme}`. Kept, because a measured negative belongs in the
        # record, but not switched on.
        self.an = ido.Analyser()
        self.glossary = {}
        for i, e, ks in corpus.glosaro('en-GB'):
            if keys is not None and not (set(ks) & keys):
                continue
            p = self.an.analyse(i.lower().split()[0])
            if p:
                self.glossary.setdefault(p[0].root, e.lower())
        self.cog = None
        if use_cognates and english:
            self.cog = cognates.Cognates(english, analyser=self.an)
        self.defs = {}
        if use_definitions:
            for r in corpus.dicionario():
                p = self.an.analyse(r['v'].lower())
                if not p:
                    continue
                senses = [s.get('t') or '' for s in (r.get('b') or [])]
                if senses:
                    self.defs.setdefault(p[0].root, senses[0])

    # -- one root ----------------------------------------------------------
    def root_gloss(self, root, depth=0):
        """(english, source). Source is 'glossary', 'cognate' or 'definition'."""
        if root in self.glossary:
            return self.glossary[root], 'glossary'
        if self.cog and self.cog.get(root):
            return self.cog.get(root), 'cognate'
        if depth == 0 and root in self.defs:
            # Read the article instead. Bounded to one level: a definition
            # glossed out of definitions of definitions stops being evidence.
            words = []
            for t in corpus.tokens(self.defs[root]):
                p = self.an.analyse(t)
                if p:
                    g = self.root_gloss(p[0].root, depth + 1)
                    if g:
                        words.append(g[0])
                        continue
                if t in IO2EN_FUNCTION:
                    words.append(IO2EN_FUNCTION[t])
            if len(words) >= 2:
                return ' '.join(words), 'definition'
        return None

    # -- one word ----------------------------------------------------------
    def word(self, tok):
        low = tok.lower()
        if low in IO2EN_FUNCTION:
            return {'io': tok, 'en': IO2EN_FUNCTION[low], 'source': 'function'}
        parses = self.an.analyse(low)
        if not parses:
            return {'io': tok, 'en': None, 'source': 'unparsed'}
        p = parses[0]
        got = self.root_gloss(p.root)
        if not got:
            return {'io': tok, 'en': None, 'source': 'no gloss'}
        en, src = got
        if src != 'definition' and ' ' not in en:
            if p.features.get('number') == 'plural':
                en = english_plural(en)
            elif p.features.get('tense') == 'past':
                en = english_past(en)
            elif p.features.get('tense') == 'future':
                en = 'will ' + en
        return {'io': tok, 'en': en, 'source': src, 'parse': p}

    def read(self, text):
        out = []
        for m in re.finditer(r"[A-Za-zÀ-ÿ'-]+", text):
            tok = m.group(0)
            # A HYPHEN IN THIS BOOK JOINS TWO ROOTS -- `vest-hoki`,
            # `ludo-korto`, `klok-tabeli`. Glossed whole they never match
            # anything; glossed apart, both halves are ordinary words.
            if '-' in tok.strip('-') and not self.an.analyse(tok.lower()):
                parts = [p for p in tok.split('-') if p]
                got = [self.word(p) for p in parts]
                if any(g['en'] for g in got):
                    out.extend(got)
                    continue
            out.append(self.word(tok))
        return out


def render(rows):
    """A line a person can read, with the induced parts MARKED as induced."""
    out = []
    for r in rows:
        if r['en'] is None:
            out.append('[%s?]' % r['io'])
        elif r['source'] == 'cognate':
            out.append('~' + r['en'])
        elif r['source'] == 'definition':
            out.append('{%s}' % r['en'])
        else:
            out.append(r['en'])
    return ' '.join(out)


def _english():
    p = Path(os.environ.get('IDO_GLOVE', Path.home() / 'glove100.kv'))
    if not p.exists():
        return None
    from gensim.models import KeyedVectors
    return list(KeyedVectors.load(str(p)).index_to_key)


if __name__ == '__main__':
    en = _english()
    if not en:
        print('No English word list; set IDO_GLOVE. Running without cognates.')
    r = Reader(english=en)
    print('glossary roots %d   cognate roots %d   articles %d\n'
          % (len(r.glossary), len(r.cog) if r.cog else 0, len(r.defs)))
    tab = corpus.tabeli()
    eng = corpus.teksti('en-GB')
    for k in list(tab)[8:13]:
        rows = r.read(tab[k]['io'])
        print('IO  %s' % tab[k]['io'][:150])
        print('->  %s' % render(rows)[:200])
        print('EN  %s' % (eng.get(k, '')[:150]))
        print()
