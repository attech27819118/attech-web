# ATTech Materials - Scripts 工具腳本使用說明書

本目錄（`scripts/`）收錄 ATTech 官網建置、技術專區靜態生成、資料庫同步、SEO 網站地圖產生以及 AWS Lambda 後端維護等自動化工具腳本。

---

## 目錄索引

1. [核心工作流速查 (Quick Start)](#1-核心工作流速查-quick-start)
2. [技術專區與 js/technology.js 關聯架構（單一事實來源）](#2-技術專區與-jstechnologyjs-關聯架構單一事實來源)
3. [技術專區核心腳本詳解](#3-技術專區核心腳本詳解)
4. [產品靜態頁面生成 (Product SSG)](#4-產品靜態頁面生成-product-ssg)
5. [快取破壞與 SEO 工具](#5-快取破壞與-seo-工具)
6. [AWS Lambda 郵件後端工具](#6-aws-lambda-郵件後端工具)
7. [歷史維護與修復腳本清單](#7-歷史維護與修復腳本清單)

---

## 1. 核心工作流速查 (Quick Start)

| 作業情境 | 建議執行順序與指令 |
| :--- | :--- |
| **A. 更新技術專區（文字、資料或版面）**<br>(修訂了 `techdatadb/技術文件摘要與重點.md` 或 `js/technology.js`) | **極致一鍵完成**：<br>`python scripts/sync_tech_updates.py`<br>*(全自動從 Markdown 萃取最新資料庫、同步注入 `js/technology.js`、並編譯 11 大靜態頁面與首頁！)* |
| **B. 產品規格/型錄資料更新**<br>(修訂了 `config.json` 或產品主檔) | `python scripts/build_static_pages.py`<br>或 `node scripts/build-static-pages.js` |
| **C. 發布新版本 / 破壞快取**<br>(更新 JS/CSS 防止瀏覽器快取) | `python scripts/update_cache_version.py 20261015_v1` |
| **D. 更新全站 Sitemap** | `node scripts/generate_sitemap.js` |
| **E. 更新/測試 AWS Lambda 郵件後端** | 測試：`node scripts/test-lambda.js`<br>打包：`powershell -File scripts/package-lambda.ps1` |

---

## 2. 技術專區全自動同步架構

技術專區提供最高效率、一鍵完成的連鎖同步工作流：

### 流程圖

```
                 【您的主要維護工作】
          修改 techdatadb/技術文件摘要與重點.md
                            │
                            ▼
           執行 python scripts/sync_tech_updates.py
                            │
    ┌───────────────────────┴───────────────────────┐
    ▼                                               ▼
[1/2 自動萃取與同步注入]                    [2/2 自動編譯 11 大靜態網頁]
更新 json/tech_database.json                生成 technology/{slug}/index.html
同步更新 js/technology.js (只增不減)        同步首頁 index.html 與 Sitemap
```

#### 🎯 平常維護結論：
未來無論是新增文獻、修改技術規格重點、調整圖片網址：
👉 **修改好 `techdatadb/技術文件摘要與重點.md`，在終端機跑一次：**
```bash
python scripts/sync_tech_updates.py
```
**全站資料庫、`js/technology.js`、以及 11 大技術靜態網頁立即一鍵同步更新完畢！**

---

### 🖼️ 技術專頁圖片網址（`mechImg`）如何更新？
系統提供 **3 種維護圖片網址的方式**，皆具備「**智慧合併防覆蓋保護**」，絕不會抹除您的手動成果：

1. **方式 A（最直覺推薦：在 Markdown 註記）**：
   在 `techdatadb/技術文件摘要與重點.md` 中該篇技術文件的段落直接加上：
   ```markdown
   - **圖表**：`techdatadb/5. MPI/1.原理/作用原理.png`
   ```
   或 `- **圖片**：...`。
   執行 `python scripts/build_tech_json.py` 時會優先提取該圖檔路徑並同步寫入 `json/tech_database.json` 與 `js/technology.js`。

2. **方式 B（直接在 `js/technology.js` 手動加入）**：
   直接在 `js/technology.js` 該文件物件中填寫 `"mechImg": "techdatadb/..."`。
   * **零覆蓋保證**：執行 `python scripts/build_tech_json.py` 時，腳本會自動先掃描現有 `js/technology.js`，智慧繼承您手動填入的 `mechImg`，絕不覆蓋手動設定！
   * 若僅調整了 JS 版面或圖片網址，無需重讀 Markdown，可直接執行：
     ```bash
     node scripts/build_technology_subpages.js
     ```
     （此指令純讀取 JS 生成靜態 HTML，100% 不動 JS 檔案）。

3. **方式 C（腳本內建預設對應表）**：
   所有未在 Markdown 或 JS 中特別指定的文件，會自動從 `scripts/build_tech_json.py` 中的 `determine_labels_and_meta()` 取得原廠預設圖表（涵蓋 Tyzor、Orion、MPI Wax、Matting Agent 等全系列預設圖表）。

---

## 3. 技術專區核心腳本詳解

### ① `scripts/build_tech_json.py`
* **功能**：由 `techdatadb/技術文件摘要與重點.md` 中解析出結構化的 JSON 技術數據，並智慧繼承保留前端 `js/technology.js` 中所有手動配置的圖片網址。
* **輸出**：`json/tech_database.json` 與同步寫入 `js/technology.js`
* **適用時機**：當技術文件的摘要、主要特點、物性參數有新增或修正時執行。
* **執行方式**：
  ```bash
  python scripts/build_tech_json.py
  ```

### ① `scripts/sync_tech_updates.py`（★ 極致一鍵推薦）
* **功能**：技術專區一鍵全自動同步與建置中樞（包裝調用 `build_technology_subpages.js`）：
  1. **以 `js/technology.js` 為唯一真理源頭 (Single Source of Truth)**，原生讀取資料與渲染函式。
  2. **絕不覆蓋、修改或破壞** `js/technology.js` 中的任何程式碼與手動圖片設定。
  3. 自動產生 11 大獨立技術靜態分頁（`technology/{slug}/index.html`）。
  4. 同步更新首頁 `index.html` 中的 `#tab-technology` 區塊與 `sitemap.xml`。
  5. 自動同步備份最新資料至 `json/tech_database.json`。
* **執行方式**：
  ```bash
  python scripts/sync_tech_updates.py
  ```
  *(若有特殊需求需從 Markdown 重新強制萃取導入，可加上參數：`python scripts/sync_tech_updates.py --from-md`)*

### ② `scripts/build_technology_subpages.js`（Node.js 原生建置核心）
* **功能**：由 Node.js VM 直接加載執行 `js/technology.js`，100% 保證靜態生成出的 HTML 與前端動態展示一模一樣。
* **執行方式**：
  ```bash
  node scripts/build_technology_subpages.js
  ```

### ③ `scripts/build_tech_json.py`（Markdown 資料庫匯入工具）
* **功能**：由 `techdatadb/技術文件摘要與重點.md` 中解析出結構化的 JSON 技術數據。
* **適用時機**：僅在需要由原始 Markdown 重新批量萃取文檔物性與摘要時使用，日常維護請直接修改 `js/technology.js`。
* **執行方式**：
  ```bash
  python scripts/build_tech_json.py
  ```

---

## 4. 產品靜態頁面生成 (Product SSG)

### ① `scripts/build_static_pages.py`（推薦） / `scripts/build-static-pages.js`
* **功能**：遍歷 `config.json` 中登記的所有品牌主檔（Dorf Ketal, Orion, Troy, King Industries 等），為每一款產品產生獨立靜態頁面（例如 `products/orion/coating/special-black-4/index.html`）。
* **特色**：
  * 注入個別 OpenGraph、Canonical URL 與結構化資料。
  * 純白現代極簡排版，自動解析規格物性表與推薦應用領域。
  * 內建 TDS 查看與索樣按鈕。
* **執行方式**：
  ```bash
  python scripts/build_static_pages.py
  # 或 Node.js 版本：
  node scripts/build-static-pages.js
  ```

---

## 5. 快取破壞與 SEO 工具

### ① `scripts/update_cache_version.py`
* **功能**：全域更新所有 HTML 及腳本引入的版本號字串（例如 `js/technology.js?v=20261015_v1`、`APP_VERSION`），並強制注入 HTTP 禁止快取 Header。
* **影響檔案**：
  * `js/state.js`
  * `scripts/build_technology_subpages.py`
  * 全站 HTML 檔案
* **執行方式**：
  ```bash
  python scripts/update_cache_version.py 20261015_v1
  ```

### ② `scripts/generate_sitemap.js`
* **功能**：讀取全站所有靜態頁面目錄與產品清單，自動更新根目錄的 `sitemap.xml`，維護 Google 搜尋引擎索引完整度。
* **執行方式**：
  ```bash
  node scripts/generate_sitemap.js
  ```

---

## 6. AWS Lambda 郵件後端工具

### ① `scripts/test-lambda.js`
* **功能**：本機或線上測試樣品申請／技術諮詢表單的 AWS Lambda Handler。
  * 支援在本地驗證 PDF 表單產生、參數檢核與輸出。
  * 支援直接打向線上 API Gateway 端點進行整合測試。
* **執行方式**：
  ```bash
  # 本機模擬測試
  node scripts/test-lambda.js --local

  # 線上端點整合測試
  node scripts/test-lambda.js --remote
  ```

### ② `scripts/package-lambda.ps1`
* **功能**：Windows PowerShell 打包腳本。自動將最新的 `index.js` 與 `fonts/` 中文字型打包進 `lambda-package.zip`，以供上傳更新至 AWS Lambda。
* **執行方式**：
  ```powershell
  powershell -ExecutionPolicy Bypass -File scripts/package-lambda.ps1
  ```

---

## 7. 歷史維護與修復腳本清單

本目錄下包含部分過去重構與補丁遷移腳本，記錄如下以供參考（日常維運通常不需重複執行）：

| 腳本名稱 | 歷史用途說明 |
| :--- | :--- |
| `update_gallery_tech.py` | 早期將首頁 `#tab-technology` 升級為 11 大畫廊卡片展開型版面的更新腳本。 |
| `update_tech_all.py` | 早期一鍵將技術資料庫注入 JS 並替換全螢幕視窗邏輯的腳本。 |
| `update_cover_flow.py` | 早期調整 PDF 封面渲染流與預覽排版之腳本。 |
| `apply_cover_fix.py` / `apply_cover_clean_fix.py` | 將舊版獨立按鈕移除，改為「點擊封面直接開啟全螢幕檢視」之遷移腳本。 |
| `apply_true_fullscreen.py` | 將原本的模態視窗升級為沉浸式多頁深色滿版閱讀器之修正腳本。 |
| `fix_tech_bugs.py` | 修復 PDF.js 載入路徑解析與全螢幕按鍵監聽事件之歷史腳本。 |
| `fix_missing_data_bug.py` | 修正「暫無公開資料」分頁邏輯與安全防護之補丁腳本。 |
| `fix_modal_zindex.py` | 修正全螢幕閱讀視窗 z-index 被 Navbar 遮擋問題之腳本。 |
