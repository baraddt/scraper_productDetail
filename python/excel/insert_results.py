import pandas as pd
import os


def append_rows_to_excel(filepath, rows, url):
    is_pivot_format = False
    if rows and isinstance(rows[0], dict):
        first_row_keys = rows[0].keys()
        if (
            "Masa Aktif" in first_row_keys
            and ("Kuota" in first_row_keys or "FUP" in first_row_keys)
            and "Harga" in first_row_keys
        ):
            is_pivot_format = True

    existing_data_list = []
    if os.path.exists(filepath):
        df_existing_raw = pd.read_excel(filepath, header=None)
        existing_data_list = df_existing_raw.values.tolist()

    new_block_data = []

    new_block_data.append([url])
    new_block_data.append([])

    if is_pivot_format:
        df_temp_rows = []
        for row in rows:
            masa_aktif = row.get("Masa Aktif", "")
            kuota_key = "Kuota" if "Kuota" in row else "FUP"
            kuota = row.get(kuota_key, "")
            harga = row.get("Harga", "")

            if masa_aktif and kuota and harga:
                df_temp_rows.append(
                    {"Masa Aktif": masa_aktif, "Kuota": kuota, "Harga": harga}
                )

        if not df_temp_rows:
            print(
                f"No valid data found for pivot table format from URL: {url}. Skipping."
            )
            return

        df_new_raw = pd.DataFrame(df_temp_rows)

        print(
            f"\nDEBUG (append_rows_to_excel): DataFrame sebelum pembersihan harga untuk {url}:"
        )
        print(df_new_raw)

        df_new_raw["Harga"] = (
            df_new_raw["Harga"]
            .astype(str)
            .str.replace("Rp", "", regex=False)
            .str.replace(".", "", regex=False)
            .str.replace(",", ".", regex=False)
        )
        df_new_raw["Harga"] = pd.to_numeric(df_new_raw["Harga"], errors="coerce")

        df_new_raw.dropna(subset=["Harga"], inplace=True)

        print(
            f"\nDEBUG (append_rows_to_excel): DataFrame SETELAH pembersihan harga dan dropna untuk {url}:"
        )
        print(df_new_raw)

        if df_new_raw.empty:
            print(
                f"No valid numeric prices found for pivot table from URL: {url}. Skipping."
            )
            return

        df_pivot = df_new_raw.pivot_table(
            index="Masa Aktif", columns="Kuota", values="Harga", aggfunc="first"
        )

        df_pivot = df_pivot.reset_index()

        pivot_headers = df_pivot.columns.tolist()

        new_block_data.append(pivot_headers)

        for _, row_data in df_pivot.iterrows():
            new_block_data.append(row_data.tolist())

    else:
        cols_to_use = []
        if any("Nama Paket" in r for r in rows):
            cols_to_use = ["Nama Produk", "Harga"]
        elif any("Masa Aktif - Kuota" in r for r in rows):
            cols_to_use = [
                "Nama Produk",
                "Harga",
            ]
        else:
            if rows:
                cols_to_use = list(rows[0].keys())

        new_block_data.append(cols_to_use)

        for row in rows:
            formatted_row = []
            for col in cols_to_use:
                if col == "Nama Produk":
                    if "Nama Paket" in row:
                        formatted_row.append(row.get("Nama Paket", ""))
                    elif "Masa Aktif - Kuota" in row:
                        formatted_row.append(row.get("Masa Aktif - Kuota", ""))
                    else:
                        formatted_row.append(row.get(col, ""))
                elif col == "Harga":
                    formatted_row.append(row.get("Harga", ""))
                else:
                    formatted_row.append(row.get(col, ""))
            new_block_data.append(formatted_row)

    if existing_data_list:
        max_width_existing = (
            max(len(row) for row in existing_data_list) if existing_data_list else 0
        )
        max_width_new_block = (
            max(len(row) for row in new_block_data) if new_block_data else 0
        )
        separator_width = max(max_width_existing, max_width_new_block, 1)

        existing_data_list.append([None] * separator_width)
        existing_data_list.append([None] * separator_width)

    existing_data_list.extend(new_block_data)

    df_final = pd.DataFrame(existing_data_list)

    df_final.to_excel(filepath, index=False, header=False)
