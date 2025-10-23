#!/bin/bash

# 使用 GitHub CLI 創建 repository
# 需要先安裝並登入 gh CLI

echo "🚀 使用 GitHub CLI 創建 repository"
echo ""

# 檢查是否安裝了 gh
if ! command -v gh &> /dev/null; then
    echo "❌ 未安裝 GitHub CLI"
    echo ""
    echo "請使用以下方式之一："
    echo ""
    echo "方法 1: 使用瀏覽器"
    echo "  訪問 https://github.com/new"
    echo "  Repository name: hktaxiquiz-questions"
    echo "  Public, 不要勾選任何初始化選項"
    echo ""
    echo "方法 2: 安裝 GitHub CLI"
    echo "  brew install gh"
    echo "  gh auth login"
    echo "  然後再運行此腳本"
    echo ""
    exit 1
fi

# 檢查是否已登入
if ! gh auth status &> /dev/null; then
    echo "❌ 未登入 GitHub CLI"
    echo "請先執行: gh auth login"
    exit 1
fi

cd /Users/louiswong/Desktop/development/hktaxiquiz-questions

echo "📝 創建 GitHub repository..."
gh repo create thethingsapp/hktaxiquiz-questions \
    --public \
    --description "HK Taxi Quiz 題庫資料庫 - 用於遠端更新功能" \
    --source=. \
    --remote=origin

echo ""
echo "✅ Repository 創建完成！"
echo ""
echo "🚀 推送代碼..."
git push -u origin main

echo ""
echo "✅ 完成！"
echo ""
echo "🌐 Repository URL:"
echo "https://github.com/thethingsapp/hktaxiquiz-questions"
