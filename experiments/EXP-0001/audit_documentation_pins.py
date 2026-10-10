#!/usr/bin/env python3
"""Prevent narrative source citations drifting from the immutable corpus manifest."""
import json
import pathlib
import re
from prepare_source import PIN, EXPECTED_BYTES, EXPECTED_SHA256

EXP=pathlib.Path(__file__).resolve().parent
ROOT=EXP.parents[1]
# Only document paths that must cite the exact commit; neither drafts nor log
# snapshots are silently rewritten when reviewed proposition counts change.
PATHS=("README.md","experiments/EXP-0001/STATUS.md","experiments/EXP-0001/REPORT.md")

def verify_texts(texts, canonical_pin):
    errors=[]
    for name,content in texts.items():
        found=re.findall(r"\b7d7dd5cb[0-9a-f]{32}\b",content)
        # Match a complete commit identifier, not an unrelated short tag.
        if canonical_pin not in found:
            errors.append(name+": canonical source pin absent")
        if any(pin!=canonical_pin for pin in found):
            errors.append(name+": source revision drift")
    return errors

def main():
    manifest=json.loads((EXP/"source_manifest.json").read_text(encoding="utf-8"))
    if manifest["commit"]!=PIN:
        raise ValueError("Pinned source commit differs between runtime and manifest")
    entry=manifest["candidate_order"][0]
    if entry["sha256"]!=EXPECTED_SHA256 or entry["size_bytes"]!=EXPECTED_BYTES:
        raise ValueError("Source digest or byte length differs from immutable source manifest")
    docs={name:(ROOT/name).read_text(encoding="utf-8") for name in PATHS}
    findings=verify_texts(docs,PIN)
    if findings:
        raise ValueError("Documentation provenance check failed: "+"; ".join(findings))
    print("Source documentation cites immutable upstream revision "+PIN+"; narrative citations consistent.")

if __name__=="__main__":main()
