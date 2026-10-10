# Independent review checkpoint and evidence requirements

**Current state: NO independent signoff exists.** Assistant editorial decisions are first-pass proposals, not a substitute for a second reviewer. An independent reviewer must check each proposed claim against the exact pinned source, including contradictions, language-switching, symbolic content, and context that could change speaker attribution.

To build a **private local review packet**, first run `prepare_source.py` and then, from the repository root, run:

```bash
python experiments/EXP-0001/make_review_packet.py --start 3001 --end 3125 --output /tmp/exp0001_3001_3125.jsonl
python experiments/EXP-0001/check_claim_overlap.py --details
python experiments/EXP-0001/audit_review_decisions.py
```

The packet includes source text and therefore MUST stay **outside the checkout** and must not be committed or redistributed. The script refuses an output location within the repository. Short snippets may be cited in audit decisions, but complete third-party source text stays with the original publisher.

Reviewers document one final classification for every one-indexed source line. The distinction between `unresolved` and `nonextractable_symbolic` is essential; unusual phonetic language alone does not establish non-extractability. Where two claims have overlapping citations, determine whether they are genuinely distinct or synonymous, retaining their supporting spans. Keep contradictory claims separate and note whether they share the same speaker. Human review must also verify that the discourse regime is stable enough to use as EXP-0001 target. If not, invoke the preregistered catalog source-escape process before any model run.

After all lines are adjudicated, `audit_review_decisions.py --strict` must pass with zero unresolved dispositions. Create `review_signoff.json` from the documented example, with the actual independent reviewer identity, UTC review date, source SHA-256, and the **current actual SHA-256** of both `propositions_draft.json` and `review_decisions.csv`. The signoff is a human attestation, not a verification of human identity by software. `validate_freeze.py` checks its digests and fields as a safeguard against stale or casually toggled approvals; a passing script cannot establish the semantic quality of the reviewer.

No one should manufacture approval to unlock the condition tests. C remains unavailable until B has exhaustive source coverage and source-faithful decisions. Q12 remains a by-model cue-only calibration.

The final `freeze.json` must include a `review_signoff_sha256` key matching the digest of the exact approved `review_signoff.json`. Approvals cannot be transferred between versions of the evidence register by changing a status field. The signoff file should be kept as part of the frozen methods evidence, without publishing the third-party full text in review packets.
