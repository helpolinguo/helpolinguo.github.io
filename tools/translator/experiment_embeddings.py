"""THE DISTRIBUTIONAL HALF OF THE PROPOSAL, TRIED AND MEASURED.

The proposal was: Doc2Vec over the Dicionario's articles, Word2Vec to carry
Ido across to another language, the Gramatiko's rules to inflect the result.
This file tests the first two. `ido.py` and `translate.py` build the third,
which is the half that works.

WHAT IS MEASURED HERE, AND WHY IT DECIDES THE QUESTION

Word2Vec learns a word's meaning from the company it keeps, so it needs each
word to keep company MANY TIMES. The whole of the Ido on this site is 251,467
tokens. Published Word2Vec vectors are trained on 10^9. That is not a
difference of degree that more epochs will close: at this size more than half
the vocabulary is seen exactly once, and a word seen once has no distribution
to estimate.

The measurements below are the ones that settle it rather than illustrate it:

  1. HOW MUCH OF THE DICTIONARY EVEN GETS A VECTOR. Word2Vec learns only words
     that occur in the running text. The running text here IS the definitions,
     so a root gets a vector only when OTHER articles happen to use it.

  2. WHETHER THE VECTORS IT DOES LEARN CARRY MEANING. The Dicionario prints a
     subject field on the articles it classes -- `(bot.)`, `(zool.)`,
     `(anat.)` -- and that is a gold label nobody here composed. If the
     embedding is worth anything, a botanical word's nearest neighbour is
     another botanical word more often than chance.

  3. THE SAME TASK, DONE BY COUNTING INSTEAD. Words that share a definition
     vocabulary are related; that needs no training and no epochs. If plain
     counting matches or beats the embedding, the embedding earned nothing.

Run: python3 tools/translator/experiment_embeddings.py
"""

import collections
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import corpus  # noqa: E402

SEED = 20260828


def bar(title):
    print('\n' + title)
    print('-' * len(title))


def load():
    docs = corpus.ido_documents()
    if not docs:
        sys.exit('The three books are not beside this repository; see CLAUDE.md.')
    return docs


# ------------------------------------------------------- 1. what gets a vector

def coverage(model, dic, freq):
    bar('1. HOW MUCH OF THE DICTIONARY GETS A VECTOR AT ALL')
    heads = [r['v'] for r in dic]
    lower = [h.lower() for h in heads]
    inv = sum(1 for h in lower if h in model.wv)
    seen = sum(1 for h in lower if freq[h] > 0)
    print('headwords in the Dicionario          %6d' % len(heads))
    print('  occurring anywhere in the corpus   %6d  (%.1f%%)'
          % (seen, 100 * seen / len(heads)))
    print('  with a vector (min_count=5)        %6d  (%.1f%%)'
          % (inv, 100 * inv / len(heads)))
    print()
    print('A HEADWORD WITHOUT A VECTOR CANNOT BE TRANSLATED BY THIS METHOD,')
    print('and the ones that fall out are the rare and technical words, which')
    print('is most of what a 10,000-root dictionary is for.')

    g = corpus.glosaro('en-GB')
    if g:
        terms = {i.lower() for i, _, _ in g}
        single = {t for t in terms if ' ' not in t and '-' not in t}
        have = sum(1 for t in single if t in model.wv)
        print()
        print('glossary Ido terms (en-GB)           %6d' % len(terms))
        print('  single-word among them             %6d' % len(single))
        print('  with a vector                      %6d  (%.1f%%)'
              % (have, 100 * have / max(1, len(single))))
        print()
        print('The glossary is the ONLY Ido-English bridge on the site, so it is')
        print('the only possible seed for a cross-lingual mapping. A mapping is')
        print('fitted on pairs whose Ido side has a vector: that is the number')
        print('above, against the several thousand pairs such a fit expects.')
    return inv


# --------------------------------------------- 2 and 3. do the vectors mean

def gold_fields(dic, floor=10):
    """Headword -> subject field, for fields the book gives >= `floor` words."""
    by = collections.defaultdict(list)
    for r in dic:
        f = r.get('f')
        if f:
            by[f].append(r['v'].lower())
    return {w: f for f, ws in by.items() if len(ws) >= floor for w in ws}, by


def neighbour_purity(name, vec_of, pool, gold):
    """Share of words whose nearest neighbour carries the same field.

    Cosine, computed here rather than by the model, so that the embedding and
    the counting baseline are scored by exactly the same code.
    """
    import numpy as np
    words = [w for w in pool if w in vec_of]
    if len(words) < 20:
        print('%-34s  too few words to score (%d)' % (name, len(words)))
        return None
    M = np.array([vec_of[w] for w in words], dtype='float32')
    M /= (np.linalg.norm(M, axis=1, keepdims=True) + 1e-9)
    S = M @ M.T
    np.fill_diagonal(S, -2.0)
    nn = S.argmax(axis=1)
    hit = sum(1 for i, j in enumerate(nn) if gold[words[i]] == gold[words[j]])
    print('%-34s  %5.1f%%   (%d words)' % (name, 100 * hit / len(words), len(words)))
    return hit / len(words)


def chance(pool, gold):
    """Two words drawn at random sharing a field -- the floor to beat."""
    c = collections.Counter(gold[w] for w in pool)
    n = len(pool)
    return sum(k * (k - 1) for k in c.values()) / (n * (n - 1)) if n > 1 else 0.0


