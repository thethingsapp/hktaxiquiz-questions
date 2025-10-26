#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extract table of contents from Road Users' Code (Chinese, 2020) PDF.
Outputs JSON of chapters and sections with page numbers (as integers when parsable).

Usage:
  python extract_ruc_toc.py [pdf_path]

Default pdf_path: ./road_users_code_chi.pdf
"""

import sys
import json
import re
from pathlib import Path

try:
    from PyPDF2 import PdfReader
except Exception as e:
    print("ERROR: PyPDF2 not available:", e, file=sys.stderr)
    sys.exit(1)

CHAPTER_RE = re.compile(r"^(第[一二三四五六七八九十]+章)\s*(.+)?$")
SECTION_RE = re.compile(r"^\s*(\d{1,3})\s+(.+?)\s*$")


def extract_text_first_pages(pdf_path: Path, first_n: int = 8) -> str:
    with pdf_path.open('rb') as f:
        r = PdfReader(f)
        n = min(first_n, len(r.pages))
        texts = []
        for i in range(n):
            try:
                t = r.pages[i].extract_text() or ''
            except Exception:
                t = ''
            texts.append(t)
        return "\n".join(texts)


def parse_toc(text: str):
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    # Find index of 目錄
    try:
        idx = next(i for i, ln in enumerate(lines) if '目錄' in ln)
    except StopIteration:
        idx = 0  # fallback: start from beginning

    chapters = []
    cur = None

    for ln in lines[idx:]:
        m_ch = CHAPTER_RE.match(ln)
        if m_ch:
            # start new chapter
            if cur:
                chapters.append(cur)
            ch_no = m_ch.group(1)
            ch_title = (m_ch.group(2) or '').strip()
            cur = {
                'chapter': ch_no,
                'title': ch_title,
                'sections': []
            }
            continue
        m_sec = SECTION_RE.match(ln)
        if m_sec and cur is not None:
            page_s = m_sec.group(1)
            title = m_sec.group(2)
            try:
                page = int(page_s)
            except ValueError:
                page = page_s
            cur['sections'].append({'page': page, 'title': title})
    if cur:
        chapters.append(cur)
    return {'chapters': chapters}


def main():
    pdf_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('road_users_code_chi.pdf')
    if not pdf_path.exists():
        print(f"ERROR: PDF not found: {pdf_path}", file=sys.stderr)
        sys.exit(2)
    text = extract_text_first_pages(pdf_path)
    toc = parse_toc(text)
    print(json.dumps(toc, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
