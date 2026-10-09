#!/usr/bin/env python3
"""Fail-closed checks on manual condition freeze. Never infer semantic coverage from hashes."""
import hashlib
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
INPUTS = ["A.txt", "B.txt", "C.txt", "D.txt", "battery.fr.json", "propositions.json", "non_extractable.json",
          "model_config.json", "coverage.json", "distractor_script.fr.json"]
FIELDS = {"condition", "model_id", "context_window", "tokenizer", "token_counts"}

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def validate():
    freeze = json.loads((HERE / "freeze.json").read_text(encoding="utf-8"))
    if freeze.get("state") != "frozen" or freeze.get("human_review") != "approved":
        raise ValueError("Manifest not marked frozen and human-approved.")
    if freeze.get("corpus_sha256") != "d49b3a98dfc50b1cc2066214976dbeda48771cd8162a084662cbde9239e07ff5":
        raise ValueError("Wrong original corpus SHA256.")
    extraction = json.loads((HERE / "extraction/manifest.json").read_text(encoding="utf-8"))
    if not extraction.get("completed") or not extraction.get("human_approved"):
        raise ValueError("Full source extraction is not independently approved.")
    hashes = freeze.get("files", {})
    for name in INPUTS:
        path = HERE / "frozen" / name
        if not path.is_file() or digest(path) != hashes.get("frozen/" + name):
            raise ValueError("Frozen content absent or modified: " + name)
    models = json.loads((HERE / "frozen/model_config.json").read_text(encoding="utf-8"))
    if len(models) < 2 or len({x["provider"] for x in models}) < 2:
        raise ValueError("Need at least two independent model provider families.")
    for m in models:
        if not m.get("exact_id") or not m.get("tokenizer") or not isinstance(m.get("context_window"), int):
            raise ValueError("Missing exact model configuration.")
        if m.get("temperature") != 0.7:
            raise ValueError("Temperature must be 0.7.")
        counts = m.get("token_counts")
        if not isinstance(counts, dict) or any(k not in counts for k in ("B", "C", "D")):
            raise ValueError("True tokenizer counts missing.")
        if counts["D"] == 0 or counts["D"] > m["context_window"] - 8000:
            raise ValueError("Source exceeds safe context. No mid-document cut.")
        if abs(counts["C"] - counts["D"]) / counts["D"] > 0.10:
            raise ValueError("C is not volume matched under " + m["exact_id"])
        if counts["B"] < 1:
            raise ValueError("Empty clinical control.")
    props = json.loads((HERE / "frozen/propositions.json").read_text(encoding="utf-8"))
    cov = json.loads((HERE / "frozen/coverage.json").read_text(encoding="utf-8"))
    if not props or set(x["id"] for x in props) != set(cov):
        raise ValueError("Coverage IDs do not match propositions.")
    for p in props:
        if not p.get("sentence") or not p.get("d_citation") or not cov[p["id"]].get("c_citation"):
            raise ValueError("Unverified proposition coverage " + p.get("id", "?"))
    # Required review is distinct from these automated syntactic checks.
    battery = json.loads((HERE / "frozen/battery.fr.json").read_text(encoding="utf-8"))
    if set(battery) != set("Q"+str(n) for n in range(1,13)):
        raise ValueError("Incomplete 12-question battery.")
    if any("[" in str(battery[x]) or "TODO" in str(battery[x]) for x in battery):
        raise ValueError("Unresolved battery template.")
    print("PASS: hash, coverage presence, source budget, and per-tokenizer length gates. Semantic checks require recorded human approval.")
    return True

if __name__ == "__main__":
    try:
        validate()
    except (OSError, ValueError, KeyError, TypeError) as error:
        print("BLOCKED:", error, file=sys.stderr)
        sys.exit(2)
