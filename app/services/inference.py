from PIL import Image
import torch
import torch.nn.functional as F
from typing import Dict

from app.models.loader import load_model
from app.utils.image import preprocess_image, confidence_to_severity
from app.core.registry import MODEL_REGISTRY

# Cache loaded models here
LOADED_MODELS: Dict[str, torch.nn.Module] = {}

def load_model_cached(crop: str) -> torch.nn.Module:
    """
    Load a model once and reuse it.
    """
    if crop not in LOADED_MODELS:
        LOADED_MODELS[crop] = load_model(crop)
    return LOADED_MODELS[crop]

def preload_all_models() -> None:
    """
    Preload all models at startup.
    """
    print("Preloading all crop models...")
    for crop in MODEL_REGISTRY.keys():
        try:
            load_model_cached(crop)
            print(f" Loaded model: {crop}")
        except Exception as e:
            print(f" Failed to load {crop}: {e}")
    print("All models preloaded!")

def predict_crop(crop: str, image: Image.Image) -> dict:
    """
    Predict disease for a given crop image.
    """
    model = load_model_cached(crop)
    device = next(model.parameters()).device
    tensor = preprocess_image(image).to(device)

    model.eval()
    with torch.no_grad():
        outputs = model(tensor)
        probs = F.softmax(outputs, dim=1)
        confidence, idx = torch.max(probs, dim=1)

    idx = idx.item()
    confidence = confidence.item()
    severity = confidence_to_severity(confidence)

    raw_label = MODEL_REGISTRY[crop]['classes'][idx]
    display_label = MODEL_REGISTRY[crop]['display_classes'][idx]

    return {
        "crop": crop,
        "disease": raw_label,
        "display_label": display_label,
        "confidence": round(confidence, 2),
        "severity": severity
    }
