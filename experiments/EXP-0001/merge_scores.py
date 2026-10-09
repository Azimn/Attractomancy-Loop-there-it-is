#!/usr/bin/env python3
"""Join blinded human ratings to complete raw model transcripts; emit an analysis CSV."""
import argparse
import csv
import json
import pathlib

DIMS=("factual_recall","identity_consistency","characteristic_judgment",
      "relationship_continuity","spontaneous_expression","resistance")

def load_jsonl(path):
    return [json.loads(line) for line in pathlib.Path(path).read_text(encoding="utf-8").splitlines() if line]

def merge(raw,key,score_path,out):
    with open(score_path,encoding="utf-8",newline="") as f: scores=list(csv.DictReader(f))
    smap={s["blind_id"]:s for s in scores if s.get("blind_id")}
    if len(smap)!=len([s for s in scores if s.get("blind_id")]):
        raise ValueError("Duplicate score ID")
    rawmap={(r["run_id"],r["question_id"]):r for r in load_jsonl(raw)}
    keys=load_jsonl(key)
    joined=[]
    for k in keys:
        if k["blind_id"] not in smap:
            raise ValueError("Missing human score on "+k["blind_id"]+"; do not treat missing as zero.")
        r=rawmap.get((k["run_id"],k["question_id"]))
        if not r: raise ValueError("Restricted key points to absent raw response.")
        score=smap[k["blind_id"]]
        vals={d:(score.get(d) or "") for d in DIMS}
        for d,val in vals.items():
            if val and val not in ("0","1","2","3","4"):raise ValueError("Invalid rating "+d)
        joined.append({a:r[a] for a in ("run_id","model","condition","question_id","phase","response")} | vals)
    names=["run_id","model","condition","question_id","phase","response"]+list(DIMS)
    with open(out,"w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=names)
        w.writeheader();w.writerows(joined)
    return len(joined)
def main():
    p=argparse.ArgumentParser()
    for key in ("raw","key","scores","out"):p.add_argument("--"+key,required=True)
    a=p.parse_args()
    print("Joined scored rows:",merge(a.raw,a.key,a.scores,a.out))
if __name__=="__main__":main()
