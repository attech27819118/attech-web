---
name: email-testing
description: 規範 ATTech 官網寄信與索樣表單之測試規則。任何寄信功能測試時，公司名稱與聯絡人一律使用「測試中」。
---

# ATTech 寄信功能測試規範 (Email Testing Guideline)

本技能定義宏威應用材料 (ATTech) 官網表單與 AWS Lambda 郵件發送功能在進行任何測試時的嚴格規範。

## 核心命名規範（重要，切勿遺忘）

在任何環境（本機開發、AWS Lambda 遠端端點、線上前端表單、自動化腳本）測試寄信功能時：

1. **公司名稱 (Company Name)**：必須一律填寫為 **`​寄信測試`**
2. **聯絡人姓名 (Contact Person)**：必須一律填寫為 **`​寄信測試`**
3. **目的**：
   - 官網表單寄信會即時發送至公司業務信箱與負責人。
   - 公司抬頭與聯絡人明確標註為「測試中」，可讓業務團隊一眼識別為內部系統連線測試，避免被誤認為真實客戶商機進行派工或聯繫。

## 標準測試 Payload 範例

### 1. 快速詢價模式 (Quick Mode)

```json
{
  "type": "快速詢價",
  "company": "​寄信測試",
  "contact": "​寄信測試",
  "email": "test@example.com",
  "mobile": "0912-345-678",
  "phone": "0912-345-678",
  "sample": "AT-801 (100g)",
  "address": "40661 台中市北屯區廍子巷116號1樓",
  "message": "系統連線自動化測試信件",
  "applyDate": "2026/11/02"
}
```

### 2. 詳細應用需求評估模式 (Detailed Mode)

```json
{
  "type": "詳細需求",
  "company": "​寄信測試",
  "contact": "​寄信測試",
  "email": "test@example.com",
  "mobile": "0912-345-678",
  "phone": "0912-345-678",
  "fax": "未提供",
  "address": "40661 台中市北屯區廍子巷116號1樓",
  "applyDate": "2026/11/02",
  "appFields": ["車用電子"],
  "otherAppDomain": "",
  "functions": ["高導熱"],
  "otherFunc": "無",
  "systems": ["環氧樹脂 (Epoxy)"],
  "compType": "單劑型",
  "appType": "透明",
  "colorDesc": "",
  "substrates": ["鋁合金 (Al)"],
  "otherSubstrate": "無",
  "filmThick": "50 um",
  "noBake": "否",
  "bakeTemp": "120°C",
  "bakeTime": "30 分鐘",
  "resins": ["環氧樹脂"],
  "otherResin": "",
  "restricted": "無",
  "sampleReq": "AT-801 (100g)",
  "sampleItems": [
    { "name": "AT-801", "qty": "100g" }
  ],
  "docs": ["TDS 物性表"],
  "pastSamples": "無",
  "remarks": "此為系統測試信件，公司與聯絡人均為​寄信測試"
}
```

## 注意事項

- 切勿在測試時填寫真實客戶公司或同仁姓名。
- 測試完成後確認郵件主題與 PDF 附件抬頭均為「​寄信測試 - ...」，即代表系統產製正常。
