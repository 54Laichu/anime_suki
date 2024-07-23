from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.controllers import image_controller
import os

app = FastAPI(
    title="Anime Suki",
    description="""
                A Website for U to Upload Pics
                """,
    version="1.0.0"
)
app.mount("/static", StaticFiles(directory="./app/static"), name="static")

if os.getenv('ENV') == 'development':
  app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

templates = Jinja2Templates(directory="./app/templates")

@app.get("/", include_in_schema=False, response_class=HTMLResponse)
async def index(request: Request):
  return templates.TemplateResponse("index.html", {"request": request})

app.include_router(image_controller.router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
