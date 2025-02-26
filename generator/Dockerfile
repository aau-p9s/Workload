FROM locustio/locust:2.23.0

WORKDIR /locust

COPY . .

RUN pip install --no-cache-dir -r ../requirements.txt

EXPOSE 8089

CMD ["locust", "-f", "main.py"]