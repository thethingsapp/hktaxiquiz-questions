#!/usr/bin/env python3
from pdfminer.high_level import extract_text
from PyPDF2 import PdfReader
import os, sys

pdf_path = "/Users/louiswong/Desktop/development/hktaxiquiz-questions/taxi_operation_booklet_tc_20250918.pdf"
if not os.path.exists(pdf_path):
    print("PDF not found:", pdf_path)
    sys.exit(1)

reader = PdfReader(pdf_path)
num_pages = len(reader.pages)
print("Total pages:", num_pages)

hits = []
for i in range(num_pages):
    try:
        text = extract_text(pdf_path, page_numbers=[i]) or ""
    except Exception:
        text = ""
    if ("最直接可行的路線是" in text) or ("路線問題" in text):
        hits.append(i)
        print(f"Hit on page {i+1}")
        if len(hits) >= 5:
            break

print("First hits:", [h+1 for h in hits])

if hits:
    start_page = max(0, hits[0]-1)
    buf = []
    for i in range(start_page, min(start_page+6, num_pages)):
        try:
            part = extract_text(pdf_path, page_numbers=[i]) or ""
        except Exception:
            part = ""
        buf.append(part)
    aggregate = "\n".join(buf)
    for needle in ["231", "232", "233", "從", "最直接可行的路線是"]:
        pos = aggregate.find(needle)
        print(f"Needle '{needle}' at:", pos)
    idx = aggregate.find("231")
    if idx != -1:
        print("\nContext around 231:\n")
        print(aggregate[max(0, idx-200): idx+1500])
    else:
        print("\nAggregate snippet:\n")
        print(aggregate[:1800])
