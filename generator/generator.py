from time import time
from typing import Any
from locust import HttpUser, task, between
from locust.clients import ResponseContextManager

from lib.args import size, min_delay, max_delay

class UserBehavior(HttpUser):
    wait_time = between(min_delay, max_delay)
    metrics: dict[int, dict[str, Any]] = {}
    
    def on_start(self):
        pass
        
    @task(2)
    def sum_test(self):
        payload:dict[str, int] = {"x": size[0], "y": size[1]}
        
        with self.client.post("/sum", json=payload, catch_response=True) as response:
            if response.status_code == 200:
                if isinstance(response, ResponseContextManager):
                    response.success()
            else:
                if isinstance(response, ResponseContextManager):
                    response.failure(f"Status code: {response.status_code}")
        self.log("/sum")
    
    @task(1)
    def matmul_test(self):
        payload:dict[str, int] = {"x": size[0], "y": size[1]}
        
        with self.client.post("/mm", json=payload, catch_response=True) as response:
            if response.status_code == 200:
                if isinstance(response, ResponseContextManager):
                    response.success()
            else:
                if isinstance(response, ResponseContextManager):
                    response.failure(f"Status code: {response.status_code}")
        self.log("/mm")
    
    @task(3)
    def home_test(self):
        with self.client.get("/", catch_response=True) as response:
            if response.text == "got request...":
                if isinstance(response, ResponseContextManager):
                    response.success()
            else:
                if isinstance(response, ResponseContextManager):
                    response.failure(f"Unexpected response: {response.text}")
        self.log("/")

    def log(self, endpoint: str):
        self.metrics[int(time())] = { "wait_time":self.wait_time(), "endpoint": endpoint }
