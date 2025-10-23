#!/usr/bin/env python3
"""
改進版：正確處理兩欄排版的 PDF 提取
提取所有 319 個官方地點問題
"""

import re
import json
from collections import OrderedDict

def extract_locations_from_two_column_layout(filename):
    """處理兩欄排版的地點提取"""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    locations = OrderedDict()
    
    # 分行處理
    lines = content.split('\n')
    
    current_number = 0
    
    for line in lines:
        line = line.strip()
        
        # 跳過空行和標題行
        if not line or '地方（問題）' in line or '位置（答案）' in line:
            continue
        
        # 跳過路線問題（編號 320 以上）
        if re.search(r'^(3[2-9]\d|[4-9]\d\d)\.', line):
            continue
        
        # 匹配單欄格式: "數字. 地點  位置"
        # 使用正則表達式，處理多個空格分隔
        single_match = re.match(r'^(\d+)\.\s+(.+?)\s{2,}(.+?)$', line)
        if single_match:
            num, place, location = single_match.groups()
            num = int(num)
            
            # 過濾明顯的非地點項
            if num <= 319 and not any(x in place for x in ['起點', '目的地', '路線', '經修訂', '暫時移除']):
                place = place.strip()
                location = location.strip()
                
                # 清理位置中的雜訊（移除後面可能混入的下一個編號）
                location = re.sub(r'\s+\d+\..*$', '', location)
                
                if place and location and len(location) < 50:  # 位置不應太長
                    locations[place] = location
                    current_number = num
            continue
        
        # 匹配兩欄格式: "數字. 地點  位置  數字. 地點  位置"
        # 分割成兩部分
        parts = re.split(r'\s{3,}', line)  # 用 3 個以上空格分割
        
        for part in parts:
            part = part.strip()
            double_match = re.match(r'^(\d+)\.\s+(.+?)\s{2,}(.+?)$', part)
            if double_match:
                num, place, location = double_match.groups()
                num = int(num)
                
                if num <= 319 and not any(x in place for x in ['起點', '目的地', '路線']):
                    place = place.strip()
                    location = location.strip()
                    
                    # 清理位置
                    location = re.sub(r'\s+\d+\..*$', '', location)
                    
                    if place and location and len(location) < 50:
                        locations[place] = location
                        current_number = num
    
    return locations

def parse_structured_sections(filename):
    """從結構化的章節中提取（醫院、酒店等）"""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    locations = OrderedDict()
    
    # 提取每一頁的內容
    pages = content.split('=== 第')
    
    for page in pages:
        lines = page.split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # 匹配格式1: "1. 地點  位置  2. 地點  位置"
            # 先找出所有 "數字. " 的位置
            pattern = r'(\d+)\.\s+([^\d]+?)(?=\s+\d+\.|\s*$)'
            matches = re.finditer(pattern, line)
            
            for match in matches:
                num_str = match.group(1)
                rest = match.group(2).strip()
                
                num = int(num_str)
                if num > 319:  # 只要地點問題
                    continue
                
                # 分離地點和位置（用多個空格分隔）
                parts = re.split(r'\s{2,}', rest, maxsplit=1)
                
                if len(parts) == 2:
                    place, location = parts
                    place = place.strip()
                    location = location.strip()
                    
                    # 清理位置（移除可能的下一個編號開頭）
                    location = re.sub(r'\d+\..*$', '', location).strip()
                    
                    if place and location and len(location) < 50:
                        locations[place] = location
    
    return locations

def main():
    print("🔍 使用改進演算法提取地點...")
    
    # 方法1: 處理兩欄排版
    locations1 = extract_locations_from_two_column_layout('extracted_questions.txt')
    print(f"📊 方法1（兩欄處理）: 提取 {len(locations1)} 個地點")
    
    # 方法2: 結構化章節處理
    locations2 = parse_structured_sections('extracted_questions.txt')
    print(f"📊 方法2（結構化）: 提取 {len(locations2)} 個地點")
    
    # 合併兩種方法的結果
    all_locations = OrderedDict()
    all_locations.update(locations1)
    all_locations.update(locations2)
    
    print(f"\n✅ 合併後總計: {len(all_locations)} 個地點")
    
    # 按類別分組統計
    categories = {
        '醫院': [],
        '酒店/賓館': [],
        '大學/學院': [],
        '商場/購物中心': [],
        '公園/景點': [],
        '政府機構': [],
        '住宅樓宇': [],
        '其他': []
    }
    
    for place in all_locations.keys():
        if '醫院' in place:
            categories['醫院'].append(place)
        elif '酒店' in place or '賓館' in place:
            categories['酒店/賓館'].append(place)
        elif '大學' in place or '學院' in place:
            categories['大學/學院'].append(place)
        elif any(x in place for x in ['廣場', '中心', '商場', 'MALL', 'Mall']):
            categories['商場/購物中心'].append(place)
        elif any(x in place for x in ['公園', '樂園', '纜車', '博物館', '展覽', '文物']):
            categories['公園/景點'].append(place)
        elif any(x in place for x in ['署', '政府', '法院', '郵政']):
            categories['政府機構'].append(place)
        elif any(x in place for x in ['邨', '苑', '花園', '樓', '閣', '灣畔', '半島', '城']):
            categories['住宅樓宇'].append(place)
        else:
            categories['其他'].append(place)
    
    print(f"\n📊 詳細分類:")
    for cat, places in categories.items():
        if places:
            print(f"   {cat}: {len(places)} 個")
    
    # 保存結果
    with open('all_locations_improved.json', 'w', encoding='utf-8') as f:
        json.dump(all_locations, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 已保存到 all_locations_improved.json")
    
    # 顯示前 30 個示例
    print(f"\n📝 前 30 個地點示例:")
    for i, (place, location) in enumerate(list(all_locations.items())[:30], 1):
        print(f"   {i:3d}. {place:30s} → {location}")
    
    # 顯示最後 10 個
    print(f"\n📝 最後 10 個地點:")
    for i, (place, location) in enumerate(list(all_locations.items())[-10:], len(all_locations)-9):
        print(f"   {i:3d}. {place:30s} → {location}")
    
    return all_locations

if __name__ == "__main__":
    locations = main()
