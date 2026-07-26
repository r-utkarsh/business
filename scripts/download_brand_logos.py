import csv
import json
import os
import re
import urllib.parse
import urllib.request
import time
import logging

logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")

ENV_FILE = ".env"
BRAND_FILE = "selected_brands.csv"
EXCLUSION_FILE = "brand_exclusions.csv"
OUTPUT_DIR = "logos"

# Known wrong matches from Brandfetch that we need to fix
WRONG_DOMAINS = {
    "P&G": "pg.com",           # was google.com
    "HIT": "godrejhit.com",    # was hitachi.com
    "Whisper": "whisper.com",  # was whisperinghomes.com
    "Livon": "marico.com",     # was livongo.com (Livon is a Marico brand)
    "FDC": "fdcindia.com",     # was fdc.org.br
    "Micro Labs": "microlabsltd.com",  # was microlabs.com.ua
    "USV": "usv.in",           # was usv.ro
    "Parachute": "marico.com", # Parachute is a Marico brand
}

# Manual domain mappings for brands Brandfetch couldn't find
MANUAL_DOMAINS = {
    "Abbott India": "abbott.com",
    "Aristo Pharmaceuticals": "aristopharma.com",
    "Baidyanath Jhansi": "baidyanath.co.in",
    "Bayer Pharmaceuticals": "bayer.com",
    "Charak Pharma": "charakpharma.com",
    "Cinthol": "godrejcp.com",
    "Dawakhana Tibbiya College": None,  # Very niche, skip
    "Dr. Willmar Schwabe India": "schwabeindia.com",
    "East India Pharmaceutical Works": None,  # Very niche
    "Eris Lifesciences": "erislifesciences.com",
    "Fair & Lovely": "glowandlovely.in",
    "Fair and Handsome": "fairandhandsome.in",
    "Franco-Indian Pharmaceuticals": None,
    "Fulford India": None,
    "GSK India": "gsk.com",
    "Galderma India": "galderma.com",
    "Glow & Lovely": "glowandlovely.in",
    "Godrej No. 1": "godrejcp.com",
    "Hamdard Dawakhana": "hamdard.in",
    "Hindustan Antibiotics": None,
    "Ind-Swift Laboratories": "indswiftlabs.com",
    "J.B. Chemicals & Pharmaceuticals": "jbcpl.com",
    "JB Chemicals & Pharmaceuticals": "jbcpl.com",
    "Jubilant Generics": "jubilantpharma.com",
    "Macleods Pharmaceuticals": "macleodspharma.com",
    "Merck India": "merck.com",
    "Meswak": "dabur.com",  # Meswak is a Dabur brand
    "Meyer Organics": "meyerorganics.com",
    "Nestlé Health Science India": "nestle.com",
    "Nihar Naturals": "marico.com",  # Nihar is a Marico brand
    "Plethico Pharmaceuticals": None,
    "Sandoz India": "sandoz.com",
    "Sun Pharmaceutical Industries": "sunpharma.com",
    "Torrent Pharmaceuticals": "torrentpharma.com",
    "Troikaa Pharmaceuticals": "troikaapharma.com",
    "Vicco Laboratories": "viccolabs.com",
    "Win-Medicare": "winmedicare.com",
}

