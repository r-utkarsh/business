import csv
import json
import os
import re
import urllib.request

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Referer": "https://www.medplusmart.com/"
}

eris_products = [
    {"name": "Dapanorm 10mg Tab", "url": "https://www.medplusmart.com/product/dapanorm-10mg-tab_dapa0007", "trade": "Dapanorm"},
    {"name": "Dapanorm 5mg Tab", "url": "https://www.medplusmart.com/product/dapanorm-5mg-tab_dapa0008", "trade": "Dapanorm"},
    {"name": "Dapanorm M 10mg Tab", "url": "https://www.medplusmart.com/product/dapanorm-m-10mg-tab_dapa0062", "trade": "Dapanorm"},
    {"name": "Dapanorm M 5mg Tab", "url": "https://www.medplusmart.com/product/dapanorm-m-5mg-tab_dapa0059", "trade": "Dapanorm"},
]

os.makedirs("product_images", exist_ok=True)

new_entries = []

for item in eris_products:
    pname = item["name"]
    purl = item["url"]
    ptrade = item["trade"]
    slug = re.sub(r'[^a-zA-Z0-9]+', '-', pname).strip('-').lower()
    img_filename = f"{slug}.jpg"
    img_filepath = os.path.join("product_images", img_filename)
    relative_img_path = f"product_images/{img_filename}"

    img_url = None
    try:
        req = urllib.request.Request(purl, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            matches = re.findall(r'(https?://static\d*\.medplusmart\.com/products/[^\s\'"]+?\.(?:jpg|png|webp|jpeg))', html, re.IGNORECASE)
            if matches:
                img_url = matches[0]
    except Exception as e:
        print(f"Error scraping {pname}: {e}")

    saved_img = ""
    if img_url:
        try:
            img_req = urllib.request.Request(img_url, headers=headers)
            with urllib.request.urlopen(img_req, timeout=10) as img_resp:
                img_data = img_resp.read()
                if len(img_data) > 500:
                    with open(img_filepath, "wb") as f:
                        f.write(img_data)
                    saved_img = relative_img_path
                    print(f"Downloaded image for {pname}: {len(img_data):,} bytes")
        except Exception as e:
            print(f"Error downloading image for {pname}: {e}")

    new_entries.append({
        "parent_brand": "Eris Lifesciences",
        "product_name": pname,
        "trade_line": ptrade,
        "product_url": purl,
        "image": saved_img
    })

# Add to shop_products.csv
csv_file = "shop_products.csv"
existing_csv = []
with open(csv_file, "r", encoding="utf-8") as f:
    existing_csv = list(csv.DictReader(f))

# Check if already present
for ne in new_entries:
    if not any(r["product_name"] == ne["product_name"] for r in existing_csv):
        existing_csv.append({
            "parent_brand": "Eris Lifesciences",
            "product_name": ne["product_name"],
            "trade_line": ne["trade_line"],
            "product_url": ne["product_url"]
        })

with open(csv_file, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["parent_brand", "product_name", "trade_line", "product_url"])
    writer.writeheader()
    writer.writerows(existing_csv)

# Add to JSON & JS dataset
json_file = "shop_products_with_images.json"
js_file = "product_data.js"

existing_json = []
if os.path.exists(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        existing_json = json.load(f)

for ne in new_entries:
    if not any(r["name"] == ne["product_name"] for r in existing_json):
        existing_json.append({
            "name": ne["product_name"],
            "brand": "Eris Lifesciences",
            "trade": ne["trade_line"],
            "image": ne["image"],
            "status": "downloaded" if ne["image"] else "no_image"
        })

existing_json.sort(key=lambda x: (x["brand"], x["name"]))

with open(json_file, "w", encoding="utf-8") as f:
    json.dump(existing_json, f, indent=2, ensure_ascii=False)

with open(js_file, "w", encoding="utf-8") as f:
    f.write("const shopProductsData = " + json.dumps(existing_json, ensure_ascii=False) + ";\n")

print(f"\nSuccessfully added {len(new_entries)} Dapanorm (Eris Lifesciences) products across all datasets!")
