FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    jq \
    git \
    build-essential \
    libffi-dev \
 && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create downloads folder
RUN mkdir -p /app/DOWNLOADS

# Optional: set safe user
RUN useradd -m botuser && chown -R botuser:botuser /app
USER botuser

CMD ["python3", "bot.py"]
