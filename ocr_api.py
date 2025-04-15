from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import tempfile
from google_drive_ocr import GoogleOCRApplication

app = FastAPI()
ocr = GoogleOCRApplication("client_secret.json")

@app.post("/ocr")
async def ocr_file(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        result = ocr.perform_ocr(tmp_path)
        return JSONResponse(content={"text": result})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
