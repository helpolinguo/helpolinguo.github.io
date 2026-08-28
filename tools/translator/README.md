# A machine translator out of the three books — what was tried, and what holds

**THE GRAMMAR HALF OF THE IDEA WORKS AND THE DISTRIBUTIONAL HALF DOES NOT, AND
NEITHER IS THE THING THAT DECIDES IT.** The rules reach 96.3 % of running Ido;
Word2Vec, given every advantage, answers 1.2 % of a held-out translation set
against the rules' 40.5 %. But the number that governs the whole idea is
neither of those: **the site's only Ido–English lexicon reaches 1,143 of the
Dicionario's 9,272 roots — 12.3 % — and all 56 languages together reach
13.5 %.** There is no translator here for want of words, not for want of
method.

Nothing in this directory is served, and nothing outside it was touched.

    corpus.py                 the three books, loaded; every count below
    ido.py                    Ido morphology: analysis and generation
    coverage.py               what the rules reach, over the site's own Ido
    experiment_embeddings.py  Doc2Vec and Word2Vec, tried and measured
    translate.py              English -> Ido: glossary, endings, valency
    evaluate.py               the two methods, one held-out split

Each runs on its own and reads the three book repositories beside this one,
degrading the way `machine_files.py` does when they are absent.

## 1. The corpus is 251,467 tokens, and that is the whole argument

| | tokens |
|---|---:|
| Dicionario, the definitions | 156,657 |
| Gramatiko, the prose | 76,583 |
| Tabeli, the Ido column | 18,227 |
| **all the Ido on the site** | **251,467** |

26,109 types, of which **52.2 % occur exactly once**. Published Word2Vec
vectors are trained on about 10⁹ tokens: this corpus is 0.025 % of that.

That is not a shortfall more epochs close. At `min_count=5` — Word2Vec's own
default, below which a word has no distribution worth estimating — **1,814 of
the 9,473 headwords get a vector, 19.1 %.** The words that fall out are the
rare and technical ones, which is most of what a 10,000-root dictionary is
for.

## 2. Doc2Vec loses to counting, and Word2Vec ties it

Scored against a gold nobody here composed: the subject field the Dicionario
prints on the articles it classes — `(bot.)`, `(zool.)`, `(anat.)`. If a
vector carries meaning, a botanical word's nearest neighbour is botanical
more often than chance.

**All three methods on one pool of 561 words**, because scored on their own
pools they answer different questions — Word2Vec's pool is the words frequent
enough to have a vector, which are the easy ones, and it flatters itself by
20 points that way:

| method | nearest neighbour shares the field |
|---|---:|
| chance | 15.3 % |
| Word2Vec skip-gram, 100d | 56.7 % |
| **tf-idf over the same definitions** | **52.8 %** |
| Doc2Vec over the definitions | 32.6 % |

And over all 4,337 classed headwords the definitions reach, where **Word2Vec
cannot compete at all** — 3,776 of them have no vector:

| method | |
|---|---:|
| chance | 9.7 % |
| **tf-idf over the definitions** | **54.0 %** |
| Doc2Vec over the definitions | 33.8 % |

**Doc2Vec is 20 points worse than counting the words in the definitions**, and
Word2Vec's 4-point edge is bought on the 13 % of the vocabulary it can see.
Neither earned its training.

The neighbours say the same thing plainly. `domo` gives *lojas, masonisto,
rempari, muri, tekto* and `skribar` gives *plumo, lektar, krayono* — both
good. `rozo` gives *larjeso, stopilo, edra, triopla*, which is geometry, and
`kavalo` gives *tayo, jungita, masto*. The model is right where the word is
common and noise where it is not, and it cannot tell you which it is doing.

## 3. The morphology is exact, and it is not learned

Ido's endings are unambiguous and exceptionless: `-o` noun, `-a` adjective,
`-e` adverb, `-as` present, `-is` past, `-os` future, `-us` conditional, `-ez`
imperative. No irregular verb, no gender, no stem change. A rule table
therefore does not approximate the morphology — **it is the morphology**, and
a model trained on 251,467 tokens could at best rediscover part of it.

