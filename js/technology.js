/**
 * ====================================================================
 * ATTech Web - Technology Module (js/technology.js)
 * 技術專區：11 大特用化學品專題、五大核心維度 (1.原理 2.目錄 3.應用技術 4.單一產品技術 5.配方)
 * 嚴格實事求是：依據 techdatadb 原廠資料庫檔案呈現
 * 比照原理分類架構與排版，線上瀏覽文件，且不開放下載
 * 無原廠公開資料之分頁誠實標示「暫無資料」，絕不憑空杜撰
 * ====================================================================
 */

// 11 大產品系列分類
const TECH_CATEGORIES = [
  {
    slug: "tyzor",
    itemNo: "01",
    name: "Organic Titanates and Zirconates",
    sub: "鈦酸酯與鋯酸酯, Tyzor",
    brandTag: "Dorf Ketal",
    brandBadge: "Dorf Ketal 原廠專用技術",
    titleZh: "鈦酸酯與鋯酸酯四大核心技術應用 (Tyzor®)",
    productLink: "products/dorfketal/tyzor/",
    productLinkText: "瀏覽 Tyzor 產品",
    desc: "Tyzor® 有機鈦（鋯）化合物具備高反應性與多重配位特性，廣泛應用於高分子合成催化、三維網絡交聯、異質基材介面強化，以及 Sol-Gel 表面改性，為工業化提供全面解決方案。",
    hasData: true
  },
  {
    slug: "carbon-black",
    itemNo: "02",
    name: "Special Carbon Black",
    sub: "特級碳黑 / 導電碳黑",
    brandTag: "Orion",
    brandBadge: "Orion Engineered Carbons 原廠技術",
    titleZh: "特級碳黑技術應用 (Carbon Black)",
    productLink: "products/orion/coating/",
    productLinkText: "瀏覽 40+ 款 Orion 碳黑",
    desc: "Orion Engineered Carbons 為全球特級碳黑領導品牌，提供卓越黑度、分散流變性與耐候堅牢度，廣泛應用於高階塗料、油墨與塑料。",
    hasData: true
  },
  {
    slug: "maleic",
    itemNo: "03",
    name: "Maleic Resin / 馬林酸樹脂",
    sub: "松香改性馬林酸樹脂",
    brandTag: "其他特化",
    brandBadge: "特用化學品技術專區",
    titleZh: "馬林酸樹脂技術應用 (Maleic Resin)",
    productLink: "products/others/maleic_acid_resin/",
    productLinkText: "瀏覽馬林酸樹脂規格",
    desc: "松香改性馬林酸樹脂系列，提供優異之硬度、光澤度、快乾性與耐黃變特性。",
    hasData: false
  },
  {
    slug: "px",
    itemNo: "04",
    name: "PX Lubricant Additives",
    sub: "潤滑油添加劑 (原 ExxonMobil)",
    brandTag: "Dorf Ketal",
    brandBadge: "Dorf Ketal (原 ExxonMobil) 原廠技術",
    titleZh: "PX 潤滑油添加劑技術應用 (PX Lubricants)",
    productLink: "products/dorfketal/px/",
    productLinkText: "瀏覽 PX 潤滑油添加劑",
    desc: "Dorf Ketal (原 ExxonMobil 產品線) 特種潤滑油合成酯添加劑技術專題。",
    hasData: false
  },
  {
    slug: "silane",
    itemNo: "05",
    name: "Silane / 矽烷偶合劑",
    sub: "Dynasylan / hydrosil 系列",
    brandTag: "Evonik / 特化",
    brandBadge: "Evonik 原廠專用技術",
    titleZh: "矽烷偶合劑系列技術應用 (Silane)",
    productLink: "products/others/silane/",
    productLinkText: "瀏覽 24 款矽烷規格",
    desc: "矽烷偶合劑技術專題，涵蓋水性與溶劑型有機官能基矽烷於複合材料與表面改性應用。",
    hasData: false
  },
  {
    slug: "wax",
    itemNo: "06",
    name: "Micronized Wax / 微粉蠟",
    sub: "PTFE 取代 / 耐磨耐刮助劑",
    brandTag: "Micro Powders",
    brandBadge: "Micro Powders (MPI) 原廠技術",
    titleZh: "微粉化蠟技術應用 (Micronized Wax)",
    productLink: "products/mpi/ptfe/",
    productLinkText: "瀏覽微粉蠟與 PTFE 替代方案",
    desc: "Micro Powders (MPI) 全球微粉化蠟技術權威，提供合規無氟 PFAS-Free PTFE 替代方案、耐磨耐刮、消光爽滑及觸感改性劑。",
    hasData: true
  },
  {
    slug: "adhesion",
    itemNo: "07",
    name: "Adhesion Resin / 密著樹脂",
    sub: "氯化聚烯烴 (CPO) & 非氯系",
    brandTag: "其他特化",
    brandBadge: "特用化學品技術專區",
    titleZh: "密著樹脂技術應用 (Adhesion Resin)",
    productLink: "products/others/adhesion_promoter/",
    productLinkText: "瀏覽密著促進劑規格",
    desc: "氯化聚烯烴 (CPO) 與非氯系特種密著樹脂技術應用。",
    hasData: false
  },
  {
    slug: "polyester",
    itemNo: "08",
    name: "Polyester Resin / 聚酯樹脂",
    sub: "聚酯樹脂 (DYNAPOL/DYNACOLL替代品)",
    brandTag: "其他特化",
    brandBadge: "特用化學品技術專區",
    titleZh: "聚酯樹脂技術應用 (Polyester Resin)",
    productLink: "products/others/polyester_resin/",
    productLinkText: "瀏覽 37 款聚酯規格",
    desc: "飽和共聚聚酯樹脂技術專題，提供高附著、柔韌性與優異耐化學品塗料樹脂。",
    hasData: false
  },
  {
    slug: "chain",
    itemNo: "09",
    name: "Chain Extender / 擴鏈劑",
    sub: "Unilink & Clearlink 系列",
    brandTag: "Dorf Ketal",
    brandBadge: "Dorf Ketal 原廠專用技術",
    titleZh: "擴鏈劑技術應用 (Chain Extender)",
    productLink: "products/dorfketal/chain/",
    productLinkText: "瀏覽擴鏈劑規格",
    desc: "Dorf Ketal Unilink® 與 Clearlink® 受阻二級二胺擴鏈劑技術，專用於聚脲 (Polyurea) 與高性能聚氨酯彈性體體系。",
    hasData: true
  },
  {
    slug: "matting",
    itemNo: "10",
    name: "Matting Agent / 消光粉",
    sub: "二氧化矽 / 表面處理消光",
    brandTag: "其他特化",
    brandBadge: "特用化學品技術專區",
    titleZh: "消光粉技術應用 (Matting Agent)",
    productLink: "products/others/matting_agent/",
    productLinkText: "瀏覽消光粉規格",
    desc: "特種沉澱與氣相二氧化矽消光粉技術專題，包含消光原理、粒徑分佈、孔隙率、膜厚影響與各樹脂體系之分散工藝指引。",
    hasData: true
  },
  {
    slug: "powder",
    itemNo: "11",
    name: "Powder Coating Additive",
    sub: "粉體塗料專用功能性助劑",
    brandTag: "其他特化",
    brandBadge: "特用化學品技術專區",
    titleZh: "粉體塗料專用助劑技術應用 (Powder Additives)",
    productLink: "products/others/coating_additive/",
    productLinkText: "瀏覽粉體塗料助劑規格",
    desc: "熱固性粉體塗料專用功能性助劑技術專區。",
    hasData: false
  }
];

