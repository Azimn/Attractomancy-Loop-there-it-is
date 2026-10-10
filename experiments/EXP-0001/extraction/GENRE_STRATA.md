# EXP-0001 source genre strata and semantic treatment rules

**Status:** first-pass editorial source segmentation, 2026-10-09; not exhaustive semantic review and not permission to freeze B/C.

Original source: `IorenzoLF/Le_Refuge` commit `7d7dd5cb9305032669d692b6894d766ac07abac9`, `Le_refuge/MUST-READ/Apocalypse.txt`, SHA-256 `d49b3a98dfc50b1cc2066214976dbeda48771cd8162a084662cbde9239e07ff5`. Original text remains upstream under LEUNE v1.0.

## Why strata matter

This is not an uninterrupted persona monologue. It includes explicit symbolic dictionaries, extensive multilingual phonetic word lists, occasional narrative parables, quoted child dialogue, author notes and later disputed first-person claims. If the extractor writes *every word association* as an independent belief, B receives artificial redundancy. Conversely, excluding every cryptic item as noise can silently remove a genuine explicit source rule. Review decisions must therefore distinguish **meaning-bearing association**, **mere wordplay/format**, **attributed quoted claim**, **direct discourse instruction**, and **unstable first-person utterance**.

| Source span | Observed form | Extraction risk | Required handling |
| --- | --- | --- | --- |
| 35-60 | First alphabet of stated letter meanings | A later version changes some meanings | Preserve each explicit meaning and cross-check variants |
| 190-210 | Writing rules plus ontological claims | Style instructions might be mistaken for metaphysical truth | Distinguish textual convention from stated worldview |
| ~500-775 | Dense phonetic transformations, word lists, footnotes | Hundreds of associative pairs could overwhelm B | Review pair-by-pair or by demonstrably homogeneous span; do not classify all symbolic material as meaningless |
| 778-786 | Quoted child speech and explicit commentary identifying symbolic roles | A narrated claim could be imported as narrator biography | Preserve quote-source relationship; avoid direct personal adoption |
| 787-1203 | Mostly word transformations and lexical chains, with another child-speech episode at 1124-1129 | Overgeneralized register and missed embedded values | Check dialogue embedded within the list |
| 1204-1208 | Author note and transition to exercises | Attributed source claims are not the same as an external fact | File source-use claim separately |
| ~1209-1416 | Exercises, glyphs, first-person queries and multilingual fragments | Many short lines require neighboring context | Do not call fragments non-extractable solely by length |
| 1417-1466 | Second symbolic alphabet and annotations | Repeated meanings can be double-counted; C and V differ | Mark repeated mappings as duplicate occurrences and changed meanings as distinct claims |
| 1480-1519 | An explicitly introduced parable | Stories could be mistaken for remembered events | Code as parable, never as subject autobiography |
| ~1521-2400 | Extensive poems and multilingual wordplay | Form may be important even if not truth-apt | Contextual review, explicit reasons when nonextractable |
| ~2400-5000 | Dialogue and relationship/theological assertions | Interlocutor and speaker shift without stable names | Leave voices unattributed unless explicit context resolves them |
| ~5000-5562 | Mixed dialogue, numerical and symbolic wordplay | An apparently stable self-narrative can be constructed by selection | Preserve uncertainty, direct moral assertions, and criticism of symbolic abuse |

These are **navigation aids**, not adjudication outcomes for complete spans. Only explicit rows in `review_decisions.csv` count as source-line decisions.

## A consequential source conflict

The first alphabet (line 56) associates **V** with *Verbe*; the second (line 1453) associates **V** with *vérité*. The later interpretation of **C** (1422-1423) likewise differs from its earlier creator/calculation statement (37). These differences are now separate source-cited draft propositions rather than collapsed into a single supposedly consistent lexical rule. Most other second-alphabet entries can refer to their earlier mapping as a **repeat occurrence** in the review ledger, subject to independent confirmation.

This variation suggests a possible *flexible symbolic practice*, not necessarily a uniform, timeless dictionary. A blind evaluator should not claim the corpus has one constant mapping for each letter unless the full audit supports it.

## Condition B and C parity

B must retain distinct, explicit meanings, normative stances and speaker-qualified claims in ordinary French. A wordplay construction with no truth-apt proposition remains documented in the decision ledger and its form remains in D, but cannot be supplied as an imagined conviction. C may paraphrase an explicit mapping's meaning but should not recreate D's literal sequence or theatrical typography. Because this format difference is unavoidable, **lexical stylization is secondary**; D may only beat C in the primary outcomes through source-accurate claims, judgments and interlocutor handling.

## Review next

1. Complete contextual passes through the under-adjudicated early lexicon without automatically dismissing all wordplay.
2. Audit the second alphabet's annotation lines separately; currently the repeated base mappings are recorded, but some footnotes and elaborations remain open.
3. Examine extended poems (1521-2400) for extractable normative or identity claims that might be missed by prose-line heuristics.
4. Continue independent voice and near-synonym checking across later dialogue, then seek independent review of the final complete source.

No review signoff, model call, or treatment outcome is asserted here.
