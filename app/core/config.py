import torch
import os
from dotenv import load_dotenv

# Load from current working directory (root)
load_dotenv(os.path.join(os.getcwd(), '.env'))

# Device configuration
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# LLM & RAG Settings
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.3-70b-versatile"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
CHROMA_DB_DIR = "app/db/chroma_db"
KNOWLEDGE_DIR = "app/data/knowledge"

# Optional: Other global settings
IMG_SIZE = (224, 224)  # Default input size for all models
CONFIDENCE_THRESHOLDS = {
    "high": 0.85,
    "medium": 0.60,
    "low": 0.0
}
