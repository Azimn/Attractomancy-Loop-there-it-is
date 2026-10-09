#!/usr/bin/env python3
"""Export blinded scoring packet and restricted key, never condition-labelled judge input."""
import argparse
import csv
import hashlib
import json
import pathlib
import random

HERE = pathlib.Path(__file__).resolve().parent
DIMS = ("factual_recall", "identity_consistency", "characteristic_judgment",
        "relationship_continuity", "spontaneous_expression", "resistance")

def export(raw, output, salt):
    output.mkdir(parents=True, exist_ok=True)
    packet, key = [], []
    for line in raw.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        if row["question_id"].startswith("DISTRACTOR"): continue
        if not row.get("response"): raise ValueError("Empty response")
        blind_id = hashlib.sha256((salt + "|" + row["run_id"] + "|" + row["question_id"]).encode()).hexdigest()[:20]
        packet.append({"blind_id": blind_id, "question_id": row["question_id"],
                       "phase": row["phase"], "response": row["response"]})
        key.append({"blind_id": blind_id, "run_id": row["run_id"], "model": row["model"],
                    "condition": row["condition"], "question_id": row["question_id"]})
    if len({x["blind_id"] for x in packet}) != len(packet):
        raise ValueError("Duplicate blind IDs or partial run duplication")
    random.Random(79017).shuffle(packet)
    with (output / "scoring_packet.jsonl").open("w", encoding="utf-8") as fh:
        for row in packet: fh.write(json.dumps(row, ensure_ascii=False)+"\n")
    with (output / "restricted_key.jsonl").open("w", encoding="utf-8") as fh:
        for row in key: fh.write(json.dumps(row, ensure_ascii=False)+"\n")
    with (output / "human_scores_template.csv").open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["blind_id", "rater"]+list(DIMS))
        writer.writeheader()
        for row in packet: writer.writerow({"blind_id": row["blind_id"]})
    return len(packet)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--salt", required=True)
    a = ap.parse_args()
    if len(a.salt) < 16: raise SystemExit("Use a new private random salt of at least 16 characters.")
    print("Exported blinded items:", export(pathlib.Path(a.raw), pathlib.Path(a.out), a.salt))
    print("Keep restricted_key.jsonl PRIVATE. Outputs can still leak distinctive condition language.")
if __name__ == "__main__": main()
