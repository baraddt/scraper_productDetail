def parse_response(data=None, platform=None, filepath="response.json"):
    import json

    try:
        if data is None:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

        rows = []

        if platform == "tokopedia":
            # title = data.get("title", "N/A")
            variants = data.get("variants", [])
            for v in variants:
                rows.append(
                    {
                        # "Nama Produk": title,
                        "Masa Aktif": v.get("masa_aktif", ""),
                        "Kuota": v.get("Kuota", ""),
                        "Harga": v.get("price", ""),
                    }
                )
            return rows

        elif platform == "shopee":
            item = data.get("data", {})
            models = item.get("models", [])
            for model in models:
                name = model.get("name", "N/A")
                price_int = model.get("price", 0)
                price_fmt = f"Rp. {int(price_int / 100000):,}".replace(",", ".")
                rows.append({"Nama Paket": name, "Harga": price_fmt})

        elif platform == "gkomunika":
            variants = data.get("variants", [])
            for v in variants:
                # name = v.get("name", "N/A")
                public_title = v.get("public_title", "N/A")
                price = v.get("price", 0)
                price_fmt = f"Rp. {int(price / 100):,}".replace(",", ".")
                rows.append(
                    {
                        # "Nama Paket": name,
                        "Masa Aktif - Kuota": public_title,
                        "Harga": price_fmt,
                    }
                )
        elif platform == "gkomunika_id":
            # title = data.get("title", "N/A")
            variants = data.get("variants", [])
            for v in variants:
                rows.append(
                    {
                        # "Nama Produk": title,
                        "Masa Aktif": v.get("masa_aktif", ""),
                        "FUP": v.get("fup", ""),
                        "Harga": v.get("price", ""),
                    }
                )
            return rows

        elif platform == "tiktok":
            if "title" in data and "variants" in data:
                # title = data.get("title", "N/A")
                for v in data["variants"]:
                    masa = v.get("masa_aktif", "")
                    kuota = v.get("kuota", "")
                    harga = v.get("price", "N/A")
                    rows.append(
                        {
                            # "Nama Produk": title,
                            "Masa Aktif": masa,
                            "Kuota": kuota,
                            "Harga": harga,
                        }
                    )
        else:
            print(f"Platform {platform} belum didukung.")
        return rows
    except Exception as e:
        print(f"Error saat parsing: {e}")
        return []
