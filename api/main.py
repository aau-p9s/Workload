#!/usr/bin/env python
import argparse
from http.server import ThreadingHTTPServer
import sys

from lib.api import Server
parser = argparse.ArgumentParser(sys.argv[0])
parser.add_argument("--addr", "-a", default="0.0.0.0", type=str)
parser.add_argument("--port", "-p", default=8000, type=int)

args = vars(parser.parse_args(sys.argv[1:]))
addr = args["addr"]
port = args["port"]

if __name__ == "__main__":
    try:
        http = ThreadingHTTPServer((addr, port), Server)
        http.serve_forever()
    except KeyboardInterrupt:
        print("\nexiting...")
