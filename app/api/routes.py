from fastapi import APIRouter

from app.models.response_models import output

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get("/summary")
async def summary():
    return output("cnn.pdf")