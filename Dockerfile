FROM python:3.13-slim

# Install system dependencies for Playwright
RUN apt-get update && apt-get install -y \
    libgtk-4-1 libgraphene-1.0-0 libgstgl-1.0-0 \
    libgstcodecparsers-1.0-0 libenchant-2-2 libsecret-1-0 \
    libmanette-0.2-0 libgles2

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt && playwright install chromium

# Copy your app code
COPY . /app
WORKDIR /app

# Start the app
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:$PORT"]