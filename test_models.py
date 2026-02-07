import os
from PIL import Image
from app.core.registry import MODEL_REGISTRY
from app.services.inference import predict_crop

# Path to a test image
TEST_IMAGE_PATH = "app/testimage.png"  

if not os.path.exists(TEST_IMAGE_PATH):
    raise FileNotFoundError(f"Test image not found: {TEST_IMAGE_PATH}")

image = Image.open(TEST_IMAGE_PATH)

print("Testing all models...\n")

for crop in MODEL_REGISTRY.keys():
    try:
        result = predict_crop(crop, image)
        print(f"Crop: {result['crop']}")
        print(f" Disease: {result['display_label']} ({result['disease']})")
        print(f" Confidence: {result['confidence']}")
        print(f" Severity: {result['severity']}")
        print("-" * 40)
    except Exception as e:
        print(f"Failed for crop '{crop}': {e}")
        print("-" * 40)

print("All models tested!")
