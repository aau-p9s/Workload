#!/usr/bin/env python
import argparse
from http.server import HTTPServer, ThreadingHTTPServer
import sys
import os
from time import sleep
from typing import Any

getEnv = lambda arg, dtype, default: dtype(os.environ[arg]) if arg in os.environ else default

from lib.api import Server
parser:argparse.ArgumentParser = argparse.ArgumentParser(sys.argv[0])
parser.add_argument("--addr", "-a", default=getEnv("WORKLOAD_ADDR", str, "0.0.0.0"), type=str)
parser.add_argument("--port", "-p", default=getEnv("WORKLOAD_PORT", int, 8000), type=int)
parser.add_argument("--delay", "-d", default=getEnv("WORKLOAD_STARTUP_DELAY", int, 0), type=int)

args:dict[str, Any] = vars(parser.parse_args(sys.argv[1:]))
addr:str = args["addr"]
port:int = args["port"]
delay:int = args["delay"]

sleep(delay)
with open("/var/ready", "w") as file:
    file.write("ready")

if __name__ == "__main__":
    try:
        http:HTTPServer = ThreadingHTTPServer((addr, port), Server)
        http.serve_forever()
    except KeyboardInterrupt:
        print("\nexiting...")
