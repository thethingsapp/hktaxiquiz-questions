# 🎯 你的題庫配置信息

## GitHub 配置

- **GitHub 用戶名**: `thethingsapp`
- **Repository 名稱**: `hktaxiquiz-questions`
- **Repository URL**: https://github.com/thethingsapp/hktaxiquiz-questions
- **本地路徑**: `/Users/louiswong/Desktop/development/hktaxiquiz-questions`

## CDN URL

```
Base URL (已配置在 APP 中):
https://cdn.jsdelivr.net/gh/thethingsapp/hktaxiquiz-questions@main

完整文件 URL:
https://cdn.jsdelivr.net/gh/thethingsapp/hktaxiquiz-questions@main/part_a1_questions.json
https://cdn.jsdelivr.net/gh/thethingsapp/hktaxiquiz-questions@main/part_a1_questions.json.version
https://cdn.jsdelivr.net/gh/thethingsapp/hktaxiquiz-questions@main/part_a2_questions.json
https://cdn.jsdelivr.net/gh/thethingsapp/hktaxiquiz-questions@main/part_a2_questions.json.version
https://cdn.jsdelivr.net/gh/thethingsapp/hktaxiquiz-questions@main/part_a3_questions.json
https://cdn.jsdelivr.net/gh/thethingsapp/hktaxiquiz-questions@main/part_a3_questions.json.version
https://cdn.jsdelivr.net/gh/thethingsapp/hktaxiquiz-questions@main/part_b_questions.json
https://cdn.jsdelivr.net/gh/thethingsapp/hktaxiquiz-questions@main/part_b_questions.json.version
```

## 📋 待完成步驟

### ✅ 已完成
- ✅ 本地 Git repository 創建
- ✅ 添加遠端 origin
- ✅ 設置主分支為 main
- ✅ 更新 APP baseUrl 配置

### 🔄 需要你完成

#### 1. 創建 GitHub Repository
訪問：https://github.com/new

填寫：
- Repository name: `hktaxiquiz-questions`
- Description: `HK Taxi Quiz 題庫資料庫 - 用於遠端更新功能`
- Visibility: **Public** ✅
- ❌ 不要勾選任何初始化選項

#### 2. 推送代碼到 GitHub

創建完 repository 後，在終端執行：

```bash
cd /Users/louiswong/Desktop/development/hktaxiquiz-questions
git push -u origin main
```

**認證信息**：
- Username: `thethingsapp`
- Password: Personal Access Token（從 https://github.com/settings/tokens 獲取）

#### 3. 驗證上傳成功

訪問：https://github.com/thethingsapp/hktaxiquiz-questions

應該看到 12 個文件：
- .gitignore
- README.md
- part_a1_questions.json
- part_a1_questions.json.version
- part_a2_questions.json
- part_a2_questions.json.version
- part_a3_questions.json
- part_a3_questions.json.version
- part_b_questions.json
- part_b_questions.json.version

#### 4. 測試 CDN 訪問

在瀏覽器打開（上傳後等待 5-10 分鐘）：
```
https://cdn.jsdelivr.net/gh/thethingsapp/hktaxiquiz-questions@main/part_a1_questions.json
```

應該能看到 JSON 內容。

#### 5. 測試 APP

```bash
cd /Users/louiswong/Desktop/development/hktaxiquiz
flutter run
```

等待 2-3 秒後，查看控制台日誌，應該看到：
```
🔍 檢查題庫更新...
📥 發現新版本 part_a_questions.json: null → v1.0.0
✅ part_a_questions.json 更新完成
...
✅ 題庫更新檢查完成
```

在 APP 中：
- 進入「設置」
- 點擊「題庫版本資訊」
- 確認顯示「本地下載」和版本號

---

## 🔄 未來更新題目流程

### 快速更新

```bash
cd /Users/louiswong/Desktop/development/hktaxiquiz-questions

# 1. 編輯題目文件
open part_a1_questions.json  # 或使用任何編輯器

# 2. 更新版本號
echo "v1.0.1" > part_a1_questions.json.version

# 3. 提交並推送
git add .
git commit -m "修正甲部A1第3題答案 (v1.0.1)"
git push

# 4. 完成！用戶下次啟動 APP 會自動下載
```

### 版本號規則

- `v1.0.1` ← 修正錯誤、微調
- `v1.1.0` ← 新增題目
- `v2.0.0` ← 大幅改動、重構

---

## 📞 常用命令

### 查看狀態
```bash
cd /Users/louiswong/Desktop/development/hktaxiquiz-questions
git status
git log --oneline -5
```

### 查看遠端配置
```bash
git remote -v
# 應該顯示：
# origin  https://github.com/thethingsapp/hktaxiquiz-questions.git (fetch)
# origin  https://github.com/thethingsapp/hktaxiquiz-questions.git (push)
```

### 更新題目模板
```bash
# 修正錯誤
git add part_a1_questions.json part_a1_questions.json.version
git commit -m "修正甲部第X題答案 (v1.0.1)"
git push

# 新增題目
git add part_b_questions.json part_b_questions.json.version
git commit -m "新增乙部5題 (v1.1.0)"
git push

# 大改動
git add .
git commit -m "重做題庫結構 (v2.0.0)"
git push
```

---

## ✅ APP 配置已更新

文件：`lib/core/services/remote_question_service.dart`

```dart
static const String baseUrl = 
    'https://cdn.jsdelivr.net/gh/thethingsapp/hktaxiquiz-questions@main';
```

✅ 配置正確，無需再修改！

---

## 🎉 下一步

1. 訪問 https://github.com/new 創建 repository
2. 完成後告訴我，我會幫你推送代碼
3. 測試 APP 功能

準備好了嗎？
