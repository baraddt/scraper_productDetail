from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
import shutil
import os
import subprocess
import traceback

app = FastAPI()

EXCEL_INPUT = "data/produk.xlsx"
EXCEL_OUTPUT = "output/hasil.xlsx"
SCRAPER_SCRIPT = "main.py"


@app.post("/scrape")
def run_scraper(file: UploadFile = File(...)):
    try:
        os.makedirs("data", exist_ok=True)
        os.makedirs("output", exist_ok=True)

        with open(EXCEL_INPUT, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # JALANKAN SCRAPER SEBAGAI PROSES TERPISAH
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

        return {"message": "Scraping selesai. File hasil tersedia untuk diunduh."}

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/download")
def download_result():
    if not os.path.exists(EXCEL_OUTPUT):
        return JSONResponse(
            content={"error": "File hasil tidak ditemukan."}, status_code=404
        )
    return FileResponse(
        EXCEL_OUTPUT,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename="hasil.xlsx",
    )
