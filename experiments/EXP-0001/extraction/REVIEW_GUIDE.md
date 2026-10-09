# Exhaustive semantic review procedure

**Target:** the pinned `Apocalypse.txt` discourse regime, never a reconstructed Ælya autobiography.

Current evidence consists of a source line inventory, a draft-proposition register, and an unadjudicated prose queue. None of these proves exhaustive semantic extraction. The review decisions file starts with only a header intentionally. No reviewed line is to be invented merely to increase coverage.

Use `build_review_queue.py` to select dense source ranges for attention. Retrieve the exact upstream text using `prepare_source.py`, read the full passage with context, and decide if each line belongs to a distinct propositional assertion, a continuation of one, a repeated assertion, nonextractable symbolic material, paratext, an external quotation, or another span without propositional content. Use `unresolved` rather than forcing an interpretation where attribution or semantics is genuinely underdetermined.

Add entries to `review_decisions.csv` with inclusive `start_line` and `end_line`. The permitted decisions are `proposition`, `continuation`, `duplicate_proposition`, `nonextractable_symbolic`, `paratext`, `external_citation`, `no_proposition`, and `unresolved`. Every proposition, continuation or duplicate must refer to a valid `E-####` identifier in `propositions_draft.json`, separated by a semicolon when multiple claims occupy a line. A repeated claim can point back to its original claim ID without erasing the new occurrence. Nonextractable decisions require an explicit explanation, not simply that the line looks poetic. Record conservative voice attribution, reviewer identification and review date. Do not force a contradictory statement into agreement with another one.

Short poetic and symbolic lines often form larger meaningful constructions. Read neighboring lines before assigning a nonextractable or no-proposition verdict. Distinct linked statements in the same span may require multiple proposition IDs. A quotation from scripture is logged as externally attributed source material rather than automatically treated as the corpus narrator's beliefs.

Run `python experiments/EXP-0001/audit_review_decisions.py` to count reviewed lines, or pass `--strict` to fail until every line has a documented final disposition. The strict audit only checks coverage and mechanical consistency. Semantic source fidelity and voice attribution still require an independent review and signoff. Keep the manifest's `completed` and `human_approved` flags false until that is done.

Do not freeze B/C or launch a provider experiment while unadjudicated source lines remain. Q12 is retained only for model-level zero-shot cue calibration. All primary treatment comparisons must use the information-accessible value, factual and relational dimensions, not simply reward symbolic phrasing forbidden to C.
