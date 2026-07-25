import json
import os
import hashlib

def remove_placeholder_images():
    print("Finding and removing MedPlus generic placeholder graphics...")

    # Known MD5 hashes of MedPlus generic placeholder graphics
    PLACEHOLDER_HASHES = {
        '38ad50764a678a4f8421e8cac2cda553', # Generic Tablet Bottle graphic
        '00755e0d92ba48545bc7aaae052325a9', # Generic Syrup Bottle graphic
        '170b4daf9a2ac8001ca2e51455159a88', # Generic Blister Pack graphic
        '581964ee3b55a948c3374115b750b2bf', # Generic Ointment/Tube graphic
        '5ff619b149245951f5354b5a1d16a1fd', # Generic Eye Drops graphic
        '1621938c4d4cdb5b3bf1d30084714ed5', # Generic Respules/Inhaler graphic
    }

    # Identify files to remove
    deleted_files = set()
    img_dir = "product_images"

    if os.path.exists(img_dir):
        for filename in os.listdir(img_dir):
            filepath = os.path.join(img_dir, filename)
            if os.path.isfile(filepath):
                with open(filepath, 'rb') as f:
                    file_hash = hashlib.md5(f.read()).hexdigest()
                if file_hash in PLACEHOLDER_HASHES:
                    try:
                        os.remove(filepath)
                        deleted_files.add(f"product_images/{filename}")
                    except Exception as e:
                        print(f"Error removing {filename}: {e}")

    print(f"Removed {len(deleted_files)} generic placeholder image files from disk.")

    # Update shop_products_with_images.json & product_data.js
    json_file = "shop_products_with_images.json"
    js_file = "product_data.js"

    with open(json_file, "r", encoding="utf-8") as f:
        products = json.load(f)

    cleaned_count = 0
    for p in products:
        if p.get("image") in deleted_files:
            p["image"] = ""
            p["status"] = "no_image"
            cleaned_count += 1

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

    with open(js_file, "w", encoding="utf-8") as f:
        f.write("const shopProductsData = " + json.dumps(products, ensure_ascii=False) + ";\n")

    print(f"Updated {cleaned_count} products to use their Brand Logo instead of generic bottle graphics!")

if __name__ == "__main__":
    remove_placeholder_images()
