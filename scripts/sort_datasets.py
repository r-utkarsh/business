import json

def sort_all_datasets():
    print("Sorting products and brands alphabetically (A-Z)...")

    json_file = "shop_products_with_images.json"
    js_file = "product_data.js"

    with open(json_file, "r", encoding="utf-8") as f:
        products = json.load(f)

    # Sort products alphabetically by name (case-insensitive)
    products.sort(key=lambda x: x["name"].lower())

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

    with open(js_file, "w", encoding="utf-8") as f:
        f.write("const shopProductsData = " + json.dumps(products, ensure_ascii=False) + ";\n")

    print(f"Successfully sorted all {len(products)} products alphabetically A-Z!")

if __name__ == "__main__":
    sort_all_datasets()
