import requests
from pathlib import Path

# === CONFIG ===
API_URL = "http://127.0.0.1:8000/api/predict"
TEST_IMAGE_PATH = Path("app/testimage.png")
CROP = "tomato"  # Testing cassava as per registry

if not TEST_IMAGE_PATH.exists():
    print(f"Error: {TEST_IMAGE_PATH} not found.")
    exit()

#  Build multipart form-data
with open(TEST_IMAGE_PATH, "rb") as f:
    files = {"file": (TEST_IMAGE_PATH.name, f, "image/png")}
    data = {"crop": CROP}

    print(f"Sending request to {API_URL} for crop: {CROP}...")
    response = requests.post(API_URL, files=files, data=data)

# Check response
if response.status_code == 200:
    import json
    print("Success! Prediction and Recommendation:")
    print(json.dumps(response.json(), indent=2))
else:
    print("Request failed:")
    print(response.status_code, response.text)
