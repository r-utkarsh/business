import json
import os

def check_product_logos():
    with open("shop_products_with_images.json", "r", encoding="utf-8") as f:
        products = json.load(f)

    # Read brandData from app.js
    with open("app.js", "r", encoding="utf-8") as f:
        app_js = f.read()

    # Extract logos in app.js
    brand_logo_map = {}
    import re
    matches = re.findall(r'\{name:"([^"]+)",logo:"([^"]+)"\}', app_js)
    for bname, logo in matches:
        brand_logo_map[bname] = logo

    print(f"Total brands in brand_logo_map: {len(brand_logo_map)}")

    missing_logo_brands = set()
    total_products = len(products)
    products_without_logo = 0

    for p in products:
        pbrand = p["brand"]
        if pbrand not in brand_logo_map:
            missing_logo_brands.add(pbrand)
            products_without_logo += 1

    print(f"\nProducts with unmapped brand string: {products_without_logo} / {total_products}")
    print("Unmapped Brand Strings:")
    for b in sorted(missing_logo_brands):
        print(f"  - '{b}'")

if __name__ == "__main__":
    check_product_logos()
