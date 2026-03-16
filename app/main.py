from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import predict
from app.services.inference import preload_all_models, LOADED_MODELS

app = FastAPI(title="Crop Disease Detection API")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Crop Disease Detection API. Visit /docs for documentation."}

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, consider listing specific Supabase project domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
