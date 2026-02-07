import requests
import base64
from pathlib import Path

# === CONFIG ===
API_URL = "http://127.0.0.1:8000/api/predict"  # FastAPI endpoint
TEST_IMAGE_PATH = Path("app/testimage.png")  #  test image 
CROP = "cassava"  # change to the crop you want to test

#  Encode image in Base64 
if not TEST_IMAGE_PATH.exists():
    raise FileNotFoundError(f"Test image not found: {TEST_IMAGE_PATH}")

with open(TEST_IMAGE_PATH, "rb") as f:
    image_bytes = f.read()
image_base64 = base64.b64encode(image_bytes).decode("utf-8")

#  Build request payload 
payload = {
    "crop": CROP,
    "image_base64": image_base64
}

# Send POST request
response = requests.post(API_URL, json=payload)

# Check response
if response.status_code == 200:
    print("Prediction Response:")
    print(response.json())
else:
    print(" Request failed:")
    print(response.status_code, response.text)