`ido.py` strips the ending, peels affixes off the stem, and looks the
remainder up among the Dicionario's roots. What that reaches, over the site's
own Ido:

| | tokens | covered | types | covered |
|---|---:|---:|---:|---:|
| **Tabeli** (ordinary prose) | 18,227 | **96.3 %** | 5,043 | 92.1 % |
| Dicionario | 156,657 | 97.5 % | 18,335 | 91.5 % |
| Gramatiko | 76,583 | 92.9 % | 10,087 | 78.0 % |
| all | 251,467 | 96.0 % | 26,109 | 85.4 % |

The Tabeli is the row that counts: the other two books talk *about* the
language and cite forms it does not otherwise use.

**Of the 4 % not reached, most is not Ido.** Sorted:

| | tokens | |
|---|---:|---|
| vocabulary the books do not reach | 7,259 | 2.9 % |
| a fragment the Gramatiko quotes (`-n`, `-iv-`) | 1,925 | 0.8 % |
| the Dicionario's abbreviated field (`metaf.`, `geom.`) | 865 | 0.3 % |

So the honest figure is **2.9 %**, and it is mostly proper nouns and nation
names — *franca, angla, germana, francia, ioannes, couturat* — which a
dictionary of roots was never going to hold.

### What had to be added to the 65 affixes, and it is a real finding

The affix chapters are not the whole of Ido's word-building. Starting from the
65 affixes alone, the analyser missed `dil` 557 times, `ulu` 523, `igar` 345,
`mea` 235, `unesma` 185 — all ordinary words. Each needed a rule the Gramatiko
states in a *different* chapter:

* the article's elisions, `al dal del dil`, one word in the text and two in
  the grammar;
* the possessives, pronoun + `-a`, regular over the whole set;
* the correlatives, a closed table — kept as a list here, because the stems
  overlap real roots and generating them would invent words;
* the numerals and their suffixes `-esma -opla -ona -ima`, which live in the
  numeral chapter and not among the affixes;
* an affix standing as a word of its own — `igar`, `ajo`, `ero`;
* a preposition used as a prefix — `de-prenar`, `ad-juntar`;
* two roots compounded — `ter-globo`, `skrib-mashino`.

Those took the Tabeli from 92.3 % to **96.3 %**. **`gramatiko/afixi/` is 65
files and it is not the whole derivational system**; `llms.txt` sends a model
there to build `kovrilo` and `dometo`, and it is right to, but a model that
reads only those 65 files cannot parse `dil`.

Compounding is bounded to two roots of three letters or more. Unbounded, a
9,272-root lexicon will cut any string into something and the parses stop
meaning anything.

## 4. English to Ido, and the wall both methods hit

The split is **of the Tabeli's 672 segments**, not of the glossary's pairs:
each pair records the segments it was lifted from, and splitting the pairs
would leave the same printed sentence on both sides of the line. 537 segments
train, 135 held out, **369 pairs occurring only in the held-out half.**

| | attempted | P@1 on attempted | of all 369 |
|---|---:|---:|---:|
| **rules** — glossary lookup + the Gramatiko's endings | 37 | **40.5 %** | 4.1 % |
| **embeddings** — Word2Vec + GloVe, Procrustes | 85 | 1.2 % | 0.3 % |

The embedding method was given every advantage that can honestly be given it:
pretrained English vectors from 6 × 10⁹ tokens, the standard orthogonal
Procrustes construction, and scoring only on the pairs it could attempt. It
answered **one of 85**. Of the 1,528 training pairs, only 405 could be used to
fit the mapping at all — the rest lose their Ido side to `min_count` or are
phrases — against the several thousand such a fit expects.

**40.5 % understates the rules, and the errors say why.** They are mostly
defensible synonyms punished by a single reference: *friend* → `kamarado`
against a gold of `amiko`, *chair* → `stulo` against `sidilo`, *flag* →
`flago` against `standardo`. Two more are artefacts of the glossary itself
(`naz)binoklo`, `tablo)-tuko`).

### The wall

The rules attempted only 37 of 369, and that is the whole story:

