# HK Taxi Quiz 題庫

香港的士筆試題庫資料庫，用於 HK Taxi Quiz APP 的遠端更新功能。

## 📁 文件結構

```
├── part_a1_questions.json         # 甲部 - 的士則例（275 題）
├── part_a2_questions.json         # 甲部 - 地方（地點題 1–230，共 230 題）
├── part_a3_questions.json         # 甲部 - 路線（路線題 231–245，共 15 題）
├── part_b_questions.json          # 乙部 - 道路使用者守則
├── part_b_questions.json.version  # 版本號
├── part_c_questions.json          # 丙部 - 道路守則
└── part_c_questions.json.version  # 版本號
```

## 📊 題目統計（甲部）

- 甲部 A1（的士則例）：275 題
- 甲部 A2（地方：1–230）：230 題
- 甲部 A3（路線：231–245）：15 題

> 備註：乙部與丙部仍沿用既有檔案，實際題數以對應 JSON 的 `totalQuestions` 欄位為準。

## 🔄 版本管理

採用語義化版本號（SemVer）：`vX.Y.Z`

- X (主版本號): 非相容的結構變更（例如 schema 大改、題庫重構）
- Y (次版本號): 相容新增（新增題目、章節、標籤等）
- Z (修訂號): 相容修正（錯字、解釋修正、微調）

所有題庫檔皆提供對應的 `*.version` 檔（例如 `part_a1_questions.json.version`），請在每次異動後同步更新為新的語義化版本號，避免使用日期版號。

## 📝 更新流程

### 1. 修改題目

編輯對應的 JSON 文件（例如 A1）：

```bash
vim part_a1_questions.json
```

### 2. 更新版本號

```bash
# 修正錯誤（小改動）
echo "v1.0.1" > part_a1_questions.json.version

# 新增題目（中改動）
echo "v1.1.0" > part_a1_questions.json.version

# 大幅改動
echo "v2.0.0" > part_a1_questions.json.version
```

### 3. 提交更改

```bash
git add .
git commit -m "同步 A1 題庫至 275 題，更新 README 統計與維護原則"
git push
```

### 4. 完成！

用戶會在下次啟動 APP 時自動下載更新。

## 🌐 CDN 加速訪問

### GitHub Raw URL
```
https://raw.githubusercontent.com/thethingsapp/hktaxiquiz-questions/main/part_a1_questions.json
```

### jsDelivr CDN（推薦）
```
https://cdn.jsdelivr.net/gh/thethingsapp/hktaxiquiz-questions@main/part_a1_questions.json
```

## 📋 JSON 格式說明（以 A1 為例）

```json
{
  "part": "甲部-的士則例",
  "title": "甲部 - 的士則例",
  "description": "的士營運相關法規",
  "passingScore": 17,
  "totalQuestions": 275,
  "questions": [
    {
      "id": "A001",
      "question": "題目內容",
      "options": { "A": "選項A", "B": "選項B", "C": "選項C", "D": "選項D" },
      "correctAnswer": "A",
      "explanation": "答案解釋",
      "difficulty": "easy",
      "tags": ["標籤1", "標籤2"]
    }
  ]
}
```

## 🧭 編修與去重原則（甲部）

- 嚴守既有 Schema 與命名；採「追加 Append」方式擴充，並保持 `totalQuestions` 正確。
- 文字避免引用具體敏感數值（非必要時），採原則導向敘述；事實依官方資料交叉核對。
- 去重：發現完全重覆的題目，做輕量改寫（微調問法/情境）保留最清晰版本；避免語義重覆堆疊。
- 維護標籤與難度的一致性；優先清晰、可驗證、不中立偏頗的表述。

## 📊 題目來源

- 運輸署官方考試大綱
- 歷屆考試題目
- 專業司機經驗

## 📄 授權

此題庫僅供學習使用，請勿用於商業用途。

## 📞 聯絡

如有題目錯誤或建議，請提交 Issue。

---

最後更新：2025-10-27
