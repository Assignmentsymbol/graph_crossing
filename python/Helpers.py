import networkx
import networkx as nwx
import matplotlib.pyplot as plt
import numpy as np
import random

import KawaiiSpringAlgorithm
from IntersectAlgorithm import Point
from IntersectAlgorithm import doIntersect
import RandomizedCrossingMinimization as rcm
import os
import json
import HeuristicAlgorithm as hrt


def show_grid():
    plt.grid('on')
    plt.axhline(0, color='black', linewidth=1)  # x axe
    plt.axvline(0, color='black', linewidth=1)
    for i in range(-1, 20):
        # adding integer dots
        plt.text(i, -0.1, str(i), ha='center', va='center', color="blue")
        plt.text(-0.3, i, str(i), ha='center', va='center', color="blue")
    # trivial stuff
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Some drawing")


def is_intersect(edge1: tuple[str], edge2: tuple[str], pos: dict, silent: bool):
    e1p1 = Point(pos[edge1[0]][0], pos[edge1[0]][1])
    e1p2 = Point(pos[edge1[1]][0], pos[edge1[1]][1])
    e2p1 = Point(pos[edge2[0]][0], pos[edge2[0]][1])
    e2p2 = Point(pos[edge2[1]][0], pos[edge2[1]][1])

    if not silent:
        if doIntersect(e1p1, e1p2, e2p1, e2p2):
            print("Intersected")
        else:
            print("Not intersected")
    if doIntersect(e1p1, e1p2, e2p1, e2p2):
        return True
    else:
        return False


def load_file_hard():
    current_directory = os.getcwd()
    # print("Current Directory:", current_directory)
    with open(current_directory + r"/examples/ex1_k6_xr32.json", 'r') as file:
        data = json.load(file)
        return data


def load_file():
    file_path = input("Please input absolute file path(If no valid path is given, a default file"
                      "will be used.): ")
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except Exception as e:
        print("Exception occurs, a default file is used.")
        return load_file_hard()


def data_process(data: dict):
    nodes_data = data["nodes"]
    nodes = []
    attributes = []
    edges = []
    pos = {}
    width = data["width"]
    height = data["height"]
    for dct in nodes_data:
        nodes.append(dct["id"])
        coordinate = dct['x'], dct['y']
        attributes.append(coordinate)
        pos[dct["id"]] = dct['x'], dct['y']
    for dct in data['edges']:
        temp = (dct["source"]), (dct["target"])
        edges.append(temp)
    graph = nwx.Graph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)
    return graph, nodes, edges, attributes, pos, width, height


def save_file(graph: networkx.Graph, pos, width, height):
    user_input = input("Do you want to save file?[y/n]: ")
    if user_input == "y":
        # print("said yes")
        current_directory = os.getcwd()
        # data_testing = {"node": {"id": 1, "di": 2}}
        data_out = {}
        nodes = []
        edges = []
        for node in graph.nodes:
            nodes.append({"id": node, "x": pos[node][0], "y": pos[node][1]})
        for edge in graph.edges:
            edges.append({"source": edge[0], "target": edge[1]})
        data_out["nodes"] = nodes
        data_out["edges"] = edges
        data_out["width"] = 0
        data_out["height"] = 0
        data_out["width"] = width
        data_out["height"] = height

        with open(os.path.join(current_directory, "output.json"), 'w', encoding='utf-8') as file:
            json.dump(data_out, file, indent=4, ensure_ascii=False)
            print("total: " + check_total(graph.edges, pos).__str__())
            print("File saved")


    elif user_input == 'n':
        # print("said no")
        print("Terminated without saving")
        return
    else:
        save_file(graph)


def perform_operation_for_single_change(positions: dict, graph: networkx.Graph):
    new_position = (random.randint(0, 13), random.randint(0, 13))
    random_node = random.choice(list(graph.nodes))
    positions[random_node] = new_position


