import os
import sys
import time
import logging
from datetime import datetime
from locust import HttpUser, task, between, events
from locust.env import Environment
from locust.stats import stats_printer, stats_history
from locust.log import setup_logging
from locust.runners import MasterRunner, LocalRunner
import gevent

from generator import UserBehavior

setup_logging("INFO", None)
logger = logging.getLogger(__name__)

def time_based_load_shape():
    current_hour = datetime.now().hour
    current_minute = datetime.now().minute
    
    decimal_hour = current_hour + (current_minute / 60)
    
    peak_hour = 16.0
    trough_hour = 3.0
    
    distance_from_peak = min(
        abs(decimal_hour - peak_hour),
        24 - abs(decimal_hour - peak_hour)
    )
    
    max_distance = 13.0
    normalized_distance = min(distance_from_peak / max_distance, 1.0)
    
    multiplier = 1.0 - (0.9 * normalized_distance)
    
    base_users = 50
    max_additional_users = 2000
    
    target_users = base_users + int(max_additional_users * multiplier)
    
    return target_users

def adjust_users(environment):
    start_time = time.time()
    
    while True:
        target_users = time_based_load_shape()
        
        current_users = environment.runner.user_count
        
        if current_users < target_users:
            spawn_count = target_users - current_users
            logger.info(f"Spawning {spawn_count} users to reach target of {target_users}")
            environment.runner.spawn_users({UserBehavior.__name__: spawn_count})
        elif current_users > target_users:
            stop_count = min(current_users - target_users, 5)
            logger.info(f"Stopping {stop_count} users to reach target of {target_users}")
            environment.runner.stop_users(stop_count)
        
        gevent.sleep(10)

def main():
    web_host = os.environ.get("WEB_HOST", "0.0.0.0")
    web_port = int(os.environ.get("WEB_PORT", 8089))
    target_host = os.environ.get("TARGET_HOST", "http://localhost:8000")
    
    env = Environment(user_classes=[UserBehavior])
    
    env.host = target_host
    env.runner = LocalRunner(env)
    
    web_ui = env.create_web_ui(host=web_host, port=web_port)
    
    
    print(f"\nLocust Web UI available at:")
    print(f" * Local:    http://localhost:{web_port}")
    print(f"\nTarget host: {target_host}")
    print("\n")
    
    env.runner.start(1, spawn_rate=1)
    logger.info(f"Load test started with 1 user against {target_host}")
    
    adjust_users_greenlet = gevent.spawn(adjust_users, env)
    
    def stats_printer():
        while True:
            current_time = datetime.now().strftime("%H:%M:%S")
            current_users = env.runner.user_count
            target_users = time_based_load_shape()
            
            logger.info(f"[{current_time}] Active users: {current_users}, Target: {target_users}")
            logger.info(f"Requests: {env.runner.stats.total.num_requests}, " 
                       f"Failures: {env.runner.stats.total.num_failures}")
            
            gevent.sleep(60)
    
    stats_greenlet = gevent.spawn(stats_printer)
    
    gevent.joinall([web_ui.greenlet, adjust_users_greenlet, stats_greenlet])

if __name__ == "__main__":
    print("=" * 70)
    print(" Locust Day-Night Traffic Test")
    print(" Press Ctrl+C to stop the test")
    print("=" * 70)
    
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        sys.exit(0)