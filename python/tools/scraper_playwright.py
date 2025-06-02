from tools.scrapers import tokopedia
from tools.scrapers import tiktok
from tools.scrapers import shopee
from tools.scrapers.gkomunika import scrape as scrape_gkomunika
from tools.scrapers import gkomunika_id


def scrape_product(platform: str, url: str):
    if platform == "tokopedia":
        return tokopedia.scrape(url)
    elif platform == "shopee":
        return shopee.scrape(url)
    elif platform == "gkomunika":
        return scrape_gkomunika(url)
    elif platform == "gkomunika_id":
        return gkomunika_id.scrape(url)
    elif platform == "tiktok":
        return tiktok.scrape(url)

    else:
        raise ValueError(f"Platform tidak dikenali: {platform}")
