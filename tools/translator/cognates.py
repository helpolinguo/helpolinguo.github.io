"""THE DICIONARIO SAYS WHICH ROOTS HAVE AN ENGLISH COGNATE, AND THAT IS A BRIDGE.

Every article carries the languages the root is ATTESTED in -- `Germana,
Angla, Franca, Italiana, Rusa, Hispana`, the `DEFIRS` the book prints. 7,165
of the 9,473 roots are marked `Angla`: the root was admitted into Ido partly
BECAUSE English has a cognate of it.

`llms.txt` warns, correctly, that this is not a translation: "An answer built
from the English cognate of a headword is not this book's answer, and for most
words it is not the same answer." MEASURED HERE, AND THE WARNING HOLDS: against
the Tabeli's gold pairs the recovered cognate is the glossary's own word only
28.6 % of the time. `kupo` recovers *cup* where the book prints *bowl*,
`pastoro` recovers *pastor* where it prints *herdsman*, `ursino` recovers
*ursine* where it prints *bear*. The cognate is right AS A COGNATE and wrong
as a gloss.

SO IT IS NOT USED AS A TRANSLATION. It is used for the one thing it is
reliable at: making the Dicionario's own Ido definitions legible. That lifts
the share of definition tokens that can be rendered in English from 16.7 % to
76.3 %, and that is what `io2en.py` reads.

THE MARK IS A REAL SIGNAL AND NOT A GUESS: recovery scores 28.6 % precision on
roots marked `Angla` against 7.0 % on roots not marked. Four times better, so
the gate is kept.
"""

import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import corpus  # noqa: E402
import ido     # noqa: E402


def _fold(w):
    w = unicodedata.normalize('NFD', w.lower())
    w = ''.join(c for c in w if not unicodedata.combining(c))
    w = re.sub(r'[^a-z]', '', w)
    return (w.replace('ph', 'f').replace('qu', 'kw').replace('x', 'ks')
             .replace('ck', 'k').replace('gh', '').replace('th', 't'))


def _tail(w):
    w = (w.replace('z', 's').replace('y', 'i')
          .replace('w', 'v').replace('j', 'i'))
    w = re.sub(r'(.)\1+', r'\1', w)          # English doubles, Ido has none
    return re.sub(r'e$', '', w)              # English's silent final -e


def skeleton_ido(word):
    """An Ido spelling, folded onto the comparison alphabet.

    IDO'S `c` IS ALWAYS /ts/ -- there is no hard-c reading of it -- so it
    folds to `s` unconditionally. Getting this wrong is what made `substanco`
    and `edifico` fail to find *substance* and *edifice*: folded with
    English's rule, the `c` before `o` became `k` and no English word matched.
    """
    w = _fold(word)
    w = re.sub(r'[tcs]i(?=[aou])', 's', w)   # -ciono = -tion
    return _tail(w.replace('c', 's'))


def skeletons_english(word):
    """Every folding an English spelling could answer to.

    English `c` is /k/ or /s/ and the spelling does not always say which, so
    both readings are indexed rather than one being guessed. Bounded to four
    `c`s, beyond which the word is not going to be an Ido root anyway.
    """
    w = _fold(word)
    w = re.sub(r'[tcs]i(?=[aou])', 's', w)
    n = w.count('c')
    if n > 4:
        return {_tail(re.sub(r'c(?=[eiy])', 's', w).replace('c', 'k'))}
    out = {w}
    for _ in range(n):
        nxt = set()
        for v in out:
            if 'c' in v:
                nxt.add(v.replace('c', 's', 1))
                nxt.add(v.replace('c', 'k', 1))
            else:
                nxt.add(v)
        out = nxt
    return {_tail(v) for v in out}


class Cognates:
    """Ido root -> the English word it is cognate with, where one is found.

    `english` is a vocabulary in frequency order -- GloVe's key list serves,
    and any frequency-ordered word list would. Frequency breaks ties: several
    English words can share a skeleton (`doors` and `dorsal` both answer
    `dorso`), and the commonest is the likeliest to be the inherited one.
    """

    def __init__(self, english, analyser=None, gate='Angla', limit=40000):
        # THE VOCABULARY IS CAPPED, AND PRECISION IS WHY. GloVe's tail is
        # mostly not English -- scanning the top 150,000 rather than the top
        # 40,000 took precision from 39.9 % to 33.5 % and bought no recall at
        # all, because the extra matches were tokens like `nacion` and `urs`
        # standing in front of `national` and `ursine`.
        english = [w for w in english[:limit] if w.isalpha() and len(w) > 2]
        self.rank = {w: i for i, w in enumerate(english)}
        self.exact = defaultdict(list)
        self.by_head = defaultdict(list)
        for w in english:
            for s in skeletons_english(w):
                self.exact[s].append(w)
                if len(s) >= 4:
                    self.by_head[s[:4]].append((s, w))
        self.an = analyser or ido.Analyser()
        self.gate = gate
        self.lexicon = {}
        self.gated_out = 0
        self._build()

    def _match(self, stem):
        """The likeliest English cognate of an Ido stem, or None.

        Exact first; failing that, an English word whose skeleton EXTENDS the
        Ido one by at most three letters, which is how `aparat` reaches
        *apparatus* and `karnavor` reaches *carnivorous*. Ranked by how little
        was added, then by frequency.
        """
        s = skeleton_ido(stem)
        if s in self.exact:
            return min(self.exact[s], key=lambda w: self.rank[w])
        best = None
        for es, w in self.by_head.get(s[:4], ()):
            if es.startswith(s) and 0 < len(es) - len(s) <= 3:
                key = (len(es) - len(s), self.rank[w])
                if best is None or key < best[0]:
                    best = (key, w)
        return best[1] if best else None

    def _build(self):
        for r in corpus.dicionario():
            head = r['v'].lower()
            if self.gate and self.gate not in (r.get('n') or []):
                self.gated_out += 1
                continue
            p = self.an.analyse(head)
            if not p:
                continue
            p = p[0]
            if p.root in self.lexicon:
                continue
            hit = self._match(''.join(p.prefixes) + p.root + ''.join(p.suffixes))
            if hit:
                self.lexicon[p.root] = hit

    def get(self, root):
        return self.lexicon.get(root)

    def __len__(self):
        return len(self.lexicon)


if __name__ == '__main__':
    from gensim.models import KeyedVectors
    import os
    kv = KeyedVectors.load(os.environ.get(
        'IDO_GLOVE', str(Path.home() / 'glove100.kv')))
    en = [w for w in kv.index_to_key if w.isalpha() and len(w) > 2]
    c = Cognates(en)
    print('English skeletons indexed: %d' % len(c.exact))
    print('roots marked %s and recovered: %d' % (c.gate, len(c)))
    for w in ('propoziciono', 'nacionala', 'mamifero', 'karnavora', 'aparato',
              'substanco', 'kupo', 'dorso', 'ursino'):
        p = c.an.analyse(w)
        r = p[0].root if p else w
        print('  %-14s -> %s' % (w, c.get(r) or '--'))
