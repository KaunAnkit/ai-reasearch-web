from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.api.routes import router

app = FastAPI()

app.include_router(router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
async def serve_index():
    return FileResponse("app/static/index.html")

