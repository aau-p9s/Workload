import numpy as np

from .task import task

class mm(task):
    def __init__(self, size: tuple[tuple[int, int], tuple[int, int]]):
        self.size = size

    def run(self):
        m1 = np.random.rand(self.size[0][0], self.size[0][1])
        m2 = np.random.rand(self.size[1][0], self.size[1][1])
        res = m1@m2
