from datetime import date
from typing import Callable

def increasing_load_shape(_load_shape: Callable, start_date: date = date.today()) -> Callable:
    def load_shape() -> int:
        raw = _load_shape()
        today = date.today()
        scalar = ((today - start_date).days / 100) * 10
        return raw + (raw * scalar)

    return load_shape