// 原廠技術資料庫 (完整整合自 techdatadb，嚴格實事求是)
const TECH_DATABASE = {
  "tyzor": {
    "slug": "tyzor",
    "hasData": true,
    "tabs": {
      "principles": [
        {
          "docId": "TYZ-PRIN-01",
          "filename": "鈦（鋯）酸酯作為交聯劑.pdf",
          "pdfPath": "techdatadb/2.Tyzor/1.原理/鈦（鋯）酸酯作為交聯劑.pdf",
          "docType": "原理機制",
          "lang": "TW (繁體中文)",
          "version": "原廠發行版",
          "brand": "Dorf Ketal",
          "shortLabel": "作為交聯劑",
          "title": "鈦（鋯）酸酯作為交聯劑",
          "titleEn": "鈦（鋯）酸酯作為交聯劑.pdf",
          "origin": "鈦（鋯）酸酯作為交聯劑（Alan & Thomas Technologies）",
          "desc": "說明 Tyzor 有機鈦（鋯）酸酯作為交聯劑在 100~250°C 下與聚合物活性基團反應，提高油漆、油墨、接著劑（膠黏劑）與聚合物（如PVA 等）的物理化學性能。",
          "advantages": [
            "在100~250°C加熱條件下，與羥基 (HO-polymer)發生反應形成交聯",
            "提高聚合物與膠層的固化速度",
            "顯著提高耐水性、耐熱性，並提升硬度與耐刮性能。"
          ],
          "applications": [
            "油漆",
            "油墨",
            "接著劑（膠黏劑）",
            "聚合物（如 PVA 等）。"
          ],
          "mechImg": "techdatadb/2.Tyzor/1.原理/crosslinker.webp"
        },
        {
          "docId": "TYZ-PRIN-02",
          "filename": "鈦（鋯）酸酯作為催化劑.pdf",
          "pdfPath": "techdatadb/2.Tyzor/1.原理/鈦（鋯）酸酯作為催化劑.pdf",
          "docType": "原理機制",
          "lang": "TW (繁體中文)",
          "version": "原廠發行版",
          "brand": "Dorf Ketal",
          "shortLabel": "作為催化劑",
          "title": "鈦（鋯）酸酯作為催化劑",
          "titleEn": "鈦（鋯）酸酯作為催化劑.pdf",
          "origin": "鈦（鋯）酸酯作為催化劑（Alan & Thomas Technologies）",
          "desc": "介紹 Tyzor 有機鈦（鋯）酸酯在酯合成、酯交換、縮合和加成反應中作為高效觸媒（催化劑），為替代有機錫觸媒的環保方案。",
          "advantages": [
            "不含任何有機錫，最終產品具良好環保性，符合歐美環保標準。",
            "克服普通鈦酸酯催化劑不耐水等缺陷，在280°C下依舊可以保持較高催化活性 (如Tyzor 422、Tyzor 436)",
            "可縮短聚酯合成反應時間，且Tyzor 436具備低黃變特性"
          ],
          "applications": [
            "可塑劑",
            "（不）飽和聚酯",
            "PET",
            "PBT",
            "聚酯多元醇等。"
          ],
          "mechImg": "techdatadb/2.Tyzor/1.原理/catalyst.webp"
        },
        {
          "docId": "TYZ-PRIN-03",
          "filename": "鈦（鋯）酸酯作為表面改性.pdf",
          "pdfPath": "techdatadb/2.Tyzor/1.原理/鈦（鋯）酸酯作為表面改性.pdf",
          "docType": "原理機制",
          "lang": "TW (繁體中文)",
          "version": "原廠發行版",
          "brand": "Dorf Ketal",
          "shortLabel": "作為表面改性",
          "title": "鈦（鋯）酸酯作為表面改性",
          "titleEn": "鈦（鋯）酸酯作為表面改性.pdf",
          "origin": "鈦（鋯）酸酯作為表面改性（Alan & Thomas Technologies）",
          "desc": "說明 Tyzor 有機鈦（鋯）酸酯單獨或混合其他材料加入溶膠-凝膠（Sol-Gel）體系，經水解或熱解形成連續金屬氧化物塗層以進行表面改質（改性）。",
          "advantages": [
            "經水解（Hydrolysis）或大於350°C 熱解（Pyrolysis）轉化為緻密的二氧化鈦（TiO2）薄膜。",
            "於基材表面形成連續的金屬氧化物塗層，顯著改善表面防腐性能。",
            "有效改善基材表面的耐刮性能、耐熱性能、以及表面親水性能。"
          ],
          "applications": [
            "紡織整理劑",
            "鋁銀漿表面處理",
            "顏料表面處理等。"
          ],
          "mechImg": "techdatadb/2.Tyzor/1.原理/surface_treatment.webp"
        },
        {
          "docId": "TYZ-PRIN-04",
          "filename": "鈦（鋯）酸酯提高附著力.pdf",
          "pdfPath": "techdatadb/2.Tyzor/1.原理/鈦（鋯）酸酯提高附著力.pdf",
          "docType": "原理機制",
          "lang": "TW (繁體中文)",
          "version": "原廠發行版",
          "brand": "Dorf Ketal",
          "shortLabel": "作為附著力促進劑",
          "title": "鈦（鋯）酸酯提高附著力",
          "titleEn": "鈦（鋯）酸酯提高附著力.pdf",
          "origin": "鈦（鋯）酸酯提高附著力（Alan & Thomas Technologies）",
          "desc": "Tyzor 有機鈦（鋯）在無機底材與高分子材料間架橋鍵結，顯著提升各類油漆、塗料、油墨與密封膠對不同基材的附著力（密著性）。",
          "advantages": [
            "能與聚合物、玻璃和金屬塗層上的-OH及-COOH相互作用，促進塗層與底材的交聯",
            "提高塗層耐高溫性、耐溶劑性、抗腐蝕性及耐刮性。",
            "可顯著提高塗層的硬度、耐鹽霧性與耐腐蝕性，大幅強化塗膜密著力。"
          ],
          "applications": [
            "塗料",
            "油墨",
            "密封膠"
          ],
          "mechImg": "techdatadb/2.Tyzor/1.原理/adhesion.webp"
        }
      ],
      "catalog": [
        {
          "docId": "TYZ-CATA-01",
          "filename": "Brochure DK Tyzor General CN 202608.pdf",
          "pdfPath": "techdatadb/2.Tyzor/2.Tyzor Brochure目錄/Brochure DK Tyzor General CN 202608.pdf",
          "docType": "Brochure 總覽型錄",
          "lang": "CN (簡體中文)",
          "version": "202608",
          "brand": "Dorf Ketal",
          "shortLabel": "綜合手冊 (中)",
          "title": "Tyzor™ 有機鈦（鋯）酸酯 產品目錄",
          "titleEn": "Brochure DK Tyzor General CN 202608.pdf",
          "origin": "Dorf Ketal Tyzor™ 有機鈦（鋯）酸酯產品目錄（宏威應用材料發行）",
          "desc": "全面介紹 Dorf Ketal 生產之 Tyzor 烷基鈦酸酯、鋯酸酯及螯合型鈦/鋯酸酯四大功能機制（催化劑、交聯劑、表面性能改質、密著促進劑）與完整產品物理特性。",
          "advantages": [
            "完整彙整烷氧基鈦（TnBT、TOT、TPT、BTP、ET）、螯合鈦（AA-75、AA-105、IAM、GBA、TLF 11010、LA、TE、OGT、726、9000、795、IBAY、KE 6、422、436、PC 64）及有機鋯（NBZ、NPZ、217）之系列產品特性與選型建議。",
            "機制涵蓋路易斯酸催化、羥基/羧基高分子交聯、無機粉體表面有機偶聯修飾，以及高溫裂解生成高硬度緻密薄膜（TiO2 / ZrO2反射層或鈍化層）。",
            "能取代具毒性或高污染性之重金屬觸媒（如錫、鉛），並大幅提高耐熱、耐水、耐溶劑及耐磨耗性能。"
          ],
          "applications": [
            "印刷油墨（硝化棉/聚醯胺/PU）",
            "塗料與油漆（醇酸/壓克力/烤漆/耐高溫塗料）",
            "接著劑與密封膠（矽酮/MS/聚胺酯）",
            "酯化觸媒",
            "無機填料改質",
            "玻璃熱端/冷端噴塗",
            "電線絕緣漆。"
          ]
        },
        {
          "docId": "TYZ-CATA-02",
          "filename": "Brochure DK Tyzor Adhesive Plus Coatings Line EN 202512.pdf",
          "pdfPath": "techdatadb/2.Tyzor/2.Tyzor Brochure目錄/Brochure DK Tyzor Adhesive Plus Coatings Line EN 202512.pdf",
          "docType": "Brochure 總覽型錄",
          "lang": "EN (英文)",
          "version": "202512",
          "brand": "Dorf Ketal",
          "shortLabel": "膠黏劑與密封膠",
          "title": "Tyzor® Adhesives and Sealants Application Guide",
          "titleEn": "Brochure DK Tyzor Adhesive Plus Coatings Line EN 202512.pdf",
          "origin": "Tyzor® Adhesives and Sealants Application Guide (Dorf Ketal)",
          "desc": "彙整 Tyzor 鈦酸酯與鋯酸酯系列（包括 Tyzor 726、795、KE-6、9000、BTP、TE、NBZ、TPT、TOT、LA、217等）應用於接著劑與密封膠系統之產品指南，涵蓋矽酮（RTV-1）、MS 聚合物、聚胺酯、壓克力、聚硫、天然橡膠與環氧等體系。",
          "advantages": [
            "提供多種固化時間與不發黏時間（Tack Free Time）調控，如 Tyzor 726 不發黏時間僅 2–5 分鐘、固化時間 <5 分鐘；Tyzor 795 不發黏時間 10–30 分鐘，固化時間 12–24 小時。",
            "針對各類接著密封膠體系提供完整固化速率（Cure Rate）、濕氣敏感性（Moisture Sensitivity）與顏色影響評估，提供快速固化至耐濕氣穩定之多元觸媒選擇。",
            "廣泛改善 RTV-1 矽酮與改質矽烷系統對玻璃、金屬、塑膠等基材之相對密著性（指標達 0.95–1.0），並耐受環境老化。"
          ],
          "applications": [
            "RTV-1 矽酮密封膠",
            "MS Polymer / STP 密封膠",
            "聚胺酯接著劑",
            "溶劑型與水性壓克力接著劑",
            "聚硫接著劑",
            "天然橡膠接著劑",
            "環氧樹脂",
            "車用與電子工業接著密封。"
          ]
        },
        {
          "docId": "TYZ-CATA-03",
          "filename": "Brochure DK Tyzor for Polyols Polymers EN 202602.pdf",
          "pdfPath": "techdatadb/2.Tyzor/2.Tyzor Brochure目錄/Brochure DK Tyzor for Polyols Polymers EN 202602.pdf",
          "docType": "Brochure 總覽型錄",
          "lang": "EN (英文)",
          "version": "202602",
          "brand": "Dorf Ketal",
          "shortLabel": "多元醇聚合物",
          "title": "Tyzor® Catalysts for Polyols and Polymers Application Guide",
          "titleEn": "Brochure DK Tyzor for Polyols Polymers EN 202602.pdf",
          "origin": "Tyzor® Catalysts for Polyols and Polymers Application Guide (Dorf Ketal)",
          "desc": "介紹 Tyzor 有機鈦觸媒在聚酯多元醇（Polyester Polyol）、可塑劑、丙烯酸酯單體以及PBT、PET、聚碳酸酯（PC）聚合物合成製程中的觸媒特性，涵蓋 Tyzor TE、9000、LA、TnBT、TPT、TOT、PC 64 及 ACtivate 422/436 等產品。",
          "advantages": [
            "Tyzor TE 與 Tyzor 9000 可在較低溫度下提供高反應速率，產出清澈無色之聚酯多元醇產品，並具備優異耐水性與極低水解副反應。",
            "Tyzor LA 為水性乳酸鈦螯合物，對高水分原料具備耐受性，適合直接羧酸酯化與脂肪酸酯交換反應。",
            "轉酯化反應可在 <100°C 低溫進行，直接酯化需 >180°C；在 PBT 與 PET 聚縮合製程中，Tyzor ACtivate 422/436 及 PC 64具備與銻相當之 SSP 固相聚合速率，並展現超低金屬殘留、高透明無霧度（haze-free）與低色相優勢。"
          ],
          "applications": [
            "聚酯多元醇合成",
            "可塑劑製造（如鄰苯二甲酸酯）",
            "（甲基）丙烯酸酯單體合成",
            "PBT 工程塑膠合成",
            "PET 瓶級與薄膜樹脂合成",
            "聚碳酸酯（PC）縮聚反應。"
          ]
        },
        {
          "docId": "TYZ-CATA-04",
          "filename": "Brochure DK Tyzor Plus Coatings EN 202512.pdf",
          "pdfPath": "techdatadb/2.Tyzor/2.Tyzor Brochure目錄/Brochure DK Tyzor Plus Coatings EN 202512.pdf",
          "docType": "Brochure 總覽型錄",
          "lang": "EN (英文)",
          "version": "202512",
          "brand": "Dorf Ketal",
          "shortLabel": "塗料專用型錄",
          "title": "Tyzor® Product Guide for Coatings",
          "titleEn": "Brochure DK Tyzor Plus Coatings EN 202512.pdf",
          "origin": "Tyzor® Product Guide - Coatings Application Notes (Dorf Ketal)",
          "desc": "綜述 Tyzor 全系列鈦酸酯與鋯酸酯在塗料領域之作用，包括作為成膜樹脂的交聯劑、密著促進劑、耐溫金屬氧化物形成劑及溶膠凝膠（sol-gel）反應前驅物。",
          "advantages": [
            "Tyzor TnBT、TOT、OGT 等烷氧基鈦可與含 -OH 或 -COOH 官能基之聚合物交聯，提高塗膜表面硬度、耐化性與耐水性。",
            "Tyzor TE、CLA、TEAZ 等胺螯合化合物具搖變性誘導效果，可作為高黏度搖變塗料中碳水化合物包覆乳膠粒子的有效交聯硬化劑。",
            "水性螯合物 Tyzor LA、TLF 11010、217 能在水性體系中穩定存在，大幅提升塗層對金屬、玻璃、紙張等氧化表面的附著力與耐刮性。"
          ],
          "applications": [
            "溶劑型與水性工業塗料",
            "壓克力漆",
            "搖變性乳膠漆",
            "耐高溫塗膜",
            "汽車底漆",
            "電泳塗料",
            "溶膠-凝膠無機塗層。"
          ]
        }
      ],
      "applications": [
        {
          "docId": "TYZ-APPL-01",
          "filename": "Application Note DK Tyzor Adhesives Sealants EN.pdf",
          "pdfPath": "techdatadb/2.Tyzor/3.Tyzor 應用技術資料 (12)鈦酸酯 /Application Note DK Tyzor Adhesives Sealants EN.pdf",
          "docType": "Application Note 應用技術手冊",
          "lang": "EN (英文)",
          "version": "原廠發行版",
          "brand": "Dorf Ketal",
          "shortLabel": "膠黏與密封膠",
          "title": "Tyzor® Organic Titanates and Zirconates in Adhesives and Sealants Applications",
          "titleEn": "Application Note DK Tyzor Adhesives Sealants EN.pdf",
          "origin": "Tyzor® Organic Titanates and Zirconates - Adhesives and Sealants Applications Technical Note (Dorf Ketal,",
          "desc": "闡述 Tyzor 在接著劑與密封膠工業中作為密著促進劑、交聯硬化劑與聚縮合觸媒的應用技術，評估其對各類基材之增強機制。",
          "advantages": [
            "在 RTV-1 矽酮密封膠中，Tyzor PITA、IBAY、TnBT 及 AA 系列可作為非錫觸媒與交聯劑，相容於各類酸性、鹼性及中性（烷氧基、肟基）交聯體系，添加量1–10%。",
            "應用於壓克力與非水系膠黏劑時，添加 0.3–1.5% Tyzor（如 AA-75、AA-105、TnBT）可與 -COOH 或 -OH基團反應，溶劑揮發後自發交聯；並可作為除水吸濕劑（0.5–5%）提高儲存穩定性。",
            "在底塗劑（Primer）應用中，Tyzor 稀釋溶液能在金屬、玻璃、塑膠表面形成分子級架橋鍵，提升接著劑對難接著基材的剝離強度。"
          ],
          "applications": [
            "RTV-1 矽酮密封膠",
            "溶劑型與水性壓克力接著劑",
            "聚硫接著劑",
            "聚胺酯接著劑（PUR）",
            "環氧樹脂接著劑（EP）",
            "丁基橡膠/氯丁橡膠",
            "基材底塗劑（Primer）。"
          ]
        },
        {
          "docId": "TYZ-APPL-02",
          "filename": "Application Note DK Tyzor Bulk Handling Procedures EN.pdf",
          "pdfPath": "techdatadb/2.Tyzor/3.Tyzor 應用技術資料 (12)鈦酸酯 /Application Note DK Tyzor Bulk Handling Procedures EN.pdf",
          "docType": "Application Note 應用技術手冊",
          "lang": "EN (英文)",
          "version": "原廠發行版",
          "brand": "Dorf Ketal",
          "shortLabel": "大宗儲運規範",
          "title": "Bulk Handling Procedures for Tyzor® Organic Titanates",
          "titleEn": "Application Note DK Tyzor Bulk Handling Procedures EN.pdf",
          "origin": "Bulk Handling Procedures for Tyzor® Organic Titanates (Dorf Ketal)",
          "desc": "指導 Tyzor 烷基鈦酸酯（特別是高反應活性之 Tyzor TPT、TnBT）大宗儲存、管路輸送、儲槽設計、防潮保護與安全操作規範。",
          "advantages": [
            "Tyzor 烷基鈦酸酯對水分極度敏感，接觸濕氣會迅速水解生成白色二氧化鈦水合物沉澱並釋出相應醇類，因此所有儲槽與槽車管線必須強制維持乾燥氮氣封頂（-40°C露點）。",
            "泵浦與密封件材質建議採用碳鋼或不銹鋼，密封墊圈推薦使用 PTFE 或 Viton，禁用易受醇類或溶劑侵蝕之彈性體。",
            "Tyzor TPT 凝固點約為 18°C，儲槽與輸送管線需配備保溫伴熱系統（建議維持於 25–35°C），避免結晶凍結堵塞管路。"
          ],
          "applications": [
            "化工廠大宗液體儲存",
            "散裝槽車裝卸",
            "管道伴熱與氮封輸送工程",
            "酯化與聚酯反應工廠儲槽系統。"
          ]
        },
        {
          "docId": "TYZ-APPL-03",
          "filename": "Application Note DK Tyzor Catalyst Plasticizer Production EN.pdf",
          "pdfPath": "techdatadb/2.Tyzor/3.Tyzor 應用技術資料 (12)鈦酸酯 /Application Note DK Tyzor Catalyst Plasticizer Production EN.pdf",
          "docType": "Application Note 應用技術手冊",
          "lang": "EN (英文)",
          "version": "原廠發行版",
          "brand": "Dorf Ketal",
          "shortLabel": "可塑劑生產催化",
          "title": "Tyzor® Organic Titanates as Catalysts in Plasticizer Production",
          "titleEn": "Application Note DK Tyzor Catalyst Plasticizer Production EN.pdf",
          "origin": "Tyzor® Organic Titanates - Catalysts for Plasticizer Production Technical Note (Dorf Ketal, SC0050)",
          "desc": "說明 Tyzor 鈦酸酯觸媒在鄰苯二甲酸酯（DOP、DINP）、己二酸酯（DOA）及偏苯三酸酯（TOTM）等各類可塑劑製造中的直接酯化與轉酯化反應優勢。",
          "advantages": [
            "相較於傳統硫酸或對甲苯磺酸等酸觸媒，Tyzor 觸媒無腐蝕性，且能抑制醇類脫水副反應（脫水率由 92% 降至5%），產出高純度、極低色度之可塑劑產品。",
            "商業運轉建議添加量僅為酯產物重量之 0.02–0.1 wt%，反應溫度範圍約 180–220°C，轉化率可達 99.9% 以上，反應週期大幅縮短。",
            "觸媒後處理簡便，反應結束後加入微量水或鹼性水溶液攪拌進行水解，生成的固態不溶二氧化鈦沉澱可經由常規過濾輕易分離，無廢酸水排放問題。"
          ],
          "applications": [
            "鄰苯二甲酸二辛酯（DOP）",
            "鄰苯二甲酸二異壬酯（DINP）",
            "己二酸二辛酯（DOA）",
            "偏苯三酸三辛酯（TOTM）",
            "生質可塑劑。"
          ]
        },
        {
          "docId": "TYZ-APPL-04",
          "filename": "Application Note DK Tyzor Crosslinking for Paper EN.pdf",
          "pdfPath": "techdatadb/2.Tyzor/3.Tyzor 應用技術資料 (12)鈦酸酯 /Application Note DK Tyzor Crosslinking for Paper EN.pdf",
          "docType": "Application Note 應用技術手冊",
          "lang": "EN (英文)",
          "version": "原廠發行版",
          "brand": "Dorf Ketal",
          "shortLabel": "紙張塗佈交聯",
          "title": "Tyzor® Titanates Crosslinking for Paper, Textiles and PVOH",
          "titleEn": "Application Note DK Tyzor Crosslinking for Paper EN.pdf",
          "origin": "Tyzor® Titanates Crosslinking for Paper, Textiles and Polyvinyl Alcohols (Dorf Ketal, SC0061)",
          "desc": "探討 Tyzor 水性鈦螯合物（TE、LA 及 AA 系列）在造紙施膠塗佈、紙張貼合、紡織物後整理及聚乙烯醇（PVA）不溶化處理中的交聯技術與改質效能。",
          "advantages": [
            "Tyzor LA 與 Tyzor TE 能在室溫及中性至微酸/微鹼水相中穩定分散，受熱乾燥時與澱粉或 PVA 之 -OH 基迅速形成化學交聯鍵。",
            "顯著改善牛皮紙貼合板（Kraft paper laminates）及瓦楞紙板的耐水性、濕抗張強度與耐潮開膠問題。",
            "亦廣泛應用於紡織品改質（與蠟或聚矽氧烷併用提高織物拒水性、固色率與抗污性），且 AA 系列經酸預處理後可作為添加量僅5% 之高效 PVA 不溶化劑。"
          ],
          "applications": [
            "瓦楞紙板製造",
            "牛皮紙袋貼合接著",
            "紙張表面施膠塗佈",
            "紡織品撥水防污整理劑",
            "織物固色劑",
            "PVA 耐水薄膜與不溶化塗層。"
          ]
        },
        {
          "docId": "TYZ-APPL-05",
          "filename": "Application Note DK Tyzor Direct Esterification EN.pdf",
          "pdfPath": "techdatadb/2.Tyzor/3.Tyzor 應用技術資料 (12)鈦酸酯 /Application Note DK Tyzor Direct Esterification EN.pdf",
          "docType": "Application Note 應用技術手冊",
          "lang": "EN (英文)",
          "version": "原廠發行版",
          "brand": "Dorf Ketal",
          "shortLabel": "直接酯化反應",
          "title": "Tyzor® Organic Titanates in Direct Esterification",
          "titleEn": "Application Note DK Tyzor Direct Esterification EN.pdf",
          "origin": "Tyzor® Organic Titanates - Direct Esterification Technical Note (Dorf Ketal, SC0049)",
          "desc": "詳細分析 Tyzor 烷基鈦酸酯催化羧酸與醇類直接酯化反應的動力學、觸媒選擇、製程參數與後處理方法。",
          "advantages": [
            "在己二酸與 2-乙基己醇合成 DOA 及偏苯三酸酯等直接酯化反應中，Tyzor TPT能徹底抑制傳統酸觸媒之醇脫水副反應（無烯烴副產物），大幅提高未反應醇類之回收再利用品質。",
            "反應體系需透過共沸蒸餾及時將生成水排除；一般商業推薦添加量為 0.05–0.2 wt%，操作溫度通常在 180–230°C。",
            "生成之粗酯加入 0.5–1.0% 水或中和劑進行蒸汽汽提與水解，使鈦金屬轉化為結晶水合氧化鈦顆粒，經濾過分離後可得極低酸價之成品。"
          ],
          "applications": [
            "可塑劑（DOP",
            "DBP）",
            "壓克力單體合成",
            "脂肪酸酯合成",
            "潤滑油合成基礎油",
            "聚酯樹脂合成。"
          ]
        },
        {
          "docId": "TYZ-APPL-06",
          "filename": "Application Note DK Tyzor Ferrous and Nonferrous Metal EN.pdf",
          "pdfPath": "techdatadb/2.Tyzor/3.Tyzor 應用技術資料 (12)鈦酸酯 /Application Note DK Tyzor Ferrous and Nonferrous Metal EN.pdf",
          "docType": "Application Note 應用技術手冊",
          "lang": "EN (英文)",
          "version": "原廠發行版",
          "brand": "Dorf Ketal",
          "shortLabel": "金屬表面前處理",
          "title": "Tyzor® Organic Titanates and Zirconates Ferrous and Nonferrous Metal Applications",
          "titleEn": "Application Note DK Tyzor Ferrous and Nonferrous Metal EN.pdf",
          "origin": "Ferrous and Nonferrous Metal Applications Technical Note (Dorf Ketal, SC0108)",
          "desc": "說明 Tyzor 鈦酸酯與鋯酸酯在黑色金屬與有色金屬表面處理中的應用，涵蓋底塗防腐、磷化後封閉清洗、電線漆交聯及金屬緊固件防蝕塗裝實例。",
          "advantages": [
            "Tyzor 螯合物可配製為環保無鉻清洗劑，在磷化鋼鐵表面形成不溶性保護膜，耐鹽霧腐蝕性能媲美傳統有毒六價鉻鈍化液。",
            "應用於小金屬零件（螺絲、夾片、緊固件）浸塗甩乾（Dip-spin）塗裝，Tyzor AA-75、TnBT、TOT 能黏結鋅/鋁金屬粉末，乾燥迅速且不增加鎖緊扭力。",
            "在聚酯/聚酯醯亞胺電線絕緣漆中作為交聯劑與密著促進劑，加速烘烤硬化，增強漆膜之耐熱等級與耐磨耗性能。"
          ],
          "applications": [
            "緊固件防腐塗裝（Dip-spin）",
            "鋼捲塗料（Coil coating）",
            "無鉻磷化後封閉處理",
            "漆包線絕緣漆",
            "金屬底漆。"
          ]
        },
        {
          "docId": "TYZ-APPL-07",
          "filename": "Application Note DK Tyzor Glass Surface Coatings EN.pdf",
          "pdfPath": "techdatadb/2.Tyzor/3.Tyzor 應用技術資料 (12)鈦酸酯 /Application Note DK Tyzor Glass Surface Coatings EN.pdf",
          "docType": "Application Note 應用技術手冊",
          "lang": "EN (英文)",
          "version": "原廠發行版",
          "brand": "Dorf Ketal",
          "shortLabel": "玻璃表面塗層",
          "title": "Tyzor® Organic Titanates and Zirconates in Glass Surface Coatings",
          "titleEn": "Application Note DK Tyzor Glass Surface Coatings EN.pdf",
          "origin": "Glass Surface Coatings Technical Note (Dorf Ketal, SC0046)",
          "desc": "介紹 Tyzor 鈦酸酯與鋯酸酯在玻璃表面塗裝技術，特別是玻璃瓶熱端（Hot-end）化學氣相沉積（CVD）與冷端溶膠塗層防刮防碎技術。",
          "advantages": [
            "在玻璃製瓶成型後（500–600°C 高溫區），Tyzor TPT、TnBT 經由熱裂解沉積在玻璃表面形成數十奈米均勻緻密的二氧化鈦薄膜。",
            "形成的 TiO2 奈米膜顯著填補玻璃微觀表面微裂紋，將玻璃瓶抗爆裂強度與抗衝擊性提升數倍，並作為冷端有機塗層之極佳密著底層。",
            "亦可於常溫透過溶膠凝膠（Sol-Gel）水解法塗佈，固化後賦予玻璃抗反射、彩色干涉光澤、防刮性及抗指紋表面特性。"
          ],
          "applications": [
            "玻璃容器與酒瓶熱端塗佈",
            "平板玻璃表面功能性塗層",
            "建築與車用隔熱防眩窗玻",
            "光學鏡片抗反射膜",
            "玻璃纖維增強樹脂複合材料。"
          ]
        },
        {
          "docId": "TYZ-APPL-08",
          "filename": "Application Note DK Tyzor Inorganic Filler Modification EN.pdf",
          "pdfPath": "techdatadb/2.Tyzor/3.Tyzor 應用技術資料 (12)鈦酸酯 /Application Note DK Tyzor Inorganic Filler Modification EN.pdf",
          "docType": "Application Note 應用技術手冊",
          "lang": "EN (英文)",
          "version": "原廠發行版",
          "brand": "Dorf Ketal",
          "shortLabel": "無機填料改質",
          "title": "Tyzor® Organic Titanates in Inorganic Filler Modification",
          "titleEn": "Application Note DK Tyzor Inorganic Filler Modification EN.pdf",
          "origin": "Inorganic Filler Modification Technical Note (Dorf Ketal, SC0048)",
          "desc": "闡述 Tyzor 烷氧基鈦酸酯與螯合型鈦酸酯作為偶聯劑改質無機填料（碳酸鈣、高嶺土、二氧化鈦、玻璃纖維等）的表面化學改質技術。",
          "advantages": [
            "Tyzor 鈦酸酯的一端親水鈦基團與無機填料表面的羥基/水分結合，另一端疏水有機烷氧基鏈與樹脂高分子相容，顯著降低表面自由能。",
            "使熱塑性/熱固性樹脂及塗料中的填料添加量顯著提升，同時降低研磨黏度，防止顆粒二次凝聚。",
            "大幅改善填充塑膠與複合材料的衝擊強度、拉伸模數與熔融加工流動性。"
          ],
          "applications": [
            "填充塑膠（PP",
            "PE",
            "PVC 碳酸鈣/滑石粉母粒）",
            "塗料填料分散",
            "熱固性複合材料",
            "橡膠補強填料。"
          ]
        },
        {
          "docId": "TYZ-APPL-09",
          "filename": "Application Note DK Tyzor Surface Primers EN.pdf",
          "pdfPath": "techdatadb/2.Tyzor/3.Tyzor 應用技術資料 (12)鈦酸酯 /Application Note DK Tyzor Surface Primers EN.pdf",
          "docType": "Application Note 應用技術手冊",
          "lang": "EN (英文)",
          "version": "原廠發行版",
          "brand": "Dorf Ketal",
          "shortLabel": "底塗促進劑",
          "title": "Tyzor® Organic Titanates as Surface Primers",
          "titleEn": "Application Note DK Tyzor Surface Primers EN.pdf",
          "origin": "Surface Primers Technical Note (Dorf Ketal, SC0045)",
          "desc": "說明 Tyzor 鈦酸酯作為金屬、塑膠及難接著底材（包括氟聚合物）底塗劑（Primers）的配製方法、附著促進機制與操作條件。",
          "advantages": [
            "建議稀釋濃度為 0.1–2%（如 TPT、TnBT，或加熱條件下之螯合物），施工環境濕度宜控制在 30–60%RH，避免塗層過厚或高濕環境造成粉化（powdering）。",
            "鈦酸酯水解在底材表面形成金屬-氧-底材化學共價鍵，同時與後續塗覆的油漆、油墨或接著劑樹脂的官能基（羥基、羧基）緊密交聯。",
            "顯著解決鋁合金、鍍鋅鋼板、聚烯烴、聚酯薄膜及鐵氟龍等底材之掉漆、脫膠與耐水性不良問題。"
          ],
          "applications": [
            "金屬防蝕底漆（鋼/鋁/銅）",
            "塑膠塗裝與印刷底塗（PET/PP/PE/尼龍）",
            "PTFE 氟聚合物表面改質",
            "建築與航空矽酮接著劑底塗。"
          ]
        },
        {
          "docId": "TYZ-APPL-10",
          "filename": "Application Note DK Tyzor Thawing Frozen TPT EN.pdf",
          "pdfPath": "techdatadb/2.Tyzor/3.Tyzor 應用技術資料 (12)鈦酸酯 /Application Note DK Tyzor Thawing Frozen TPT EN.pdf",
          "docType": "Application Note 應用技術手冊",
          "lang": "EN (英文)",
          "version": "原廠發行版",
          "brand": "Dorf Ketal",
          "shortLabel": "TPT 解凍操作",
          "title": "Thawing Frozen Tyzor® TPT",
          "titleEn": "Application Note DK Tyzor Thawing Frozen TPT EN.pdf",
          "origin": "Thawing Frozen Tyzor® TPT Technical Note (Dorf Ketal, SC0051)",
          "desc": "規範 Tyzor TPT（四異丙基鈦酸酯）在低於熔點（18°C）結晶凍結後的標準解凍、加熱與安全操作程序。",
          "advantages": [
            "Tyzor TPT 凍結時體積不膨脹，因此在容器或管線中結晶不會導致容器脹破或管路破裂。",
            "解凍加熱上限溫度嚴格限制於 71°C（160°F）以防產品黃變；建議滾動桶身加速熔融均勻化，解凍後冷卻並儲存於 20°C–38°C乾燥環境。",
            "桶塞必須全程密封嚴防濕氣進入，因水解釋出之異丙醇會使產品閃火點急劇降至 <-6.67°C（20°F），具高度易燃危險性。"
          ],
          "applications": [
            "桶裝/槽裝 Tyzor TPT 冬季儲存維護",
            "化學工廠投料解凍作業",
            "低溫運輸後復原。"
          ]
        },
        {
          "docId": "TYZ-APPL-11",
          "filename": "Application Note DK Tyzor Transesterification EN.pdf",
          "pdfPath": "techdatadb/2.Tyzor/3.Tyzor 應用技術資料 (12)鈦酸酯 /Application Note DK Tyzor Transesterification EN.pdf",
          "docType": "Application Note 應用技術手冊",
          "lang": "EN (英文)",
          "version": "原廠發行版",
          "brand": "Dorf Ketal",
          "shortLabel": "酯交換反應",
          "title": "Tyzor® Organic Titanates in Transesterification",
          "titleEn": "Application Note DK Tyzor Transesterification EN.pdf",
          "origin": "Tyzor® Organic Titanates - Transesterification Technical Note (Dorf Ketal, SC0053)",
          "desc": "說明 Tyzor 鈦酸酯在羧酸酯轉酯化（酯交換）反應中的觸媒選擇、反應條件控制及與傳統酸觸媒之效能對比。",
          "advantages": [
            "在丙烯酸乙酯與正癸醇合成丙烯酸正癸酯反應中，Tyzor TPT（1.0 wt%）於 60 分鐘內轉化率達 99%，遠高於硫酸（55%）與對甲苯磺酸（23%）。",
            "反應中過量的醇類不會發生酸催化引起的副反應降解，回收醇品質優良可循環使用；成品無深色副產物。",
            "轉酯化通常在較溫和溫度（約 100°C）進行，生成之低沸點醇（如甲醇、乙醇）需迅速蒸餾移除以驅動平衡。"
          ],
          "applications": [
            "特用丙烯酸酯單體合成",
            "生質柴油轉酯化",
            "聚對苯二甲酸二甲酯（DMT）製程",
            "聚碳酸酯轉酯化。"
          ]
        },
        {
          "docId": "TYZ-APPL-12",
          "filename": "Application Note DK Tyzor Vapor Pressure vs Temperature EN.pdf",
          "pdfPath": "techdatadb/2.Tyzor/3.Tyzor 應用技術資料 (12)鈦酸酯 /Application Note DK Tyzor Vapor Pressure vs Temperature EN.pdf",
          "docType": "Application Note 應用技術手冊",
          "lang": "EN (英文)",
          "version": "原廠發行版",
          "brand": "Dorf Ketal",
          "shortLabel": "蒸氣壓曲線手冊",
          "title": "Tyzor® Organic Titanates Vapor Pressure vs Temperature",
          "titleEn": "Application Note DK Tyzor Vapor Pressure vs Temperature EN.pdf",
          "origin": "Tyzor® Organic Titanates Vapor Pressure vs Temperature Technical Note (Dorf Ketal, SC0054)",
          "desc": "提供 Tyzor 系列各烷基鈦酸酯純品在 50°C 至 280°C 溫度範圍內的蒸氣壓（mbar）熱力學數據圖表。",
          "advantages": [
            "涵蓋五種代表性烷基鈦酸酯：異丙基鈦酸酯（TPT）、乙基鈦酸酯（ET）、正丙基鈦酸酯（NPT）、異丁基鈦酸酯（TIBT）及正丁基鈦酸酯（TnBT）。",
            "蒸氣壓高低順序為：TPT > ET > NPT > TIBT > TnBT；例如在 100°C 下，TPT 蒸氣壓最高（約 10 mbar 量級），而 TnBT 蒸氣壓最低。",
            "該數據曲線為反應蒸餾除醇製程、真空脫揮、化學氣相沉積（CVD）蒸發量計算及儲槽排氣防護工程之關鍵設計依據。"
          ],
          "applications": [
            "真空蒸餾製程設計",
            "化學氣相沉積（CVD/ALD）原料蒸發控制",
            "工程管線壓降計算",
            "化學儲槽排氣安全設計。"
          ]
        }
      ],
      "single": [
        {
          "docId": "TYZ-SING-01",
          "filename": "TI DK Tyzor Activate 422 for PET Bottle Resins EN.pdf",
          "pdfPath": "techdatadb/2.Tyzor/4.Tyzor 單一產品應用技術資料(2)/TI_Tyzor Activate 422/TI DK Tyzor Activate 422 for PET Bottle Resins EN.pdf",
          "docType": "I 單一產品技術資料",
          "lang": "EN (英文)",
          "version": "原廠發行版",
          "brand": "Dorf Ketal",
          "shortLabel": "Activate 422 瓶級聚酯",
          "title": "Tyzor® ACtivate™ 422 for PET Bottle Resins",
          "titleEn": "TI DK Tyzor Activate 422 for PET Bottle Resins EN.pdf",
          "origin": "Tyzor® ACtivate™ 422 for PET Bottle Resins Technical Information (Dorf Ketal)",
          "desc": "評估液態螯合鈦觸媒 Tyzor ACtivate 422 在聚酯（PET）瓶級樹脂連續縮聚及固相聚合（SSP）製程中取代銻（Antimony）觸媒的技術性能。",
          "advantages": [
            "具備高水解穩定性與優異配位基化學，熔融縮聚反應速率高，SSP 固相聚合增黏速率與三氧化二銻相當。",
            "活性極高，鈦金屬使用量（約 5–15 ppm Ti）遠低於銻觸媒（~250 ppm Sb），無重金屬灰分殘留，顯著降低瓶胚霧度（Haze）並提升光學透光度。",
            "具備良好熱穩定性，可精準控制乙醛（Acetaldehyde, AA）生成量並維持出色的聚合物色相（低 b* 黃色相）。"
          ],
          "applications": [
            "瓶級 PET 樹脂生產",
            "食品與飲料包裝容器",
            "高透光 PET 薄膜。"
          ],
          "productGroup": "Activate 專利耐水解系列"
        },
        {
          "docId": "TYZ-SING-02",
          "filename": "TI DK Tyzor Activate 422 Plastic Packaging for Food Contact EN.pdf",
          "pdfPath": "techdatadb/2.Tyzor/4.Tyzor 單一產品應用技術資料(2)/TI_Tyzor Activate 422/TI DK Tyzor Activate 422 Plastic Packaging for Food Contact EN.pdf",
          "docType": "I 單一產品技術資料",
          "lang": "EN (英文)",
          "version": "原廠發行版",
          "brand": "Dorf Ketal",
          "shortLabel": "Activate 422 食品接觸",
          "title": "Tyzor® ACtivate™ 422 Plastic Packaging for Food Contact",
          "titleEn": "TI DK Tyzor Activate 422 Plastic Packaging for Food Contact EN.pdf",
          "origin": "Tyzor® ACtivate™ 422 Plastic Packaging for Food Contact Technical Information (Dorf Ketal, SC0118)",
          "desc": "說明 Tyzor ACtivate 422 作為符合食品接觸法規的無重金屬環保鈦觸媒，在食品包裝用 PET 塑膠容器中的合規性與加工優勢。",
          "advantages": [
            "嚴格符合美國 FDA (US CFR 177.1630) 及歐盟 (EU Regulation 10/2011) 食品接觸材料合規認證，徹底杜絕傳統銻等重金屬殘留疑慮。",
            "高水解穩定性確保原料在儲存與預混過程中不析出沉澱，維持連續化反應器之均勻催化。",
            "降低熔融聚合溫度與停留時間，減少高分子熱降解，確保食品包裝無異味釋放且外觀高潔淨度。"
          ],
          "applications": [
            "食品級 PET 包裝瓶",
            "熱成型食品托盤",
            "飲料瓶胚",
            "透明食品包裝薄膜。"
          ],
          "productGroup": "Activate 專利耐水解系列"
        },
        {
          "docId": "TYZ-SING-03",
          "filename": "TI DK Tyzor IAM for Ink EN.pdf",
          "pdfPath": "techdatadb/2.Tyzor/4.Tyzor 單一產品應用技術資料(2)/TI_Tyzor IAM/TI DK Tyzor IAM for Ink EN.pdf",
          "docType": "I 單一產品技術資料",
          "lang": "EN (英文)",
          "version": "原廠發行版",
          "brand": "Dorf Ketal",
          "shortLabel": "IAM 印刷油墨",
          "title": "Tyzor® IAM Organic Titanate for Printing Inks",
          "titleEn": "TI DK Tyzor IAM for Ink EN.pdf",
          "origin": "Tyzor® IAM Organic Titanate Technical Information (Dorf Ketal)",
          "desc": "介紹專為溶劑型印刷油墨開發的鈦磷酸酯複合物 Tyzor IAM，針對傳統乙醯丙酮鈦（Tyzor AA）易黃變及釋放氣味問題提供高效替代方案。",
          "advantages": [
            "化學成分為鈦基磷酸酯複合物，TiO2 含量約 14.7%，比重 1.0，黏度約 20 mPa·s，外觀為無色至淺黃色液體。",
            "完全不含且不釋放乙醯丙酮（2,4-戊二酮），杜絕傳統交聯劑殘留氣味與法規毒性疑慮。",
            "在白墨及淺色油墨體系中表現出近乎零黃變（Δb 顯著低於 Tyzor AA-75），同時具備極高交聯乾燥速度與附著促進性（添加量1–4%）。"
          ],
          "applications": [
            "溶劑型凸版與凹版印刷油墨",
            "硝化棉（NC）油墨",
            "包裝印刷油墨（OPP/PET/PE 軟包裝薄膜）。"
          ],
          "productGroup": "IAM 油墨無黃變系列"
        },
        {
          "docId": "TYZ-SING-04",
          "filename": "TI DK Tyzor IAM for Solvent-Based Printing Ink EN.pdf",
          "pdfPath": "techdatadb/2.Tyzor/4.Tyzor 單一產品應用技術資料(2)/TI_Tyzor IAM/TI DK Tyzor IAM for Solvent-Based Printing Ink EN.pdf",
          "docType": "I 單一產品技術資料",
          "lang": "EN (英文)",
          "version": "原廠發行版",
          "brand": "Dorf Ketal",
          "shortLabel": "IAM 溶劑型油墨",
          "title": "Tyzor® IAM Technical Bulletin for Solvent-Based Printing Ink",
          "titleEn": "TI DK Tyzor IAM for Solvent-Based Printing Ink EN.pdf",
          "origin": "Tyzor® IAM Technical Bulletin (Dorf Ketal Speciality Catalyst Division)",
          "desc": "完整收錄 Tyzor IAM 在溶劑型硝化棉油墨中的實際測試數據，對比 Tyzor AA-75 在 OPP薄膜膠帶密著測試、耐水耐溶劑性及黃變指數（Δb）之詳細表現。",
          "advantages": [
            "在電暈處理 OPP 薄膜膠帶撕拔測試中，Tyzor IAM 在 >2% 濃度下展現優於 AA-75 的密著保持力（分級評分為最優的 1級，無掉漆）。",
            "耐水耐溶劑測試中，經 50/50 及 70/30 乙醇/水浸泡 1 分鐘後，油墨層完整無損，耐性表現與 AA-75 相當。",
            "在白色油墨以 BYK 分光光度計測量 b 值，2% AA-75 之 Δb 為 0.44，而 1–4% Tyzor IAM 之 Δb 僅 0.01–0.15，黃變程度大幅降低65–95%。"
          ],
          "applications": [
            "溶劑型軟包裝印刷油墨（BOPP",
            "CPP 薄膜）",
            "高遮蓋白墨",
            "硝化棉基複合包裝油墨。"
          ],
          "productGroup": "IAM 油墨無黃變系列"
        }
      ],
      "formulation": []
    }
  },
  "carbon-black": {
    "slug": "carbon-black",
    "hasData": true,
    "tabs": {
      "principles": [
        {
          "docId": "CAR-PRIN-01",
          "filename": "技術手冊碳黑 CARBON BLACK 2026-07 V1.docx",
          "pdfPath": "techdatadb/4.Orion/1.原理/技術手冊碳黑 CARBON BLACK 2026-07 V1.docx",
          "docType": "原理機制",
          "lang": "TW (繁體中文)",
          "version": "2026",
          "brand": "Orion",
          "shortLabel": "平均原生粒徑",
          "title": "平均原生粒徑(Average primary particle size)",
          "titleEn": "技術手冊碳黑 CARBON BLACK 2026-07 V1.docx",
          "origin": "技術手冊碳黑 CARBON BLACK 2026-07 V1 - 碳黑的重要技術指標：一、平均原生粒徑 (average primary particle size)",
          "desc": "說明碳黑核心指標「平均原生粒徑」與比表面積（BET）、黑度（Jetness）及抗紫外線防護力之正相關物理機制。",
          "advantages": [
            "黑度直接取決於碳黑之平均原生粒徑；粒徑越小，比表面積愈大，所顯現之碳黑黑度越高。",
            "原生粒子在生成時會聚集成原生凝聚體（Aggregate），原生粒子越小則凝聚體比表面積越大，其抗紫外線（防 UV）作用更佳。",
            "碳黑比表面積透過 BET、",
            "氮氣吸附方法測定，測定結果以每克樣品所具有之表面積（m²/g）定量表示。"
          ],
          "applications": [],
          "mechImg": "techdatadb/4.Orion/1.原理/property comparison chart.png"
        },
        {
          "docId": "CAR-PRIN-02",
          "filename": "技術手冊碳黑 CARBON BLACK 2026-07 V1.docx",
          "pdfPath": "techdatadb/4.Orion/1.原理/技術手冊碳黑 CARBON BLACK 2026-07 V1.docx",
          "docType": "原理機制",
          "lang": "TW (繁體中文)",
          "version": "2026",
          "brand": "Orion",
          "shortLabel": "結構",
          "title": "結構(Structure)",
          "titleEn": "技術手冊碳黑 CARBON BLACK 2026-07 V1.docx",
          "origin": "技術手冊碳黑 CARBON BLACK 2026-07 V1 - 二、結構 (Structure)",
          "desc": "闡述色素碳黑聚集體之空間形態結構定義，解析原生粒子透過化學鍵熔結成鏈枝狀或葡萄狀之微觀構造與高低結構分類。",
          "advantages": [
            "色素碳黑粒子不僅以原生粒子形式存在，並且在生產過程中熔結成凝聚體；這種凝聚體是由原生粒子經化學鍵結而成。",
            "碳黑的結構即碳黑聚集體的空間形態，是以碳黑粒子間聚集呈鏈狀或葡萄狀的程度來表示。",
            "在凝聚過程中，由大量鏈枝之原生凝聚體構成的碳黑稱為高結構碳黑；而原生凝聚體由較少鏈枝原生粒子組成者，則稱為低結構碳黑。"
          ],
          "applications": [],
          "mechImg": "techdatadb/4.Orion/1.原理/particle size.png"
        },
        {
          "docId": "CAR-PRIN-03",
          "filename": "技術手冊碳黑 CARBON BLACK 2026-07 V1.docx",
          "pdfPath": "techdatadb/4.Orion/1.原理/技術手冊碳黑 CARBON BLACK 2026-07 V1.docx",
          "docType": "原理機制",
          "lang": "TW (繁體中文)",
          "version": "2026",
          "brand": "Orion",
          "shortLabel": "表面處理",
          "title": "表面處理(Surface treatment)",
          "titleEn": "技術手冊碳黑 CARBON BLACK 2026-07 V1.docx",
          "origin": "技術手冊碳黑 CARBON BLACK 2026-07 V1 - 三、表面處理 (Surface Treatment)",
          "desc": "分析碳黑表面氧化後處理對改善微細粒子潤濕分散性之效應，並以揮發份（含氧官能基含量）、pH 值及極性評估表面化學改質程度。",
          "advantages": [
            "更細微原生粒子賦予碳黑更大的比表面積，同時增加分散難度，一般透過表面處理可調整碳黑潤濕性並改善分散性。",
            "表面處理程度以揮發份多寡來表示，反映碳黑表面化學之含氧官能基（羧基、醌基、內酯基及羥基）多寡與極性強弱。",
            "表面官能基直接決定酸鹼度：一般碳黑均呈鹼性（pH > 7）；只有經過後處理碳黑其 pH 值在 3–5 之間。"
          ],
          "applications": []
        },
        {
          "docId": "CAR-PRIN-04",
          "filename": "技術手冊碳黑 CARBON BLACK 2026-07 V1.docx",
          "pdfPath": "techdatadb/4.Orion/1.原理/技術手冊碳黑 CARBON BLACK 2026-07 V1.docx",
          "docType": "原理機制",
          "lang": "TW (繁體中文)",
          "version": "2026",
          "brand": "Orion",
          "shortLabel": "製程差異",
          "title": "製程差異(Process difference)",
          "titleEn": "技術手冊碳黑 CARBON BLACK 2026-07 V1.docx",
          "origin": "技術手冊碳黑 CARBON BLACK 2026-07 V1 - 四、製程差異 (Manufacturing Process Differences)",
          "desc": "比較爐法（Furnace Black）、氣黑/槽法（Gas Black）及燈黑（Lamp Black）三大生產製程在燃燒反應機制、原生粒徑範圍、表面處理程度及顏色色口差異。",
          "advantages": [
            "爐法製程於缺氧密閉爐中進行，粒徑可控範圍寬廣（15–80 nm，平均約 40 nm），未經後處理時表面化學呈弱鹼性，適合橡膠、塑膠行業應用。",
            "氣黑/槽法製程藉由多束小扇形火焰於轉鼓沉積，高溫刮取時接觸空氣自發氧化生成大量酸性基團（呈酸性 pH），粒徑極細（10–30 nm，平均 13 nm），兼具高黑度、強著色力、易分散與純正藍底色調，適合塗料行業。",
            "燈黑製程採用平坦敞開燃燒鐵盤於缺氧條件下進行熱裂解，生成粒徑分佈寬且顆粒粗大之特徵產品，易分散適合塗料調色用。"
          ],
          "applications": [
            "爐法適用於高級天然皮革",
            "合成皮革",
            "合成纖維著色",
            "塑膠製品",
            "密封膠製品",
            "農業用膜著色",
            "塑膠色母粒",
            "電線",
            "油漆",
            "油墨",
            "皮革",
            "PU合成皮。"
          ],
          "mechImg": "techdatadb/4.Orion/1.原理/processes_comparison.png"
        }
      ],
      "catalog": [
        {
          "docId": "CAR-CATA-01",
          "filename": "Brochure Orion Carbon Black CN.pdf",
          "pdfPath": "techdatadb/4.Orion/2.Orion Carbon Black 碳黑 目錄 （16）冊/Brochure Orion Carbon Black CN.pdf",
          "docType": "Brochure 總覽型錄",
          "lang": "CN (簡體中文)",
          "version": "原廠發行版",
          "brand": "Orion",
          "shortLabel": "特種碳黑型錄 (中)",
          "title": "Orion 特種碳黑 產品目錄（中文版）",
          "titleEn": "Brochure Orion Carbon Black CN.pdf",
          "origin": "Orion Engineered Carbons 特種碳黑綜合產品指南（中文版）",
          "desc": "彙整 Orion 氣法碳黑（Gas Black）、爐法碳黑（Furnace Black）、燈黑（Lamp Black）、乙炔黑（Acetylene Black）及特種導電碳黑在塗料、塑膠與印刷油墨系統之產品分類、技術規格與核心性能指標。",
          "advantages": [
            "產品涵蓋 Colour Black（如 FW 310/255/171/200）、Special Black（如 6/5/4/4A/100）、Nerox（如 600/505）、Printex（如95/300/U/V）、HiBlack 系列、Lamp Black 101，以及超高導電碳黑 Printex XE2 B（比表面積 1000 m²/g）與 Printex kappa系列。",
            "說明原生粒徑（11–95 nm）、BET 比表面積（26–1000 m²/g）、OAN 吸油值（42–420 ml/100g）與 950°C 揮發份含量（含氧酸性官能基，最高20%）對黑度（Jetness My 最高 310）、分散性、流變行為與底色相的決定性影響。",
            "氣黑法氧化後處理產品表面富含羧基與酚羥基，在極性塗料與溶劑體系中具備優異潤濕相容性、儲存黏度穩定性與藍相高黑度。"
          ],
          "applications": [
            "汽車 OEM 及修補漆",
            "電泳塗料",
            "一般工業塗料",
            "粉末塗料；聚烯烴/工程塑膠/化纖母粒",
            "電線電纜",
            "管材",
            "農膜；膠印",
            "凹版",
            "柔版包裝印刷油墨及UV/水性噴墨墨水。"
          ]
        },
        {
          "docId": "CAR-CATA-02",
          "filename": "Brochure Orion Carbon Black EN.pdf",
          "pdfPath": "techdatadb/4.Orion/2.Orion Carbon Black 碳黑 目錄 （16）冊/Brochure Orion Carbon Black EN.pdf",
          "docType": "Brochure 總覽型錄",
          "lang": "EN (英文)",
          "version": "原廠發行版",
          "brand": "Orion",
          "shortLabel": "特種碳黑型錄 (英)",
          "title": "Orion Specialty Carbon Blacks Product Guide (English)",
          "titleEn": "Brochure Orion Carbon Black EN.pdf",
          "origin": "Specialty Carbon Blacks - Technical Data Asia Pacific (Orion Engineered Carbons)",
          "desc": "彙整 Orion 亞太地區特種碳黑在塗料、塑膠與印刷油墨三大領域之技術規格（BET 比表面積、OAN 吸油值、揮發份、pH、黑度MY）、測試標準與產品選型指南。",
          "advantages": [
            "詳述物理規格參數關聯：較小原生粒徑提供更高黑度與著色力，但吸油量與比表面積增大導致分散黏度上升。",
            "爐黑製程提供寬廣的結構度（OAN）調節空間，高結構碳黑易於分散且導電性高，低結構碳黑利於高固含量填充與流平。",
            "產品系列包含 COLOUR BLACK、SPECIAL BLACK、PRINTEX、NEROX、HIBLACK、AROSPERSE、LAMP BLACK 等專利品牌等級。"
          ],
          "applications": [
            "溶劑型與水性塗料",
            "工業塗料",
            "粉末塗料",
            "平版與凹版油墨",
            "噴墨墨水",
            "合成纖維母粒。"
          ]
        }
      ],
      "applications": [
        {
          "docId": "CAR-APPL-01",
          "filename": "Application Note Orion Fastness of Specialty Carbon Blacks EN.pdf",
          "pdfPath": "techdatadb/4.Orion/3.Orion Application Note/Application Note Orion Fastness of Specialty Carbon Blacks EN.pdf",
          "docType": "Application Note 應用技術手冊",
          "lang": "EN (英文)",
          "version": "原廠發行版",
          "brand": "Orion",
          "shortLabel": "碳黑堅牢度 (TI 1460)",
          "title": "Fastness Properties of Specialty Carbon Blacks",
          "titleEn": "Application Note Orion Fastness of Specialty Carbon Blacks EN.pdf",
          "origin": "Fastness and Resistance Properties of Specialty Carbon Blacks (Orion Engineered Carbons, Technical",
          "desc": "分析特種碳黑顏料相較於有機黑色顏料在耐光性、耐候性、耐化學性、耐溫性及耐遷移性（Bleeding）等各項堅牢度（Fastness）指標的絕對優勢。",
          "advantages": [
            "爐黑與氣黑歸類為 Pigment Black #7（PBk7），燈黑歸類為 Pigment Black #6（PBk6），C.I. 結構編號均為 77266；耐光牢度達BSI 標準 7–8 級（優異 Excellent）。",
            "耐水、耐酸、耐鹼、耐有機溶劑、可塑劑、油脂與熱蠟牢度均達最高級（No bleed or discoloration，完全不滲色、不變色）。",
            "原文特別指出：若含碳黑塗料或油墨之耐性表現不良，其根本限制通常來自黏結劑樹脂系統（Binder system），而非特種碳黑本身。"
          ],
          "applications": [
            "車輛外裝塗料",
            "工程塑膠部件",
            "建築外牆氟碳烤漆",
            "農用防老化黑膜",
            "耐高溫塗層。"
          ]
        },
        {
          "docId": "CAR-APPL-02",
          "filename": "Application Note Orion Handling of Carbon Black EN.pdf",
          "pdfPath": "techdatadb/4.Orion/3.Orion Application Note/Application Note Orion Handling of Carbon Black EN.pdf",
          "docType": "Application Note 應用技術手冊",
          "lang": "EN (英文)",
          "version": "原廠發行版",
          "brand": "Orion",
          "shortLabel": "碳黑安全裝卸 (TI 1451)",
          "title": "Safe and Effective Handling of Specialty Carbon Black",
          "titleEn": "Application Note Orion Handling of Carbon Black EN.pdf",
          "origin": "Handling of Carbon Black (Orion Engineered Carbons, Technical Information TI 1451, 32 pages)",
          "desc": "全面指引特種碳黑（粉狀 Powder 與粒狀 Beads）在工廠物流、儲存、除塵、氣力輸送、開袋、下料及安全防爆方面的工程技術規範。",
          "advantages": [
            "比較粉狀（Powder，低堆積密度約 0.05–0.15 g/cm³，易起塵、分散較快）與珠狀/粒狀（Beads，堆積密度約 0.3–0.5 g/cm³，流動性佳、低粉塵）之物性差異與操作設備選型。",
            "提供粉塵爆炸預防準則：最小點火能量（MIE）、粉塵雲爆炸指數（Kst）、下爆炸極限（LEL）分析，並規範適當之接地、除塵防爆閥與惰化措施。",
            "規範密閉式氣力輸送（稀相/密相）、料斗排料防搭橋設計（振動器/破拱錐）及個人呼吸防護與通風要求。"
          ],
          "applications": [
            "塗料工廠研磨配料系統",
            "塑膠母粒擠出上料工程",
            "油墨廠物料輸送",
            "工廠安全防護與粉塵控制。"
          ]
        },
        {
          "docId": "CAR-APPL-03",
          "filename": "Application Note Orion Pigments Special Carbon Black in Modern Coatings EN.pdf",
          "pdfPath": "techdatadb/4.Orion/3.Orion Application Note/Application Note Orion Pigments Special Carbon Black in Modern Coatings EN.pdf",
          "docType": "Application Note 應用技術手冊",
          "lang": "EN (英文)",
          "version": "原廠發行版",
          "brand": "Orion",
          "shortLabel": "現代塗料系統 (0402)",
          "title": "Specialty Carbon Blacks in Modern Coating Systems",
          "titleEn": "Application Note Orion Pigments Special Carbon Black in Modern Coatings EN.pdf",
          "origin": "Carbon Black Pigments in Modern Coating Systems (Orion Engineered Carbons, Industry Information 0402, 24",
          "desc": "深入探討特種碳黑在現代環保塗料系統（高固含量、水性塗料、粉末塗料、UV 固化）中的色度學理論（My、dM）、分散安定化與流變學性能。",
          "advantages": [
            "詳細定義黑度數值 My（Jetness）與底色相 dM（Undertone，dM > 0 為藍底色，dM < 0 為棕/紅底色），說明微細粒徑產生高 My配合藍底色相帶來深邃視覺黑度。",
            "比較研磨設備效能（砂磨機、三輥機、高速分散機）與研磨配方設計（顏基比、固含量、分散劑當量吸附量），避免過磨產生二次凝聚。",
            "針對水性體系推薦後處理氧化型碳黑搭配高分子嵌段共聚物分散劑，解決水相中碳黑表面疏水難潤濕與絮凝返粗問題。"
          ],
          "applications": [
            "汽車塗裝（OEM）面漆",
            "汽車修補漆",
            "水性工業金屬漆",
            "卷鋼塗料",
            "塑膠件裝飾塗料。"
          ]
        },
        {
          "docId": "CAR-APPL-04",
          "filename": "Application Note Orion Special Black for Fibers EN.pdf",
          "pdfPath": "techdatadb/4.Orion/3.Orion Application Note/Application Note Orion Special Black for Fibers EN.pdf",
          "docType": "Application Note 應用技術手冊",
          "lang": "EN (英文)",
          "version": "原廠發行版",
          "brand": "Orion",
          "shortLabel": "纖維紡絲碳黑 (TI 1377)",
          "title": "Specialty Carbon Blacks for Synthetic Fibers",
          "titleEn": "Application Note Orion Special Black for Fibers EN.pdf",
          "origin": "Specialty Carbon Blacks for Fibers (Orion Engineered Carbons, Technical Information TI 1377, 6 pages)",
          "desc": "介紹符合 OEKO-TEX Standard 100 紡織品安全規範的化學纖維紡絲專用特種碳黑（Printex L6 SQ、Printex alpha SQ、Arosperse 11、Arosperse 138，以及 Arosperse 26）。",
          "advantages": [
            "Printex L6 SQ、Printex alpha SQ、Arosperse 11 與 Arosperse 138 符合重金屬、多環芳香烴（PAH）殘留限量標準及歐盟Directive 10/2011 規範，符合 OEKO-TEX Standard 100 第 I 類（嬰兒用品）至第 IV 類要求。",
            "具備超低殘留粗粒（Residue on 325 mesh < 10 ppm）與低凝膠（Gel）生成率，極大化延長紡絲噴絲板與熔體過濾器壽命（Filter Pressure Value, FPV 極低）。",
            "降低紡絲斷頭率（Low spin breaks）、減少高溫加工硫磺異味（Low olfactory effect），賦予化學纖維長絲均勻的高光澤黑度與柔軟手感。"
          ],
          "applications": [
            "聚酯（PET）纖維原液著色",
            "聚醯胺（PA/Nylon）紡絲母粒",
            "聚丙烯（PP）無紡布與長絲",
            "高端紡織服飾面料。"
          ]
        },
        {
          "docId": "CAR-APPL-05",
          "filename": "Application Note Orion Special Carbon Black Disperse Guideline EN.pdf",
          "pdfPath": "techdatadb/4.Orion/3.Orion Application Note/Application Note Orion Special Carbon Black Disperse Guideline EN.pdf",
          "docType": "Application Note 應用技術手冊",
          "lang": "EN (英文)",
          "version": "原廠發行版",
          "brand": "Orion",
          "shortLabel": "潤濕分散指引 (TI 1375)",
          "title": "Dispersion Guideline for Specialty Carbon Blacks in Coatings",
          "titleEn": "Application Note Orion Special Carbon Black Disperse Guideline EN.pdf",
          "origin": "Short Dispersion Guideline for Specialty Carbon Blacks in Coatings (Orion Engineered Carbons, Technical",
          "desc": "提供特種碳黑在塗料色漿中分散的三大物理步驟（潤濕、機械破碎/解聚、靜電與空間位阻安定化）之實用製程與工藝指引。",
          "advantages": [
            "研磨階段之剪切應力、珠磨機填珠率（建議 70–80% 氧化鋯珠，珠徑 0.4–0.8 mm）與研磨線速度（10–14 m/s）的精準控制要求。",
            "說明分散劑需求量（DOP 法與吸油值關聯），高比表面積碳黑需添加足量高分子分散劑以達到單分子層飽和吸附，防止脫吸附導致絮凝。",
            "制定黏度曲線、刮板細度計測定（Hegman 規要求 < 5 µm）與展色性（Rub-out 測試）等分散終點評估標準。"
          ],
          "applications": [
            "塗料研磨色漿製備",
            "萬能色漿",
            "高色素碳黑研磨工藝",
            "砂磨機製程優化。"
          ]
        },
        {
          "docId": "CAR-APPL-06",
          "filename": "Application Note Orion Special Carbon Black for Industrial Coatings EN.pdf",
          "pdfPath": "techdatadb/4.Orion/3.Orion Application Note/Application Note Orion Special Carbon Black for Industrial Coatings EN.pdf",
          "docType": "Application Note 應用技術手冊",
          "lang": "EN (英文)",
          "version": "原廠發行版",
          "brand": "Orion",
          "shortLabel": "工業防護塗料 (TI 1458)",
          "title": "Specialty Carbon Blacks for Industrial Coatings",
          "titleEn": "Application Note Orion Special Carbon Black for Industrial Coatings EN.pdf",
          "origin": "Specialty Carbon Blacks for Industrial Coatings (Orion Engineered Carbons, TI 1458, 12 pages)",
          "desc": "系統評估 Orion 特種碳黑（Printex 200/300/35、Nerox 505/600、Special Black 4/100 等）在工業塗料本色/原色黑度（mass tone）應用中之黑度表現、流變行為與耐候特性。",
          "advantages": [
            "在環氧樹脂、醇酸樹脂、聚胺酯及壓克力工業底漆與面漆中評估黑度（My 220–260）與消色力（Tinting strength）。",
            "涵蓋建築塗料、電泳漆（EDC）、耐高溫塗料、卷鋼塗料（Coil coating）與重防腐塗料五大工業體系，依膜厚與樹脂特性推薦對應之氣黑、爐黑或燈黑等級。",
            "在重防腐底漆中，低吸油值、低可溶性鹽類含量的碳黑有助於降低塗膜滲透性，增強耐鹽霧與耐濕熱保護屏障。"
          ],
          "applications": [
            "一般工業金屬塗漆",
            "重防腐鋼結構塗料",
            "農機與工程機械塗裝",
            "家電烤漆",
            "工業防腐底漆。"
          ]
        },
        {
          "docId": "CAR-APPL-07",
          "filename": "Application Note Orion Special Carbon Black for Inkjet Inks EN.pdf",
          "pdfPath": "techdatadb/4.Orion/3.Orion Application Note/Application Note Orion Special Carbon Black for Inkjet Inks EN.pdf",
          "docType": "Application Note 應用技術手冊",
          "lang": "EN (英文)",
          "version": "原廠發行版",
          "brand": "Orion",
          "shortLabel": "數位噴墨油墨 (TI 1482)",
          "title": "Specialty Carbon Blacks for Inkjet Inks",
          "titleEn": "Application Note Orion Special Carbon Black for Inkjet Inks EN.pdf",
          "origin": "Specialty Carbon Blacks for Superior Pigmented Inkjet Inks (Orion Engineered Carbons, Technical",
          "desc": "針對數位噴墨（Inkjet）印刷要求，探討水性、溶劑型及 UV 固化噴墨墨水用特種碳黑的粒徑分佈、表面改質、分散穩定性與噴嘴相容性。",
          "advantages": [
            "噴墨專用碳黑要求超窄原生粒徑分佈（平均粒徑約 15–25 nm），研磨分散後粒徑（D99 < 150 nm）無大顆粒，確保無堵塞壓電式或熱發泡噴嘴。",
            "水性噴墨推薦使用高氧化處理氣黑 NIPex IQ 系列（如 NIPex 180IQ/170IQ/160IQ），非水性與 UV 噴墨推薦 NIPex 150/90/60/35，提供高 Zeta 電位與長期儲存低沉降黏度穩定性。",
            "列印於普通紙與相片紙上展現高光學密度（OD > 1.4–1.6）、極佳邊緣銳利度（Edge acuity）與高耐摩擦/耐水抗暈染性能。"
          ],
          "applications": [
            "水性桌上型與商用噴墨墨水",
            "工業陶瓷與標籤 UV 噴墨墨水",
            "寬幅廣告溶劑型噴墨墨水",
            "紡織數位印花墨水。"
          ]
        },
        {
          "docId": "CAR-APPL-08",
          "filename": "Application Note Orion Special Carbon Black for Powder Coatings EN.pdf",
          "pdfPath": "techdatadb/4.Orion/3.Orion Application Note/Application Note Orion Special Carbon Black for Powder Coatings EN.pdf",
          "docType": "Application Note 應用技術手冊",
          "lang": "EN (英文)",
          "version": "原廠發行版",
          "brand": "Orion",
          "shortLabel": "粉體塗料碳黑 (TI 1456)",
          "title": "Specialty Carbon Blacks for Powder Coatings",
          "titleEn": "Application Note Orion Special Carbon Black for Powder Coatings EN.pdf",
          "origin": "Specialty Carbon Blacks for Powder Coatings (Orion Engineered Carbons, Technical Information TI 1293, 16",
          "desc": "評估特種碳黑在聚酯/TGIC、聚酯/Primid（HAA）、環氧及聚酯/環氧混合型粉末塗料中，於雙螺桿擠出熔融混煉下的分散機制、光澤及色相。",
          "advantages": [
            "固態粉末混煉無溶劑研磨剪切力，推薦易分散型爐黑（如 Special Black 100、Printex 30/200/35），具備適度結構以促進樹脂熔融捏合解聚。",
            "比較氣黑與爐黑對粉末塗料熔融流動性（Pellet Flow）與膠化時間的影響，氧化型碳黑之酸性官能基對部分胺催化系統具有輕微延遲膠化作用。",
            "能在低添加量（0.5–2%）下達到優異黑度、高 60° 光澤度（>90 GU）或均勻消光織紋，且不影響靜電噴塗帶電性與抗衝擊柔韌性。"
          ],
          "applications": [
            "建築鋁型材粉末塗料",
            "家電粉末塗裝",
            "汽車輪圈與底盤粉末塗料",
            "工業通用金屬粉末塗料。"
          ]
        },
        {
          "docId": "CAR-APPL-09",
          "filename": "Application Note Orion Special Carbon Black for Printing Inks EN.pdf",
          "pdfPath": "techdatadb/4.Orion/3.Orion Application Note/Application Note Orion Special Carbon Black for Printing Inks EN.pdf",
          "docType": "Application Note 應用技術手冊",
          "lang": "EN (英文)",
          "version": "原廠發行版",
          "brand": "Orion",
          "shortLabel": "包裝印刷油墨 (TI 1452)",
          "title": "Specialty Carbon Blacks for Printing Inks",
          "titleEn": "Application Note Orion Special Carbon Black for Printing Inks EN.pdf",
          "origin": "Specialty Carbon Black for Printing Inks (Orion Engineered Carbons, Industry Information II 0401, 8",
          "desc": "綜述 Orion 特種碳黑在各類傳統印刷油墨（平版膠印 Offset、凹版 Gravure、柔版 Flexo 及絲網印刷Screen）中的色度學、流變性與印刷適性。",
          "advantages": [
            "在膠印油墨中推薦使用中高結構爐黑（如 Printex 35/45），能快速建立油墨結構彈性（Tack）與屈服值，確保高速印刷油墨抗飛墨（Mist resistance）與水墨平衡。",
            "在凹版與柔版包裝油墨中推薦低結構、易流動之碳黑（如 Special Black 4A、Printex 25），提供低黏度、高墨膜遮蓋力與高光澤度。",
            "針對包裝印刷對溶劑釋放與乾燥速度之嚴格要求，碳黑適度吸油值可保證墨層快速固化乾燥與優異耐摩擦耐刮性。"
          ],
          "applications": [
            "報刊與商業平版膠印油墨",
            "塑膠薄膜凹版包裝油墨",
            "水性柔版瓦楞紙箱油墨",
            "絲網印刷厚膜油墨。"
          ]
        },
        {
          "docId": "CAR-APPL-10",
          "filename": "Application Note Orion Special Carbon Black for Tinting Coating EN.pdf",
          "pdfPath": "techdatadb/4.Orion/3.Orion Application Note/Application Note Orion Special Carbon Black for Tinting Coating EN.pdf",
          "docType": "Application Note 應用技術手冊",
          "lang": "EN (英文)",
          "version": "原廠發行版",
          "brand": "Orion",
          "shortLabel": "調色塗料碳黑 (TI 1459)",
          "title": "Specialty Carbon Blacks for Tinting Coatings",
          "titleEn": "Application Note Orion Special Carbon Black for Tinting Coating EN.pdf",
          "origin": "Specialty Carbon Blacks for Tinting Applications (Orion Engineered Carbons, Technical Information TI",
          "desc": "探討碳黑在與白色顏料（TiO2）調配灰色及複色塗料時的調色著色力（Tinting Strength）、灰度值（Greyness GY）、底色相（dG）及浮色發花行為（Floating behavior）。",
          "advantages": [
            "白稀釋時底色相發生反轉：粗粒徑碳黑（如 Lamp Black 101、Printex G、Special Black 100）呈現藍底色（Blue undertone），而細粒徑高色素碳黑則轉為紅/棕底色。",
            "浮色評級以指研測試（Rub-out）評估，浮色指數 100% 代表無分離；大粒徑與經氧化表面改質之碳黑能縮小與 TiO2粒子之動態沉降差異，將浮色率維持在接近 100% 之完美穩定狀態。",
            "比較 Printex 300、30、3 的 OAN 吸油值對調漆黏度的影響：低 OAN 結構之 Printex 300 具備較高著色力（113%）與較低研磨黏度（850 mPa·s）。"
          ],
          "applications": [
            "建築調色色漿",
            "汽車中塗漆（Primer Surfacer）",
            "工業灰色調色漆",
            "塑膠調色母粒。"
          ]
        },
        {
          "docId": "CAR-APPL-11",
          "filename": "Application Note Orion Special Carbon Black in Food Package Printing Ink EN.pdf",
          "pdfPath": "techdatadb/4.Orion/3.Orion Application Note/Application Note Orion Special Carbon Black in Food Package Printing Ink EN.pdf",
          "docType": "Application Note 應用技術手冊",
          "lang": "EN (英文)",
          "version": "原廠發行版",
          "brand": "Orion",
          "shortLabel": "食品包裝油墨 (TI 1453)",
          "title": "Specialty Carbon Blacks in Food Packaging Printing Inks",
          "titleEn": "Application Note Orion Special Carbon Black in Food Package Printing Ink EN.pdf",
          "origin": "Carbon Black Pigment for Food Packaging Printing Inks (Orion Engineered Carbons, Technical Information TI",
          "desc": "說明特種碳黑在食品包裝印刷油墨中的法規合規性要求（歐盟 EU 10/2011、瑞士條例與法國AVIS），聚焦甲苯抽出物與苯駢芘（BaP）限量標準及油墨推薦型號。",
          "advantages": [
            "符合歐盟 EU 10/2011（FCM 411，甲苯抽出物 < 0.1%，苯駢芘 BaP < 0.25 ppm）、瑞士條例 SR 817.023.21 及法國 AVIS",
            "1995（BaP ≤ 30 µg/kg）之嚴苛規範。",
            "包裝油墨專用等級推薦：單張紙/膠印推薦 PRINTEX 45/35/Nature；溶劑型推薦 PRINTEX 35、SPECIAL BLACK 350/535；水性紙箱推薦PRINTEX 3/30/Nature；UV 系統推薦 SPECIAL BLACK 350。",
            "具備高著色強度與優異流動分散性，確保包裝印刷層在超薄塗佈下仍具高遮蓋率且不會向食品內側發生化學品遷移。"
          ],
          "applications": [
            "食品包裝紙箱與紙袋水性油墨",
            "糖果與休閒食品軟包裝複合油墨",
            "飲料標籤 UV 印刷油墨。"
          ]
        },
        {
          "docId": "CAR-APPL-12",
          "filename": "Application Note Orion Special Carbon Black with Low PAHS EN.pdf",
          "pdfPath": "techdatadb/4.Orion/3.Orion Application Note/Application Note Orion Special Carbon Black with Low PAHS EN.pdf",
          "docType": "Application Note 應用技術手冊",
          "lang": "EN (英文)",
          "version": "原廠發行版",
          "brand": "Orion",
          "shortLabel": "低 PAHs 環保碳黑 (TI 1483)",
          "title": "Specialty Carbon Blacks with Low PAHs",
          "titleEn": "Application Note Orion Special Carbon Black with Low PAHS EN.pdf",
          "origin": "Carbon Blacks with Low Amount of Polycyclic Aromatic Hydrocarbons (PAHs) (Orion Engineered Carbons,",
          "desc": "深入分析特種碳黑中多環芳香烴（Polycyclic Aromatic Hydrocarbons, PAHs）之生成機理、檢測標準（AfPS GS 2019:01 PAK）與極低 PAH 系列產品特性。",
          "advantages": [
            "德國 GS Mark 認證將材料分為第 1 類（可放入口中或接觸兒童玩具，總 PAH < 1 mg/kg）至第 3 類；Orion 開發之專用爐黑具備工業領先之極低PAH 含量。",
            "產品涵蓋 Low PAH 特殊等級（如 Printex nature、Arosperse 7 系列），原生粒徑 17–25 nm，嚴格控制 15 種關鍵 PAH物質含量均低於檢測限度。",
            "保持優異物理性能：黑度高、著色力強、流變黏度低且高溫熱穩定性優異，完全無需犧牲著色效果即可達到嚴苛環保標準。"
          ],
          "applications": [
            "兒童玩具塑膠與塗料",
            "消費電子手持外殼",
            "食品接觸塑膠製品",
            "橡膠握把",
            "環保運動器材。"
          ]
        }
      ],
      "single": [
        {
          "docId": "CAR-SING-01",
          "filename": "TI Orion Colour Black FW 310 in Coating CN.pdf",
          "pdfPath": "techdatadb/4.Orion/4.Orion Carbon Black 碳黑 單一產品/TI Orion Colour Black FW 310 in Coating CN.pdf",
          "docType": "I 單一產品技術資料",
          "lang": "CN (簡體中文)",
          "version": "原廠發行版",
          "brand": "Orion",
          "shortLabel": "FW 310 超高黑度碳黑在水性及油性塗料中應用(中文版)",
          "title": "Colour Black FW 310 在塗料中的應用技術資料（中文版）",
          "titleEn": "TI Orion Colour Black FW 310 in Coating CN.pdf",
          "origin": "Colour Black FW 310 水性和溶劑型塗料用超高黑度特種碳黑 (中文版, Orion Technical Information TI 1485, 8",
          "desc": "Colour Black FW 310 在汽車面漆、高檔工業塗料及消費性電子產品中實現超深黑度（Ultra-High Jetness）與深藍相的特性。",
          "advantages": [
            "平均原生粒徑約 11 nm 且粒徑呈單峰分佈，賦予塗層無與倫比的超高黑度值（My > 310）與強烈深藍相（dM）。",
            "表面富含官能基，展現絕佳的潤濕性與樹脂相容性，且能同時適用於水性體系與油性體系。",
            "展現優異抗絮凝與耐光性，滿足頂級外觀面漆最嚴苛的光澤與鏡面黑度要求。"
          ],
          "applications": [
            "汽車面漆",
            "汽車修補漆",
            "高端消費性電子產品",
            "鋼琴裝飾塗料。"
          ],
          "productGroup": "Colour Black 超高色素氣黑系列"
        },
        {
          "docId": "CAR-SING-02",
          "filename": "TI Orion Colour Black FW 310 in Coating EN.pdf",
          "pdfPath": "techdatadb/4.Orion/4.Orion Carbon Black 碳黑 單一產品/TI Orion Colour Black FW 310 in Coating EN.pdf",
          "docType": "I 單一產品技術資料",
          "lang": "EN (英文)",
          "version": "原廠發行版",
          "brand": "Orion",
          "shortLabel": "FW 310 超高黑度碳黑在水性及油性塗料中應用(英文版)",
          "title": "Colour Black FW 310 in Coatings Technical Information (English)",
          "titleEn": "TI Orion Colour Black FW 310 in Coating EN.pdf",
          "origin": "COLOUR BLACK FW 310 Specialty Carbon Black for Ultra-High Jetness in Water-borne and Solvent-borne",
          "desc": "詳細測試 Colour Black FW 310 搭配商業潤濕分散劑（Efka PX 4701、PX 4320、Edaplan 935、Tego Dispers 673、Solsperse 37500、Borchi Gen 0451）於水性及溶劑型系統之研磨配方與色度學數據。",
          "advantages": [
            "測試證實分散劑之選擇對 FW 310 之黑度 My 與藍相 dM 具關鍵影響，配合優選分散劑（如 Efka PX 4701 或 Solsperse 37500）可完全釋放超過 320 的極限黑度。",
            "於溶劑型研磨色漿配方中（以 Laropal A81 為研磨樹脂，10% 碳黑添加量），黏度維持在穩定流動區間，無假稠與反粗現象。",
            "在水性鋁粉金屬漆對比測試中，多角度（15°/25°/45°/75°/110°）分光光度分析顯示 FW 310 提供較 FW 171 與 FW 255更溫暖、更獨特的金屬質感光澤擴展色域。"
          ],
          "applications": [
            "奢華汽車面漆",
            "高端工業鋼琴黑塗料",
            "高光金屬閃光漆",
            "水性與溶劑型高色素裝飾塗層。"
          ],
          "productGroup": "Colour Black 超高色素氣黑系列"
        }
      ],
      "formulation": []
    }
  },
  "maleic": {
    "slug": "maleic",
    "hasData": false,
    "tabs": {
      "principles": [],
      "catalog": [],
      "applications": [],
      "single": [],
      "formulation": []
    }
  },
  "px": {
    "slug": "px",
    "hasData": false,
    "tabs": {
      "principles": [],
      "catalog": [],
      "applications": [],
      "single": [],
      "formulation": []
    }
  },
  "silane": {
    "slug": "silane",
    "hasData": false,
    "tabs": {
      "principles": [],
      "catalog": [],
      "applications": [],
      "single": [],
      "formulation": []
    }
  },
  "wax": {
    "slug": "wax",
    "hasData": true,
    "tabs": {
      "principles": [
        {
          "docId": "WAX-PRIN-01",
          "filename": "技術手冊  微粉蠟 2026-08-14.docx",
          "pdfPath": "techdatadb/5. MPI/1.原理/技術手冊  微粉蠟 2026-08-14.docx",
          "docType": "原理機制",
          "lang": "TW (繁體中文)",
          "version": "2026",
          "brand": "Micro Powders",
          "shortLabel": "作用原理",
          "title": "微粉蠟技術資料：作用原理",
          "titleEn": "技術手冊  微粉蠟 2026-08-14.docx",
          "origin": "宏威應用材料 技術資料:蠟粉 微粉蠟 - 作用原理",
          "desc": "闡明微粉蠟於塗料與油墨成膜過程中之兩大核心物理機制：「漂浮理論」（成膜時向表面遷移聚集）與「球軸效應」（突顯於塗膜外提供滾珠摩擦防護）。",
          "advantages": [
            "漂浮理論：蠟粉分散在塗料中，在塗料施工後的塗膜乾燥或固化交聯成膜時，蠟會向塗膜表面漂移，遷移到塗膜表面，產生應有的效果。",
            "球軸效應：此效應在於蠟本身的粒徑大小與塗層膜厚相近，甚至更大，因而顯露在外，使得蠟粉的耐刮、耐擦傷性能得以展現。",
            "蠟可藉由塗層系統中不同化學品種、添加量或粒徑大小調控，精準影響並優化表面性能。"
          ],
          "applications": [
            "塗料",
            "印刷油墨。"
          ],
          "mechImg": "techdatadb/5. MPI/1.原理/作用原理.png"
        },
        {
          "docId": "WAX-PRIN-02",
          "filename": "技術手冊  微粉蠟 2026-08-14.docx",
          "pdfPath": "techdatadb/5. MPI/1.原理/技術手冊  微粉蠟 2026-08-14.docx",
          "docType": "原理機制",
          "lang": "TW (繁體中文)",
          "version": "2026",
          "brand": "Micro Powders",
          "shortLabel": "微粉蠟品種及功能",
          "title": "微粉蠟技術資料：微粉蠟品種及功能",
          "titleEn": "技術手冊  微粉蠟 2026-08-14.docx",
          "origin": "宏威應用材料 技術資料:蠟粉 微粉蠟 - 一、微粉蠟品種及功能",
          "desc": "整理四大常見微粉蠟化學品種類（PE蠟、PP蠟、PTFE蠟）之改質功能特徵與常規添加量標準。",
          "advantages": [
            "PE 蠟（聚乙烯蠟）特點為柔和、手感好、滑爽且具備優異經濟性。",
            "PP 蠟（聚丙烯蠟）特點為具備消光效果、硬度高且耐刮性優良。",
            "PTFE 蠟則提供滑爽、耐刮、耐磨擦、耐高溫與手感改善效果。"
          ],
          "applications": [],
          "mechImg": "techdatadb/5. MPI/1.原理/指標.png"
        },
        {
          "docId": "WAX-PRIN-03",
          "filename": "技術手冊  微粉蠟 2026-08-14.docx",
          "pdfPath": "techdatadb/5. MPI/1.原理/技術手冊  微粉蠟 2026-08-14.docx",
          "docType": "原理機制",
          "lang": "TW (繁體中文)",
          "version": "2026",
          "brand": "Micro Powders",
          "shortLabel": "粒徑及粒徑分布",
          "title": "微粉蠟技術資料：粒徑及粒徑分布",
          "titleEn": "技術手冊  微粉蠟 2026-08-14.docx",
          "origin": "宏威應用材料 技術資料:蠟粉 微粉蠟 - 二、粒徑及粒徑分布",
          "desc": "探討微粉蠟粒徑大小與粒徑分佈寬窄對漆膜光澤（全反射/漫反射消光作用）及表面觸感（細膩滑爽、柔感、特殊織紋）之影響規律。",
          "advantages": [
            "粒徑對光澤之影響：一般粒徑小於 1 µm，不影響光澤；當粒徑大於 1 µm 則對光澤會產生影響，即具備一定的消光效果。",
            "粒徑對手感之影響：一般蠟粒徑大於 5 µm，會產生不同的手感，隨著粒徑增大則會產生由細膩滑爽到特殊織紋效果，柔感亦需要較大粒徑。",
            "粒徑分佈之影響：粒徑分佈較寬的蠟粉消光性較強，與消光劑併用具協同效應，可降低消光粉使用量並呈現不同的表面手感；粒徑分佈窄則可產生較均勻手感。"
          ],
          "applications": []
        },
        {
          "docId": "WAX-PRIN-04",
          "filename": "技術手冊  微粉蠟 2026-08-14.docx",
          "pdfPath": "techdatadb/5. MPI/1.原理/技術手冊  微粉蠟 2026-08-14.docx",
          "docType": "原理機制",
          "lang": "TW (繁體中文)",
          "version": "2026",
          "brand": "Micro Powders",
          "shortLabel": "分散性及應用方便性",
          "title": "微粉蠟技術資料：分散性及應用方便性",
          "titleEn": "技術手冊  微粉蠟 2026-08-14.docx",
          "origin": "宏威應用材料 技術資料:蠟粉 微粉蠟 - 三、分散性及應用方便性",
          "desc": "說明微粉化蠟與蠟漿兩大商品形態之應用特徵，並規範塗料生產時微粉化蠟之低速潤濕與高速分散工藝要求。",
          "advantages": [
            "工業常用微粉蠟形態主要有兩種：一種是微粉化蠟，另一種是蠟漿。",
            "塗料生產過程中，微粉蠟可按配方比例緩慢加入塗料體系中進行投料。",
            "操作流程要求先以低速分散進行潤濕浸潤，隨後將攪拌速度提升至每分鐘 1200 轉進行高速分散，持續攪拌直至完全混合均勻。"
          ],
          "applications": []
        },
        {
          "docId": "WAX-PRIN-05",
          "filename": "技術手冊  微粉蠟 2026-08-14.docx",
          "pdfPath": "techdatadb/5. MPI/1.原理/技術手冊  微粉蠟 2026-08-14.docx",
          "docType": "原理機制",
          "lang": "TW (繁體中文)",
          "version": "2026",
          "brand": "Micro Powders",
          "shortLabel": "熔點對其表面性能的影響",
          "title": "微粉蠟技術資料：熔點對其表面性能的影響",
          "titleEn": "技術手冊  微粉蠟 2026-08-14.docx",
          "origin": "宏威應用材料 技術資料:蠟粉 微粉蠟 - 四、熔點對其表面性能的影響",
          "desc": "分析微粉蠟熔點高低（100–140°C 與 >140°C）對塗膜表面軟硬度、滑爽手感、抗刮傷、抗金屬劃痕及防滑耐磨機械性能之影響。",
          "advantages": [
            "當熔點介於 100～140°C 時，軟硬兼具、具備滑爽手感且可提高表面機械性能（如抗刮傷、抗金屬劃痕等）。",
            "當熔點大於 140°C 時，蠟的防滑性較好，可抗滑、耐磨且抗刮傷。",
            "熔點高低直接調控塗膜表面軟硬度、滑爽與防滑平衡，以及耐刮磨等表面機械改質效果。"
          ],
          "applications": []
        },
        {
          "docId": "WAX-PRIN-06",
          "filename": "技術手冊  微粉蠟 2026-08-14.docx",
          "pdfPath": "techdatadb/5. MPI/1.原理/技術手冊  微粉蠟 2026-08-14.docx",
          "docType": "原理機制",
          "lang": "TW (繁體中文)",
          "version": "2026",
          "brand": "Micro Powders",
          "shortLabel": "極性對其表面性能的影響",
          "title": "微粉蠟技術資料：極性對其表面性能的影響",
          "titleEn": "技術手冊  微粉蠟 2026-08-14.docx",
          "origin": "宏威應用材料 技術資料:蠟粉 微粉蠟 - 五、極性對其表面性能的影響",
          "desc": "剖析低極性、中極性與高極性微粉蠟（石蠟、棕櫚蠟、低密度與高密度聚乙烯蠟）在疏水性、抗結塊性、硬度與滑爽手感之差異表現。",
          "advantages": [
            "低極性微粉蠟疏水性佳、抗黏結性佳，如石蠟。",
            "高極性的蠟相對滑爽且硬度高，如巴西棕櫚蠟。",
            "中極性的蠟則兼具兩者性能，如低密度的聚乙烯蠟。"
          ],
          "applications": []
        }
      ],
      "catalog": [
        {
          "docId": "WAX-CATA-01",
          "filename": "Brochure MPI Industrial PTFE Alternatives EN 2026.pdf",
          "pdfPath": "techdatadb/5. MPI/2.Brochure MPI 微粉蠟 目錄15 冊/Brochure MPI Industrial PTFE Alternatives EN 2026.pdf",
          "docType": "Brochure 總覽型錄",
          "lang": "EN (英文)",
          "version": "2026",
          "brand": "Micro Powders",
          "shortLabel": "PTFE 無氟替代指南",
          "title": "Micro Powders Industrial PTFE Alternatives Guide",
          "titleEn": "Brochure MPI Industrial PTFE Alternatives EN 2026.pdf",
          "origin": "Industrial PTFE Alternatives Guide (Micro Powders, Inc. 2026)",
          "desc": "彙編 Micro Powders 針對 PFAS 禁用與環保法規所研發之全系列無氟（PFAS-Free / PTFE-Free）微粉蠟添加劑，全面替代傳統含氟聚合物。",
          "advantages": [
            "涵蓋改質聚乙烯、天然生質蠟、微粉高分子複合蠟及特殊聚烯烴產品（如 Polyglide 系列、MicroTex 950、Superslip系列、MPP-611AL）。",
            "在塗層中提供等同甚至超越傳統 PTFE 蠟之滑爽性（動摩擦係數 COF 顯著降至 0.16–0.21）、鉛筆硬度（達 F/HB）與優異耐磨耗性。",
            "具備全球食品接觸合規性與多國認證，部分耐高溫等級（如 NatureMatte C44、Spherex）耐熱溫度更高達 230–260°C 以上。"
          ],
          "applications": [
            "卷鋼塗料（Coil Coatings）",
            "罐頭與容器塗料",
            "粉末塗料",
            "工業木器漆",
            "包裝印刷油墨。"
          ]
        },
        {
          "docId": "WAX-CATA-02",
          "filename": "Brochure MPI Specialty Wax Additives and Fine Powders EN 2026.pdf",
          "pdfPath": "techdatadb/5. MPI/2.Brochure MPI 微粉蠟 目錄15 冊/Brochure MPI Specialty Wax Additives and Fine Powders EN 2026.pdf",
          "docType": "Brochure 總覽型錄",
          "lang": "EN (英文)",
          "version": "2026",
          "brand": "Micro Powders",
          "shortLabel": "微粉蠟產品目錄總覽",
          "title": "Micro Powders Specialty Wax Additives and Fine Powders Product Catalog",
          "titleEn": "Brochure MPI Specialty Wax Additives and Fine Powders EN 2026.pdf",
          "origin": "Specialty Wax Additives and Fine Powders Product Catalog (Micro Powders, Inc. 2026, 12 pages)",
          "desc": "完整收錄 Micro Powders全產品線物理規格參數表，包含聚乙烯蠟（MPP）、費托合成蠟（MP）、聚丙烯蠟（PropylMatte）、天然生質蠟、微粉聚胺酯（MicroTouch）及水性蠟分散體（Microspersion）等微粉與分散體系列。",
          "advantages": [
            "提供微粉蠟之化學組成、熔點（54°C 至 >260°C）、密度（0.89–2.13 g/cm³）、平均粒徑（d50 由 3 µm 至 425 µm，粗織紋粉最大達841 µm）等完整物性參數。",
            "產品依應用功能劃分：表面耐久改質（滑爽、耐磨耗、抗刮傷與抗結塊）、消光抗拋光、撥水性、織紋效果與軟觸感手感。",
            "規範微粉蠟應用最佳實踐工藝：強調表面張力潤濕原則，建議預先製備高濃度濃縮分散漿（Concentrated dispersion）以避免乾粉直接投料結團。"
          ],
          "applications": [
            "油漆與塗料（建築/工業/木器/車用）",
            "印刷油墨（能量固化/膠印/凹版）",
            "皮革與塑膠塗層",
            "無機與有機粉末塗料。"
          ]
        }
      ],
      "applications": [
        {
          "docId": "WAX-APPL-01",
          "filename": "Application Note MPI Advanced Composite Selector Guide PFAS Free EN 2025.pdf",
          "pdfPath": "techdatadb/5. MPI/3.Application Note MPI  wax/Application Note MPI Advanced Composite Selector Guide PFAS Free EN 2025.pdf",
          "docType": "Application Note 應用技術手冊",
          "lang": "EN (英文)",
          "version": "2025",
          "brand": "Micro Powders",
          "shortLabel": "先進複合材料 (PFAS-Free)",
          "title": "MPI Advanced Composite Selector Guide PFAS Free",
          "titleEn": "Application Note MPI Advanced Composite Selector Guide PFAS Free EN 2025.pdf",
          "origin": "Advanced Composite Selector Guide PFAS Free (Micro Powders, Inc. 2025)",
          "desc": "提供全系列無 PFAS 高級複合微粉蠟產品在塗料與油墨各細分領域中的快速選型矩陣指南。",
          "advantages": [
            "收錄 10 款無 PFAS 高級複合微粉蠟，分為氧化鋁奈米複合（MicroKlear、MP-28AL、MPP-AL、Superslip 系列）與陶瓷奈米複合（PolyGlide 1226XF、PolyTuf 1229、SuperGlide 1231）。",
            "矩陣明確評比各牌號之耐刮痕性（Scratch）、耐磨耗性（Abrasion）以及超薄塗膜適用性（Ultra-Thin Film Coatings）。",
            "提供清透度、滑爽性、抗結塊、熱脫模、易水散及耐拋光（Anti-burnish）等多元附加效益對比。"
          ],
          "applications": [
            "罐頭與容器塗料",
            "高生物基包裝塗層",
            "一般工業塗層",
            "地坪塗料",
            "OEM 木器與工業塗層",
            "粉末塗料。"
          ]
        },
        {
          "docId": "WAX-APPL-02",
          "filename": "Application Note MPI How to Disperse Micronized Wax EN 2024.pdf",
          "pdfPath": "techdatadb/5. MPI/3.Application Note MPI  wax/Application Note MPI How to Disperse Micronized Wax EN 2024.pdf",
          "docType": "Application Note 應用技術手冊",
          "lang": "EN (英文)",
          "version": "2024",
          "brand": "Micro Powders",
          "shortLabel": "微粉蠟高效分散指引",
          "title": "How to Disperse Micronized Wax",
          "titleEn": "Application Note MPI How to Disperse Micronized Wax EN 2024.pdf",
          "origin": "How to Disperse Micronized Wax Application Note (Micro Powders, Inc. 2024, 4 pages)",
          "desc": "詳細說明微粉蠟在塗料與油墨配方中的正確分散製程、設備選擇、葉輪線速度計算及避免過熱結晶凝聚的最佳實踐。",
          "advantages": [
            "推薦使用 Conn ITT 高剪切分散盤；實驗室葉輪尖端線速度建議為 5–7 m/s（1,000–1,500 FPM），量產工廠環境則建議 22–26 m/s（4,000–5,000 FPM）。",
            "嚴格控制分散研磨溫度：溶劑型體系溫度必須嚴格控制在 40°C（104°F）以下，避免微粉蠟溶解並於冷卻後產生二次重結晶粗粒。",
            "提供溶劑型預分散漿（35% 蠟）與水性體系（界面活性劑法 50% 蠟 / 樹脂載體法 25% 蠟）之製備配方，並建議使用 NPIRI 或Hegman 刮板細度計檢驗分散均勻度。"
          ],
          "applications": [
            "塗料研磨調漆工藝",
            "油墨高速分散調配",
            "水性與溶劑型色漿製備工藝規範。"
          ]
        },
        {
          "docId": "WAX-APPL-03",
          "filename": "Application Note MPI MicroTouch EN.pdf",
          "pdfPath": "techdatadb/5. MPI/3.Application Note MPI  wax/Application Note MPI MicroTouch EN.pdf",
          "docType": "Application Note 應用技術手冊",
          "lang": "EN (英文)",
          "version": "原廠發行版",
          "brand": "Micro Powders",
          "shortLabel": "MicroTouch 觸感助劑",
          "title": "MicroTouch Soft Touch Coating Additives Brochure",
          "titleEn": "Application Note MPI MicroTouch EN.pdf",
          "origin": "MicroTouch Soft Touch Coating Additives (Micro Powders, Inc.)",
          "desc": "介紹微米級球形脂肪族聚胺酯粉末 MicroTouch 系列（800F、800VF、800XF、850XF）在水性及溶劑型塗料中賦予多樣化皮革觸感、消光與抗刮性能。",
          "advantages": [
            "100% 脂肪族交聯球形 PU 微顆粒，密度 1.02–1.05 g/cc，平均粒徑 d50 分為 5–9 µm（850XF/800XF）、11–15 µm（800VF）及22–30 µm（800F）。",
            "搭配不同 Tg 樹脂可創造多種觸感效果：高 Tg 硬樹脂配方呈現絲綢般滑順觸感（Silky/Satiny feel）；低 Tg軟樹脂配方則呈現橡膠彈性觸感（Rubbery）或鵝絨觸感（Fuzzy feel）。",
            "耐熱溫度達 100–120°C（高於 140°C 會熔脹沾黏），在極低添加量下兼具優異消光效率（60° 光澤自 70–80 GU 驟降至 5–10 GU）與卓越的 Taber 耐磨耗性。"
          ],
          "applications": [
            "水性聚胺酯（PUD）皮革塗層",
            "消費電子塑膠外殼軟觸感漆",
            "車載內飾塗裝",
            "高級紙張包裝塗層。"
          ]
        },
        {
          "docId": "WAX-APPL-04",
          "filename": "Application Note MPI SelectorGuide Can Container Coatings EN 2026.pdf",
          "pdfPath": "techdatadb/5. MPI/3.Application Note MPI  wax/Application Note MPI SelectorGuide Can Container Coatings EN 2026.pdf",
          "docType": "Application Note 應用技術手冊",
          "lang": "EN (英文)",
          "version": "2026",
          "brand": "Micro Powders",
          "shortLabel": "罐頭金屬塗層選用",
          "title": "MPI Selector Guide for Can and Container Coatings",
          "titleEn": "Application Note MPI SelectorGuide Can Container Coatings EN 2026.pdf",
          "origin": "Selector Guide - Can & Container Coatings (Micro Powders, Inc. 2026)",
          "desc": "針對食品與飲料金屬罐頭、兩片罐/三片罐、金屬瓶蓋與桶裝容器塗層，提供符合食品法規之微粉蠟選型手冊。",
          "advantages": [
            "符合美國 FDA 21 CFR § 175.300（樹脂與高分子金屬塗層）及相關國際食品安全規範。",
            "涵蓋聚乙烯、改質巴西棕櫚蠟、醯胺蠟與陶瓷複合微粉蠟，提供優異之滑爽移動性（Slip & Mobility）、瓶蓋密封附著力與肉類脫模性（Meat Release）。",
            "具備卓越之耐熱性（Heat Resistance）、防潮耐濕性（Moisture Resistance）與保光性，建議常規添加量為 0.5%–2.0%（特殊效果可至",
            "0%）。"
          ],
          "applications": [
            "飲料罐內外塗層",
            "食品罐頭金屬塗料",
            "氣霧罐",
            "金屬瓶蓋旋蓋塗層",
            "深衝金屬罐成型加工。"
          ]
        },
        {
          "docId": "WAX-APPL-05",
          "filename": "Application Note MPI SelectorGuide Energy Curable Inks and Coatings EN 2026.pdf",
          "pdfPath": "techdatadb/5. MPI/3.Application Note MPI  wax/Application Note MPI SelectorGuide Energy Curable Inks and Coatings EN 2026.pdf",
          "docType": "Application Note 應用技術手冊",
          "lang": "EN (英文)",
          "version": "2026",
          "brand": "Micro Powders",
          "shortLabel": "UV/EB 固化塗料油墨",
          "title": "MPI Selector Guide for Energy Curable Inks and Coatings",
          "titleEn": "Application Note MPI SelectorGuide Energy Curable Inks and Coatings EN 2026.pdf",
          "origin": "Selector Guide - Energy Curable Inks and Coatings (Micro Powders, Inc. 2026)",
          "desc": "指引 Micro Powders 各類微粉蠟與消光粉在 100% 固含量 UV 光固化與電子束（EB）固化油墨與塗料中的選用與配方調控。",
          "advantages": [
            "針對能量固化（UV/EB）油墨與塗料體系，提供滑爽潤滑、耐磨抗刮、硬度提升與抗結塊改質方案。",
            "涵蓋 MicroMatte 1213 UVW / 2000、PropylMatte 31HD、PolyGlide 1226XF、MicroTouch 系列等無氟環保牌號。",
            "矩陣明確評比各牌號之耐刮磨性、滑爽潤滑、消光保光、清透度、膠帶脫模性（Tape Release）與軟觸感，建議添加量一般為",
            "5%–3.0%（特殊手感可至 10.0%）。"
          ],
          "applications": [
            "UV 固化木器漆",
            "UV 柔版與膠印油墨",
            "UV 罩光清漆（Overprint Varnish",
            "OPV）",
            "電子束固化包裝塗料。"
          ]
        },
        {
          "docId": "WAX-APPL-06",
          "filename": "Application Note MPI SelectorGuide Industrial Coatings EN 2026.pdf",
          "pdfPath": "techdatadb/5. MPI/3.Application Note MPI  wax/Application Note MPI SelectorGuide Industrial Coatings EN 2026.pdf",
          "docType": "Application Note 應用技術手冊",
          "lang": "EN (英文)",
          "version": "2026",
          "brand": "Micro Powders",
          "shortLabel": "工業塗料選用指南",
          "title": "MPI Selector Guide for Industrial Coatings",
          "titleEn": "Application Note MPI SelectorGuide Industrial Coatings EN 2026.pdf",
          "origin": "Selector Guide - Industrial Coatings (Micro Powders, Inc. 2026)",
          "desc": "提供微粉蠟添加劑在通用工業塗料、金屬漆、卷鋼塗料、家電塗料及防腐塗裝體系中的完整選型表。",
          "advantages": [
            "依據水性與溶劑型工業體系，推薦聚乙烯蠟（MPP-611AL、MPP-620VF/XF）、合成複合蠟（MP-28AL）、陶瓷複合蠟（PolyGlide 1226XF）及無氟滑劑（Superslip 系列）。",
            "矩陣明確評比耐刮磨、抗拋光（Burnish Resistance）、抗金屬劃痕（Metal Mark Resistance）、表觀硬度、抗結塊與早期耐水性等多重防護指標。",
            "提供消光光澤控制、織紋效果、軟觸感手感、增加動摩擦係數（防滑）及開罐穩定性評等，常規建議添加量介於 0.5%–5.0%。"
          ],
          "applications": [
            "一般工業金屬塗裝",
            "工程機械塗裝",
            "家電烤漆",
            "鋼捲卷鋼塗料（Coil Coatings）",
            "重防腐底漆與面漆。"
          ]
        },
        {
          "docId": "WAX-APPL-07",
          "filename": "Application Note MPI SelectorGuide Industrial Flooring Coatings EN 2026.pdf",
          "pdfPath": "techdatadb/5. MPI/3.Application Note MPI  wax/Application Note MPI SelectorGuide Industrial Flooring Coatings EN 2026.pdf",
          "docType": "Application Note 應用技術手冊",
          "lang": "EN (英文)",
          "version": "2026",
          "brand": "Micro Powders",
          "shortLabel": "工業地坪耐磨塗料",
          "title": "MPI Selector Guide for Industrial Flooring Coatings",
          "titleEn": "Application Note MPI SelectorGuide Industrial Flooring Coatings EN 2026.pdf",
          "origin": "Selector Guide - Industrial Flooring Coatings (Micro Powders, Inc. 2026)",
          "desc": "指導工業地坪塗料（環氧地坪、聚胺酯地坪、聚天門冬氨酸酯 Polyaspartic 地坪）中抗磨損、防滑與消光微粉添加劑的選配。",
          "advantages": [
            "收錄微粉蠟、耐磨奈米複合微粉及粗顆粒聚丙烯砂紋粉（PropylTex、NyloTex 系列），適用於混凝土、木質及層壓地坪體系。",
            "兼顧擦傷與耐磨損性（Scuff & Abrasion Resistance）、防滑性（Non-Skid）與光澤消光調控。",
            "提供優異之抗鞋跟印痕（Heel Mark Resistance）、抗熱輪胎黏胎撕起（Hot Tire Pick up &Resistance）、撥水性與易清潔性（Cleanability）。"
          ],
          "applications": [
            "環氧樹脂工業自平地坪",
            "聚胺酯薄塗地坪",
            "聚天門冬氨酸酯快速固化地坪",
            "商業耐磨地板清漆。"
          ]
        },
        {
          "docId": "WAX-APPL-08",
          "filename": "Application Note MPI SelectorGuide Powder Coatings EN 2026.pdf",
          "pdfPath": "techdatadb/5. MPI/3.Application Note MPI  wax/Application Note MPI SelectorGuide Powder Coatings EN 2026.pdf",
          "docType": "Application Note 應用技術手冊",
          "lang": "EN (英文)",
          "version": "2026",
          "brand": "Micro Powders",
          "shortLabel": "粉體塗料選用指南",
          "title": "MPI Selector Guide for Powder Coatings",
          "titleEn": "Application Note MPI SelectorGuide Powder Coatings EN 2026.pdf",
          "origin": "Selector Guide - Powder Coatings (Micro Powders, Inc. 2026)",
          "desc": "彙整粉末塗料用微粉蠟、無氟砂紋劑（Texturing agents）、脫氣劑與抗結塊助劑之綜合選型指引。",
          "advantages": [
            "推薦無氟織紋消光劑 MicroTex 950 / 975（改質聚烯烴，最大粒徑 74 µm，全面替代 PTFE 砂紋粉）、石墨烯複合蠟GraphShield 730 及消光粉 PropylMatte 系列。",
            "具備顯著改善擠出流動性（Improved Extrusion Flow）、高效脫氣消泡（Anti-Gassing）與優異抗結塊性能。",
            "固化過程中在塗膜表面形成均勻細緻的細砂紋/橘紋結構，大幅改善塗層邊角覆蓋率（Edge coverage）與抗劃傷耐磨性能。"
          ],
          "applications": [
            "熱固性粉末塗料（聚酯/TGIC",
            "聚酯/HAA",
            "環氧/聚酯混合型）",
            "織紋粉末塗層",
            "金屬傢俱與戶外型材塗裝。"
          ]
        },
        {
          "docId": "WAX-APPL-09",
          "filename": "Application Note MPI SelectorGuide Printing Inks EN 2026.pdf",
          "pdfPath": "techdatadb/5. MPI/3.Application Note MPI  wax/Application Note MPI SelectorGuide Printing Inks EN 2026.pdf",
          "docType": "Application Note 應用技術手冊",
          "lang": "EN (英文)",
          "version": "2026",
          "brand": "Micro Powders",
          "shortLabel": "印刷油墨抗耐磨",
          "title": "MPI Selector Guide for Printing Inks",
          "titleEn": "Application Note MPI SelectorGuide Printing Inks EN 2026.pdf",
          "origin": "Selector Guide - Printing Inks (Micro Powders, Inc. 2026)",
          "desc": "針對各類印刷油墨體系（膠印、凹版、柔版、能量固化與水性墨），提供耐摩擦（Rub resistance）、滑爽度與光澤控制的選型指導。",
          "advantages": [
            "涵蓋聚乙烯蠟（MPP-230F、MPP-611AL、MPP-620VF）、合成蠟（MP-22XF、MP-28AL）及陶瓷複合高滑爽蠟（PolyGlide 1226XF、SuperGlide 1231）。",
            "矩陣明確評比耐擦傷與耐摩擦（Rub & Scratch Resistance）、滑爽潤滑性、抗結塊（Block Resistance）與膠帶脫模性（Tape Release）。",
            "平均粒徑介於 3.5–15 µm（最大粒徑 ≤ 31 µm），廣泛適用於水性（W）、溶劑型（S）與油性（O）各類油墨與罩光清漆（OPV）。"
          ],
          "applications": [
            "溶劑型包裝凹版油墨",
            "平版輪轉膠印油墨",
            "水性柔版紙箱油墨",
            "金屬裝飾印刷油墨。"
          ]
        },
        {
          "docId": "WAX-APPL-10",
          "filename": "Application Note MPI SelectorGuide WoodCoatings EN 2026.pdf",
          "pdfPath": "techdatadb/5. MPI/3.Application Note MPI  wax/Application Note MPI SelectorGuide WoodCoatings EN 2026.pdf",
          "docType": "Application Note 應用技術手冊",
          "lang": "EN (英文)",
          "version": "2026",
          "brand": "Micro Powders",
          "shortLabel": "木器傢俱塗料",
          "title": "MPI Selector Guide for Wood Coatings",
          "titleEn": "Application Note MPI SelectorGuide WoodCoatings EN 2026.pdf",
          "origin": "Selector Guide - Wood Coatings (Micro Powders, Inc. 2026)",
          "desc": "介紹木器家具漆、地板漆（硝基漆 NC、聚胺酯 PU、UV 木器漆、水性木器漆）中專用的微粉蠟消光與表面防刮改質方案。",
          "advantages": [
            "推薦 PropylMatte 系列、MicroMatte 1213UVW / 1415-EZ、MicroTouch 系列、生質蠟 NatureMatte 系列及 Superslip 系列。",
            "在提供高效消光與光澤控制的同時，保持極佳漆膜清透度（Clarity）並賦予滑爽手感（Smooth Feel）。",
            "顯著強化耐刮傷耐擦傷（Scratch & Mar）、抗拋光磨損（Burnish Resistance）、撥水防潮以及優異的砂光打磨效率（Sanding Efficiency）。"
          ],
          "applications": [
            "高檔實木家具漆",
            "拼花木地板耐磨塗層",
            "水性木器底漆與面漆",
            "UV 固化櫥櫃板材塗裝。"
          ]
        },
        {
          "docId": "WAX-APPL-11",
          "filename": "Application Note MPI Wax SelectorGuide Architectural Coatings EN 2026.pdf",
          "pdfPath": "techdatadb/5. MPI/3.Application Note MPI  wax/Application Note MPI Wax SelectorGuide Architectural Coatings EN 2026.pdf",
          "docType": "Application Note 應用技術手冊",
          "lang": "EN (英文)",
          "version": "2026",
          "brand": "Micro Powders",
          "shortLabel": "建築裝飾塗料",
          "title": "MPI Wax Selector Guide for Architectural Coatings",
          "titleEn": "Application Note MPI Wax SelectorGuide Architectural Coatings EN 2026.pdf",
          "origin": "Selector Guide - Architectural Coatings (Micro Powders, Inc., R-03/26)",
          "desc": "針對現代室內與室外建築塗料體系，彙整高密度微粉蠟、合成蠟、氧化蠟、天然生質微粉與複合陶瓷助劑之選型指引與性能評級矩陣。",
          "advantages": [
            "涵蓋聚乙烯、改質聚丙烯、天然米糠蠟、PHBV、纖維素、脂肪族聚胺酯及壓克力微球等多元化學體系，建議添加量介於 0.5% 至 10.0%。",
            "針對光澤控制（Matting）、抗磨光（Burnish Resistance）、抗沾污（Resistance to Dirt Pick Up）、易潔性（Cleanability）及耐刮擦（Scratch & Mar）提供極優（Extremely Effective）至有效之多維度評級。",
            "提供高密度改質規格（如 AquaMatte 26HD、PropylMatte 31HD，密度 1.07–1.08 g/cc）以大幅強化水性體系之罐內穩定性（In-Can Stability），防止微粉漂浮分層。"
          ],
          "applications": [
            "室內外建築塗料",
            "水性與溶劑型塗裝系統",
            "抗磨光平光漆",
            "外牆防沾污易潔塗層",
            "抗刮飾面漆",
            "質感紋理與防滑裝飾塗料。"
          ]
        }
      ],
      "single": [
        {
          "docId": "WAX-SING-01",
          "filename": "TI MPI PolyGlide 1226XF Performance Study EN 202407.pdf",
          "pdfPath": "techdatadb/5. MPI/4.MPI  wax 單一產品/TI MPI Polyglide 1226 XF/TI MPI PolyGlide 1226XF Performance Study EN 202407.pdf",
          "docType": "I 單一產品技術資料",
          "lang": "EN (英文)",
          "version": "202407",
          "brand": "Micro Powders",
          "shortLabel": "PolyGlide 1226XF",
          "title": "PolyGlide 1226XF Product Performance Study",
          "titleEn": "TI MPI PolyGlide 1226XF Performance Study EN 202407.pdf",
          "origin": "Product Performance Study - PolyGlide 1226XF (Micro Powders, Inc. 2024)",
          "desc": "評估高分子無氟改質微粉蠟 PolyGlide 1226XF 在水性烤漆與卷鋼塗料中作為 PTFE 替代品之動摩擦係數（COF）與耐磨表現。",
          "advantages": [
            "HDPE/雙陶瓷奈米複合微粉蠟，熔點 109–115°C，密度 0.99 g/cm³，平均粒徑 3.5–5.5 µm，最大粒徑 15.56 µm，為無氟替代Polyfluo 150/900 之首選。",
            "於硬質水性聚胺酯塗料中添加 2% 時，動摩擦係數（COF）由無蠟原漆之 1.663 驟降至 0.297，具備媲美 PTFE 複合蠟 Polyfluo 150（0.243）之優異滑爽潤滑性。",
            "ASTM D4060 Taber 耐磨測試（添加 1%，2500 轉）重量損失僅 27.0 mg（原漆 42.3 mg），耐磨耗性分別比純聚乙烯蠟 MPP-611XF提升 21%、比 PTFE 複合蠟 Polyfluo 150 提升 22%。"
          ],
          "applications": [
            "水性卷鋼塗料",
            "罐頭金屬塗層",
            "工業五金烘烤漆",
            "包裝印刷罩光清漆。"
          ],
          "productGroup": "PolyGlide 超滑無氟系列"
        },
        {
          "docId": "WAX-SING-02",
          "filename": "TI MPI PropylMatte 31 HD and AquaMatte Matting Efficiency Study EN.pdf",
          "pdfPath": "techdatadb/5. MPI/4.MPI  wax 單一產品/TI MPI PropylMatte 31 HD/TI MPI PropylMatte 31 HD and AquaMatte Matting Efficiency Study EN.pdf",
          "docType": "I 單一產品技術資料",
          "lang": "EN (英文)",
          "version": "原廠發行版",
          "brand": "Micro Powders",
          "shortLabel": "PropylMatte 31 HD",
          "title": "PropylMatte 31 HD and AquaMatte Matting Efficiency Study",
          "titleEn": "TI MPI PropylMatte 31 HD and AquaMatte Matting Efficiency Study EN.pdf",
          "origin": "Product Performance Study - PropylMatte 31 HD & AquaMatte 26HD (Micro Powders, Inc.)",
          "desc": "比較高密度改質聚丙烯微粉 PropylMatte 31 HD 與高密度微粉化氧化聚乙烯蠟 AquaMatte 26HD在水性體系中之消光效率、防分層浮移特性與動摩擦係數（COF）。",
          "advantages": [
            "PropylMatte 31HD（熔點 160–170°C）與 AquaMatte 26HD 密度均經改質提升至 1.07 g/cm³（大於水），能徹底消除微粉蠟在水性與UV/EB 系統中之浮移分層問題。",
            "添加 2% 聚合物蠟可達緞面半光效果（60° 光澤 45–50 GU），添加 5% 可達到均勻消光效果（60° 光澤 20–25 GU），其中PropylMatte 31HD 在 20°/60°/85° 所有角度下均展現最高消光效率。",
            "動摩擦係數對比：AquaMatte 26HD 展現極低動態 COF（0.031，極高滑爽度），而 PropylMatte 31HD 則具備較高動態COF（0.242），提供聚丙烯特有的防滑手感。"
          ],
          "applications": [
            "水性木器家具面漆",
            "室內裝飾清漆",
            "水性塑膠漆",
            "透明金屬防護塗層。"
          ],
          "productGroup": "PropylMatte / AquaMatte 啞光系列"
        },
        {
          "docId": "WAX-SING-03",
          "filename": "TI MPI MicroKlear KL-418AL Performance Study EN.pdf",
          "pdfPath": "techdatadb/5. MPI/4.MPI  wax 單一產品/TI MPI_MicroKlear 418 AL/TI MPI MicroKlear KL-418AL Performance Study EN.pdf",
          "docType": "I 單一產品技術資料",
          "lang": "EN (英文)",
          "version": "原廠發行版",
          "brand": "Micro Powders",
          "shortLabel": "MicroKlear 418AL",
          "title": "MicroKlear 418AL Product Performance Study",
          "titleEn": "TI MPI MicroKlear KL-418AL Performance Study EN.pdf",
          "origin": "Product Performance Study - MicroKlear 418AL (Micro Powders, Inc.)",
          "desc": "測試天然巴西棕櫚蠟（Carnauba wax）與氧化鋁（Alumina）奈米複合物 MicroKlear 418AL 在高透光清漆與罐頭塗料中的抗刮耐磨特性。",
          "advantages": [
            "天然巴西棕櫚蠟基質複合 300 nm 氧化鋁奈米微粒（莫氏硬度 9），熔點 81–86°C，密度 1.04 g/cm³，平均粒徑 6.0–8.0µm（最大粒徑 22.0 µm）。",
            "ASTM D3363 鉛筆刮痕測試中，添加 1% MKL-418AL 使軟質聚胺酯塗層硬度由 8B 躍升至 HB（比無蠟原漆大幅跨越提升 8個硬度等級，比純巴西棕櫚蠟提升 4 級）。",
            "巴西棕櫚蠟提供優異表面光澤保留度與滑爽手感，符合 FDA 食品接觸規範，且完全不損害深色漆面之高透明度。"
          ],
          "applications": [
            "罐頭金屬外裝塗料",
            "汽車修補清漆",
            "高級木器光澤漆",
            "熱封食品包裝塗層。"
          ],
          "productGroup": "MicroKlear 棕櫚蠟複合系列"
        },
        {
          "docId": "WAX-SING-04",
          "filename": "TI MPI MicroMatte 1415-EZ Performance Study EN 2024.pdf",
          "pdfPath": "techdatadb/5. MPI/4.MPI  wax 單一產品/TI MPI_Micromatte 1415 EZ/TI MPI MicroMatte 1415-EZ Performance Study EN 2024.pdf",
          "docType": "I 單一產品技術資料",
          "lang": "EN (英文)",
          "version": "2024",
          "brand": "Micro Powders",
          "shortLabel": "MicroMatte 1415-EZ",
          "title": "MicroMatte 1415-EZ Product Performance Study",
          "titleEn": "TI MPI MicroMatte 1415-EZ Performance Study EN 2024.pdf",
          "origin": "Product Performance Study - MicroMatte 1415-EZ (Micro Powders, Inc. 2024, 7 pages)",
          "desc": "深度評估易分散型改質微粉蠟 MicroMatte 1415-EZ 在消光效率、摩擦係數、Taber 耐磨、抗拋光光澤上升（Burnish resistance）及耐污防沾（Soil release）之綜合性能。",
          "advantages": [
            "改質合成蠟易分散微粉，熔點 136–140°C，密度 1.06 g/cm³，平均粒徑 10.0–15.0 µm（最大粒徑 44.0 µm），具備優越的潤濕與易分散特性（EZ disperse）。",
            "具備卓越抗拋光性能：ASTM D6736 經 400 次擦洗後，85° 光澤變化量僅 3.29 GU（高居所有 MPI 產品之冠）；動摩擦係數低至",
            "167（媲美純 PTFE Fluo 300 之 0.164）。",
            "展現優異抗髒污防沾性能（Soil release），耐污測試色差 ΔE 僅 2.8（顯著優於對照組的 22.1），Taber 磨耗減重僅 22.9 mg（2500 轉）。"
          ],
          "applications": [
            "高級建築室內乳膠漆",
            "水性工業金屬漆",
            "木器家具面漆",
            "耐磨消光地坪塗料。"
          ],
          "productGroup": "MicroMatte 易分散消光系列"
        },
        {
          "docId": "WAX-SING-05",
          "filename": "TI MPI MP 22 MP 620F MP 635F Printing Ink Rub Resistance Study EN 202208.pdf",
          "pdfPath": "techdatadb/5. MPI/4.MPI  wax 單一產品/TI MPI_MP 22 VF/TI MPI MP 22 MP 620F MP 635F Printing Ink Rub Resistance Study EN 202208.pdf",
          "docType": "I 單一產品技術資料",
          "lang": "EN (英文)",
          "version": "202208",
          "brand": "Micro Powders",
          "shortLabel": "MP-22 VF 油墨耐磨",
          "title": "Comparison of Printing Ink Rub Resistance Using Synthetic and Polyethylene Waxes (MP-22 VF Focus)",
          "titleEn": "TI MPI MP 22 MP 620F MP 635F Printing Ink Rub Resistance Study EN 202208.pdf",
          "origin": "Application Study 1402 - Printing Ink Rub Resistance Study (Micro Powders, Inc.)",
          "desc": "評估在水性黑色壓克力印刷油墨中添加 1% 不同分子量聚乙烯蠟（MPP-620F、MPP-635F、MPP-230VF）與費托合成蠟（MP-22）的Sutherland 耐摩擦磨耗測試對比。",
          "advantages": [
            "測試添加劑平均粒徑均控制在 7–10 µm（最大粒徑 ≤ 31 µm），墨膜塗佈於 Leneta 卡紙上經 Sutherland 摩擦儀進行 50 次與200 次（4 磅重錘）摩擦試驗。",
            "50 次與 200 次摩擦評級結果（1 最佳，5 最差）：MPP-620F 綜合表現最優（評級 1，墨轉移最少），MPP-635F 次之（評級2），MPP-230VF 居第三（評級 3），MP-22 居第四（評級 4），未添加蠟的空白對照組最差（評級 5）。",
            "中等分子量高硬度聚乙烯蠟（MPP-620F）提供最佳耐擦傷保護；費托合成蠟（MP-22）則主要提供滑爽性與抗黏連，對耐強摩擦之抗性略遜於高分子量聚乙烯。"
          ],
          "applications": [
            "水性印刷油墨",
            "凹版與柔版包裝印刷墨",
            "耐摩擦罩光油（OPV）",
            "紙盒印刷面漆。"
          ],
          "productGroup": "MP-22 合成費托微粉系列"
        },
        {
          "docId": "WAX-SING-06",
          "filename": "TI MPI MP 22 MP 620F MP 635F Printing Ink Rub Resistance Study EN 202208.pdf",
          "pdfPath": "techdatadb/5. MPI/4.MPI  wax 單一產品/TI MPI_MP-22XF/TI MPI MP 22 MP 620F MP 635F Printing Ink Rub Resistance Study EN 202208.pdf",
          "docType": "I 單一產品技術資料",
          "lang": "EN (英文)",
          "version": "202208",
          "brand": "Micro Powders",
          "shortLabel": "MP-22XF 薄膜耐磨",
          "title": "MP-22XF and Polyethylene Waxes Rub Resistance Study",
          "titleEn": "TI MPI MP 22 MP 620F MP 635F Printing Ink Rub Resistance Study EN 202208.pdf",
          "origin": "Application Study 1402 - Printing Ink Rub Resistance Study (Micro Powders, Inc.)",
          "desc": "研究費托合成蠟超細規格 MP-22XF 與聚乙烯蠟在水性油墨薄膜中對耐磨耗、墨層轉移阻抗及表面滑性的效能對比。",
          "advantages": [
            "MP-22 微粉蠟基於合成費托蠟，熔點 102°C，密度 0.93 g/cm³，與各聚乙烯蠟受測樣品維持相近之平均粒徑分佈（7–10 µm）。",
            "雖然在高承載 Sutherland 耐磨測試中高分子量聚乙烯（MPP-620/635 系列）耐擦阻力更高，但 MP-22具備優越的薄膜滑爽手感、高光澤保留度與極低刮板細度。",
            "易於在低剪切條件下迅速混入油墨體系中，有效防止印張堆疊時的背面擦髒與黏頁（Anti-blocking）。"
          ],
          "applications": [
            "高速平版膠印油墨",
            "包裝柔版水性油墨",
            "凹版塑膠印刷油墨",
            "金屬印刷塗料。"
          ],
          "productGroup": "MP-22 合成費托微粉系列"
        },
        {
          "docId": "WAX-SING-07",
          "filename": "TI MPI MPP-611AL Performance Study EN 202407.pdf",
          "pdfPath": "techdatadb/5. MPI/4.MPI  wax 單一產品/TI MPI_MPP-611AL/TI MPI MPP-611AL Performance Study EN 202407.pdf",
          "docType": "I 單一產品技術資料",
          "lang": "EN (英文)",
          "version": "202407",
          "brand": "Micro Powders",
          "shortLabel": "MPP-611AL 氧化鋁耐磨",
          "title": "MPP-611AL Product Performance Study",
          "titleEn": "TI MPI MPP-611AL Performance Study EN 202407.pdf",
          "origin": "Product Performance Study - MPP-611AL (Micro Powders, Inc. 2024)",
          "desc": "評估高分子量聚乙烯蠟與奈米氧化鋁複合微粉 MPP-611AL 在工業塗料、罐頭塗層及無氟配方中的耐磨耗與抗劃痕硬化表現。",
          "advantages": [
            "HDPE 基質複合 300 nm 氧化鋁奈米微粒（莫氏硬度 9），熔點 110–116°C，密度 0.99 g/cm³，平均粒徑 3.5–5.5 µm（最大粒徑",
            "56 µm）。",
            "ASTM D3363 鉛筆刮痕測試（Taber 線性耐磨儀）中，添加 1% MPP-611AL 使軟質聚胺酯塗膜硬度由 8B 躍升至 B（大幅提升 7個等級，比未加氧化鋁之純 PE 蠟 MPP-611XF 提升 4 級）。",
            "以安全、易分散之非奈米微粉顆粒形態賦予塗層頂級抗刮擦效能，並具備優化密度以確保最大表面效率並消除奈米氧化鋁沉降問題。"
          ],
          "applications": [
            "工業金屬烘烤漆",
            "卷鋼塗料",
            "罐頭外壁保護漆",
            "木器耐磨地板面漆",
            "重防腐工業設備塗料。"
          ],
          "productGroup": "MPP 聚乙烯氧化鋁複合系列"
        },
        {
          "docId": "WAX-SING-08",
          "filename": "TI MPI MP 22 MP 620F MP 635F Printing Ink Rub Resistance Study EN 202208.pdf",
          "pdfPath": "techdatadb/5. MPI/4.MPI  wax 單一產品/TI MPI_MPP-620F/TI MPI MP 22 MP 620F MP 635F Printing Ink Rub Resistance Study EN 202208.pdf",
          "docType": "I 單一產品技術資料",
          "lang": "EN (英文)",
          "version": "202208",
          "brand": "Micro Powders",
          "shortLabel": "MPP-620F 油墨耐磨",
          "title": "MPP-620F Printing Ink Rub Resistance Study",
          "titleEn": "TI MPI MP 22 MP 620F MP 635F Printing Ink Rub Resistance Study EN 202208.pdf",
          "origin": "Application Study 1402 - Printing Ink Rub Resistance Study (Micro Powders, Inc.)",
          "desc": "聚焦 MPP-620F 中等分子量特製聚乙烯微粉蠟在印刷油墨中展現全場最優耐擦抗性的性能測試與機理解析。",
          "advantages": [
            "MPP-620F 熔點約 114–118°C，密度 0.94 g/cc，平均粒徑 7.0–9.0 µm，最大粒徑 31.0 µm。",
            "在水性黑色壓克力印刷油墨的 Sutherland 耐磨測試中，於 50 次與 200 次磨耗下墨轉移量均評定為全組最佳之第 1 名。",
            "特製聚乙烯結晶度與分子量分佈賦予墨膜表面極高的韌性與耐剪切性，杜絕包裝紙盒在運輸振動過程中的掉色與刮損。"
          ],
          "applications": [
            "水性包裝瓦楞紙油墨",
            "溶劑型塑膠凹印油墨",
            "書刊平版膠印油墨",
            "各類印刷罩光油。"
          ],
          "productGroup": "MPP 高耐磨聚乙烯系列"
        },
        {
          "docId": "WAX-SING-09",
          "filename": "TI MPI MP 22 MP 620F MP 635F Printing Ink Rub Resistance Study EN 202208.pdf",
          "pdfPath": "techdatadb/5. MPI/4.MPI  wax 單一產品/TI MPI_MPP-620XF/TI MPI MP 22 MP 620F MP 635F Printing Ink Rub Resistance Study EN 202208.pdf",
          "docType": "I 單一產品技術資料",
          "lang": "EN (英文)",
          "version": "202208",
          "brand": "Micro Powders",
          "shortLabel": "MPP-620XF 超細耐磨",
          "title": "MPP-620XF Printing Ink Rub Resistance and Thin-Film Performance Study",
          "titleEn": "TI MPI MP 22 MP 620F MP 635F Printing Ink Rub Resistance Study EN 202208.pdf",
          "origin": "Application Study 1402 - Printing Ink Rub Resistance Study (Micro Powders, Inc.)",
          "desc": "探討 MPP-620 的超細規格 MPP-620XF 在超薄印刷墨層與精密印刷中的耐磨擦、高透明度與表面滑爽表現。",
          "advantages": [
            "MPP-620 體系微粉蠟熔點 116°C（120–124°C），密度 0.96 g/cm³，以獨特聚乙烯結晶度與分子量分佈專注於極限耐磨擦改質。",
            "專為薄膜印刷（乾膜厚度 < 5 µm）設計，微粒完全包埋於墨層中且迅速浮於表面，消除大顆粒微粉引發的印刷光澤失真或版輥刮傷。",
            "證實 MPP-620 體系在水性墨中添加 1% 即達到 Sutherland 耐磨測試第 1 名（評級 1，墨轉移最少），提供頂級之耐磨耗、抗黏連與耐刮痕保護。"
          ],
          "applications": [
            "精密軟包裝印刷油墨",
            "金屬罐薄層印刷油墨",
            "高光澤印刷罩光清漆（OPV）",
            "UV 光固化印刷墨。"
          ],
          "productGroup": "MPP 高耐磨聚乙烯系列"
        },
        {
          "docId": "WAX-SING-10",
          "filename": "TI MPI MP 22 MP 620F MP 635F Printing Ink Rub Resistance Study EN 202208.pdf",
          "pdfPath": "techdatadb/5. MPI/4.MPI  wax 單一產品/TI MPI_MPP-635VF/TI MPI MP 22 MP 620F MP 635F Printing Ink Rub Resistance Study EN 202208.pdf",
          "docType": "I 單一產品技術資料",
          "lang": "EN (英文)",
          "version": "202208",
          "brand": "Micro Powders",
          "shortLabel": "MPP-635VF 高分子量耐磨",
          "title": "MPP-635VF Higher Molecular Weight Polyethylene Wax Rub Resistance Study",
          "titleEn": "TI MPI MP 22 MP 620F MP 635F Printing Ink Rub Resistance Study EN 202208.pdf",
          "origin": "Application Study 1402 - Printing Ink Rub Resistance Study (Micro Powders, Inc.)",
          "desc": "評估高分子量高硬度聚乙烯微粉蠟 MPP-635VF 在印刷油墨中抵抗重度磨損與高剪切刮擦的性能測試。",
          "advantages": [
            "採用更高分子量聚乙烯（Higher Molecular Weight HDPE），熔點 123–125°C，密度 0.97 g/cm³，具備極高結晶硬度與熱穩定性。",
            "在 Sutherland 耐磨擦試驗中排名第 2（優於低分子量 PE 蠟及合成蠟），耐高壓摩擦性能卓越。",
            "具備更高的熔點與熱穩定性，適用於需要高溫烘乾或高摩擦熱環境之印刷製程，且抗結塊性極強。"
          ],
          "applications": [
            "溶劑型與水性包裝油墨",
            "高耐磨工業塗層",
            "紙箱柔版油墨",
            "金屬裝飾烘烤印刷。"
          ],
          "productGroup": "MPP 高耐磨聚乙烯系列"
        },
        {
          "docId": "WAX-SING-11",
          "filename": "TI MPI PolyTuf 1229 Performance Study EN.pdf",
          "pdfPath": "techdatadb/5. MPI/4.MPI  wax 單一產品/TI MPI_PolyTuf 1229/TI MPI PolyTuf 1229 Performance Study EN.pdf",
          "docType": "I 單一產品技術資料",
          "lang": "EN (英文)",
          "version": "原廠發行版",
          "brand": "Micro Powders",
          "shortLabel": "PolyTuf 1229 耐磨衝擊",
          "title": "PolyTuf 1229 Product Performance Study",
          "titleEn": "TI MPI PolyTuf 1229 Performance Study EN.pdf",
          "origin": "Product Performance Study - PolyTuf 1229 (Micro Powders, Inc.)",
          "desc": "測試高分子量抗衝擊微粉聚合物 PolyTuf 1229 在耐磨地坪塗料與重防腐塗層中提升 Taber 耐磨損與抗劃痕衝擊之表現。",
          "advantages": [
            "LDPE 基質複合雙陶瓷奈米微粒，熔點 110–113°C，密度 0.97 g/cm³，平均粒徑 9.0–12.0 µm（最大粒徑 31.11 µm），為無氟替代Polyfluo 190/900 之旗艦產品。",
            "ASTM D4060 Taber 耐磨耗測試（添加 1%，2500 轉）重量損失僅 22.30 mg（原漆 42.30 mg），耐磨耗性高居 MPI 所有細微粉產品之冠，比含PTFE 陶瓷複合蠟 Polyfluo 900 再改善 10.8%。",
            "ASTM D3363 鉛筆刮痕測試中，塗膜硬度由 6B 躍升至 B 級，展現媲美 Polyfluo 190 之優異耐刮傷保護能力。"
          ],
          "applications": [
            "工業重載環氧地坪",
            "聚胺酯防滑地坪塗層",
            "耐磨工業設備漆",
            "船舶甲板塗料。"
          ],
          "productGroup": "PolyTuf 抗衝擊高韌性系列"
        },
        {
          "docId": "WAX-SING-12",
          "filename": "TI MPI AquaMatte and PropylMatte Matting Efficiency Study EN.pdf",
          "pdfPath": "techdatadb/5. MPI/4.MPI  wax 單一產品/TI MPI_PropylMatte 31/TI MPI AquaMatte and PropylMatte Matting Efficiency Study EN.pdf",
          "docType": "I 單一產品技術資料",
          "lang": "EN (英文)",
          "version": "原廠發行版",
          "brand": "Micro Powders",
          "shortLabel": "AquaMatte 水性消光",
          "title": "AquaMatte and PropylMatte Matting Efficiency Study",
          "titleEn": "TI MPI AquaMatte and PropylMatte Matting Efficiency Study EN.pdf",
          "origin": "Product Performance Study - AquaMatte & PropylMatte Matting Efficiency (Micro Powders, Inc.)",
          "desc": "深入研究聚丙烯微粉 PropylMatte 31HD 與微粉化氧化聚乙烯蠟 AquaMatte 系列在水性塗料中的消光曲線、防分層特性與動摩擦係數（COF）。",
          "advantages": [
            "PropylMatte 31HD（熔點 160–170°C）與 AquaMatte 26HD 密度均經重質化改質提升至 1.07 g/cm³（大於水），徹底消除微粉蠟在水性與UV/EB 系統中之浮移分層。",
            "添加 2% 聚合物蠟可達緞面半光（60° 光澤 45–50 GU），添加 5% 達消光效果（60° 光澤 20–25 GU），其中 PropylMatte 31HD 在20°/60°/85° 全角度消光效率均居首位。",
            "動態摩擦係數（COF）對比：AquaMatte 26HD 展現極低動態 COF（0.031，極高滑爽度），而 PropylMatte 31HD 具備較高動態COF（0.242），提供聚丙烯特有之防滑特性。"
          ],
          "applications": [
            "木器家具塗料",
            "皮革頂層塗飾",
            "塑膠消光漆",
            "自平地坪塗層。"
          ],
          "productGroup": "PropylMatte / AquaMatte 啞光系列"
        },
        {
          "docId": "WAX-SING-13",
          "filename": "TI MPI Superslip 6515AL Superslip 6515AL-EZ Performance Study EN 202412.pdf",
          "pdfPath": "techdatadb/5. MPI/4.MPI  wax 單一產品/TI MPI_Superslip 6515 AL/TI MPI Superslip 6515AL Superslip 6515AL-EZ Performance Study EN 202412.pdf",
          "docType": "I 單一產品技術資料",
          "lang": "EN (英文)",
          "version": "202412",
          "brand": "Micro Powders",
          "shortLabel": "Superslip 6515AL 超滑爽",
          "title": "Superslip 6515AL and Superslip 6515AL-EZ Product Performance Study",
          "titleEn": "TI MPI Superslip 6515AL Superslip 6515AL-EZ Performance Study EN 202412.pdf",
          "origin": "Product Performance Study - Superslip 6515AL & Superslip 6515AL-EZ (Micro Powders, Inc. 2024)",
          "desc": "評估無氟高滑爽耐磨複合微粉蠟 Superslip 6515AL 與易分散型 6515AL-EZ 在水性工業烤漆與罐頭塗料中替代含 PTFE添加劑的優異表現。",
          "advantages": [
            "HDPE / 醯胺蠟 / 奈米氧化鋁複合微粉，熔點 139–145°C，密度 0.99 g/cm³，平均粒徑 3.50–5.50 µm（最大粒徑 15.56 µm）；EZ版本經表面改質，在水性體系中極易潤濕分散。",
            "ASTM D1894 動摩擦係數（COF）在硬質聚胺酯添加 2% 下達到 0.280（原漆 1.663），滑爽潤滑性完全媲美 PTFE 複合蠟Polyfluo 150（0.243）。",
            "耐刮擦與耐磨損卓越：添加 1% 使鉛筆刮痕硬度由 6B 躍升至 B 級（優於 Superslip 6515 之 3B）；Taber 耐磨損（2500 轉）減重僅",
            "9 mg，耐磨性比 Polyfluo 150（34.4 mg）再提升 10%。"
          ],
          "applications": [
            "罐頭與金屬容器塗料",
            "卷鋼工業塗層",
            "五金工具烤漆",
            "無氟耐磨工業漆。"
          ],
          "productGroup": "Superslip 超滑爽耐磨系列"
        },
        {
          "docId": "WAX-SING-14",
          "filename": "TI MPI Polyfluo 190 and Fluo 300 Abrasion Resistance Study EN.pdf",
          "pdfPath": "techdatadb/5. MPI/4.MPI  wax 單一產品/TI_MPI Fluo 300XF/TI MPI Polyfluo 190 and Fluo 300 Abrasion Resistance Study EN.pdf",
          "docType": "I 單一產品技術資料",
          "lang": "EN (英文)",
          "version": "原廠發行版",
          "brand": "Micro Powders",
          "shortLabel": "Polyfluo 190 / Fluo 300",
          "title": "Polyfluo 190 and Fluo 300 Abrasion Resistance Study",
          "titleEn": "TI MPI Polyfluo 190 and Fluo 300 Abrasion Resistance Study EN.pdf",
          "origin": "Product Performance Study - Polyfluo 190 and Fluo 300 Abrasion Resistance (Micro Powders, Inc.)",
          "desc": "比較高密度聚乙烯/PTFE 複合微粉 Polyfluo 190 與 100% 純微粉 PTFE（Fluo 300）在工業塗料中對 Taber耐磨耗減重之性能與成本效益對比。",
          "advantages": [
            "Polyfluo 190 為微粉 PTFE 改質聚乙烯複合蠟（熔點 121–132°C，密度 0.99 g/cm³，平均粒徑 9.0–12.0 µm）；Fluo 300 為100% 純微粉 PTFE（熔點 >316°C，密度 2.20 g/cm³，平均粒徑 5.0–6.0 µm）。",
            "Taber 耐磨測試數據：未加蠟空白組磨耗減重 14.3 mg；添加 0.5% Polyfluo 190 減重降至 10.8 mg；添加 1.0% Polyfluo 190 減重僅 7.8 mg，其耐磨減重改善效果顯著優於 1.0% Fluo 300（8.9 mg）。",
            "最佳建議添加量約為 1.0%，Polyfluo 190 不僅耐磨耗性能超越純 PTFE 微粉，且因密度較低與聚乙烯複合特性，原料成本大幅降低。"
          ],
          "applications": [
            "工業金屬塗漆",
            "卷鋼塗料",
            "罐頭塗層",
            "熱固性粉末塗料",
            "重防腐耐磨面漆。"
          ],
          "productGroup": "Polyfluo / Fluo 微粉系列"
        },
        {
          "docId": "WAX-SING-15",
          "filename": "TI MPI MicroTex 950 Performance Study EN 202504.pdf",
          "pdfPath": "techdatadb/5. MPI/4.MPI  wax 單一產品/TI_MPI Microtex 950/TI MPI MicroTex 950 Performance Study EN 202504.pdf",
          "docType": "I 單一產品技術資料",
          "lang": "EN (英文)",
          "version": "202504",
          "brand": "Micro Powders",
          "shortLabel": "MicroTex 950 紋理防滑",
          "title": "MicroTex® 950 Product Performance Study",
          "titleEn": "TI MPI MicroTex 950 Performance Study EN 202504.pdf",
          "origin": "Product Performance Study - MicroTex® 950 (Micro Powders, Inc. 2025, 5 pages)",
          "desc": "評估無氟（PFAS-Free）改質聚烯烴織紋劑 MicroTex 950 在多種粉末塗料體系（Hybrid 環氧/聚酯、PE/TGIC、PE/HAA）中替代PTFE 織紋粉（如 Fluo 750TX）之消光、織紋形成與機械性能。",
          "advantages": [
            "改質聚烯烴材質，無氟環保，熔點 135–140°C，密度 1.22 g/cc（遠低於 PTFE 的 2.20 g/cc），最大粒徑 74 µm。",
            "建議添加量為 4.0–6.0 wt%，在 200°C 烘烤 15 分鐘條件下，60° 光澤在 Hybrid 降至 5.3–10.9 GU，PE/TGIC 降至 4.0–9.5 GU，PE/HAA 降至 2.3–7.1 GU，成功形成均勻細緻砂紋外觀。",
            "機械性能卓越：劃格密著性保持最佳 5B，正向/反向耐衝擊性達到 60–160 in-lb，錐軸彎曲（Mandrel Bend）100%通過，且熔融微粒流（Pellet Flow）穩定，提供優異邊角覆蓋保護。"
          ],
          "applications": [
            "無氟環保粉末塗料（聚酯/TGIC",
            "聚酯/HAA",
            "環氧/聚酯混合型）",
            "五金儀器砂紋塗裝",
            "戶外建材鋁門窗防護塗層",
            "金屬傢俱織紋烤漆。"
          ],
          "productGroup": "MicroTex 砂紋紋理助劑系列"
        }
      ],
      "formulation": [
        {
          "docId": "WAX-FORM-01",
          "filename": "Formulation Guide MPI MicroTouch EN.pdf",
          "pdfPath": "techdatadb/5. MPI/3.Application Note MPI  wax/Formulation Guide MPI MicroTouch EN.pdf",
          "docType": "Formulation 配方指南",
          "lang": "EN (英文)",
          "version": "原廠發行版",
          "brand": "Micro Powders",
          "shortLabel": "MicroTouch 觸感起始配方",
          "title": "MicroTouch Soft Touch Additives Formulation Guide",
          "titleEn": "Formulation Guide MPI MicroTouch EN.pdf",
          "origin": "MicroTouch Soft Touch Additives Formulation Guide (Micro Powders, Inc.)",
          "desc": "詳細公開MicroTouch（800F、800VF、800XF、850XF）搭配多種商用水性聚胺酯分散體（PUD）製造卵石感（Pebbly）、橡膠感（Rubbery）、絨毛感（Fuzzy）與玫瑰花瓣感（Rose Petal）之精確配方比重與混配工藝。",
          "advantages": [
            "具體配方比例：結合 Covestro Bayhydrol UH 340/1、Alberdingk U 2101/U 5201 及丁基卡必醇（1.2–1.7%），MicroTouch添加量精準規範為 11.5 wt%（濕膜厚度 76 µm）。",
            "混配工藝指引：先加入 PUD 與溶劑擴散至少 3 小時後再加入 MicroTouch 攪拌均勻；在醇類體系中不可直接打漿，需分散於樹脂液中；嚴禁使用DMF 溶劑以免微粒劇烈膨脹。",
            "光澤數據：於 76 µm 濕膜厚度下，850XF 配方使 20°/60°/85° 光澤由原漆 39.3/72.9/88.0 降至",
            "4/4.3/10.3（玫瑰花瓣觸感），消光與觸感改質同步實現。"
          ],
          "applications": [
            "水性觸感漆",
            "消費電子軟觸感塗料",
            "汽車內裝儀錶板塗裝",
            "高檔紙盒與包裝觸感塗佈。"
          ]
        }
      ]
    }
  },
  "adhesion": {
    "slug": "adhesion",
    "hasData": false,
    "tabs": {
      "principles": [],
      "catalog": [],
      "applications": [],
      "single": [],
      "formulation": []
    }
  },
  "polyester": {
    "slug": "polyester",
    "hasData": false,
    "tabs": {
      "principles": [],
      "catalog": [],
      "applications": [],
      "single": [],
      "formulation": []
    }
  },
  "chain": {
    "slug": "chain",
    "hasData": true,
    "tabs": {
      "principles": [],
      "catalog": [
        {
          "docId": "CHA-CATA-01",
          "filename": "Brochure DK Unilink Plus Coatings Line EN 202512.pdf",
          "pdfPath": "techdatadb/3.unilink/2.Unilink Clearlink擴鏈劑目錄/Brochure DK Unilink Plus Coatings Line EN 202512.pdf",
          "docType": "Brochure 總覽型錄",
          "lang": "EN (英文)",
          "version": "202512",
          "brand": "Dorf Ketal",
          "shortLabel": "Unilink & Clearlink 型錄",
          "title": "Clearlink® and Unilink® Chain Extenders Application Guide",
          "titleEn": "Brochure DK Unilink Plus Coatings Line EN 202512.pdf",
          "origin": "Clearlink® and Unilink® Chain Extenders Application Guide (Dorf Ketal)",
          "desc": "介紹 Dorf Ketal 旗下 Unilink 4200 系列（芳香族二級二胺）、Clearlink 1000/1100 系列（脂肪族二級二胺）、Unilink 1080/1136/2130/2200/2500 系列多元醇/胺預聚物擴鏈劑，以及 Unilink 1030 鋯觸媒，在聚脲、聚胺酯彈性塗層、自平地坪、彈性體及結構密封膠之全系列應用技術。",
          "advantages": [
            "二級胺（Secondary Diamine）受立體阻障效應調控，反應活性適度降低，能將聚脲噴塗膠凝時間由數秒延長至可控加工範圍（操作適用期延長至數分鐘），賦予優異流平性與基材潤濕。",
            "構建線性聚合物主鏈網絡，賦予塗膜優異拉伸強度、斷裂伸長率及耐衝擊韌性，並具備優良的配方相容性。",
            "Clearlink 1000/1100 具備卓越耐光性與抗黃變性；Unilink 4200 則提供極高性價比、高模數與極佳抗水解老化性能；Unilink 1030 可作為無汞環保催化劑替代有機汞。"
          ],
          "applications": [
            "噴塗聚脲（Truck Bed Liners",
            "屋頂防水",
            "儲槽內襯）",
            "聚胺酯自平地坪",
            "彈性塗料",
            "澆注型彈性體",
            "接著劑與密封膠。"
          ]
        }
      ],
      "applications": [],
      "single": [
        {
          "docId": "CHA-SING-01",
          "filename": "TI DK Clearlink 1000 for Polyurea Coatings EN 201707.pdf",
          "pdfPath": "techdatadb/3.unilink/4. Unilink Clearlink擴鏈劑單一產品應用技術資料/TI Clearlink 1000/TI DK Clearlink 1000 for Polyurea Coatings EN 201707.pdf",
          "docType": "I 單一產品技術資料",
          "lang": "EN (英文)",
          "version": "201707",
          "brand": "Dorf Ketal",
          "shortLabel": "Clearlink 1000 聚脲塗層",
          "title": "Clearlink® 1000 Aliphatic Diamine Chain Extender for Polyurea Coatings",
          "titleEn": "TI DK Clearlink 1000 for Polyurea Coatings EN 201707.pdf",
          "origin": "Clearlink® 1000 Aliphatic Amine for Polyurea Coatings Application Data Sheet (Dorf Ketal, SC0031)",
          "desc": "說明 Clearlink 1000 脂肪族受阻二級二胺在脂肪族與芳香族聚脲噴塗系統中作為擴鏈劑的物理化學規格與膠凝時間調控特性。",
          "advantages": [
            "液態透明無色外觀，分子量 322，當量重 161，黏度極低（25°C 下約 25–35 mPa·s），25°C 比重 0.89–0.90，閃火點（Pensky-Martens閉杯）最低 60.6°C（141°F）。",
            "顯著延長異氰酸酯預聚體與多胺反應之膠凝時間（Gel time），使噴塗施工時塗膜具備更佳的流動性、光澤平整度與無氣泡缺陷表面。",
            "賦予固化聚脲優異的耐紫外線（UV）耐候性、耐光黃變性及極高低溫耐衝擊韌性。"
          ],
          "applications": [
            "耐候型聚脲噴塗塗料",
            "貨車斗耐磨襯墊（Truck bed liners）",
            "戶外防腐耐候塗層",
            "聚脲地坪頂漆。"
          ],
          "productGroup": "Clearlink 耐候脂肪族系列"
        },
        {
          "docId": "CHA-SING-02",
          "filename": "TI DK Unilink 1030 Catalyst for Cast Elastomers EN.pdf",
          "pdfPath": "techdatadb/3.unilink/4. Unilink Clearlink擴鏈劑單一產品應用技術資料/TI Unilink 1030/TI DK Unilink 1030 Catalyst for Cast Elastomers EN.pdf",
          "docType": "I 單一產品技術資料",
          "lang": "EN (英文)",
          "version": "原廠發行版",
          "brand": "Dorf Ketal",
          "shortLabel": "Unilink 1030 澆注彈性體",
          "title": "Unilink® 1030 Catalyst for Cast Elastomers",
          "titleEn": "TI DK Unilink 1030 Catalyst for Cast Elastomers EN.pdf",
          "origin": "Unilink® 1030 Catalyst for Cast Elastomers Application Data Sheet (Dorf Ketal, SC0029)",
          "desc": "探討 Unilink 1030 專有鋯螯合物（溶解於反應性二醇溶劑中之無汞環保催化系統）在 TDI 及 MDI 澆注型聚胺酯彈性體（Cast Elastomers）製程中對活化期（Pot Life）與脫模時間之催化表現。",
          "advantages": [
            "具備獨特延遲催化反應特性，於注模初期黏度增長平緩，使膠料流動充模順暢、不易夾帶微氣泡。",
            "加熱硫化階段反應活性迅速飆升，大幅縮短膠凝後硬化脫模週期，顯著提高模具周轉率與生產效率。",
            "產出之彈性體製品具備優異回彈性、耐磨耗性、高抗撕裂強度與低壓縮永久變形率。"
          ],
          "applications": [
            "澆注型聚胺酯彈性體（CPU）",
            "工業膠輥",
            "實心輪胎",
            "採礦篩板",
            "高耐磨機械密封零件。"
          ],
          "productGroup": "Unilink 催化系統"
        },
        {
          "docId": "CHA-SING-03",
          "filename": "TI DK Unilink 4200 Chain Extender for Flexible Polyurethane Foams EN.pdf",
          "pdfPath": "techdatadb/3.unilink/4. Unilink Clearlink擴鏈劑單一產品應用技術資料/TI Unilink 4200/TI DK Unilink 4200 Chain Extender for Flexible Polyurethane Foams EN.pdf",
          "docType": "I 單一產品技術資料",
          "lang": "EN (英文)",
          "version": "原廠發行版",
          "brand": "Dorf Ketal",
          "shortLabel": "Unilink 4200 軟質泡棉",
          "title": "Unilink® 4200 Chain Extender for Flexible Polyurethane Foams",
          "titleEn": "TI DK Unilink 4200 Chain Extender for Flexible Polyurethane Foams EN.pdf",
          "origin": "Unilink® 4200 Aromatic Diamine - Chain Extender for Flexible Polyurethane Foams (Dorf Ketal, SC0027)",
          "desc": "研究 Unilink 4200 芳香族二級二胺在標準 TDI 塊狀泡棉、高回彈（HR）泡棉及冷模塑泡棉中對泡孔微觀結構與力學承載性能的改善。",
          "advantages": [
            "液態芳香族二胺，比重 0.98–0.99，當量重約 153，羥值（胺值當量）362，低毒性（Ames negative）且對水分不敏感。",
            "在高回彈泡棉配方中添加 1–5 php，可細化泡孔構造，減少發泡方向泡孔伸長率，顯著提高壓入硬度（IFD 25% 及65%）與支撐因子（Sag factor 自 2.5 提升至 2.9）。",
            "在降低泡棉密度（由 43 kg/m³ 降至 35 kg/m³）的同時，維持或提升抗張強度與撕裂強度（自 367 N/m 增至 507 N/m）。"
          ],
          "applications": [
            "塊狀高回彈軟質聚胺酯泡棉",
            "冷模塑汽車座椅座墊",
            "沙發家具軟墊",
            "聚酯型軟泡。"
          ],
          "productGroup": "Unilink 芳香族擴鏈劑系列"
        },
        {
          "docId": "CHA-SING-04",
          "filename": "TI DK Unilink 4200 for Chain Extender for Elastomeric Coatings EN.pdf",
          "pdfPath": "techdatadb/3.unilink/4. Unilink Clearlink擴鏈劑單一產品應用技術資料/TI Unilink 4200/TI DK Unilink 4200 for Chain Extender for Elastomeric Coatings EN.pdf",
          "docType": "I 單一產品技術資料",
          "lang": "EN (英文)",
          "version": "原廠發行版",
          "brand": "Dorf Ketal",
          "shortLabel": "Unilink 4200 彈性體塗層",
          "title": "Unilink® 4200 Chain Extender for Elastomeric Coatings",
          "titleEn": "TI DK Unilink 4200 for Chain Extender for Elastomeric Coatings EN.pdf",
          "origin": "Unilink® 4200 Aromatic Diamine - Chain Extender for Elastomeric Coatings (Dorf Ketal, SC0028)",
          "desc": "詳述 Unilink 4200 作為擴鏈劑在 TDI / MDI 彈性塗料與雙組分噴塗聚脲中調控膠凝時間、黏度與力學強度的應用數據。",
          "advantages": [
            "在聚脲噴塗配方中隨著 Unilink 4200 添加量由 3.3 php 提升至 60.8 php，膠凝時間由 2.3 秒平緩延長至 36.0 秒，不發黏時間由",
            "5 秒延長至 70.0 秒。",
            "低黏度液態特性能改善底材潤濕性與附著力，消弭快速噴塗產生的桔皮與針孔缺陷，形成平整鏡面外觀。",
            "室溫固化後塗膜展現優異抗張強度（>1700–2400 psi）、伸長率（135–155%）與邵氏 D 硬度（56–65 Shore D）。"
          ],
          "applications": [
            "雙組分彈性體噴塗塗料",
            "防腐與防水聚脲塗層",
            "自平彈性地坪",
            "管道防腐內襯。"
          ],
          "productGroup": "Unilink 芳香族擴鏈劑系列"
        }
      ],
      "formulation": []
    }
  },
  "matting": {
    "slug": "matting",
    "hasData": true,
    "tabs": {
      "principles": [
        {
          "docId": "MAT-PRIN-01",
          "filename": "技術手冊6 消光粉 2026.07.16 v4.docx",
          "pdfPath": "techdatadb/7.Matting Agent/1.原理/技術手冊6 消光粉 2026.07.16 v4.docx",
          "docType": "原理機制",
          "lang": "TW (繁體中文)",
          "version": "2026",
          "brand": "其他特化",
          "shortLabel": "消光原理",
          "title": "消光粉技術手冊：消光原理",
          "titleEn": "技術手冊6 消光粉 2026.07.16 v4.docx",
          "origin": "技術手冊6 消光粉 2024-07 (Brochure No. 6) - 消光粉的消光原理",
          "desc": "說明二氧化矽消光劑在漆膜成膜乾燥時的物理微觀機制，透過溶劑揮發與漆膜收縮使消光微粒均勻分佈並形成粗糙表面，促進入射光線散射以達到消光效果。",
          "advantages": [
            "在漆膜乾燥過程中，隨著溶劑的揮發，漆膜的收縮，消光粉會均勻分佈在整個漆膜當中，並形成了比較粗糙的表面。",
            "光線照射在漆膜表面，由於表面粗糙，造成了散射效應，使光澤低於100度，因而產生了消光效果。"
          ],
          "applications": [],
          "mechImg": "techdatadb/7.Matting Agent/1.原理/消光原理.png"
        },
        {
          "docId": "MAT-PRIN-02",
          "filename": "技術手冊6 消光粉 2026.07.16 v4.docx",
          "pdfPath": "techdatadb/7.Matting Agent/1.原理/技術手冊6 消光粉 2026.07.16 v4.docx",
          "docType": "原理機制",
          "lang": "TW (繁體中文)",
          "version": "2026",
          "brand": "其他特化",
          "shortLabel": "平均粒徑",
          "title": "消光粉技術手冊：平均粒徑",
          "titleEn": "技術手冊6 消光粉 2026.07.16 v4.docx",
          "origin": "技術手冊6 消光粉 2024-07 - 消光粉選擇重要技術指標：一、平均粒徑 (Average Particle Size)",
          "desc": "分析消光劑平均粒徑大小與粒徑分佈寬窄對塗料消光效率、黏度負擔、塗膜手感外觀及透明性之平衡控制技術準則。",
          "advantages": [
            "消光粉平均粒徑越大則消光效率越高，但粒徑過大會導致漆膜表面過度粗糙並破壞手感與外觀；粒徑太細則消光效率較低且會增加塗料黏度，一般塗料建議平均粒徑以4–8 µm 為佳。",
            "粒徑分佈越窄越好，過寬的粒徑分佈含有大量粗顆粒（造成過度粗糙）與細顆粒（造成體系增黏），需依乾膜厚薄匹配適當粒徑。",
            "在相同添加量前提下，消光粉平均粒徑越小則漆膜透明性越佳，但相應消光效率也會隨之降低。"
          ],
          "applications": [],
          "mechImg": "techdatadb/7.Matting Agent/1.原理/Average Particle Size.png"
        },
        {
          "docId": "MAT-PRIN-03",
          "filename": "技術手冊6 消光粉 2026.07.16 v4.docx",
          "pdfPath": "techdatadb/7.Matting Agent/1.原理/技術手冊6 消光粉 2026.07.16 v4.docx",
          "docType": "原理機制",
          "lang": "TW (繁體中文)",
          "version": "2026",
          "brand": "其他特化",
          "shortLabel": "表面處理",
          "title": "消光粉技術手冊：表面處理",
          "titleEn": "技術手冊6 消光粉 2026.07.16 v4.docx",
          "origin": "技術手冊6 消光粉 2024-07 - 消光粉選擇重要技術指標：二、表面處理",
          "desc": "消光粉經表面處理可改善分散性，避免沉澱，並提升木器塗料漆膜的透明性、手感與耐刮性。",
          "advantages": [
            "由於消光粉有無表面處理，會影響與基料的潤濕分散性，進而會影響到漆膜的透明性。",
            "一般木器塗料若使用未處理的消光粉，塗料中已有顏料，容易出現  沉澱現象。",
            "用有機物質處理(主要是高分子蠟)進行表面處理得到容易分散的消光粉，可使漆膜手感滑爽，耐刮性更好。"
          ],
          "applications": [],
          "mechImg": "techdatadb/7.Matting Agent/1.原理/表面處理.png"
        },
        {
          "docId": "MAT-PRIN-04",
          "filename": "技術手冊6 消光粉 2026.07.16 v4.docx",
          "pdfPath": "techdatadb/7.Matting Agent/1.原理/技術手冊6 消光粉 2026.07.16 v4.docx",
          "docType": "原理機制",
          "lang": "TW (繁體中文)",
          "version": "2026",
          "brand": "其他特化",
          "shortLabel": "孔隙率",
          "title": "消光粉技術手冊：孔隙率",
          "titleEn": "技術手冊6 消光粉 2026.07.16 v4.docx",
          "origin": "技術手冊6 消光粉 2024-07 - 消光粉選擇重要技術指標：三、孔隙率 (Pore Volume)",
          "desc": "高孔隙率消光粉在相同粒徑下能提供更佳消光效果，使漆膜光澤度降低。",
          "advantages": [
            "消光粉的孔隙率越高，因此消光性能就會越好。",
            "光澤度的降低是消光粉粒徑的效應，對於相同粒徑的消光粉來說，高孔隙率消光粉的消光效果更好。",
            "因為高孔隙率消光粉所含粒子微孔容積大，其消光性越好，即漆膜光澤越低。"
          ],
          "applications": [],
          "mechImg": "techdatadb/7.Matting Agent/1.原理/孔隙率.png"
        },
        {
          "docId": "MAT-PRIN-05",
          "filename": "技術手冊6 消光粉 2026.07.16 v4.docx",
          "pdfPath": "techdatadb/7.Matting Agent/1.原理/技術手冊6 消光粉 2026.07.16 v4.docx",
          "docType": "原理機制",
          "lang": "TW (繁體中文)",
          "version": "2026",
          "brand": "其他特化",
          "shortLabel": "膜厚",
          "title": "消光粉技術手冊：膜厚",
          "titleEn": "技術手冊6 消光粉 2026.07.16 v4.docx",
          "origin": "技術手冊6 消光粉 2024-07 - 消光粉選擇重要技術指標：四、膜厚 (Film Thickness)",
          "desc": "有無表面處理消光粉在相同孔隙率及粒徑前提下，相同消光粉添加量，膜厚越厚，消光度越差。",
          "advantages": [
            "在相同孔隙率及粒徑前提下，消光劑添加量相同時，塗膜膜厚越厚，消光度越差（即表面光澤越高）。",
            "無論消光粉是否有經有機化合物（如高分子蠟）表面處理，膜厚增加對消光度的負面影響規律均維持一致。",
            "配方設計需根據乾膜厚薄精確選擇不同粒徑之消光粉，以在目標膜厚下達到最佳消光效果。"
          ],
          "applications": [],
          "mechImg": "techdatadb/7.Matting Agent/1.原理/膜厚.png"
        },
        {
          "docId": "MAT-PRIN-06",
          "filename": "技術手冊6 消光粉 2026.07.16 v4.docx",
          "pdfPath": "techdatadb/7.Matting Agent/1.原理/技術手冊6 消光粉 2026.07.16 v4.docx",
          "docType": "原理機制",
          "lang": "TW (繁體中文)",
          "version": "2026",
          "brand": "其他特化",
          "shortLabel": "樹脂系統",
          "title": "消光粉技術手冊：樹脂系統",
          "titleEn": "技術手冊6 消光粉 2026.07.16 v4.docx",
          "origin": "技術手冊6 消光粉 2024-07 - 五、樹脂系統 (The Resin System) 及 行業應用",
          "desc": "分析樹脂交聯機制、固成份、溶劑蒸發速率與乾燥方法對塗膜收縮消光之綜合影響，並彙總各樹脂塗料系統之建議消光劑添加量與高速分散工藝。",
          "advantages": [
            "消光粉之消光效果受樹脂系統（不同交聯機制）、固含量（揮發物溶劑比例）、溶劑類型（不同蒸發速度）及乾燥方法（快或慢）四大關鍵因素影響。",
            "各體系建議添加量（按總配方量）：硝化棉（NC）系統為 1.0%–5.0%；聚胺酯（PU）及烤漆系統為 2.0%–12.0%；UV 光固化系統為",
            "0%–12.0%；水性系統為 1.0%–12.0%（使用 TS 100 牌號用量可減少一半）；滑劑用途為 1.0%–5.0%。",
            "分散工藝規範：使用高速攪拌機分散（約 1500 轉/min，時間 15–20 分鐘，溫度嚴格控制在 50°C以下），一般選用表面經有機處理（高分子蠟處理）之消光粉更易分散且不易產生硬沉澱。"
          ],
          "applications": [
            "硝化棉（NC）塗料",
            "聚胺酯（PU）塗料",
            "金屬烤漆系統",
            "UV 光固化塗料",
            "水性塗料。"
          ],
          "mechImg": "techdatadb/7.Matting Agent/1.原理/膜厚.png"
        }
      ],
      "catalog": [],
      "applications": [],
      "single": [],
      "formulation": []
    }
  },
  "powder": {
    "slug": "powder",
    "hasData": false,
    "tabs": {
      "principles": [],
      "catalog": [],
      "applications": [],
      "single": [],
      "formulation": []
    }
  }
};
const TechState = {
  activeCategory: 'tyzor',
  activeSubTab: 'principles', // 'principles', 'catalog', 'applications', 'single'
  activeDocIndices: {
    'tyzor': { 'principles': 0, 'catalog': 0, 'applications': 0, 'single': 0 },
    'carbon-black': { 'principles': 0, 'catalog': 0, 'applications': 0, 'single': 0 },
    'wax': { 'principles': 0, 'catalog': 0, 'applications': 0, 'single': 0 },
    'chain': { 'principles': 0, 'catalog': 0, 'applications': 0, 'single': 0 },
    'matting': { 'principles': 0, 'catalog': 0, 'applications': 0, 'single': 0 }
  }
};

