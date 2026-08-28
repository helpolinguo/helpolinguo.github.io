# A machine translator out of the three books — what was tried, and what holds

**MACHINE TRANSLATION IN IDO CANNOT BE SOLVED OUT OF THESE THREE BOOKS, AND
THE REASON IS THE LEXICON, NOT THE METHOD.** Five routes were tried and
measured. The one number that governs all of them: **the site's only
Ido–English lexicon reaches 1,143 of the Dicionario's 9,272 roots — 12.3 % —
and all 56 languages together reach 13.5 %**, because every glossary is built
from the same bold runs of the same 672 segments.

| route | what it scored |
|---|---|
| the Gramatiko's rules, as morphology | **96.7 %** of running Ido analysed |
| glossary lookup + those rules, EN → IO | **40.5 %** P@1, on 10 % of held-out words |
| Word2Vec + GloVe, Procrustes, EN → IO | **1.2 %** P@1 |
| Doc2Vec over the articles | **32.6 %**, against tf-idf's 52.8 % |
| cognates + definitions, IO → EN | **F1 17.9 %**, glossing 76.7 % of tokens |

**THE TWO DIRECTIONS ARE NOT SYMMETRICAL, AND THAT IS THE USEFUL FINDING.**
Going English → Ido you must CHOOSE a word, and there is nothing to choose
from: 89.7 % of the glossary's English terms appear in exactly one segment, so
hold that segment out and the word is absent, not mistranslated. Going Ido →
English you need only RECOGNISE one, and recognition has three sources where
choice had one — the glossary, the cognate the Dicionario itself marks, and
the article every root has. That direction produces a rough reading gloss for
arbitrary Ido. It is not a translator, and it is not called one here.

Nothing in this directory is served, and nothing outside it was touched.

    corpus.py                 the three books, loaded; every count below
    ido.py                    Ido morphology: analysis and generation
    coverage.py               what the rules reach, over the site's own Ido
    experiment_embeddings.py  Doc2Vec and Word2Vec, tried and measured
    cognates.py               the English cognate the Dicionario marks
    translate.py              English -> Ido: glossary, endings, valency
    io2en.py                  Ido -> English: the direction that goes further
    evaluate.py               every route, one held-out split

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
| **Tabeli** (ordinary prose) | 18,227 | **96.7 %** | 5,043 | 93.0 % |
| Dicionario | 156,657 | 97.7 % | 18,335 | 92.6 % |
| Gramatiko | 76,583 | 93.1 % | 10,087 | 79.0 % |
| all | 251,467 | 96.2 % | 26,109 | 86.6 % |

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

Those took the Tabeli from 92.3 % to **96.3 %**, and the linking vowel below took it to **96.7 %**. **`gramatiko/afixi/` is 65
files and it is not the whole derivational system**; `llms.txt` sends a model
there to build `kovrilo` and `dometo`, and it is right to, but a model that
reads only those 65 files cannot parse `dil`.

Compounding is bounded to two roots of three letters or more. Unbounded, a
9,272-root lexicon will cut any string into something and the parses stop
meaning anything.

**And Ido welds with a linking vowel**, usually `-o-`. Without allowing for it
`docochambro` — the word the Tabeli's first chapter is *about* — had no parse
at all, nor did `ludokorto` or `klokotabelo`. That one rule took the Tabeli's
types from 92.1 % to 93.0 %.

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

## 5. The Dicionario marks which roots have an English cognate

Every article prints the languages the root is ATTESTED in — the `DEFIRS` the
book sets as `Germana, Angla, Franca, Italiana, Rusa, Hispana`. **7,165 of the
9,473 roots are marked `Angla`, 75.6 %**: the root was admitted into Ido partly
*because* English has a cognate of it. That is a bridge nothing else on the
site provides, and it was worth testing.

`cognates.py` folds an Ido spelling and an English one onto one alphabet and
matches them. **The mark is a real signal and not a guess:** recovery scores
**28.6 % precision on roots marked `Angla` against 7.0 % on roots not marked** —
four times better, so the gate is kept.

**BUT `llms.txt` IS RIGHT, AND THE MEASUREMENT SAYS SO.** The map warns that
"an answer built from the English cognate of a headword is not this book's
answer, and for most words it is not the same answer." Against the Tabeli's
gold pairs the recovered cognate is the glossary's own word only 28.6 % of the
time, and the failures are not noise — they are *correct cognates*:

| Ido | cognate recovered | what the book prints |
|---|---|---|
| `kupo` | cup | bowl |
| `pastoro` | pastor | herdsman |
| `ursino` | ursine | bear |
| `dorso` | doors | back |

Three of those four are the right cognate and the wrong gloss. **So the
cognate is never used as a translation here.** It is used for the one thing it
is reliable at: making the Dicionario's own Ido definitions legible, which
takes the share of definition tokens renderable in English **from 16.7 % to
76.3 %**.

Two things had to be got right, and both are recorded because both were wrong
first:

* **Ido's `c` is always /ts/**, where English's is /k/ or /s/. Folded with
  English's rule, `substanco` and `edifico` failed to reach *substance* and
  *edifice*. The two spellings need two foldings, and English is indexed under
  both readings of every `c`.
* **The vocabulary is capped at the commonest 40,000 English words.** Scanning
  150,000 took precision from **39.9 % to 33.5 % and bought no recall**: the
  extra matches were tokens like `nacion` and `urs` standing in front of
  *national* and *ursine*.

