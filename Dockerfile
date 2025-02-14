FROM python:3.12

WORKDIR /workload

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]
