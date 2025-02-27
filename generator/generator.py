import time
import random
from datetime import datetime
import json
from locust import HttpUser, task, between, events

from args import size

class UserBehavior(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        pass
        
    @task(2)
    def sum_test(self):
        payload = {"x": size[0], "y": size[1]}
        
        with self.client.post("/sum", json=payload, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Status code: {response.status_code}")
    
    @task(1)
    def matmul_test(self):
        payload = {"x": size[0], "y": size[1]}
        
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
