# syntax=docker/dockerfile:1
FROM python:3.15.0a2-alpine3.21

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

# Install deps first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY --chown=appuser:appgroup calculator.py .

USER appuser

EXPOSE 5000

CMD ["python", "calculator.py"]
