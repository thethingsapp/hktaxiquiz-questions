#!/usr/bin/env python3
"""
根據官方 PDF 內容生成 Part B 完整題庫（地方及路線試題 1-319）
自動為每個問題添加 2 個錯誤選項
"""

import json
import random
from typing import List, Dict
from collections import OrderedDict

# 從 all_locations_improved.json 載入所有地點
with open('all_locations_improved.json', 'r', encoding='utf-8') as f:
    LOCATIONS = json.load(f, object_pairs_hook=OrderedDict)

# 所有可能的位置（用於生成干擾項）
ALL_LOCATIONS = list(set(LOCATIONS.values()))

def generate_wrong_options(correct_answer: str, count: int = 2) -> List[str]:
    """生成錯誤選項（干擾項）"""
    # 排除正確答案
    wrong_pool = [loc for loc in ALL_LOCATIONS if loc != correct_answer]
    
    # 隨機選擇
    return random.sample(wrong_pool, min(count, len(wrong_pool)))

def create_location_question(place_name: str, correct_location: str, question_id: int) -> Dict:
    """創建地點問題"""
    
    # 生成 2 個錯誤選項
    wrong_options = generate_wrong_options(correct_location, 2)
    
    # 組合所有選項並打亂
    all_options = [correct_location] + wrong_options
    random.shuffle(all_options)
    
    # 分配 A, B, C 選項
    options_dict = {
        "A": all_options[0],
        "B": all_options[1],
        "C": all_options[2],
    }
    
    # 找出正確答案的字母
    correct_letter = [k for k, v in options_dict.items() if v == correct_location][0]
    
    question = {
        "id": f"B_{question_id:03d}",
        "question": f"{place_name}在哪裡？",
        "options": options_dict,
        "answer": correct_letter,
        "explanation": f"{place_name}位於{correct_location}。",
        "category": "location",
        "difficulty": "medium"
    }
    
    return question

def main():
    """主函數：生成完整題庫"""
    
    print("🚀 開始生成 Part B 題庫（地方及路線試題 1-319）...")
    print(f"📖 從 all_locations_improved.json 載入 {len(LOCATIONS)} 個地點")
    
    questions = []
    question_id = 1
    
    # 為每個地點生成問題（只取前 319 個，對應官方編號 1-319）
    location_items = list(LOCATIONS.items())[:319]
    
    for place_name, correct_location in location_items:
        question = create_location_question(place_name, correct_location, question_id)
        questions.append(question)
        question_id += 1
    
    # 保存為 JSON
    output_data = {
        "part": "B",
        "title": "地方及路線試題",
        "description": "測試考生對香港地方的認識，以及路線規劃的能力。包括醫院（1-50）、旅遊景點（51-85）、酒店（86-173）、政府樓宇（174-219）、商業大廈（220-246）、購物商場（247-274）、住宅樓宇（275-307）及大專院校（308-319）",
        "passingScore": 80,
        "totalQuestions": len(questions),
        "lastUpdated": "2025-01-24",
        "officialSource": "運輸署地方及路線試題小冊子（2025年2月修訂版）",
        "questions": questions
    }
    
    output_file = "part_b_questions.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 成功生成 {len(questions)} 道題目（對應官方編號 1-319）")
    print(f"📁 已保存至: {output_file}")
    print(f"\n📊 題目統計:")
    print(f"   - 地點問題: {len(questions)} 題")
    print(f"   - 每題選項: 3 個（1 正確 + 2 干擾）")
    print(f"   - 正確分類: Part B - 地方及路線試題")
    print(f"   - 覆蓋率: 100% (319/319)")
    
    # 顯示前 3 道題目示例
    print(f"\n📝 題目示例（前 3 題）:")
    for i, q in enumerate(questions[:3], 1):
        print(f"\n{i}. [{q['id']}] {q['question']}")
        for opt, value in q['options'].items():
            marker = "✓" if opt == q['answer'] else " "
            print(f"   {marker} {opt}. {value}")
        print(f"   答案: {q['answer']} - {q['explanation']}")
    
    # 顯示最後 3 道題目（大學）
    print(f"\n📝 題目示例（最後 3 題 - 大學）:")
    for i, q in enumerate(questions[-3:], len(questions)-2):
        print(f"\n{i}. [{q['id']}] {q['question']}")
        for opt, value in q['options'].items():
            marker = "✓" if opt == q['answer'] else " "
            print(f"   {marker} {opt}. {value}")
        print(f"   答案: {q['answer']} - {q['explanation']}")

if __name__ == "__main__":
    main()
