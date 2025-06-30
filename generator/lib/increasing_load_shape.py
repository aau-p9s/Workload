from datetime import datetime
from typing import Callable


start_date = datetime.now().date()

def increasing_load_shape(_load_shape: Callable) -> Callable:
    def load_shape() -> int:
        raw = _load_shape()
        today = datetime.now().date()
        scalar = (1 + (today - start_date).days)
        return raw * scalar

    return load_shape
