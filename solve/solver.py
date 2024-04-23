# from print import print

import numpy as np
from numpy.linalg import solve as slae_solve

from sympy.abc import x as X
from sympy import exp, log
from solve.utils import *


def deter_coef(act_y, f_y):
    s1 = sum([(a_y_i - f_y_i) ** 2 for a_y_i, f_y_i in zip(act_y, f_y)])
    s = sum(act_y) / len(act_y)
    s2 = sum([(a_y_i - s) ** 2 for a_y_i, f_y_i in zip(act_y, f_y)])
    return 1 - s1 / s2


def pirson_coef(x, y):
    x = np.array(x)
    y = np.array(y)

    x_ = x.mean()
    y_ = y.mean()

    # sum([ (x_i - x_) * (y_i - y_) for x_i, y_i in zip(x, y)])
    s1 = np.dot((x - x_), (y - y_).T)

    s2 = (x - x_).dot((x - x_).T) * (y - y_).dot((y - y_).T)

    return s1 / np.sqrt(s2)


def do_linear(x, y, pow=1):
    matrix = list()
    b = list()

    for i in range(pow + 1):
        matrix.append(
            [pow_sum(x, i + j) for j in range(pow + 1)])  # [pow_sum(x, i), pow_sum(x, i + 1), pow_sum(x, i + 2)]
        b.append(sum([x_i ** i * y_i for x_i, y_i in zip(x, y)]))

    A = slae_solve(np.array(matrix), np.array(b))

    func = lambda x: count_polinom(x, A)

    new_y = [func(i) for i in x]
    S = sum([(res - target) ** 2 for res, target in zip(new_y, y)])
    return [x, new_y], S, A


def do_tetra(x, y):
    table, s, a = do_linear(x, y, 3)
    return table, s, sum([X ** i * a[i] for i in range(4)])


def do_quadratic(x, y):
    table, s, a = do_linear(x, y, 2)
    return table, s, sum([X ** i * a[i] for i in range(3)])


def do_line(x, y):
    table, s, a = do_linear(x, y)
    return table, s, sum([X ** i * a[i] for i in range(2)]), pirson_coef(x, y)


def do_exp(x, y):  # a*e^(bx)
    y = np.log(y)
    table, s, a = do_linear(x, y)
    a[0] = np.exp(a[0])
    return table, s, a[0] * exp(X * a[1])


def do_pow(x, y):  # a*x^b
    x = np.log(x)
    y = np.log(y)
    table, s, a = do_linear(x, y)
    a[0] = np.exp(a[0])
    return table, s, a[0] * X ** a[1]


def do_log(x, y):  # a*ln(x) + b
    x = np.log(x)
    table, s, a = do_linear(x, y)

    return table, s, a[1] * log(X) + a[0]


def approximate_func(x, y):
    if (len(x) == 1):
        return 0, X * 0 + y[0], 1
    f_list = [
        do_line,
        do_pow,
        do_exp,
        do_log
    ]
    if (len(x) >= 3):
        f_list.append(do_quadratic)
    if (len(x) >= 4):
        f_list.append(do_tetra)

    res_r = {'max': -1000, 'res': None}
    res_s = {'max': -1000, 'res': None}
    for f_i in range(len(f_list)):
        f = f_list[f_i]
        print(f_i)
        if (f in [do_pow, do_log]) and (np.array(x) <= 0).any():
            continue
        if (f == do_exp) and (np.array(y) <= 0).any():
            continue
        vars = f(x, y) # table, s, a, pirson

        if f in [do_exp, do_pow]:
            c = deter_coef(np.log(y), vars[0][1])
        else:
            c = deter_coef(y, vars[0][1])

        if res_r['max'] < c:
            res_r['max'] = c
            res_r['res'] = vars[1:]

        if res_s['max'] < vars[1]:
            res_s['max'] = vars[1]
            res_s['res'] = vars[1:]
        # print(*a, s, c, sep='\t')
        # print('===')
    if res_r['max'] != -1000:
        return *res_r['res'], res_r['max']
    return *res_s['res'], res_s['max']


if __name__ == '__main__':
    x = np.linspace(-2, 0, int(2 / 0.2)+1)
    f = lambda x: 23*x/(x**4 + 7)
    y = np.vectorize(f)(x)
    print(*[round(i, 3) for i in x], sep='\t')
    print(*[round(i, 3) for i in y], sep='\t')
    print(approximate_func(x, y))

    exit()
    x = np.linspace(0.2, 2, int(2 / 0.2))
    f = lambda x: 56 * x - 72
    y = np.vectorize(f)(x)
    print(do_line(x, y)[2])

    f = lambda x: 3 * x ** 2 - 4.5 * x + 7.8
    y = np.vectorize(f)(x)
    print(do_quadratic(x, y)[2])

    f = lambda x: 3 * x ** 3 - 3.3 * x ** 2 - 41.25 * x + 17.8
    y = np.vectorize(f)(x)
    print(do_tetra(x, y)[2])

    f = lambda x: 38 * np.exp(x * 15)
    y = np.vectorize(f)(x)
    print(do_exp(x, y)[2])

    f = lambda x: 45 * x ** 16
    y = np.vectorize(f)(x)
    print(do_pow(x, y)[2])

    f = lambda x: 13 * np.log(x) - 78
    y = np.vectorize(f)(x)
    print(do_log(x, y)[2])
