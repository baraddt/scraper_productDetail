from playwright.sync_api import sync_playwright
import json


def scrape(url: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=False)
        context = browser.new_context()

        with open("cookies.json", "r", encoding="utf-8") as f:
            cookies = json.load(f)
        context.add_cookies(cookies)

        page = context.new_page()
        page.goto(url)
        page.wait_for_timeout(6000)

        result = {"title": "", "variants": []}

        try:
            result["title"] = page.locator("h1.vR6K3w").inner_text()
        except Exception as e:
            print("Gagal ambil judul:", e)

        masa_aktif_buttons = page.locator("h2.Dagtcd", has_text="Masa Aktif").locator(
            "xpath=../following-sibling::div[1]//button"
        )
        kuota_buttons = page.locator("h2.Dagtcd", has_text="Kuota").locator(
            "xpath=../following-sibling::div[1]//button"
        )

        masa_aktif_count = masa_aktif_buttons.count()
        kuota_count = kuota_buttons.count()

        for i in range(masa_aktif_count):
            masa_aktif_option = masa_aktif_buttons.nth(i)
            masa_aktif_text = masa_aktif_option.get_attribute("aria-label")
            masa_aktif_option.click()
            page.wait_for_timeout(1000)

            for j in range(kuota_count):
                kuota_option = kuota_buttons.nth(j)
                kuota_text = kuota_option.get_attribute("aria-label")
                kuota_option.click()
                page.wait_for_timeout(1000)

                try:
                    price = page.locator(".IZPeQz").inner_text()
                except:
                    price = "?"

                result["variants"].append(
                    {"masa_aktif": masa_aktif_text, "kuota": kuota_text, "price": price}
                )

        with open("response.json", "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        browser.close()
        return result
