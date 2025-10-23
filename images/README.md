# 📸 題目圖片資源

本目錄存放 HK Taxi Quiz 應用的題目圖片資源。

## 📁 目錄結構

```
images/
├── signs/              # 交通標誌圖片
│   ├── no_entry.png
│   ├── stop.png
│   ├── yield.png
│   └── ...
├── situations/         # 道路情況圖片
│   ├── curve_road.png
│   ├── pedestrian_crossing.png
│   └── ...
└── explanations/       # 答案解析圖片
    └── ...
```

## 🎯 圖片規範

### 交通標誌 (signs/)
- **格式**: PNG（推薦透明背景）
- **尺寸**: 400×400 px
- **大小**: < 100 KB
- **命名**: 小寫英文_下劃線 (例如: no_entry.png)

### 道路情況 (situations/)
- **格式**: JPG 或 PNG
- **尺寸**: 1200×800 px (16:9 比例)
- **大小**: < 200 KB
- **命名**: 描述性英文 (例如: curve_road.png)

### 解析圖片 (explanations/)
- **格式**: PNG 或 JPG
- **尺寸**: 800×600 px
- **大小**: < 150 KB
- **命名**: 與題目ID關聯 (例如: C001_explanation.png)

## 📝 使用方式

### 在 JSON 中引用圖片

使用 jsDelivr CDN URL：

```json
{
  "id": "C001",
  "question": "下圖所示的交通標誌代表什麼意思？",
  "questionImage": "https://cdn.jsdelivr.net/gh/thethingsapp/hktaxiquiz-questions@main/images/signs/no_entry.png",
  "options": {
    "A": "禁止駛入",
    "B": "禁止停車"
  },
  "correctAnswer": "A",
  "explanation": "這是「禁止駛入」標誌。",
  "explanationImage": "https://cdn.jsdelivr.net/gh/thethingsapp/hktaxiquiz-questions@main/images/explanations/C001_explanation.png"
}
```

### 選項圖片範例

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
    "C": "https://cdn.jsdelivr.net/gh/thethingsapp/hktaxiquiz-questions@main/images/signs/speed_limit.png",
    "D": "https://cdn.jsdelivr.net/gh/thethingsapp/hktaxiquiz-questions@main/images/signs/no_parking.png"
  },
  "correctAnswer": "A"
}
```

## 🔧 圖片優化工具

### ImageMagick 批量壓縮

```bash
# 壓縮 PNG
for file in *.png; do
  convert "$file" -quality 80 -resize 800x600 "optimized_$file"
done

# 壓縮 JPG
for file in *.jpg; do
  convert "$file" -quality 85 "optimized_$file"
done
```

### 在線工具
- [TinyPNG](https://tinypng.com/) - PNG/JPG 壓縮
- [Squoosh](https://squoosh.app/) - 圖片優化
- [SVGOMG](https://jakearchibald.github.io/svgomg/) - SVG 優化

## 📦 添加新圖片流程

1. **準備圖片**
   - 優化圖片大小
   - 使用規範的命名

2. **放入對應目錄**
   ```bash
   cp ~/Downloads/new_sign.png images/signs/
   ```

3. **提交到 GitHub**
   ```bash
   git add images/
   git commit -m "Add new traffic sign image"
   git push
   ```

4. **等待 CDN 同步**
   - jsDelivr 需要 5-10 分鐘
   - 測試 URL 是否可訪問

5. **更新題目 JSON**
   - 在題目中添加 `questionImage` / `optionImages` / `explanationImage` 欄位
   - 使用完整的 CDN URL

## 🔗 CDN URL 格式

```
https://cdn.jsdelivr.net/gh/thethingsapp/hktaxiquiz-questions@main/images/{category}/{filename}
```

範例：
- `https://cdn.jsdelivr.net/gh/thethingsapp/hktaxiquiz-questions@main/images/signs/no_entry.png`
- `https://cdn.jsdelivr.net/gh/thethingsapp/hktaxiquiz-questions@main/images/situations/curve_road.png`

## ⚠️ 注意事項

1. **版權問題**
   - 確保圖片有使用權限
   - 優先使用官方素材
   - 自製圖片需註明來源

2. **檔案大小**
   - 保持合理大小以節省流量
   - 建議單個圖片 < 200 KB

3. **命名規範**
   - 使用英文命名
   - 小寫字母 + 下劃線
   - 避免特殊字符和空格

4. **版本管理**
   - 圖片一旦使用就不要刪除
   - 如需更新，使用新文件名
   - 或更新版本號 (v1.1.0)

## 📚 參考資源

- [運輸署交通標誌](https://www.td.gov.hk/tc/road_safety/road_traffic_signs/)
- [jsDelivr CDN](https://www.jsdelivr.com/)
- [ImageMagick](https://imagemagick.org/)
