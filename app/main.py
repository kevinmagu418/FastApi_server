from fastapi import FastAPI
from app.api import predict
from app.services.inference import preload_all_models, LOADED_MODELS

app = FastAPI(title="Crop Disease Detection API")

# Preload models on startup
preload_all_models()

# Health check endpoint
@app.get("/health")
def health():
    return {
        "status": "ok",
        "loaded_models": list(LOADED_MODELS.keys())
    }

# Include prediction router
app.include_router(predict.router, prefix="/api")
