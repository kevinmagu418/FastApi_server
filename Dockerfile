# 1️⃣ Base image
FROM python:3.10

# 2️⃣ Set working directory
WORKDIR /app

# 3️⃣ Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 4️⃣ Copy requirements first
COPY requirements.txt .

# 5️⃣ Upgrade pip
RUN pip install --upgrade pip

# 6️⃣ Install CPU-only torch first (IMPORTANT)
RUN pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# 7️⃣ Install remaining dependencies
RUN pip install --no-cache-dir fastapi uvicorn[standard] pillow requests

# 8️⃣ Copy full project
COPY . .

# 9️⃣ Expose port
EXPOSE 8000

# 🔟 Start server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
