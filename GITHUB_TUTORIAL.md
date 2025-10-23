# 📸 GitHub 設置圖文教程

## 🎯 目標
將本地題庫 repository 上傳到 GitHub，讓 APP 能夠遠端下載更新。

---

## 第一步：創建 GitHub Repository

### 1.1 打開 GitHub 創建頁面

在瀏覽器中訪問：**https://github.com/new**

### 1.2 填寫 Repository 資訊

```
┌─────────────────────────────────────────────────┐
│ Create a new repository                         │
├─────────────────────────────────────────────────┤
│                                                 │
│ Repository name *                               │
│ ┌─────────────────────────────────────────┐    │
│ │ hktaxiquiz-questions                     │    │
│ └─────────────────────────────────────────┘    │
│                                                 │
│ Description (optional)                          │
│ ┌─────────────────────────────────────────┐    │
│ │ HK Taxi Quiz 題庫資料庫                   │    │
│ └─────────────────────────────────────────┘    │
│                                                 │
│ ○ Private      ● Public ← 選擇 Public         │
│                                                 │
│ Initialize this repository with:               │
│ ☐ Add a README file        ← 不要勾選         │
│ ☐ Add .gitignore           ← 不要勾選         │
│ ☐ Choose a license         ← 不要勾選         │
│                                                 │
│        [ Create repository ]                    │
└─────────────────────────────────────────────────┘
```

**重要提醒**：
- ✅ **Public**（必須，才能使用免費 CDN）
- ❌ **不要勾選任何初始化選項**

### 1.3 點擊綠色按鈕 "Create repository"

---

## 第二步：連接到 GitHub

創建完成後，GitHub 會顯示一個快速設置頁面：

```
┌─────────────────────────────────────────────────┐
│ Quick setup — if you've done this kind of      │
│ thing before                                    │
├─────────────────────────────────────────────────┤
│                                                 │
│ HTTPS    SSH                                    │
│ https://github.com/你的用戶名/hktaxiquiz-...   │
│                                                 │
│ …or push an existing repository from the       │
│ command line                                    │
│                                                 │
│ git remote add origin https://github.com/...   │
│ git branch -M main                              │
│ git push -u origin main                         │
└─────────────────────────────────────────────────┘
```

### 2.1 複製 GitHub 提供的命令

**注意**：GitHub 會自動生成包含你用戶名的正確命令！

### 2.2 在終端中執行

打開終端（Terminal），執行以下命令：

```bash
# 進入題庫目錄
cd /Users/louiswong/Desktop/development/hktaxiquiz-questions

# 添加遠端 repository（使用 GitHub 顯示的命令）
git remote add origin https://github.com/你的用戶名/hktaxiquiz-questions.git

# 設置主分支名稱
git branch -M main

# 推送到 GitHub
git push -u origin main
```

### 2.3 輸入 GitHub 認證

首次推送時會要求輸入：
- **Username**: 你的 GitHub 用戶名
- **Password**: 你的 Personal Access Token（不是密碼！）

**如何獲取 Personal Access Token**：
1. 訪問：https://github.com/settings/tokens
2. 點擊 "Generate new token (classic)"
3. 勾選 `repo` 權限
4. 點擊 "Generate token"
5. **複製 token**（只顯示一次！）
6. 使用 token 作為密碼

---

## 第三步：驗證上傳成功

### 3.1 刷新 GitHub 頁面

你應該看到類似這樣的內容：

```
┌─────────────────────────────────────────────────┐
│ 你的用戶名 / hktaxiquiz-questions              │
├─────────────────────────────────────────────────┤
│                                                 │
│ 📁 .gitignore                                   │
│ 📄 README.md                                    │
│ 📄 part_a_questions.json                        │
│ 📄 part_a_questions.json.version                │
│ 📄 part_b_questions.json                        │
│ 📄 part_b_questions.json.version                │
│ 📄 part_c_questions.json                        │
│ 📄 part_c_questions.json.version                │
│                                                 │
│ Initial commit: 初始題庫 v1.0.0                 │
└─────────────────────────────────────────────────┘
```

### 3.2 測試文件訪問

點擊 `part_a_questions.json`，應該能看到 JSON 內容。

---

## 第四步：獲取 CDN URL

### 4.1 確定你的 GitHub 用戶名

在 GitHub 頁面右上角，點擊頭像 → 你的用戶名就在下拉菜單頂部。

### 4.2 構建 CDN URL

**格式**：
```
https://cdn.jsdelivr.net/gh/用戶名/hktaxiquiz-questions@main/文件名
```

