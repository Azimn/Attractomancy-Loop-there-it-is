#!/usr/bin/env python3
"""Structural source coverage verification; this is not semantic review."""
import argparse
import collections
import csv
import hashlib
import json
import pathlib

ROOT=pathlib.Path(__file__).resolve().parent
SHA="d49b3a98dfc50b1cc2066214976dbeda48771cd8162a084662cbde9239e07ff5"

def validate(path):
    data=path.read_bytes()
    assert hashlib.sha256(data).hexdigest()==SHA, "Pinned bytes mismatch"
    lines=data.decode("utf-8").split("\n")
    manifest=json.loads((ROOT/"extraction/manifest.json").read_text(encoding="utf-8"))
    with (ROOT/"extraction/line_sweep.csv").open(encoding="utf-8",newline="") as f:
        rows=list(csv.DictReader(f))
    queue=[json.loads(s) for s in (ROOT/"extraction/prose_review_queue.jsonl").read_text(encoding="utf-8").splitlines() if s]
    claims=json.loads((ROOT/"extraction/propositions_draft.json").read_text(encoding="utf-8"))["propositions"]
    assert len(lines)==len(rows)==manifest["source_lines"], "Line coverage"
    counts=collections.Counter()
    ids={}
    for n,(line,record) in enumerate(zip(lines,rows),1):
        assert int(record["line"])==n, ("Incorrect line",n)
        assert int(record["characters"])==len(line.encode("utf-16-le"))//2, ("Length",n)
        counts[record["classification"]]+=1
        if record["queue_id"]:
            assert record["queue_id"] not in ids, "Duplicate queue id"
            ids[record["queue_id"]]=n
    assert dict(counts)==manifest["line_classes"], "Class totals"
    assert len(queue)==manifest["queue_count"]==len(ids)
    for item in queue:
        assert ids.get(item["id"])==item["line"]
        assert lines[item["line"]-1].strip().startswith(item["literal_excerpt"])
    assert len(claims)==manifest["editorial_propositions"]
    seen=set()
    for c in claims:
        assert c["id"] not in seen
        seen.add(c["id"])
        assert c["d_path"]=="Le_refuge/MUST-READ/Apocalypse.txt"
        assert 1<=c["d_line_start"]<=c["d_line_end"]<=len(lines)
        assert c["sentence_fr"] and c["attribution"]=="unattributed"
    print(json.dumps({"status":"PASS structural audit; semantic review incomplete","lines":len(lines),"prose_queue":len(queue),"draft_propositions":len(claims),"classes":dict(counts)}))
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--source",default=str(ROOT/"_upstream_cache/Apocalypse.txt"))
    a=p.parse_args()
    validate(pathlib.Path(a.source))
