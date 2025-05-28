from csv import reader
import sys
from datetime import datetime, timedelta

from lib.args import min_delay, max_delay

user_scalar = (sum([min_delay, max_delay]) // 2) // 10

filename = "/var/agg_minute.csv"

def parse_date(string) -> datetime:
    return datetime.strptime(string, "%Y-%m-%d %H:%M:%S")

def normalize_datetime(dt) -> datetime:
    return datetime.combine(datetime.now().date(), dt.time())

with open(filename, "r") as file:
    lines = [(parse_date(line[0]), int(line[1])) for line in list(reader(file))[1:]]

old_start = lines[0][0]
relative_lines = [(time - old_start, value) for time, value in lines]
now = datetime.now()

now_mapping = { (now + delta).replace(microsecond=0, second=0) : value for delta, value in relative_lines }


def mapped_load_shape() -> int:
    now = datetime.now().replace(second=0, microsecond=0)
    return now_mapping[now]
