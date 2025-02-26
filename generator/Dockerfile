FROM python:3.11-slim
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    locust==2.19.1 \
    greenlet==2.0.2 \
    gevent==23.9.1 \
    requests==2.31.0

COPY generator.py /app/
COPY main.py /app/

RUN touch /app/__init__.py

# Expose port for Locust web interface
EXPOSE 8089

ENV TARGET_HOST=http://localhost:8000
ENV WEB_PORT=8089
ENV WEB_HOST=0.0.0.0

HEALTHCHECK --interval=5s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8089/ || exit 1

ENTRYPOINT ["python", "main.py"]