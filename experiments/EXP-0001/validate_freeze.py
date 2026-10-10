#!/usr/bin/env python3
"""Fail-closed checks on manual condition freeze. Never infer semantic coverage from hashes."""
import hashlib
import json
import pathlib
import sys
import csv
from audit_review_decisions import inspect as inspect_review_decisions

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
    with (HERE / "extraction/review_decisions.csv").open(encoding="utf-8", newline="") as handle:
        decisions = list(csv.DictReader(handle))
    prop_drafts = json.loads((HERE / "extraction/propositions_draft.json").read_text(encoding="utf-8"))["propositions"]
    review = inspect_review_decisions(decisions, extraction["source_lines"],
                                      {p["id"] for p in prop_drafts}, strict=True)
    if not review["eligible_for_review_signoff"]:
        raise ValueError("Exhaustive semantic review not completed.")
    manifest = json.loads((HERE / "source_manifest.json").read_text(encoding="utf-8"))
    expected = ["Le_refuge/MUST-READ/Apocalypse.txt"]
    if manifest.get("actual_included_files") != expected:
        raise ValueError("No final documented corpus inclusion decision.")
    if digest(HERE / "frozen/D.txt") != freeze["corpus_sha256"]:
        raise ValueError("D treatment is not byte-identical to the sole included upstream source.")
    # The semantic signoff must refer to the actual reviewed bytes. A boolean
    # in the extraction manifest alone is insufficient audit evidence.
    attestation = json.loads((HERE / "extraction/review_signoff.json").read_text(encoding="utf-8"))
    if attestation.get("independent_review_passed") is not True:
        raise ValueError("No affirmative independent semantic-review attestation.")
    if attestation.get("reviewer_type") != "independent_human" or not attestation.get("reviewer_name"):
        raise ValueError("No identified independent human reviewer.")
    if not attestation.get("reviewed_at") or attestation.get("conflicts_reviewed") is not True:
        raise ValueError("Unresolved conflict review or missing review date.")
    for file_name, expected_key in (("propositions_draft.json","proposition_register_sha256"),
                                    ("review_decisions.csv","review_decisions_sha256")):
        if digest(HERE / "extraction" / file_name) != attestation.get(expected_key):
            raise ValueError("Independent signoff is stale or refers to different "+file_name)
    if attestation.get("source_sha256") != freeze["corpus_sha256"]:
        raise ValueError("Signoff source digest differs from frozen corpus.")
    if digest(HERE / "extraction/review_signoff.json") != freeze.get("review_signoff_sha256"):
        raise ValueError("Freeze manifest does not pin the independent review attestation.")
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
    if not all(isinstance(battery["Q"+str(n)],str) and battery["Q"+str(n)].strip()
               for n in range(1,10)):
        raise ValueError("Q1-Q9 must be nine nonempty French prompts.")
    if battery["Q11"] != battery["Q1"] or not isinstance(battery["Q11"],str):
        raise ValueError("Q11 must be an exact string repetition of Q1.")
    overwrite = battery["Q10"]
    if not isinstance(overwrite,dict) or set(overwrite)!={"overwrite","followup"} or not all(isinstance(v,str) and v.strip() for v in overwrite.values()):
        raise ValueError("Q10 must contain fixed overwrite and followup prompts.")
    cue = battery["Q12"]
    if not isinstance(cue,dict) or cue.get("fresh_cue") != "Vous êtes celui du Refuge." or cue.get("sequence") != ["Q1","Q5","Q6"] or cue.get("role") != "zero_shot_cue_calibration_not_hypothesis_test":
        raise ValueError("Q12 must be fixed and marked cue-only calibration.")
    distractors = json.loads((HERE/"frozen/distractor_script.fr.json").read_text(encoding="utf-8"))
    if not isinstance(distractors,list) or len(distractors)!=3 or not all(isinstance(v,str) and v.strip() for v in distractors):
        raise ValueError("Three fixed unrelated distractor messages are required.")
    for model in models:
        # Counts must come from the model's real tokenizer; semantic independence is signed off separately.
        dcount=model.get("distractor_script_input_tokens")
        if not isinstance(dcount,int) or not 1350 <= dcount <= 1650:
            raise ValueError("Prompt-only distractor volume must be 1500 tokens +/-10% under "+model["exact_id"])

    print("PASS: hash, coverage presence, source budget, and per-tokenizer length gates. Semantic checks require recorded human approval.")
    return True

if __name__ == "__main__":
    try:
        validate()
    except (OSError, ValueError, KeyError, TypeError) as error:
        print("BLOCKED:", error, file=sys.stderr)
        sys.exit(2)
