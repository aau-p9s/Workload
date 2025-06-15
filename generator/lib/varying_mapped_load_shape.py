from csv import reader
from datetime import datetime, timedelta
from typing import Callable

def flip(start: datetime, target: datetime) -> bool:
    return abs((start - target).days) % 2 == 0

def parse_date(string) -> datetime:
    return datetime.strptime(string, "%Y-%m-%d %H:%M:%S")

def varying_mapped_load_shape(min_delay, max_delay) -> Callable:

    user_scalar = (sum([min_delay, max_delay]) // 2)
    
    filename = "/var/agg_minute.csv"
   
    with open(filename, "r") as file:
        lines = [(parse_date(line[0]), int(line[1])) for line in list(reader(file))[1:]]
    
    old_start = lines[0][0]
    relative_lines = [(time - old_start, value) for time, value in lines]
    now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) # reset to midnight
    
    now_mapping = { (now + delta).replace(microsecond=0, second=0) : value for delta, value in relative_lines }
    max_value = max(now_mapping.values())
    
    flipped_mapping = { time : value if flip(now, time) else max_value - value for time, value in now_mapping.items() }
    
    def load_shape() -> int:
        now = datetime.now().replace(second=0, microsecond=0)
        return flipped_mapping[now] // user_scalar

    return load_shape
