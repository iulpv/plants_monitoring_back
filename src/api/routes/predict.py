from fastapi import APIRouter
from fastapi import File, UploadFile

from src.api.services.predict import PredictService

router = APIRouter()
service = PredictService()


@router.post("/predict/photo")
async def predict_photo(file: UploadFile = File(...)):
    return await service.predict_photo(file)


@router.post("/predict/camera-photo")
async def handle_camera_photo(file: UploadFile = File(...)):
    return await service.handle_camera_photo(file)


@router.get("/predict/camera-photo")
async def predict_camera_photo():
    return await service.predict_camera_photo()
