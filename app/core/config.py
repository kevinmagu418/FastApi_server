import torch

# Device configuration
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Optional: Other global settings
IMG_SIZE = (224, 224)  # Default input size for all models
CONFIDENCE_THRESHOLDS = {
    "high": 0.85,
    "medium": 0.60,
    "low": 0.0
}
