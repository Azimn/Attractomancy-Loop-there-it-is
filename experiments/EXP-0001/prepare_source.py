#!/usr/bin/env python3
"""Acquire byte-identical pinned source, verify against independent digest; never mirror into Git."""
import argparse
import hashlib
import json
import pathlib
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
PIN = "7d7dd5cb9305032669d692b6894d766ac07abac9"
NAME = "Le_refuge/MUST-READ/Apocalypse.txt"
EXPECTED_BYTES = 142596
EXPECTED_SHA256 = "d49b3a98dfc50b1cc2066214976dbeda48771cd8162a084662cbde9239e07ff5"
EXPECTED_BLOB = "5971a09164688ecb8afbaafe53d7e16439b7f94d"

def git_blob_sha1(data):
    return hashlib.sha1(("blob %d\0" % len(data)).encode() + data).hexdigest()

def fetch(out):
    url = "https://raw.githubusercontent.com/IorenzoLF/Le_Refuge/" + PIN + "/" + NAME
    req = urllib.request.Request(url, headers={"User-Agent": "attractomancy-exp0001/1.0"})
    with urllib.request.urlopen(req, timeout=45) as response:
        data = response.read()
    audit = {
        "url": url, "revision": PIN, "file": NAME,
        "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
        "git_blob_sha1": git_blob_sha1(data), "language": "fr",
        "verified": False
    }
    audit["verified"] = (audit["bytes"] == EXPECTED_BYTES and
                         audit["sha256"] == EXPECTED_SHA256 and
                         audit["git_blob_sha1"] == EXPECTED_BLOB)
    if not audit["verified"]:
        raise ValueError("Pinned source integrity failed. Do not use source or change expectations. " + json.dumps(audit))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    return audit

def tokenize(audit, source, model):
    try:
        import tiktoken
    except ImportError as e:
        raise RuntimeError("Exact tokenizer unavailable. Install tiktoken, or do not freeze counts.") from e
    # Explicitly disallow falling back to approximate encoding.
    enc = tiktoken.encoding_for_model(model)
    audit.setdefault("token_counts", {})[model] = len(enc.encode(source.read_text(encoding="utf-8")))
    audit.setdefault("tokenizers", {})[model] = enc.name

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(HERE / "_upstream_cache" / "Apocalypse.txt"))
    parser.add_argument("--tiktoken-model", action="append", default=[])
    args = parser.parse_args()
    path = pathlib.Path(args.out)
    audit = fetch(path)
    for m in args.tiktoken_model:
        tokenize(audit, path, m)
    auditfile = path.parent / "source_audit.json"
    auditfile.write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(audit, indent=2, ensure_ascii=False))
    print("Cache file and audit generated; not an experiment freeze.")
if __name__ == "__main__":
    main()
