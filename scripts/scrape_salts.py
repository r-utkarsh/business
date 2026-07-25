"""
Scrape real salt/composition from MedPlus product pages using Schema.org
structured data ('activeIngredient' field in JSON-LD).
Updates shop_products_with_images.json and product_data.js.
"""
import json, os, re, time, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Referer': 'https://www.medplusmart.com/'
}

def extract_salt(url):
    """Fetch a MedPlus product page and extract activeIngredient from JSON-LD."""
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=12) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
        # Extract activeIngredient from JSON-LD schema
        m = re.search(r'"activeIngredient"\s*:\s*"([^"]+)"', html)
        if m:
            return m.group(1).strip()
        # Fallback: try og:description composition
        m2 = re.search(r'composition\(formula\) of ([^"]+?)\.', html)
        if m2:
            return m2.group(1).strip()
    except Exception as e:
        pass
    return None


def main():
    json_file = "shop_products_with_images.json"
    js_file = "product_data.js"

    with open(json_file, "r", encoding="utf-8") as f:
        products = json.load(f)

    # Build work list: only products that have a medplusmart URL
    work = []
    for i, p in enumerate(products):
        url = p.get("url", "")
        if not url:
            # Try to find URL from shop_products.csv
            continue
        work.append((i, p["name"], url))

    # Also load URLs from shop_products.csv
    import csv
    url_map = {}
    with open("shop_products.csv", "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            url_map[row["product_name"]] = row["product_url"]

    # Fill in missing URLs
    for i, p in enumerate(products):
        if not p.get("url") and p["name"] in url_map:
            products[i]["url"] = url_map[p["name"]]

    # Rebuild work list
    work = []
    for i, p in enumerate(products):
        url = p.get("url", "")
        if url and "medplusmart.com" in url:
            work.append((i, p["name"], url))

    print(f"Total products: {len(products)}")
    print(f"Products with MedPlus URLs: {len(work)}")
    print(f"Starting salt scrape with 8 threads...\n")

    scraped = 0
    failed = 0
    skipped_no_url = len(products) - len(work)

    def fetch(item):
        idx, name, url = item
        salt = extract_salt(url)
        return idx, name, salt

    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = {pool.submit(fetch, item): item for item in work}
        for i, future in enumerate(as_completed(futures)):
            idx, name, salt = future.result()
            if salt:
                products[idx]["salt_verified"] = salt
                scraped += 1
            else:
                failed += 1

            if (i + 1) % 50 == 0:
                print(f"  Progress: {i+1}/{len(work)} scraped ({scraped} found, {failed} failed)")

    print(f"\nDone! Scraped: {scraped}, Failed: {failed}, No URL: {skipped_no_url}")

    # Update salt field: prefer verified over manual
    updated = 0
    for p in products:
        verified = p.get("salt_verified", "")
        if verified:
            p["salt"] = verified
            updated += 1
        # Clean up temp field
        if "salt_verified" in p:
            del p["salt_verified"]
        # Clean up url field (don't need it in frontend JS)
        if "url" in p:
            del p["url"]

    print(f"Updated {updated} products with verified salt from MedPlus")

    # Save
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

    with open(js_file, "w", encoding="utf-8") as f:
        f.write("const shopProductsData = " + json.dumps(products, ensure_ascii=False) + ";\n")

    # Show some examples
    print("\nSample verified salts:")
    count = 0
    for p in products:
        if p.get("salt") and count < 15:
            print(f"  {p['name']}: {p['salt']}")
            count += 1

if __name__ == "__main__":
    main()
