import torch
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
from typing import Tuple, List, cast

from app.core.config import IMG_SIZE, CONFIDENCE_THRESHOLDS

def preprocess_image(image: Image.Image) -> torch.Tensor:
    """
    Convert a PIL image into a model-ready tensor.
    Output shape: (1, 3, 224, 224) or size from config.
    """
    image = image.convert("RGB")

    transform = transforms.Compose([
        transforms.Resize(IMG_SIZE),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225],
        ),
    ])

    tensor = cast(torch.Tensor, transform(image))
    tensor = tensor.unsqueeze(0)  # add batch dimension

    return tensor

def confidence_to_severity(confidence: float) -> str:
    """Map confidence score to severity level using thresholds from config."""
    if confidence >= CONFIDENCE_THRESHOLDS["high"]:
        return "High"
    elif confidence >= CONFIDENCE_THRESHOLDS["medium"]:
        return "Medium"
    else:
        return "Low"
