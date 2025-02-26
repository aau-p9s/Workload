import time
import random
from datetime import datetime
import json
from locust import HttpUser, task, between, events

class UserBehavior(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        pass
        
    @task(2)
    def sum_test(self):
        x = random.randint(1, 100)
        y = random.randint(1, 100)
        payload = {"x": x, "y": y}
        
        with self.client.post("/sum", json=payload, catch_response=True) as response:
            try:
                expected = str(x + y)
                if response.text == expected:
                    response.success()
                else:
                    response.failure(f"Got {response.text}, expected {expected}")
            except Exception as e:
                response.failure(f"Exception: {str(e)}")
    
    @task(1)
    def matmul_test(self):
        x = random.randint(1, 10)
        y = random.randint(1, 10)
        payload = {"x": x, "y": y}
        
        with self.client.post("/mm", json=payload, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Status code: {response.status_code}")
    
    @task(3)
    def home_test(self):
        with self.client.get("/", catch_response=True) as response:
            if response.text == "got request...":
                response.success()
            else:
                response.failure(f"Unexpected response: {response.text}")