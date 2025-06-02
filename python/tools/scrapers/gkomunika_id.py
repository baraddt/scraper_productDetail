from playwright.sync_api import sync_playwright
import json


def scrape(url: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto(url)
        page.wait_for_timeout(5000)

        result = {"title": "", "variants": []}

        # Ambil title produk
        try:
            result["title"] = page.title()
        except:
            result["title"] = "N/A"

        masa_labels = page.locator(".variant-section-0 label")
        fup_labels = page.locator(".variant-section-1 label")

        for i in range(masa_labels.count()):
            masa_label = masa_labels.nth(i)
            masa_text = masa_label.inner_text()
            masa_label.click()
            page.wait_for_timeout(500)

            for j in range(fup_labels.count()):
                fup_label = fup_labels.nth(j)
                fup_text = fup_label.inner_text()

                # Ambil harga sebelum klik fup
                try:
                    old_price = page.locator(".product-price ins").inner_text()
                except:
                    old_price = ""

                fup_label.click()
                page.wait_for_timeout(500)

                # Tunggu sampai harga berubah dari old_price
                max_wait = 8000
                interval = 500
                elapsed = 0
                price_final = ""

                while elapsed < max_wait:
                    try:
                        new_price = page.locator(".product-price ins").inner_text()
                        if new_price != old_price and " - " not in new_price:
                            price_final = new_price
                            break
                    except:
                        new_price = ""
                    page.wait_for_timeout(interval)
                    elapsed += interval

                # Jika tidak berubah dari old_price
                if price_final == "":
                    price_final = "[UNSTABLE] " + old_price
                    print(
                        f"Gilee lama bet loadingnya yauda Harga nya ga ngubah yang ini: {masa_text} + {fup_text}"
                    )

                result["variants"].append(
                    {"masa_aktif": masa_text, "fup": fup_text, "price": price_final}
                )

        with open("response.json", "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
            print("Scrape Success save to response.json")

        print("Selesai scrape dengan pemantauan harga yang sinkron")
        browser.close()
        return result
