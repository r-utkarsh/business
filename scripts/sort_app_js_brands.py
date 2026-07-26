import re

def sort_app_js():
    with open("app.js", "r", encoding="utf-8") as f:
        content = f.read()

    # Insert brandData.sort line
    sort_line = "brandData.sort((a,b) => a.name.localeCompare(b.name));\n"
    if "brandData.sort" not in content:
        content = content.replace("const brands = brandData.map(b => b.name);", sort_line + "const brands = brandData.map(b => b.name);")

    # Update featuredBrands to pick popular brands
    featured_code = "$('featuredBrands').innerHTML = ['Dabur India', 'Himalaya', 'Abbott India', 'Cipla', 'Mankind Pharma', 'Sun Pharmaceutical'].filter(b=>brands.includes(b)).map(brandCard).join('');"
    content = re.sub(r"\$\('featuredBrands'\)\.innerHTML\s*=\s*brands\.slice\(0,6\)\.map\(brandCard\)\.join\(''\);", featured_code, content)

    with open("app.js", "w", encoding="utf-8") as f:
        f.write(content)

    print("Updated app.js with alphabetical sorting for brandData & clean Featured Brands!")

if __name__ == "__main__":
    sort_app_js()
