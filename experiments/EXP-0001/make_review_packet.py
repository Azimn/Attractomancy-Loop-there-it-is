#!/usr/bin/env python3
"""Build a local, contextual human-review packet from exact pinned source bytes.

Never commit generated packets: they contain third-party Le Refuge text.
This is an inspection aid, not an extractor or a semantic signoff.
"""
import argparse
import collections
import csv
import hashlib
import json
import pathlib
import sys

ROOT=pathlib.Path(__file__).resolve().parent
HASH="d49b3a98dfc50b1cc2066214976dbeda48771cd8162a084662cbde9239e07ff5"

def make_packet(root, source, start, end, context=2):
    contents=source.read_bytes()
    if hashlib.sha256(contents).hexdigest()!=HASH:
        raise ValueError("Source bytes do not match pinned reference")
    lines=contents.decode("utf-8").split("\n")
    if not 1<=start<=end<=len(lines):
        raise ValueError("Invalid review range")
    props=json.loads((root/"extraction/propositions_draft.json").read_text(encoding="utf-8"))["propositions"]
    by_line=collections.defaultdict(list)
    by_id={p["id"]:p for p in props}
    for p in props:
        for n in range(p["d_line_start"],p["d_line_end"]+1):
            by_line[n].append(p["id"])
    with (root/"extraction/review_decisions.csv").open(encoding="utf-8",newline="") as f:
        decisions=list(csv.DictReader(f))
    directly_reviewed_claim_ids={id for row in decisions if row["decision"] in ("proposition","continuation")
                                 for id in row["proposition_ids"].split(";") if id}
    lookup={}
    for row in decisions:
        for n in range(int(row["start_line"]),int(row["end_line"])+1):
            if n in lookup:raise ValueError("Overlapping reviews")
            lookup[n]=row
    with (root/"extraction/line_sweep.csv").open(encoding="utf-8",newline="") as f:
        triage=list(csv.DictReader(f))
    if len(triage)!=len(lines):
        raise ValueError("Inventory not aligned with source")
    packet=[]
    for n in range(start,end+1):
        row=lookup.get(n)
        linked_claims=[by_id[id] for id in by_line[n]]
        pending_claims=[p["id"] for p in linked_claims if p["id"] not in directly_reviewed_claim_ids]
        packet.append({
            "source_line":n, "literal_line":lines[n-1],
            "context_before":[{"source_line":i,"text":lines[i-1]}
                              for i in range(max(1,n-context),n)],
            "context_after":[{"source_line":i,"text":lines[i-1]}
                             for i in range(n+1,min(len(lines),n+context)+1)],
            "lexical_class":triage[n-1]["classification"],
            "proposition_ids":by_line[n],
            "draft_claims":[{"id":p["id"],"sentence_fr":p["sentence_fr"],
                "source_lines":[p["d_line_start"],p["d_line_end"]],
                "source_form":p.get("source_form","not_yet_coded"),
                "contradiction_group":p.get("contradiction_group"),
                "review_status":p["review_status"]} for p in linked_claims],
            "claim_ids_missing_direct_editorial_decision":pending_claims,
            "editorial_decision":row["decision"] if row else None,
            "editorial_reason":row["reason"] if row else None,
            "human_approved":False,
            "requires_review":row is None or row["decision"]=="unresolved" or bool(pending_claims),
        })
    return packet

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--start",type=int,required=True)
    p.add_argument("--end",type=int,required=True)
    p.add_argument("--context",type=int,default=2)
    p.add_argument("--source",default=str(ROOT/"_upstream_cache/Apocalypse.txt"))
    p.add_argument("--output",required=True)
    a=p.parse_args()
    if not 0<=a.context<=10:raise ValueError("Context radius must be between 0 and 10 lines")
    out=pathlib.Path(a.output)
    if out.resolve().is_relative_to(ROOT.parent.parent.resolve()):
        # Source text is LEUNE-licensed and must not be mirrored in the repo.
        raise ValueError("Use an output location outside the checked-out experiment directory")
    packet=make_packet(ROOT,pathlib.Path(a.source),a.start,a.end,a.context)
    out.parent.mkdir(parents=True,exist_ok=True)
    with out.open("w",encoding="utf-8") as handle:
        for row in packet:handle.write(json.dumps(row,ensure_ascii=False)+"\n")
    print(json.dumps({"status":"PRIVATE_REVIEW_ONLY","lines":len(packet),
         "open_or_unresolved":sum(x["requires_review"] for x in packet),
         "output":str(out)},indent=2))

if __name__=="__main__":
    try:main()
    except (OSError,ValueError,KeyError) as e:
        print("REVIEW PACKET BLOCKED:",e,file=sys.stderr);sys.exit(2)
