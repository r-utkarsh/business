from scripts.allProd import is_medplus_url as sitemap_url, spreadsheet_cell
from scripts.download_product_images import product_from_row
from scripts.scrape_salts import is_medplus_url as salt_url


assert sitemap_url("https://www.medplusmart.com/sitemap.xml")
assert sitemap_url("https://static1.medplusmart.com/products/example.jpg")
assert not sitemap_url("https://medplusmart.com.attacker.example/product/x")
assert not salt_url("http://www.medplusmart.com/product/x")
assert spreadsheet_cell("=SUM(1,1)") == "'=SUM(1,1)"
assert spreadsheet_cell("Product name") == "Product name"
assert product_from_row({"product_name": "Test", "product_url": "https://www.medplusmart.com/product/test", "parent_brand": "Brand", "trade_line": "Trade"})
assert product_from_row({"product_name": "Test", "product_url": "https://attacker.example/product/test", "parent_brand": "Brand", "trade_line": "Trade"}) is None

print("security self-check passed")
