FROM python:3.12

WORKDIR /workload

COPY ./main.py ./requirements.txt .
COPY ./lib/*.py ./lib/
COPY ./lib/tasks/*.py ./lib/tasks/


RUN pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]