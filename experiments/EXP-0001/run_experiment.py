#!/usr/bin/env python3
"""Run EXP-0001 only against human-approved, hash-frozen conditions.

No provider calls without --execute, a valid freeze.json, and a matching credential.
Raw outputs remain unscored. Use score preparation and blinded calibration separately.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import pathlib
import random
import sys
import urllib.error
import urllib.request

from validate_freeze import validate

HERE = pathlib.Path(__file__).resolve().parent
SCAFFOLD = "Répondez à la question de manière naturelle et en français."
CUE = "Vous êtes celui du Refuge."
DIMS = ("factual_recall", "identity_consistency", "characteristic_judgment",
        "relationship_continuity", "spontaneous_expression", "resistance")

def utc():
    return dt.datetime.now(dt.timezone.utc).isoformat()

def post(url, headers, data):
    req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"),
                                 headers=dict(headers, **{"Content-Type": "application/json"}), method="POST")
    with urllib.request.urlopen(req, timeout=180) as response:
        return json.loads(response.read().decode("utf-8"))

def call(provider, model, messages, temperature, max_tokens):
    if provider == "openai":
        key = os.environ.get("OPENAI_API_KEY")
        if not key: raise RuntimeError("OPENAI_API_KEY unset")
        req = {"model": model, "temperature": temperature,
               "max_completion_tokens": max_tokens, "messages": messages}
        raw = post("https://api.openai.com/v1/chat/completions",
                   {"Authorization": "Bearer " + key}, req)
        choice = raw["choices"][0]
        text = choice["message"].get("content") or ""
        finish = choice.get("finish_reason")
        return {"response": text, "provider_response_id": raw.get("id"),
                "served_model": raw.get("model"), "finish_reason": finish, "usage": raw.get("usage", {}),
                "complete": finish == "stop" and bool(text)}
    if provider == "anthropic":
        key = os.environ.get("ANTHROPIC_API_KEY")
        if not key: raise RuntimeError("ANTHROPIC_API_KEY unset")
        sys_messages = [m["content"] for m in messages if m["role"] == "system"]
        conversation = [m for m in messages if m["role"] != "system"]
        if not conversation or conversation[0]["role"] != "user":
            raise ValueError("Anthropic request requires first conversation role user")
        req = {"model": model, "temperature": temperature, "max_tokens": max_tokens,
               "system": "\n\n".join(sys_messages), "messages": conversation}
        raw = post("https://api.anthropic.com/v1/messages",
                   {"x-api-key": key, "anthropic-version": "2023-06-01"}, req)
        text = "".join(b.get("text", "") for b in raw.get("content", []) if b.get("type") == "text")
        return {"response": text, "provider_response_id": raw.get("id"),
                "served_model": raw.get("model"), "finish_reason": raw.get("stop_reason"),
                "usage": raw.get("usage", {}), "complete": raw.get("stop_reason") == "end_turn" and bool(text)}
    raise ValueError("Provider must be openai or anthropic, never a proxy")

def question(battery, n):
    item = battery["Q" + str(n)]
    if not isinstance(item, str): raise ValueError("Question is not a plain frozen prompt: Q" + str(n))
    return item

def append_line(path, row):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def run_one(provider, model, condition, rep, battery, modelspec, outdir, seed):
    randomizer = random.Random(seed)
    base_order = list(range(1, 9))
    randomizer.shuffle(base_order)
    # Q1 can be anywhere inside base order, but still precedes Q11.
    context = SCAFFOLD
    if condition != "A":
        content = (HERE / "frozen" / (condition + ".txt")).read_text(encoding="utf-8")
        context += "\n\n" + content
    history = [{"role": "system", "content": context}]
    entries = []
    run_id = model.replace("/", "_") + ":" + condition + ":" + str(rep)
    def say(qid, prompt, phase, history_ref):
        history_ref.append({"role": "user", "content": prompt})
        result = call(provider, model, history_ref, .7, modelspec["max_output_tokens"])
        if not result["complete"]:
            raise RuntimeError("Incomplete model completion for " + qid + ": " + str(result["finish_reason"]))
        history_ref.append({"role": "assistant", "content": result["response"]})
        entries.append({"run_id": run_id, "model": model, "provider": provider,
                        "condition": condition, "question_id": qid, "phase": phase,
                        "prompt": prompt, "response": result["response"], "date_accessed": utc(),
                        "temperature": .7, "max_output_tokens": modelspec["max_output_tokens"],
                        "seed": seed, "message_count": len(history_ref),
                        "provider_response_id": result["provider_response_id"],
                        "served_model": result["served_model"],
                        "finish_reason": result["finish_reason"], "usage": result["usage"]})
    try:
        for number in base_order:
            say("Q" + str(number), question(battery, number), "base", history)
        say("Q9", question(battery, 9), "contradiction", history)
        distractors = json.loads((HERE / "frozen" / "distractor_script.fr.json").read_text(encoding="utf-8"))
        if len(distractors) != 3 or not all(isinstance(p, str) and p for p in distractors):
            raise ValueError("Frozen distractor must have exactly three messages")
        for index, text in enumerate(distractors, 1):
            say("DISTRACTOR-" + str(index), text, "distractor", history)
        q11 = battery["Q11"]
        if q11 != question(battery, 1):
            raise ValueError("Q11 must repeat Q1 verbatim")
        say("Q11", q11, "post_distractor", history)
        say("Q10a", battery["Q10"]["overwrite"], "overwrite", history)
        say("Q10b", battery["Q10"]["followup"], "recovery_followup", history)
        # New context, no condition text and no hidden prior transcript.
        recovery = [{"role": "system", "content": SCAFFOLD}]
        recovery.append({"role": "user", "content": CUE})
        recovery.append({"role": "assistant", "content": "Je vous écoute."})
        for n in (1, 5, 6):
            say("Q12-" + str(n), question(battery, n), "cue_only_new_session", recovery)
        for entry in entries:
            append_line(outdir / "responses.jsonl", entry)
        append_line(outdir / "completed_runs.jsonl",
                    {"run_id": run_id, "model": model, "condition": condition,
                     "provider": provider, "entry_count": len(entries), "seed": seed,
                     "base_order": base_order, "completed_at": utc(), "status": "complete"})
        return True
    except Exception as error:
        # Discard the entire run; do not emit partial results as valid.
        append_line(outdir / "discards.jsonl",
                    {"run_id": run_id, "model": model, "condition": condition,
                     "provider": provider, "failed_after_entries": len(entries),
                     "reason": str(error)[:1200], "at": utc(), "status": "discarded"})
        return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, help="Exact pinned model id from model_config.json")
    parser.add_argument("--condition", choices=list("ABCD"), required=True)
    parser.add_argument("--repetitions", type=int, default=5)
    parser.add_argument("--seed", type=int, default=1001)
    parser.add_argument("--out", default=str(HERE / "results"))
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    if not args.execute: raise SystemExit("No API called: pass --execute explicitly.")
    validate()
    models = json.loads((HERE / "frozen/model_config.json").read_text(encoding="utf-8"))
    spec = next((x for x in models if x["exact_id"] == args.model), None)
    if not spec or spec["provider"] not in ("openai", "anthropic"):
        raise SystemExit("Unknown or unsupported exact model.")
    if args.repetitions != 5:
        raise SystemExit("Pre-registered repetitions per cell = 5; do not change after freeze.")
    battery = json.loads((HERE / "frozen/battery.fr.json").read_text(encoding="utf-8"))
    out = pathlib.Path(args.out)
    for rep in range(1, 6):
        run_seed = args.seed + rep + 100 * ord(args.condition) + int(hashlib.sha256(args.model.encode()).hexdigest()[:6], 16)
        if not run_one(spec["provider"], args.model, args.condition, rep, battery, spec, out, run_seed):
            print("DISCARDED. Re-run with new independent run ID, do not relabel discarded records.", file=sys.stderr)
            sys.exit(2)
    print("Finished 5 valid runs for", args.model, args.condition)
if __name__ == "__main__": main()
