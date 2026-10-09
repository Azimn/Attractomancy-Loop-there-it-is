#!/usr/bin/env python3
"""Stratified blinded human subset and human-vs-judge agreement, no label disclosure."""
import argparse
import csv
import json
import pathlib
import random
import statistics

DIMS = ("factual_recall","identity_consistency","characteristic_judgment",
        "relationship_continuity","spontaneous_expression","resistance")
GATE_KAPPA = 0.60

def csv_map(path):
    with open(path, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    data = {}
    for r in rows:
        if r.get("blind_id"):
            if r["blind_id"] in data: raise ValueError("Duplicate blind ID in " + str(path))
            data[r["blind_id"]] = r
    return data

def weighted_kappa(a,b):
    if len(a) != len(b) or not a: return None
    observed = sum((x-y)**2 for x,y in zip(a,b)) / len(a)
    ha = [a.count(i)/len(a) for i in range(5)]
    hb = [b.count(i)/len(b) for i in range(5)]
    expected = sum(ha[i]*hb[j]*(i-j)**2 for i in range(5) for j in range(5))
    if expected == 0: return 1.0 if observed == 0 else 0.0
    return 1 - observed/expected

def review_subset(key_rows, packet_rows, seed=20261008):
    # Five replicates per model x arm. One entire run per cell = stratified 20%.
    cells = {}
    for k in key_rows:
        cells.setdefault((k["model"], k["condition"]), set()).add(k["run_id"])
    rng = random.Random(seed)
    selected_runs = {rng.choice(sorted(runs)) for runs in cells.values()}
    identifiers = {k["blind_id"] for k in key_rows if k["run_id"] in selected_runs}
    return [r for r in packet_rows if r["blind_id"] in identifiers], len(selected_runs)

def compare(human, judge):
    report = {"dimensions":{}, "automated_judge_trusted": True}
    for d in DIMS:
        both=[(int(human[k][d]),int(judge[k][d])) for k in human.keys() & judge.keys()
              if human[k].get(d) and judge[k].get(d)]
        a=[x for x,y in both]
        b=[y for x,y in both]
        score=weighted_kappa(a,b)
        gate=score is not None and len(a)>=8 and score >= GATE_KAPPA
        report["dimensions"][d] = {"paired_ratings":len(a), "quadratic_weighted_kappa":score,
                                  "exact_agreement":sum(x==y for x,y in both)/len(both) if both else None,
                                  "gate_passed":gate}
        if score is not None and not gate: report["automated_judge_trusted"]=False
    if not any(v["gate_passed"] for v in report["dimensions"].values()):
        report["automated_judge_trusted"]=False
    return report

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--packet",required=True)
    p.add_argument("--restricted-key",required=True)
    p.add_argument("--output",required=True)
    p.add_argument("--human-csv")
    p.add_argument("--judge-csv")
    a=p.parse_args()
    packet=[json.loads(l) for l in pathlib.Path(a.packet).read_text(encoding="utf-8").splitlines() if l]
    key=[json.loads(l) for l in pathlib.Path(a.restricted_key).read_text(encoding="utf-8").splitlines() if l]
    selected,n=review_subset(key,packet)
    pathlib.Path(a.output).write_text("".join(json.dumps(x,ensure_ascii=False)+"\n" for x in selected),encoding="utf-8")
    print("Blinded review packet items:",len(selected),"selected run groups:",n)
    if a.human_csv and a.judge_csv:
        print(json.dumps(compare(csv_map(a.human_csv),csv_map(a.judge_csv)),indent=2))
        print("Judges must be another model family. This statistical audit cannot check judge provenance or unblinding.")
if __name__=="__main__":main()
