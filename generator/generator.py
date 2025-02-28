from locust import HttpUser, task, between
from locust.clients import ResponseContextManager

from lib.args import size

class UserBehavior(HttpUser):
    wait_time = between(1, 3)
    
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
    
    @task(3)
    def home_test(self):
        with self.client.get("/", catch_response=True) as response:
            if response.text == "got request...":
                if isinstance(response, ResponseContextManager):
                    response.success()
            else:
                if isinstance(response, ResponseContextManager):
                    response.failure(f"Unexpected response: {response.text}")
