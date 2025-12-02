# Build from the repository root:
#   docker build -f backend/Dockerfile -t docs-events-api .
FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ .
RUN mkdir -p /app/data
ENV PYTHONPATH=/app/src
ENV DATA_DIR=/app/data
EXPOSE 8000
CMD ["uvicorn", "src.main:backend_app", "--host", "0.0.0.0", "--port", "8000"]
