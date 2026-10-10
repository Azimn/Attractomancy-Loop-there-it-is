#!/usr/bin/env python3
"""Rank outstanding source review batches, without copying licensed source text.

Ranks lexical triage for *inspection*, not automatic semantic classification.
All original source lines still need a formal decision, including blank lines.
"""
import argparse
import collections
import csv
import json
import pathlib

ROOT=pathlib.Path(__file__).resolve().parent

def rank(lines, queued, decisions, propositions, width=100, limit=12):
    if width < 10 or limit < 1:
        raise ValueError("width must be >= 10 and limit >= 1")
    classes={int(x["line"]):x["classification"] for x in lines}
    if len(classes)!=len(lines) or sorted(classes)!=list(range(1,len(lines)+1)):
        raise ValueError("line sweep must index each original line exactly once")
    occupied={}
    for row in decisions:
        a,b=int(row["start_line"]),int(row["end_line"])
        if not 1<=a<=b<=len(lines):
            raise ValueError("review decision out of source range")
        for n in range(a,b+1):
            if n in occupied:
                raise ValueError("overlapping reviewer decisions")
            occupied[n]=row["decision"]
    cited=set()
    for p in propositions:
        cited.update(range(p["d_line_start"],p["d_line_end"]+1))
    queued_by_start=collections.defaultdict(list)
    for row in queued:
        queued_by_start[int(row["line"])].append(row["id"])
    buckets=[]
    for a in range(1,len(lines)+1,width):
        b=min(a+width-1,len(lines))
        open_lines=[n for n in range(a,b+1) if n not in occupied]
        disputed=[n for n in range(a,b+1) if occupied.get(n)=="unresolved"]
        prose=[n for n in open_lines if classes[n]=="prose_candidate"]
        unmatched=[n for n in open_lines if n in queued_by_start and n not in cited]
        symbolic=[n for n in open_lines if classes[n]=="symbolic_candidate"]
        opaque=[n for n in open_lines if classes[n]=="unresolved_fragment"]
        if not open_lines and not disputed:
            continue
        buckets.append({
            "start_line":a,"end_line":b,
            "unadjudicated_source_lines":len(open_lines),
            "explicitly_unresolved_lines":len(disputed),
            "unadjudicated_prose_lines":len(prose),
            "unadjudicated_queued_starts_without_draft":len(unmatched),
            "unadjudicated_symbolic_candidate_lines":len(symbolic),
            "unadjudicated_opaque_fragment_lines":len(opaque),
            "priority":"review_existing_unresolved" if disputed else "review_source_context",
            "source_text_included":False,
        })
    # Work through probable omitted meaning before mechanical sparse formatting.
    buckets.sort(key=lambda b:(-b["explicitly_unresolved_lines"],
                               -b["unadjudicated_queued_starts_without_draft"],
                               -b["unadjudicated_prose_lines"],
                               -b["unadjudicated_symbolic_candidate_lines"],
                               b["start_line"]))
    return {"status":"EDITORIAL_TRIAGE_NOT_SEMANTIC_APPROVAL",
            "batches_total":len(buckets),
            "unadjudicated_source_lines":len(lines)-len(occupied),
            "explicitly_unresolved_lines":sum(v=="unresolved" for v in occupied.values()),
            "batches":buckets[:limit]}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--width",type=int,default=100)
    p.add_argument("--top",type=int,default=12)
    p.add_argument("--out",help="Optional JSON metadata output (no source text)")
    args=p.parse_args()
    with (ROOT/"extraction/line_sweep.csv").open(encoding="utf-8",newline="") as f:
        lines=list(csv.DictReader(f))
    queued=[json.loads(s) for s in (ROOT/"extraction/prose_review_queue.jsonl").read_text(encoding="utf-8").splitlines() if s]
    with (ROOT/"extraction/review_decisions.csv").open(encoding="utf-8",newline="") as f:
        decisions=list(csv.DictReader(f))
    propositions=json.loads((ROOT/"extraction/propositions_draft.json").read_text(encoding="utf-8"))["propositions"]
    report=rank(lines,queued,decisions,propositions,args.width,args.top)
    result=json.dumps(report,ensure_ascii=False,indent=2)+"\n"
    if args.out:
        pathlib.Path(args.out).write_text(result,encoding="utf-8")
    print(result)

if __name__=="__main__":main()
