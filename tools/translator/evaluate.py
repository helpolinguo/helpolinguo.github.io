"""THE TWO METHODS, ON ONE HELD-OUT SPLIT, SCORED THE SAME WAY.

THE TASK. Given an English word, produce the Ido word. This is the question
the proposal was about, and `llms.txt` says the site answers it in exactly one
place: the Tabeli's glossary, 1,897 en-GB pairs lifted from a parallel text.

WHY A SPLIT IS NEEDED AND WHAT IS SPLIT. The glossary is derived from the 672
segments of the Tabeli, and each pair records the segments it came from. So
the split here is OF THE SEGMENTS, not of the pairs: the lexicon is built from
the training segments' pairs, and scored on pairs that occur ONLY in the
held-out segments. Splitting the pairs instead would leave the same printed
sentence on both sides of the line and score nothing.

THE TWO METHODS.

  RULES       look the English up in the training lexicon; put the Ido into
              the form the English asks for, using the Gramatiko's endings.

  EMBEDDINGS  the proposal. Word2Vec over all 251,467 tokens of Ido on the
              site; GloVe (400k words, 6B tokens) for the English; a linear
              map between the two spaces fitted by orthogonal Procrustes on
              the TRAINING pairs, which is the standard construction. To
              translate, carry the English vector into the Ido space and take
              the nearest Ido words.

The embedding method is given every advantage that can honestly be given it:
pretrained English vectors from a corpus 24,000 times the size of the Ido one,
and scoring only on pairs it is actually able to attempt.

Run: python3 tools/translator/evaluate.py
"""

import collections
import os
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import corpus     # noqa: E402
import ido        # noqa: E402
import translate  # noqa: E402

# workers=1 THROUGHOUT, and it is not an oversight. gensim's seed fixes the
# initialisation, not the order several threads apply their updates in, so
# with workers=4 this file printed P@5 of 10.6%% and 14.1%% on two runs of the
# same code. One worker costs seconds here and makes the numbers quotable.
SEED = 20260828

# The English vectors are NOT in this repository and are not fetched by it:
# 128 MB of somebody else's corpus, needed only to give the embedding method
# its fairest possible run. Without them the file still runs and reports the
# rules alone. To get them:
#
#     python3 -c "import gensim.downloader as api; \
#         api.load('glove-wiki-gigaword-100').save('glove100.kv')"
#
# then point IDO_GLOVE at the result.
GLOVE = Path(os.environ.get('IDO_GLOVE', Path.home() / 'glove100.kv'))


def split(frac=0.8):
    keys = sorted(corpus.tabeli())
    random.Random(SEED).shuffle(keys)
    cut = int(len(keys) * frac)
    return set(keys[:cut]), set(keys[cut:])


def held_out_pairs(train, test, code='en-GB'):
    """Pairs whose every segment is in the held-out half."""
    out = []
    for i, e, ks in corpus.glosaro(code):
        ks = set(ks)
        if ks and ks <= test and not (ks & train):
            out.append((i, e))
    return out


def bare(an, word):
    """The root of an Ido word, so that `tabli` and `tablo` count as one.

    Scoring on the surface would punish the rules for the plural the glossary
    happens to print, and reward nothing.
    """
    p = an.analyse(word.lower())
    return p[0].root if p else word.lower()


