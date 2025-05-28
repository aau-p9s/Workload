from csv import reader
import sys
from datetime import datetime, timedelta

from lib.args import min_delay, max_delay

user_scalar = (sum([min_delay, max_delay]) // 2) // 10

filename = "/var/agg_minute.csv"

def parse_date(string) -> datetime:
    return datetime.strptime(string, "%Y-%m-%d %H:%M:%S")

with open(filename, "r") as file:
    lines = list(reader(file))[1:]

final = {}
start = parse_date(lines[0][0])
end = start + timedelta(days=1)
for line in lines:
    if parse_date(line[0]) >= end:
        break
    final[datetime.combine(
        datetime.now().date(),
        parse_date(line[0]).time())
    ] = int(line[1])*user_scalar


def mapped_load_shape() -> int:
    now = datetime.now().replace(second=0, microsecond=0)
    return final[now]

