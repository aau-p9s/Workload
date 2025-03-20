FROM python:3.12-slim

WORKDIR /generator

RUN apt-get update && apt-get install -y --no-install-recommends \
    libc-dev \
    curl \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt .
RUN pip install -r ./requirements.txt

COPY ./*.py .
COPY ./lib/*.py ./lib/

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python", "main.py"]
