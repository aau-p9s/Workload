from datetime import datetime
from typing import Callable


start_date = datetime.now().date()

def increasing_load_shape(_load_shape: Callable) -> Callable:
    def load_shape() -> int:
        raw = _load_shape()
        today = datetime.now().date()
        scalar = (1 + (today - start_date).days) * 10
        if scalar > 100:
            return raw
        else:
            return raw * (scalar / 100)

    return load_shape
