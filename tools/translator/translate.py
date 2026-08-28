"""ENGLISH -> IDO, BUILT OUT OF THE THREE BOOKS AND NOTHING ELSE.

WHAT THIS IS. A transfer translator with three stages, each taking its data
from the book that holds it:

    the word     Tabeli     the glossary's 1,897 attested en-GB <-> Ido pairs
    the form     Gramatiko  the endings and the 65 affixes, applied as rules
    the frame    Dicionario whether the verb takes an object, and which
                            preposition it governs

WHAT IT IS NOT. It is not a model, and it does not generalise: it has the
vocabulary the glossary has, which is 1,897 pairs of ONE REGISTER -- a
schoolroom, a house, trades, games. An abstract word is not in it and will be
reported missing rather than guessed at. THIS IS THE REAL CEILING OF THE
WHOLE IDEA, and `evaluate.py` measures where it stands.

WHY MISSING IS PRINTED AND NOT FILLED. The site's own instruction to a machine
is that a word absent from the Dicionario is an answer, and that an English
cognate is not a substitute for the book's reading. A translator that quietly
invents `*abstrakteso` because English has *abstractness* would be doing the
thing `llms.txt` spends a section forbidding.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import corpus  # noqa: E402
import ido     # noqa: E402

WORD = re.compile(r"[A-Za-z][A-Za-z'-]*")

# English function words. They are translated from a table because they are a
# closed class in both languages, and because the glossary -- lifted from the
# bold terms of a picture book -- contains almost none of them.
FUNCTION = {
    'the': 'la', 'a': None, 'an': None,
    'and': 'e', 'or': 'o', 'but': 'ma', 'because': 'nam', 'that': 'ke',
    'if': 'se', 'not': 'ne', 'also': 'anke', 'only': 'nur', 'already': 'ja',
    'of': 'di', 'by': 'da', 'from': 'de', 'to': 'a', 'in': 'en', 'on': 'sur',
    'under': 'sub', 'with': 'kun', 'without': 'sen', 'through': 'tra',
    'for': 'por', 'about': 'pri', 'between': 'inter', 'against': 'kontre',
    'during': 'dum', 'after': 'pos', 'before': 'ante', 'out': 'ek',
    'i': 'me', 'you': 'vu', 'he': 'il', 'she': 'el', 'it': 'ol',
    'we': 'ni', 'they': 'li', 'me': 'me', 'him': 'il', 'her': 'el',
    'us': 'ni', 'them': 'li', 'this': 'ica', 'these': 'ici',
    'there': 'ibe', 'here': 'hike', 'where': 'ube', 'when': 'kande',
    'who': 'qua', 'what': 'quo', 'which': 'qua', 'how': 'quale',
    'very': 'tre', 'too': 'tro', 'more': 'plu', 'less': 'min',
    'all': 'omna', 'every': 'omna', 'some': 'ula', 'no': 'nula',
    'one': 'un', 'two': 'du', 'three': 'tri', 'four': 'quar',
    'five': 'kin', 'six': 'sis', 'seven': 'sep', 'eight': 'ok',
    'nine': 'non', 'ten': 'dek', 'hundred': 'cent', 'thousand': 'mil',
    'first': 'unesma', 'second': 'duesma', 'third': 'triesma',
    'is': 'esas', 'are': 'esas', 'was': 'esis', 'were': 'esis',
    'be': 'esar', 'been': 'esinta', 'has': 'havas', 'have': 'havas',
    'had': 'havis', 'will': None, 'would': None,
}


class Lexicon:
    """English -> Ido, from the Tabeli's glossary.

    `keys` restricts the lexicon to pairs drawn from a given set of segments.
    That is what makes a HELD-OUT measurement possible: the glossary was
    lifted from the same 672 segments a test set would be drawn from, so
    scoring against a segment whose own bold terms are in the lexicon scores
    nothing. `evaluate.py` passes the training half's keys here.
    """

    def __init__(self, code='en-GB', keys=None):
        self.code = code
        self.pairs = 0
        self.en2io = {}
        for i, e, ks in corpus.glosaro(code):
            if keys is not None and not (set(ks) & keys):
                continue
            self.pairs += 1
            self.en2io.setdefault(e.lower(), []).append(i)
        self.verbi = (corpus.verbi() or {}).get('verbi') or {}

    def lookup(self, en):
        return self.en2io.get(en.lower(), [])


# -------------------------------------------------- the little English there is
# Enough morphology to carry number and tense across, and no more. English is
# the source language here and only its INFLECTION has to be read; its lexicon
# is the glossary's problem.

IRREGULAR_PLURAL = {
    'men': 'man', 'women': 'woman', 'children': 'child', 'feet': 'foot',
    'teeth': 'tooth', 'geese': 'goose', 'mice': 'mouse', 'people': 'person',
    'leaves': 'leaf', 'knives': 'knife', 'wives': 'wife', 'lives': 'life',
}


def english_forms(w):
    """(lemma, features) candidates for an English word, likeliest first."""
    w = w.lower()
    out = [(w, {})]
    if w in IRREGULAR_PLURAL:
        out.append((IRREGULAR_PLURAL[w], {'number': 'plural'}))
        return out
    if w.endswith('ies') and len(w) > 4:
        out.append((w[:-3] + 'y', {'number': 'plural'}))
    if w.endswith('es') and len(w) > 3:
        out.append((w[:-2], {'number': 'plural'}))
    if w.endswith('s') and not w.endswith('ss') and len(w) > 3:
        out.append((w[:-1], {'number': 'plural'}))
    if w.endswith('ing') and len(w) > 5:
        out.append((w[:-3], {'tense': 'present', 'verbal': True}))
        out.append((w[:-3] + 'e', {'tense': 'present', 'verbal': True}))
    if w.endswith('ed') and len(w) > 4:
        out.append((w[:-2], {'tense': 'past', 'verbal': True}))
        out.append((w[:-1], {'tense': 'past', 'verbal': True}))
    return out


class Translator:
    def __init__(self, lexicon=None, code='en-GB', keys=None):
        self.lex = lexicon or Lexicon(code, keys)
        self.an = ido.Analyser()

    # -- one word ----------------------------------------------------------
    def word(self, en, want=None):
        """Translate one English word. Returns (ido, note) or (None, why).

        `want` carries features read off the English -- number, tense -- which
        are then realised by the Gramatiko's endings rather than copied.
        """
        want = dict(want or {})
        low = en.lower()
        if low in FUNCTION:
            v = FUNCTION[low]
            return (v, 'function word') if v else (None, 'dropped: Ido has no '
                                                   'indefinite article')
        for lemma, feat in english_forms(low):
            hits = self.lex.lookup(lemma)
            if not hits:
                continue
            f = dict(want)
            f.update(feat)
            return self._realise(hits[0], f)
        return (None, 'not in the glossary')

    def _realise(self, head, feat):
        """Put a Dicionario headword into the form the features ask for."""
        parses = self.an.analyse(head.lower())
        if not parses:
            return (head, 'glossary form, unanalysed')
        p = parses[0]
        stem = ''.join(p.prefixes) + p.root + ''.join(p.suffixes)
        pos = p.pos
        # THE GLOSSARY'S IDO SIDE IS ALREADY INFLECTED -- it is lifted from a
        # printed sentence, so `tables` is paired with `tabli` and not with
        # `tablo`. Its own number is the default; the English overrides it
        # only where the English actually carried one. Without this the
        # plural is silently thrown away and every noun comes out singular.
        for k in ('number', 'tense'):
            if k not in feat and k in p.features:
                feat[k] = p.features[k]
        note = []
        if feat.get('verbal') and pos != 'verb':
            pos = 'verb'
        if pos == 'verb':
            surface = ido.generate(stem, 'verb',
                                   tense=feat.get('tense', 'present'))
            v = self.lex.verbi.get(head.lower())
            if v:
                kind = ', '.join(v.get('speco') or [])
                if kind:
                    note.append(kind)
                if v.get('regas'):
                    note.append('regas ' + ', '.join(v['regas']))
                if v.get('senci'):
                    note.append('SEGUN LA SENCO: ' + '; '.join(
                        '%s=%s' % kv for kv in sorted(v['senci'].items())))
        elif pos in ('noun', 'adjective', 'adverb'):
            surface = ido.generate(stem, pos,
                                   number=feat.get('number', 'singular'))
        else:
            surface = head
        return (surface, '; '.join(note) or pos)

    # -- a sentence, glossed ----------------------------------------------
    def gloss(self, text):
        """Word by word, in the English order.

        NOT A SENTENCE TRANSLATOR, and the order is left alone deliberately.
        Ido and English are both subject-verb-object, so the order carries
        for a plain declarative and is wrong for everything else; a reordering
        rule would need a parse of the English, and there is no English parser
        in these three books.
        """
        out = []
        for m in WORD.finditer(text):
            en = m.group(0)
            io, note = self.word(en)
            out.append({'en': en, 'io': io, 'note': note})
        return out


def render(rows):
    got = [r for r in rows if r['io']]
    line = ' '.join(r['io'] for r in got)
    miss = [r['en'] for r in rows if not r['io']
            and 'indefinite' not in (r['note'] or '')]
    return line, miss


if __name__ == '__main__':
    t = Translator()
    print('glossary pairs loaded: %d\n' % t.lex.pairs)
    for w, f in [('table', {}), ('tables', {}), ('school', {}),
                 ('bench', {}), ('benches', {}), ('to give', {}),
                 ('horse', {}), ('happiness', {})]:
        io, note = t.word(w.replace('to ', ''), f)
        print('  %-12s -> %-16s %s' % (w, io or '--', note))

    print()
    for s in ['The teacher is in the classroom.',
              'This chart shows a classroom in a secondary school.',
              'The children are writing with pens on eight tables.']:
        line, miss = render(t.gloss(s))
        print('  EN  %s' % s)
        print('  IO  %s' % line)
        if miss:
            print('  MISSING  %s' % ', '.join(miss))
        print()
