from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import Optional, Dict, Any
import base64
import logging
from io import BytesIO
from PIL import Image

from app.services.inference import predict_crop
from app.services.recommendation import engine as rec_engine

router = APIRouter()
logger = logging.getLogger("uvicorn.error")

@router.post("/predict")
async def predict_endpoint(
    crop: str = Form(..., description="Crop name, e.g., 'bean'"),
    file: Optional[UploadFile] = File(None, description="Upload an image file"),
    image_base64: Optional[str] = Form(None, description="Or provide Base64 encoded image")
):
    """
    Predict crop disease and generate recommendations.
    Refactored to match Supabase Edge Function and DB schema.
    """
    # 2. Normalize crop input: lowercase and strip
    crop = crop.lower().strip()
    print("crop:", crop)

    # 3. Load image safely: ensure convert("RGB")
    try:
        if file:
            image_content = await file.read()
            image = Image.open(BytesIO(image_content)).convert("RGB")
        elif image_base64:
            # Base64 loading logic
            image_data = base64.b64decode(image_base64)
            image = Image.open(BytesIO(image_data)).convert("RGB")
        else:
            raise HTTPException(status_code=400, detail="No image provided")
    except Exception as e:
        logger.error(f"Image load error: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid image format or source")

    # 4. Wrap predict_crop in try/catch
    try:
        result = predict_crop(crop, image)
        print("prediction:", result)
    except ValueError as e:
        # Handle unsupported crop or model error
        logger.error(f"Prediction input error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Inference error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Disease prediction failed: {str(e)}")

    # 5. Wrap recommendation engine in try/catch so it NEVER crashes the API
    recommendation = None
    try:
        # Generate Recommendation via RAG + Groq
        raw_rec = rec_engine.generate_recommendation(result)
        
        # 8. Normalize recommendation structure exactly as required
        # Now raw_rec will always have these fields due to the fallback in generate_recommendation
        recommendation = {
            "disease": str(raw_rec.get("disease", result.get("display_label", "unknown"))),
            "severity": str(raw_rec.get("severity", result.get("severity", "medium"))),
            "chemical_treatment": str(raw_rec.get("chemical_treatment", "Not specified")),
            "organic_treatment": str(raw_rec.get("organic_treatment", "Not specified")),
            "prevention": str(raw_rec.get("prevention", "Not specified"))
        }
    except Exception as e:
        logger.error(f"Recommendation engine error: {str(e)}")
        # Ultimate fallback if even the engine's internal fallback fails
        recommendation = {
            "disease": str(result.get("display_label", "unknown")),
            "severity": str(result.get("severity", "medium")),
            "chemical_treatment": "Consult a local agricultural expert.",
            "organic_treatment": "Remove infected parts and improve hygiene.",
            "prevention": "Ensure proper spacing and resistant varieties."
        }

    # 6 & 7. Normalize final response BEFORE returning
    # Always return disease, confidence, severity, recommendation
    # No extra fields like crop or raw_disease as per Requirement 10
    final_response = {
        "disease": str(result.get("display_label", "unknown")),
        "confidence": float(result.get("confidence", 0.0)),
        "severity": str(result.get("severity", "medium")),
        "recommendation": recommendation
    }

    return final_response
