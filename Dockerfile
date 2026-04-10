# 1️⃣ Base image (using slim for smaller footprint)
FROM python:3.10-slim

# 2️⃣ Install system dependencies (Must be done first as root)
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 3️⃣ Create a non-root user (Hugging Face strict requirement)
RUN useradd -m -u 1000 user
# Switch to the new user
USER user
# Set environment variables for the user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 4️⃣ Set working directory
WORKDIR $HOME/app
ENV PYTHONPATH=$HOME/app

# 5️⃣ Copy requirements (Ensuring the 'user' owns it)
COPY --chown=user requirements.txt .

# 6️⃣ Install pip and key libraries
RUN pip install --upgrade pip
# Install CPU-only torch to save space
RUN pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download SentenceTransformer model to cache it in the image (Now correctly stored in the user's ~/.cache)
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# 7️⃣ Copy the rest of the application
COPY --chown=user . $HOME/app

# 8️⃣ Expose Hugging Face Port
EXPOSE 7860

# 9️⃣ Start server on exactly port 7860
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
