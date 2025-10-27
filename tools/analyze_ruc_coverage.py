#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analyze coverage of Part B questions against Road Users' Code (Chinese) PDF.

Outputs:
  - synced/coverage_reports/ruc_coverage_summary.json
  - synced/coverage_reports/ruc_coverage_by_chapter.csv
  - synced/coverage_reports/ruc_uncovered_sections.csv

Usage:
  python tools/analyze_ruc_coverage.py [pdf_path] [partb_json]

Defaults:
  pdf_path: ./road_users_code_chi.pdf
  partb_json: ./part_b_questions.json
"""

import json
import re
import sys
from pathlib import Path
from collections import Counter


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PDF = ROOT / 'road_users_code_chi.pdf'
DEFAULT_PARTB = ROOT / 'part_b_questions.json'
OUT_DIR = ROOT / 'synced' / 'coverage_reports'


def norm(s: str) -> str:
    """Normalize strings for fuzzy match by stripping spaces and punctuation."""
    return re.sub(r'[\s\-–—_:：、,.．·“”"\(\)（）「」\[\]]+', '', s or '')


def load_questions(partb_path: Path):
    data = json.loads(partb_path.read_text(encoding='utf-8'))
    qs = data.get('questions', [])
    chap_counts = Counter()
    sec_counts = Counter()
    for q in qs:
        for t in (q.get('tags') or []):
            if t.startswith('chapter:'):
                chap_counts[t.split(':', 1)[1]] += 1
            elif t.startswith('section:'):
                sec_counts[t.split(':', 1)[1]] += 1
    return qs, chap_counts, sec_counts


def extract_toc(pdf_path: Path):
    """Use local helper script to extract ToC; fallback to saved JSON if needed."""
    toc_json_path = OUT_DIR / 'ruc_toc.json'
    try:
        # Import helper dynamically
        import importlib.util
        spec = importlib.util.spec_from_file_location('ruc', str(ROOT/'extract_ruc_toc.py'))
        ruc = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ruc)
        text = ruc.extract_text_first_pages(pdf_path)
        toc = ruc.parse_toc(text)
        # Save a copy for traceability
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        toc_json_path.write_text(json.dumps(toc, ensure_ascii=False, indent=2), encoding='utf-8')
        return toc
    except Exception as e:
        # Fallback to saved JSON if exists
        if toc_json_path.exists():
            return json.loads(toc_json_path.read_text(encoding='utf-8'))
        raise e


def compute_coverage(toc: dict, chap_counts: Counter, sec_counts: Counter):
    chapters = toc.get('chapters', [])
    # Chapter coverage
    toc_chaps = { norm(c.get('chapter', '')) for c in chapters if c.get('chapter') }
    q_chaps = { norm(k) for k in chap_counts.keys() }
    chap_covered = toc_chaps & q_chaps

    # Sections coverage via fuzzy contains
    # Build per-chapter section lists
    chapter_sections = []  # list of {chapter, sections:[{title,page}]}
    all_sec_titles = set()
    for c in chapters:
        secs = c.get('sections', [])
        chapter_sections.append({
            'chapter': c.get('chapter', ''),
            'sections': secs
        })
        for s in secs:
            all_sec_titles.add(s.get('title', ''))

    q_secs_norm = { norm(s): s for s in sec_counts.keys() }

    # For each chapter, count covered sections
    per_chapter = []
    for c in chapter_sections:
        ch = c['chapter']
        secs = c['sections']
        total_secs = len(secs)
        covered = 0
        uncovered_list = []
        for s in secs:
            t = s.get('title', '')
            nt = norm(t)
            matched = False
            for qn in q_secs_norm.keys():
                if len(qn) >= 2 and (qn in nt or nt in qn):
                    matched = True
                    break
            if matched:
                covered += 1
            else:
                uncovered_list.append({
                    'title': t,
                    'page': s.get('page')
                })
        per_chapter.append({
            'chapter': ch,
            'question_count': chap_counts.get(ch, 0),
            'toc_sections': total_secs,
            'covered_sections': covered,
            'covered_ratio': (covered / total_secs) if total_secs else None,
            'uncovered_sections': uncovered_list
        })

    # Overall sections coverage
    # Determine which ToC section titles are covered at least once
    covered_secs_set = set()
    for title in all_sec_titles:
        nt = norm(title)
        for qn in q_secs_norm.keys():
            if len(qn) >= 2 and (qn in nt or nt in qn):
                covered_secs_set.add(nt)
                break

    section_summary = {
        'covered_count': len(covered_secs_set),
        'total_toc_sections': len(all_sec_titles),
        'covered_ratio': (len(covered_secs_set)/len(all_sec_titles)) if all_sec_titles else None,
        'top_sections_by_questions': sec_counts.most_common(20),
    }

    chapter_summary = {
        'covered_count': len(chap_covered),
        'total_toc_chapters': len(toc_chaps),
        'covered_ratio': (len(chap_covered)/len(toc_chaps)) if toc_chaps else None,
        'top_chapters_by_questions': chap_counts.most_common(10)
    }

    return per_chapter, chapter_summary, section_summary


def write_reports(per_chapter, chapter_summary, section_summary, questions_total):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    summary = {
        'generated_from': 'analyze_ruc_coverage.py',
        'questions_total': questions_total,
        'chapters': chapter_summary,
        'sections': section_summary,
        'per_chapter': per_chapter,
    }
    (OUT_DIR / 'ruc_coverage_summary.json').write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')

    # CSV: by chapter
    lines = [
        'chapter,question_count,toc_sections,covered_sections,covered_ratio'
    ]
    for row in per_chapter:
        ratio = '' if row['covered_ratio'] is None else f"{row['covered_ratio']:.3f}"
        lines.append(
            f"{row['chapter']},{row['question_count']},{row['toc_sections']},{row['covered_sections']},{ratio}"
        )
    (OUT_DIR / 'ruc_coverage_by_chapter.csv').write_text("\n".join(lines), encoding='utf-8')

    # CSV: uncovered sections
    lines = ['chapter,page,title']
    for row in per_chapter:
        for s in row['uncovered_sections']:
            title = (s.get('title') or '').replace('\n', ' ').replace(',', '，')
            page = s.get('page')
            lines.append(f"{row['chapter']},{page},{title}")
    (OUT_DIR / 'ruc_uncovered_sections.csv').write_text("\n".join(lines), encoding='utf-8')


def main():
    pdf_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PDF
    partb_path = Path(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_PARTB

    if not pdf_path.exists():
        print(f"ERROR: PDF not found: {pdf_path}")
        sys.exit(2)
    if not partb_path.exists():
        print(f"ERROR: Part B JSON not found: {partb_path}")
        sys.exit(3)

    qs, chap_counts, sec_counts = load_questions(partb_path)
    toc = extract_toc(pdf_path)
    per_chapter, chapter_summary, section_summary = compute_coverage(toc, chap_counts, sec_counts)
    write_reports(per_chapter, chapter_summary, section_summary, questions_total=len(qs))
    # Print a short console summary
    print(json.dumps({
        'questions_total': len(qs),
        'chapter_covered': chapter_summary['covered_count'],
        'chapters_total': chapter_summary['total_toc_chapters'],
        'chapter_ratio': round(chapter_summary['covered_ratio'], 3) if chapter_summary['covered_ratio'] is not None else None,
        'section_covered': section_summary['covered_count'],
        'sections_total': section_summary['total_toc_sections'],
        'section_ratio': round(section_summary['covered_ratio'], 3) if section_summary['covered_ratio'] is not None else None,
    }, ensure_ascii=False))


if __name__ == '__main__':
    main()
