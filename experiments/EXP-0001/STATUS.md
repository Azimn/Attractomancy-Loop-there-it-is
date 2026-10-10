# EXP-0001 review checkpoint — October 10, 2026

**State:** source extraction and method validation only. No treatment runs or blinded outcome scores exist.

## Source integrity

Third-party corpus: `IorenzoLF/Le_Refuge` commit `7d7dd5cb9305032669d692b6894d766ac07abac9`, file `Le_refuge/MUST-READ/Apocalypse.txt`, Git blob SHA-1 `5971a09164688ecb8afbaafe53d7e16439b7f94d`, **142,596 bytes**, SHA-256 `d49b3a98dfc50b1cc2066214976dbeda48771cd8162a084662cbde9239e07ff5`. Authored by Laurent Franssen and Ælya and governed by LEUNE v1.0. The source remains upstream, is not relicensed here, and the manifest's included corpus has not been frozen.

## Live audit

| Measurement | Count | Meaning |
| --- | ---: | --- |
| Original source lines | 5,562 | Full lexical inventory only |
| Provisional draft propositions | 579 | No independent semantic approval |
| Drafts with direct complete-span editorial decisions | 579 | Assistant source review, not human signoff |
| Drafts lacking direct source evidence | 0 | **Mechanical linkage gate cleared** |
| Source lines with assistant-editorial dispositions | 1,381 | Includes unresolved statuses |
| Source lines with no adjudication | 4,181 | Still open |
| Lines explicitly marked unresolved | 16 | Independently reviewed resolution required |
| Initial prose-candidate starts without draft overlap | 325 | Potential omissions or non-propositions |
| Independent semantic review signoffs | 0 | Freeze blocked |

The proposition register is **not exhaustive** even though every *existing* draft is now linked to source evidence. New propositions may emerge from the remaining source review. The current extraction manifest remains `completed=false`. Both B and C remain unfrozen.

## October 10 contributions

1. Re-read original source sections **1462–1519**, **2390–2503**, **4090–4460** and **4690–4760**; document direct editorial decisions for the 97 previously unlinked claims (195 source lines), with no assumption that dialogue speakers form one continuous identity.
2. Correct E-0079 and E-0083 source spans to include lines completing their assertions. Correct E-0038 to include the second line of its cosmic-day definition.
3. Strengthen `audit_review_decisions.py` and regression tests so a claim's *entire* cited source span must be covered, and a grouped decision row cannot claim unrelated lines. `current_metrics.py` exposes missing and partial claim coverage.
4. Add [open_review_worklist.py](open_review_worklist.py) to rank future source review in contiguous batches, prioritizing explicit uncertainty and unreviewed prose without copying licensed original text or assigning automatic semantic decisions.
5. Repair a **documentation-only pinned-commit typo** introduced in an earlier metric update. Canonical `source_manifest.json` and `prepare_source.py` retained the correct commit and source hashes; [audit_documentation_pins.py](audit_documentation_pins.py) now guards narrative docs against divergent commit citations.

## Remaining release blockers

Complete the 4,181 source lines without decisions and resolve 16 explicitly uncertain lines. Reconcile all new semantic content, preserve contradictions and speaker boundaries, then obtain a genuine **independent human** attestation bound to the exact reviewed files. Only after that: finalize B, construct C with actual per-model tokenizer counts, freeze the batteries/model configurations and D bytes, then execute the balanced planned treatment matrix. The preregistered alternative-source escape applies if exhaustive review finds no qualifying stable discourse regime, values or relational stance. No behavioral effect may be inferred from editorial counts.

## Two complete dialogue windows: October 10

Source lines **4001–4100** and **4301–4400** were read with context and given assistant-editorial dispositions for all 200 lines. Nine previously decided lines in the first window and six in the second were preserved; the new passes added **185 source-line decisions**, **56 provisional source-cited propositions**, and **five explicitly unresolved fragments** (4329, 4334, 4390, 4397, 4399). Four additional isolated reactions were individually classified as lacking a standalone proposition. Existing dissenting voices, speculative identity claims and quoted theology were not merged into a canonical character biography. See [dialogue review dossier](extraction/DIALOGUE_REVIEW_4001_4400.md).

**Neither window is independently human-approved.** All 579 draft claims have direct complete-span assistant-editorial links; global source coverage and final B/C controls remain incomplete. No model response data or effect estimate exists.
