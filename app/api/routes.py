from fastapi import APIRouter, UploadFile, File
import shutil
import os

from app.models.response_models import output

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.post("/analyse")
async def summary(file: UploadFile=File(...)):

    path = f"temp_{file.filename}"

    with open(path,"wb") as buffer:
        shutil.copyfileobj(file.file,buffer)
    
    temp = output(path)

    os.remove(path)
    return temp



