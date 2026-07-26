import csv
import os
import re
import json
import urllib.request
import urllib.parse
import time
import random
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse

logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")

CSV_FILE = "shop_products.csv"
OUTPUT_DIR = "product_images"
OUTPUT_JS = "product_data.js"
OUTPUT_JSON = "shop_products_with_images.json"
REQUEST_DELAY_RANGE = (0.5, 1.5)

os.makedirs(OUTPUT_DIR, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Referer": "https://www.medplusmart.com/"
}

def get_product_slug(name):
    return re.sub(r'[^a-zA-Z0-9]+', '-', name).strip('-').lower()

def is_medplus_url(url):
    parsed = urlparse(url)
    return parsed.scheme == "https" and (parsed.hostname == "www.medplusmart.com" or parsed.hostname.endswith(".medplusmart.com"))

def product_from_row(row):
    fields = ("product_name", "product_url", "parent_brand", "trade_line")
    if not isinstance(row, dict) or any(not isinstance(row.get(field), str) or not row[field].strip() for field in fields):
        logging.warning("Skipping CSV row with missing required fields")
        return None
    if not is_medplus_url(row["product_url"].strip()):
        logging.warning("Skipping non-MedPlus product URL")
        return None
    return tuple(row[field].strip() for field in fields)

def write_catalog(results):
    json_temp = OUTPUT_JSON + ".tmp"
    js_temp = OUTPUT_JS + ".tmp"
    with open(json_temp, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    with open(js_temp, "w", encoding="utf-8") as f:
        f.write("const shopProductsData = " + json.dumps(results, ensure_ascii=False) + ";\n")
    os.replace(json_temp, OUTPUT_JSON)
    os.replace(js_temp, OUTPUT_JS)

def scrape_and_download(row):
    product = product_from_row(row)
    if not product:
        return None
    pname, purl, pbrand, trade = product

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
            "image": relative_img_path
        }

    time.sleep(random.uniform(*REQUEST_DELAY_RANGE))
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
        logging.warning("Failed to fetch page for %s: %s", pname, e)

    if img_url and is_medplus_url(img_url):
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
                        "image": relative_img_path
                    }
        except Exception as e:
            logging.warning("Failed to download image for %s: %s", pname, e)

    return {
        "name": pname,
        "brand": pbrand,
        "trade": trade,
        "image": ""  # Fallback to Brand Logo / Category Icon on website
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

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(scrape_and_download, row) for row in products]
        for future in as_completed(futures):
            try:
                res = future.result()
            except Exception:
                logging.exception("Skipping product after scraper failure")
                continue
            if not res:
                continue
            results.append(res)
            if res["image"] and not os.path.exists(res["image"].replace("product_images/", "product_images\\")):
                downloaded_count += 1
            elif res["image"]:
                existing_count += 1
            else:
                fallback_count += 1

    # Sort results by brand then name
    results.sort(key=lambda x: (x["brand"], x["name"]))

    write_catalog(results)

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
