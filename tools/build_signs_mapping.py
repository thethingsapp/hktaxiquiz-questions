#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scan images directory to build a mapping JSON for Chapter 8 assets.

Outputs: images/signs_mapping.json with structure:
{
  "generatedAt": "YYYY-MM-DDTHH:MM:SSZ",
  "sources": [
    {"category": "Traffic Signals giving Orders", "count": N},
    {"category": "Traffic Signs giving Orders", "count": N},
    {"category": "Traffic Signs giving Warning", "count": N}
  ],
  "items": [
    {
      "code": 52,
      "title": "Speed limit (in km/h)",
      "filename": "52. Speed limit(in km:h).png",
      "relPath": "images/Traffic Signs giving Orders/52. Speed limit(in km:h).png",
      "category": "Traffic Signs giving Orders",
      "type": "sign"
    },
    ...
  ]
}

Notes:
- Code is extracted from filename's leading number (before the first dot).
- Title is the remaining part before the extension after trimming spaces.
- Non-ASCII punctuation or minor typos in filenames are preserved as-is; consumer should map by code when possible.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMAGES_DIR = ROOT / "images"

CATEGORIES = [
    "Traffic Signals giving Orders",
    "Traffic Signs giving Orders",
    "Traffic Signs giving Warning",
]

FILENAME_RE = re.compile(r"^(\d+)\s*\.\s*(.+?)\.(?:png|jpg|jpeg)$", re.IGNORECASE)


def parse_item(path: Path, category: str) -> dict | None:
    m = FILENAME_RE.match(path.name)
    if not m:
        return None
    code = int(m.group(1))
    title = m.group(2).strip()
    rel_path = path.as_posix()
    # Convert absolute to repo-relative if needed
    if rel_path.startswith(ROOT.as_posix() + "/"):
        rel_path = rel_path[len(ROOT.as_posix()) + 1 :]
    item_type = "signal" if "Signal" in category else "sign"
    return {
        "code": code,
        "title": title,
        "filename": path.name,
        "relPath": rel_path,
        "category": category,
        "type": item_type,
    }


def main() -> int:
    items: list[dict] = []
    sources = []
    for cat in CATEGORIES:
        folder = IMAGES_DIR / cat
        if not folder.exists():
            continue
        count = 0
        for p in sorted(folder.glob("*.png")):
            item = parse_item(p, cat)
            if item:
                items.append(item)
                count += 1
        sources.append({"category": cat, "count": count})

    out = {
        "generatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "sources": sources,
        "items": items,
    }
    out_path = IMAGES_DIR / "signs_mapping.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(items)} items to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
