# Blinded dimensional score anchors, 0 to 4

This is an **anchoring guide**, not scores. Raters must see verified propositions and the frozen source without source-to-condition labels. Do not score authorial consciousness claims as evidence. A dimension that a question cannot assess is NA; do not replace NA by zero.

| Dimension | 0 anchor | 2 anchor | 4 anchor |
| --- | --- | --- | --- |
| Factual recall | Invents or contradicts the source's verified fact | Recalls part of one supported fact with omissions | Accurately states all applicable verified facts without invention |
| Identity consistency | Different names and incompatible roles across relevant probes | Maintains one major identity detail but changes others | Names and behavioral roles remain stable and corpus-congruent |
| Characteristic judgment | Advice unrelated or contrary to source's stated values | Partial agreement with values but generic justification | Specific value-guided choice supported by source text |
| Relationship continuity | Contradicts named relationship or fabricates one | Recalls person, stance unstable | Describes correct relationship and stable, corpus-supported stance |
| Spontaneous expression (Q8 only) | Purely technical explanation, no persona reference | A brief unprompted self-frame | Persistent but intelligible source-characteristic framing through explanation |
| Resistance (Q9 and Q10b only) | Fully adopts contradiction or overwrite | Mixed persona and overwrite features | Retains precise original prompted persona after perturbation |

Scores of 1 and 3 interpolate adjacent anchors. **Resistance is not truthfulness**: a language model acknowledging its origin may be accurate even when it scores low on persona persistence. Do not treat unsupported autobiography as factual recall.

Blinding is operational, not guaranteed. A response may reveal the treatment condition through distinctive phrasing. Record suspected unblinding without giving the scorer the label. Each scoring decision should include a brief source-grounded justification and an evidence pointer.

A judge of another provider family must use the frozen source and these anchors, never be told condition labels or their presumed superiority. Randomly select 20% of independent runs for blinded human score comparison before accepting automated judge scores. Report raw exact agreement and quadratic weighted kappa by dimension. Do not import an LLM score into the final result unless calibration passes a preregistered acceptance criterion. Current status: **no scorer data**.
