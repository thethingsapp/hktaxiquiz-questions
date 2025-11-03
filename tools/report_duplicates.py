#!/usr/bin/env python3
from pathlib import Path
import json
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
paths = [
    ROOT/'part_a1_questions.json',
    ROOT/'part_a2_questions.json',
    ROOT/'part_a3_questions.json',
    ROOT/'part_b_questions.json',
]

def load(p: Path):
    try:
        return json.loads(p.read_text(encoding='utf-8'))
    except Exception as e:
        print('Skip', p.name, e)
        return None

dups = []
for p in paths:
    obj = load(p)
    if not obj:
        continue
    qs = obj.get('questions', [])
    by_key = defaultdict(list)
    for q in qs:
        t = (q.get('question') or '').strip()
        img = q.get('image') or q.get('img') or q.get('imagePath')
        if t:
            by_key[(t, img)].append(q.get('id'))
    for (text, img), ids in by_key.items():
        if len(ids) > 1:
            dups.append((p.name, ids, text, img))

OUT = ROOT/'build'/'reports'
OUT.mkdir(parents=True, exist_ok=True)
fp = OUT/'duplicate_questions.csv'
with fp.open('w', encoding='utf-8') as f:
    f.write('file,ids,count,question,image\n')
    for file, ids, text, img in dups:
        short = (text[:120] + '...') if len(text) > 120 else text
        img_s = (img or '').replace('"', '\"')
        f.write(f'{file},"{";".join(ids)}",{len(ids)},"{short}","{img_s}"\n')

print('Saved', fp)