def counting_vectors(dic, gold):
    """The baseline: a word IS the words its definition uses, weighted by how
    rare they are. No training, no epochs, no seed. Built with the same
    tokeniser the embedding saw."""
    import numpy as np
    text = collections.defaultdict(list)
    for r in dic:
        w = r['v'].lower()
        if w not in gold:
            continue
        for s in r.get('b') or []:
            text[w] += corpus.tokens(s.get('t') or '')
    df = collections.Counter(t for ts in text.values() for t in set(ts))
    kept = [t for t in sorted(df) if df[t] >= 2]
    vocab = {t: i for i, t in enumerate(kept)}
    import math
    N = len(text)
    out = {}
    for w, ts in text.items():
        v = np.zeros(len(vocab), dtype='float32')
        for t, n in collections.Counter(ts).items():
            if t in vocab:
                v[vocab[t]] = (1 + math.log(n)) * math.log(N / df[t])
        if v.any():
            out[w] = v
    return out


def main():
    random.seed(SEED)
    from gensim.models import Word2Vec, Doc2Vec
    from gensim.models.doc2vec import TaggedDocument

    docs = load()
    sents = [d for _, d in docs]
    freq = collections.Counter(w for d in sents for w in d)
    dic = corpus.dicionario()

    bar('THE CORPUS THE PROPOSAL WOULD BE TRAINED ON')
    per = collections.Counter()
    for tag, d in docs:
        per[tag] += len(d)
    for tag in ('dicionario', 'gramatiko', 'tabeli'):
        print('  %-11s %7d tokens' % (tag, per[tag]))
    n = sum(per.values())
    print('  %-11s %7d tokens, %d types' % ('TOTAL', n, len(freq)))
    print('  hapax        %7d  (%.1f%% of types)'
          % (sum(1 for c in freq.values() if c == 1),
             100 * sum(1 for c in freq.values() if c == 1) / len(freq)))
    print('\n  Published Word2Vec vectors are trained on ~10^9 tokens.')
    print('  This corpus is %.5f%% of that.' % (100 * n / 1e9))

    print('\ntraining Word2Vec (sg, 100d, window 5, min_count 5, 30 epochs)...')
    w2v = Word2Vec(sents, vector_size=100, window=5, min_count=5, sg=1,
                   epochs=30, workers=1, seed=SEED)
    print('vocabulary with a vector: %d of %d types (%.1f%%)'
          % (len(w2v.wv), len(freq), 100 * len(w2v.wv) / len(freq)))

    coverage(w2v, dic, freq)

    gold, by = gold_fields(dic)
    bar("2. DO THE VECTORS CARRY MEANING? (gold: the book's subject fields)")
    print('fields with >= 10 headwords: %d, covering %d headwords'
          % (len({gold[w] for w in gold}), len(gold)))

    print('\ntraining Doc2Vec over the senses (PV-DM, 100d, 40 epochs)...')
    tagged = [TaggedDocument(d, [i]) for i, (_, d) in enumerate(docs)]
    d2v = Doc2Vec(tagged, vector_size=100, window=5, min_count=5, epochs=40,
                  workers=1, seed=SEED)
    import numpy as np
    art = {}
    for r in dic:
        w = r['v'].lower()
        if w not in gold:
            continue
        vs = [d2v.infer_vector(corpus.tokens(s.get('t') or ''))
              for s in (r.get('b') or []) if (s.get('t') or '').strip()]
        if vs:
            art[w] = np.mean(vs, axis=0)

    print('building the counting baseline (tf-idf over the same definitions)...')
    cv = counting_vectors(dic, gold)
    wv = {w: w2v.wv[w] for w in gold if w in w2v.wv}

    # ONE POOL FOR ALL THREE. Scored on their own pools the three answer
    # different questions: Word2Vec's pool is the words frequent enough to
    # have a vector, which are the easy ones, and it flatters itself by 20
    # points that way. The comparison below is like for like.
    pool = sorted(set(wv) & set(art) & set(cv))
    print('\npool scored by all three (every method has a vector): %d words'
          % len(pool))
    print()
    print('%-34s  %s' % ('method', 'nearest neighbour shares the field'))
    print('%-34s  %5.1f%%' % ('chance (the floor)', 100 * chance(pool, gold)))
    neighbour_purity('Word2Vec skip-gram 100d', wv, pool, gold)
    neighbour_purity('Doc2Vec over the definitions', art, pool, gold)
    neighbour_purity('tf-idf over the definitions', cv, pool, gold)

    # And what each covers, which is half the answer.
    full = sorted(set(art) & set(cv))
    print('\nthe same, over every classed headword the definitions reach')
    print('(Word2Vec cannot enter: %d of these %d have no vector)'
          % (len([w for w in full if w not in wv]), len(full)))
    print('%-34s  %5.1f%%' % ('chance (the floor)', 100 * chance(full, gold)))
    neighbour_purity('Doc2Vec over the definitions', art, full, gold)
    neighbour_purity('tf-idf over the definitions', cv, full, gold)

    bar('WHAT THE NEIGHBOURS LOOK LIKE')
    for w in ('hundo', 'kavalo', 'rozo', 'lakto', 'domo', 'skribar'):
        if w in w2v.wv:
            print('  %-10s %s' % (w, ', '.join(
                x for x, _ in w2v.wv.most_similar(w, topn=6))))
        else:
            print('  %-10s NO VECTOR (occurs %d times)' % (w, freq[w]))


if __name__ == '__main__':
    main()
