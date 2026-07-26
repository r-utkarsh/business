"""
MedPlusMart product catalog downloader.

What this does:
- Fetches MedPlusMart's sitemap.xml (and any linked sub-sitemaps, like
  generalProducts.xml) to get a list of every product page URL.
- Extracts a readable product name from each URL.
- Saves everything into a CSV file you can open directly in Excel.

Run this on YOUR OWN computer, not in a cloud sandbox — the site blocks
requests that don't look like they're coming from a normal browser/location.

Before running:
    pip install requests beautifulsoup4 lxml

Usage:
    python medplus_catalog_scraper.py

Output:
    medplus_catalog.csv  (columns: product_name, brand_guess, product_url)

Notes on responsible use:
- This adds a small delay between requests so it doesn't hammer their
  servers. Please don't remove the delay or run multiple copies at once.
- This only reads publicly listed sitemap data (the same data Google uses
  to index the site) — it does not log in, place orders, or access
  anything private.
- Check https://www.medplusmart.com/robots.txt yourself before running,
  and stop using this if the site's terms change or if you get consistently
  blocked — that's the site telling you not to.
"""

import csv
import re
import time
import sys
import os
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.medplusmart.com"
SITEMAP_INDEX_CANDIDATES = [
    "/sitemap.xml",
    "/generalProducts.xml",
]
OUTPUT_FILE = "medplus_catalog.csv"
DELAY_SECONDS = 1.5  # be polite between requests

# Headers to look like a normal browser request, not a script.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def fetch(url, session):
    """Fetch a URL, return the raw text, or None on failure."""
    try:
        resp = session.get(url, headers=HEADERS, timeout=20)
        if resp.status_code == 200:
            return resp.text
        print(f"  [!] {url} returned status {resp.status_code}")
    except requests.RequestException as e:
        print(f"  [!] Failed to fetch {url}: {e}")
    return None


def find_sitemap_urls(xml_text, current_url):
    """Given sitemap XML text, return all <loc> URLs inside it."""
    soup = BeautifulSoup(xml_text, "xml")
    locs = [loc.get_text(strip=True) for loc in soup.find_all("loc")]
    # Resolve relative URLs just in case.
    return [urljoin(current_url, loc) for loc in locs]


def is_medplus_url(url):
    parsed = urlparse(url)
    return parsed.scheme == "https" and (parsed.hostname == "www.medplusmart.com" or parsed.hostname.endswith(".medplusmart.com"))


def spreadsheet_cell(value):
    value = str(value)
    return "'" + value if value.startswith(("=", "+", "-", "@")) else value


def slug_to_name(product_url):
    """
    Turn a URL like:
      .../product/a-cn-75gm-soap_a_cn0001
    into a readable product name like:
      "A Cn 75gm Soap"
    """
    slug = product_url.rstrip("/").split("/")[-1]
    # Drop trailing product-code suffix, e.g. "_a_cn0001" or "_AIR_0018"
    slug = re.sub(r"_[a-zA-Z0-9]+$", "", slug)
    words = slug.replace("_", "-").split("-")
    name = " ".join(w.capitalize() for w in words if w)
    return name


def collect_product_urls(session):
    """
    Walk the sitemap structure starting from likely entry points,
    following any nested sitemap files, and collect all /product/ URLs.
    """
    seen_sitemaps = set()
    to_visit = [urljoin(BASE_URL, path) for path in SITEMAP_INDEX_CANDIDATES]
    product_urls = set()

    while to_visit:
        url = to_visit.pop(0)
        if url in seen_sitemaps:
            continue
        seen_sitemaps.add(url)

        if not is_medplus_url(url):
            print(f"  [!] Skipping off-domain sitemap: {url}")
            continue
        print(f"Fetching sitemap: {url}")
        xml_text = fetch(url, session)
        time.sleep(DELAY_SECONDS)
        if not xml_text:
            continue

        found = find_sitemap_urls(xml_text, url)
        if not found:
            continue

        for loc in found:
            if is_medplus_url(loc) and "/product/" in urlparse(loc).path:
                product_urls.add(loc)
            elif is_medplus_url(loc) and urlparse(loc).path.endswith(".xml") and loc not in seen_sitemaps:
                to_visit.append(loc)

        print(f"  -> {len(found)} entries found so far, "
              f"{len(product_urls)} product URLs total")

    return sorted(product_urls)


def main():
    session = requests.Session()

    print("Step 1: collecting product URLs from sitemap(s)...")
    product_urls = collect_product_urls(session)

    if not product_urls:
        print(
            "\nNo product URLs found. This usually means the site blocked "
            "the request. Try:\n"
            "  - opening https://www.medplusmart.com/generalProducts.xml "
            "in your browser to confirm it still exists,\n"
            "  - waiting a while and trying again,\n"
            "  - or manually saving that XML page and pointing this script "
            "at the local file instead."
        )
        sys.exit(1)

    print(f"\nStep 2: found {len(product_urls)} product URLs. "
          f"Writing to {OUTPUT_FILE}...")

    temp_file = OUTPUT_FILE + ".tmp"
    with open(temp_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["product_name", "product_url"])
        for url in product_urls:
            name = slug_to_name(url)
            writer.writerow([spreadsheet_cell(name), spreadsheet_cell(url)])
    os.replace(temp_file, OUTPUT_FILE)

    print(f"Done. Saved {len(product_urls)} products to {OUTPUT_FILE}")
    print("Open this file in Excel, then filter/sort by brand or name "
          "to build your checklist.")


if __name__ == "__main__":
    main()
