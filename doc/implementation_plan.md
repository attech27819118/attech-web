# 從 Localhost 到雲端：ATTech 專案部署現況分析與後端上線實施計畫

本計畫針對 ATTech Materials 專案進行完整的「網站部署技術地圖」對照分析，並規劃將 Node.js 後端（負責郵件發送與 PDF 報表生成）部署至 Render PaaS 雲端平台，實現與現有 GitHub Pages 前端無縫串接。

---

## 📊 一、專案現況與技術地圖階段對照

依據《從 localhost 到雲端：一張看懂網站部署的技術地圖》的分類，本專案的現狀與定位如下：

```mermaid
flowchart TD
    subgraph 階段0_本機開發 ["階段 0：本機開發 (Localhost)"]
        LocalClient["本機瀏覽器 (127.0.0.1:5500)"]
        LocalServer["本機後端 (localhost:3000 server.js)"]
        LocalClient -->|POST /api/send-email| LocalServer
    end

    subgraph 階段2_雲端正式部署 ["階段 2：雲端正式部署 (前後端分離架構)"]
        GH["前端：GitHub Pages (已完成)<br/>https://rosf000.github.io/attech-web/"]
        RenderAPI["後端：Render PaaS (本次實施)<br/>https://attech-backend.onrender.com"]
        SMTP["企業郵件主機 (mail.attech.com.tw)"]
        
        GH -->|1. 靜態頁面 & JSON 資料| User[全球訪客]
        User -->|2. 填寫樣品申請/詢價表單| GH
        GH -->|3. POST /api/send-email (跨域 CORS)| RenderAPI
        RenderAPI -->|4. 動態生成 PDF 附件 (NotoSansTC)| RenderAPI
        RenderAPI -->|5. SMTP TLS 465 發信| SMTP
    end

    style GH fill:#dcfce7,stroke:#16a34a,stroke-width:2px
    style RenderAPI fill:#dbeafe,stroke:#2563eb,stroke-width:2px
    style LocalServer fill:#fee2e2,stroke:#ef4444,stroke-width:2px
```

| 元件層級 | 目前狀態 | 部署方式 / 所在位置 | 狀態說明 |
| :--- | :--- | :--- | :--- |
| **前端 (UI / 樣式 / 靜態資源)** | 🟢 **已上線** | GitHub Pages (`rosf000.github.io/attech-web`) | HTML5 + Tailwind CSS + JS + 中文字型 + TDS 資料已正常運作 |
| **資料庫 (產品規格與分類)** | 🟢 **已上線** | 靜態 JSON 檔案 (`json/mpi/mpiall.json` 等) | 隨前端直接託管於 GitHub Pages，前端以 `fetch` 載入 |
| **後端 (API / 寄信 / PDF 生成)** | 🔴 **待部署** | 本機 `server.js` (`localhost:3000`) | GitHub Pages 為純靜態託管，無法執行 Node.js，表單目前無法在線上成功寄信 |

---

## 🎯 二、接下來的核心目標

1. **改造 `server.js` 為雲端相容模式**：
   - 支援動態 `process.env.PORT`（Render 會自動注入 Port）。
   - CORS 跨域白名單加入 `https://rosf000.github.io` 與自訂網域。
   - 新增健康檢查端點 `GET /` 與 `GET /api/health`，便於確認服務在線狀態。
   - 支援環境變數（SMTP 帳號密碼可透過雲端後台安全設定）。
2. **改造 `index.html` 的 API 連線設定**：
   - 本地開發時自動連線 `http://localhost:3000`。
   - 線上環境（GitHub Pages / 外部網域）自動切換至 Render 雲端後端網址 (`https://attech-backend.onrender.com`)。
3. **提供 Render 雲端部署操作步驟**：
   - 連結 GitHub 倉庫 `rosf000/attech-web`，零費用、自動 HTTPS 憑證、程式碼 Push 即自動部署。

---

## 🛠️ 三、具體變更計畫 (Proposed Changes)

### 1. 後端架構修改

#### [MODIFY] [server.js](file:///c:/Users/MARCO/OneDrive/Desktop/J/vscode/attech0818%20-%20%E8%A4%87%E8%A3%BD/server.js)
- 動態取得 Port：`const PORT = process.env.PORT || 3000;`
- 更新 CORS 白名單，包含 `https://rosf000.github.io`、`https://www.attech.com.tw` 及本地除錯埠。
- 支援環境變數讀取 SMTP 資訊：`process.env.SMTP_USER`、`process.env.SMTP_PASS`、`process.env.SMTP_HOST`、`process.env.SMTP_PORT`。
- 新增服務健康檢查路由：
  ```javascript
  app.get('/', (req, res) => {
      res.json({
          status: 'online',
          service: 'ATTech Materials API Server',
          version: '1.0.0',
          timestamp: new Date().toISOString()
      });
  });
  app.get('/api/health', (req, res) => res.json({ status: 'ok' }));
  ```

---

### 2. 前端表單連線修改

#### [MODIFY] [index.html](file:///c:/Users/MARCO/OneDrive/Desktop/J/vscode/attech0818%20-%20%E8%A4%87%E8%A3%BD/index.html)
- 統一抽出 `BACKEND_API_BASE` 配置常數。
- 邏輯改為：
  ```javascript
  const PROD_API_BASE = 'https://attech-backend.onrender.com'; // Render 後端網址
  const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
  const apiBase = isLocal ? 'http://localhost:3000' : PROD_API_BASE;
  ```

---

## 📋 四、Render 雲端部署操作指引 (雲端上線三步驟)

等程式碼更新並 `git push` 至 GitHub 倉庫後，依照以下步驟在 Render 上線：

1. **登入 [Render](https://render.com)**（可直接使用 GitHub 帳號登入）。
2. **建立 Web Service**：
   - 點擊 **New +** -> 選擇 **Web Service**。
   - 連接 GitHub 倉庫 `rosf000/attech-web`（或手動輸入 Git Repository URL）。
3. **填寫基本設定**：
   - **Name**: `attech-backend` (或您喜好的名稱，將決定產生的網址)
   - **Region**: Singapore (新加坡) 或 Oregon (美國)
   - **Branch**: `main`
   - **Root Directory**: （留空即可，代表根目錄）
   - **Runtime**: `Node`
   - **Build Command**: `npm install`
   - **Start Command**: `npm start`
   - **Instance Type**: `Free` (免費方案)
4. **點擊 "Deploy Web Service"**，約 1~2 分鐘後即可取得專屬 HTTPS 網址！

---

## 🧪 五、驗證計畫 (Verification Plan)

### 本地驗證
1. 啟動 `node server.js`。
2. 測試健康檢查端點：`curl http://localhost:3000/` 或在瀏覽器開啟。
3. 測試前端於本地送出表單，確認信件與 PDF 生成正常。

### 線上驗證
1. Render 部署完成後，在瀏覽器開啟 `https://attech-backend.onrender.com/`，應顯示 JSON 狀態訊息。
2. 開啟 GitHub Pages 網址 `https://rosf000.github.io/attech-web/`。
3. 填寫樣品單送出，確認收到「需求表單已成功送出！」提示，並確認 `atservice@attech.com.tw` 與 CC 信箱收到帶有單頁 PDF 附件的正式郵件。
