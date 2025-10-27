# 🎯 GitHub Repository 設置完成指南

## ✅ 已完成的步驟

### 1. 本地 Repository 創建
- ✅ 目錄位置：`/Users/louiswong/Desktop/development/hktaxiquiz-questions`
- ✅ 已複製所有題目 JSON 文件
- ✅ 已創建版本文件（v1.0.0）
- ✅ 已創建 README.md
- ✅ 已初始化 Git repository
- ✅ 已完成首次 commit

### 2. 文件清單
```
hktaxiquiz-questions/
├── .git/                            # Git 倉庫
├── .gitignore                       # Git 忽略文件
├── README.md                        # 說明文檔
├── part_a1_questions.json           # 甲部 - 的士則例
├── part_a1_questions.json.version   # v1.0.0
├── part_a2_questions.json           # 甲部 - 地方
├── part_a2_questions.json.version   # v1.0.0
├── part_a3_questions.json           # 甲部 - 路線
├── part_a3_questions.json.version   # v1.0.0
├── part_b_questions.json            # 乙部 - 道路使用者守則
└── part_b_questions.json.version    # v1.0.0
```

---

## 📋 下一步：上傳到 GitHub

### 步驟 1：在 GitHub 創建 Repository

1. **打開瀏覽器訪問**：https://github.com/new

2. **填寫資訊**：
   - **Repository name**: `hktaxiquiz-questions`
   - **Description**: `HK Taxi Quiz 題庫資料庫 - 用於遠端更新功能`
   - **Visibility**: ✅ **Public**（必須是 public 才能使用 CDN）
   - **❌ 不要勾選**：
     - [ ] Add a README file
     - [ ] Add .gitignore
     - [ ] Choose a license

3. **點擊**：`Create repository`

---

### 步驟 2：連接到 GitHub

在創建完 repository 後，GitHub 會顯示指令。你需要運行：

```bash
cd /Users/louiswong/Desktop/development/hktaxiquiz-questions

# 替換 "你的用戶名" 為你的 GitHub 用戶名
git remote add origin https://github.com/你的用戶名/hktaxiquiz-questions.git

# 設置主分支名稱
git branch -M main

# 推送到 GitHub
git push -u origin main
```

**示例**（假設你的 GitHub 用戶名是 `louiswong123`）：
```bash
cd /Users/louiswong/Desktop/development/hktaxiquiz-questions
git remote add origin https://github.com/louiswong123/hktaxiquiz-questions.git
git branch -M main
git push -u origin main
```

---

### 步驟 3：驗證上傳成功

1. 刷新 GitHub repository 頁面
2. 應該能看到以下文件：
   - README.md
   - part_a1_questions.json / .version
   - part_a2_questions.json / .version
   - part_a3_questions.json / .version
   - part_b_questions.json / .version

---

### 步驟 4：獲取 CDN URL

上傳成功後，你的文件可以通過以下 URL 訪問：

#### GitHub Raw URL（直接訪問）
```
https://raw.githubusercontent.com/你的用戶名/hktaxiquiz-questions/main/part_a1_questions.json
```

#### jsDelivr CDN URL（推薦，更快）
```
https://cdn.jsdelivr.net/gh/你的用戶名/hktaxiquiz-questions@main/part_a1_questions.json
```

**測試 URL**：
在瀏覽器打開 CDN URL，應該能看到 JSON 內容。

---

### 步驟 5：更新 APP 代碼

1. **打開文件**：
   ```
   /Users/louiswong/Desktop/development/hktaxiquiz/lib/core/services/remote_question_service.dart
   ```

2. 確認來源設定：目前已預設使用 jsDelivr（並內建 GitHub Raw 備援），通常無需修改。

4. **保存文件**

---

### 步驟 6：測試 APP

```bash
cd /Users/louiswong/Desktop/development/hktaxiquiz

# 運行 APP
flutter run

# 查看日誌（等待 2-3 秒）
# 應該看到：
# 🔍 檢查題庫更新...
# ✓ part_a1_questions.json 已是最新版本 (v1.0.0)
# ✓ part_a2_questions.json 已是最新版本 (v1.0.0)
# ✓ part_a3_questions.json 已是最新版本 (v1.0.0)
# ✓ part_b_questions.json 已是最新版本 (v1.0.0)
# ✅ 題庫更新檢查完成
```

