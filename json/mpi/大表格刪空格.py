import os
import json

def clean_empty_values(d):
    """
    遞迴清理字典或清單中沒有 Value 的 Key/元素
    """
    if isinstance(d, dict):
        cleaned = {}
        for k, v in d.items():
            cleaned_v = clean_empty_values(v)
            # 判定沒有 value 的條件 (排除 None, "", {}, [], "N/A", "—")
            if cleaned_v not in [None, "", {}, [], "N/A", "—"]:
                cleaned[k] = cleaned_v
        return cleaned
    elif isinstance(d, list):
        cleaned_list = [clean_empty_values(v) for v in d]
        return [v for v in cleaned_list if v not in [None, "", {}, [], "N/A", "—"]]
    else:
        return d

def merge_json_databases(file_mapping, output_filename="master_database_clear.json"):
    master_db = {}

    for app_key, file_info in file_mapping.items():
        file_path = file_info["filename"]
        app_title_zh = file_info["title_zh"]
        app_title_en = file_info["title_en"]

        if not os.path.exists(file_path):
            print(f"⚠️ 找不到檔案: {file_path}，跳過處理。")
            continue

        with open(file_path, "r", encoding="utf-8") as f:
            try:
                products_list = json.load(f)
            except json.JSONDecodeError as e:
                print(f"❌ 解析 {file_path} 失敗: {e}")
                continue

        for item in products_list:
            prod_name = item.get("product_name")
            if not prod_name:
                continue

            featured_cats = item.get("featured_categories", [])
            ratings = item.get("performance_ratings", {})
            desc_zh = item.get("performance_descriptions_zh", {})
            desc_en = item.get("performance_descriptions_en", {})

            # 1. 建立產品基本資料 (第一層，完整保留 application_fields_zh 與 application_fields_en)
            if prod_name not in master_db:
                master_db[prod_name] = {
                    "product_name": prod_name,
                    "brand_code": item.get("brand_code", "MPI"),
                    "website": item.get("website", ""),
                    "composition_zh": item.get("composition_zh", ""),
                    "composition_en": item.get("composition_en", ""),
                    "chemical_component": item.get("chemical_component", ""),
                    "recommended_system_type_zh": item.get("recommended_system_type_zh", ""),
                    "recommended_system_type_en": item.get("recommended_system_type_en", ""),
                    "application_fields_zh": item.get("application_fields_zh", ""),
                    "application_fields_en": item.get("application_fields_en", ""),
                    "suggested_use_level_zh": item.get("suggested_use_level_zh", ""),
                    "suggested_use_level_en": item.get("suggested_use_level_en", ""),
                    "system": item.get("system", {}),
                    "typical_properties": item.get("typical_properties", {}),
                    "applications_data": {}
                }
            else:
                # 若主檔原本沒有 application_fields，有新讀到時自動補齊
                if not master_db[prod_name].get("application_fields_zh") and item.get("application_fields_zh"):
                    master_db[prod_name]["application_fields_zh"] = item.get("application_fields_zh")
                if not master_db[prod_name].get("application_fields_en") and item.get("application_fields_en"):
                    master_db[prod_name]["application_fields_en"] = item.get("application_fields_en")

            # 2. 建立領域資料 (第二層)
            master_db[prod_name]["applications_data"][app_key] = {
                "application_key": app_key,
                "application_title_zh": app_title_zh,
                "application_title_en": app_title_en,
                "featured_categories": featured_cats,
                "performance_ratings": ratings,
                "performance_descriptions_zh": desc_zh,
                "performance_descriptions_en": desc_en
            }

    # 3. 轉為 List 陣列格式，並執行「自動刪除無 Value 欄位」
    final_result = [clean_empty_values(p) for p in master_db.values()]

    # 寫入輸出的 JSON 檔
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(final_result, f, ensure_ascii=False, indent=2)

    print(f"✅ 合併且清理空值完成！已儲存至 '{output_filename}'。")

# 執行合併
if __name__ == "__main__":
    files_to_merge = {
        "ptfe": {"filename": "ptfe.json", "title_zh": "PTFE 取代", "title_en": "PTFE Alternative"},
        "powder": {"filename": "powder_coatings.json", "title_zh": "粉體塗料", "title_en": "Powder Coating"},
        "industrial": {"filename": "industrial_coatings.json", "title_zh": "工業塗料", "title_en": "Industrial Coating"},
        "ink": {"filename": "inks.json", "title_zh": "油墨", "title_en": "Energy Curable Inks & OPVs"},
        "industrial_floor": {"filename": "industrial_floor_coatings.json", "title_zh": "地板塗料", "title_en": "Industrial Floor Coatings"},
        "wood": {"filename": "wood.json", "title_zh": "木器漆", "title_en": "Wood Coatings"},
        "leather": {"filename": "leather_coatings.json", "title_zh": "皮革塗料", "title_en": "Leather Coatings"},
        "automotive_polishes": {"filename": "automotive_polishes.json", "title_zh": "汽車蠟", "title_en": "Automotive Polishes"}
    }

    merge_json_databases(files_to_merge)