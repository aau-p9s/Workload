import sys
import os
import argparse
from typing import Any, Callable

from lib.mapped_load_shape import mapped_load_shape
from lib.time_based_load_shape import time_based_load_shape
from lib.varying_mapped_load_shape import varying_mapped_load_shape

getEnv = lambda arg, dtype, default: dtype(os.environ[arg]) if arg in os.environ else default

parser:argparse.ArgumentParser = argparse.ArgumentParser(sys.argv[0])
parser.add_argument("--addr", "-a", default=getEnv("GENERATOR_API_ADDR", str, "0.0.0.0"), type=str)
parser.add_argument("--port", "-p", default=getEnv("GENERATOR_API_PORT", int, 8000), type=int)
parser.add_argument("--sizex", "-x", default=getEnv("GENERATOR_X", int, 100), type=int)
parser.add_argument("--sizey", "-y", default=getEnv("GENERATOR_Y", int, 100), type=int)
parser.add_argument("--max", "-M", default=getEnv("GENERATOR_MAX", int, 2000), type=int)
parser.add_argument("--min", "-m", default=getEnv("GENERATOR_MIN", int, 50), type=int)
parser.add_argument("--web-addr", "-A", default=getEnv("GENERATOR_ADDR", str, "0.0.0.0"), type=str)
parser.add_argument("--web-port", "-P", default=getEnv("GENERATOR_PORT", int, 8089), type=int)
parser.add_argument("--peak-time", "-t", default=getEnv("GENERATOR_PEAK", float, 16.0), type=float)
parser.add_argument("--min-delay", default=getEnv("GENERATOR_MIN_DELAY", int, 1), type=int)
parser.add_argument("--max-delay", default=getEnv("GENERATOR_MAX_DELAY", int, 3), type=int)
parser.add_argument("--shape", default=getEnv("GENERATOR_SHAPE", str, "mapped"), type=str) # mapped or sinusodal

args:dict[str, Any] = vars(parser.parse_args(sys.argv[1:]))
addr:str = args["addr"]
port:int = args["port"]
size:tuple[int, int] = (int(args["sizex"]), int(args["sizey"]))
peak:int = args["max"]
base:int = args["min"]
web_addr:str = args["web_addr"]
web_port:int = args["web_port"]
peak_time:float = args["peak_time"]
min_delay:int = args["min_delay"]
max_delay:int = args["max_delay"]
match args["shape"]:
    case "mapped":
        load_shape = mapped_load_shape(min_delay, max_delay)
    case "varying":
        load_shape = varying_mapped_load_shape(min_delay, max_delay)
    case _:
        load_shape = time_based_load_shape(base, peak, peak_time)
# small hack to avoid locust dying due to argparse
sys.argv = sys.argv[:1]
