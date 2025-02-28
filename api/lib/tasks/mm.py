from typing import Any
import numpy as np

from .task import Task

class mm(Task):
    def __init__(self, size: tuple[tuple[int, int], tuple[int, int]]):
        self.size = size

    def run(self) -> Any:
        m1:np.ndarray = np.random.rand(self.size[0][0], self.size[0][1])
        m2:np.ndarray = np.random.rand(self.size[1][0], self.size[1][1])
        return m1@m2
