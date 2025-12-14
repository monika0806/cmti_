from fastapi import FastAPI, UploadFile, File
from typing import List
import os
import uuid
from trocr_engine import trocr_extract

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# ✅ Correct imports (NO name conflicts)
from image_preprocess import preprocess_image
from ocr import extract_text
from text_postprocess import correct_text

print("🔥 THIS IS THE REAL app.py 🔥")

app = FastAPI()

# Serve frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_frontend():
    return FileResponse("static/index.html")


@app.post("/ocr")
async def ocr_images(files: List[UploadFile] = File(...)):
    print("✅ OCR endpoint HIT")

    job_id = str(uuid.uuid4())
    upload_dir = os.path.join("storage", "uploads", job_id)
    os.makedirs(upload_dir, exist_ok=True)

    pages = []

    for file in files:
        # Save original image
        original_path = os.path.join(upload_dir, file.filename)
        with open(original_path, "wb") as f:
            f.write(await file.read())

        try:
            # 1️⃣ Preprocess image
            processed_path = preprocess_image(original_path)

            # 2️⃣ OCR
            raw_text = trocr_extract(processed_path)

            # 3️⃣ Post-process text
            final_text = correct_text(raw_text)

        except Exception as e:
            print("❌ OCR pipeline error:", e)
            final_text = ""

        pages.append({
            "filename": file.filename,
            "text": final_text
        })

    return {
        "job_id": job_id,
        "pages": pages
    }