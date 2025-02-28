import sys
import argparse
from typing import Any

parser:argparse.ArgumentParser = argparse.ArgumentParser(sys.argv[0])
parser.add_argument("--addr", "-a", default="0.0.0.0", type=str)
parser.add_argument("--port", "-p", default=8000, type=int)
parser.add_argument("--sizex", "-x", default=100, type=int)
parser.add_argument("--sizey", "-y", default=100, type=int)
parser.add_argument("--max", "-M", default=2000, type=int)
parser.add_argument("--min", "-m", default=50, type=int)
parser.add_argument("--web-addr", "-A", default="0.0.0.0", type=str)
parser.add_argument("--web-port", "-P", default=8089, type=int)
parser.add_argument("--peak-time", "-t", default=16.0, type=float)

args:dict[str, Any] = vars(parser.parse_args(sys.argv[1:]))
addr:str = args["addr"]
port:int = args["port"]
size:tuple[int, int] = (int(args["sizex"]), int(args["sizey"]))
peak:int = args["max"]
base:int = args["min"]
web_addr:str = args["web_addr"]
web_port:int = args["web_port"]
peak_time:float = args["peak_time"]
# small hack to avoid locust dying due to argparse
sys.argv = sys.argv[:1]
