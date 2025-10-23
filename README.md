# HK Taxi Quiz 題庫

香港的士筆試題庫資料庫，用於 HK Taxi Quiz APP 的遠端更新功能。

## 📁 文件結構

```
├── part_a_questions.json          # 甲部 - 的士則例 (20題)
├── part_a_questions.json.version  # 版本號
├── part_b_questions.json          # 乙部 - 地方試題 (20題)
├── part_b_questions.json.version  # 版本號
├── part_c_questions.json          # 丙部 - 道路守則 (50題)
└── part_c_questions.json.version  # 版本號
```

## 📊 題目統計

- **甲部（的士則例）**: 20 題，及格 17 題（85%）
- **乙部（地方試題）**: 20 題，及格 17 題（85%）
- **丙部（道路守則）**: 50 題，及格 43 題（86%）

## 🔄 版本管理

採用語義化版本號：`vX.Y.Z`

- **X (主版本號)**: 大幅改動（如：全部重寫）
- **Y (次版本號)**: 新增題目或章節
- **Z (修訂號)**: 修正錯誤、微調

### 當前版本

- 甲部: v1.0.0
- 乙部: v1.0.0
- 丙部: v1.0.0

## 📝 更新流程

### 1. 修改題目

編輯對應的 JSON 文件：

```bash
# 例如修改甲部題目
vim part_a_questions.json
```

### 2. 更新版本號

```bash
# 修正錯誤（小改動）
echo "v1.0.1" > part_a_questions.json.version

# 新增題目（中改動）
echo "v1.1.0" > part_a_questions.json.version

# 大幅改動
echo "v2.0.0" > part_a_questions.json.version
```

### 3. 提交更改

```bash
git add .
git commit -m "更新甲部題目 v1.0.1: 修正第3題答案"
git push
```

### 4. 完成！

用戶會在下次啟動 APP 時自動下載更新。

## 🌐 CDN 加速訪問

### GitHub Raw URL
```
https://raw.githubusercontent.com/你的用戶名/hktaxiquiz-questions/main/part_a_questions.json
```

### jsDelivr CDN（推薦，中國大陸訪問快）
```
https://cdn.jsdelivr.net/gh/你的用戶名/hktaxiquiz-questions@main/part_a_questions.json
```

## 📋 JSON 格式說明

```json
{
  "category": "甲部",
  "title": "的士則例",
  "description": "香港的士則例相關題目",
  "passingScore": 17,
  "totalQuestions": 20,
  "questions": [
    {
      "id": "A001",
      "question": "題目內容",
      "options": {
        "A": "選項A",
        "B": "選項B",
        "C": "選項C",
        "D": "選項D"
      },
      "correctAnswer": "A",
      "explanation": "答案解釋",
      "difficulty": "easy",
      "tags": ["標籤1", "標籤2"]
    }
  ]
}
```

## 📊 題目來源

- 運輸署官方考試大綱
- 歷屆考試題目
- 專業司機經驗

## 📄 授權

此題庫僅供學習使用，請勿用於商業用途。

## 📞 聯絡

如有題目錯誤或建議，請提交 Issue。

---

最後更新：2025-10-23
