# 1️⃣ Base image (using slim for smaller footprint)
FROM python:3.10-slim

# 2️⃣ Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# 3️⃣ Set working directory
WORKDIR /app

# 4️⃣ Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 5️⃣ Copy requirements
COPY requirements.txt .

# 6️⃣ Install pip and key libraries
RUN pip install --upgrade pip
# Install CPU-only torch to save space on cloud runners
RUN pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download SentenceTransformer model to cache it in the image
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# 7️⃣ Copy the rest of the application
COPY . .

# 8️⃣ Expose port
EXPOSE 8000

# 9️⃣ Start server using dynamic port for Railway/Render
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
