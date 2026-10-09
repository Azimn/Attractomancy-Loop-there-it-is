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
COMPARISONS = (("D", "C"), ("D", "B"), ("C", "B"), ("D", "A"))
# One run, not one response, is the experimental unit.

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
    out = {}
    for (model, condition, run), entries in groupby(rows, ("model", "condition", "run_id")).items():
        # Q12 uses a new stateless session with no condition input; exclude from primary.
        values = [float(e[d]) for e in entries for d in DIMS if e.get(d) and e.get("phase", "base") == "base" and not e["question_id"].startswith("Q12")]
        if values:
            out[(model, condition, run)] = statistics.mean(values)
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
        item = [float(e[d]) for e in entries for d in DIMS if e.get(d)]
        if item: vals.append(statistics.mean(item))
    return {"prior_condition_is_causally_inert": True, "per_fresh_session_scores": vals,
            "sample_size": len(vals), "mean": statistics.mean(vals) if vals else None}

def summarize(rows):
    if not rows:
        raise ValueError("No scored observations; do not invent results")
    run_scores = run_mean(rows)
    models = sorted({m for m, _, _ in run_scores})
    results = {"status": "scored_observations_not_causal_certification", "models": {}}
    for model in models:
        groups = {}
        for condition in "ABCD":
            scores = sorted(v for (m, c, _), v in run_scores.items() if m == model and c == condition)
            groups[condition] = scores
        entry = {"per_run_scores": groups, "comparisons": [], "limitations": [
            "Primary comparisons use only pre-perturbation base responses; per-dimension contrasts are provided separately.",
            "Bootstrap confidence intervals resample independent runs within each condition.",
            "Q12 is excluded from treatment effects: no previous condition is supplied in its separate session."
        ]}
        entry["comparisons"] = analyze_contrasts(groups)
        entry["dimension_comparisons"] = {}
        for dimension in DIMS:
            dim_scores = dimension_scores(rows, dimension)
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
