from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional
import base64
from io import BytesIO
from PIL import Image

from app.services.inference import predict_crop

router = APIRouter()

# Response model
class PredictionResponse(BaseModel):
    crop: str
    disease: str
    display_label: str
    confidence: float
    severity: str

@router.post("/predict", response_model=PredictionResponse)
async def predict_endpoint(
    crop: str = Form(..., description="Crop name, e.g., 'bean'"),
    file: Optional[UploadFile] = File(None, description="Upload an image file"),
    image_base64: Optional[str] = Form(None, description="Or provide Base64 encoded image")
):
    """
    Predict crop disease from either a file upload or a Base64 image.
    Priority: file > Base64
    """

    # Load image
    if file:
        try:
            image = Image.open(file.file)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid uploaded image")
    elif image_base64:
        try:
            image_data = base64.b64decode(image_base64)
            image = Image.open(BytesIO(image_data))
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid Base64 image")
    else:
        raise HTTPException(status_code=400, detail="No image provided")

    # Predict
    try:
        result = predict_crop(crop, image)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return result
