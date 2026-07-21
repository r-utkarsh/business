"""
MedPlusMart catalog — brand grouping helper.

Takes the CSV produced by medplus_catalog_scraper.py (columns:
product_name, product_url) and adds a best-guess brand for each row,
then writes a new CSV sorted/grouped by that guessed brand.

How the brand is guessed, in order:
  1. The short code prefix hidden in the product URL slug (e.g. "avel"
     in avel0033) — products from the same brand tend to share this
     prefix, so rows with the same prefix are grouped together even if
     their names don't obviously match.
  2. The first word of the product name, as a human-readable brand label
     shown next to each group.

This is a rough first pass, not a finished brand list — it's meant to
make manual review and correction much faster than starting from a flat
89,000-row file. Expect to fix mislabeled rows by eye afterward.

Usage:
    python group_by_brand.py

Input:
    medplus_catalog.csv   (from the previous script)

Output:
    medplus_catalog_grouped.csv
        columns: guessed_brand_code, guessed_brand_name, product_name, product_url
        sorted so same-brand rows sit next to each other
"""

import csv
import re
import sys

INPUT_FILE = "medplus_catalog.csv"
OUTPUT_FILE = "medplus_catalog_grouped.csv"


def extract_code_prefix(product_url):
    """
    Pull the short alphabetic prefix from the trailing product code in the
    URL, e.g. '.../avel0033' -> 'avel', '.../a_cn0001' -> 'a_cn'.
    Falls back to empty string if no clear pattern is found.
    """
    slug = product_url.rstrip("/").split("/")[-1]
    match = re.search(r"([a-zA-Z_]+)\d+$", slug)
    if match:
        return match.group(1).lower().strip("_")
    return ""


def first_word_brand(product_name):
    """Use the first word of the product name as a readable brand guess."""
    words = product_name.strip().split()
    return words[0] if words else "Unknown"


def main():
    try:
        with open(INPUT_FILE, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except FileNotFoundError:
        print(f"Couldn't find {INPUT_FILE} — make sure it's in the same "
              f"folder as this script.")
        sys.exit(1)

    print(f"Loaded {len(rows)} products from {INPUT_FILE}")

    for row in rows:
        row["guessed_brand_code"] = extract_code_prefix(row["product_url"])
        row["guessed_brand_name"] = first_word_brand(row["product_name"])

    # Group same-code products next to each other; within a group, sort
    # by product name so it reads cleanly.
    rows.sort(key=lambda r: (r["guessed_brand_code"], r["product_name"]))

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "guessed_brand_code",
                "guessed_brand_name",
                "product_name",
                "product_url",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    unique_codes = len(set(r["guessed_brand_code"] for r in rows if r["guessed_brand_code"]))
    print(f"Done. Wrote {len(rows)} rows to {OUTPUT_FILE}")
    print(f"Found roughly {unique_codes} distinct brand-code groups.")
    print("Open this file in Excel, then scan down the "
          "'guessed_brand_code' column — same-brand products should now "
          "sit together, ready for you to rename/fix and build your "
          "checklist from.")


if __name__ == "__main__":
    main()