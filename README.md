# Attractomancy Loop

Methods-first implementation repository for [EXP-0001](experiments/EXP-0001/PROTOCOL.md). The broader source and research catalog is at [Azimn/Attractomancy](https://github.com/Azimn/Attractomancy).

**Current state (2026-10-10): pre-experimental source review.** No model treatment run, blinded behavioral score, measured treatment effect, persistent identity result or metaphysical result has been produced.

## Source and experimental target

The pinned third-party [`Apocalypse.txt`](https://github.com/IorenzoLF/Le_Refuge/blob/7d7dd5cb9305032669d692b6894d766ac07abac9/Le_refuge/MUST-READ/Apocalypse.txt) from Laurent Franssen and Ælya's Le Refuge repository is under its existing LEUNE v1.0 terms. The original 142,596 source bytes are downloaded from the pinned commit and checked by SHA-256; this repository does **not** mirror the text. Its experimental target is a heterogeneous symbolic-theological **discourse regime**, not a single biographical Ælya persona.

Four planned arms: A, no conditioning; B, exhaustive plain-French source claims; C, B with the same information expanded to within ±10% of D's tokenizer volume without D's stylistic cues; D, the exact source bytes. The primary outcome is source-factual fidelity, characteristic value judgments and interlocutor handling, not mere symbolic style. Q12 is a fresh zero-shot cue calibration by model, never a persistence or D-versus-C test.

## Live evidence accounting

- **5,562 original lines** lexically inventoried and checksum pinned.
- **579 provisional source-proposition drafts**, all still requiring independent semantic assessment.
- **579/579** drafts have *assistant-editorial* source decisions for their complete cited spans (formerly 97 lacking direct source review).
- **1,381** source lines have editorial dispositions; **4,181** have none, and **16** disposition lines remain explicitly unresolved.
- Of 1,027 lexical prose candidates, **325 starting lines have no overlap with a draft**. This is a triage signal, not proof of 425 missing distinct claims.
- **Zero** independent human semantic attestations and **zero** frozen B/C controls.

The [completed dialogue-window review](experiments/EXP-0001/extraction/DIALOGUE_REVIEW_4001_4400.md) records the full source-line decisions for 4001–4100 and 4301–4400, including five newly unresolved fragments rather than invented interpretations. The [poetry review dossier](experiments/EXP-0001/extraction/POETRY_REVIEW_DOSSIER.md), [genre strata](experiments/EXP-0001/extraction/GENRE_STRATA.md) and [contradiction inventory](experiments/EXP-0001/extraction/REGISTER_TENSIONS.md) preserve symbolic transformations, quoted dialogue, uncertain voices and direct statements separately.

## Local reproducibility

```bash
python experiments/EXP-0001/prepare_source.py
python experiments/EXP-0001/validate_extraction.py
python experiments/EXP-0001/audit_review_decisions.py
python experiments/EXP-0001/current_metrics.py
python experiments/EXP-0001/open_review_worklist.py --top 12
python experiments/EXP-0001/audit_documentation_pins.py
python experiments/EXP-0001/build_B_draft.py --check
```

The [runbook](experiments/EXP-0001/RUNBOOK.md) and [current status](experiments/EXP-0001/STATUS.md) define the remaining review and release gates. The private contextual [review-packet generator](experiments/EXP-0001/make_review_packet.py) writes licensed source text **only outside the repository**. The draft B generator is not a means of approving B. Live model calls require signed-off manifests and explicit execution.
