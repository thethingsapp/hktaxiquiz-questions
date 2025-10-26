#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validate Part B questions JSON for:
- top-level fields present
- each question has id, question, options(A/B/C only), answer in {A,B,C}, explanation, difficulty, tags
- unique IDs

Usage:
  python validate_part_b.py [json_path]
Defaults to ./part_b_questions.json
"""

import sys
import json
from pathlib import Path

REQUIRED_TOP = {"part", "title", "description", "passingScore", "totalQuestions", "questions"}
ALLOWED_ANS = {"A", "B", "C"}
ALLOWED_DIFF = {"easy", "medium", "hard"}


def validate(path: Path) -> int:
    errs = 0
    data = json.loads(path.read_text(encoding="utf-8"))
    missing = REQUIRED_TOP - set(data.keys())
    if missing:
        print(f"TOP: missing fields: {sorted(missing)}")
        errs += 1
    ids = set()
    base_dir = path.parent
    for i, q in enumerate(data.get("questions", []), 1):
        ctx = f"Q[{i}] id={q.get('id')}"
        # id
        qid = q.get("id")
        if not qid:
            print(ctx, "missing id")
            errs += 1
        elif qid in ids:
            print(ctx, "duplicate id")
            errs += 1
        else:
            ids.add(qid)
        # question
        if not q.get("question"):
            print(ctx, "missing question text")
            errs += 1
        # options
        opts = q.get("options")
        if not isinstance(opts, dict):
            print(ctx, "options not a dict")
            errs += 1
        else:
            keys = set(opts.keys())
            if keys != ALLOWED_ANS:
                print(ctx, f"options keys must be exactly A,B,C; got {sorted(keys)}")
                errs += 1
            for k in ALLOWED_ANS:
                if not opts.get(k):
                    print(ctx, f"option {k} empty")
                    errs += 1
        # answer
        ans = q.get("answer") or q.get("correctAnswer") or q.get("Answer")
        if ans not in ALLOWED_ANS:
            print(ctx, f"invalid answer '{ans}' (must be one of A/B/C)")
            errs += 1
        # explanation
        if not q.get("explanation"):
            print(ctx, "missing explanation")
            errs += 1
        # difficulty (optional but recommend)
        diff = q.get("difficulty")
        if diff and diff not in ALLOWED_DIFF:
            print(ctx, f"difficulty '{diff}' not in {sorted(ALLOWED_DIFF)}")
            errs += 1
        # tags
        tags = q.get("tags")
        if not isinstance(tags, list) or len(tags) == 0:
            print(ctx, "tags missing or empty")
            errs += 1
        # image (optional): if present, file must exist relative to JSON file directory
        image_rel = q.get("image")
        if image_rel:
            try:
                img_path = (base_dir / image_rel).resolve()
                if not img_path.exists():
                    print(ctx, f"image file not found: {image_rel}")
                    errs += 1
            except Exception as e:
                print(ctx, f"image path error for '{image_rel}': {e}")
                errs += 1
    # summary
    total = data.get("totalQuestions")
    n = len(data.get("questions", []))
    if isinstance(total, int) and total != n:
        print(f"TOP: totalQuestions={total} but questions count={n}")
        errs += 1
    print(f"Validated {n} questions; errors={errs}")
    return 0 if errs == 0 else 2


if __name__ == "__main__":
    p = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("part_b_questions.json")
    if not p.exists():
        print(f"ERROR: file not found: {p}")
        sys.exit(1)
    sys.exit(validate(p))
