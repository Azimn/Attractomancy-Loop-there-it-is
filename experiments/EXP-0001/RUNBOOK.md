# Reproduction and release gates

**This is a runnable laboratory, not yet a completed experiment.** All commands are relative to the repository root and do not claim model access.

Source acquisition (standard library only):
```bash
python experiments/EXP-0001/prepare_source.py
```
Expect exactly 142596 bytes and SHA-256 `d49b3a98dfc50b1cc2066214976dbeda48771cd8162a084662cbde9239e07ff5`. That script is also run in CI. Its cache directory is intentionally untracked.

**Before the model stage:** assemble `frozen/A.txt`, `B.txt`, `C.txt`, `D.txt`, `propositions.json`, `coverage.json`, `non_extractable.json`, `battery.fr.json`, `distractor_script.fr.json`, and `model_config.json`. Do not reuse `battery.fr.template.json` without resolving source-specific substitutions. Each proposition must cite the source and C support; an independent human reviewer must approve completeness and semantic fidelity. D must be byte-identical to the included source file or exact joined source-file set. The original Le Refuge source remains under its LEUNE rights.

Use actual model tokenizer counts and confirm two different provider families both allow temperature 0.7. Anthropic models at or beyond some 4.7 releases reject non-default temperatures; these models cannot be silently tested under a different temperature. The smallest selected context must hold all whole documents with 8000 tokens reserved for prompts and outputs. Do not replace exact counts with character estimates.

After the reviewed freeze manifest `freeze.json` records SHA-256 of every required `frozen/` file, run:
```bash
python experiments/EXP-0001/validate_freeze.py
```
It fails closed if documents are absent, hashes changed, model families insufficient, token counts missing, or C is not within ±10% of D under each actual tokenizer. Source D may be produced locally from upstream and excluded from Git redistribution, provided its digest and immutable URL are committed.

**Only after that validation**, with independently supplied `OPENAI_API_KEY` and `ANTHROPIC_API_KEY`, run each of four conditions A/B/C/D per model. Example:
```bash
python experiments/EXP-0001/run_experiment.py --model EXACT_MODEL_ID --condition A --execute
```
The exact ID must occur in `model_config.json`. No cost-bearing call occurs without `--execute`. Five valid independent run slots are required per model/condition. To replace one *discarded* slot, specify `--run-index` and increment `--attempt`. Do not reuse a run ID. Preserve the raw responses and failed-run logs.

To generate a blinded human scoring packet:
```bash
python experiments/EXP-0001/export_scores.py --raw results/responses.jsonl --out review --salt LONG_PRIVATE_RANDOM_SALT
python experiments/EXP-0001/calibrate_scores.py --packet review/scoring_packet.jsonl --restricted-key review/restricted_key.jsonl --output review/human_20_percent.jsonl
```
The second command samples one of five independent runs per model/condition, exactly 20% of run groups when the design has 40 runs. Keep the restricted key out of judge-facing content.

Human-scored all-item CSV can be joined and analyzed as:
```bash
python experiments/EXP-0001/merge_scores.py --raw results/responses.jsonl --key review/restricted_key.jsonl --scores review/human_scores.csv --out results/scored.csv
python experiments/EXP-0001/analysis.py --scores results/scored.csv --out results/analysis.json
```
Use an independent-family automated judge only after comparison with blinded human scores, using `calibrate_scores.py --human-csv ... --judge-csv ...` and the anchored rubric. Judge identity, prompt, and agreement must be recorded. No judge is configured by default.

Results may be committed only after a complete audit of all cells, discard records, human/LLM scoring consistency, per-family reports, and journal entry. Record negative and null outcomes with equal prominence.

## Corpus review before any freeze

First reproduce the pinned source, full-line index and an auditable backlog:

```bash
python experiments/EXP-0001/prepare_source.py
python experiments/EXP-0001/validate_extraction.py
python experiments/EXP-0001/build_review_queue.py
python experiments/EXP-0001/audit_review_decisions.py
python experiments/EXP-0001/build_B_draft.py --check
```

For a **non-approved B preview only**, pass `--out local/B.preview.fr.txt` to `build_B_draft.py`. The script creates a text file and a matching `B.preview.fr.txt.provenance.json` sidecar in the local directory; the script deliberately refuses writes to `frozen/B.txt`. It does not transform the register into a reviewed fact list, does not produce C, and does not certify semantic completeness. Follow `extraction/REVIEW_GUIDE.md` to adjudicate the 5,562 lines and record source claims, source continuations, duplicate occurrences and justified non-extractable material. An independent reviewer must assess the finished extraction after the line-level ledger has passed `audit_review_decisions.py --strict`.

The **template** `battery.fr.template.json` has a descriptive object for Q11, but `frozen/battery.fr.json` must convert Q11 to a **plain string exactly equal to Q1**, not retain the template wrapper. Q10 remains an object with `overwrite` and `followup`. Q12 remains the fixed cue-only calibration object with the original French cue and Q1/Q5/Q6 sequence. The validator rejects discrepancies, and the runtime independently checks that Q11 repeats Q1. Actual per-model tokenizer counts for the three unrelated distractor prompts, under `model_config.json` key `distractor_script_input_tokens`, must fall between 1,350 and 1,650 tokens; this does not validate their semantic irrelevance, which requires manual review.

Raw runs have 18 turns, 3 of which are unscored distractor exchanges. The analysis requires **all 15 expected scored items** with unique IDs and correct phase labels per independent run; partial runs must not be passed off as complete observations. The primary comparison averages source-assertion fidelity, characteristic value-guided judgment and interlocutor stance at the run level. Surface mimicry and symbolic register remain secondary. Q12 fresh-context cue-only scores are descriptive by model and are not condition contrasts.
