import json
import re
import os

BRAND_ALIAS_MAP = {
    "Nestle India Ltd": "Nestlé Health Science India",
    "Nestle": "Nestlé Health Science India",
    "Nestlé": "Nestlé Health Science India",
    "Amul": "Amul",
    "Apex Laboratories Pvt Ltd": "Apex Laboratories",
    "Bournvita": "Bournvita",
    "Centaur Pharmaceuticals Pvt Ltd": "Centaur Pharmaceuticals",
    "Complan": "Complan",
    "Dynaglipt": "Eris Lifesciences",
    "Dynapar": "Troikaa Pharmaceuticals",
    "Godrej Consumer Products": "Godrej Products",
    "Haleon (formerly GSK Consumer Healthcare)": "GSK India",
    "Hamdard": "Hamdard Dawakhana",
    "Hansaplast": "Hansaplast",
    "J.B. Chemicals & Pharmaceuticals": "JB. Chemicals & Pharmaceuticals",
    "Khadirarishta": "Baidyanath Jhansi",
    "MamyPoko": "MamyPoko",
    "Mamy Poko": "MamyPoko",
    "Pears": "Pears",
    "Pfizer Ltd": "Pfizer India",
    "Reckitt Benckiser (India) Ltd": "Reckitt",
    "Savlon": "Savlon",
    "Sofy": "Sofy",
    "Sun Pharmaceutical Industries": "Sun Pharmaceutical",
    "Win-Medicare Pvt Ltd": "Win-Medicare",
    "Zydus Wellness Ltd": "Zydus Wellness"
}

def update_brand_names():
    json_file = "shop_products_with_images.json"
    js_file = "product_data.js"
    csv_file = "shop_products.csv"

    with open(json_file, "r", encoding="utf-8") as f:
        products = json.load(f)

    updated_count = 0
    for p in products:
        b = p["brand"]
        if b in BRAND_ALIAS_MAP:
            p["brand"] = BRAND_ALIAS_MAP[b]
            updated_count += 1

    print(f"Standardized brand names for {updated_count} products in JSON/JS.")

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

    with open(js_file, "w", encoding="utf-8") as f:
        f.write("const shopProductsData = " + json.dumps(products, ensure_ascii=False) + ";\n")

if __name__ == "__main__":
    update_brand_names()
