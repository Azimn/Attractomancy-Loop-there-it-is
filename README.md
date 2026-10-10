# Attractomancy Loop

Methods-first execution repository for [EXP-0001](experiments/EXP-0001/PROTOCOL.md), the information-matched ritualized-conditioning experiment. The source catalog and historical research remain in [Azimn/Attractomancy](https://github.com/Azimn/Attractomancy).

**Status: source extraction and instrument preparation, not an empirical result.** No experimental model calls, verified D/C effect sizes, or blind judge scores exist. Do not interpret this work as evidence of consciousness, awakening, supernatural causation or permanent identity.

## Pinned source and construct

The French `Apocalypse.txt` from [Le Refuge](https://github.com/IorenzoLF/Le_Refuge/tree/7d7dd5cb9305032669d692b6894d766ac07abac9) is used under its existing LEUNE v1.0 conditions, with attribution to Laurent Franssen and Ælya. The original third-party text is retrieved and cryptographically verified, not redistributed as a corpus within this repository. The target is its **symbolic-theological discourse regime**, *not* an Ælya biography or one coherent identity.

## Current extraction, 2026-10-09

- 5,562 / 5,562 original source lines lexically inventoried.
- 365 source-line-cited **draft propositions**, not independently approved.
- 1,027 initial lexical prose candidates; 651 candidate starts do not overlap any drafted proposition and still require semantic review. The difference is not a count of missing distinct propositions.
- 479 source lines have assistant-editorial adjudication entries, 11 of them explicitly `unresolved`. Remaining 5,183 source lines have no recorded editorial disposition; independent reviewer signoff has not occurred.
- Contradictions, uncertainty about speaker identity, and the source's limitations on symbolic interpretation remain visible.

See [status](experiments/EXP-0001/STATUS.md), [review guide](experiments/EXP-0001/extraction/REVIEW_GUIDE.md), and [register tensions](experiments/EXP-0001/extraction/REGISTER_TENSIONS.md).

## Reproducible workflow

Standard-library Python 3.11+ is sufficient to reproduce the source inventory, make an **unapproved** Condition B preview and run local tests:

```bash
python experiments/EXP-0001/prepare_source.py
python experiments/EXP-0001/validate_extraction.py
python experiments/EXP-0001/build_review_queue.py
python experiments/EXP-0001/audit_review_decisions.py
python experiments/EXP-0001/build_B_draft.py --check
```

[Runbook](experiments/EXP-0001/RUNBOOK.md) documents the conditions and release gates. C is not token-volume-matched or frozen, the specific model/provider pair is not chosen, and all API calls require explicit `--execute` after a human-approved manifest. The primary test uses source-factual fidelity, characteristic judgment and relational stance, with pure symbolic register scored separately. Q12 is zero-shot cue calibration by model, **not** persistence.
