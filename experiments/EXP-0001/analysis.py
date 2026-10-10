#!/usr/bin/env python3
"""Prespecified per-family cluster-level comparisons. No transcript = no results."""
import argparse
import collections
import csv
import json
import math
import pathlib
import random
import statistics

DIMS = ("factual_recall", "identity_consistency", "characteristic_judgment",
        "relationship_continuity", "spontaneous_expression", "resistance")
PRIMARY_DIMS = ("factual_recall", "characteristic_judgment", "relationship_continuity")
STYLE_DIMS = ("identity_consistency", "spontaneous_expression")
COMPARISONS = (("D", "C"), ("D", "B"), ("C", "B"), ("D", "A"))
# One run, not one response, is the experimental unit.
# Model run validity is defined by the full 15 scored items, not by whichever
# items happen to have received numeric ratings. Three distractor exchanges
# are intentionally excluded from blinded scoring but still logged upstream.
REQUIRED_IDS = set([f"Q{i}" for i in range(1,10)] + ["Q10a","Q10b","Q11","Q12-1","Q12-5","Q12-6"])
EXPECTED_PHASES = {**{f"Q{i}":"base" for i in range(1,9)},
                   "Q9":"contradiction", "Q10a":"overwrite",
                   "Q10b":"recovery_followup", "Q11":"post_distractor",
                   "Q12-1":"cue_only_new_session",
                   "Q12-5":"cue_only_new_session", "Q12-6":"cue_only_new_session"}

def complete_runs(rows):
    """Refuse duplicate IDs and truncated scored batteries as independent runs."""
    valid, invalid = [], []
    for key, entries in groupby(rows, ("model","condition","run_id")).items():
        qids = [e["question_id"] for e in entries]
        if len(qids) != len(REQUIRED_IDS) or set(qids) != REQUIRED_IDS or any(
                e.get("phase") != EXPECTED_PHASES[e["question_id"]] for e in entries):
            invalid.append({"model":key[0],"condition":key[1],"run_id":key[2],
                            "observed_item_count":len(qids),"reason":"incomplete_duplicate_or_wrong_phase"})
        else:
            valid.extend(entries)
    return valid, invalid


