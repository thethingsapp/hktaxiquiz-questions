# -*- coding: utf-8 -*-
"""
Sync Part B explanations from the app assets JSON into this repository's part_b_questions.json.
- Source: /Users/louiswong/Desktop/development/hktaxiquiz/assets/questions/part_b_questions.json
- Target: /Users/louiswong/Desktop/development/hktaxiquiz-questions/part_b_questions.json

Strategy:
- Match questions by 'id'.
- For matching ids, copy over 'explanation' from source to target.
- Optionally could sync options/title/etc., but we keep scope minimal per request.
- Create a .bak sync backup next to the target before writing.
- Print the number of updated questions.
"""
import json
import shutil
from pathlib import Path

SRC = Path("/Users/louiswong/Desktop/development/hktaxiquiz/assets/questions/part_b_questions.json")
DST = Path("/Users/louiswong/Desktop/development/hktaxiquiz-questions/part_b_questions.json")
BACKUP = DST.with_suffix(DST.suffix + ".bak_sync")

def load_json(p: Path):
    with p.open(encoding="utf-8") as f:
        return json.load(f)

def main():
    src = load_json(SRC)
    dst = load_json(DST)
    src_qs = {q.get('id'): q for q in src.get('questions', []) if isinstance(q, dict) and q.get('id')}
    changed = 0
    for q in dst.get('questions', []):
        if not isinstance(q, dict):
            continue
        qid = q.get('id')
        if not qid or qid not in src_qs:
            continue
        src_exp = src_qs[qid].get('explanation')
        if isinstance(src_exp, str) and q.get('explanation') != src_exp:
            q['explanation'] = src_exp
            changed += 1
    # Backup and write
    shutil.copy2(DST, BACKUP)
    with DST.open('w', encoding='utf-8') as f:
        json.dump(dst, f, ensure_ascii=False, indent=2)
    print("synced_explanations:", changed)

if __name__ == '__main__':
    main()
