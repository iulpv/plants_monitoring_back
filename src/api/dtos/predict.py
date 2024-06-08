from pydantic import BaseModel


class Prediction(BaseModel):
    plant_type: str
    plant_disease: str
    probability: float
    photo: str
