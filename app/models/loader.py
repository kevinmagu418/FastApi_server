import torch
from torchvision import models
from app.core.registry import MODEL_REGISTRY
from app.core.config import DEVICE

# Cache loaded models to avoid reloading
LOADED_MODELS = {}

def load_model(crop: str) -> torch.nn.Module:
    """
    Load a PyTorch model for a specific crop.
    Returns a MobileNetV2 model loaded with weights.
    Uses caching to prevent reloading.
    """
    if crop in LOADED_MODELS:
        return LOADED_MODELS[crop]

    if crop not in MODEL_REGISTRY:
        raise ValueError(f"Unknown crop '{crop}'")

    model_path = MODEL_REGISTRY[crop]['model_path']
    num_classes = len(MODEL_REGISTRY[crop]['classes'])

    model = models.mobilenet_v2(pretrained=False)
    model.classifier[1] = torch.nn.Linear(model.last_channel, num_classes)
    model.load_state_dict(torch.load(model_path, map_location=DEVICE))
    model.eval()
    model.to(DEVICE)

    LOADED_MODELS[crop] = model
    return model
