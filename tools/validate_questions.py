#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, List, Tuple
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
FILES = [
    ROOT/'part_a1_questions.json',
    ROOT/'part_a2_questions.json',
    ROOT/'part_a3_questions.json',
    ROOT/'part_b_questions.json',
]

FORBIDDEN_PHRASES = [
    # 避免題目直接引用來源（可保留於編者備註，但不在題幹/解釋出現）
    '根據附錄', '附錄甲（', '附錄乙（', '附錄丙（', '附錄丁（', '附錄戊（', '附錄己（'
]

# 允許的 ID 形式：
# - A1/A 類：A001
# - A2/A3 類：A2_001, A3_015
# - B 類：B131, B0001
ID_PATTERN = re.compile(r'^(?:A[0-9]{3}|A[23]_[0-9]{3}|B[0-9]{2,4})$')


def load(path: Path) -> Dict:
    return json.loads(path.read_text(encoding='utf-8'))


def validate_file(path: Path) -> Tuple[Dict, List[str], Dict]:
    """Return (obj, issues, stats)."""
    issues: List[str] = []
    obj = load(path)

    title = obj.get('title') or obj.get('part') or path.name
    qs: List[Dict] = obj.get('questions', [])

    # Stats
    stats = {
        'file': path.name,
        'title': title,
        'count_declared': obj.get('totalQuestions'),
        'count_actual': len(qs),
        'correct_dist': {k: 0 for k in list('ABCD')},
        'empty_explanations': 0,
        'forbidden_hits': 0,
    }

    # Check top-level count
    if obj.get('totalQuestions') != len(qs):
        issues.append(f"[COUNT] {path.name}: totalQuestions={obj.get('totalQuestions')} but actual={len(qs)}")

    seen_ids = set()
    dup_q_text = {}

    for i, q in enumerate(qs):
        qid = q.get('id')
        if not qid:
            issues.append(f"[SCHEMA] {path.name} Q#{i}: missing id")
            continue
        if qid in seen_ids:
            issues.append(f"[DUP-ID] {path.name} {qid} duplicated")
        seen_ids.add(qid)

        # ID pattern warning（不強制）
        if not ID_PATTERN.match(qid):
            issues.append(f"[ID] {path.name} {qid}: non-standard id format")

        question = (q.get('question') or '').strip()
        if not question:
            issues.append(f"[SCHEMA] {path.name} {qid}: empty question")

        # Duplicate detection: consider image path if present to avoid false positives
        img = q.get('image') or q.get('img') or q.get('imagePath')
        dup_key = (question, img)
        dup_q_text.setdefault(dup_key, []).append(qid)

        options = q.get('options') or {}
        if not isinstance(options, dict):
            issues.append(f"[SCHEMA] {path.name} {qid}: options not a dict")
            continue
        # 檢查選項鍵：允許 3 或 4 個選項（A~C 或 A~D）
        opt_keys = ''.join(sorted(options.keys()))
        if opt_keys not in ('ABC', 'ABCD'):
            issues.append(f"[SCHEMA] {path.name} {qid}: unexpected option keys {sorted(options.keys())}")
        # 準備實際存在的鍵
        present_keys = [k for k in 'ABCD' if k in options]
        # Empty options（只檢查實際存在的鍵）
        for k in present_keys:
            v = (options.get(k) or '').strip()
            if v == '':
                issues.append(f"[SCHEMA] {path.name} {qid}: option {k} empty")
        # Option duplication
        opt_values = [options.get(k, '').strip() for k in present_keys]
        if len(opt_values) != len(set(opt_values)):
            issues.append(f"[CONTENT] {path.name} {qid}: duplicate option texts")

        # 支援 A1 的 correctAnswer 或 A2/A3/B 的 answer
        ans = q.get('correctAnswer') if 'correctAnswer' in q else q.get('answer')
        if ans not in list('ABCD'):
            issues.append(f"[SCHEMA] {path.name} {qid}: invalid answer/correctAnswer={ans}")
        else:
            stats['correct_dist'][ans] += 1

        expl = (q.get('explanation') or '').strip()
        if not expl:
            stats['empty_explanations'] += 1
        # Forbidden phrases in question/explanation
        s = question + expl
        if any(p in s for p in FORBIDDEN_PHRASES):
            stats['forbidden_hits'] += 1
            issues.append(f"[STYLE] {path.name} {qid}: contains annex reference or forbidden phrase")

        # Tags
        tags = q.get('tags', [])
        if not isinstance(tags, list):
            issues.append(f"[SCHEMA] {path.name} {qid}: tags not a list")
        else:
            # empty tag string warn
            for t in tags:
                if not isinstance(t, str) or not t.strip():
                    issues.append(f"[SCHEMA] {path.name} {qid}: invalid tag entry")

        # Whitespace anomalies
        if question != q.get('question'):
            issues.append(f"[STYLE] {path.name} {qid}: leading/trailing spaces in question")
        for k in 'ABCD':
            if options.get(k) and options.get(k) != options.get(k).strip():
                issues.append(f"[STYLE] {path.name} {qid}: leading/trailing spaces in option {k}")
        if expl != q.get('explanation'):
            issues.append(f"[STYLE] {path.name} {qid}: leading/trailing spaces in explanation")

    # Exact-duplicate questions
    for (text, img), ids in dup_q_text.items():
        if text and len(ids) > 1:
            if img:
                issues.append(f"[DUP-Q] {path.name}: same question text and image for ids {ids}")
            else:
                issues.append(f"[DUP-Q] {path.name}: same question text for ids {ids}")

    return obj, issues, stats


