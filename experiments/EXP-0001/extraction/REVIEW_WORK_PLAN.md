# Prioritized open source review worklist

EXP-0001 remains **unfrozen**. The initial backlog of draft propositions without direct editorial evidence was addressed on October 10, 2026: all 523 provisional claims now have direct, complete-span assistant-editorial source citations. That resolves **one evidence-integrity problem**, not the independently verified semantic extraction.

Use `python experiments/EXP-0001/open_review_worklist.py --width 100 --top 12` to prioritize further source inspection. This ranks explicitly unresolved reviewer decisions first, then unmatched prose-candidate starting lines, then open prose and symbolic lines, without reproducing the third-party text. Inspect each batch using `make_review_packet.py` with an output path outside the repository. Do not automatically assign dispositions based on lexical scores; snippets, homophones and quotation contexts can change their meaning.

Before source freeze, still required:

- All 5,562 original lines must have source-grounded, complete dispositions with no `unresolved` classification.
- Every currently drafted proposition must retain direct source-span review, and actual independent human semantic assessment must inspect all of them.
- Source-specific contradictions and attribution uncertainty must not be harmonized to make B more coherent.
- B and C must be human-approved, and the actual tokenizer length parity, D bytes, battery and model manifests must pass verification.

The worklist numbers **do not measure experimental success** and the ordering algorithm must not be used as evidence for non-extractability.
