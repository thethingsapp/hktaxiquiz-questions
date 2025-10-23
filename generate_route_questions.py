#!/usr/bin/env python3
"""
生成 Part B 路線問題（320-356 題）
為每個路線問題生成 3 個選項：1 正確 + 2 干擾項
"""

import json
import random
from collections import OrderedDict

# 載入路線數據
with open('route_questions_raw.json', 'r', encoding='utf-8') as f:
    ROUTE_DATA = json.load(f)

def generate_route_distractors(correct_route: str, all_routes: list) -> list:
    """
    生成路線干擾項
    策略：選擇其他真實路線作為干擾項，更真實
    """
    # 排除正確路線
    other_routes = [r for r in all_routes if r != correct_route]
    
    # 隨機選擇 2 個作為干擾項
    return random.sample(other_routes, min(2, len(other_routes)))

def create_route_question(question_num: int, route_data: dict, all_routes: list) -> dict:
    """創建單個路線問題"""
    
    start = route_data['start']
    destination = route_data['destination']
    correct_route = route_data['route']
    
    # 生成干擾項
    wrong_routes = generate_route_distractors(correct_route, all_routes)
    
    # 組合所有選項並打亂
    all_options = [correct_route] + wrong_routes
    random.shuffle(all_options)
    
    # 分配選項字母
    options_dict = {
        "A": all_options[0],
        "B": all_options[1],
        "C": all_options[2],
    }
    
    # 找出正確答案的字母
    correct_letter = [k for k, v in options_dict.items() if v == correct_route][0]
    
    question = {
        "id": f"B_{question_num:03d}",
        "question": f"從{start}前往{destination}，最直接可行的路線是？",
        "options": options_dict,
        "answer": correct_letter,
        "explanation": f"從{start}前往{destination}，最直接可行的路線是：{correct_route}",
        "category": "route",
        "difficulty": "hard"
    }
    
    return question

def main():
    """主函數：生成路線題庫"""
    
    print("🚀 開始生成 Part B 路線題庫（320-356 題）...")
    
    # 收集所有路線（用於生成干擾項）
    all_routes = [data['route'] for data in ROUTE_DATA.values()]
    
    questions = []
    
    # 為每個路線生成問題
    for question_num_str, route_data in ROUTE_DATA.items():
        question_num = int(question_num_str)
        question = create_route_question(question_num, route_data, all_routes)
        questions.append(question)
    
    # 保存為 JSON
    output_data = {
        "part": "B",
        "title": "地方及路線試題 - 路線部分",
        "description": "測試考生對香港路線規劃的能力。考生需要選擇從起點到目的地的最直接可行路線。",
        "passingScore": 80,
        "totalQuestions": len(questions),
        "lastUpdated": "2025-10-24",
        "officialSource": "運輸署地方及路線試題小冊子（2024年12月修訂版）",
        "questions": questions
    }
    
    output_file = "part_b_route_questions.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 成功生成 {len(questions)} 道路線題目（320-356）")
    print(f"📁 已保存至: {output_file}")
    print(f"\n📊 題目統計:")
    print(f"   - 路線問題: {len(questions)} 題")
    print(f"   - 每題選項: 3 個（1 正確 + 2 干擾）")
    print(f"   - 難度: 困難 (hard)")
    print(f"   - 覆蓋率: 100% (37/37)")
    
    # 顯示前 2 道題目示例
    print(f"\n📝 題目示例（前 2 題）:")
    for i, q in enumerate(questions[:2], 320):
        print(f"\n{i}. [{q['id']}] {q['question']}")
        for opt, value in q['options'].items():
            marker = "✓" if opt == q['answer'] else " "
            # 截斷長路線顯示
            display_value = value if len(value) <= 60 else value[:57] + "..."
            print(f"   {marker} {opt}. {display_value}")
        print(f"   答案: {q['answer']}")
    
    # 顯示最後 1 道題目
    print(f"\n📝 題目示例（最後 1 題）:")
    q = questions[-1]
    print(f"\n356. [{q['id']}] {q['question']}")
    for opt, value in q['options'].items():
        marker = "✓" if opt == q['answer'] else " "
        display_value = value if len(value) <= 60 else value[:57] + "..."
        print(f"   {marker} {opt}. {display_value}")
    print(f"   答案: {q['answer']}")

if __name__ == "__main__":
    main()
