#!/usr/bin/env python3
"""Deterministic non-approved Condition B preview and provenance sidecar.

This is a drafting aid only. It neither asserts exhaustive extraction nor
authorizes copying its preview into frozen/B.txt before human review.
"""
import argparse
import hashlib
import json
import pathlib
import sys

ROOT=pathlib.Path(__file__).resolve().parent

def build(register):
    if register.get("status")!="editorial_draft_semantic_audit_open":
        raise ValueError("Unexpected proposition register status")
    propositions=register["propositions"]
    ids=set()
    result=[]
    for record in sorted(propositions,key=lambda p:(p["d_line_start"],p["d_line_end"],p["id"])):
        identity=record["id"]
        if identity in ids:raise ValueError("Duplicate proposition identity")
        ids.add(identity)
        if record["review_status"]!="editorial_draft_requires_independent_audit":
            raise ValueError("Unexpectedly approved claim cannot bypass review workflow")
        if record["attribution"]!="unattributed":
            raise ValueError("Unexpected speaker attribution requires explicit reviewer decision")
        if not record["sentence_fr"].strip() or not 1<=record["d_line_start"]<=record["d_line_end"]<=5562:
            raise ValueError("Missing draft text or provenance range")
        result.append(record)
    text="\n".join(r["sentence_fr"].strip() for r in result)+"\n"
    trace=[{"ordinal":i+1,"id":r["id"],"source_path":r["d_path"],
            "source_lines":[r["d_line_start"],r["d_line_end"]],
            "review_status":r["review_status"],"contradiction_group":r["contradiction_group"]}
           for i,r in enumerate(result)]
    return text,trace

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",help="Output path for UNAPPROVED French B preview")
    p.add_argument("--check",action="store_true",help="Only validate and print metrics")
    a=p.parse_args()
    manifest=json.loads((ROOT/"extraction/manifest.json").read_text(encoding="utf-8"))
    register=json.loads((ROOT/"extraction/propositions_draft.json").read_text(encoding="utf-8"))
    preview,trace=build(register)
    if len(trace)!=manifest["editorial_propositions"]:
        raise ValueError("Manifest count differs from source register")
    if a.out and not a.check:
        dest=pathlib.Path(a.out)
        if dest.resolve().parent==(ROOT/"frozen").resolve() or dest.name=="B.txt":
            raise ValueError("Cannot write an unapproved draft as frozen/B.txt")
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_text(preview,encoding="utf-8")
        dest.with_suffix(dest.suffix+".provenance.json").write_text(
            json.dumps({"approval":"NOT_APPROVED","items":trace},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":"UNAPPROVED_DRAFT",
        "propositions":len(trace),"preview_sha256":hashlib.sha256(preview.encode("utf-8")).hexdigest(),
        "preview_utf8_bytes":len(preview.encode("utf-8")),
        "ready_to_freeze":False},indent=2))

if __name__=="__main__":
    try:main()
    except (OSError,KeyError,TypeError,ValueError) as e:
        print("DRAFT BLOCKED:",e,file=sys.stderr)
        sys.exit(2)
