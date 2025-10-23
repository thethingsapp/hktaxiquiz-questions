#!/usr/bin/env python3
"""
根據官方 PDF 內容生成 Part C 完整題庫
自動為每個問題添加 2 個錯誤選項
"""

import json
import random
from typing import List, Dict

# 從 PDF 提取的地點資料（示例）
LOCATIONS = {
    # 醫院
    "瑪麗醫院": "薄扶林",
    "威爾斯親王醫院": "沙田",
    "贊育醫院": "西營盤",
    "東華醫院": "上環",
    "東華三院馮堯敬醫院": "薄扶林",
    "葛量洪醫院": "黃竹坑",
    "東區尤德夫人那打素醫院": "柴灣",
    "東華東院": "大坑",
    "鄧肇堅醫院": "灣仔",
    "律敦治醫院": "灣仔",
    "黃竹坑醫院": "黃竹坑徑",
    "伊利沙伯醫院": "油麻地",
    "九龍醫院": "九龍城",
    "香港佛教醫院": "樂富",
    "香港眼科醫院": "九龍城",
    "東華三院黃大仙醫院": "沙田坳道",
    "聖母醫院": "黃大仙",
    "廣華醫院": "油麻地",
    "明愛醫院": "長沙灣",
    "瑪嘉烈醫院": "荔景",
    "葵涌醫院": "荔景",
    "仁濟醫院": "荃灣",
    "基督教聯合醫院": "秀茂坪",
    "靈實醫院": "將軍澳",
    "將軍澳醫院": "寶寧里",
    "沙田醫院": "亞公角街",
    "雅麗氏何妙齡那打素醫院": "大埔",
    "大埔醫院": "全安路",
    "北區醫院": "上水",
    "屯門醫院": "青松觀路",
    "博愛醫院": "元朗",
    "嘉諾撒醫院": "半山",
    "明德國際醫院": "山頂",
    "香港港安醫院": "跑馬地",
    "聖保祿醫院": "東院道",
    "養和醫院": "跑馬地",
    "寶血醫院（明愛）": "深水埗",
    "播道醫院": "九龍城",
    "聖德肋撒醫院": "九龍城",
    "香港浸信會醫院": "九龍塘",
    "荃灣港安醫院": "荃景圍",
    "仁安醫院": "富健街",
    "青山醫院": "屯門",
    "小欖醫院": "青松觀路",
    "大口環根德公爵夫人兒童醫院": "薄扶林",
    "北大嶼山醫院": "松仁路",
    
    # 新增地點（2025年修訂）
    "啟德郵輪碼頭": "承豐道",
    "香港故宮文化博物館": "博物館道",
    "戲曲中心": "柯士甸道西",
    "香港麗晶酒店": "尖沙咀",
    "名迪港島酒店": "摩頓臺",
    "香港富麗敦海洋公園酒店": "香港仔",
    "麗豪航天城酒店": "赤鱲角",
    "西九龍政府合署": "海庭道",
    "入境事務處總部": "將軍澳",
    "機電工程署總部大樓": "啟成街",
    "美麗華廣場": "尖沙咀",
    "世貿中心": "告士打道",
    "AIRSIDE": "啟德",
    "圍方": "車公廟路",
    "APM": "觀塘",
    "V Walk": "深旺道",
    "富榮花園": "海庭道",
    "海山樓": "鰂魚涌",
    "嘉匯": "沐寧街",
    "擎天半島": "柯士甸道西",
    "形點": "朗日路",
    "聖方濟各大學": "翠嶺里",
    
    # 旅遊景點
    "九龍寨城公園": "九龍城",
    "昂坪纜車-東涌纜車站": "達東路",
    "香港海洋公園": "黃竹坑",
    "寶蓮禪寺": "昂坪",
    "凌霄閣": "山頂道",
    "亞洲國際博覽館": "赤鱲角",
    "屏山文物徑": "元朗",
    "香港會議展覽中心": "灣仔",
    "香港文化博物館": "沙田",
}

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
    
    print("🚀 開始生成 Part B 題庫（地方及路線試題）...")
    
    questions = []
    question_id = 1
    
    # 為每個地點生成問題
    for place_name, correct_location in LOCATIONS.items():
        question = create_location_question(place_name, correct_location, question_id)
        questions.append(question)
        question_id += 1
    
    # 保存為 JSON
    output_data = {
        "part": "B",
        "title": "地方及路線試題",
        "description": "測試考生對香港地方的認識，以及路線規劃的能力。包括醫院、旅遊景點、酒店、政府樓宇、商業大廈、購物商場、住宅樓宇及大專院校",
        "passingScore": 80,
        "totalQuestions": len(questions),
        "lastUpdated": "2025-10-24",
        "officialSource": "運輸署地方及路線試題小冊子（2025年2月修訂版）",
        "questions": questions
    }
    
    output_file = "part_b_questions.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 成功生成 {len(questions)} 道題目")
    print(f"📁 已保存至: {output_file}")
    print(f"\n📊 題目統計:")
    print(f"   - 地點問題: {len(questions)} 題")
    print(f"   - 每題選項: 3 個（1 正確 + 2 干擾）")
    print(f"   - 正確分類: Part B - 地方及路線試題")
    
    # 顯示前 3 道題目示例
    print(f"\n📝 題目示例:")
    for i, q in enumerate(questions[:3], 1):
        print(f"\n{i}. [{q['id']}] {q['question']}")
        for opt, value in q['options'].items():
            marker = "✓" if opt == q['answer'] else " "
            print(f"   {marker} {opt}. {value}")
        print(f"   答案: {q['answer']} - {q['explanation']}")

if __name__ == "__main__":
    main()
