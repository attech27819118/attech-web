# 歷史維護與一次性修復補丁 (Legacy Maintenance Patches)

本資料夾（`scripts/legacy_patches/`）收錄專案在過去迭代重構期間所撰寫的一次性補丁與遷移腳本。  
**注意：日常維運與建置工作流皆不需重複執行本目錄下的腳本。**  
相關功能均已整併進主系統核心（`scripts/sync_tech_updates.py`、`scripts/build_technology_subpages.js` 與 `js/technology.js`）。

---

## 腳本清單與歷史背景說明

| 腳本檔名 | 歷史用途說明 |
| :--- | :--- |
| `apply_cover_clean_fix.py` | 批次將舊版獨立按鈕移除，改為「點擊封面直接開啟全螢幕檢視」之遷移腳本。 |
| `apply_cover_fix.py` | 早期 PDF 封面直接觸發模態檢視器之遷移腳本。 |
| `apply_true_fullscreen.py` | 將原本的居中模態視窗升級為沉浸式多頁深色滿版閱讀器之修正腳本。 |
| `fix_missing_data_bug.py` | 修正「暫無公開資料」分頁邏輯與防呆跳轉之歷史補丁。 |
| `fix_modal_zindex.py` | 修正全螢幕閱讀視窗 z-index 被頂部導覽列 Navbar 遮擋問題之樣式補丁。 |
| `fix_tech_bugs.py` | 修復 PDF.js 載入路徑解析與全螢幕按鍵監聽事件之歷史腳本。 |
| `update_cover_flow.py` | 早期調整 PDF 封面渲染流與預覽排版之腳本。 |
| `update_gallery_tech.py` | 早期將首頁 `#tab-technology` 升級為 11 大畫廊卡片展開型版面的更新腳本。 |
| `update_tech_all.py` | 早期一鍵將技術資料庫注入 JS 並替換全螢幕視窗邏輯的腳本。 |