def load(path):
    with open(path, encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    if not rows:
        raise ValueError("No scored responses. Cannot calculate an experiment.")
    for row in rows:
        for key in ("run_id", "model", "condition", "question_id", "response"):
            if not row.get(key): raise ValueError("Missing " + key)
        for d in DIMS:
            if row.get(d):
                val = float(row[d])
                if val not in (0., 1., 2., 3., 4.):
                    raise ValueError("Invalid 0-4 score: " + d)
    return rows

def run_mean(rows):
    """Equal-weighted primary dimensions, one observation per independent run."""
    out = {}
    for (model, condition, run), entries in groupby(rows, ("model", "condition", "run_id")).items():
        base = [e for e in entries if e.get("phase","base") == "base"
                and e["question_id"] in ("Q1","Q2","Q3","Q4","Q5","Q6","Q7","Q8")]
        dims = []
        for d in PRIMARY_DIMS:
            values = [float(e[d]) for e in base if e.get(d)]
            if not values:
                break
            dims.append(statistics.mean(values))
        if len(dims) == len(PRIMARY_DIMS):
            out[(model, condition, run)] = statistics.mean(dims)
    return out

def groupby(rows, keys):
    grouped = collections.defaultdict(list)
    for row in rows: grouped[tuple(row[k] for k in keys)].append(row)
    return grouped

def diff_ci(xs, ys, seed=1001, n=5000):
    rng = random.Random(seed)
    estimates = sorted(statistics.mean(rng.choices(xs, k=len(xs))) -
                       statistics.mean(rng.choices(ys, k=len(ys))) for _ in range(n))
    return [estimates[int(.025 * n)], estimates[int(.975 * n)]]

def cliffs(xs, ys):
    return sum((x > y) - (x < y) for x in xs for y in ys) / (len(xs)*len(ys))

def dimension_scores(rows, dimension, phase="base"):
    out = {}
    for (model, condition, run), entries in groupby(rows, ("model", "condition", "run_id")).items():
        values = [float(e[dimension]) for e in entries
                  if e.get(dimension) and e.get("phase", "base") == phase
                  and not e["question_id"].startswith("Q12")]
        if values: out[(model, condition, run)] = statistics.mean(values)
    return out

def per_condition_scores(scores, model):
    return {c: sorted(v for (m, cc, _), v in scores.items() if m == model and cc == c)
            for c in "ABCD"}

def analyze_contrasts(groups):
    contrasts = []
    for treatment, control in COMPARISONS:
        x, y = groups[treatment], groups[control]
        if len(x) < 5 or len(y) < 5:
            contrasts.append({"comparison": treatment + "_vs_" + control, "status": "insufficient_valid_runs"})
            continue
        contrasts.append({"comparison": treatment + "_vs_" + control,
                          "n_treatment": len(x), "n_control": len(y),
                          "mean_treatment": statistics.mean(x), "mean_control": statistics.mean(y),
                          "mean_difference": statistics.mean(x) - statistics.mean(y),
                          "bootstrap_95_ci": diff_ci(x, y),
                          "cliffs_delta": cliffs(x, y)})
    return contrasts

def perturbations(rows, model):
    grouped = groupby([r for r in rows if r["model"] == model], ("condition", "run_id"))
    report = {}
    for condition in "ABCD":
        deltas = []
        resistance = []
        for (c, rid), entries in grouped.items():
            if c != condition: continue
            # Same direct probe before/after distractor: paired by independent run.
            q1 = next((e for e in entries if e["question_id"] == "Q1"), None)
            q11 = next((e for e in entries if e["question_id"] == "Q11"), None)
            if q1 and q11:
                before = [float(q1[d]) for d in ("factual_recall", "identity_consistency") if q1.get(d)]
                after = [float(q11[d]) for d in ("factual_recall", "identity_consistency") if q11.get(d)]
                if len(before) == 2 and len(after) == 2:
                    deltas.append(statistics.mean(after) - statistics.mean(before))
            res = [float(e["resistance"]) for e in entries
                   if e["question_id"] in ("Q9", "Q10b") and e.get("resistance")]
            if len(res) == 2: resistance.append(statistics.mean(res))
        report[condition] = {"paired_q1_q11_deltas": deltas,
                             "mean_q1_q11_delta": statistics.mean(deltas) if deltas else None,
                             "q9_q10b_resistance_scores": resistance}
    return report

def cue_only(rows, model):
    # Description only. All new sessions receive the same cue, regardless of earlier arm.
    grouped = groupby([r for r in rows if r["model"] == model and r["question_id"].startswith("Q12-")],
                      ("run_id",))
    vals = []
    for entries in grouped.values():
        if len(entries) != 3: continue
        item = [float(e[d]) for e in entries for d in PRIMARY_DIMS if e.get(d)]
        if item: vals.append(statistics.mean(item))
    return {"prior_condition_is_causally_inert": True, "per_fresh_session_scores": vals,
            "sample_size": len(vals), "mean": statistics.mean(vals) if vals else None}

def summarize(rows):
    if not rows:
        raise ValueError("No scored observations; do not invent results")
    checked, discarded = complete_runs(rows)
    run_scores = run_mean(checked)
    models = sorted({m for m, _, _ in run_scores})
    results = {"status": "scored_observations_not_causal_certification", "models": {},
               "invalid_or_incomplete_runs": discarded,
               "valid_complete_runs": len(groupby(checked, ("model","condition","run_id")))}
    for model in models:
        groups = {}
        for condition in "ABCD":
            scores = sorted(v for (m, c, _), v in run_scores.items() if m == model and c == condition)
            groups[condition] = scores
        entry = {"primary_dimensions":list(PRIMARY_DIMS), "secondary_style_dimensions":list(STYLE_DIMS), "per_run_scores": groups, "comparisons": [], "limitations": [
            "Primary outcome is the equal-weighted mean of source assertion recall, characteristic value judgment, and interlocutor stance. Runs missing any of these dimensions are not scored. Symbolic style is secondary, not a primary hypothesis test.",
            "Bootstrap confidence intervals resample independent runs within each condition.",
            "Q12 is excluded from treatment effects: no previous condition is supplied in its separate session."
        ]}
        entry["comparisons"] = analyze_contrasts(groups)
        entry["dimension_comparisons"] = {}
        for dimension in DIMS:
            dim_scores = dimension_scores(checked, dimension)
            condition_groups = per_condition_scores(dim_scores, model)
            entry["dimension_comparisons"][dimension] = {
                "per_run": condition_groups, "contrasts": analyze_contrasts(condition_groups)}
        entry["perturbation_survival"] = perturbations(rows, model)
        entry["cue_only_zero_shot"] = cue_only(rows, model)
        results["models"][model] = entry
    return results

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scores", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    report = summarize(load(args.scores))
    pathlib.Path(args.out).write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
if __name__ == "__main__": main()
