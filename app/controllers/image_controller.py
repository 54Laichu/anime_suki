from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from app.database import get_db
from fastapi.responses import JSONResponse
from typing import Generator
import os
import shutil
import boto3

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
CLOUDFRONT_DOMAIN = os.getenv('CLOUDFRONT_DOMAIN')

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

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
        if os.getenv('ENV') == 'production':
            # 如果正式環境，上傳到 S3
            s3_file_key = f"images/{img.filename}"
            s3_client.upload_fileobj(img.file, S3_BUCKET_NAME, s3_file_key)
            s3_url = f"https://{CLOUDFRONT_DOMAIN}/{s3_file_key}"
        else:
            # 如果測試環境，上傳本機
            file_location = os.path.join(UPLOAD_DIR, img.filename)
            with open(file_location, "wb+") as file_object:
                shutil.copyfileobj(img.file, file_object)
            s3_url = f"/uploads/{img.filename}"

        with db as connection:
            cursor = connection.cursor()
            cursor.execute('''
                INSERT INTO Images (note, url) VALUES (%s, %s)
            ''', (note, s3_url))
            connection.commit()
            cursor.close()

        return JSONResponse(status_code=201, content={"message": "Image created", "url": s3_url, "note": note})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": True, "message": str(e)})
