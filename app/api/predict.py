from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional, Dict, Any
import base64
from io import BytesIO
from PIL import Image

from app.services.inference import predict_crop
from app.services.recommendation import engine as rec_engine

router = APIRouter()

# Response model
class RecommendationResponse(BaseModel):
    disease: str
    severity: str
    chemical_treatment: str
    organic_treatment: str
    prevention: str

class PredictionResponse(BaseModel):
    crop: str
    disease: str
    display_label: str
    confidence: float
    severity: str
    recommendation: Optional[RecommendationResponse] = None

@router.post("/predict", response_model=PredictionResponse)
async def predict_endpoint(
    crop: str = Form(..., description="Crop name, e.g., 'bean'"),
    file: Optional[UploadFile] = File(None, description="Upload an image file"),
    image_base64: Optional[str] = Form(None, description="Or provide Base64 encoded image")
):
    """
    Predict crop disease and generate recommendations.
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

    # Predict Disease
    try:
        result = predict_crop(crop, image)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Generate Recommendation via RAG + Groq
    recommendation = rec_engine.generate_recommendation(result)
    
    # Merge result with recommendation
    result["recommendation"] = recommendation

    return result
