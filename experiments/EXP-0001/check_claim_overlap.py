#!/usr/bin/env python3
"""Find overlapping draft source citations requiring semantic duplicate decisions.

Overlap is a REVIEW FLAG, not an automatic rejection: multiple distinct claims
may genuinely occur in the same line of this heterogeneous source.
"""
import collections
import json
import pathlib

ROOT=pathlib.Path(__file__).resolve().parent

def examine(claims):
    exact=collections.defaultdict(list)
    by_line=collections.defaultdict(list)
    for p in claims:
        key=(p["d_path"],p["d_line_start"],p["d_line_end"])
        exact[key].append(p["id"])
        for n in range(p["d_line_start"],p["d_line_end"]+1):
            by_line[(p["d_path"],n)].append(p["id"])
    identical=[{"source":k[0],"start":k[1],"end":k[2],"ids":ids}
               for k,ids in sorted(exact.items()) if len(ids)>1]
    line_conflicts=[{"source":k[0],"line":k[1],"ids":v}
                    for k,v in sorted(by_line.items()) if len(v)>1]
    return {"exactly_same_citation_groups":identical,
            "overlapping_source_lines":line_conflicts,
            "needs_semantic_duplicate_review":bool(identical or line_conflicts),
            "claims":len(claims),"auto_removed":0}

def main():
    doc=json.loads((ROOT/"extraction/propositions_draft.json").read_text(encoding="utf-8"))
    print(json.dumps(examine(doc["propositions"]),ensure_ascii=False,indent=2))
if __name__=="__main__":main()
