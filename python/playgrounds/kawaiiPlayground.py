from pprint import pprint
from sympy import *
import sympy
from sympy.abc import i, k, m, n, x, y, A
from sympy.polys.polyoptions import Series
from sympy import Sum, factorial, oo, IndexedBase, Function, Integer
import numpy as np


def compute_pdx(list_x, list_y, list_d, list_k, L, vertex_index):
    list_l = [x * L for x in list_d]
    m1 = vertex_index
    sum_1 = 0
    for i1 in range(len(list_x) - 1):
        if i1 != m1:
                factor_x = (list_x[i1] - list_x[m1])
                factor_y = (list_y[i1] - list_y[m1])
                factor_1 = list_l[i1][m1] * factor_x
                factor_2 = (factor_x ** 2 + factor_y ** 2) ** (1 / 2)
                summa = list_k[i1][m1] * (factor_x - factor_1 / factor_2)
                sum_1 += summa
    return sum_1


def compute_delta(list_x, list_y, list_l, list_k, vertex_index):
    return (compute_pdx(list_x, list_y, list_l, list_k, vertex_index) ** 2
            + compute_pdx(list_y, list_x, list_l, list_k, vertex_index) ** 2) ** (1 / 2)


def compute_common_denominator(x_m, x_i, y_m, y_i):
    return ((x_m - x_i) ** 2 + (y_m - y_i) ** 2) ** (3 / 2)


def compute_coefficients(list_x, list_y, list_d, list_k, L, vertex_index):
    list_l = [x * L for x in list_d]
    sum_1 = 0
    m1 = vertex_index
    for i1 in range(len(list_x) - 1):
            if i1 != m1:
                numerator = list_l[m][i](list_y[i1] - list_y[m1]) ** 2
                denominator = compute_common_denominator()
                summa = list_k[i1][m1] * (1 - numerator / denominator)
                sum_1 += summa
    sum_4 = 0
    for i1 in range(len(list_x) - 1):
            if i1 != m1:
                numerator = list_l[m][i](list_x[i1] - list_x[m1]) ** 2
                denominator = compute_common_denominator()
                summa = list_k[i1][m1] * (1 - numerator / denominator)
                sum_4 += summa
    sum_2 = 0
    for i1 in range(len(list_x) - 1):
            if i1 != m1:
                numerator = list_l[m][i](list_x[i1] - list_x[m1])(list_y[i1] - list_y[m1])
                denominator = compute_common_denominator()
                summa = list_k[i1][m1] * (numerator / denominator)
                sum_2 += summa
    coeffs = np.array([sum_1, sum_2], [sum_2, sum_4])
    vector = np.array([-compute_pdx(list_x, list_y, list_d, list_k, L,vertex_index)],
                      [-compute_pdx(list_y, list_x, list_d, list_k, L, vertex_index)])
    return coeffs, vector


def solve_sdelta(list_x, list_y, list_d, list_k, L, vertex_index):
    return np.linalg.solve(compute_coefficients(list_x, list_y, list_d, list_k, L, vertex_index))


def iterate(list_x, list_y, list_d, list_k, L, vertex_index,satisfied_diff):
    list_delta = []
    for i in range(list_x-1):
        list_delta.append(compute_delta(list_x, list_y, list_d, list_k, L, vertex_index))
    temp = max(list_delta)
    counter = 0
    while temp > satisfied_diff:
        for chosen_index in range(list_x-1):
            if compute_delta(list_x, list_y, list_d, list_k, L, chosen_index) == temp:
                while compute_delta(list_x, list_y, list_d, list_k, L, chosen_index) > satisfied_diff:
                    movement_x, moment_y = solve_sdelta(list_x, list_y, list_d, list_k, L, vertex_index)
                    list_x[vertex_index] += movement_x
                    list_y[vertex_index] += movement_x
                    counter += 1
                    if counter > 1000:
                        print("break for overlooping: "+counter)
                        break

    print("terminated normally")


def o(x):
    return x + 1


L = 3

x, i = symbols("x i")
s = Sum(Indexed('x', 0) + Indexed('x', o(i)), (i, 0, 1))
f = lambdify(x, s)
pdxm = 0
b = [0, 2, 3, 3]
l = [[1, 2, 1, 2], [3, 4, 3, 4], [5, 6, 6, 7], [5, 6, 6, 7]]
print(f(b))

sum1 = 0
for i1 in range(len(b) - 1):
    for m1 in range(len(b) - 1):
        if i1 != m1:
            sum1 += l[i1][m1] * (b[i1] - b[m1])

print(sum1)
