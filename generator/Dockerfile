FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libc-dev \
    curl \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /app/
RUN pip install -r requirements.txt

COPY main.py /app/
COPY generator.py /app/

EXPOSE 8089

ENV WEB_PORT=8089
ENV WEB_HOST=0.0.0.0
ENV PYTHONUNBUFFERED=1

HEALTHCHECK --interval=5s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8089/ || exit 1

CMD ["python", "-u", "main.py"]