#!/usr/bin/env python3
"""Generate an auditable editorial review queue from pinned source-line evidence.

A line overlapped by a draft proposition is NOT semantically approved.
All extracted, symbolic and unresolved source lines still need explicit review.
No third-party source content is copied into the generated report.
"""
import argparse
import collections
import csv
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
SIZE = 250

def analyze(root=ROOT):
    with (root / "extraction/line_sweep.csv").open(encoding="utf-8", newline="") as handle:
        lines = list(csv.DictReader(handle))
    entries = [json.loads(s) for s in
               (root / "extraction/prose_review_queue.jsonl").read_text(encoding="utf-8").splitlines() if s]
    draft = json.loads((root / "extraction/propositions_draft.json").read_text(encoding="utf-8"))["propositions"]
    manifest = json.loads((root / "extraction/manifest.json").read_text(encoding="utf-8"))
    referenced = collections.defaultdict(list)
    for prop in draft:
        for n in range(prop["d_line_start"], prop["d_line_end"] + 1):
            referenced[n].append(prop["id"])
    candidate_start = {entry["line"] for entry in entries}
    if len(lines) != manifest["source_lines"] or len(entries) != manifest["queue_count"]:
        raise ValueError("Review queue is inconsistent with extraction manifest")
    bands = []
    for start in range(1, len(lines) + 1, SIZE):
        end = min(start + SIZE - 1, len(lines))
        window = [row for row in lines if start <= int(row["line"]) <= end]
        candidates = [int(r["line"]) for r in entries if start <= int(r["line"]) <= end]
        covered = [n for n in candidates if referenced[n]]
        status_counts = collections.Counter(row["classification"] for row in window)
        bands.append({
            "start_line": start, "end_line": end,
            "candidate_prose_lines": len(candidates),
            "candidate_prose_lines_with_draft_overlap": len(covered),
            "candidate_prose_lines_without_draft_overlap": len(candidates) - len(covered),
            "symbolic_candidate_lines": status_counts["symbolic_candidate"],
            "unresolved_fragment_lines": status_counts["unresolved_fragment"],
            "draft_propositions_starting_in_range": sum(start <= p["d_line_start"] <= end for p in draft),
            "human_semantic_review": "pending"})
    by_urgency = sorted(bands,
                        key=lambda b: (-b["candidate_prose_lines_without_draft_overlap"], b["start_line"]))
    return {"source_lines": len(lines), "draft_propositions":len(draft),
            "prose_candidates":len(entries),
            "candidate_without_draft_on_same_line":sum(b["candidate_prose_lines_without_draft_overlap"] for b in bands),
            "symbolic_candidates_not_semantically_resolved":sum(b["symbolic_candidate_lines"] for b in bands),
            "unresolved_fragments_not_semantically_resolved":sum(b["unresolved_fragment_lines"] for b in bands),
            "review_buckets_prioritized":by_urgency, "status":"not_frozen",
            "interpretation":"Overlap with an editorial draft does not establish completeness or semantic signoff."}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",help="Write JSON review metrics to this file")
    a=p.parse_args()
    report=analyze()
    content=json.dumps(report,indent=2,ensure_ascii=False)+"\n"
    if a.output:
        pathlib.Path(a.output).write_text(content, encoding="utf-8")
    print(content)
if __name__=="__main__": main()
