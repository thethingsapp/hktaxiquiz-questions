#!/usr/bin/env python3
import json
from collections import Counter, defaultdict
from pathlib import Path
import re

# Load A1 questions
p = Path(__file__).resolve().parents[1]/'part_a1_questions.json'
obj = json.loads(p.read_text(encoding='utf-8'))
qs = obj['questions']

# Normalized tags per question
qtags = []
for q in qs:
    tags = [t.strip() for t in q.get('tags', [])]
    qtags.append((q['id'], tags, q.get('question','')))

# Topic mapping heuristics
# Each topic: name -> list of keywords to match against tags or question text
TOPICS = {
    '一 計程錶': ['計程錶','旗','FOR HIRE','HIRED','STOPPED','收據打印設備'],
    '二 收據打印設備': ['收據','收據打印','打印設備'],
    '三 行車記錄系統': ['行車記錄','紀錄器','行車記錄系統'],
    '四 照明標誌與標記': ['標誌','標記','車頂','照明'],
    '五 上落乘客': ['上落','乘客','的士站','站頭'],
    '六 租用': ['租用','預約','約定時間','供出租'],
    '七 的士收費': ['收費','車費','附加費','的士收費'],
    '八 出租車輛': ['車輛','車身','車牌','維修','保養'],
    '九 的士車隊': ['車隊','車隊的士'],
    '十 運載貨物': ['貨物','行李','載貨'],
    '十一 運載動物雀鳥': ['動物','雀鳥','導盲犬','輔助犬'],
    '十二 失物': ['失物','遺失物','失物處理'],
    '十三 安全帶': ['安全帶','兒童','增高座椅'],
    '十四 司機操守': ['操守','行為','禮貌','拒載','醉酒','毒品','騷擾'],
    '十五 違例記分制度': ['記分','違例','扣分','不誠實','拒載記分'],
    # 附錄：嚴格以「附錄X」字樣匹配，避免與一般主題重疊
    '附錄甲 收據格式': ['附錄甲'],
    '附錄乙 手寫收據': ['附錄乙'],
    '附錄丙 的士收費': ['附錄丙'],
    '附錄丁 車隊識別牌': ['附錄丁'],
    '附錄戊 車隊停車處標記': ['附錄戊'],
    '附錄己 記分制': ['附錄己'],
}

# Tally by topic using tags first, then fallback to question text keyword
counts = Counter()
examples = defaultdict(list)
for qid, tags, text in qtags:
    joined = '\n'.join(tags)
    for topic, kws in TOPICS.items():
        hit = False
        for kw in kws:
            # keyword can be ascii words or chinese; match in tags or question
            if kw in joined or kw in text:
                hit = True
                break
        if hit:
            counts[topic] += 1
            if len(examples[topic]) < 2:
                examples[topic].append(qid)

# Print report
total = len(qs)
print(f"A1 題庫總數: {total}")

for topic in TOPICS.keys():
    c = counts.get(topic, 0)
    ex = ', '.join(examples.get(topic, []))
    print(f"- {topic}: {c} 題 例: {ex}")

covered = sum(counts.values())
print(f"\n按主題匹配到的題數（有交疊可能）: {covered}")