* **89.7 % of the glossary's English terms appear in exactly one segment.**
  Hold that segment out and the word is simply gone — not mistranslated,
  absent.
* The held-out misses are *Cornflowers, wagtail, alpenstock, apricots,
  arsenal, forearm* — a picture book's vocabulary, each word printed once.
* **The en-GB glossary reaches 1,143 of 9,272 roots, 12.3 %.**
* **All 56 languages together reach 1,250, 13.5 %.** Adding 55 languages buys
  1.2 points, because every glossary is built from the same bold runs of the
  same 672 segments. **Pivoting through another language cannot help**, and
  that was worth measuring before believing.

## 5. What the Dicionario does give a writer, and it is not vectors

`verbi.json` marks 2,020 verbs transitive or intransitive and gives the
preposition 396 of them govern. `translate.py` carries it through, so
`donar` comes out marked `transitiva, regas ad`, and the 31 verbs that answer
differently for different senses come out saying so rather than picking. In
Ido that mark decides whether `-ig-` or `-es-` is the right derivation: a verb
used without it is a guess, and this is gold data, not an estimate.

## 6. What was tried and abandoned

* **Doc2Vec over the articles** — the proposal's first leg. 32.6 % against
  tf-idf's 52.8 % on the same words. The documents are the reason: 11,690
  senses averaging 17.8 tokens. There is no paragraph for PV-DM to learn from.
* **Cross-lingual Word2Vec** — the proposal's second leg. 1.2 % P@1. Killed
  upstream: only 480 of the glossary's 1,423 single-word Ido terms have a
  vector at all.
* **Scoring each method on its own pool.** The first run gave Word2Vec 57.9 %
  and Doc2Vec 33.7 % — on different words. Meaningless, and it favoured
  Word2Vec by about 20 points. One pool now.
* **`workers=4`.** gensim's seed fixes the initialisation, not the order
  threads apply updates in: two runs of identical code printed P@5 of 10.6 %
  and 14.1 %. `workers=1` throughout — it costs seconds and makes the numbers
  quotable.
* **Reordering the English in `gloss()`.** Ido and English are both
  subject-verb-object, so the order carries for a plain declarative and is
  wrong for everything else. Fixing it needs a parse of the English, and there
  is no English parser in these three books.
* **Generating the accusative `-n`.** Stripped on analysis, never generated.
  `temi/akuzativo.md` is 47 blocks on when the ending is obligatory, and it
  turns on a word order this translator does not compute. Leaving it off is
  always grammatical in the plain order; guessing it is not.

## 7. Where this would go next, if anywhere

Not to a bigger model. **To a bigger lexicon**, which is the only thing that
moves the number:

1. **The Dicionario's definitions are the untapped asset.** 9,473 roots
   defined in Ido, and tf-idf over them already beat both embeddings at
   grouping words by field. That gives Ido → *understanding* for the whole
   dictionary, where the glossary gives 12.3 %. It does not give English, but
   it is the only structure covering the whole vocabulary.
2. **The 65 affixes plus 9,272 roots generate far more than either book
   lists** — `kovrilo`, `dometo`, `hundino` are the point `llms.txt` makes.
   Derivation is a multiplier on a lexicon; it is not one.
3. **An Ido–English lexicon at dictionary scale would have to come from
   outside this site**, and that should be said plainly rather than
   engineered around. The three books are a monolingual dictionary, a
   grammar, and one 672-segment parallel text. Two of those three are exactly
   what a rule-based translator wants. The third is 1,897 pairs of one
   register, and no method run over it makes it larger.

## Running it

    python3 tools/translator/corpus.py                 # the counts
    python3 tools/translator/ido.py                    # analyse and generate
    python3 tools/translator/coverage.py               # what the rules reach
    python3 tools/translator/translate.py              # English -> Ido
    python3 tools/translator/experiment_embeddings.py  # needs gensim
    python3 tools/translator/evaluate.py               # the head-to-head

`experiment_embeddings.py` and `evaluate.py` need `gensim`. `evaluate.py`
additionally scores the embedding method only if English vectors are pointed
at by `IDO_GLOVE`; without them it runs and reports the rules alone.
