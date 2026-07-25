import csv
import json
import os
import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Referer": "https://www.medplusmart.com/"
}

# Trade line to Salt Map for USV / Ecosprin products
USV_SALT_MAP = {
    "ecosprin gold": "Aspirin 75 MG+Atorvastatin 10 MG+Clopidogrel 75 MG",
    "ecosprin av": "Aspirin 75 MG+Atorvastatin 10 MG",
    "ecosprin": "Aspirin (Acetylsalicylic Acid)",
    "glycomet gp star": "Glimepiride + Metformin SR",
    "glycomet trio": "Glimepiride 1 MG+Metformin 500 MG+Voglibose 0.2 MG",
    "glycomet gp": "Glimepiride 1 MG+Metformin 500 MG",
    "glycomet sr": "Metformin 500 MG (Sustained Release)",
    "glycomet": "Metformin Hydrochloride",
    "tazloc trio": "Amlodipine 5 MG+Chlorthalidone 12.5 MG+Telmisartan 40 MG",
    "tazloc am": "Amlodipine 5 MG+Telmisartan 40 MG",
    "tazloc ct": "Chlorthalidone 12.5 MG+Telmisartan 40 MG",
    "tazloc h": "Hydrochlorothiazide 12.5 MG+Telmisartan 40 MG",
    "tazloc beta": "Metoprolol Succinate 25 MG+Telmisartan 40 MG",
    "tazloc r": "Ramipril 2.5 MG+Telmisartan 40 MG",
    "tazloc": "Telmisartan 40 MG",
    "dytor plus": "Spironolactone 50 MG+Torsemide 10 MG",
    "dytor md": "Torsemide 10 MG (Mouth Dissolving)",
    "dytor e": "Eplerenone 25 MG+Torsemide 10 MG",
    "dytor": "Torsemide 10 MG",
    "erytop a": "Adapalene 0.1 %W/W+Clindamycin 1 %W/W",
    "erytop n": "Clindamycin 1 %W/W+Nicotinamide 4 %W/W",
    "erytop mist": "Clindamycin Phosphate 1 %W/V",
    "erytop": "Clindamycin Phosphate 1 %W/W",
    "triglycomet": "Glibenclamide 2.5 MG+Metformin 500 MG"
}

def get_salt(pname):
    plower = pname.lower()
    for key in sorted(USV_SALT_MAP.keys(), key=len, reverse=True):
        if key in plower:
            return USV_SALT_MAP[key]
    return "USV Prescription Healthcare"

def download_image(item):
    pname = item["name"]
    purl = item["url"]
    slug = re.sub(r'[^a-zA-Z0-9]+', '-', pname).strip('-').lower()
    img_filename = f"{slug}.jpg"
    img_filepath = os.path.join("product_images", img_filename)
    relative_img_path = f"product_images/{img_filename}"

    if os.path.exists(img_filepath) and os.path.getsize(img_filepath) > 5000:
        return pname, relative_img_path

    img_url = None
    try:
        req = urllib.request.Request(purl, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            matches = re.findall(r'(https?://static\d*\.medplusmart\.com/products/[^\s\'"]+?\.(?:jpg|png|webp|jpeg))', html, re.IGNORECASE)
            if matches:
                img_url = matches[0]
    except Exception as e:
        pass

    if img_url:
        try:
            img_req = urllib.request.Request(img_url, headers=HEADERS)
            with urllib.request.urlopen(img_req, timeout=10) as img_resp:
                img_data = img_resp.read()
                # Ensure it's not a generic placeholder
                if len(img_data) > 6000:
                    with open(img_filepath, "wb") as f:
                        f.write(img_data)
                    return pname, relative_img_path
        except Exception as e:
            pass

    return pname, ""

def main():
    print("Finding all Ecosprin & USV products in master catalog...")
    
    usv_items = []
    with open("medplus_catalog_grouped.csv", "r", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)
        for row in reader:
            pname = row.get("product_name", "").strip()
            purl = row.get("product_url", "").strip()
            plower = pname.lower()
            if any(k in plower for k in ["ecosprin", "glycomet", "tazloc", "dytor", "erytop", "triglycomet"]):
                trade = pname.split()[0]
                usv_items.append({"name": pname, "url": purl, "trade": trade})

    print(f"Found {len(usv_items)} Ecosprin & USV products!")

    os.makedirs("product_images", exist_ok=True)
    print("Downloading product pack photos concurrently...")

    image_map = {}
    with ThreadPoolExecutor(max_workers=10) as pool:
        futures = {pool.submit(download_image, item): item for item in usv_items}
        for future in as_completed(futures):
            pname, img_path = future.result()
            image_map[pname] = img_path

    # Build new product objects
    json_file = "shop_products_with_images.json"
    js_file = "product_data.js"
    csv_file = "shop_products.csv"

    existing_json = []
    if os.path.exists(json_file):
        with open(json_file, "r", encoding="utf-8") as f:
            existing_json = json.load(f)

    existing_names = {p["name"] for p in existing_json}
    added_count = 0

    for item in usv_items:
        pname = item["name"]
        if pname not in existing_names:
            img = image_map.get(pname, "")
            salt = get_salt(pname)
            existing_json.append({
                "name": pname,
                "brand": "USV",
                "trade": item["trade"],
                "image": img,
                "status": "downloaded" if img else "no_image",
                "salt": salt
            })
            added_count += 1
            existing_names.add(pname)

    existing_json.sort(key=lambda x: (x["brand"], x["name"]))

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(existing_json, f, indent=2, ensure_ascii=False)

    with open(js_file, "w", encoding="utf-8") as f:
        f.write("const shopProductsData = " + json.dumps(existing_json, ensure_ascii=False) + ";\n")

    # Also update shop_products.csv
    csv_rows = []
    for item in existing_json:
        csv_rows.append({
            "parent_brand": item["brand"],
            "product_name": item["name"],
            "trade_line": item.get("trade", item["brand"]),
            "product_url": ""
        })

    with open(csv_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["parent_brand", "product_name", "trade_line", "product_url"])
        writer.writeheader()
        writer.writerows(csv_rows)

    print(f"\nSuccessfully added {added_count} Ecosprin & USV products across all datasets!")
    print(f"Total products live in database: {len(existing_json):,}")

if __name__ == "__main__":
    main()
