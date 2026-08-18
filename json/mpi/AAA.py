import json

input_file = "mpiall.json"
output_file = "mpiall.json"

# 1. 讀取 JSON 檔案
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# 2. 遍歷每個產品底下的所有 application，並在 featured_categories 後插入 example: ""
for product in data:
    apps_data = product.get("applications_data", {})

    for app_key, app_val in apps_data.items():
        if isinstance(app_val, dict):
            new_app = {}
            for k, v in app_val.items():
                new_app[k] = v
                # 當遇到 featured_categories 時，緊接著插入空字串 example
                if k == "featured_categories":
                    new_app["example"] = ""

            # 若原本沒有 featured_categories，也可以直接補在最後
            if "example" not in new_app:
                new_app["example"] = ""

            apps_data[app_key] = new_app

# 3. 儲存檔案
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"處理完成！已儲存至 {output_file}")