def fix_safe_whitespace(obj: Dict) -> Tuple[Dict, int]:
    changed = 0
    for q in obj.get('questions', []):
        s = q.get('question')
        if isinstance(s, str):
            ns = s.strip()
            if ns != s:
                q['question'] = ns
                changed += 1
        for k in 'ABCD':
            s = q.get('options', {}).get(k)
            if isinstance(s, str):
                ns = s.strip()
                if ns != s:
                    q['options'][k] = ns
                    changed += 1
        s = q.get('explanation')
        if isinstance(s, str):
            ns = re.sub(r'\s+', ' ', s.strip())
            if ns != s:
                q['explanation'] = ns
                changed += 1
        tags = q.get('tags')
        if isinstance(tags, list):
            uniq = []
            for t in tags:
                if isinstance(t, str):
                    tt = t.strip()
                    if tt and tt not in uniq:
                        uniq.append(tt)
            if uniq != tags:
                q['tags'] = uniq
                changed += 1
    return obj, changed


def main(argv: List[str]) -> int:
    do_fix = '--fix' in argv
    overall_issues = []
    overall_stats = []

    for f in FILES:
        if not f.exists():
            print(f"Skip {f.name} (not found)")
            continue
        obj, issues, stats = validate_file(f)
        overall_issues.extend(issues)
        overall_stats.append(stats)
        print(f"Checked {f.name}: {stats['count_actual']} questions; empty_expl={stats['empty_explanations']}; forbidden_hits={stats['forbidden_hits']}; correctDist={stats['correct_dist']}")
        if do_fix:
            obj2, changed = fix_safe_whitespace(obj)
            if changed:
                # Keep totalQuestions in sync
                obj2['totalQuestions'] = len(obj2.get('questions', []))
                f.write_text(json.dumps(obj2, ensure_ascii=False, indent=2), encoding='utf-8')
                print(f"  Auto-fixed whitespace/tags: {changed} fields updated")

    # Summary
    print("\n=== Issues ===")
    if overall_issues:
        for it in overall_issues[:200]:
            print(it)
        if len(overall_issues) > 200:
            print(f"... and {len(overall_issues)-200} more")
    else:
        print("No issues found")

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
