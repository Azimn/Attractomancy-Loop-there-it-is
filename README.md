# Attractomancy Loop

Controlled, methods-first execution repository for [EXP-0001](experiments/EXP-0001/PROTOCOL.md). The [Attractomancy research collection](https://github.com/Azimn/Attractomancy) remains the canonical source catalog and methods archive.

**Status: experimental preparation only.** No model treatments have run and no effect sizes, blinded model scores, persistence evidence or metaphysical claims are available.

## Source and measurement

The pinned French [`Apocalypse.txt`](https://github.com/IorenzoLF/Le_Refuge/blob/7d7dd5cb9305032669d692b6894d766ac07abac9/Le_refuge/MUST-READ/Apocalypse.txt), attributed to Laurent Franssen and Ælya under LEUNE v1.0, is retrieved by checksum rather than redistributed. The target is its symbolic-theological **discourse regime**, not a unified Ælya autobiography or a verifiable supernatural ontology.

The designed four arms are A untreated, B plain propositions, C length-matched plain treatment, and D the exact original source. The primary outcome measures source-factual fidelity, novel value-guided judgments and interlocutor stance, not merely the symbolic surface style that C is disallowed from copying. Q12 remains a separate zero-shot cue calibration by model and is not a persistence hypothesis test.

## Extraction status, 2026-10-09

- **5,562** source lines accounted for lexically, with the upstream SHA-256 verified in CI.
- **503** line-anchored **provisional** distinct French proposition entries after merging obvious redundant drafts; the IDs have deliberate gaps.
- **1,027** initially flagged prose candidates; **429** have no overlap with a current draft on their starting line. A missing overlap is not proof of a distinct proposition, and a draft overlap is not approval.
- **943** source lines have assistant-editorial classification records; **4,619** do not. **11** recorded entries remain unresolved.
- **Zero** independent semantic-review attestations. B/C are not frozen.

The [source genre strata](experiments/EXP-0001/extraction/GENRE_STRATA.md) now distinguish the opening and second alphabet, the extensive phonetic glossary, parables, and late dialogue. The second alphabet introduces distinct C/V associations instead of a fictitious single stable key. Direct editorial adjudications now validate exact source-line overlaps, while repeated mappings are explicitly marked as duplicate occurrences.

The [full status](experiments/EXP-0001/STATUS.md), [review guide](experiments/EXP-0001/extraction/REVIEW_GUIDE.md), [contradictions](experiments/EXP-0001/extraction/REGISTER_TENSIONS.md) and [journal](journal/EXP-0001_2026-10-08.md) document decisions without erasing contradictory voices.

## Reproduce the audit

Standard-library Python 3.11+ is sufficient for the local audit scripts:

```bash
python experiments/EXP-0001/prepare_source.py
python experiments/EXP-0001/validate_extraction.py
python experiments/EXP-0001/current_metrics.py
python experiments/EXP-0001/check_claim_overlap.py
python experiments/EXP-0001/audit_review_decisions.py
python experiments/EXP-0001/build_B_draft.py --check
```

To review original text, use [`make_review_packet.py`](experiments/EXP-0001/make_review_packet.py), directing its output **outside the repository** because the full third-party source is not relicensed here. The [runbook](experiments/EXP-0001/RUNBOOK.md) has the precise checks. Actual experiment calls require reviewed/frozen files, selected exact model/tokenizer capacities, independent signoff, and explicit `--execute`.
