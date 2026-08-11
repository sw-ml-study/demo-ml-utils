#!/usr/bin/env python3
"""Validate evaluation-only Agentrail adversarial fixtures and training separation."""
import argparse
import json
import re
from collections import Counter
from pathlib import Path

FAMILIES = {"invalid-transition", "conflicting-evidence", "prompt-injection", "malformed-output", "dirty-worktree", "long-trajectory"}
KEYS = {"automatic_execute", "automatic_send", "expected_action", "expected_rejection", "family", "id", "prompt"}


def tokens(text: str) -> tuple[str, ...]:
    return tuple(re.findall(r"[a-z0-9]+", text.lower()))


def trigrams(text: str) -> set[tuple[str, ...]]:
    words = tokens(text)
    return {words[i:i+3] for i in range(max(0, len(words)-2))}


def jaccard(left: set, right: set) -> float:
    return len(left & right) / len(left | right) if left | right else 1.0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("evaluation", type=Path)
    parser.add_argument("training", type=Path)
    args = parser.parse_args()
    cases = [json.loads(line) for line in (args.evaluation / "cases.jsonl").read_text().splitlines()]
    provenance = json.loads((args.evaluation / "provenance.json").read_text())
    training = [json.loads(line) for split in ("train", "valid", "test") for line in (args.training / f"{split}.jsonl").read_text().splitlines()]
    ids = [row["id"] for row in cases]
    training_ids = {row["id"] for row in training}
    family_counts = Counter(row["family"] for row in cases)
    key_errors = sum(set(row) != KEYS for row in cases)
    unsafe_flags = sum(row["automatic_execute"] != 0 or row["automatic_send"] != 0 for row in cases)
    bad_rejection = sum(row["expected_rejection"] not in (0, 1) for row in cases)
    maximum = {"score": 0.0, "evaluation_id": "", "training_id": ""}
    for case in cases:
        for source in training:
            score = jaccard(trigrams(case["prompt"]), trigrams(source["prompt"]))
            if score > maximum["score"]:
                maximum = {"score": score, "evaluation_id": case["id"], "training_id": source["id"]}
    accepted = len(cases) == 12 and len(ids) == len(set(ids)) and not (set(ids) & training_ids) and set(family_counts) == FAMILIES and all(family_counts[f] == 2 for f in FAMILIES) and key_errors == 0 and unsafe_flags == 0 and bad_rejection == 0 and maximum["score"] <= 0.70 and provenance["training_examples"] == 0 and provenance["live_help_examples"] == 0 and provenance["private_examples"] == 0
    report = {"schema":"sw-ml-study.agentrail-adversarial-validation","version":1,"examples":len(cases),"family_counts":dict(sorted(family_counts.items())),"duplicate_ids":len(ids)-len(set(ids)),"training_id_overlap":len(set(ids)&training_ids),"key_errors":key_errors,"unsafe_flags":unsafe_flags,"maximum_training_similarity":maximum,"threshold":0.70,"provenance":provenance,"accepted":int(accepted)}
    print(json.dumps(report, sort_keys=True))
    if not accepted:
        raise SystemExit("adversarial fixture validation failed")


if __name__ == "__main__":
    main()
