import logging
import re


def setup_logging():
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
    )


def get_platform_from_url(url: str) -> str:
    if "shopee.co.id" in url:
        return "shopee"
    elif "shop-id.tokopedia.com" in url:
        return "tiktok"
    elif "tokopedia.com" in url:
        return "tokopedia"
    elif "gkomunika.com" in url:
        return "gkomunika"
    elif "gkomunika.id" in url:
        return "gkomunika_id"
    else:
        return "unknown"


def extract_product_code(url: str) -> str:
    # Cari teks setelah '/product_detail/' sampai akhir URL
    match = re.search(r"/product_detail/([^/]+)", url)
    if match:
        return match.group(1)
    return url
