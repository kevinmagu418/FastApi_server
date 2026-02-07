from PIL import Image
import torch
import torch.nn.functional as F

from app.models.loader import load_model
from app.utils.image import preprocess_image, confidence_to_severity
from app.core.registry import MODEL_REGISTRY

def predict_crop(crop: str, image: Image.Image) -> dict:
    """
    Predict disease for a given crop image.
    
    Args:
        crop (str): Crop name, e.g., "tomato"
        image (PIL.Image.Image): Input image
    
    Returns:
        dict: {
            "crop": str,
            "disease": str,          # raw label
            "display_label": str,    # human-readable label
            "confidence": float,     # 0-1
            "severity": str          # High/Medium/Low
        }
    """
    # Load model
    model = load_model(crop)

    # Ensure tensor is on same device as model
    device = next(model.parameters()).device
    tensor = preprocess_image(image).to(device)

    # Inference
    model.eval()
    with torch.no_grad():
        outputs = model(tensor)
        probs = F.softmax(outputs, dim=1)
        confidence, idx = torch.max(probs, dim=1)

    # Convert results to Python types
    idx = idx.item()
    confidence = confidence.item()
    severity = confidence_to_severity(confidence)

    # Map to labels
    raw_label = MODEL_REGISTRY[crop]['classes'][idx]
    display_label = MODEL_REGISTRY[crop]['display_classes'][idx]

    return {
        "crop": crop,
        "disease": raw_label,
        "display_label": display_label,
        "confidence": round(confidence, 2),
        "severity": severity
    }