def check_total(edges, pos):
    max_Value = 0
    total = 0
    local_max = 0
    worst_edge = ()
    for edge_1 in edges:
        max_Value = max(max_Value, local_max)
        local_max = 0
        for edge_2 in [x for x in edges if x != edge_1]:
            if is_intersect(edge_1, edge_2, pos, True):
                total += 1
                local_max += 1
                if local_max > max_Value:
                    worst_edge = edge_1
    total /= 2
    print('One edge with most crossings is: ' + worst_edge.__str__())
    print('The maximum value of crossings in a single edge is: ' + max_Value.__str__())
    print('The total number of the crossings is: ' + total.__str__())
    return total


def check_total_silence(edges, pos):
    max_Value = 0
    total = 0
    local_max = 0
    worst_edge = ()
    for edge_1 in edges:
        max_Value = max(max_Value, local_max)
        local_max = 0
        for edge_2 in [x for x in edges if x != edge_1]:
            if is_intersect(edge_1, edge_2, pos, True):
                total += 1
                local_max += 1
                if local_max > max_Value:
                    worst_edge = edge_1
    total /= 2
    return total


def report_and_draw(graph, edges, new_pos):
    check_total(edges, new_pos)
    nwx.draw_networkx(graph, pos=new_pos, with_labels=True, node_color="red", node_size=100,
                      font_color="white", font_size=10, font_family="Times New Roman",
                      font_weight="bold", width=1, edge_color="black")
    plt.margins(0.2)
    show_grid()
    plt.show()


def initial_report(edges, pos, graph):
    check_total(edges, pos)
    plt.figure()
    nwx.draw_networkx(graph, pos=pos, with_labels=True, node_color="red", node_size=100,
                      font_color="white", font_size=10, font_family="Times New Roman",
                      font_weight="bold", width=1, edge_color="black")
    plt.margins(0.2)
    show_grid()
    plt.show()


def check_identical(pos_old, pos_new):
    if pos_old == pos_new:
        print("This optimization cycle results the identical position...")
        return True
    else:
        print("Position changed...")
        return False


def ask_for_random_movement(graph, pos, edges):
    inputString = input("Do you want to perform a random change?[y/n]")
    if inputString == "y":
        perform_operation_for_single_change(pos, graph)
        report_and_draw(graph, edges, pos)
        ask_for_random_movement(graph, pos, edges)


def ask_for_kawaii_movement(graph, pos, L, K, satisfied_diff, edges, d_range):
    input_string = input("Do you want to perform spring balance?[y/n]")
    if input_string == "y":
        new_pos = KawaiiSpringAlgorithm.iterate(
            *KawaiiSpringAlgorithm.data_convertor(graph, pos, L, K, satisfied_diff, d_range))
        print(".........optimization circle terminated.........")
        report_and_draw(graph, edges, new_pos)
        ask_for_kawaii_movement(graph, pos, L, K, satisfied_diff, edges, d_range)
    elif input_string == '2':
        pass


def ask_for_trivial_random_optimization(edges, graph, pos, times, width, height):
    old_copy = pos.copy()
    input_string = input("Do you want to perform a trivial random optimization?[y/n]")
    new_pos = pos
    if input_string == "y":
        new_pos = rcm.random_optimization_trivial(edges, graph, pos, times, width, height)
        print(".........optimization circle terminated.........")
        report_and_draw(graph, edges, new_pos)
        check_identical(old_copy, new_pos)
        new_pos = ask_for_trivial_random_optimization(edges, graph, new_pos, times, width, height)
    elif input_string == 'e' or input_string == '4':
        ask_for_random_exchange_optimization(edges, graph, pos, times, width, height)
    elif input_string == 'c' or input_string == '2':
        ask_for_combined_optimization(edges, graph, pos, times, width, height)
    elif input_string == 'h' or input_string == '3':
        ask_for_heuristic_with_given_function(edges, graph, pos, times, width, height)
    return new_pos


def ask_for_random_exchange_optimization(edges, graph, pos, times, width, height):
    old_copy = pos.copy()
    input_string = input("Do you want to perform a random exchange optimization?[y/n]")
    new_pos = pos
    if input_string == "y":
        new_pos = rcm.random_optimization_exchange(edges, graph, pos, times, width, height)
        print(".........optimization circle terminated.........")
        report_and_draw(graph, edges, new_pos)
        check_identical(old_copy, new_pos)
        new_pos = ask_for_random_exchange_optimization(edges, graph, new_pos, times, width, height)
    elif input_string == 't' or input_string == '1':
        ask_for_trivial_random_optimization(edges, graph, pos, times, width, height)
    elif input_string == 'c' or input_string == '2':
        ask_for_combined_optimization(edges, graph, pos, times, width, height)
    elif input_string == 'h' or input_string == '3':
        ask_for_heuristic_with_given_function(edges, graph, pos, times, width, height)
    return new_pos


