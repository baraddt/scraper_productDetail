from playwright.sync_api import sync_playwright
import json


def scrape(url: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            ignore_https_errors=True,
        )
        page = context.new_page()
        page.goto(url, wait_until="domcontentloaded")
        page.wait_for_timeout(3000)

        try:
            qr_popup = page.locator("div.css-18qem4c")
            if qr_popup.is_visible():
                qr_popup.locator("div.css-11hzwo5 button").click()
                page.wait_for_timeout(1000)
        except:
            pass

        result = {"title": "", "variants": []}

        # Ambil judul produk
        try:
            result["title"] = (
                page.locator("h1[data-testid='lblPDPDetailProductName']")
                .inner_text()
                .strip()
            )
        except:
            result["title"] = "N/A"

        containers = page.locator(
            "div[data-testid='pdpVariantContainer'] div.css-1b2d3hk"
        )

        kuota_container = None
        masa_container = None

        for i in range(containers.count()):
            label = containers.nth(i).locator("p").nth(0).inner_text()
            if "Pilih kuota" in label or "Pilih fup" in label:
                kuota_container = containers.nth(i)
            elif "Pilih masa aktif" in label:
                masa_container = containers.nth(i)

        def get_options(container):
            if container is None:
                return []
            buttons = container.locator("div[data-testid^='btnVariantChip'] button")
            return [buttons.nth(i).inner_text().strip() for i in range(buttons.count())]

        kuota_options = get_options(kuota_container)
        masa_options = get_options(masa_container)

        if not kuota_options and not masa_options:
            try:
                price = (
                    page.locator("div[data-testid='lblPDPDetailProductPrice']")
                    .inner_text()
                    .strip()
                )
            except:
                price = "?"
            result["variants"].append(
                {"Kuota": None, "masa_aktif": None, "price": price}
            )
        elif kuota_options and not masa_options:
            for kuota in kuota_options:
                kuota_container.locator(f"button:has-text('{kuota}')").first.click()
                page.wait_for_timeout(600)
                try:
                    price = (
                        page.locator("div[data-testid='lblPDPDetailProductPrice']")
                        .inner_text()
                        .strip()
                    )
                except:
                    price = "?"
                result["variants"].append(
                    {"Kuota": kuota, "masa_aktif": None, "price": price}
                )
        # Jika cuma ada masa aktif saja
        elif masa_options and not kuota_options:
            for masa in masa_options:
                masa_container.locator(f"button:has-text('{masa}')").first.click()
                page.wait_for_timeout(600)
                try:
                    price = (
                        page.locator("div[data-testid='lblPDPDetailProductPrice']")
                        .inner_text()
                        .strip()
                    )
                except:
                    price = "?"
                result["variants"].append(
                    {"Kuota": None, "masa_aktif": masa, "price": price}
                )
        else:
            # Ganti loop ini untuk klik masa aktif dulu baru kuota
            for masa in masa_options:
                masa_btn = masa_container.locator(f"button:has-text('{masa}')").first
                if not masa_btn.is_enabled():
                    continue  # skip jika disabled

                masa_btn.click()
                page.wait_for_timeout(600)

                for kuota in kuota_options:
                    kuota_btn = kuota_container.locator(
                        f"button:has-text('{kuota}')"
                    ).first
                    if not kuota_btn.is_enabled():
                        continue  # skip jika disabled

                    kuota_btn.click()
                    page.wait_for_timeout(600)

                    try:
                        price = (
                            page.locator("div[data-testid='lblPDPDetailProductPrice']")
                            .inner_text()
                            .strip()
                        )
                    except:
                        price = "?"
                    result["variants"].append(
                        {"Kuota": kuota, "masa_aktif": masa, "price": price}
                    )

        with open("response.json", "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print("Sukses: Semua kombinasi diambil.")
        browser.close()
        return result
