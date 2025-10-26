#!/usr/bin/env python3
from pathlib import Path
import sys
try:
    import PyPDF2
except Exception as e:
    print('PyPDF2 not available', e)
    sys.exit(2)

PDF = Path(__file__).resolve().parents[1]/'taxi_operation_booklet_tc_20250918.pdf'
OUT = Path(__file__).resolve().parents[1]/'extracted_questions_from_pdf.txt'

if not PDF.exists():
    print('PDF not found:', PDF)
    sys.exit(3)

text = ''
with open(PDF, 'rb') as f:
    r = PyPDF2.PdfReader(f)
    for i,p in enumerate(r.pages):
        t = ''
        try:
            t = p.extract_text() or ''
        except Exception:
            t = ''
        text += f"\n\n=== 第 {i+1} 頁 ===\n\n" + t

OUT.write_text(text, encoding='utf-8')
print('Saved to', OUT)
