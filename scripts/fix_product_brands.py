import csv
import json
import os
import re

def fix_all_datasets():
    print("Fixing Neo Mercazole and brand overrides...")

    # 1. Update shop_products.csv
    csv_file = "shop_products.csv"
    updated_csv_rows = []
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            pname = row["product_name"]
            pbrand = row["parent_brand"]
            ptrade = row["trade_line"]
            purl = row["product_url"]

            if "mercazole" in pname.lower():
                pbrand = "Abbott India"
                ptrade = "Neo Mercazole"

            updated_csv_rows.append({
                "parent_brand": pbrand,
                "product_name": pname,
                "trade_line": ptrade,
                "product_url": purl
            })

    with open(csv_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["parent_brand", "product_name", "trade_line", "product_url"])
        writer.writeheader()
        writer.writerows(updated_csv_rows)

    # 2. Update shop_products_with_images.json
    json_file = "shop_products_with_images.json"
    if os.path.exists(json_file):
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        for item in data:
            if "mercazole" in item["name"].lower():
                item["brand"] = "Abbott India"
                item["trade"] = "Neo Mercazole"

        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        # 3. Update product_data.js
        js_file = "product_data.js"
        with open(js_file, "w", encoding="utf-8") as f:
            f.write("const shopProductsData = " + json.dumps(data, ensure_ascii=False) + ";\n")

    print("Successfully fixed Neo Mercazole brand to Abbott India across all datasets!")

if __name__ == "__main__":
    fix_all_datasets()
