from datetime import datetime
from .args import base, peak, peak_time


def time_based_load_shape() -> int:
    current_hour:int = datetime.now().hour
    current_minute:int = datetime.now().minute
    
    decimal_hour:float = current_hour + (current_minute / 60)
    
    peak_hour:float = peak_time
    
    distance_from_peak:float = min(
        abs(decimal_hour - peak_hour),
        24 - abs(decimal_hour - peak_hour)
    )
    
    max_distance:float = 13.0
    normalized_distance:float = min(distance_from_peak / max_distance, 1.0)
    
    multiplier:float = 1.0 - (0.9 * normalized_distance)
    
    base_users:int = base
    
    max_additional_users:int = peak
    
    target_users:int = base_users + int(max_additional_users * multiplier)
    
    return target_users
