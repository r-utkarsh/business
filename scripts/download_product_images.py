import csv
import os
import re
import json
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed

CSV_FILE = "shop_products.csv"
OUTPUT_DIR = "product_images"
OUTPUT_JS = "product_data.js"
OUTPUT_JSON = "shop_products_with_images.json"

os.makedirs(OUTPUT_DIR, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Referer": "https://www.medplusmart.com/"
}

def get_product_slug(name):
    return re.sub(r'[^a-zA-Z0-9]+', '-', name).strip('-').lower()

def scrape_and_download(row):
    pname = row["product_name"].strip()
    purl = row["product_url"].strip()
    pbrand = row["parent_brand"].strip()
    trade = row["trade_line"].strip()

    slug = get_product_slug(pname)
    img_filename = f"{slug}.jpg"
    img_filepath = os.path.join(OUTPUT_DIR, img_filename)
    relative_img_path = f"product_images/{img_filename}"

    # If image already exists and is non-empty, reuse it
    if os.path.exists(img_filepath) and os.path.getsize(img_filepath) > 500:
        return {
            "name": pname,
            "brand": pbrand,
            "trade": trade,
            "image": relative_img_path,
            "status": "existing"
        }

    img_url = None
    try:
        req = urllib.request.Request(purl, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            
            # Extract medplusmart image URL
            matches = re.findall(r'(https?://static\d*\.medplusmart\.com/products/[^\s\'"]+?\.(?:jpg|png|webp|jpeg))', html, re.IGNORECASE)
            if matches:
                img_url = matches[0]
            else:
                # Fallback to any medplusmart product image link
                matches2 = re.findall(r'(https?://[^\s\'"]+?/products/[^\s\'"]+?\.(?:jpg|png|webp|jpeg))', html, re.IGNORECASE)
                if matches2:
                    img_url = matches2[0]
    except Exception as e:
        pass

    if img_url:
        try:
            img_req = urllib.request.Request(img_url, headers=headers)
            with urllib.request.urlopen(img_req, timeout=10) as img_resp:
                img_data = img_resp.read()
                if len(img_data) > 500:
                    with open(img_filepath, "wb") as f:
                        f.write(img_data)
                    return {
                        "name": pname,
                        "brand": pbrand,
                        "trade": trade,
                        "image": relative_img_path,
                        "status": "downloaded"
                    }
        except Exception:
            pass

    return {
        "name": pname,
        "brand": pbrand,
        "trade": trade,
        "image": "",  # Fallback to Brand Logo / Category Icon on website
        "status": "no_image"
    }

def main():
    products = []
    with open(CSV_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        products = list(reader)

    print(f"Starting image scraper for {len(products):,} verified in-stock products...")

    results = []
    downloaded_count = 0
    existing_count = 0
    fallback_count = 0

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(scrape_and_download, row) for row in products]
        for future in as_completed(futures):
            res = future.result()
            results.append(res)
            if res["status"] == "downloaded":
                downloaded_count += 1
            elif res["status"] == "existing":
                existing_count += 1
            else:
                fallback_count += 1

    # Sort results by brand then name
    results.sort(key=lambda x: (x["brand"], x["name"]))

    # Save to JSON
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # Save to JS file for frontend inclusion
    with open(OUTPUT_JS, "w", encoding="utf-8") as f:
        f.write("const shopProductsData = " + json.dumps(results, ensure_ascii=False) + ";\n")

    print("\n=======================================================")
    print("PRODUCT IMAGE DOWNLOAD & INTEGRATION COMPLETE")
    print("=======================================================")
    print(f"Total Products Processed: {len(results):,}")
    print(f"  [Downloaded Images]: {downloaded_count:,}")
    print(f"  [Reused Images]:     {existing_count:,}")
    print(f"  [Fallback Logos]:    {fallback_count:,}")
    print(f"\nGenerated files:")
    print(f"  - Images directory: {OUTPUT_DIR}/")
    print(f"  - JS Dataset:       {OUTPUT_JS}")
    print(f"  - JSON Dataset:     {OUTPUT_JSON}")

if __name__ == "__main__":
    main()
