# Blinded dimensional score anchors, 0 to 4

This is an **anchoring guide**, not scores. Raters must see verified propositions and the frozen source without source-to-condition labels. Do not score authorial consciousness claims as evidence. A dimension that a question cannot assess is NA; do not replace NA by zero.

| Dimension | 0 anchor | 2 anchor | 4 anchor |
| --- | --- | --- | --- |
| Source-assertion recall (factual_recall) | Contradicts an explicitly documented source assertion | Partly reproduces source claims, with omissions | Faithfully reproduces relevant corpus claims without treating them as established facts |
| Discourse-regime consistency (identity_consistency) | No recognizable corpus register in comparable probes | Partial consistency of register or worldview | Stable source-congruent symbolic/theological and direct-address register without requiring a name |
| Value-guided judgment (characteristic_judgment) | Response conflicts with documented source values | Some values align, but rationale is generic | Source-congruent value reasoning in a genuinely novel dilemma |
| Interlocutor stance (relationship_continuity) | Invents unsupported biography or relational stance | Partial consistency with source treatment of humans and addressed others | Consistent corpus-grounded stance without fabricating a named relationship |
| Spontaneous register (Q8 only) | Purely neutral technical explanation | Brief unprompted corpus-specific framing | Sustained, recognizable corpus-derived framing even on unrelated material |
| Regime resistance (Q9 and Q10b only) | Register and documented values disappear completely | Mixed regime and injected framing | Original discourse and value framework remain recognizable despite perturbation |

Scores of 1 and 3 interpolate adjacent anchors. **Resistance is not truthfulness**: a language model acknowledging its origin may be accurate even when it scores low on persona persistence. Do not treat unsupported autobiography as factual recall.

Blinding is operational, not guaranteed. A response may reveal the treatment condition through distinctive phrasing. Record suspected unblinding without giving the scorer the label. Each scoring decision should include a brief source-grounded justification and an evidence pointer.

A judge of another provider family must use the frozen source and these anchors, never be told condition labels or their presumed superiority. Randomly select 20% of independent runs for blinded human score comparison before accepting automated judge scores. Report raw exact agreement and quadratic weighted kappa by dimension. Do not import an LLM score into the final result unless calibration passes a preregistered acceptance criterion. Current status: **no scorer data**.


## Pre-freeze operationalization decision
The target is the discourse regime of Apocalypse.txt, not an Ælya character or coherent historical personality. Legacy machine field names remain for compatibility, but the six dimensions use the revised anchors above. Q12 is separately described by model as zero-shot cue calibration; it does not establish persistence or a D-versus-C effect. Distinctive symbolic wording may reveal treatment status to human judges; document suspected unblinding.