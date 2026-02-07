from fastapi import FastAPI
from app.api import predict

app = FastAPI(title="Crop Disease Detection API")

app.include_router(predict.router, prefix="/api")
