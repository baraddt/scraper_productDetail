from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
import shutil
import os
import subprocess
import traceback

app = FastAPI()

EXCEL_INPUT = "data/produk.xlsx"
EXCEL_OUTPUT = "output/hasil.xlsx"
SCRAPER_SCRIPT = "python/main.py"


@app.post("/scrape")
def run_scraper(file: UploadFile = File(...)):
    try:
        os.makedirs("data", exist_ok=True)
        os.makedirs("output", exist_ok=True)

        # Simpan file input Excel
        with open(EXCEL_INPUT, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Jalankan scraper
        result = subprocess.run(
            ["python", SCRAPER_SCRIPT], capture_output=True, text=True
        )

        if result.returncode != 0:
            print("SCRAPER ERROR:")
            print(result.stderr)
            return JSONResponse(
                content={"error": "Scraper gagal dijalankan", "detail": result.stderr},
                status_code=500,
            )

        # Tambahan pengecekan apakah file hasil dibuat
        if not os.path.exists(EXCEL_OUTPUT):
            print("Scraping selesai, tapi file hasil.xlsx tidak ditemukan.")
            return JSONResponse(
                content={
                    "message": "Scraping selesai, tapi file hasil.xlsx tidak ditemukan.",
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                },
                status_code=500,
            )

        # File ditemukan, langsung kirim respon
        return {
            "message": "Scraping berhasil & file hasil.xlsx tersedia.",
            "stdout": result.stdout,
            "detail": "Gunakan endpoint /download untuk mengambil hasil.",
        }

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            content={"error": "Unhandled exception", "detail": str(e)}, status_code=500
        )


@app.get("/download")
def download_result():
    if not os.path.exists(EXCEL_OUTPUT):
        return JSONResponse(
            content={"error": "File hasil.xlsx tidak ditemukan."}, status_code=404
        )
    return FileResponse(
        EXCEL_OUTPUT,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename="hasil.xlsx",
    )
