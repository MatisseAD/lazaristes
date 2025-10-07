# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install git (required for repository operations)
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Initialize git repository if needed (for local testing)
RUN git init || true && \
    git config --global user.email "lazaristes@example.com" || true && \
    git config --global user.name "Lazaristes" || true

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

# Run application with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "app:app"]
