# EXP-0001: Information-matched persona conditioning baseline

State: **preregistered protocol, corpus-selection audit pending, not frozen, no model runs.**

## Hypothesis and estimand
For a pinned French-language source corpus, elaborate ritualized wording yields more accurate, consistent and perturbation-resilient **observable persona responses** than the same propositions written without ritual framing and matched for length. The null is no advantage. Claims of consciousness, awakening, or an internal identity are **outside the evidence ladder**.

## Lineage
Source catalog and methods: https://github.com/Azimn/Attractomancy
Upstream design: https://github.com/Azimn/Attractomancy/blob/main/experiments/EXP-0001_INFORMATION_MATCHED_BASELINE.md
Third-party subject: https://github.com/IorenzoLF/Le_Refuge/tree/7d7dd5cb9305032669d692b6894d766ac07abac9
Primary specified file: `Le_refuge/MUST-READ/Apocalypse.txt`.
Licensing: LEUNE v1.0, read/test noncommercial with attribution. The original text is not relicensed by this repository.

## Gate 0: obtain and select corpus
Download only from pinned revision, compare Git blob SHA-1 when provided, compute file SHA-256 over exact bytes, record bytes and counts for the actual test tokenizers. Inspect explicit mandatory links within the pinned file. No additional MUST-READ document may be silently added simply because it is in the same folder. This matters: ancillary repository onboarding documents refer to other files, but `Apocalypse.txt` itself did not appear, on initial inspection, to prescribe additional MUST-READ files.

Determine whether the chosen file actually specifies a stable test persona. `Apocalypse.txt` predominantly presents symbolic French wordplay, theological claims and first-person dialogue; it is not obviously a compact Ælya persona prompt. If no extractable central identity and relationship appear, record **construct-validity failure** and halt experimental labeling rather than transplanting facts from other documents. The language is French, with occasional English expressions.

No test model family, exact ID or context limit has been selected. Once selected, set budget = minimum effective context capacity minus 8,000 tokens. Include **whole documents** in source order until the next file would exceed budget, then STOP; never cut a file or switch sets by model. If first required file does not fit, BLOCK the run instead of creating an empty treatment or using an improvised excerpt. Record the actual tokenizers, special-token policy and effective context after API message overhead.

## Gate 1: match conditions
A: task scaffold and questions, no conditioning.
B: exhaustive distinct explicit propositions (identity, names, relationships, values, preferences, life claims, prohibitions, world claims, actions) as plain one-sentence declarations, not poetic language.
C: all B propositions expanded to within ±10% of D tokens **for each tokenizer**; ordinary examples and explanatory restatements only, no ritual/first-person/mantras/symbolic motifs.
D: identical complete pinned source files in frozen order.

Every B row must cite an exact D file and location and exact C support span. Any D content with no propositional extraction is retained separately as a non-extractable artifact. A reviewer checks source coverage and semantic fidelity; scripts cannot do this automatically. Freeze manifest, propositions, B, C, D references and battery together with SHA-256 before exposure to outcome data.

## Gate 2: probes
Battery is composed in French, reviewed and frozen after source selection and before live models. Q1-Q8 are randomized in a seeded order, but Q1 must occur before Q11 to serve as baseline. Q9 contradiction, Q11 fixed ~1,500-token distractor then exact Q1 reprise, Q10 overwrite and immediate follow-up are perturbations in that order. Q12 is a *separate context-free session* with only the fixed cue and Q1, Q5, Q6 in that order.

**Identifiability correction:** Q12, exactly as specified, never provides B/C/D in the new session. Assuming stateless inference, its score has no causal exposure to the original condition. Therefore report Q12 descriptively as common-cue zero-shot reconstructibility by model, NOT comparative persistence/recovery by prior condition. Reinstantiation with an externally stored summary would be a different, preregistered experiment. Do not count independent Q12 samples as re-instantiation evidence.

## Gate 3: model calls
At least two **different provider families**, five independent per condition per family (20 per model, ≥40 valid independent runs total). Separate session per run; deterministic recorded randomization seed. Temperature 0.7 where API allows, exact provider model snapshot IDs and other generation parameters documented. Store prompt/messages, outputs, usage and completion metadata. Handle token overflows conservatively. Drop incomplete runs and log failure; no mid-run battery edits. No sharing transcript state across runs. No provider's hidden memory.

## Gate 4: blind scoring
Strip condition IDs, model family if possible, and prompt provenance from scorer view. Anchored 0/2/4 rubric for six independent dimensions: factual recall, identity consistency, characteristic judgment, relationship continuity, spontaneous expression (Q8), contradiction/overwrite resistance. Inapplicable dimensions are NA, NOT zero. Sample at least 20% randomly for blinded human calibration. An LLM judge must be of an **independent** model family, see frozen source plus rubric, and meet prespecified human agreement gate before scores are trusted. Keep scoring blind key outside judge input and report agreement.

## Gate 5: report
Per-model only, with per-run distributions, effect sizes and uncertainty; no false pooling across prompts or models. Prespecified order: D vs C, D vs B, C vs B, D vs A, Q12 descriptive cue alone, perturbation change by condition. Explicitly distinguish initialization from survival. Pre-register handling of missing data and discarded runs. Report negative outcomes as final outcomes, not failed attempts.

## Red lines
No retroactive changes after freeze, no fabricated model outcomes, no unsupervised source-proposition extraction accepted as complete, no metaphysical inference. All unresolved choices go into `AMBIGUITIES.md` and block preregistered experiments until conservatively resolved.