**示例**（假設用戶名是 `louiswong123`）：
```
https://cdn.jsdelivr.net/gh/louiswong123/hktaxiquiz-questions@main/part_a_questions.json
https://cdn.jsdelivr.net/gh/louiswong123/hktaxiquiz-questions@main/part_a_questions.json.version
https://cdn.jsdelivr.net/gh/louiswong123/hktaxiquiz-questions@main/part_b_questions.json
...
```

### 4.3 測試 URL

在瀏覽器打開 CDN URL，應該能看到 JSON 內容。

**注意**：首次訪問可能需要等待 5-10 分鐘讓 CDN 緩存。

---

## 第五步：更新 APP 代碼

### 5.1 打開文件

在 VS Code 中打開：
```
lib/core/services/remote_question_service.dart
```

### 5.2 找到第 22 行

```dart
static const String baseUrl = 'https://your-server.com/questions';
```

### 5.3 替換為你的 CDN URL

**修改前**：
```dart
static const String baseUrl = 'https://your-server.com/questions';
```

**修改後**（記得替換 `louiswong123` 為你的用戶名）：
```dart
static const String baseUrl = 
    'https://cdn.jsdelivr.net/gh/louiswong123/hktaxiquiz-questions@main';
```

### 5.4 保存文件

按 `Cmd + S` (macOS) 或 `Ctrl + S` (Windows/Linux) 保存。

---

## 第六步：測試 APP

### 6.1 運行 APP

```bash
cd /Users/louiswong/Desktop/development/hktaxiquiz
flutter run
```

### 6.2 查看日誌

等待 2-3 秒，應該在控制台看到：

```
🔍 檢查題庫更新...
📥 發現新版本 part_a_questions.json: null → v1.0.0
✅ part_a_questions.json 更新完成
📥 發現新版本 part_b_questions.json: null → v1.0.0
✅ part_b_questions.json 更新完成
📥 發現新版本 part_c_questions.json: null → v1.0.0
✅ part_c_questions.json 更新完成
✅ 題庫更新檢查完成
```

### 6.3 在 APP 中驗證

1. 在 APP 底部導航，點擊「設置」
2. 向下滾動，找到「題庫管理」區塊
3. 點擊「題庫版本資訊」

應該看到：
```
┌─────────────────────────────┐
│ 題庫版本資訊                 │
├─────────────────────────────┤
│                             │
│ 甲部                        │
│ 版本: v1.0.0                │
│ 來源: 本地下載              │
│                             │
│ 乙部                        │
│ 版本: v1.0.0                │
│ 來源: 本地下載              │
│                             │
│ 丙部                        │
│ 版本: v1.0.0                │
│ 來源: 本地下載              │
│                             │
│         [ 關閉 ]            │
└─────────────────────────────┘
```

---

## 🎉 成功！

恭喜！你已經完成了遠端題庫系統的設置。

### ✅ 已完成項目
- ✅ 本地 Git repository
- ✅ 上傳到 GitHub
- ✅ 配置 CDN URL
- ✅ 更新 APP 代碼
- ✅ 測試自動更新功能

### 🚀 現在你可以：

**快速更新題目**（不需要發布新 APP 版本）：
```bash
cd /Users/louiswong/Desktop/development/hktaxiquiz-questions

# 1. 編輯題目文件
open part_a_questions.json  # 用編輯器打開

# 2. 更新版本號
echo "v1.0.1" > part_a_questions.json.version

# 3. 提交到 GitHub
git add .
git commit -m "修正甲部第3題答案"
git push

# 4. 完成！用戶下次啟動 APP 會自動下載
```

---

## 📝 快速參考卡

### 你的配置信息

```
GitHub Repository: https://github.com/你的用戶名/hktaxiquiz-questions
CDN Base URL: https://cdn.jsdelivr.net/gh/你的用戶名/hktaxiquiz-questions@main
本地目錄: /Users/louiswong/Desktop/development/hktaxiquiz-questions
```

### 常用命令

```bash
# 查看狀態
cd /Users/louiswong/Desktop/development/hktaxiquiz-questions
git status

# 更新題目流程
# 1. 編輯文件
# 2. 更新版本號
echo "v1.0.1" > part_a_questions.json.version
# 3. 提交
git add .
git commit -m "更新說明"
git push
```

### 版本號規則

- `v1.0.1` ← 修正錯誤
- `v1.1.0` ← 新增題目
- `v2.0.0` ← 大幅改動

---

## ❓ 遇到問題？

### 問題 1：推送失敗，要求認證
**解決**：使用 Personal Access Token 作為密碼

### 問題 2：CDN URL 404
**解決**：等待 5-10 分鐘，CDN 需要時間緩存

### 問題 3：APP 沒有下載更新
**解決**：
1. 檢查網絡連接
2. 確認 baseUrl 配置正確
3. 手動點擊「檢查題庫更新」
4. 查看控制台日誌

---

需要更多幫助？隨時詢問！
