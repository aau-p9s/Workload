#!/usr/bin/env python
import argparse
import sys

from lib.tasks.mm import mm

parser = argparse.ArgumentParser(sys.argv[0])
parser.add_argument("--size1", "-1", default="1000x1000")
parser.add_argument("--size2", "-2", default="1000x1000")

args = vars(parser.parse_args(sys.argv[1:]))

size1 = [int(n) for n in args["size1"].split("x")]
size2 = [int(n) for n in args["size2"].split("x")]

if __name__ == "__main__":
    task = mm()
    while True:
        task.run((size1, size2))
