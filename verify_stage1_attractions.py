#!/usr/bin/env python3
"""
分階段驗證官方地點題庫
"""

import json

# 官方地點列表
OFFICIAL_LOCATIONS = {
    # 旅遊景點 51-85 (35個)
    "attractions": {
        51: ("星光大道", "尖沙咀"),
        52: ("金紫荊廣場", "灣仔"),
        53: ("香港迪士尼樂園", "竹篙灣"),
        54: ("香港濕地公園", "天水圍"),
        55: ("玉器市場", "油麻地"),
        56: ("九龍寨城公園", "九龍城"),
        57: ("昂坪纜車-東涌纜車站", "達東路"),
        58: ("香港海洋公園", "黃竹坑"),
        59: ("寶蓮禪寺", "昂坪"),
        60: ("凌霄閣", "山頂道"),
        61: ("亞洲國際博覽館", "赤鱲角"),
        62: ("屏山文物徑", "元朗"),
        63: ("香港會議展覽中心", "灣仔"),
        64: ("香港文化博物館", "沙田"),
        65: ("香港歷史博物館", "尖沙咀"),
        66: ("香港科學館", "尖沙咀"),
        67: ("香港太空館", "尖沙咀"),
        68: ("香港大會堂", "中環"),
        69: ("香港體育館", "紅磡"),
        70: ("香港文化中心", "尖沙咀"),
        71: ("伊利沙伯體育館", "灣仔"),
        72: ("沙田大會堂", "源禾路"),
        73: ("尖沙咀天星碼頭", "尖沙咀"),
        74: ("1881", "廣東道"),
        75: ("沙田車公廟", "大圍"),
        76: ("文武廟", "上環"),
        77: ("林村許願廣場", "大埔"),
        78: ("龍躍頭文物徑", "粉嶺"),
        79: ("美利樓", "赤柱"),
        80: ("和昌大押", "莊士敦道"),
        81: ("大館", "荷李活道"),
        82: ("香港藝術館", "尖沙咀"),
        83: ("啟德郵輪碼頭", "承豐道"),
        84: ("香港故宮文化博物館", "博物館道"),
        85: ("戲曲中心", "柯士甸道西"),
    }
}

def verify_section(section_name, official_data, extracted_data):
    """驗證某一部分的數據"""
    print(f"\n{'='*70}")
    print(f"🔍 檢查：{section_name}")
    print(f"{'='*70}")
    
    correct = 0
    incorrect = []
    missing = []
    
    for num, (name, location) in official_data.items():
        # 處理可能的名稱變體
        name_variants = [
            name,
            name.replace("-", ""),
            name.replace("  ", " "),
            name.replace(" ", ""),
        ]
        
        found = False
        extracted_loc = None
        
        for variant in name_variants:
            if variant in extracted_data:
                extracted_loc = extracted_data[variant]
                found = True
                break
        
        if found:
            if extracted_loc == location:
                correct += 1
                print(f"✅ {num:3d}. {name:35s} → {location}")
            else:
                incorrect.append((num, name, location, extracted_loc))
                print(f"❌ {num:3d}. {name:35s} → 官方:{location} | 我們:{extracted_loc}")
        else:
            missing.append((num, name, location))
            print(f"⚠️  {num:3d}. {name:35s} → {location} (缺失)")
    
    total = len(official_data)
    print(f"\n{'='*70}")
    print(f"📊 統計結果:")
    print(f"   ✅ 正確: {correct}/{total} ({correct/total*100:.1f}%)")
    print(f"   ❌ 錯誤: {len(incorrect)}/{total}")
    print(f"   ⚠️  缺失: {len(missing)}/{total}")
    
    return {
        'correct': correct,
        'incorrect': incorrect,
        'missing': missing,
        'total': total
    }

def main():
    # 載入提取的數據
    with open('all_locations_improved.json', 'r', encoding='utf-8') as f:
        extracted = json.load(f)
    
    print(f"📖 已載入 {len(extracted)} 個地點")
    
    # 第一階段：旅遊景點 51-85
    results = verify_section(
        "旅遊景點 (51-85)",
        OFFICIAL_LOCATIONS['attractions'],
        extracted
    )
    
    # 返回結果供後續處理
    return results

if __name__ == "__main__":
    results = main()
    
    if results['missing']:
        print(f"\n⚠️  需要添加 {len(results['missing'])} 個缺失項目")
    else:
        print(f"\n🎉 完美！所有項目都已包含！")