def main():
    import numpy as np

    train, test = split()
    pairs = held_out_pairs(train, test)
    an = ido.Analyser()

    print('Tabeli segments: %d train, %d held out' % (len(train), len(test)))
    print('pairs occurring ONLY in the held-out segments: %d' % len(pairs))

    lex = translate.Lexicon('en-GB', keys=train)
    print('lexicon built from the training segments: %d pairs' % lex.pairs)

    # ---------------------------------------------------------- the rules
    tr = translate.Translator(lexicon=lex)
    hit = attempt = 0
    for gold, en in pairs:
        io, _ = tr.word(en)
        if io is None:
            continue
        attempt += 1
        if bare(an, io) == bare(an, gold):
            hit += 1
    print()
    print('RULES  (glossary lookup + the Gramatiko\'s endings)')
    print('  attempted  %4d of %d  (%.1f%% -- the rest are words the training'
          % (attempt, len(pairs), 100 * attempt / len(pairs)))
    print('             half never showed it, and it says so rather than guessing)')
    print('  correct    %4d of %d attempted   P@1 = %.1f%%'
          % (hit, attempt, 100 * hit / max(1, attempt)))
    print('  correct    %4d of %d overall     %.1f%% of the whole held-out set'
          % (hit, len(pairs), 100 * hit / len(pairs)))

    # ----------------------------------------------------- the embeddings
    if not GLOVE.exists():
        print('\nEMBEDDINGS  skipped: no English vectors at %s' % GLOVE)
        return
    from gensim.models import Word2Vec, KeyedVectors
    print('\ntraining Word2Vec over the site\'s Ido (251,467 tokens)...')
    docs = [d for _, d in corpus.ido_documents()]
    w2v = Word2Vec(docs, vector_size=100, window=5, min_count=5, sg=1,
                   epochs=30, workers=1, seed=SEED).wv
    print('loading GloVe (6B tokens of English)...')
    en_kv = KeyedVectors.load(str(GLOVE))

    def one(w):
        """A single lowercase token, or None -- both spaces are word-level."""
        w = w.lower().strip()
        return w if w and ' ' not in w and '-' not in w else None

    # Fit on the training pairs.
    X, Y = [], []
    used = 0
    for i, e, ks in corpus.glosaro('en-GB'):
        if not (set(ks) & train):
            continue
        io, eng = one(i), one(e)
        if io and eng and io in w2v and eng in en_kv:
            X.append(w2v[io])
            Y.append(en_kv[eng])
            used += 1
    print('training pairs the mapping can actually use: %d' % used)
    print('  (of %d in the training half -- the rest lose the Ido side to'
          % lex.pairs)
    print('   min_count, or are phrases rather than single words)')
    if used < 20:
        print('TOO FEW TO FIT A MAPPING. That is the result.')
        return

    X = np.array(X, dtype='float64')
    Y = np.array(Y, dtype='float64')
    X /= np.linalg.norm(X, axis=1, keepdims=True) + 1e-9
    Y /= np.linalg.norm(Y, axis=1, keepdims=True) + 1e-9
    # Orthogonal Procrustes: W = UV' from the SVD of X'Y. Maps Ido -> English.
    U, _, Vt = np.linalg.svd(X.T @ Y)
    W = U @ Vt

    # Every Ido word with a vector, carried into the English space.
    ido_words = list(w2v.index_to_key)
    M = np.array([w2v[w] for w in ido_words], dtype='float64')
    M /= np.linalg.norm(M, axis=1, keepdims=True) + 1e-9
    M = M @ W
    M /= np.linalg.norm(M, axis=1, keepdims=True) + 1e-9

    scored = collections.Counter()
    at1 = at5 = at10 = 0
    for gold, en in pairs:
        g, e = one(gold), one(en)
        if not (g and e) or g not in w2v or e not in en_kv:
            scored['cannot attempt'] += 1
            continue
        scored['attempted'] += 1
        q = en_kv[e].astype('float64')
        q /= np.linalg.norm(q) + 1e-9
        sims = M @ q
        top = np.argsort(-sims)[:10]
        names = [ido_words[j] for j in top]
        gb = bare(an, g)
        ranks = [k for k, n in enumerate(names) if bare(an, n) == gb]
        if ranks:
            r = ranks[0]
            at1 += r < 1
            at5 += r < 5
            at10 += r < 10

    a = scored['attempted']
    print()
    print('EMBEDDINGS  (Word2Vec on Ido + GloVe on English, Procrustes)')
    print('  attempted  %4d of %d  (%.1f%%)'
          % (a, len(pairs), 100 * a / len(pairs)))
    print('  cannot attempt %d: the Ido word has no vector, or the pair is a'
          % scored['cannot attempt'])
    print('             phrase rather than a single word')
    if a:
        print('  P@1  %5.1f%%   P@5  %5.1f%%   P@10 %5.1f%%'
              % (100 * at1 / a, 100 * at5 / a, 100 * at10 / a))
        print('  correct at 1: %d of %d attempted, %d of %d overall (%.1f%%)'
              % (at1, a, at1, len(pairs), 100 * at1 / len(pairs)))

    print()
    print('%-14s %10s %10s %10s' % ('', 'attempted', 'P@1', 'of all pairs'))
    print('%-14s %9d %9.1f%% %9.1f%%'
          % ('rules', attempt, 100 * hit / max(1, attempt),
             100 * hit / len(pairs)))
    print('%-14s %9d %9.1f%% %9.1f%%'
          % ('embeddings', a, 100 * at1 / max(1, a), 100 * at1 / len(pairs)))


if __name__ == '__main__':
    main()
