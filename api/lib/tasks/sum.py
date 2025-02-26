from lib.tasks.task import task
import numpy as np


class sumTask(task):
    def __init__(self, size:tuple[int, int]) -> None:
        self.size = size

    def run(self):
        m = np.random.rand(self.size[0], self.size[1])
        return m.sum()
