#!/usr/bin/env python
import argparse
from http.server import HTTPServer, ThreadingHTTPServer
import sys
import os
from typing import Any

getEnv = lambda arg, dtype, default: dtype(os.environ[arg]) if arg in os.environ else default

from lib.api import Server
parser:argparse.ArgumentParser = argparse.ArgumentParser(sys.argv[0])
parser.add_argument("--addr", "-a", default=getEnv("WORKLOAD_ADDR", str, "0.0.0.0"), type=str)
parser.add_argument("--port", "-p", default=getEnv("WORKLOAD_PORT", int, 8000), type=int)

args:dict[str, Any] = vars(parser.parse_args(sys.argv[1:]))
addr:str = args["addr"]
port:int = args["port"]

if __name__ == "__main__":
    try:
        http:HTTPServer = ThreadingHTTPServer((addr, port), Server)
        http.serve_forever()
    except KeyboardInterrupt:
        print("\nexiting...")
