"""
Match guessed brand names to their real parent company, using a curated
reference list (known_brand_parents.csv) rather than guesswork.

Why this approach:
There's no single public database that reliably maps every trade name to
its manufacturer, so this script does NOT try to invent a match for every
row. It only fills in a parent company when the brand name is found in
the curated reference list you can see and edit yourself. Everything else
is left blank on purpose, so you know exactly which entries still need a
human look.

Usage:
    python match_brand_parents.py

Inputs (must be in the same folder):
    unique_brands_summary.csv     columns: guessed_brand_name, product_count, ...
    known_brand_parents.csv       columns: brand_name, parent_company, source_note

Output:
    brand_parent_matches.csv
        columns: guessed_brand_name, product_count, parent_company,
                 source_note, match_type
        match_type is one of: "exact", "normalized", "" (no match)
"""

import csv
import re
import sys

BRANDS_FILE = "unique_brands_summary.csv"
REFERENCE_FILE = "known_brand_parents.csv"
OUTPUT_FILE = "brand_parent_matches.csv"


def normalize(name):
    """
    Lowercase, strip punctuation/spacing differences so 'Dr Reddy's' and
    'dr. reddys' can still match each other.
    """
    name = name.lower().strip()
    name = re.sub(r"[.\-']", "", name)
    name = re.sub(r"\s+", " ", name)
    return name


def load_reference(path):
    """Load the curated list into two lookup dicts: exact and normalized."""
    exact = {}
    normalized = {}
    try:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                brand = row["brand_name"].strip()
                exact[brand] = row
                normalized[normalize(brand)] = row
    except FileNotFoundError:
        print(f"Couldn't find {path} — put it in the same folder as this script.")
        sys.exit(1)
    return exact, normalized


def main():
    exact_lookup, normalized_lookup = load_reference(REFERENCE_FILE)
    print(f"Loaded {len(exact_lookup)} known brand-to-parent mappings.")

    try:
        with open(BRANDS_FILE, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            brand_rows = [
                row for row in reader
                if row.get("guessed_brand_name", "").strip()
            ]
    except FileNotFoundError:
        print(f"Couldn't find {BRANDS_FILE} — put it in the same folder as this script.")
        sys.exit(1)

    print(f"Loaded {len(brand_rows)} guessed brand names to check.")

    matched = 0
    output_rows = []

    for row in brand_rows:
        guessed = row.get("guessed_brand_name", "").strip()
        parent_company = ""
        source_note = ""
        match_type = ""

        if guessed in exact_lookup:
            ref = exact_lookup[guessed]
            parent_company = ref["parent_company"]
            source_note = ref["source_note"]
            match_type = "exact"
        else:
            norm = normalize(guessed)
            if norm in normalized_lookup:
                ref = normalized_lookup[norm]
                parent_company = ref["parent_company"]
                source_note = ref["source_note"]
                match_type = "normalized"

        if match_type:
            matched += 1

        output_rows.append({
            "guessed_brand_name": guessed,
            "product_count": row.get("product_count", ""),
            "parent_company": parent_company,
            "source_note": source_note,
            "match_type": match_type,
        })

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "guessed_brand_name",
                "product_count",
                "parent_company",
                "source_note",
                "match_type",
            ],
        )
        writer.writeheader()
        writer.writerows(output_rows)

    print(f"\nDone. Matched {matched} of {len(brand_rows)} brand names "
          f"({matched / len(brand_rows) * 100:.1f}%).")
    print(f"Results saved to {OUTPUT_FILE}")
    print(
        "\nEverything left blank simply means it wasn't in the curated "
        "reference list yet. To improve coverage over time, open "
        f"{REFERENCE_FILE} and add rows for brands you recognize — the "
        "script will pick them up automatically on the next run."
    )


if __name__ == "__main__":
    main()
