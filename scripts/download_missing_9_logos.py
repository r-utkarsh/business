import urllib.request
import json
import os

LOGODEV_TOKEN = "pk_Cb3LPnZgTEmi_ZiW9JSr2A"

missing_brands = [
    ("Amul", "amul.com", "logos/amul.png"),
    ("Apex Laboratories", "apexlab.com", "logos/apex-laboratories.png"),
    ("Bournvita", "bournvita.in", "logos/bournvita.png"),
    ("Complan", "complan.in", "logos/complan.png"),
    ("Hansaplast", "hansaplast.in", "logos/hansaplast.png"),
    ("MamyPoko", "mamypoko.co.in", "logos/mamypoko.png"),
    ("Pears", "pearssoap.com", "logos/pears.png"),
    ("Savlon", "savlon.in", "logos/savlon.png"),
    ("Sofy", "sofy.in", "logos/sofy.png"),
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

for name, domain, save_path in missing_brands:
    url = f"https://img.logo.dev/{domain}?token={LOGODEV_TOKEN}&size=200&format=png"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read()
            if len(data) > 500:
                with open(save_path, "wb") as f:
                    f.write(data)
                print(f"Downloaded logo for {name} ({len(data):,} bytes) -> {save_path}")
            else:
                print(f"Failed logo for {name}: image too small")
    except Exception as e:
        print(f"Error fetching logo for {name} ({domain}): {e}")

print("Done downloading missing brand logos!")