**在 APP 中測試**：
1. 進入「設置」頁面
2. 點擊「題庫版本資訊」
3. 應該顯示：
   - 甲部-的士則例 / 甲部-地方 / 甲部-路線：各自版本（本地下載或內嵌）
   - 乙部-道路使用者守則：版本（本地下載或內嵌）

---

## 🔄 未來更新題目流程

### 情境 1：修正錯誤答案

```bash
cd /Users/louiswong/Desktop/development/hktaxiquiz-questions

# 1. 編輯文件
# 修改 part_a1_questions.json 中的錯誤

# 2. 更新版本號
echo "v1.0.1" > part_a1_questions.json.version

# 3. 提交更改
git add part_a1_questions.json part_a1_questions.json.version
git commit -m "修正甲部第3題答案 (v1.0.1)"
git push

# 4. 完成！用戶下次啟動會自動下載
```

### 情境 2：新增題目

```bash
cd /Users/louiswong/Desktop/development/hktaxiquiz-questions

# 1. 編輯文件，新增題目
# 修改 part_a1_questions.json，增加新題目

# 2. 更新版本號（次版本號+1）
echo "v1.1.0" > part_a1_questions.json.version

# 3. 提交更改
git add part_a1_questions.json part_a1_questions.json.version
git commit -m "新增甲部5題 (v1.1.0)"
git push
```

### 情境 3：大幅改動

```bash
# 更新版本號（主版本號+1）
echo "v2.0.0" > part_a1_questions.json.version

git commit -m "重做甲部題庫 (v2.0.0)"
git push
```

---

## 🧪 測試檢查清單

### ✅ 基本功能測試
- [ ] APP 啟動後自動檢查更新（查看日誌）
- [ ] 設置頁面顯示版本資訊
- [ ] 手動點擊「檢查題庫更新」能正常工作
- [ ] 題目能正常顯示和作答

### ✅ 更新流程測試
- [ ] 在 GitHub 修改題目
- [ ] 更新版本號
- [ ] 在 APP 中手動檢查更新
- [ ] 確認下載新版本
- [ ] 確認題目已更新

### ✅ 離線測試
- [ ] 關閉網絡
- [ ] 啟動 APP
- [ ] 確認仍能使用（內嵌版本）

---

## 📞 需要幫助？

### 常見問題

**Q1: 推送時提示需要身份驗證？**
```bash
# 使用 GitHub Personal Access Token
# 1. 訪問 https://github.com/settings/tokens
# 2. Generate new token (classic)
# 3. 勾選 repo 權限
# 4. 使用 token 作為密碼
```

**Q2: 如何查看 GitHub 用戶名？**
```bash
# 訪問 https://github.com/
# 右上角頭像 → 點擊 "Your profile"
# URL 中的名字就是你的用戶名
```

**Q3: CDN URL 無法訪問？**
- 等待 5-10 分鐘（CDN 緩存更新）
- 嘗試清除瀏覽器緩存
- 確認 repository 是 Public

**Q4: APP 沒有下載更新？**
- 檢查網絡連接
- 查看控制台日誌
- 確認 baseUrl 配置正確
- 嘗試手動點擊「檢查題庫更新」

---

## 🎉 完成！

一切準備就緒！現在你只需要：

1. ✅ 在 GitHub 創建 repository
2. ✅ 推送代碼
3. ✅ 更新 APP 的 baseUrl
4. ✅ 測試功能

之後更新題目就像編輯文本文件一樣簡單！

---

## 📝 快速命令參考

```bash
# 查看當前 repository 狀態
cd /Users/louiswong/Desktop/development/hktaxiquiz-questions
git status

# 查看提交歷史
git log --oneline

# 查看遠端 URL
git remote -v

# 更新題目流程
# 1. 編輯 JSON 文件
# 2. 更新版本號
echo "v1.0.1" > part_a_questions.json.version
# 3. 提交
git add .
git commit -m "更新描述"
git push
```

祝你使用順利！🚀
