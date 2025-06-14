import sys
import logging
from datetime import datetime

from flask import Response
from locust.web import WebUI
from locust.env import Environment
from locust.log import setup_logging
from locust.runners import LocalRunner
import gevent
import lib.args as args

from generator import UserBehavior

setup_logging("INFO", None)
logger:logging.Logger = logging.getLogger(__name__)


def adjust_users(environment:Environment) -> None:
    if environment.runner is None:
        exit(1)
    while True:
        target_users:int = args.load_shape()
        
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

print("=" * 70)
print(" Locust Day-Night Traffic Test")
print(" Press Ctrl+C to stop the test")
print("=" * 70)

target_host:str = f"http://{args.addr}:{args.port}"

env:Environment = Environment(user_classes=[UserBehavior])

env.host = target_host
env.runner = LocalRunner(env)

web_ui:WebUI = env.create_web_ui(host=args.web_addr, port=args.web_port)

print(web_ui.app)

if web_ui.app is not None:
    @web_ui.app.route("/api/metrics")
    def get():
        if env.runner is not None:
            return Response(status=200, response=str(int(env.runner.user_count // (sum([args.min_delay, args.max_delay]) / 2))))
        else:
            exit(1)

print(f"\nLocust Web UI available at:")
print(f" * Local:    http://localhost:{args.web_port}")
print(f"\nTarget host: {target_host}")
print("\n")

env.runner.start(1, spawn_rate=1)
logger.info(f"Load test started with 1 user against {target_host}")

adjust_users_greenlet:gevent.Greenlet = gevent.spawn(adjust_users, env)

def stats_printer():
    while True:
        if env.runner is None:
            continue
        current_time:str = datetime.now().strftime("%H:%M:%S")
        current_users:int = env.runner.user_count
        target_users:int = args.load_shape()
        
        logger.info(f"[{current_time}] Active users: {current_users}, Target: {target_users}")
        logger.info(f"Requests: {env.runner.stats.total.num_requests}, " 
                   f"Failures: {env.runner.stats.total.num_failures}")
        
        gevent.sleep(60)

stats_greenlet:gevent.Greenlet = gevent.spawn(stats_printer)
    
try:
    if web_ui.greenlet is not None:
        gevent.joinall([web_ui.greenlet, adjust_users_greenlet, stats_greenlet])

except KeyboardInterrupt:
    logger.info("Shutting down...")
    sys.exit(0)
