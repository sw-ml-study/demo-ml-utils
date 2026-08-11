#!/usr/bin/env python3
"""Deterministic lexical leakage and coverage analysis for frozen Agentrail JSONL."""
import argparse
import json
import re
from pathlib import Path


def normalize(text: str) -> tuple[str, ...]:
    return tuple(re.findall(r"[a-z0-9]+", text.lower()))


def ngrams(tokens: tuple[str, ...], width: int = 3) -> set[tuple[str, ...]]:
    return {tokens[i : i + width] for i in range(max(0, len(tokens) - width + 1))}


def similarity(left: set, right: set) -> float:
    union = left | right
    return len(left & right) / len(union) if union else 1.0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("data", type=Path)
    parser.add_argument("--max-jaccard", type=float, default=0.70)
    args = parser.parse_args()
    splits = {}
    for split in ("train", "valid", "test"):
        splits[split] = [json.loads(line) for line in (args.data / f"{split}.jsonl").read_text().splitlines()]

    ids = [row["id"] for rows in splits.values() for row in rows]
    duplicate_ids = len(ids) - len(set(ids))
    exact_duplicates = 0
    maximum = {"score": 0.0, "left": "", "right": ""}
    names = list(splits)
    for left_index, left_name in enumerate(names):
        for right_name in names[left_index + 1 :]:
            for left in splits[left_name]:
                left_tokens = normalize(left["prompt"])
                for right in splits[right_name]:
                    right_tokens = normalize(right["prompt"])
                    exact_duplicates += int(left_tokens == right_tokens)
                    score = similarity(ngrams(left_tokens), ngrams(right_tokens))
                    if score > maximum["score"]:
                        maximum = {"score": score, "left": left["id"], "right": right["id"]}

    families = sorted({row["source_family"] for rows in splits.values() for row in rows})
    coverage = {split: {family: sum(row["source_family"] == family for row in rows) for family in families} for split, rows in splits.items()}
    missing_family_cells = sum(count == 0 for row in coverage.values() for count in row.values())
    thresholds = {"duplicate_ids": 0, "exact_cross_split_duplicates": 0, "max_word_trigram_jaccard": args.max_jaccard, "missing_family_cells": 0, "minimum_held_out": 3}
    accepted = duplicate_ids == 0 and exact_duplicates == 0 and maximum["score"] <= args.max_jaccard and missing_family_cells == 0 and len(splits["test"]) >= 3
    report = {"schema": "sw-ml-study.agentrail-leakage", "version": 1, "counts": {k: len(v) for k, v in splits.items()}, "families": families, "coverage": coverage, "duplicate_ids": duplicate_ids, "exact_cross_split_duplicates": exact_duplicates, "maximum_cross_split_word_trigram_jaccard": maximum, "missing_family_cells": missing_family_cells, "thresholds": thresholds, "accepted": int(accepted), "model_calls": 0, "network_calls": 0}
    print(json.dumps(report, sort_keys=True))
    if not accepted:
        raise SystemExit("Agentrail corpus failed leakage/coverage promotion thresholds")


if __name__ == "__main__":
    main()