def get_client_id():
    with open(ENV_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("BRANDFETCH_CLIENT_ID="):
                return line.split("=", 1)[1].strip().strip('"')
    return ""

def normalize(name):
    return re.sub(r'[^a-z0-9]', '', name.lower())

def is_safe_domain(domain):
    """Allow only plain hostnames — no IPs, no paths, no internal addresses."""
    return bool(re.fullmatch(r'[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z]{2,})+', domain))

def search_domain_brandfetch(brand_name, client_id):
    """Use Brandfetch search to find the domain for a brand."""
    if not client_id:
        return None
    query = urllib.parse.quote(brand_name)
    url = f"https://api.brandfetch.io/v2/search/{query}?c={client_id}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            candidates = json.loads(resp.read().decode("utf-8"))
        if candidates:
            norm = normalize(brand_name)
            # Exact match first
            for c in candidates:
                if normalize(c.get("name", "")) == norm:
                    return c.get("domain")
            # Stem match
            for c in candidates:
                cn = normalize(c.get("name", ""))
                if len(cn) >= 3 and (norm.startswith(cn) or cn.startswith(norm)):
                    return c.get("domain")
            # Top result
            return candidates[0].get("domain")
    except Exception as e:
        logging.warning("Brandfetch search failed for %s: %s", brand_name, e)
    return None

def download_hunter_logo(domain, filepath):
    """Download logo from Hunter.io."""
    url = f"https://logos.hunter.io/{domain}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = resp.read()
        ct = resp.headers.get("Content-Type", "")
        # Verify it's actually an image
        if not ct.startswith("image/") and data[:4] != b'\x89PNG' and data[:3] != b'\xff\xd8\xff':
            raise ValueError(f"Not an image: {ct}")
        # Determine extension from content type
        ext = ".png"
        if "jpeg" in ct or "jpg" in ct:
            ext = ".jpg"
        elif "svg" in ct:
            raise ValueError("SVG logos are not accepted (may contain scripts)")
        elif "webp" in ct:
            ext = ".webp"
        # Update filepath extension if needed
        base = os.path.splitext(filepath)[0]
        filepath = base + ext
        with open(filepath, "wb") as f:
            f.write(data)
    return filepath, len(data)

def main():
    client_id = get_client_id()

    # Load exclusions
    excluded = set()
    if os.path.exists(EXCLUSION_FILE):
        with open(EXCLUSION_FILE, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row.get("excluded_name"):
                    excluded.add(row["excluded_name"])

    # Load brands
    brands = []
    with open(BRAND_FILE, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            b = row.get("brand", "").strip()
            if b and b not in excluded:
                brands.append(b)
    brands.sort()

    # Load existing Brandfetch domain results (reuse correct ones)
    bf_domains = {}
    if os.path.exists("logo_results.csv"):
        with open("logo_results.csv", "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row.get("domain"):
                    bf_domains[row["brand"]] = row["domain"]

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Clean out old broken Brandfetch HTML files
    cleaned = 0
    for fname in os.listdir(OUTPUT_DIR):
        fpath = os.path.join(OUTPUT_DIR, fname)
        if fname.endswith(".svg") and os.path.getsize(fpath) == 489805:
            os.remove(fpath)
            cleaned += 1
    if cleaned:
        print(f"Cleaned {cleaned} broken Brandfetch HTML files from logos/")

    results = []
    missing = []

    print(f"Downloading logos for {len(brands)} brands via Hunter.io...\n")

    for name in brands:
        slug = re.sub(r'[^a-zA-Z0-9]+', '-', name).strip('-').lower()
        # Check if already downloaded (real image)
        existing = None
        for ext in [".png", ".jpg", ".svg", ".webp"]:
            p = os.path.join(OUTPUT_DIR, slug + ext)
            if os.path.exists(p) and os.path.getsize(p) > 0:
                # Verify it's not an HTML file
                with open(p, "rb") as chk:
                    head = chk.read(15)
                if not head.startswith(b'<!DOCTYPE') and not head.startswith(b'<html'):
                    existing = p
                    break

        if existing:
            results.append({"brand": name, "status": "existing", "domain": "", "file": existing})
            continue

        # Determine domain
        domain = None
        if name in WRONG_DOMAINS:
            domain = WRONG_DOMAINS[name]
        elif name in MANUAL_DOMAINS:
            domain = MANUAL_DOMAINS[name]
        elif name in bf_domains and name not in WRONG_DOMAINS:
            domain = bf_domains[name]

        # If still no domain, try Brandfetch search
        if not domain and client_id:
            domain = search_domain_brandfetch(name, client_id)

        if not domain:
            missing.append({"brand": name, "reason": "No domain found", "domain": ""})
            print(f"  [SKIP] {name}: no domain")
            continue

        if not is_safe_domain(domain):
            missing.append({"brand": name, "reason": f"Unsafe domain rejected: {domain}", "domain": domain})
            print(f"  [SKIP] {name}: unsafe domain '{domain}'")
            continue

        # Download from Hunter.io
        target = os.path.join(OUTPUT_DIR, slug + ".png")
        try:
            filepath, size = download_hunter_logo(domain, target)
            results.append({"brand": name, "status": "downloaded", "domain": domain, "file": filepath})
            print(f"  [OK] {name} -> {domain} ({size:,} bytes)")
            time.sleep(0.3)  # Be polite to Hunter.io
        except Exception as e:
            missing.append({"brand": name, "reason": str(e), "domain": domain})
            print(f"  [FAIL] {name} ({domain}): {e}")

    # Write results
    with open("logo_results.csv", "w", newline="", encoding="utf-8") as rf:
        writer = csv.DictWriter(rf, fieldnames=["brand", "status", "domain", "file"])
        writer.writeheader()
        writer.writerows(results)

    with open("missing_logos.csv", "w", newline="", encoding="utf-8") as mf:
        writer = csv.DictWriter(mf, fieldnames=["brand", "reason", "domain"])
        writer.writeheader()
        writer.writerows(missing)

    print(f"\nDone! Downloaded/Reused: {len(results)}, Needs review: {len(missing)}")

if __name__ == "__main__":
    main()
