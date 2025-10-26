from pypdf import PdfReader
from pathlib import Path
import re

pdf_path = Path('/Users/louiswong/Desktop/development/hktaxiquiz-questions/taxi_operation_booklet_tc_20250918.pdf')
reader = PdfReader(str(pdf_path))
print('Pages:', len(reader.pages))

terms = ['計程錶', '拒載', '收據', '失物', '罰款', '監禁', '導盲犬', '動物', '安全帶', '車費', '附加費', '司機', '的士駕駛執照', '車主', '乘客', '的士站', '路線', '行車紀錄', '身份證明', '酒精', '毒品']

hits = {t: [] for t in terms}
for i, page in enumerate(reader.pages):
    text = (page.extract_text() or '').replace('\n', ' ')
    for term in terms:
        if term in text:
            hits[term].append(i+1)

for term, pages in hits.items():
    if pages:
        print(f"{term}: pages {pages[:12]}{'...' if len(pages)>12 else ''}")

# Print small snippets for a subset of core terms
core_terms = ['計程錶', '拒載', '收據', '失物', '導盲犬', '動物', '安全帶', '的士駕駛執照', '的士站']
print('\n=== Snippets ===')
for i, page in enumerate(reader.pages):
    text = (page.extract_text() or '').replace('\n', ' ')
    for term in core_terms:
        m = re.search(term, text)
        if m:
            start = max(0, m.start()-80)
            end = min(len(text), m.end()+200)
            print(f"[p{i+1}] {term}: ...{text[start:end]}...")
