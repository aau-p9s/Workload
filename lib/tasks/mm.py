import numpy as np

from .task import task

class mm(task):
    def run(self, size:tuple[tuple[int, int], tuple[int, int]]):
        m1 = np.random.rand(size[0][0], size[0][1])
        m2 = np.random.rand(size[1][0], size[1][1])
        res1 = m1@m2
        res2 = m2@m1
        final = res1@res2
        if final.all():
            print("success, no zeros")
        else:
            print("error, zeros present")
