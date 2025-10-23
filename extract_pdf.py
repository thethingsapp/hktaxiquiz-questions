#!/usr/bin/env python3
"""
提取官方 PDF 試題內容
"""

import sys
import re

try:
    import PyPDF2
    print("使用 PyPDF2 提取...")
except ImportError:
    print("PyPDF2 未安裝，嘗試安裝...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyPDF2"])
    import PyPDF2

def extract_pdf_text(pdf_path):
    """提取 PDF 文字內容"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            print(f"總頁數: {len(pdf_reader.pages)}")
            
            for i, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                text += f"\n\n=== 第 {i+1} 頁 ===\n\n"
                text += page_text
            
            return text
    except Exception as e:
        print(f"錯誤: {e}")
        return None

if __name__ == "__main__":
    pdf_path = "official_location_route_questions.pdf"
    
    print(f"正在提取: {pdf_path}")
    text = extract_pdf_text(pdf_path)
    
    if text:
        # 保存到文字檔案
        output_path = "extracted_questions.txt"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"\n✅ 已保存到: {output_path}")
        
        # 顯示前 2000 字符
        print("\n=== 內容預覽 ===")
        print(text[:2000])
    else:
        print("❌ 提取失敗")
