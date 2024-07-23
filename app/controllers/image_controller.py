from fastapi import APIRouter, Depends, File, UploadFile, Form
from app.database import get_db
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Generator
import os
import shutil

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class Image(BaseModel):
    note: str | None = None
    url: str | None = None

router = APIRouter()

@router.get("/images")
async def get_images(db: Generator = Depends(get_db)):
    try:
        with db as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute('''
              SELECT * FROM Images
            ''')
            images = cursor.fetchall()
            cursor.close()

            if images:
                return JSONResponse(status_code=200, content={"message": images})
            else:
                return JSONResponse(status_code=404, content={"message": "No images found"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": True, "message": str(e)})

@router.post("/image")
async def post_image(note: str = Form(...), img: UploadFile = File(...), db: Generator = Depends(get_db)):
    try:
        file_location = os.path.join(UPLOAD_DIR, img.filename)

        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(img.file, file_object)

        with db as connection:
            cursor = connection.cursor()
            cursor.execute('''
              INSERT INTO Images (note, url) VALUES (%s, %s)
            ''', (note, file_location))
            connection.commit()
            cursor.close()

            return JSONResponse(status_code=201, content={"message": "Image created", "url": f"/{file_location}", "note": note})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": True, "message": str(e)})
