import requests
import re
import json


def scrape(url: str):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"Gagal akses halaman: {response.status_code}")
            return {}

        html = response.text
        match = re.search(r"var\s+meta\s*=\s*({.*?});", html, re.DOTALL)

        if not match:
            print("Tidak menemukan 'var meta'")
            return {}

        meta_json = match.group(1).replace("\n", "").replace("\r", "")
        meta = json.loads(meta_json)

        variants = meta.get("product", {}).get("variants", [])

        result = {"variants": variants}

        with open("response.json", "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
            print("Scrap success save to response.json")

        return result

    except Exception as e:
        print(f"Error saat scraping Gkomunika: {e}")
        return {}
