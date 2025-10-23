#!/usr/bin/env python3
"""
合併 Part B 地點題（1-319）和路線題（320-356）
生成完整的 Part B 題庫（1-356）
"""

import json

def main():
    """合併兩個題庫"""
    
    print("🚀 合併 Part B 題庫...")
    
    # 載入地點題
    with open('part_b_questions.json', 'r', encoding='utf-8') as f:
        location_data = json.load(f)
    
    # 載入路線題
    with open('part_b_route_questions.json', 'r', encoding='utf-8') as f:
        route_data = json.load(f)
    
    print(f"📖 地點題: {len(location_data['questions'])} 題 (1-319)")
    print(f"📖 路線題: {len(route_data['questions'])} 題 (320-356)")
    
    # 合併問題
    all_questions = location_data['questions'] + route_data['questions']
    
    # 創建完整題庫
    complete_data = {
        "part": "B",
        "title": "地方及路線試題",
        "description": "測試考生對香港地方的認識，以及路線規劃的能力。包括地點問題（1-319）：醫院、旅遊景點、酒店、政府樓宇、商業大廈、購物商場、住宅樓宇及大專院校；路線問題（320-356）：從起點到目的地的最直接可行路線。",
        "passingScore": 80,
        "totalQuestions": len(all_questions),
        "lastUpdated": "2025-10-24",
        "officialSource": "運輸署地方及路線試題小冊子（2025年2月修訂版 + 2024年12月修訂版）",
        "sections": [
            {
                "name": "地點問題",
                "range": "1-319",
                "count": 319,
                "categories": [
                    {"name": "醫院", "range": "1-50", "count": 50},
                    {"name": "旅遊景點", "range": "51-85", "count": 35},
                    {"name": "酒店", "range": "86-173", "count": 88},
                    {"name": "政府樓宇", "range": "174-219", "count": 46},
                    {"name": "商業大廈", "range": "220-246", "count": 27},
                    {"name": "購物商場", "range": "247-274", "count": 28},
                    {"name": "住宅樓宇", "range": "275-307", "count": 33},
                    {"name": "大專院校", "range": "308-319", "count": 12}
                ]
            },
            {
                "name": "路線問題",
                "range": "320-356",
                "count": 37
            }
        ],
        "questions": all_questions
    }
    
    # 保存合併後的題庫
    output_file = "part_b_complete_questions.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(complete_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 成功合併 {len(all_questions)} 道題目")
    print(f"📁 已保存至: {output_file}")
    print(f"\n📊 完整題庫統計:")
    print(f"   - 地點問題: 319 題 (B_001 - B_319)")
    print(f"   - 路線問題: 37 題 (B_320 - B_356)")
    print(f"   - 總計: {len(all_questions)} 題")
    print(f"   - 覆蓋率: 100% (356/356)")
    
    # 驗證 ID 連續性
    ids = [q['id'] for q in all_questions]
    expected_ids = [f"B_{i:03d}" for i in range(1, 357)]
    
    if ids == expected_ids:
        print(f"\n✅ ID 連續性檢查: 通過 (B_001 → B_356)")
    else:
        print(f"\n❌ ID 連續性檢查: 失敗")
        missing = set(expected_ids) - set(ids)
        if missing:
            print(f"   缺少: {sorted(missing)[:10]}...")
    
    # 檢查檔案大小
    import os
    file_size = os.path.getsize(output_file)
    print(f"\n📦 檔案大小: {file_size/1024:.1f} KB")
    
    # 顯示關鍵題目
    print(f"\n🔍 關鍵題目檢查:")
    key_indices = [0, 49, 84, 218, 273, 306, 318, 319, -1]
    key_labels = ["第1題(地點)", "第50題(醫院結束)", "第85題(景點結束)", 
                  "第219題(政府結束)", "第274題(商場結束)", "第307題(住宅結束)",
                  "第319題(地點結束)", "第320題(路線開始)", "第356題(路線結束)"]
    
    for idx, label in zip(key_indices, key_labels):
        q = all_questions[idx]
        question_text = q['question'][:50] + "..." if len(q['question']) > 50 else q['question']
        print(f"   {label}: {q['id']} - {question_text}")

if __name__ == "__main__":
    main()
