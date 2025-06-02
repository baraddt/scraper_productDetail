from excel.reader import get_links_from_excel
from tools.scraper_playwright import scrape_product
from utils.tools import get_platform_from_url
from core.parser import parse_response
from excel.insert_results import append_rows_to_excel
import json

EXCEL_INPUT = "python/data/produk.xlsx"
EXCEL_OUTPUT = "python/output/hasil.xlsx"


def main():
    links = get_links_from_excel(EXCEL_INPUT)
    for url in links:
        platform = get_platform_from_url(url)
        if platform == "unknown":
            print(f"Platform tidak dikenali untuk URL: {url}")
            continue

        print(f"Scraping {platform}")
        response_json = scrape_product(platform, url)

        with open("response.json", "w", encoding="utf-8") as f:
            json.dump(response_json, f, indent=2, ensure_ascii=False)

        parsed_rows = parse_response(data=response_json, platform=platform)
        if parsed_rows:
            append_rows_to_excel(EXCEL_OUTPUT, parsed_rows, url)
            print("Data scrap berhasil ditambahkan ke Excel")
        else:
            print(f"nothing for product in URL from: {platform}")


if __name__ == "__main__":
    main()
