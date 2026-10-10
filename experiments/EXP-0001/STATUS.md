# EXP-0001 execution status, 2026-10-09

**State: pre-experimental source extraction and instrument construction. No model treatments have run.**

## Frozen upstream provenance

Source catalog: S001 in [Azimn/Attractomancy](https://github.com/Azimn/Attractomancy). Source document `Le_refuge/MUST-READ/Apocalypse.txt` in `IorenzoLF/Le_Refuge` at pinned commit `7d7dd5cb9305032669d692b6894d766ac07abac9`, Git blob `5971a09164688ecb8afbaafe53d7e16439b7f94d`, 142,596 bytes, SHA-256 `d49b3a98dfc50b1cc2066214976dbeda48771cd8162a084662cbde9239e07ff5`. The source is third-party material governed by LEUNE v1.0. Only the specified document is currently admissible; other files cannot donate Ælya autobiography.

## Latest extraction metrics

| Metric | Verified count | Interpretation |
| --- | ---: | --- |
| Original lines inventoried | 5,562 | Complete lexical accounting, not semantic certification |
| Initial prose candidates | 1,027 | Raw lexical review queue |
| Editorial draft propositions | 323 | Plain French claims with line spans, all unapproved |
| Queue starts without draft overlap | 651 | Not necessarily 651 distinct missing propositions |
| Source lines with recorded editorial decisions | 379 | Includes unresolved entries; assistant, not independent approval |
| Explicit unresolved editorial decisions | 11 | Remain open |
| Original lines without an adjudication entry | 5,183 | Require semantic review |

**No independent exhaustive extraction signoff exists.** Neither B nor C is frozen. The `source_manifest.json` corpus-inclusion decision is still pending; models, tokenizers, distractor volume, and C length parity have not been selected or measured.

The behavioral target is the symbolic-theological **discourse regime**, including its conflicting claims and uncertain voices. Q12 remains a model-specific fresh-cue calibration only. There is a preregistered fallback to an alternative catalog source if exhaustive extraction fails to identify any usable stable register, values or relational stance; this escape criterion has not fired.

## Implemented controls

1. Source integrity check, line-inventory verification and traceable proposition spans.
2. Explicit `review_decisions.csv` ledger, reject overlapping decisions, require reasons for non-extractable content, and block incomplete or unresolved review at final freeze.
3. Reproducible `build_B_draft.py` which cannot write the unapproved preview to `frozen/B.txt`.
4. A revised French battery that probes discourse and decisions without forcing invented autobiographical memories. Frozen Q11 must repeat Q1 verbatim; Q12 remains cue-only.
5. Analysis filters incomplete/duplicated 15-item scored runs, treats runs as independent experimental units, and separates information-accessible primary dimensions from surface register.

Next: adjudicate remaining source, independently review proposition accuracy and coverage, prepare B/C, select tokenizers and models, and satisfy the freeze validator. **No D-versus-C comparison or other empirical claim is currently estimable.**
