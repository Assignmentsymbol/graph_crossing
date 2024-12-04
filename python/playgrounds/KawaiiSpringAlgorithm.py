from pprint import pprint
import random
import networkx as nx
from sympy import *
import sympy
from sympy.abc import i, k, m, n, x, y, A
from sympy.polys.polyoptions import Series
from sympy import Sum, factorial, oo, IndexedBase, Function, Integer
import numpy as np


def compute_pdx(list_x, list_y, dict_d, dict_k, L, vertex_index):
    dict_l = {v1: {v2: dis * L for v2, dis in dict_d[v1].items()} for v1 in dict_d}
    print("logging")
    print(dict_l[0][6])
    print("logging")
    m1 = vertex_index
    sum_1 = 0
    for i1 in range(len(list_x)):
        if i1 != m1:
            diff_x = (list_x[m1] - list_x[i1])
            # print("log1: " + str(diff_x))
            diff_y = (list_y[m1] - list_y[i1])
            numerator = dict_l[i1][m1] * diff_x
            denominator = (diff_x ** 2 + diff_y ** 2) ** (1 / 2)
            summa = dict_k[i1][m1] * (diff_x - numerator / denominator)
            sum_1 += summa
    return sum_1


def compute_delta(list_x, list_y, dict_l, dict_k, L, vertex_index):
    temp = (compute_pdx(list_x, list_y, dict_l, dict_k, L, vertex_index) ** 2
            + compute_pdx(list_y, list_x, dict_l, dict_k, L, vertex_index) ** 2) ** (1 / 2)
    return temp


def compute_common_denominator(x_m, x_i, y_m, y_i):
    return ((x_m - x_i) ** 2 + (y_m - y_i) ** 2) ** (3 / 2)


def convert_distance_to_length(dict_d, L):
    return {v1: {v2: dis * L for v2, dis in dict_d[v1].items()} for v1 in dict_d}


def compute_coefficients(list_x, list_y, dict_d, dict_k, L, vertex_index):
    size = len(list_x)
    dict_l = convert_distance_to_length(dict_d, L)
    m1 = vertex_index
    pdx_square = 0
    for i1 in range(size):
        if i1 != m1:
            numerator = dict_l[m1][i1] * (list_y[m1] - list_y[i1]) ** 2
            denominator = compute_common_denominator(list_x[m1], list_x[i1],
                                                     list_y[m1], list_y[i1])
            summa = dict_k[m1][i1] * (1 - numerator / denominator)
            pdx_square += summa
    pdy_square = 0
    for i1 in range(size):
        if i1 != m1:
            numerator = dict_l[m1][i1] * (list_x[m1] - list_x[i1]) ** 2
            denominator = compute_common_denominator(list_x[m1], list_x[i1],
                                                     list_y[m1], list_y[i1])
            summa = dict_k[m1][i1] * (1 - numerator / denominator)
            pdy_square += summa
    pdxy = 0
    for i1 in range(size):
        if i1 != m1:
            numerator = dict_l[m1][i1] * (list_x[m1] - list_x[i1]) * (list_y[m1] - list_y[i1])
            denominator = compute_common_denominator(list_x[m1], list_x[i1],
                                                     list_y[m1], list_y[i1])
            summa = dict_k[m1][i1] * (numerator / denominator)
            pdxy += summa

    coeffs = np.array([[pdx_square, pdxy], [pdxy, pdy_square]])
    vector = np.array([-compute_pdx(list_x, list_y, dict_d, dict_k, L, vertex_index),
                       -compute_pdx(list_y, list_x, dict_d, dict_k, L, vertex_index)])
    return coeffs, vector


def solve_sdelta(list_x, list_y, list_d, list_k, L, vertex_index):
    a, b = compute_coefficients(list_x, list_y, list_d, list_k, L, vertex_index)
    return np.linalg.solve(a, b)


def iterate(list_x, list_y, dict_d, list_k, L, vertex_index, satisfied_diff, drawing_range):
    list_delta = []
    for i in range(len(list_x)):
        list_delta.append(compute_delta(list_x, list_y, dict_d, list_k, L, vertex_index))
    temp = max(list_delta)
    max_index = list_delta.index(temp)
    counter = 0
    while temp > satisfied_diff:
        if counter > 20:
            print("break for overlooping: " + str(counter))
            break
        while compute_delta(list_x, list_y, dict_d, list_k, L, vertex_index) > satisfied_diff:
            movement_x, movement_y = solve_sdelta(list_x, list_y, dict_d, list_k, L, vertex_index)
            # list_x[vertex_index] += movement_x
            # list_y[vertex_index] += movement_y
            temp_x = list_x[vertex_index] + movement_x
            temp_y = list_y[vertex_index] + movement_y
            counter += 1
            print(counter)
            if counter > 20:
                print("break for overlooping: " + str(counter))
                break
            elif temp_x in list_x and temp_y in list_y:
                continue
            elif temp_x > drawing_range[0] or temp_y > drawing_range[1] or temp_x < 0 or temp_y < 0:
                continue
            else:
                list_x[vertex_index] = temp_x
                list_y[vertex_index] = temp_y
                list_delta[vertex_index] = compute_delta(list_x, list_y, dict_d, list_k, L, vertex_index)
                temp = max(list_delta)
                vertex_index = list_delta.index(temp)



    temp2 = []
    for i in range(len(list_x)):
        temp2.append((list_x[i], list_y[i]))
        # print(temp2)
    new_pos = {node: temp2[node] for node in range(len(list_x))}
    print(new_pos)
    print("terminated normally")
    print(new_pos[19])
    return new_pos


def data_convertor(graph, pos: dict, L, K, satisfied_diff, d_range):
    list_x = [pos[vertex][0] for vertex in sorted(pos, key=int)]
    list_y = [pos[vertex][1] for vertex in sorted(pos, key=int)]
    temp = nx.floyd_warshall(graph, weight="weight")
    # default self connected
    dict_d = {a: dict(b) for a, b in temp.items()}
    filtered = {v1: {v2: dis for v2, dis in dict_d[v1].items() if dis != 0} for v1 in dict_d}
    dict_d = filtered
    print(dict_d)
    dict_k = {x1: {x2: K / y ** 2 for x2, y in dict_d[x1].items()} for x1 in dict_d}
    random_pick = random.choice(list(graph.nodes))
    return list_x, list_y, dict_d, dict_k, L, random_pick, satisfied_diff, d_range
