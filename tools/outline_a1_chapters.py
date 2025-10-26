from pypdf import PdfReader
import re
from pathlib import Path
from collections import defaultdict

pdf_path = Path('/Users/louiswong/Desktop/development/hktaxiquiz-questions/taxi_operation_booklet_tc_20250918.pdf')
reader = PdfReader(str(pdf_path))

# Extract full text per page
pages = [(i+1, (p.extract_text() or '')) for i, p in enumerate(reader.pages)]

# Simple heading patterns: Chinese number + '、' at line start; also '附錄' headings
heading_pat = re.compile(r'^(?:[一二三四五六七八九十]{1,3}、\s*[^\n]+|附錄[甲乙丙丁戊己庚辛壬癸]\s*[^\n]*)', re.M)

chapters = []
for pno, text in pages:
    for m in heading_pat.finditer(text):
        title = m.group(0).strip()
        chapters.append((pno, title))

# Group content between headings
chapters_sorted = sorted(chapters, key=lambda x: (x[0], x[1]))
sections = []
for idx, (pno, title) in enumerate(chapters_sorted):
    # Determine end boundary
    end_page = pages[-1][0]
    start_index = next(i for i,(pn,_) in enumerate(pages) if pn == pno)
    if idx+1 < len(chapters_sorted):
        next_pno, _ = chapters_sorted[idx+1]
        end_index = next(i for i,(pn,_) in enumerate(pages) if pn == next_pno)
    else:
        end_index = len(pages)
    # Concatenate text from start_index page (from match onward) to end_index-1 page
    start_text = pages[start_index][1]
    start_pos = start_text.find(title)
    content = start_text[start_pos:]
    for j in range(start_index+1, end_index):
        content += '\n' + pages[j][1]
    sections.append((title, content))

# Heuristics for question potential
num_pat = re.compile(r'(HK\$|\$)?\s?\d+[\d,]*(?:\.\d+)?')
units_pat = re.compile(r'(毫米|米|公里|分鐘|秒|小時|日|月|年)')
item_pat = re.compile(r'\([0-9]{1,2}\)')
obligation_terms = ['不得', '必須', '需要', '應', '禁止', '可拒絕', '違法', '罰款', '監禁', '記分']

report = []

def estimate_questions(text: str) -> dict:
    # Features
    nums = len(num_pat.findall(text))
    units = len(units_pat.findall(text))
    items = len(item_pat.findall(text))
    obligations = sum(text.count(t) for t in obligation_terms)
    length = len(text)
    # Simple scoring heuristic
    score = items * 1.2 + (nums + units) * 0.5 + obligations * 0.8 + (length/4000)
    # Convert to range (min 2 per substantial section)
    low = max(1, int(score*0.6))
    high = max(low+1, int(score*1.1)+1)
    # Cap extremes
    low = min(low, 15)
    high = min(high, 25)
    return {
        'nums': nums, 'units': units, 'items': items, 'obligations': obligations, 'len': length,
        'estimate_low': low, 'estimate_high': high
    }

summary = []

total_low = 0
total_high = 0
for title, content in sections:
    est = estimate_questions(content)
    total_low += est['estimate_low']
    total_high += est['estimate_high']
    summary.append((title, est))

print('Detected sections (ordered):')
for title, est in summary:
    print(f"- {title}: ~{est['estimate_low']}–{est['estimate_high']} 題 (nums={est['nums']}, units={est['units']}, items={est['items']}, oblig={est['obligations']})")

print(f"\nTotal potential: ~{total_low}–{total_high} 題")
