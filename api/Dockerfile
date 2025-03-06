FROM python:3.12-slim

WORKDIR /workload

COPY ./main.py ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./lib/*.py ./lib/
COPY ./lib/tasks/*.py ./lib/tasks/


ENTRYPOINT ["python", "main.py"]
