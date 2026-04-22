FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ── Persistent volume on HF Spaces is mounted at /data ──────────────────────
# We create it here so the container works even without the volume mount.
RUN mkdir -p /data /app/uploads /app/data

ENV DATA_DIR=/data
ENV PORT=7860
ENV PYTHONUNBUFFERED=1
# Set to "true" only if the Space is served over HTTPS (HF Spaces default)
ENV SESSION_COOKIE_SECURE=false

EXPOSE 7860

# Single worker — HF Spaces free tier is CPU-limited.
# threads=4 allows concurrent request handling without multiple processes.
CMD ["gunicorn", \
     "--bind", "0.0.0.0:7860", \
     "--workers", "1", \
     "--threads", "4", \
     "--timeout", "120", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "app:app"]
