import numpy as np


def pow_sum(x, pow=2):
    return np.power(x, pow).sum()


def count_polinom(x, a):
    x = np.array([x ** i for i in range(a.size)])
    return x.dot(a.T)

