#!/usr/bin/env python3
"""Compute live source review metrics without inflating editor work into approvals."""
import csv
import json
import pathlib
from audit_review_decisions import inspect as check_reviews
from check_claim_overlap import examine as check_claims

ROOT=pathlib.Path(__file__).resolve().parent

def metrics(root=ROOT):
    manifest=json.loads((root/"extraction/manifest.json").read_text(encoding="utf-8"))
    register=json.loads((root/"extraction/propositions_draft.json").read_text(encoding="utf-8"))
    claims=register["propositions"]
    queue=[json.loads(s) for s in (root/"extraction/prose_review_queue.jsonl").read_text(encoding="utf-8").splitlines() if s]
    with (root/"extraction/review_decisions.csv").open(encoding="utf-8",newline="") as f:
        decisions=list(csv.DictReader(f))
    if len(claims)!=manifest["editorial_propositions"]:
        raise ValueError("Manifest proposition count drifted")
    if len(queue)!=manifest["queue_count"]:
        raise ValueError("Manifest candidate count drifted")
    spans={x["id"]:(x["d_line_start"],x["d_line_end"]) for x in claims}
    report=check_reviews(decisions,manifest["source_lines"],set(spans),proposition_spans=spans)
    clashes=check_claims(claims)
    cited=set()
    for c in claims:
        cited.update(range(c["d_line_start"],c["d_line_end"]+1))
    outstanding=sum(x["line"] not in cited for x in queue)
    return {
        "stage":"EXTRACTION_ONLY",
        "source_lines":manifest["source_lines"],
        "editorial_proposition_drafts":len(claims),
        "initial_lexical_prose_candidates":len(queue),
        "candidate_start_lines_without_draft_overlap":outstanding,
        "source_lines_with_editorial_decisions":report["adjudicated_source_lines"],
        "source_lines_without_editorial_decisions":report["unadjudicated_source_lines"],
        "explicit_unresolved_decisions":report["unresolved_adjudications"],
        "line_level_semantic_eligibility":report["eligible_for_review_signoff"],
        "exact_citation_collision_groups":len(clashes["exactly_same_citation_groups"]),
        "overlapping_claim_source_lines":len(clashes["overlapping_source_lines"]),
        "independent_review_attestation_present":(root/"extraction/review_signoff.json").is_file(),
        "condition_B_frozen":(root/"freeze.json").is_file(),
        "treatment_runs_completed_by_this_script":0,
        "interpretation":"Draft coverage is not semantic completeness. Reviewer approval not implied."
    }

if __name__=="__main__":
    print(json.dumps(metrics(),indent=2,ensure_ascii=False))
