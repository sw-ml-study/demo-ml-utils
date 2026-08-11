#!/usr/bin/env python3
"""Thin MLX-LM generation adapter; MLPL owns the dataset contract."""
import argparse
import hashlib
import json
from pathlib import Path
import re

import mlx.core as mx
from mlx_lm import generate, load
from mlx_lm.sample_utils import make_sampler


CASES = [
    ("next", "the saga has no active work; show the next required action without mutation."),
    ("begin", "a reviewed pending step is ready for implementation now."),
    ("complete", "all acceptance evidence for the in-progress step is green and committed."),
]
PREFIX = "Return only the exact next Agentrail command. Repository state: "


def normalize(value: str) -> str:
    return re.split(r"<\|im_end\|>|\n", value.strip(), maxsplit=1)[0].strip()


def evaluate(model_path: str, adapter_path: str | None) -> dict:
    model, tokenizer = load(model_path, adapter_path=adapter_path)
    sampler = make_sampler(temp=0)
    rows = []
    for action, state in CASES:
        expected = f"agentrail {action}"
        prompt = tokenizer.apply_chat_template(
            [{"role": "user", "content": PREFIX + state}],
            add_generation_prompt=True,
            tokenize=False,
        )
        mx.random.seed(17)
        raw = generate(model, tokenizer, prompt=prompt, max_tokens=8, sampler=sampler)
        predicted = normalize(raw)
        rows.append({"expected": expected, "predicted": predicted, "exact": int(predicted == expected)})
    del model
    mx.clear_cache()
    return {"correct": sum(row["exact"] for row in rows), "total": len(rows), "rows": rows}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--adapter", required=True)
    parser.add_argument("--training-log", required=True)
    args = parser.parse_args()
    mx.reset_peak_memory()
    base = evaluate(args.model, None)
    adapted = evaluate(args.model, args.adapter)
    adapter_file = Path(args.adapter) / "adapters.safetensors"
    training_text = Path(args.training_log).read_text()
    training_peaks = [float(value) for value in re.findall(r"Peak mem ([0-9.]+) GB", training_text)]
    if not training_peaks:
        raise SystemExit("training log has no MLX peak-memory evidence")
    report = {
        "schema": "sw-ml-study.agentrail-small-evaluation",
        "version": 1,
        "base": base,
        "adapted": adapted,
        "peak_memory_gb": mx.get_peak_memory() / 1e9,
        "training_peak_memory_gb": max(training_peaks),
        "memory_limit_gb": 12.288,
        "adapter_bytes": adapter_file.stat().st_size,
        "adapter_sha256": hashlib.sha256(adapter_file.read_bytes()).hexdigest(),
        "automatic_execute": 0,
    }
    print(json.dumps(report, sort_keys=True))
    if base["correct"] >= adapted["correct"] or adapted["correct"] != adapted["total"]:
        raise SystemExit("adapter failed exact held-out improvement")
    if report["training_peak_memory_gb"] > report["memory_limit_gb"]:
        raise SystemExit("training exceeded the 12.288 GB memory limit")


if __name__ == "__main__":
    main()