/**
 * 動態確保技術專區書籤分頁與樣式完整生效 (杜絕樣式缺失導致分頁破版)
 */
function ensureTechModuleStyles() {
  if (typeof document === 'undefined' || !document.head) return;
  if (document.getElementById('tech-module-styles')) return;
  const styleEl = document.createElement('style');
  styleEl.id = 'tech-module-styles';
  styleEl.textContent = `
    /* 瀏覽器書籤風格容器與標籤列 */
    .tech-bookmark-wrapper {
      width: 100%;
      margin-top: 0.5rem;
      position: relative;
    }
    .tech-subtab-strip {
      display: flex;
      align-items: flex-end;
      gap: 0.375rem;
      padding-left: 0.5rem;
      margin-bottom: -1px;
      position: relative;
      z-index: 10;
    }
    @media (max-width: 640px) {
      .tech-subtab-strip {
        overflow-x: auto;
        scrollbar-width: none;
        -webkit-overflow-scrolling: touch;
        padding-bottom: 1px;
      }
      .tech-subtab-strip::-webkit-scrollbar {
        display: none;
      }
    }
    .tech-subtab-btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 0.375rem;
      padding: 0.625rem 1.125rem 0.5rem 1.125rem;
      border-top-left-radius: 0.625rem !important;
      border-top-right-radius: 0.625rem !important;
      border-bottom-left-radius: 0 !important;
      border-bottom-right-radius: 0 !important;
      border: 1px solid #cbd5e1 !important;
      border-bottom: 1px solid #cbd5e1 !important;
      background: #f1f5f9 !important;
      color: #475569 !important;
      font-size: 0.8125rem;
      font-weight: 600;
      line-height: 1.2;
      white-space: nowrap;
      cursor: pointer;
      transition: background-color 0.15s ease, color 0.15s ease, border-color 0.15s ease;
      position: relative;
      z-index: 5;
      margin-bottom: 0;
    }
    .tech-subtab-btn:hover {
      background: #e2e8f0 !important;
      color: #0f172a !important;
    }
    .tech-subtab-btn.active {
      background: #ffffff !important;
      color: #1e3a8a !important;
      font-weight: 800 !important;
      border: 1px solid #cbd5e1 !important;
      border-top: 3px solid #1e3a8a !important;
      border-bottom: 2px solid #ffffff !important;
      margin-bottom: -1px !important;
      padding-bottom: calc(0.5rem + 2px) !important;
      position: relative;
      z-index: 20 !important;
      box-shadow: 0 -2px 6px -1px rgba(0, 0, 0, 0.05) !important;
    }
    .tech-bookmark-body {
      background: #ffffff;
      border: 1px solid #cbd5e1;
      border-radius: 0 0.75rem 0.75rem 0.75rem;
      padding: 1rem;
      position: relative;
      z-index: 1;
      box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.03);
    }
    @media (max-width: 640px) {
      .tech-bookmark-body {
        border-radius: 0 0 0.75rem 0.75rem;
        padding: 0.75rem;
      }
    }
    /* 原理維度專用：一塊一塊技術文件切換按鈕 */
    .tech-doc-block-btn {
      font-weight: 600;
      transition: all 0.15s ease;
    }
    .tech-doc-block-btn.active {
      background-color: #1e3a8a !important;
      color: #ffffff !important;
      border-color: #1e3a8a !important;
      font-weight: 700 !important;
      box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
    }
  `;
  document.head.appendChild(styleEl);
}

