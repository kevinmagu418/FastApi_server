from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import base64
from io import BytesIO
from PIL import Image

from app.services.inference import predict_crop

router = APIRouter()

class PredictionRequest(BaseModel):
    crop: str
    image_base64: str

class PredictionResponse(BaseModel):
    crop: str
    disease: str
    display_label: str
    confidence: float
    severity: str

@router.post("/predict", response_model=PredictionResponse)
async def predict_endpoint(request: PredictionRequest):
    try:
        # Decode base64 image
        image_data = base64.b64decode(request.image_base64)
        image = Image.open(BytesIO(image_data))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image data")

    try:
        result = predict_crop(request.crop, image)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return result
