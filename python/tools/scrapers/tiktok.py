# from playwright.sync_api import sync_playwright
# import json


# def scrape(url: str):
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         context = browser.new_context()
#         page = context.new_page()
#         page.goto(url)
#         page.wait_for_timeout(6000)

#         result = {"title": "", "variants": []}

#         # Ambil nama produk
#         try:
#             result["title"] = page.locator(".title-v0v6fK").inner_text()
#         except:
#             pass

#         # Klik opsi
#         page.locator("text=Select options").click(force=True)
#         page.wait_for_selector(".skuMain-zLbDSB")

#         # Lokator masa aktif (static)
#         masa_aktif_locator = page.locator(
#             ".title-U0a3zD", has_text="Masa Aktif"
#         ).locator("xpath=../following-sibling::div[1]/div")
#         masa_aktif_count = masa_aktif_locator.count()

#         for i in range(masa_aktif_count):
#             masa_aktif_option = masa_aktif_locator.nth(i)
#             masa_aktif_text = masa_aktif_option.inner_text()
#             masa_aktif_option.click()
#             page.wait_for_timeout(500)

#             # Re-locate kuota setelah klik masa aktif
#             kuota_locator = page.locator(".title-U0a3zD", has_text="kuota").locator(
#                 "xpath=../following-sibling::div[1]/div"
#             )
#             kuota_count = kuota_locator.count()

#             for j in range(kuota_count):
#                 kuota_option = kuota_locator.nth(j)
#                 kuota_text = kuota_option.inner_text()
#                 kuota_option.click()
#                 page.wait_for_timeout(700)

#                 try:
#                     price = page.locator(".price-LYdk0Q span").inner_text()
#                 except:
#                     price = "?"

#                 result["variants"].append(
#                     {"masa_aktif": masa_aktif_text, "kuota": kuota_text, "price": price}
#                 )

#         # Simpan hasil
#         with open("response.json", "w", encoding="utf-8") as f:
#             json.dump(result, f, indent=2, ensure_ascii=False)

#         print("Success save to response.json")
#         browser.close()
#         return result


from playwright.sync_api import sync_playwright
import json


def scrape(url: str):
    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)
        # kalo False biar bisa lihat proses nya

        context = browser.new_context()
        context.set_default_timeout(5000)
        page = context.new_page()
        page.goto(url)

        result = {"title": "", "variants": []}

        # Ambil nama produk
        try:
            title_locator = page.locator(".title-v0v6fK")
            title_locator.wait_for()
            result["title"] = title_locator.inner_text()
        except:
            print("Gagal mengambil judul produk")

        # Klik tombol "Select options"
        try:
            page.locator("text=Select options").click(force=True)
            page.wait_for_selector(".skuMain-zLbDSB")
        except:
            print("Gagal klik tombol Select Options")

        # Variasi "Masa Aktif"
        try:
            masa_aktif_locator = page.locator(
                ".title-U0a3zD", has_text="Masa Aktif"
            ).locator("xpath=../following-sibling::div[1]/div")
            masa_aktif_count = masa_aktif_locator.count()
        except:
            masa_aktif_count = 0

        for i in range(masa_aktif_count):
            masa_aktif_option = masa_aktif_locator.nth(i)
            masa_aktif_text = masa_aktif_option.inner_text()
            masa_aktif_option.click()
            page.wait_for_timeout(200)  # Sedikit delay agar UI stabil

            # Variasi "Kuota"
            try:
                kuota_locator = page.locator(".title-U0a3zD", has_text="Kuota").locator(
                    "xpath=../following-sibling::div[1]/div"
                )
                kuota_count = kuota_locator.count()
            except:
                kuota_count = 0

            for j in range(kuota_count):
                kuota_option = kuota_locator.nth(j)
                kuota_text = kuota_option.inner_text()
                kuota_option.click()
                page.wait_for_timeout(300)

                try:
                    price = page.locator(".price-LYdk0Q span").inner_text()
                except:
                    price = "?"

                result["variants"].append(
                    {"masa_aktif": masa_aktif_text, "kuota": kuota_text, "price": price}
                )

        # Simpan hasil
        with open("response.json", "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print("Success save to response.json")
        browser.close()
        return result
