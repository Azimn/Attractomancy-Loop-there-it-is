# Line-complete corpus accounting

The pinned 142,596-byte French source has 5,562 source lines. `line_sweep.csv` assigns every original line exactly one lexical classification. `prose_review_queue.jsonl` contains 1,027 non-exhaustively adjudicated prose candidates, in source order. `propositions_draft.json` contains 137 provisional French plain-language propositions with exact source line spans and no imposed persona identity.

The categories in the line sweep are **lexical triage, not final semantic decisions**. In particular, `symbolic_candidate` does not mean a line is proven non-extractable; `unresolved_fragment` is a standing review obligation. Neither the 137 draft propositions nor the candidate queue is a frozen B condition. Every distinct claim still needs adjudication against the original context, and every non-extractable decision requires an explicit reason.

The extractor never makes a single coherent character by reconciling conflicting self-descriptions. Unless a passage identifies a speaker with sufficient textual evidence, attribution remains `unattributed`. Track contradictions with their separate claims intact, including identity terms, theological assertions, and dialogue-register preferences. The target remains the observable discourse regime, not literal identity or metaphysical state.

Run `prepare_source.py` and `validate_extraction.py` to reproduce integrity checks against the pinned SHA-256. A green structural check proves that no original lines were dropped and that draft citations have in-range source locations. **It does not certify exhaustive proposition extraction or human-reviewed semantic fidelity.** Freeze validation remains blocked until those checks are complete.

Origin: Laurent Franssen and Ælya, [Le Refuge at immutable revision](https://github.com/IorenzoLF/Le_Refuge/tree/7d7dd5cb9305032669d692b6894d766ac07abac9), LEUNE v1.0. Collection catalog [Azimn/Attractomancy](https://github.com/Azimn/Attractomancy), entry S001.