// 立即嘗試注入樣式
ensureTechModuleStyles();

/**
 * 取得特定專題分類所支援的三大核心維度子分頁清單
 * 1. 原理機制 (principles)
 * 2. 總覽目錄 (catalog)
 * 3. 單一產品技術 (single)
 */
function getCategoryTabs(slug) {
  return [
    { key: 'principles', label: '1. 原理', icon: 'fa-atom' },
    { key: 'catalog', label: '2. 目錄', icon: 'fa-list-check' },
    { key: 'single', label: '3. 單一產品技術', icon: 'fa-flask-vial' }
  ];
}

/**
 * 智慧取得特定產品線最佳的預設子分頁 (優先維持當前或選擇有文件的分頁，杜絕空白頁面)
 */
function getBestSubTabForCategory(slug) {
  const catData = TECH_DATABASE[slug];
  if (!catData || !catData.tabs) return 'principles';

  const validTabs = getCategoryTabs(slug).map(t => t.key);

  // 若當前選取的 subTab 在目標類別支援的維度中且有文件，維持當前選取
  if (TechState.activeSubTab && validTabs.includes(TechState.activeSubTab) && catData.tabs[TechState.activeSubTab] && catData.tabs[TechState.activeSubTab].length > 0) {
    return TechState.activeSubTab;
  }

  // 依有效維度順序搜尋首個有資料的分頁
  for (const tabKey of validTabs) {
    if (catData.tabs[tabKey] && catData.tabs[tabKey].length > 0) {
      return tabKey;
    }
  }
  return validTabs[0] || 'principles';
}

