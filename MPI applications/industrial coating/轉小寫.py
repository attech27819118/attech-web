import json


def convert_keys_to_lowercase(obj):
    """遞迴將所有字典的 key 轉換為小寫"""
    if isinstance(obj, dict):
        return {k.lower(): convert_keys_to_lowercase(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_keys_to_lowercase(element) for element in obj]
    else:
        return obj


# 讀取原始的 JSON 檔案
with open("industrial coatings.json", "r", encoding="utf-8") as f:

    data = json.load(f)

# 執行深層轉換
all_lower_data = convert_keys_to_lowercase(data)

# 將結果存回新的 JSON 檔案
with open("industrial_coatings2.json", "w", encoding="utf-8") as f:
    json.dump(all_lower_data, f, indent=2, ensure_ascii=False)

print("所有深層巢狀的 Key 已成功全部轉換為小寫！")