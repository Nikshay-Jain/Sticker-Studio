from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import os, shutil
from model import generate_sticker
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Ensure directories exist
UPLOAD_DIR = "uploads"
STATIC_DIR = "static"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)

@app.get("/")
async def root():
    return {"message": "Welcome to AI Sticker Studio!"}

@app.post("/process")
async def create_sticker(
    file: UploadFile = File(...),
    text: str = Form(...),
    style: str = Form(...)
):
    try:
        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            raise HTTPException(400, detail="Only image files are allowed")

        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        sticker_filename = generate_sticker(file_path, text, style)
        if not sticker_filename:
            raise HTTPException(500, detail="Failed to generate sticker")

        return {"filename": f"/static/{sticker_filename}"}

    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})

# Mount static files for serving images
app.mount("/static", StaticFiles(directory="static"), name="static")