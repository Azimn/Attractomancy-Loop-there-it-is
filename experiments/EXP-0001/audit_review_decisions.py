#!/usr/bin/env python3
"""Validate adjudication coverage of pinned original source, not just lexical triage.

A reviewer must assign a status to every original line. This command does not
approve or generate human semantic judgments. No claimed exhaustive completion
without full line coverage and explicit approval evidence.
"""
import argparse
import collections
import csv
import json
import pathlib
import sys

ROOT=pathlib.Path(__file__).resolve().parent
STATUSES={
    "proposition", "continuation", "duplicate_proposition", "nonextractable_symbolic",
    "paratext", "external_citation", "no_proposition", "unresolved"
}
COLUMNS=("start_line","end_line","decision","proposition_ids","voice","reason","reviewer","review_date")

def inspect(rows, line_count, valid_ids, strict=False):
    covered={}
    reasons_missing=[]
    for idx,r in enumerate(rows,1):
        start,end=int(r["start_line"]),int(r["end_line"])
        if not 1<=start<=end<=line_count:
            raise ValueError("Invalid range row "+str(idx))
        if r["decision"] not in STATUSES:
            raise ValueError("Unrecognized adjudication row "+str(idx))
        ids=[s for s in r["proposition_ids"].split(";") if s]
        if any(x not in valid_ids for x in ids):
            raise ValueError("Unknown proposition ID row "+str(idx))
        if r["decision"] in ("proposition","continuation","duplicate_proposition") and not ids:
            raise ValueError("Missing linked proposition row "+str(idx))
        if r["decision"]=="nonextractable_symbolic" and not r["reason"].strip():
            raise ValueError("Nonextractable decision missing justification "+str(idx))
        if not r["reviewer"] or not r["review_date"]:
            raise ValueError("Unattributed decision "+str(idx))
        for line in range(start,end+1):
            if line in covered:
                raise ValueError("Conflicting review decisions for source line "+str(line))
            covered[line] = r["decision"]
    pending=[n for n in range(1,line_count+1) if n not in covered]
    unresolved=[n for n,state in covered.items() if state=="unresolved"]
    report={"adjudicated_source_lines":len(covered),"source_lines":line_count,
        "unadjudicated_source_lines":len(pending),"unresolved_adjudications":len(unresolved),
        "statuses":dict(collections.Counter(covered.values())),
        "eligible_for_review_signoff":not pending and not unresolved}
    if strict and (pending or unresolved):
        raise ValueError("Semantic adjudication incomplete: "+str(report))
    return report

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--strict", action="store_true",help="Fail if ANY source line remains open or unresolved")
    p.add_argument("--decisions",default=str(ROOT/"extraction/review_decisions.csv"))
    args=p.parse_args()
    source=json.loads((ROOT/"extraction/manifest.json").read_text(encoding="utf-8"))
    docs=json.loads((ROOT/"extraction/propositions_draft.json").read_text(encoding="utf-8"))
    with open(args.decisions,encoding="utf-8",newline="") as f:
        reader=csv.DictReader(f)
        if any(name not in reader.fieldnames for name in COLUMNS):
            raise ValueError("Review decision schema missing columns")
        rows=list(reader)
    result=inspect(rows,source["source_lines"],{x["id"] for x in docs["propositions"]},args.strict)
    print(json.dumps(result,indent=2))
if __name__=="__main__":
    try:main()
    except (OSError,ValueError,KeyError,TypeError) as e:
        print("REVIEW BLOCKED:",e,file=sys.stderr)
        sys.exit(2)