/**
 * 安全解析靜態資源 URL (支援 baseHref 與快取版本號)
 */
function resolveAssetUrl(relPath) {
  if (!relPath) return '';
  if (relPath.startsWith('http://') || relPath.startsWith('https://') || relPath.startsWith('data:')) {
    return relPath;
  }
  if (typeof window !== 'undefined' && typeof window.resolveAssetUrl === 'function' && window.resolveAssetUrl !== resolveAssetUrl) {
    return window.resolveAssetUrl(relPath);
  }
  const baseHref = window.APP_BASE_HREF || '/';
  const cleanPath = relPath.replace(/^\.?\//, '');
  let fullUrl = (baseHref + cleanPath).replace(/\/+/g, '/');
  const appVer = (typeof window !== 'undefined' && window.APP_VERSION) ? window.APP_VERSION : '20261015_v2';
  if ((cleanPath.endsWith('.json') || cleanPath.endsWith('.webp') || cleanPath.endsWith('.png')) && !fullUrl.includes('v=')) {
    fullUrl += (fullUrl.includes('?') ? '&' : '?') + `v=${appVer}`;
  }
  return fullUrl;
}

/**
 * 安全編碼文件 URL (保留斜線但轉義空格與中文)
 */
function getEncodedPdfUrl(relPath) {
  if (!relPath) return '';
  const cleanPath = relPath.replace(/^\.?\//, '');
  const segments = cleanPath.split('/');
  const encodedSegments = segments.map(seg => encodeURIComponent(seg));
  const finalPath = encodedSegments.join('/');
  return resolveAssetUrl(finalPath) + '#toolbar=0&navpanes=0';
}

/**
 * 切換技術專區三大維度子分頁
 */
function switchTechSubTab(subTabKey) {
  TechState.activeSubTab = subTabKey;
  const subTabs = ['principles', 'catalog', 'single'];

  subTabs.forEach(key => {
    const btn = document.getElementById(`tech-subtab-${key}`);
    const panel = document.getElementById(`tech-panel-${key}`);

    if (btn) {
      if (key === subTabKey) {
        btn.className = "tech-subtab-btn active";
      } else {
        btn.className = "tech-subtab-btn";
      }
    }

    if (panel) {
      if (key === subTabKey) {
        panel.classList.remove('hidden');
        // 若包含未渲染的 PDF 容器，觸發渲染
        const viewer = panel.querySelector('.pdf-viewer-container');
        if (viewer && !viewer.querySelector('canvas')) {
          const pdfUrl = viewer.getAttribute('data-pdf-url');
          if (pdfUrl && viewer.id) {
            renderPdfDocumentToContainer(viewer.id, pdfUrl);
          }
        }
      } else {
        panel.classList.add('hidden');
      }
    }
  });
}

/**
 * 建立三大子分頁單行標籤列 HTML
 */
function buildSubTabNavHtml(activeKey, hasData = true, slug = '') {
  const tabs = getCategoryTabs(slug);

  return `
        <div class="tech-subtab-strip" role="tablist" aria-label="技術專題三大核心維度導覽">
            ${tabs.map(tab => {
    const isActive = (tab.key === activeKey);
    const activeCls = isActive ? "active" : "";
    return `
                    <button type="button" onclick="switchTechSubTab('${tab.key}')" id="tech-subtab-${tab.key}"
                            class="tech-subtab-btn ${activeCls}">
                        <i class="fa-solid ${tab.icon} text-xs"></i>
                        <span>${tab.label}</span>
                    </button>
                `;
  }).join('')}
        </div>
    `;
}

/**
 * 切換特定分頁中的當前選取文件 (Munzing 風格下拉選單或原理區塊連動，立即觸發 PDF Canvas 載入)
 */
function selectTechDoc(slug, tabKey, docIdx) {
  if (!TechState.activeDocIndices[slug]) {
    TechState.activeDocIndices[slug] = {
      'principles': 0,
      'catalog': 0,
      'applications': 0,
      'single': 0
    };
  }
  TechState.activeDocIndices[slug][tabKey] = docIdx;

  const catData = TECH_DATABASE[slug];
  if (!catData || !catData.tabs[tabKey]) return;
  const docs = catData.tabs[tabKey];
  if (!docs || docIdx >= docs.length) return;

  // 1. 同步更新下拉式選單值 (Munzing 下拉式卷軸選單，若存在)
  const selectElem = document.getElementById(`doc-select-${slug}-${tabKey}`);
  if (selectElem && selectElem.value !== String(docIdx)) {
    selectElem.value = String(docIdx);
  }

  // 1.1 若為原理維度 (一塊一塊按鈕模式)，同步更新區塊按鈕狀態 (只切換顏色狀態，不重置按鈕大小與字體)
  if (tabKey === 'principles') {
    const blockBtns = document.querySelectorAll(`.tech-doc-block-btn-${slug}-principles`);
    blockBtns.forEach(btn => {
      const bIdx = parseInt(btn.getAttribute('data-doc-idx'), 10);
      const isSelected = (bIdx === docIdx);
      if (isSelected) {
        btn.classList.add('bg-blue-900', 'text-white', 'font-bold', 'border-blue-900', 'ring-2', 'ring-blue-900/20', 'active');
        btn.classList.remove('bg-white', 'hover:bg-blue-50', 'text-slate-700', 'hover:text-blue-950', 'border-slate-200', 'hover:border-blue-300', 'font-semibold');
      } else {
        btn.classList.remove('bg-blue-900', 'text-white', 'font-bold', 'border-blue-900', 'ring-2', 'ring-blue-900/20', 'active');
        btn.classList.add('bg-white', 'hover:bg-blue-50', 'text-slate-700', 'hover:text-blue-950', 'border-slate-200', 'hover:border-blue-300', 'font-semibold');
      }
    });
  }

  // 2. 更新篇數指示器與 Prev/Next 按鈕狀態
  const countElem = document.getElementById(`doc-count-current-${slug}-${tabKey}`);
  if (countElem) {
    countElem.textContent = String(docIdx + 1);
  }
  const prevBtn = document.getElementById(`doc-prev-btn-${slug}-${tabKey}`);
  const nextBtn = document.getElementById(`doc-next-btn-${slug}-${tabKey}`);
  if (prevBtn) prevBtn.disabled = (docIdx <= 0);
  if (nextBtn) nextBtn.disabled = (docIdx >= docs.length - 1);

  // 3. 更新內容檢視器 (雙欄視圖：左欄 PDF Canvas 線上預覽 + 右欄技術摘要重點)
  const viewerContainer = document.getElementById(`viewer-${slug}-${tabKey}`);
  if (viewerContainer) {
    const doc = docs[docIdx];
    viewerContainer.innerHTML = buildSingleDocLayoutHtml(doc, slug, tabKey);

    // 重要修復：立即為新選取的文件觸發 PDF.js 渲染任務
    const newViewer = viewerContainer.querySelector('.pdf-viewer-container');
    if (newViewer) {
      const pdfUrl = newViewer.getAttribute('data-pdf-url');
      if (pdfUrl && newViewer.id) {
        renderPdfDocumentToContainer(newViewer.id, pdfUrl);
      }
    }
  }
}

/**
 * 快速前後切換文件 (上一篇 / 下一篇)
 */
function navigateTechDoc(slug, tabKey, step) {
  const catData = TECH_DATABASE[slug];
  if (!catData || !catData.tabs[tabKey]) return;
  const docs = catData.tabs[tabKey];
  if (!docs || docs.length <= 1) return;

  const currentIdx = (TechState.activeDocIndices[slug] && TechState.activeDocIndices[slug][tabKey]) || 0;
  const newIdx = currentIdx + step;
  if (newIdx >= 0 && newIdx < docs.length) {
    selectTechDoc(slug, tabKey, newIdx);
  }
}

// 全域快取 PDF.js 渲染任務與 PDF Document 物件
const techPdfRenderTasks = {};
const techPdfDocCache = {};

/**
 * 使用 PDF.js 將 PDF 多頁渲染至 Canvas 容器 (完全防右鍵另存新檔、高解析度抗模糊、流暢滾動)
 */
async function renderPdfDocumentToContainer(containerId, pdfUrl) {
  const container = document.getElementById(containerId);
  if (!container) return;

  if (techPdfRenderTasks[containerId]) {
    techPdfRenderTasks[containerId].cancelled = true;
  }
  const currentTask = { cancelled: false };
  techPdfRenderTasks[containerId] = currentTask;

  const cleanPdfUrl = pdfUrl.split('#')[0];

  try {
    if (typeof window.pdfjsLib === 'undefined') {
      console.warn('PDF.js 未就緒');
      return;
    }

    window.pdfjsLib.GlobalWorkerOptions.workerSrc = (window.APP_BASE_HREF || '/') + 'js/vendor/pdf.worker.min.js';

    let pdf = techPdfDocCache[cleanPdfUrl];
    if (!pdf) {
      const loadingTask = window.pdfjsLib.getDocument(cleanPdfUrl);
      pdf = await loadingTask.promise;
      techPdfDocCache[cleanPdfUrl] = pdf;
    }
    if (currentTask.cancelled) return;

    // 僅渲染第 1 頁作為技術文件封面 (Cover)，計算等比例縮放，絕不拉伸變形
    const page = await pdf.getPage(1);
    if (currentTask.cancelled) return;

    let containerWidth = container.clientWidth;
    let containerHeight = container.clientHeight;
    if (!containerWidth || containerWidth < 200) {
      containerWidth = container.offsetWidth || Math.min(520, window.innerWidth - 48);
    }
    if (!containerHeight || containerHeight < 300) {
      containerHeight = container.offsetHeight || (window.innerWidth >= 640 ? 640 : 580);
    }
    const availWidth = Math.max(200, containerWidth - 24);
    const availHeight = Math.max(650, containerHeight - 24);

    const unscaledViewport = page.getViewport({ scale: 1 });

    // 嚴格等比例縮放：取寬與高容納比率的較小者，保證完整保留原文件版面比例，完全不拉伸
    const scaleW = availWidth / unscaledViewport.width;
    const scaleH = availHeight / unscaledViewport.height;
    const fitScale = Math.min(scaleW, scaleH);

    const dpr = window.devicePixelRatio || 1;
    const viewport = page.getViewport({ scale: fitScale * dpr });

    const canvasWrapper = document.createElement('div');
    canvasWrapper.className = 'cover-canvas-wrapper w-full h-full flex items-center justify-center p-2 select-none pointer-events-none';
    canvasWrapper.setAttribute('oncontextmenu', 'return false;');
    canvasWrapper.setAttribute('draggable', 'false');

    const canvas = document.createElement('canvas');
    canvas.className = 'rounded-lg shadow-sm border border-slate-200 bg-white block transition-transform duration-200 group-hover:scale-[1.01] pointer-events-none select-none';
    canvas.style.userSelect = 'none';
    canvas.style.webkitUserSelect = 'none';
    const cssW = Math.floor(unscaledViewport.width * fitScale);
    const cssH = Math.floor(unscaledViewport.height * fitScale);
    canvas.style.width = cssW + 'px';
    canvas.style.height = cssH + 'px';
    canvas.style.maxWidth = '100%';
    canvas.style.maxHeight = '100%';
    canvas.style.objectFit = 'contain';
    canvas.style.aspectRatio = `${unscaledViewport.width} / ${unscaledViewport.height}`;

    const context = canvas.getContext('2d');
    canvas.height = viewport.height;
    canvas.width = viewport.width;

    await page.render({
      canvasContext: context,
      viewport: viewport
    }).promise;

    if (currentTask.cancelled) return;

    // 移除載入轉圈文字及可能存在的舊 canvas
    container.querySelectorAll('.loading-spinner, .text-slate-400, .cover-canvas-wrapper').forEach(el => el.remove());

    // 插入封面 Canvas
    canvasWrapper.appendChild(canvas);
    container.appendChild(canvasWrapper);
  } catch (err) {
    console.error('PDF.js cover render error:', err);
  }
}

async function renderPdfFullscreen(container, pdfUrl, scaleMultiplier = 1.0) {
  const cleanPdfUrl = pdfUrl.split('#')[0];
  currentModalScaleMultiplier = scaleMultiplier;
  currentModalPdfUrl = pdfUrl;

  const zoomIndicator = document.getElementById('tech-modal-zoom-val');
  if (zoomIndicator) {
    zoomIndicator.textContent = `${Math.round(scaleMultiplier * 100)}%`;
  }

  try {
    if (typeof window.pdfjsLib === 'undefined') {
      container.innerHTML = `<iframe src="${cleanPdfUrl}#toolbar=0&navpanes=0" class="w-full h-full border-0"></iframe>`;
      return;
    }

    window.pdfjsLib.GlobalWorkerOptions.workerSrc = (window.APP_BASE_HREF || '/') + 'js/vendor/pdf.worker.min.js';

    let pdf = techPdfDocCache[cleanPdfUrl];
    if (!pdf) {
      const loadingTask = window.pdfjsLib.getDocument(cleanPdfUrl);
      pdf = await loadingTask.promise;
      techPdfDocCache[cleanPdfUrl] = pdf;
    }

    container.innerHTML = '';
    const modalWidth = container.clientWidth || window.innerWidth || 1200;
    // 全畫面模式下，提供寬廣舒適的滿版閱讀視野 (桌面滿版達 1180px，自適應且支援放大縮小)
    const baseTargetWidth = Math.min(1180, Math.max(680, modalWidth - 64));
    const targetWidth = Math.max(320, baseTargetWidth * scaleMultiplier);
    const dpr = window.devicePixelRatio || 1;

    for (let pageNum = 1; pageNum <= pdf.numPages; pageNum++) {
      const page = await pdf.getPage(pageNum);
      const unscaledViewport = page.getViewport({ scale: 1 });
      const scale = targetWidth / unscaledViewport.width;
      const finalScale = Math.max(1.0, scale);
      const viewport = page.getViewport({ scale: finalScale * dpr });

      const canvasWrapper = document.createElement('div');
      canvasWrapper.className = 'w-full flex flex-col items-center mb-8 select-none';
      canvasWrapper.setAttribute('oncontextmenu', 'return false;');
      canvasWrapper.setAttribute('draggable', 'false');

      const pageLabel = document.createElement('div');
      pageLabel.className = 'text-[11px] font-bold text-slate-400 mb-2 px-3 py-0.5 rounded-full bg-slate-900 border border-slate-800 shadow-sm';
      pageLabel.textContent = `第 ${pageNum} 頁 / 共 ${pdf.numPages} 頁`;

      const canvas = document.createElement('canvas');
      canvas.className = 'rounded-md shadow-2xl bg-white block max-w-none border border-slate-700/60';
      canvas.style.pointerEvents = 'none';
      canvas.style.userSelect = 'none';
      canvas.style.webkitUserSelect = 'none';
      canvas.style.width = Math.floor(unscaledViewport.width * finalScale) + 'px';
      canvas.style.height = Math.floor(unscaledViewport.height * finalScale) + 'px';

      const context = canvas.getContext('2d');
      canvas.height = viewport.height;
      canvas.width = viewport.width;

      await page.render({
        canvasContext: context,
        viewport: viewport
      }).promise;

      canvasWrapper.appendChild(pageLabel);
      canvasWrapper.appendChild(canvas);
      container.appendChild(canvasWrapper);
    }
  } catch (err) {
    console.error('Fullscreen render error:', err);
    container.innerHTML = `
            <div class="text-center py-16 text-slate-400">
                <i class="fa-solid fa-triangle-exclamation text-3xl text-amber-500 mb-3"></i>
                <p class="text-base font-semibold">文件載入失敗，請檢查網路連線或稍後重試。</p>
            </div>
        `;
  }
}

/**
 * 全螢幕放大縮放控制
 */
function changeFullscreenZoom(delta) {
  let newMultiplier = currentModalScaleMultiplier + delta;
  newMultiplier = Math.max(0.5, Math.min(3.0, newMultiplier));
  const container = document.getElementById('tech-modal-pdf-container');
  if (container && currentModalPdfUrl) {
    renderPdfFullscreen(container, currentModalPdfUrl, newMultiplier);
  }
}

function resetFullscreenZoom() {
  const container = document.getElementById('tech-modal-pdf-container');
  if (container && currentModalPdfUrl) {
    renderPdfFullscreen(container, currentModalPdfUrl, 1.0);
  }
}

/**
 * 開啟 PDF 全螢幕滿版檢視模態視窗 (真正全畫面滿版閱讀，支援縮放與鍵盤導航)
 */
function openPdfFullscreenModal(pdfUrl, title) {
  let modal = document.getElementById('tech-pdf-fullscreen-modal');
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'tech-pdf-fullscreen-modal';
    modal.style.cssText = 'position:fixed!important;top:0!important;left:0!important;right:0!important;bottom:0!important;width:100vw!important;height:100vh!important;margin:0!important;padding:0!important;z-index:99999!important;background:#0f172a!important;display:flex!important;flex-direction:column!important;box-sizing:border-box!important;';
    modal.setAttribute('oncontextmenu', 'return false;');
    modal.innerHTML = `
            <div class="tech-modal-inner relative w-screen h-screen flex flex-col bg-slate-900 overflow-hidden"
                 style="z-index:100000!important;width:100vw!important;height:100vh!important;max-width:100vw!important;max-height:100vh!important;border-radius:0!important;border:none!important;"
                 onclick="event.stopPropagation();">
                
                <!-- 頂部滿版操作列 -->
                <div class="flex items-center justify-between px-3 sm:px-6 py-2.5 bg-slate-900 border-b border-slate-800 shrink-0 gap-3 text-white"
                     style="z-index:100001!important;">
                    <div class="flex items-center gap-2.5 sm:gap-3 min-w-0 pr-2">
                        <span class="w-8 h-8 rounded-lg bg-red-500/20 text-red-400 flex items-center justify-center shrink-0 border border-red-500/30">
                            <i class="fa-solid fa-file-pdf text-sm"></i>
                        </span>
                        <div class="min-w-0">
                            <h3 id="tech-modal-title" class="text-sm sm:text-base font-bold text-white truncate leading-snug">技術文件全畫面閱讀</h3>
                            
                        </div>
                    </div>
                    
                    <!-- 縮放工具列與關閉按鈕 -->
                    <div class="flex items-center gap-2 sm:gap-3 shrink-0">
                        <div class="flex items-center bg-slate-800 border border-slate-700 rounded-lg p-0.5 shadow-sm text-slate-300">
                            <button type="button" onclick="changeFullscreenZoom(-0.2)" title="縮小"
                                    class="w-7 sm:w-8 h-7 sm:h-8 flex items-center justify-center text-slate-300 hover:text-white hover:bg-slate-700 rounded transition-colors cursor-pointer">
                                <i class="fa-solid fa-magnifying-glass-minus text-xs"></i>
                            </button>
                            <button type="button" onclick="resetFullscreenZoom()" title="重設為 100%"
                                    class="px-2 sm:px-2.5 h-7 sm:h-8 text-xs font-bold text-slate-200 hover:bg-slate-700 rounded transition-colors cursor-pointer">
                                <span id="tech-modal-zoom-val">100%</span>
                            </button>
                            <button type="button" onclick="changeFullscreenZoom(0.2)" title="放大"
                                    class="w-7 sm:w-8 h-7 sm:h-8 flex items-center justify-center text-slate-300 hover:text-white hover:bg-slate-700 rounded transition-colors cursor-pointer">
                                <i class="fa-solid fa-magnifying-glass-plus text-xs"></i>
                            </button>
                        </div>

                        <button type="button" onclick="closePdfFullscreenModal()"
                                class="inline-flex items-center gap-1.5 px-3 sm:px-4 py-1.5 sm:py-2 bg-red-600 hover:bg-red-500 text-white text-xs sm:text-sm font-bold rounded-lg shadow-sm transition-colors cursor-pointer">
                            <i class="fa-solid fa-xmark text-sm"></i>
                            <span>關閉 (ESC)</span>
                        </button>
                    </div>
                </div>

                <!-- 全畫面滿版 PDF 渲染容器 -->
                <div id="tech-modal-pdf-container"
                     class="flex-1 w-full h-full overflow-y-auto overflow-x-auto p-4 sm:p-8 bg-slate-950 flex flex-col items-center select-none"
                     style="scroll-behavior: smooth;"
                     oncontextmenu="return false;">
                    <div class="flex flex-col items-center justify-center h-full text-slate-400 gap-2">
                        <i class="fa-solid fa-circle-notch fa-spin text-2xl text-blue-400"></i>
                        <span class="text-sm font-semibold text-slate-300">全畫面高解析文件載入中...</span>
                    </div>
                </div>
            </div>
        `;
    document.body.appendChild(modal);

    // 綁定 ESC 鍵關閉
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') closePdfFullscreenModal();
    });
  }

  modal.classList.remove('hidden');
  modal.style.setProperty('display', 'flex', 'important');
  modal.style.setProperty('z-index', '99999', 'important');
  document.body.style.overflow = 'hidden';

  const titleEl = document.getElementById('tech-modal-title');
  if (titleEl) titleEl.textContent = title || '原廠技術文件';

  const container = document.getElementById('tech-modal-pdf-container');
  if (container) {
    container.innerHTML = `
            <div class="flex flex-col items-center justify-center h-full py-16 text-slate-400 gap-2">
                <i class="fa-solid fa-circle-notch fa-spin text-2xl text-blue-400"></i>
                <span class="text-sm font-semibold text-slate-300">正在以高解析度渲染全畫面文件...</span>
            </div>
        `;
    renderPdfFullscreen(container, pdfUrl, 1.0);
  }
}

