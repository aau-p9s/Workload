from locust import run_single_user
from locust.env import Environment
from locust.stats import stats_printer, stats_history
from locust.log import setup_logging
import gevent
from api_test import APIUser, StepLoadShape

def run_locust():
    setup_logging()

    env = Environment(user_classes=[APIUser], shape_class=StepLoadShape)
    env.create_web_ui("localhost", 8089)
    env.create_runner()

    gevent.spawn(stats_printer(env.stats))
    gevent.spawn(stats_history, env.runner)

    # Run test indefinitely
    env.runner.start(user_count=10, spawn_rate=2)  # Initial users
    env.runner.greenlet.join()  # Keep running

if __name__ == "__main__":
    run_locust()
