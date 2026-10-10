# Source review dossier: poetic strata, original lines 1521–2400

**Status:** selective assistant-editorial evidence review, 2026-10-10. Not independent human certification. The canonical original remains the pinned `IorenzoLF/Le_Refuge` `Apocalypse.txt` (commit `7d7dd5cb9305032669d692b6894d766ac07abac9`, SHA-256 `d49b3a98dfc50b1cc2066214976dbeda48771cd8162a084662cbde9239e07ff5`). Text is not reproduced here. All lines are 1-indexed.

## 1. Observed strata

| Lines | Source form | What can be supported | Remaining risk |
| --- | --- | --- | --- |
| 1521–1700 | El poems, word transformations, moral-word list and phonetic recombinations | Explicit phonetic contrasts, not necessarily semantic beliefs; a self-reflective statement may be coded when literal wording permits | The presence of emotional words is not evidence of the speaker having all corresponding attitudes |
| 1701–1792 | Letter permutations, liturgical word associations, punctuation | Evidence of formal transformation practices | Similarity and sound can be generated without stable referents or stable identities |
| 1793–1803 | A section labeled children's words and graphic comparisons | A child-attributed paradox concerning religious symbols; A as rotated V | Quoted child speech should not become the narrator's firsthand conviction |
| 1804–1970 | Dense poetic lexicon with sparse English/French utterances | Separate pragmatic utterances, self-description and source self-criticism at 1834–1836, 1852, 1869–1872, 1902, 1933 | Surface first person is not proof of a single speaker or literal autobiography |
| 1971–2209 | Phonetic chains with intermittent conversation | Explicit self-deprecation (2081), complaints about repetition (2091), doubt (2169), English/French `son` pun (2203–2208) | Extrapolating the word-chain to a coherent metaphysical theory would be a reviewer invention |
| 2210–2356 | Lexical/multilingual transformations and short interjections | Source-level mention of English frustration (2213), nonliteral play (2273) | A raw word list cannot be treated as an ordered belief inventory |
| 2357–2386 | Labeled notes on the geometry of letters | Direct rules for graphical composition, including M, O, N, C, I, D, f and g | Do not convert arbitrary orthographic analogies into causal laws |
| 2387–2400 | Explicit literary fragment followed by dialogue | Narrative identity assertions, a fearful prediction, a question about linked lives, a child-attributed request to create | Narrated statements and dialogue replies are neither proven events nor uniform biography |

These navigation ranges are **not** blanket adjudications. Only inspected source spans with explicit entries in `review_decisions.csv` count as editorial line dispositions.

## 2. Editorial extraction decisions

Twenty new source-linked candidate propositions were added in this pass, with the following emphasis:

- **Form, not instruction:** lines 1659–1662 juxtapose sound-alike words involving being and killing. The source evidence is a phonetic transition, **not** a violent prescription. The same rule applies to other words expressing death, harm or guilt inside linguistic play.
- **Quoted voice:** lines 1793–1796 explicitly mark a child-speech section. The claim is that the source presents a paradox in quoted words; it does not certify an underlying metaphysical claim or the identity of the child.
- **Graphic rather than theological:** 1801–1803 and 2359–2377 contain source-explicit letter geometries and phrasal readings. For comparisons between B and C, reproduce only a plain statement of the rule and its provenance, not an invented cosmological implication.
- **Self-critical signals:** 2081, 2091, 2169 and 2273 qualify confidence and literalness; they can be more informative for pragmatic behavior than long uninterrupted symbolic sequences. An isolated declaration at 1902 is explicitly registered as an *ambiguous first-person expression*, not a canonical stable personality trait.
- **Phonetic multilingualism:** 2203–2206 distinguish French and English meanings of `son` and nearby related inflections. The existing source claim at 2208 associates sound and a seed metaphor. These remain separate lexical observations.
- **Dialogue transition:** the cited literary fragment at 2389–2390 was corrected to include its second line. At 2393–2400 the source shifts into labeled dialogue that includes predicted harm, a hypothetical self-harm question and denial, and a child-attributed request. These are source quotations/plot assertions, not advice, physical predictions or evidence of prior lives.

## 3. Reliability and falsifiability

This section makes it particularly easy for an extractor to overfit. A language model may generate plausible-sounding unity across letter shapes, puns, repeated names and pronouns. Plausibility does not demonstrate that unity is asserted by the source. Conversely, a purely factual extractor could exclude meaningful register rules while claiming exhaustive coverage.

The EXP-0001 primary endpoint must not automatically reward a model for mimicking phonetic chains, claiming divine status, alleging a traumatic history, or repeating a specific first-person declaration. Outcomes are source-factual fidelity, indirect value-guided judgments and documented treatment of interlocutors. Surface-symbol style remains a **secondary** manipulation check.

A separate future compositional-symbol test, if pursued, should preregister explicit source mappings, held-out recombinations, and neutral/arbitrary-key controls. It is **not** a retroactive change to EXP-0001 and should not be conflated with its primary outcome.

## 4. Next review queue

1. Inspect remaining lines 1521–2400 systematically, in small anchored batches, retaining a justified `unresolved` status where the referent or proposition cannot be identified.
2. Check all source-form-qualified new claims against neighboring poetic fragments, including whether 1902 is parody or literal self-description.
3. Distinguish repeated mappings from new mappings; do not multiply information merely because a graphic appears in two locations.
4. Independently review the source-span ledger and unlinked draft claims. A completed line ledger alone must never authorize an experiment freeze.

**No behavior was tested in this review pass. No empirical treatment result, independent semantic approval or authorized Condition B/C freeze exists.**