## 6. Ido to English, which is the direction that goes further

Scored against the printed English of the same 672 segments — a real parallel
text — as bag-of-content-words overlap, which is the right measure for a
reading aid: the question is whether a reader gets the content, not whether
the word order matches a translator's. Glossary built from the training
segments only, scored on 135 held-out ones.

| configuration | tokens glossed | precision | recall | F1 |
|---|---:|---:|---:|---:|
| glossary only | 57.2 % | 26.2 % | 11.0 % | 15.5 % |
| **glossary + cognate** | **76.7 %** | 20.8 % | 15.8 % | **17.9 %** |
| glossary + cognate + definition | 93.5 % | 4.9 % | 17.4 % | 7.6 % |

**The cognate earns its place and the definition does not.** Reading an
unknown word out of its own article glosses 93.5 % of tokens instead of
76.7 % — and takes precision from 20.8 % to 4.9 %, halving F1. The extra
seventeen points of coverage are noise wearing a sentence's clothes: `mezo`
comes out `{part which dictate dee horsemen extreme}`. It is kept in the code,
switched off, because a measured negative belongs in the record.

That failure was predicted by a cleaner measurement and then confirmed in
running text: asked to name the single English word for a held-out Ido one, a
definition's centroid scores **0.0 % P@1**. A definition points at the region
of its own words — *domesticated carnivorous mammal* — and not at `dog`.

**What it actually produces**, on held-out segments (`~` marks a gloss induced
from a cognate rather than attested, `[?]` a word with no gloss at all):

    IO  La ludo-korto
    ->  the games yard
    EN  The playground.

    IO  An la parieto esas fixigita vest-hoki (58) , de li pendas la kapvesti
    ->  [An?] the wall is [fixigita?] coat hooks from they ~pending the clothings
    EN  Coat hooks (58) are fixed to the partition; the pupils' hats and coats hang

**F1 of 17.9 % is a rough gloss, not a translation, and it is not called one.**
What it is good for is that it degrades honestly: every induced word is marked
as induced and every unknown one is left in Ido, so a reader is never handed a
confident sentence built out of guesses.

## 7. What the Dicionario does give a writer, and it is not vectors

`verbi.json` marks 2,020 verbs transitive or intransitive and gives the
preposition 396 of them govern. `translate.py` carries it through, so
`donar` comes out marked `transitiva, regas ad`, and the 31 verbs that answer
differently for different senses come out saying so rather than picking. In
Ido that mark decides whether `-ig-` or `-es-` is the right derivation: a verb
used without it is a guess, and this is gold data, not an estimate.

## 8. What was tried and abandoned

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
* **Glossing an unknown word out of its own article.** 0.0 % P@1 asked for a
  single word, and in running text it halves F1 while looking like prose. The
  most confident-sounding output of anything here and the worst.
* **A bigger English vocabulary for the cognate matcher.** 150,000 words
  against 40,000: precision fell 6.4 points and recall did not move.
* **Generating the accusative `-n`.** Stripped on analysis, never generated.
  `temi/akuzativo.md` is 47 blocks on when the ending is obligatory, and it
  turns on a word order this translator does not compute. Leaving it off is
  always grammatical in the plain order; guessing it is not.

## 9. What would actually solve it

Not a bigger model, and this has now been measured five ways. **A lexicon.**
Ranked by what each would buy:

1. **An Ido–English word list at dictionary scale is the whole problem, and it
   has to come from outside these three books.** Nothing here generates one:
   the glossary is 1,897 pairs of one register, the cognate route is 28.6 %
   precise and confuses a cognate with a gloss, and the definitions score
   0.0 %. Ido has published bilingual dictionaries — Dyer 1924 among them —
   and one of those, transcribed the way these three were, would move the
   12.3 % figure and nothing else on this site will. **That is the honest next
   step, and it is a transcription project, not a modelling one.**
2. **The morphology and the valency are already done and would carry over
   unchanged.** They are exact, they cover 96.7 % of running Ido, and they are
   the half of a translator that usually costs the most. Whatever lexicon
   arrives, `ido.py` inflects it correctly and `verbi.json` frames its verbs.
   Nothing built here would be thrown away.
3. **The Ido → English gloss is usable now, for reading.** It marks what it
   induced and leaves what it cannot gloss in Ido, so it fails visibly. For a
   reader working through the Tabeli or the Gramatiko with the Dicionario
   open, that is worth something; for anyone wanting fluent English out of
   Ido, it is not, and it says so.

**What should NOT be tried again**, because it has been: training embeddings
on 251,467 tokens; scoring a method on its own convenient pool; treating the
English cognate of a headword as its translation; and glossing an unknown word
out of the definitions of its definitions.

## Running it

    python3 tools/translator/corpus.py                 # the counts
    python3 tools/translator/ido.py                    # analyse and generate
    python3 tools/translator/coverage.py               # what the rules reach
    python3 tools/translator/translate.py              # English -> Ido
    python3 tools/translator/cognates.py               # the cognate lexicon
    python3 tools/translator/io2en.py                  # Ido -> English
    python3 tools/translator/experiment_embeddings.py  # needs gensim
    python3 tools/translator/evaluate.py               # every route

`experiment_embeddings.py` and `evaluate.py` need `gensim`. `evaluate.py`
additionally scores the embedding method only if English vectors are pointed
at by `IDO_GLOVE`; without them it runs and reports the rules alone.
