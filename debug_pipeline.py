import os
import torch
from PIL import Image
from app.services.inference import predict_crop
from app.services.recommendation import engine as rec_engine

# Set PYTHONPATH to root
import sys
sys.path.append(os.getcwd())

def test_full_pipeline():
    test_image_path = "app/testimage.png"
    crop = "cassava"
    
    if not os.path.exists(test_image_path):
        print(f"Error: {test_image_path} not found.")
        return

    print(f"--- Testing Prediction for {crop} ---")
    image = Image.open(test_image_path)
    
    try:
        # Test Inference
        result = predict_crop(crop, image)
        print("Prediction Result:", result)
        
        # Test Recommendation
        print("\n--- Generating Recommendation ---")
        recommendation = rec_engine.generate_recommendation(result)
        print("Recommendation:", recommendation)
        
    except Exception as e:
        print(f"Pipeline failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_full_pipeline()
