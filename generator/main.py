import sys
import logging
from datetime import datetime
from lib.get_shape import time_based_load_shape
from locust.env import Environment
from locust.log import setup_logging
from locust.runners import LocalRunner
import gevent
from lib.args import addr, port, web_port, web_addr

from generator import UserBehavior

setup_logging("INFO", None)
logger:logging.Logger = logging.getLogger(__name__)


def adjust_users(environment:Environment) -> None:
    if environment.runner is None:
        exit(1)
    while True:
        target_users:int = time_based_load_shape()
        
        current_users:int = environment.runner.user_count
        print(f"{target_users=} {current_users=}")
        
        if current_users < target_users:
            spawn_count:int = target_users - current_users
            logger.info(f"Spawning {spawn_count} users to reach target of {target_users}")
            environment.runner.spawn_users({UserBehavior.__name__: spawn_count})
        elif current_users > target_users:
            stop_count:int = min(current_users - target_users, 5)
            logger.info(f"Stopping {stop_count} users to reach target of {target_users}")
            environment.runner.stop_users({UserBehavior.__name__:stop_count})
        
        gevent.sleep(10)

def main(addr:str, port:int) -> None:
    target_host:str = f"http://{addr}:{port}"
    
    env = Environment(user_classes=[UserBehavior])
    
    env.host = target_host
    env.runner = LocalRunner(env)
    
    web_ui = env.create_web_ui(host=web_addr, port=web_port)
    
    
    print(f"\nLocust Web UI available at:")
    print(f" * Local:    http://localhost:{web_port}")
    print(f"\nTarget host: {target_host}")
    print("\n")
    
    env.runner.start(1, spawn_rate=1)
    logger.info(f"Load test started with 1 user against {target_host}")
    
    adjust_users_greenlet = gevent.spawn(adjust_users, env)
    
    def stats_printer():
        while True:
            if env.runner is None:
                continue
            current_time = datetime.now().strftime("%H:%M:%S")
            current_users = env.runner.user_count
            target_users = time_based_load_shape()
            
            logger.info(f"[{current_time}] Active users: {current_users}, Target: {target_users}")
            logger.info(f"Requests: {env.runner.stats.total.num_requests}, " 
                       f"Failures: {env.runner.stats.total.num_failures}")
            
            gevent.sleep(60)
    
    stats_greenlet = gevent.spawn(stats_printer)
    
    if web_ui.greenlet is not None:
        gevent.joinall([web_ui.greenlet, adjust_users_greenlet, stats_greenlet])

if __name__ == "__main__":
    print("=" * 70)
    print(" Locust Day-Night Traffic Test")
    print(" Press Ctrl+C to stop the test")
    print("=" * 70)

    try:
        main(addr, port)
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        sys.exit(0)
