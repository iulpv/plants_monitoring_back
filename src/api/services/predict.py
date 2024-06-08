import base64
from io import BytesIO

from PIL import Image
from fastapi import UploadFile
from fastapi.responses import JSONResponse

from src.api.dtos.predict import Prediction
from src.api.settings import Settings
from src.ml.model import Model


class PredictService:
    def __init__(self):
        self.model = Model()
        self.settings = Settings()
        self.greenhouse_prediction = None

    async def predict_photo(self, file: UploadFile):
        if file.size > self.settings.max_file_size:
            return JSONResponse(content={'message': 'File is too large. Maximum allowed size is 5MB'}, status_code=400)

        content = await file.read()
        if not self._is_image(content):
            return JSONResponse(content={'status': 'File is not an image'}, status_code=400)

        plant_type, plant_disease, probability = self.model.eval_model(content)
        img = Image.open(BytesIO(content))
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        return Prediction(plant_type=plant_type, plant_disease=plant_disease, probability=probability, photo=base64.b64encode(img_byte_arr).decode('utf-8'))

    async def handle_camera_photo(self, file: UploadFile):
        prediction = await self.predict_photo(file)
        self.greenhouse_prediction = prediction

        return JSONResponse(content={'status': 'successfully'}, status_code=200)

    async def predict_camera_photo(self):
        if self.greenhouse_prediction is not None:
            return self.greenhouse_prediction
        else:
            return JSONResponse(content={'message': 'No data'}, status_code=400)

    def _is_image(self, content):
        try:
            img = Image.open(BytesIO(content))
            img.verify()
            return True
        except Exception:
            return False
