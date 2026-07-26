import json
import re

def update_app_js():
    with open("app.js", "r", encoding="utf-8") as f:
        content = f.read()

    # Add missing entries to brandData
    new_brand_entries = [
        '  {name:"Amul",logo:"logos/amul.png"},',
        '  {name:"Apex Laboratories",logo:"logos/apex-laboratories.png"},',
        '  {name:"Bournvita",logo:"logos/bournvita.png"},',
        '  {name:"Complan",logo:"logos/complan.png"},',
        '  {name:"Hansaplast",logo:"logos/hansaplast.png"},',
        '  {name:"MamyPoko",logo:"logos/mamypoko.png"},',
        '  {name:"Nestle India Ltd",logo:"logos/nestl-health-science-india.png"},',
        '  {name:"Pears",logo:"logos/pears.png"},',
        '  {name:"Savlon",logo:"logos/savlon.png"},',
        '  {name:"Sofy",logo:"logos/sofy.png"},'
    ]

    # Insert into brandData
    insert_marker = 'const brandData = ['
    if insert_marker in content:
        content = content.replace(insert_marker, insert_marker + "\n" + "\n".join(new_brand_entries))

    # Add fuzzy getBrandLogo helper
    fuzzy_helper = """
function getBrandLogo(brandName) {
  if (!brandName) return '';
  if (brandLogoMap[brandName]) return brandLogoMap[brandName];
  
  const norm = brandName.toLowerCase().replace(/[^a-z0-9]/g, '');
  for (const b in brandLogoMap) {
    const bNorm = b.toLowerCase().replace(/[^a-z0-9]/g, '');
    if (bNorm && (norm.includes(bNorm) || bNorm.includes(norm))) {
      return brandLogoMap[b];
    }
  }
  return '';
}
"""

    if "function getBrandLogo" not in content:
        content = content.replace("const brandLogoMap = {};", "const brandLogoMap = {};\n" + fuzzy_helper)

    # Update productCard to use getBrandLogo(p.brand)
    content = content.replace("const logo = brandLogoMap[p.brand];", "const logo = getBrandLogo(p.brand);")

    with open("app.js", "w", encoding="utf-8") as f:
        f.write(content)

    print("Updated app.js with missing brand entries and smart fuzzy getBrandLogo helper!")

if __name__ == "__main__":
    update_app_js()
