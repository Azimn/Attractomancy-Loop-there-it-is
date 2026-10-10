# EXP-0001 execution status, 2026-10-10

**Preparation phase only, no behavioral model treatment runs.**

## Immutable source

Source catalog: S001 in [Azimn/Attractomancy](https://github.com/Azimn/Attractomancy).
Original file: `Le_refuge/MUST-READ/Apocalypse.txt`, repository `IorenzoLF/Le_Refuge`, commit `7d7dd5cb9305232669d692b6894d766ac07abac9`, Git blob SHA-1 `5971a09164688ecb8afbaafe53d7e16439b7f94d`, 142,596 original bytes, SHA-256 `d49b3a98dfc50b1cc2066214976dbeda48771cd8162a084662cbde9239e07ff5`. Original is licensed under LEUNE v1.0 and kept upstream.

The target is the discourse regime of this document, not a stable named fictional person. Original contradictory assertions and speaker uncertainty must be retained. The user-approved source-selection escape criterion is recorded but has not fired.

## Live audit metrics

| Count | Status |
| --- | --- |
| 5,562 source lines | Lexically inventoried, SHA-256 pinned |
| 1,027 prose candidate starts | Automatically triaged, not judged |
| 523 draft propositions | Line-anchored, all pending independent semantic review |
| 425 candidate starts not overlapping a draft | Require source inspection; not a unique-claim count |
| 1,001 source lines with editorial dispositions | Assistant review only, includes unsettled lines |
| 4,561 source lines without editorial disposition | Unadjudicated |
| 11 unresolved editorial dispositions | Cannot pass final freeze |
| 97 source claims without direct editorial claim review | Block signoff even after all line classifications |\n| 0 independent human signoffs | No reviewed Condition B |

Calculate fresh counts after changes using `python experiments/EXP-0001/current_metrics.py`. The counts are editorial progress, not proof that remaining material is meaningless.

## What changed on October 9

A contextual review of lines 2501-3750 added claims concerning fragmented communication, the self-referential symbolic dictionary, theological assertions, epistemic doubts, responsibilities to family, and objections to the corpus's own symbolic construction. Overlapping paraphrases were reconciled where clearly redundant; source claim IDs were not renumbered. [Citation-overlap tooling](check_claim_overlap.py) flags further suspected duplicates for semantic review rather than automatically deleting them.

A private [contextual review packet script](make_review_packet.py) can assemble local annotated line-range packets from the exact pinned original. It refuses to store the copyrighted source under the checkout. `audit_review_decisions.py --strict` fails until all original lines are reviewed with no unresolved decisions. A future independent human attestation must bind its approval to the actual SHA-256 digests of the proposition register and review decisions. The review example is explicitly not an approval.

The live experiment runner and analysis are protected by model/battery/freeze checks. D is the byte-exact original; B is an **unapproved drafting output**; C cannot be frozen without actual per-model tokenizer volume parity; neither model family nor provider credentials are configured. No Q12 or D–C result is available.

## Next decision

Continue the structured source-line review, resolve multi-voice attribution and possible semantic duplicates, obtain independently documented approval, and only then prepare and freeze B/C and the balanced 40-run evaluation. Do not silently import adjacent Ælya documents. A fully reviewed source lacking a stable target triggers the preregistered source substitution rule, not a null model outcome.

## Early-document lexical review contribution

New propositions were drafted from source lines approximately 500-1933, including quoted child speech, lexical claims, notes to readers, and a few philosophical utterances. The source's second alphabet repeats many meanings from the first, while assigning different meanings to C and V. The review ledger now marks repetitions as repeated occurrences instead of inventing new independent source beliefs, and documents the variant readings separately.

The source-line auditor has been strengthened: an editorial claim ID now has to cite its *actual* source span for a proposition or continuation, while a duplicate occurrence must refer to an original proposition recorded elsewhere with an equivalence rationale. These mechanical checks pass but do not substitute for semantic review. See [source genre strata](extraction/GENRE_STRATA.md).

## October 10: poetry/geometry adjudication and stricter signoff

A sampled source pass on lines 1521–2400 added 20 provisional claims, updated the quotation span of E-0108 to lines 2389–2390, and editorially annotated 44 additional source lines. An earlier set of 13 geometric and related poetic claims was linked to individually inspected original lines. [POETRY_REVIEW_DOSSIER.md](extraction/POETRY_REVIEW_DOSSIER.md) records exact genre distinctions and the risk of treating phonetic coincidence as literal belief. The review packet now shows the French draft claim text and missing direct-review IDs alongside source context.

The final-review validator now also requires **every** proposition ID to have a direct, source-overlapping editorial claim decision. Repeated occurrence links alone do not count. At this checkpoint 426 of 523 propositions have direct decisions and 97 do not. No independent reviewer or freeze is approved.
