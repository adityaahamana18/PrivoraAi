# Multi-stage Dockerfile for Privora AI Platform
# Stage 1: Build React Frontend
FROM node:18-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Setup Python FastAPI Backend & Serve Frontend
FROM python:3.11-slim
WORKDIR /app

# Install system dependencies for scipy & openpyxl
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy backend code & sample data
COPY backend/ ./backend/
COPY data/ ./data/
COPY models/ ./models/
COPY reports/ ./reports/

# Copy built frontend assets to backend static directory
COPY --from=frontend-builder /app/frontend/dist ./frontend_dist

# Environment variables
ENV PORT=8000
EXPOSE 8000

# Start FastAPI server
CMD ["python", "backend/main.py"]
