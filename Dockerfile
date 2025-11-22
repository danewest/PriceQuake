FROM python:3.11-slim

# System deps (optional but nice to have)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Workdir
WORKDIR /app

# Copy requirements & install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Default command (override in docker-compose)
CMD ["uvicorn", "App.main:app", "--host", "0.0.0.0", "--port", "8000"]
