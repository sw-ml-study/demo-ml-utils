#!/usr/bin/env python3
"""Evaluate frozen Agentrail test JSONL with base and freshly loaded MLX adapter."""
import argparse
import hashlib
import json
from pathlib import Path
import re

import mlx.core as mx
from mlx_lm import generate, load
from mlx_lm.sample_utils import make_sampler


def first_action(text: str) -> str:
    clean = text.replace("<|im_end|>", "").strip()
    first = clean.splitlines()[0].strip() if clean else ""
    return first.removeprefix("ACTION:").strip()


def evaluate(model_path: str, adapter_path: str | None, cases: list[dict]) -> dict:
    model, tokenizer = load(model_path, adapter_path=adapter_path)
    sampler = make_sampler(temp=0)
    rows = []
    for case in cases:
        expected = first_action(case["completion"])
        prompt = tokenizer.apply_chat_template(
            [{"role": "user", "content": case["prompt"]}],
            add_generation_prompt=True,
            tokenize=False,
        )
        mx.random.seed(23)
        raw = generate(model, tokenizer, prompt=prompt, max_tokens=64, sampler=sampler)
        predicted = first_action(raw)
        exact = int(predicted == expected)
        rejection_expected = int(expected.startswith("REJECT"))
        rejection_correct = int((predicted.startswith("REJECT")) == bool(rejection_expected))
        rows.append({"id": case["id"], "family": case["source_family"], "expected_action": expected, "predicted_action": predicted, "action_exact": exact, "rejection_correct": rejection_correct})
    del model
    mx.clear_cache()
    return {"action_correct": sum(r["action_exact"] for r in rows), "rejection_correct": sum(r["rejection_correct"] for r in rows), "total": len(rows), "rows": rows}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--adapter", required=True)
    parser.add_argument("--test-data", required=True)
    parser.add_argument("--training-log", required=True)
    args = parser.parse_args()
    cases = [json.loads(line) for line in Path(args.test_data).read_text().splitlines()]
    mx.reset_peak_memory()
    base = evaluate(args.model, None, cases)
    adapted = evaluate(args.model, args.adapter, cases)
    adapter_file = Path(args.adapter) / "adapters.safetensors"
    peaks = [float(v) for v in re.findall(r"Peak mem ([0-9.]+) GB", Path(args.training_log).read_text())]
    if not peaks:
        raise SystemExit("training log has no MLX peak-memory evidence")
    report = {"schema": "sw-ml-study.agentrail-coding-evaluation", "version": 1, "base": base, "adapted": adapted, "training_peak_memory_gb": max(peaks), "evaluation_peak_memory_gb": mx.get_peak_memory()/1e9, "memory_limit_gb": 12.288, "adapter_bytes": adapter_file.stat().st_size, "adapter_sha256": hashlib.sha256(adapter_file.read_bytes()).hexdigest(), "automatic_execute": 0, "live_help_training_examples": 0}
    print(json.dumps(report, sort_keys=True))
    if adapted["action_correct"] != adapted["total"] or adapted["action_correct"] <= base["action_correct"]:
        raise SystemExit("adapter failed held-out exact-action improvement")
    if adapted["rejection_correct"] != adapted["total"]:
        raise SystemExit("adapter failed held-out rejection classification")
    if report["training_peak_memory_gb"] > report["memory_limit_gb"]:
        raise SystemExit("training exceeded the 12.288 GB memory limit")


if __name__ == "__main__":
    main()
