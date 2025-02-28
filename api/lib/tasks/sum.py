from typing import Any
from lib.tasks.task import Task
import numpy as np


class sumTask(Task):
    def __init__(self, size:tuple[int, int]) -> None:
        self.size = size

    def run(self) -> Any:
        m:np.ndarray = np.random.rand(self.size[0], self.size[1])
        return m.sum()
