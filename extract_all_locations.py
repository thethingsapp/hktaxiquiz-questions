#!/usr/bin/env python3
"""
從官方 PDF 提取所有地點問題（完整版）
"""

import re
import json

def extract_locations_from_pdf_text(filename):
    """提取所有地點和位置"""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    locations = {}
    
    # 方法1: 匹配 "數字. 地點  位置" 格式
    # 處理多空格分隔
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        # 匹配格式: "1. 地點名稱  位置"
        match = re.match(r'^(\d+)\.\s+(.+?)\s{2,}(.+?)$', line.strip())
        if match:
            num, place, location = match.groups()
            place = place.strip()
            location = location.strip()
            
            # 過濾掉非地點的行
            if place and location and not any(x in place for x in ['地方（問題）', '起點', '目的地', '路線']):
                locations[place] = location
                
    return locations

def main():
    print("📖 正在提取所有地點...")
    
    locations = extract_locations_from_pdf_text('extracted_questions.txt')
    
    print(f"\n✅ 成功提取 {len(locations)} 個地點")
    
    # 按類別分組
    hospitals = {k: v for k, v in locations.items() if '醫院' in k}
    hotels = {k: v for k, v in locations.items() if '酒店' in k or '賓館' in k}
    universities = {k: v for k, v in locations.items() if '大學' in k or '學院' in k}
    shopping = {k: v for k, v in locations.items() if '廣場' in k or '中心' in k or '商場' in k}
    parks = {k: v for k, v in locations.items() if '公園' in k or '樂園' in k or '纜車' in k}
    government = {k: v for k, v in locations.items() if '署' in k or '政府' in k or '法院' in k}
    residential = {k: v for k, v in locations.items() if '邨' in k or '苑' in k or '花園' in k or '樓' in k or '閣' in k}
    
    print(f"\n📊 分類統計:")
    print(f"   醫院: {len(hospitals)} 個")
    print(f"   酒店: {len(hotels)} 個")
    print(f"   大學: {len(universities)} 個")
    print(f"   商場: {len(shopping)} 個")
    print(f"   公園景點: {len(parks)} 個")
    print(f"   政府機構: {len(government)} 個")
    print(f"   住宅: {len(residential)} 個")
    print(f"   其他: {len(locations) - len(hospitals) - len(hotels) - len(universities) - len(shopping) - len(parks) - len(government) - len(residential)} 個")
    
    # 保存完整列表
    with open('all_locations.json', 'w', encoding='utf-8') as f:
        json.dump(locations, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 已保存到 all_locations.json")
    
    # 顯示示例
    print(f"\n📝 部分示例:")
    for i, (place, location) in enumerate(list(locations.items())[:20], 1):
        print(f"   {i}. {place} → {location}")
    
    return locations

if __name__ == "__main__":
    locations = main()
