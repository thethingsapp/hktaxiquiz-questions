# 🖼️ 如何添加圖片到題目

## 快速開始

### 步驟 1: 準備圖片

1. **下載或製作圖片**
   - 交通標誌: 從運輸署網站下載
   - 道路情況: 拍照或使用示意圖
   - 解析圖片: 使用圖片編輯工具製作

2. **優化圖片**
   ```bash
   # 使用 ImageMagick 壓縮
   convert input.png -quality 80 -resize 800x600 output.png
   
   # 或使用線上工具
   # https://tinypng.com/
   ```

3. **重命名圖片**
   ```bash
   # 好的命名
   no_entry.png
   stop_sign.png
   curve_road_warning.png
   
   # 不好的命名
   IMG_001.png
   圖片1.png
   traffic sign.png  # 有空格
   ```

---

### 步驟 2: 上傳圖片到 GitHub

1. **複製圖片到對應目錄**
   ```bash
   cd hktaxiquiz-questions
   
   # 交通標誌
   cp ~/Downloads/no_entry.png images/signs/
   
   # 道路情況
   cp ~/Downloads/curve_road.png images/situations/
   
   # 解析圖片
   cp ~/Downloads/explanation_001.png images/explanations/
   ```

2. **提交到 Git**
   ```bash
   git add images/
   git commit -m "Add traffic sign images"
   git push
   ```

3. **等待 CDN 同步**
   - jsDelivr 需要 5-10 分鐘同步
   - 可以訪問以下 URL 測試:
     ```
     https://cdn.jsdelivr.net/gh/thethingsapp/hktaxiquiz-questions@main/images/signs/no_entry.png
     ```

---

### 步驟 3: 在 JSON 中引用圖片

#### 範例 1: 題目圖片

```json
{
  "id": "C001",
  "question": "下圖所示的交通標誌代表什麼意思？",
  "questionImage": "https://cdn.jsdelivr.net/gh/thethingsapp/hktaxiquiz-questions@main/images/signs/no_entry.png",
  "options": {
    "A": "禁止駛入",
    "B": "禁止停車",
    "C": "禁止超車",
    "D": "單行道"
  },
  "correctAnswer": "A",
  "explanation": "這是「禁止駛入」標誌。"
}
```

#### 範例 2: 選項圖片

```json
{
  "id": "C002",
  "question": "以下哪個是「停車讓路」標誌？",
  "options": {
    "A": "標誌A",
    "B": "標誌B",
    "C": "標誌C",
    "D": "標誌D"
  },
  "optionImages": {
    "A": "https://cdn.jsdelivr.net/gh/thethingsapp/hktaxiquiz-questions@main/images/signs/stop.png",
    "B": "https://cdn.jsdelivr.net/gh/thethingsapp/hktaxiquiz-questions@main/images/signs/yield.png",
    "C": "https://cdn.jsdelivr.net/gh/thethingsapp/hktaxiquiz-questions@main/images/signs/speed.png",
    "D": "https://cdn.jsdelivr.net/gh/thethingsapp/hktaxiquiz-questions@main/images/signs/parking.png"
  },
  "correctAnswer": "A"
}
```

#### 範例 3: 帶解析圖片

```json
{
  "id": "C003",
  "question": "觀察下圖的道路情況，應該如何處理？",
  "questionImage": "https://cdn.jsdelivr.net/gh/thethingsapp/hktaxiquiz-questions@main/images/situations/intersection.png",
  "options": {
    "A": "減速並讓路",
    "B": "保持速度",
    "C": "加速通過",
    "D": "鳴笛警告"
  },
  "correctAnswer": "A",
  "explanation": "在這種情況下，應該減速並讓其他車輛先行。",
  "explanationImage": "https://cdn.jsdelivr.net/gh/thethingsapp/hktaxiquiz-questions@main/images/explanations/intersection_explained.png"
}
```

---

### 步驟 4: 更新版本號

