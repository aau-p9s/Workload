#!/usr/bin/env python
import argparse
from http.server import HTTPServer, ThreadingHTTPServer
import sys
from typing import Any

from lib.api import Server
parser:argparse.ArgumentParser = argparse.ArgumentParser(sys.argv[0])
parser.add_argument("--addr", "-a", default="0.0.0.0", type=str)
parser.add_argument("--port", "-p", default=8000, type=int)

args:dict[str, Any] = vars(parser.parse_args(sys.argv[1:]))
addr:str = args["addr"]
port:int = args["port"]

if __name__ == "__main__":
    try:
        http:HTTPServer = ThreadingHTTPServer((addr, port), Server)
        http.serve_forever()
    except KeyboardInterrupt:
        print("\nexiting...")
