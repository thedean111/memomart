FROM python:3.12-slim-bookworm

WORKDIR /app

# System packages required by OpenCV and hardware-related Python packages
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libusb-1.0-0 \
    swig \
    network-manager \
    v4l-utils \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY src/ ./src/
COPY web/ ./web/
COPY fonts/ ./fonts/
COPY media/ ./media/

# Flask/Gunicorn listens here
EXPOSE 8000

# Entry point
CMD ["python", "src/memomart.py"]