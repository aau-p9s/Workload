from locust import HttpUser, task, between
from locust import LoadTestShape
import datetime

class StepLoadShape(LoadTestShape):
    """
    Load shape that simulates real-world traffic:
    - Morning: gradual increase
    - Afternoon: peak load around 4 PM
    - Evening: gradual decrease
    - Night: lowest traffic
    """
    def tick(self):
        now = datetime.datetime.now().hour

        if 0 <= now < 6:  # Midnight - 6 AM (Low traffic)
            users = 100
            spawn_rate = 20
        elif 6 <= now < 12:  # 6 AM - 12 PM (Increasing)
            users = 500
            spawn_rate = 50
        elif 12 <= now < 16:  # 12 PM - 4 PM (High load)
            users = 1000
            spawn_rate = 100
        elif 16 <= now < 20:  # 4 PM - 8 PM (Peak time)
            users = 2000
            spawn_rate = 150
        elif 20 <= now < 24:  # 8 PM - Midnight (Decreasing)
            users = 500
            spawn_rate = 50
        else:
            users = 100
            spawn_rate = 20  # Default safe fallback

        return users, spawn_rate


class APIUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def call_root(self):
        self.client.get("/")

    @task(2)
    def call_mm(self):
        payload = {"x": 10, "y": 20}
        self.client.post("/mm", json=payload)

    @task(1)
    def call_sum(self):
        payload = {"x": 5, "y": 15}
        self.client.post("/sum", json=payload)