```bash
# 更新版本號（如果有重大更新）
echo "v1.1.0" > part_c_questions.json.version

git add part_c_questions.json part_c_questions.json.version
git commit -m "Update part C with image questions - v1.1.0"
git push
```

---

## 📝 完整工作流程範例

### 添加一個新的交通標誌題目

1. **準備圖片**
   ```bash
   # 下載「禁止駛入」標誌圖片
   # 保存為: no_entry_sign.png
   ```

2. **優化並上傳**
   ```bash
   cd hktaxiquiz-questions
   cp ~/Downloads/no_entry_sign.png images/signs/
   
   git add images/signs/no_entry_sign.png
   git commit -m "Add no entry sign image"
   git push
   ```

3. **等待 5-10 分鐘**
   - 訪問測試: https://cdn.jsdelivr.net/gh/thethingsapp/hktaxiquiz-questions@main/images/signs/no_entry_sign.png

4. **編輯 part_c_questions.json**
   ```json
   {
     "id": "C_NEW_001",
     "question": "下圖所示的交通標誌代表什麼意思？",
     "questionImage": "https://cdn.jsdelivr.net/gh/thethingsapp/hktaxiquiz-questions@main/images/signs/no_entry_sign.png",
     "options": {
       "A": "禁止駛入",
       "B": "禁止停車",
       "C": "禁止超車",
       "D": "單行道"
     },
     "correctAnswer": "A",
     "explanation": "這是「禁止駛入」標誌，所有車輛禁止進入。"
   }
   ```

5. **提交更新**
   ```bash
   git add part_c_questions.json
   git commit -m "Add new traffic sign question with image"
   git push
   ```

6. **完成！**
   - 用戶端會自動檢測並下載更新
   - 新題目會在下次練習時出現

---

## 🎯 圖片規範總結

| 類型 | 尺寸 | 格式 | 大小限制 | 目錄 |
|------|------|------|----------|------|
| 交通標誌 | 400×400px | PNG | < 100KB | `images/signs/` |
| 道路情況 | 1200×800px | JPG/PNG | < 200KB | `images/situations/` |
| 解析圖片 | 800×600px | PNG/JPG | < 150KB | `images/explanations/` |

---

## 🔗 CDN URL 格式

```
https://cdn.jsdelivr.net/gh/thethingsapp/hktaxiquiz-questions@main/images/{目錄}/{檔名}
```

**範例:**
- 標誌: `https://cdn.jsdelivr.net/gh/thethingsapp/hktaxiquiz-questions@main/images/signs/stop.png`
- 情況: `https://cdn.jsdelivr.net/gh/thethingsapp/hktaxiquiz-questions@main/images/situations/curve.png`
- 解析: `https://cdn.jsdelivr.net/gh/thethingsapp/hktaxiquiz-questions@main/images/explanations/detail.png`

---

## ⚠️ 常見問題

### Q: 圖片無法顯示？
**A:** 檢查：
1. GitHub 是否已 push 成功
2. CDN 是否已同步（等待 10 分鐘）
3. URL 是否正確（區分大小寫）
4. 圖片檔案是否存在

### Q: 如何更新已使用的圖片？
**A:** 兩種方式：
1. 使用新檔名上傳，更新 JSON 引用
2. 覆蓋原檔案，等待 CDN 刷新（可能需要 24 小時）

### Q: 可以使用中文檔名嗎？
**A:** 不建議。請使用英文 + 下劃線命名，例如: `traffic_light_red.png`

---

## 📚 更多資源

- **完整文檔**: `images/README.md`
- **範例題目**: `example_with_images.json`
- **運輸署標誌**: https://www.td.gov.hk/tc/road_safety/road_traffic_signs/
- **圖片壓縮工具**: https://tinypng.com/
- **jsDelivr CDN**: https://www.jsdelivr.com/

---

💡 **提示**: 可以參考 `example_with_images.json` 文件，裡面有完整的範例！