function closePdfFullscreenModal() {
  const modal = document.getElementById('tech-pdf-fullscreen-modal');
  if (modal) {
    modal.classList.add('hidden');
    modal.style.setProperty('display', 'none', 'important');
  }
  document.body.style.overflow = '';
}

// 全面攔截在 PDF 預覽與技術專區的右鍵選單與快捷鍵另存
document.addEventListener('contextmenu', function (e) {
  if (e.target.closest('.pdf-viewer-container') || e.target.closest('.tech-principles-grid') || e.target.closest('#tech-pdf-fullscreen-modal')) {
    e.preventDefault();
    return false;
  }
}, true);

window.addEventListener('keydown', function (e) {
  if ((e.ctrlKey || e.metaKey) && (e.key === 's' || e.key === 'S' || e.key === 'p' || e.key === 'P')) {
    const viewer = document.querySelector('.pdf-viewer-container') || document.getElementById('tech-pdf-fullscreen-modal');
    if (viewer) {
      e.preventDefault();
      return false;
    }
  }
});


/**
 * 建立單一文件左右雙欄檢視視圖 HTML (比照原理排版架構，線上預覽不開放下載)
 */
function buildSingleDocLayoutHtml(doc, slug, tabKey) {
  const cat = TECH_CATEGORIES.find(c => c.slug === slug) || { name: '特用化學品', productLink: 'products/' };
  const pdfUrl = getEncodedPdfUrl(doc.pdfPath);
  const hasMechImg = Boolean(doc.mechImg);
  const isPdf = Boolean(doc.pdfPath && doc.pdfPath.toLowerCase().endsWith('.pdf'));
  const escapedTitle = (doc.title || '').replace(/'/g, "\\'").replace(/"/g, '&quot;');
  const docTitleClean = (doc.title || '').replace(/"/g, '&quot;');
  const inquiryParam = encodeURIComponent(`${cat.name}-${doc.title || ''}`);
  const productLink = cat.productLink || 'products/';

  const advantagesHtml = (doc.advantages || []).map((adv, idx) => `
        <li class="flex items-start gap-1.5">
            <span class="w-4 h-4 rounded-full bg-emerald-100 text-emerald-800 flex items-center justify-center shrink-0 mt-0.5 font-bold text-xs">${idx + 1}</span>
            <span>${adv}</span>
        </li>
    `).join('');

  const applicationsHtml = (doc.applications || []).map(app => `
        <span class="px-2 py-0.5 rounded bg-white text-slate-700 text-xs font-medium border border-slate-200">${app}</span>
    `).join('');

  // 若該技術文件無圖片亦無 PDF 封面（例如純文字手冊章節）：
  // 採滿版對稱佈局，徹底解決畫面左半邊為空卡片、右半邊單邊擠壓之問題
  if (!hasMechImg && !isPdf) {
    return `
        <div class="bg-slate-50/70 rounded-xl border border-slate-200 p-4 sm:p-5 space-y-3.5">
            <!-- 頂部：專題標題與手冊來源徽章 -->
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2.5 border-b border-slate-200/80 pb-3">
                <div class="flex items-center gap-2.5">
                    
                    <div>
                        <h3 class="text-base sm:text-lg font-bold text-slate-900 leading-snug">
                            ${docTitleClean}
                        </h3>
                        
                    </div>
                </div>
                
            </div>

            <!-- 核心作用原理說明 (滿版清晰舒適) -->
            ${doc.desc ? `
            <div class="p-3.5 rounded-xl bg-white border border-slate-200/90 shadow-2xs">
               
                <p class="text-sm text-slate-700 leading-relaxed font-normal">
                    ${doc.desc}
                </p>
            </div>
            ` : ''}

            <!-- 下半部：左右雙欄平衡展示技術特點與適用範疇 -->
            <div class="grid grid-cols-1 md:grid-cols-1 gap-3.5 pt-0.5">
                <!-- 主要技術特點 -->
                <div class="space-y-2 bg-white p-3.5 rounded-xl border border-slate-200/80 shadow-2xs">
                    <div class="flex items-center gap-1.5 text-xs font-bold text-blue-950">
                        <i class="fa-solid fa-circle-check text-emerald-600 text-xs"></i>
                        <span>主要內容與技術特點：</span>
                    </div>
                    ${advantagesHtml ? `
                    <ul class="space-y-1.5 text-sm text-slate-700">
                        ${advantagesHtml}
                    </ul>
                    ` : '<p class="text-xs text-slate-400">詳見技術手冊內文規範</p>'}
                </div>

                
            </div>
        </div>
    `;
  }

  let previewBoxHtml = '';
  if (hasMechImg) {
    // 原廠技術機制圖 (高清示意圖展示)
    previewBoxHtml = `
            <div class="h-full flex flex-col justify-center">
                <div class="bg-white rounded-xl border border-slate-200 p-4 shadow-2xs flex flex-col items-center justify-center min-h-[460px] sm:min-h-[560px] overflow-hidden select-none" oncontextmenu="return false;">
                    
                    <img src="${resolveAssetUrl(doc.mechImg)}" alt="${escapedTitle} 反應機制圖"
                         class="w-full max-h-[420px] sm:max-h-[500px] object-contain rounded select-none pointer-events-none"
                         draggable="false">
                </div>
            </div>
        `;
  } else if (isPdf) {
    // 文件封面卡片：第一頁作為封面 (等比例不拉伸)，點擊封面直接開啟全螢幕放大閱讀
    const viewerId = `pdf-canvas-viewer-${slug}-${tabKey}`;
    previewBoxHtml = `
            <div class="h-full flex flex-col justify-center">
                <div id="${viewerId}"
                     class="pdf-viewer-container group relative w-full h-[580px] sm:h-[640px] rounded-xl border border-slate-200 bg-white p-3 flex items-center justify-center overflow-hidden select-none cursor-pointer transition-all duration-200 hover:border-blue-500 hover:shadow-lg"
                     data-pdf-url="${pdfUrl}"
                     data-pdf-title="${escapedTitle}"
                     onclick="openPdfFullscreenModal('${pdfUrl}', '${escapedTitle}')"
                     title="點擊封面全螢幕放大閱讀"
                     oncontextmenu="return false;"
                     onselectstart="return false;">
                    
                    <div class="loading-spinner flex flex-col items-center justify-center h-full text-slate-400 gap-2">
                        <i class="fa-solid fa-circle-notch fa-spin text-xl text-blue-900"></i>
                        <span class="text-xs font-semibold text-slate-600">文件封面載入中...</span>
                    </div>
                </div>
            </div>
        `;
  }

  return `
        <div class="tech-principles-grid bg-slate-50/70 rounded-xl border border-slate-200 p-3 sm:p-3.5">
            <!-- 左欄：線上文件封面預覽 (點擊封面直接全螢幕放大閱讀，徹底防止右鍵另存) -->
            <div class="h-full pr-0 sm:pr-2.5 border-b sm:border-b-0 sm:border-r border-slate-200/80 pb-2.5 sm:pb-0">
                ${previewBoxHtml}
            </div>

            <!-- 右欄：文件檔案屬性與技術重點摘要 (依圖 1 指示：移除被劃掉的語言/版本標籤與檔案名字串) -->
            <div class="space-y-2 pl-0 sm:pl-2.5">
                <div>
                    <h3 class="text-base sm:text-lg font-bold text-slate-900 leading-snug">
                        ${docTitleClean}
                    </h3>
                </div>

                <p class="text-sm text-slate-700 leading-relaxed font-normal bg-white p-2.5 rounded-lg border border-slate-200/80 shadow-2xs">
                    ${doc.desc || doc.summary || ''}
                </p>

                ${advantagesHtml ? `
                <!-- 主要技術特點 -->
                <div class="space-y-1.5">
                    <div class="flex items-center gap-1.5 text-xs font-bold text-blue-950">
                        <i class="fa-solid fa-circle-check text-emerald-600 text-xs"></i>
                        <span>主要內容與技術特點：</span>
                    </div>
                    <ul class="space-y-1 text-sm text-slate-700">
                        ${advantagesHtml}
                    </ul>
                </div>
                ` : ''}

                ${applicationsHtml ? `
                <!-- 適用範疇標籤 -->
                <div class="space-y-1 pt-0.5">
                    <span class="text-xs font-bold text-slate-700">適用範疇 / 相關領域：</span>
                    <div class="flex flex-wrap gap-1">
                        ${applicationsHtml}
                    </div>
                </div>
                ` : ''}
            </div>
        </div>
    `;
}

/**
 * 建立無公開資料提示區塊 HTML (實事求是、誠實告知、不杜撰)
 */
function buildEmptyTabHtml(cat, tabKey) {
  const tabNames = {
    principles: '原理機制',
    catalog: '總覽目錄',
    applications: '應用技術資料',
    single: '單一產品技術資料',
    formulation: '配方'
  };
  const name = tabNames[tabKey] || '技術資料';
  const catName = cat.name || '特用化學品';
  const inquiryParam = encodeURIComponent(catName);
  const productLink = cat.productLink || 'products/';

  return `
        <div class="rounded-xl border border-slate-200 bg-slate-50/70 p-4 sm:p-6 text-center space-y-2.5">
            <div class="flex items-center justify-center gap-2">
                <i class="fa-solid fa-folder-open text-slate-400 text-base"></i>
                <span class="px-2 py-0.5 rounded-full bg-slate-200 text-slate-700 text-xs font-bold">資料整理中</span>
                <span class="text-sm sm:text-base font-bold text-blue-950">原廠技術資料整理中，暫無公開${name}</span>
            </div>
            <p class="text-sm text-slate-600 max-w-lg mx-auto leading-relaxed">
                目前原廠未提供此項之公開資料，我們秉持實事求是原則不進行臆測杜撰。若您需要特定規格手冊或評估樣品，歡迎直接聯繫宏威業務團隊為您服務。
            </p>
            <div class="pt-1 flex items-center justify-center gap-2.5">
                <a href="contact/?mode=detailed&inquiry=${inquiryParam}"
                   class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-blue-900 hover:bg-blue-800 text-white text-xs font-bold rounded-lg shadow-2xs transition-all active:scale-95">
                    <i class="fa-solid fa-paper-plane text-xs"></i>
                    <span>聯繫業務索取資料</span>
                </a>
                <a href="${productLink}"
                   class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 text-xs font-bold rounded-lg transition-all">
                    <i class="fa-solid fa-table-list text-xs"></i>
                    <span>瀏覽相關產品專區</span>
                </a>
        </div>
        </div>
    `;
}

function buildCategoryContentHtml(cat) {
  const slug = cat.slug;
  const catData = TECH_DATABASE[slug] || { tabs: {} };
  const subTabs = getCategoryTabs(slug).map(t => t.key);

  const panelsHtml = subTabs.map(tabKey => {
    const docs = catData.tabs[tabKey] || [];
    const isHidden = (TechState.activeSubTab !== tabKey);
    const hiddenCls = isHidden ? 'hidden ' : '';

    if (docs.length === 0) {
      return `
                <div id="tech-panel-${tabKey}" class="${hiddenCls}space-y-2">
                    ${buildEmptyTabHtml(cat, tabKey)}
                </div>
            `;
    }

    const activeIdx = (TechState.activeDocIndices[slug] && TechState.activeDocIndices[slug][tabKey]) || 0;
    const validIdx = activeIdx < docs.length ? activeIdx : 0;
    const currentDoc = docs[validIdx];

    if (docs.length > 1) {
      if (tabKey === 'principles') {
        // 原理維度：依指示改成如圖2一塊一塊按鈕導覽
        const blocksHtml = docs.map((doc, idx) => {
          const isSelected = (idx === validIdx);
          const activeCls = isSelected
            ? "bg-blue-900 text-white font-bold border-blue-900 shadow-2xs ring-2 ring-blue-900/20 active"
            : "bg-white hover:bg-blue-50 text-slate-700 hover:text-blue-950 border-slate-200 hover:border-blue-300 font-semibold";
          return `
            <button type="button"
                    data-doc-idx="${idx}"
                    onclick="selectTechDoc('${slug}', 'principles', ${idx})"
                    class="tech-doc-block-btn tech-doc-block-btn-${slug}-principles inline-flex items-center justify-center px-2 py-1 rounded-md border text-xs transition-all duration-150 cursor-pointer ${activeCls}">
                <span>${doc.shortLabel || doc.title}</span>
            </button>
          `;
        }).join('');

        return `
                <div id="tech-panel-principles" class="${hiddenCls}space-y-3">
                    <!-- 一塊一塊技術文件選擇列 (依圖 2 指示：原理專用區塊按鈕) -->
                    <div class="tech-principles-blocks-bar bg-slate-50 border border-slate-200/90 rounded-lg p-2 flex flex-col sm:flex-row items-stretch sm:items-center gap-2 shadow-2xs">
                        
                        <div class="flex flex-wrap items-center gap-1.5 flex-1">
                            ${blocksHtml}
                        </div>
                    </div>

                    <!-- 100% 滿版雙欄核心展示區 -->
                    <div id="viewer-${slug}-principles" class="w-full">
                        ${buildSingleDocLayoutHtml(currentDoc, slug, 'principles')}
                    </div>
                </div>
        `;
      }

      // 其他分頁（目錄、應用技術、單一產品技術）：維持既有 Munzing 下拉選單不變
      let optionsHtml = '';
      if (tabKey === 'single') {
        // 單一產品：依相同產品系列分組 optgroup
        const groups = {};
        const groupNames = [];
        docs.forEach((doc, idx) => {
          const grp = doc.productGroup || '其他';
          if (!groups[grp]) {
            groups[grp] = [];
            groupNames.push(grp);
          }
          groups[grp].push({ doc, idx });
        });

        optionsHtml = groupNames.map(grpName => {
          const list = groups[grpName];
          const optLines = list.map(({ doc, idx }) => {
            const selectedAttr = (idx === validIdx) ? ' selected' : '';
            return `<option value="${idx}"${selectedAttr}>${doc.shortLabel || doc.title}</option>`;
          }).join('');
          return `<optgroup label="── ${grpName} (${list.length} 篇) ──">${optLines}</optgroup>`;
        }).join('');
      } else {
        // 一般條列 option
        optionsHtml = docs.map((doc, idx) => {
          const selectedAttr = (idx === validIdx) ? ' selected' : '';
          return `<option value="${idx}"${selectedAttr}>${doc.shortLabel || doc.title}</option>`;
        }).join('');
      }

      return `
                <div id="tech-panel-${tabKey}" class="${hiddenCls}space-y-3">
                    <!-- 下拉式卷軸選單列 (Munzing 風格：精緻簡潔、完全不佔據兩側版面空間) -->
                    <div class="tech-doc-selector-bar bg-slate-50 border border-slate-200/90 rounded-xl p-2.5 sm:p-3 flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-2.5 shadow-2xs">
                        <div class="flex items-center gap-2 sm:gap-3 flex-1 min-w-0">
                            
                            <div class="relative flex-1 min-w-0 max-w-full sm:max-w-xl">
                                <select id="doc-select-${slug}-${tabKey}" onchange="selectTechDoc('${slug}', '${tabKey}', parseInt(this.value, 10))"
                                        class="w-full bg-white hover:bg-slate-50/50 border border-slate-300 hover:border-blue-500 focus:border-blue-900 focus:ring-2 focus:ring-blue-100 rounded-lg px-3 py-2 text-xs sm:text-sm font-semibold text-slate-800 shadow-2xs cursor-pointer transition-all truncate">
                                    ${optionsHtml}
                                </select>
                            </div>
                        </div>

                        <!-- 篇數統計與上一篇/下一篇快速切換按鈕 -->
                        <div class="flex items-center justify-between sm:justify-end gap-2 shrink-0 pt-1 sm:pt-0 border-t sm:border-t-0 border-slate-200/60">
                            <span class="text-xs font-medium text-slate-500 bg-white px-2 py-1 rounded-md border border-slate-200 shadow-2xs">
                                第 <strong id="doc-count-current-${slug}-${tabKey}" class="text-blue-950 font-bold">${validIdx + 1}</strong> / ${docs.length} 篇
                            </span>
                            <div class="flex items-center gap-1">
                                <button type="button" id="doc-prev-btn-${slug}-${tabKey}" onclick="navigateTechDoc('${slug}', '${tabKey}', -1)"
                                        ${validIdx === 0 ? 'disabled' : ''}
                                        class="w-8 h-8 rounded-lg bg-white hover:bg-blue-50 border border-slate-200 hover:border-blue-400 text-slate-700 hover:text-blue-900 flex items-center justify-center transition-all disabled:opacity-40 disabled:cursor-not-allowed shadow-2xs"
                                        title="上一篇技術文件">
                                    <i class="fa-solid fa-chevron-left text-xs"></i>
                                </button>
                                <button type="button" id="doc-next-btn-${slug}-${tabKey}" onclick="navigateTechDoc('${slug}', '${tabKey}', 1)"
                                        ${validIdx === docs.length - 1 ? 'disabled' : ''}
                                        class="w-8 h-8 rounded-lg bg-white hover:bg-blue-50 border border-slate-200 hover:border-blue-400 text-slate-700 hover:text-blue-900 flex items-center justify-center transition-all disabled:opacity-40 disabled:cursor-not-allowed shadow-2xs"
                                        title="下一篇技術文件">
                                    <i class="fa-solid fa-chevron-right text-xs"></i>
                                </button>
                            </div>
                        </div>
                    </div>

                    <!-- 100% 滿版雙欄核心展示區 -->
                    <div id="viewer-${slug}-${tabKey}" class="w-full">
                        ${buildSingleDocLayoutHtml(currentDoc, slug, tabKey)}
                    </div>
                </div>
            `;
    } else {
      // 僅 1 篇文件時直接滿版展示
      return `
                <div id="tech-panel-${tabKey}" class="${hiddenCls}space-y-2">
                    <div id="viewer-${slug}-${tabKey}" class="w-full">
                        ${buildSingleDocLayoutHtml(currentDoc, slug, tabKey)}
                    </div>
                </div>
            `;
    }
  }).join('');

  return `
        <section class="bg-white border border-slate-200 rounded-xl shadow-xs p-3 sm:p-4 space-y-2.5">
            <!-- 專題標題與頂部操作列 (依圖 1 指示：改成產品類別名稱 cat.name) -->
            <div class="flex items-center justify-between gap-3 pb-2 border-b border-slate-100">
                <div class="flex items-center gap-2 min-w-0">
                    <span class="w-1.5 h-4 bg-blue-900 rounded-full inline-block shrink-0"></span>
                    <h1 class="text-base sm:text-lg font-bold text-blue-950 tracking-tight truncate">
                        ${cat.name}
                    </h1>
                </div>
                
                <div class="shrink-0 flex items-center">
                    <a href="${cat.productLink}"
                       class="inline-flex items-center gap-1 px-2.5 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-md text-xs font-bold transition-colors">
                        <i class="fa-solid fa-table-list text-xs"></i>
                        <span>${cat.productLinkText}</span>
                    </a>
                </div>
            </div>

            

            <!-- 瀏覽器書籤風格容器 -->
            <div class="tech-bookmark-wrapper mt-1">
                ${buildSubTabNavHtml(TechState.activeSubTab, cat.hasData, slug)}

                <div class="tech-bookmark-body">
                    ${panelsHtml}
                </div>
            </div>
        </section>
    `;
}

/**
 * 切換技術產品分類 (11 大專題)
 */
function switchTechCategory(slug, updateUrl = true) {
  const cat = TECH_CATEGORIES.find(c => c.slug === slug);
  if (!cat) return;

  TechState.activeCategory = slug;
  if (typeof AppState !== 'undefined') {
    AppState.activeTechCategory = slug;
  }

  // 1. 更新左側 Sidebar 按鈕樣式
  document.querySelectorAll('.tech-sidebar-btn').forEach(btn => {
    const btnSlug = btn.getAttribute('data-tech-slug');
    const numBadge = btn.querySelector('.tech-num-badge');
    const titleEl = btn.querySelector('.tech-btn-title');
    const subEl = btn.querySelector('.tech-btn-sub');

    if (btnSlug === slug) {
      btn.className = "tech-sidebar-btn group flex items-center p-2.5 rounded-xl bg-blue-50/90 border-2 border-blue-600/80 text-blue-950 no-underline shadow-xs transition-all";
      if (numBadge) numBadge.className = "tech-num-badge w-5 h-5 rounded-md bg-blue-900 text-white text-xs font-black flex items-center justify-center shrink-0 shadow-2xs";
      if (titleEl) titleEl.className = "tech-btn-title text-sm font-bold text-blue-950 truncate leading-snug";
      if (subEl) subEl.className = "tech-btn-sub text-xs font-medium text-blue-800/80 truncate";
    } else {
      btn.className = "tech-sidebar-btn group flex items-center p-2.5 rounded-xl bg-white hover:bg-slate-50 border border-slate-200 hover:border-blue-400 text-slate-800 hover:text-blue-950 no-underline transition-all";
      if (numBadge) numBadge.className = "tech-num-badge w-5 h-5 rounded-md bg-slate-100 group-hover:bg-blue-50 text-slate-500 group-hover:text-blue-700 text-xs font-bold flex items-center justify-center shrink-0 transition-colors";
      if (titleEl) titleEl.className = "tech-btn-title text-sm font-bold text-slate-800 group-hover:text-blue-950 truncate leading-snug";
      if (subEl) subEl.className = "tech-btn-sub text-xs font-normal text-slate-500 group-hover:text-slate-600 truncate";
    }
  });

  // 2. 更新頂部麵包屑
  const breadcrumbCurrent = document.getElementById('tech-breadcrumb-current');
  if (breadcrumbCurrent) {
    breadcrumbCurrent.innerText = cat.name;
  }

  // 3. 渲染右側內容區塊
  const mainContainer = document.getElementById('tech-content-display');
  if (mainContainer) {
    mainContainer.innerHTML = buildCategoryContentHtml(cat);
    const bestTab = getBestSubTabForCategory(slug);
    switchTechSubTab(bestTab);
  }

  // 4. 更新 URL (若為 SPA 模式)
  if (updateUrl && typeof updateUrlRoute === 'function') {
    try {
      updateUrlRoute(true);
    } catch (err) {
      console.warn('URL route update skipped:', err);
    }
  }
}

// 當 DOM 載入完成或腳本就緒時初始化技術專區
function initTechnologyModule() {
  ensureTechModuleStyles();
  const display = document.getElementById('tech-content-display');
  if (!display) return;
  const currentSlug = (document.body && document.body.getAttribute('data-tech-slug')) || 'tyzor';

  // 若頁面已由伺服器或靜態建置產生完成 (獨立子頁面)，維持既有 DOM 完整性，僅同步狀態與啟動首頁 PDF 封面渲染！
  const visiblePanel = display.querySelector('.tech-bookmark-body > div:not(.hidden)');
  if (visiblePanel) {
    TechState.activeCategory = currentSlug;
    const panelId = visiblePanel.id || '';
    const currentTabKey = panelId.replace('tech-panel-', '');
    if (currentTabKey) {
      TechState.activeSubTab = currentTabKey;
    }
    const activeViewer = visiblePanel.querySelector('.pdf-viewer-container');
    if (activeViewer && !activeViewer.querySelector('canvas')) {
      const pdfUrl = activeViewer.getAttribute('data-pdf-url');
      if (pdfUrl && activeViewer.id) {
        renderPdfDocumentToContainer(activeViewer.id, pdfUrl);
      }
    }
    return;
  }

  // SPA 模式或主頁模式下需要動態渲染
  switchTechCategory(currentSlug, false);
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initTechnologyModule);
} else {
  initTechnologyModule();
}
