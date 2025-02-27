import sys
import argparse

parser = argparse.ArgumentParser(sys.argv[0])
parser.add_argument("--addr", "-a", default="0.0.0.0", type=str)
parser.add_argument("--port", "-p", default=8000, type=int)
parser.add_argument("--sizex", "-x", default=100, type=int)
parser.add_argument("--sizey", "-y", default=100, type=int)
parser.add_argument("--peak", "-P", default=2000, type=int)
parser.add_argument("--base", "-b", default=50, type=int)

args = vars(parser.parse_args(sys.argv[1:]))
print(args)
addr = args["addr"]
port = args["port"]
size = (int(args["sizex"]), int(args["sizey"]))
peak = args["peak"]
base = args["base"]
# small hack to avoid locust dying due to argparse
sys.argv = sys.argv[:1]