def ask_for_combined_optimization(edges, graph, pos, times, width, height):
    old_copy = pos.copy()
    input_string = input("Do you want to perform a combined random optimization?[y/n]")
    new_pos = pos
    if input_string == "y":
        new_pos = rcm.combined_randomized_opt(edges, graph, pos, times, width, height)
        print(".........(combined)optimization circle terminated.........")
        report_and_draw(graph, edges, new_pos)
        check_identical(old_copy, new_pos)
        new_pos = ask_for_combined_optimization(edges, graph, new_pos, times, width, height)
    elif input_string == 't' or input_string == '1':
        ask_for_trivial_random_optimization(edges, graph, pos, times, width, height)
    elif input_string == 'e' or input_string == '4':
        ask_for_random_exchange_optimization(edges, graph, pos, times, width, height)
    elif input_string == 'h' or input_string == '3':
        ask_for_heuristic_with_given_function(edges, graph, pos, times, width, height)
    return new_pos


def ask_for_heuristic_with_given_function(edges, graph, pos, times, width, height):
    old_copy = pos.copy()
    input_string = input("Do you want to perform a heuristic optimization?[y/n]")
    new_pos = pos
    if input_string == "y":
        new_pos = hrt.heuristic_with_random(edges, graph, pos, times, width, height, hrt.diameter_induced_function)
        print(".........heuristic optimization circle terminated.........")
        report_and_draw(graph, edges, new_pos)
        check_identical(old_copy, new_pos)
        new_pos = ask_for_heuristic_with_given_function(edges, graph, new_pos, times, width, height)
    elif input_string == 't' or input_string == '1':
        ask_for_trivial_random_optimization(edges, graph, pos, times, width, height)
    elif input_string == 'e' or input_string == '4':
        ask_for_random_exchange_optimization(edges, graph, pos, times, width, height)
    elif input_string == 'c' or input_string == '2':
        ask_for_combined_optimization(edges, graph, pos, times, width, height)
    return new_pos


def ask_for_simulate_annealing(edges, graph, pos, times, width, height):
    old_copy = pos.copy()
    input_string = input("Do you want to perform a SA optimization?[y/n]")
    new_pos = pos
    if input_string == "y":
        new_pos = hrt.heuristic_with_random(edges, graph, pos, times, width, height, hrt.diameter_induced_function)
        print(".........SA circle terminated.........")
        report_and_draw(graph, edges, new_pos)
        check_identical(old_copy, new_pos)
        new_pos = ask_for_simulate_annealing(edges, graph, new_pos, times, width, height)
    elif input_string == 't' or input_string == '1':
        ask_for_trivial_random_optimization(edges, graph, pos, times, width, height)
    elif input_string == 'e' or input_string == '4':
        ask_for_random_exchange_optimization(edges, graph, pos, times, width, height)
    elif input_string == 'c' or input_string == '2':
        ask_for_combined_optimization(edges, graph, pos, times, width, height)
    return new_pos


def planarity_check(graph, edges, pos, width, height):
    planarity = nwx.is_planar(graph)
    print(f"The graph is planar? : {planarity}")
    if planarity:
        show = input("Do you want to use nwx planar layout in case the graph is planar?[y/n]")
        if show == 'y':
            pos = nwx.planar_layout(graph)
            # Note that snapped layout might not be necessarily planar if there is an un-snapped layout. Consider
            # the complete graph of k(4,4)/{any single e} with 4 square grid(√) and 6 square grid(X)
            print("The planar layout generated by nwx is :")
            # The nwx pos is such: {node_name: NumPy.array} not python array for better performance
            print(pos)
            # print({0: [1, 2], 1: [3, 4]})
            report_and_draw(graph, edges, pos)
            save_file(graph, pos, width, height)

# {nodes:[{id,x,y},],edges:[{s,t}],width,height}
