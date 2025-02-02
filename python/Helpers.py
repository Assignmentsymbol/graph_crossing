import math
from itertools import combinations

import networkx
import networkx as nwx
import matplotlib.pyplot as plt
import random

import numpy as np

import NewSchema
from playgrounds import KawaiiSpringAlgorithm
import RandomizedCrossingMinimization
from IntersectAlgorithm import Point, doIntersect_adapted
from IntersectAlgorithm import doIntersect
import RandomizedCrossingMinimization as rcm
import os
import json
import HeuristicAlgorithm as hrt


def manual_prompt():
    print("-----------------------------------------------------------------------------------------------------")
    print("The following shortcut can be used to switch to another operation whenever the prompt [y/n] is shown")
    print("[t] stands for trivial random operation")
    print("[c] stands for combined operation")
    print("[h] stands for diameter based heuristic operation")
    print("[e] stands for exchange/swap based random operation")
    print("[s] stands for simulated annealing")
    print("-----------------------------------------------------------------------------------------------------")


# def show_grid(width,height):
#     plt.grid('on')
#     plt.axhline(0, color='black', linewidth=1)  # x axe
#     plt.axvline(0, color='black', linewidth=1)
#     # adding integer dots
#     fig, ax = plt.subplots()
#     display_width = ax.transData.transform([width, 0])[0]
#     display_height = ax.transData.transform([height, 0])[0]
#     for i in range(int(display_width)):
#         inverted_i = ax.transData.inverted().transform([(i, -0.1)])[0]
#         plt.text(inverted_i, -0.1, str(inverted_i), ha='center', va='center', color="blue")
#     for j in range(int(display_height)):
#         inverted_j = ax.transData.inverted().transform([(-0.1,j)])[0]
#         plt.text(-0.1, inverted_j, str(inverted_j), ha='center', va='center', color="blue")
#     plt.xlabel("X")
#     plt.ylabel("Y")
#     plt.title("Some drawing(coordinates are snapped to the grid)")


def show_grid(width,height):
    plt.grid('on')
    plt.axhline(0, color='black', linewidth=1)  # x axe
    plt.axvline(0, color='black', linewidth=1)
    # for i in range(-1, 20):
    #     # adding integer dots
    #     plt.text(i, -0.1, str(i), ha='center', va='center', color="blue")
    #     plt.text(-0.3, i, str(i), ha='center', va='center', color="blue")
    # trivial stuff
    # plt.xlabel("X")
    # plt.ylabel("Y")
    # plt.title("Some drawing")


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


def is_intersect_adapted(edge1: tuple[str], edge2: tuple[str], pos: dict, silent: bool):
    e1p1 = Point(pos[edge1[0]][0], pos[edge1[0]][1])
    e1p2 = Point(pos[edge1[1]][0], pos[edge1[1]][1])
    e2p1 = Point(pos[edge2[0]][0], pos[edge2[0]][1])
    e2p2 = Point(pos[edge2[1]][0], pos[edge2[1]][1])

    if not silent:
        if doIntersect_adapted(e1p1, e1p2, e2p1, e2p2) == 1:
            print("Intersected")
        else:
            print("Not intersected")

    return doIntersect_adapted(e1p1, e1p2, e2p1, e2p2)




def load_file_hard():
    current_directory = os.getcwd()
    # print("Current Directory:", current_directory)
    with open(current_directory + r"/benchmarks/ex1_k6_xr32.json", 'r') as file:
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
    print("Input size is: " + len(data["nodes"]).__str__() + " nodes.")
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
    print("Data loaded...")
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
            # print("total: " + check_total(graph.edges, pos).__str__())
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


def check_total_quick(edges, pos):
    maxc,_ = NewSchema.check_degree_reusable(None,edges,pos,None,None)
    print('The max number of the crossings is: ' + maxc.__str__())
    return maxc


def check_max_degree(edges, pos):
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
    return max_Value


def check_max_degree_silence(edges, pos):
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
    return max_Value


def check_total_silence(edges, pos):
    # 5t spent
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


def check_total(edges, pos):
    # 5t spent
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


def find_worst(edges, pos):
    max_Value = 0
    local_max = 0
    worst_edge = ()
    for edge_1 in edges:
        max_Value = max(max_Value, local_max)
        local_max = 0
        for edge_2 in [x for x in edges if x != edge_1]:
            if is_intersect(edge_1, edge_2, pos, True):
                local_max += 1
                if local_max > max_Value:
                    worst_edge = edge_1
    print("worst edge is : "+worst_edge.__str__())
    return worst_edge


def find_worst_cluster(edges, pos):
    # 2t spent
    max_Value = 0
    local_max = 0
    worst_edge = ()
    worst_cluster = []
    j = 0
    for edge_1 in edges:
        if j > 20:
            break
        j += 1
        max_Value = max(max_Value, local_max)
        local_max = 0
        cluster = []
        i = 0
        for edge_2 in [x for x in edges if x != edge_1]:
            if i > 20:
                break
            i += 1
            if is_intersect(edge_1, edge_2, pos, True):
                local_max += 1
                cluster.append(edge_2[0])
                cluster.append(edge_2[1])
                if local_max > max_Value:
                    worst_edge = edge_1
                    worst_cluster = cluster
    worst_cluster.append(worst_edge[0])
    worst_cluster.append(worst_edge[1])
    print("worst edge is : "+worst_edge.__str__())
    # print("log3400 :  "+worst_cluster.__str__())
    return worst_cluster


def find_random_cluster(nodes, pos):
    # 2t spent
    cluster = random.sample(nodes, min((len(nodes) - 1),20))

    # print("worst edge is : "+worst_edge.__str__())
    return cluster


def report_and_draw(graph, edges, new_pos, width, height):
    diameter = (width**2+height**2)**(1/2)
    check_total(edges, new_pos)
    fig = plt.figure()
    nwx.draw_networkx(graph, pos=new_pos, with_labels=True, node_color="red", node_size=1,
                      font_color="white", font_size=10, font_family="Times New Roman",
                      font_weight="bold", width=1, edge_color="black")
    plt.margins(0.2)
    show_grid(width, height)
    plt.show()
    # plt.pause(5)
    plt.close(fig)
    # plt.draw()
    # plt.show()


def initial_report(edges, pos, graph,width, height):
    # check_total(edges, pos)
    plt.figure()
    diameter = (width**2+height**2)**(1/2)
    nwx.draw_networkx(graph, pos=pos, with_labels=True, node_color="red", node_size=1,
                      font_color="white", font_size=10, font_family="Times New Roman",
                      font_weight="bold", width=1, edge_color="black")
    plt.margins(0.2)
    show_grid(width, height)
    plt.show()


def initial_report_smart(edges, pos, graph):
    """

    :rtype: object
    """
    if len(graph.nodes()) < 400 and len(edges) < 500:
        print(f'nodes size: {len(graph.nodes())}, edges size: {len(graph.edges())}')
        print("checking total and degree........")
        check_total(edges, pos)
    plt.figure()
    nwx.draw_networkx(graph, pos=pos, with_labels=True, node_color="red", node_size=100,
                      font_color="white", font_size=10, font_family="Times New Roman",
                      font_weight="bold", width=1, edge_color="black")
    plt.margins(0.2)
    # show_grid(width= 10, height=10)
    plt.show()


def check_identical(pos_old, pos_new):
    if pos_old == pos_new:
        print("This optimization cycle results the identical position...")
        return False
    for entry in pos_new:
        if pos_old[entry] != pos_new[entry]:
            print("Position changed...")
            print(f'Moved {entry} to {pos_new[entry]} from old{pos_old[entry]}')
            return True
    print("This optimization cycle results a identical position from the previous one...")
    return False
    # if pos_old == pos_new:
    #     print("This optimization cycle results the identical position...")
    #     return True
    # else:
    #     print("Position changed...")
    #     return False


def ask_for_random_movement(graph, pos, edges, width, height):
    inputString = input("Do you want to perform a random change?[y/n]")
    if inputString == "y":
        perform_operation_for_single_change(pos, graph)
        report_and_draw(graph, edges, pos, width, height)
        ask_for_random_movement(graph, pos, edges, width, height)


def ask_for_kawaii_movement(graph, pos, L, K, satisfied_diff, edges, d_range, width, height):
    input_string = input("Do you want to perform spring balance?[y/n]")
    if input_string == "y":
        new_pos = KawaiiSpringAlgorithm.iterate(
            *KawaiiSpringAlgorithm.data_convertor(graph, pos, L, K, satisfied_diff, d_range))
        print(".........optimization circle terminated.........")
        report_and_draw(graph, edges, new_pos, width, height)
        ask_for_kawaii_movement(graph, pos, L, K, satisfied_diff, edges, d_range, width, height)
    elif input_string == '2':
        pass


def ask_for_trivial_random_optimization(edges, graph, pos, times, width, height):
    old_copy = pos.copy()
    input_string = input("Do you want to perform a trivial random optimization?[y/n]")
    new_pos = pos
    if input_string == "y":
        new_pos = rcm.random_optimization_trivial(edges, graph, pos, times, width, height) #newpos?
        # new_pos = rcm.random_optimization_trivial_fast(edges, graph, pos, times, width, height) #newpos?
        print(".........optimization circle terminated.........")
        # report_and_draw(graph, edges, new_pos, width, height)
        check_identical(old_copy, new_pos)
        new_pos = ask_for_trivial_random_optimization(edges, graph, new_pos, times, width, height)
    elif input_string == "rp":
        report_and_draw(graph, edges, new_pos, width, height)
    elif input_string == 'e' or input_string == '4':
        new_pos = ask_for_random_exchange_optimization(edges, graph, pos, times, width, height)
    elif input_string == 'c' or input_string == '2':
        new_pos = ask_for_combined_optimization(edges, graph, pos, times, width, height)
    elif input_string == 'h' or input_string == '3':
        new_pos = ask_for_heuristic_with_func1(edges, graph, pos, times, width, height)
    return new_pos

def ask_for_testing_method(edges, graph, pos, times, width, height):
    old_copy = pos.copy()
    input_string = input("Do you want to perform a test?[y/n]")
    new_pos = pos
    if input_string == "y":
        print('------------------log1---------------------')
        RandomizedCrossingMinimization.random_test(edges, graph, pos, times, width, height)
        # new_pos = rcm.random_optimization_trivial_fast(edges, graph, pos, times, width, height) #newpos?
        print(".........optimization circle terminated.........")

        new_pos = ask_for_testing_method(edges, graph, new_pos, times, width, height)
    elif input_string == "rp":
        report_and_draw(graph, edges, new_pos, width, height)
    elif input_string == 'e' or input_string == '4':
        new_pos = ask_for_random_exchange_optimization(edges, graph, pos, times, width, height)
    elif input_string == 'c' or input_string == '2':
        new_pos = ask_for_combined_optimization(edges, graph, pos, times, width, height)
    elif input_string == 'h' or input_string == '3':
        new_pos = ask_for_heuristic_with_func1(edges, graph, pos, times, width, height)
    return new_pos



def ask_for_random_exchange_optimization(edges, graph, pos, times, width, height):
    old_copy = pos.copy()
    input_string = input("Do you want to perform a random exchange optimization?[y/n]")
    new_pos = pos
    if input_string == "y":
        new_pos = rcm.random_optimization_exchange(edges, graph, pos, times, width, height)
        print(".........optimization circle terminated.........")
        report_and_draw(graph, edges, new_pos, width, height)
        check_identical(old_copy, new_pos)
        new_pos = ask_for_random_exchange_optimization(edges, graph, new_pos, times, width, height)
    elif input_string == 't' or input_string == '1':
        new_pos = ask_for_trivial_random_optimization(edges, graph, pos, times, width, height)
    elif input_string == 'c' or input_string == '2':
        new_pos = ask_for_combined_optimization(edges, graph, pos, times, width, height)
    elif input_string == 'h' or input_string == '3':
        new_pos = ask_for_heuristic_with_func1(edges, graph, pos, times, width, height)
    return new_pos


def ask_for_combined_optimization(edges, graph, pos, times, width, height):
    old_copy = pos.copy()
    input_string = input("Do you want to perform a combined random optimization?[y/n]")
    new_pos = pos
    if input_string == "y":
        new_pos = rcm.combined_randomized_opt(edges, graph, pos, times, width, height)
        print(".........(combined)optimization circle terminated.........")
        report_and_draw(graph, edges, new_pos, width, height)
        check_identical(old_copy, new_pos)
        new_pos = ask_for_combined_optimization(edges, graph, new_pos, times, width, height)
    elif input_string == 't' or input_string == '1':
        new_pos = ask_for_trivial_random_optimization(edges, graph, pos, times, width, height)
    elif input_string == 'e' or input_string == '4':
        new_pos = ask_for_random_exchange_optimization(edges, graph, pos, times, width, height)
    elif input_string == 'h' or input_string == '3':
        new_pos = ask_for_heuristic_with_func1(edges, graph, pos, times, width, height)
    return new_pos


def ask_for_heuristic_with_func1(edges, graph, pos, times, width, height):
    """not in use"""
    old_copy = pos.copy()
    input_string = input("Do you want to perform a heuristic optimization?[y/n]")
    new_pos = pos
    if input_string == "y":
        new_pos = hrt.heuristic_with_random(edges, graph, pos, times, width, height, hrt.diameter_induced_function)
        print(".........heuristic optimization circle terminated.........")
        report_and_draw(graph, edges, new_pos, width, height)
        check_identical(old_copy, new_pos)
        new_pos = ask_for_heuristic_with_func1(edges, graph, new_pos, times, width, height)
    elif input_string == 't' or input_string == '1':
        new_pos = ask_for_trivial_random_optimization(edges, graph, pos, times, width, height)
    elif input_string == 'e' or input_string == '4':
        new_pos = ask_for_random_exchange_optimization(edges, graph, pos, times, width, height)
    elif input_string == 'c' or input_string == '2':
        new_pos = ask_for_combined_optimization(edges, graph, pos, times, width, height)
    return new_pos


def ask_for_diameter_based_heuristic(edges, graph, pos, times, width, height):
    old_copy = pos.copy()
    input_string = input("Do you want to perform a diameter based heuristic optimization?[y/n]")
    new_pos = pos
    if input_string == "y":
        new_pos = hrt.heuristic_with_random(edges, graph, pos, times, width, height, hrt.diameter_induced_function)
        print(".........SA circle terminated.........")
        report_and_draw(graph, edges, new_pos, width, height)
        check_identical(old_copy, new_pos)
        new_pos = ask_for_diameter_based_heuristic(edges, graph, new_pos, times, width, height)
    elif input_string == 't' or input_string == '1':
        new_pos = ask_for_trivial_random_optimization(edges, graph, pos, times, width, height)
    elif input_string == 'e' or input_string == '4':
        new_pos = ask_for_random_exchange_optimization(edges, graph, pos, times, width, height)
    elif input_string == 'c' or input_string == '2':
        new_pos = ask_for_combined_optimization(edges, graph, pos, times, width, height)
    return new_pos


def ask_for_trivial_simulate_annealing(edges, graph, pos:dict, width, height, times, initial_temp):
    old_copy = pos.copy()
    # print("log2000")
    # check_total(edges,pos)
    new_pos = pos
    temperature = initial_temp
    # while True:
    #     input_string = input("Do you want to perform a SA optimization?[y/n]")
    #     if input_string == 'n':
    #         break
    #     if input_string == 'rp':
    #         report_and_draw(graph, edges, new_pos, width, height)
    #     while input_string == "y":
    #         new_pos, temperature = hrt.simulate_annealing_exponent(edges, graph, new_pos, times,
    #                                                                width, height, temperature)
    #         report_and_draw(graph, edges, new_pos, width, height)
    #         break
    input_string = input("Do you want to perform a SA optimization?[y/n]")
    if input_string == "y":
        # new_pos,temperature = hrt.simulate_annealing_exponent(edges, graph, new_pos, times,
        #                                                        width, height, temperature)
        new_pos = rcm.random_optimization_trivial(edges, graph, pos, times, width, height)
        new_pos, temperature = ask_for_trivial_simulate_annealing(edges, graph, new_pos, width, height,times, temperature)
    elif input_string == "rp":
        report_and_draw(graph, edges, new_pos, width, height)
    elif input_string == 't' or input_string == '1':
        new_pos = ask_for_trivial_random_optimization(edges, graph, pos, times, width, height)
    elif input_string == 'e' or input_string == '4':
        new_pos = ask_for_random_exchange_optimization(edges, graph, pos, times, width, height)
    elif input_string == 'c' or input_string == '2':
        new_pos = ask_for_combined_optimization(edges, graph, pos, times, width, height)

    return new_pos, temperature

# {nodes:[{id,x,y},],edges:[{s,t}],width,height}

def trivial_snap(nodes,pos,width,height):
    pos_int = {node: (round(x), round(y)) for node, (x, y) in pos.items()}
    # min_x = min([x for x,y in pos_int.values()])
    # min_y = min([y for x,y in pos_int.values()])
    # pos_int = {node: (x+abs(min_x) ,y+abs(min_y)) for node,(x,y) in pos_int.values()}
    clean = True
    for node in nodes:
        if has_overlap(nodes,pos):
            clean = False
    if clean:
        return pos_int
    for n1,n2 in combinations(nodes,2):
        if pos_int[n1] == pos_int[n2]:
            goto_closest_spot(n2,pos,width,height)
    return pos_int



def is_out_of_scope(node,pos,width_interval,height_interval):
    if (pos[node][0] > width_interval[1] or pos[node][1] > height_interval[1] or pos[node][0] < width_interval[0]
            or pos[node][1] < height_interval[0]):
        return True
    return False


def matching_snap(nodes,pos,width_interval,height_interval):
    out_of_scope = [x for x in nodes if is_out_of_scope(x,pos,width_interval,height_interval)]
    print(width_interval, height_interval)
    if out_of_scope.__len__()==0:
        print('nothing out of scope in this area')
        return -1
    print(f"one out of scopes is with {pos[out_of_scope[0]][0]} , {pos[out_of_scope[0]][1]}")
    available_grid = []
    g2 = nwx.Graph()
    for x in range(width_interval[0],width_interval[1]+1):
        for y in range(height_interval[0],height_interval[1]+1):
            if (x, y) not in pos.values():
                available_grid.append((x, y))
    if out_of_scope.__len__() * available_grid.__len__()>1000000:
        print('matching too big')
        return -1
    for node in out_of_scope:
        for (x, y) in available_grid:
            distance = math.dist(pos[node], (x, y))
            g2.add_edge(node, (x, y), weight=distance)

    nwx.max_weight_matching(g2)
    for node in out_of_scope:
        for ed in g2.edges:
            if node == ed[0]:
                pos[node] = ed[1]
    return 1


def partition(nodes, pos, width, height):
    scope = ([],[])
    for node in nodes:
        if pos[node][0] > width:
            scope[0].append(pos[node][0])
        if pos[node][1] > height:
            scope[1].append(pos[node][1])
    # print(scope[0])
    # breakpoint()
    scope = max(scope[0]),max(scope[1])
    diff = scope[0]-width,scope[1] - height
    right_partition_point_1 = height+(1/3)*diff[0]
    right_partition_point_2 = height+(2/3)*diff[0]
    upper_partition_point_1 = height+(1/3)*diff[1]
    upper_partition_point_2 = height + (2 / 3) * diff[1]
    print()

    out_of_scope_right_1 = [x for x in nodes if right_partition_point_1 > pos[x][0] > height]
    out_of_scope_right_2 = [x for x in nodes if upper_partition_point_2 > pos[x][0] > right_partition_point_1]
    out_of_scope_right_3 = [x for x in nodes if pos[x][0] > right_partition_point_2]
    print(out_of_scope_right_1,out_of_scope_right_2,out_of_scope_right_3)

    out_of_scope_upper_1 = [x for x in nodes if upper_partition_point_1 > pos[x][1] > height]
    out_of_scope_upper_2 = [x for x in nodes if upper_partition_point_2 > pos[x][1] > upper_partition_point_1]
    out_of_scope_upper_3 = [x for x in nodes if pos[x][1] > upper_partition_point_2]
    print(scope[1],upper_partition_point_2)
    return (out_of_scope_right_1, out_of_scope_right_2, out_of_scope_right_3, out_of_scope_upper_1, out_of_scope_upper_2,
            out_of_scope_upper_3)


def partition_interval(interval):
    partition_point = round((interval[0]+interval[1])/2)+1
    return (interval[0],partition_point),(partition_point,interval[1])


def get_grids(pos,width,interval):
    available_grids = []
    for x in range(interval[0],interval[1]+1):
        for y in range(width + 1):
            if (x, y) not in pos.values():
                available_grids.append((x, y))
    return available_grids


def compute_scope(nodes,pos,height):
    scope = []
    for node in nodes:
        if pos[node][1] > height:
            scope.append(pos[node][1])

    return 0,max(scope)


def fast_matching_snap(nodes,pos,width,height,domain,codomain):
    if domain is None:
        domain = compute_scope(nodes,pos,height)
    if codomain is None:
        codomain = 0,height

    out_of_scope_upper_interval,out_of_scope_lower_interval = partition_interval(domain)
    available_grids_upper_interval, available_grids_lower_interval = partition_interval(codomain)

    free_spots_count1 = width*(available_grids_upper_interval[1] - available_grids_upper_interval[0])
    free_spots_count2 = width*(available_grids_lower_interval[1] - available_grids_lower_interval[0])
    for n in nodes:
        if available_grids_upper_interval[1] > pos[n][1] > available_grids_upper_interval[0]:
            free_spots_count1 -= 1
        if available_grids_lower_interval[1] > pos[n][1] > available_grids_lower_interval[0]:
            free_spots_count2 -= 1
    branch1 = [x for x in nodes if out_of_scope_upper_interval[1] > pos[x][1] >= out_of_scope_upper_interval[0]]
    domain_order1 = branch1.__len__()
    branch2 = [x for x in nodes if out_of_scope_lower_interval[1] > pos[x][1] >= out_of_scope_lower_interval[0]]
    domain_order2 = branch2.__len__()
    terminate = free_spots_count1 < domain_order1 or free_spots_count2 < domain_order2

    if codomain[1]-codomain[0] <=4 or terminate:
        available_grids = get_grids(pos,width,codomain)
        out_of_scope = [x for x in nodes if domain[1]>= pos[x][1] > domain[0] and not (width >= pos[x][0] >= 0
                                                                                       and height >= pos[x][1] >= 0)]
        if out_of_scope.__len__() == 0:
            return -1

        g2 = nwx.Graph()
        for x in range(width+1):
            for y in range(codomain[0], codomain[1] + 1):
                if (x, y) not in pos.values():
                    available_grids.append((x, y))
        if out_of_scope.__len__() * available_grids.__len__() > 1000000:
            print('matching too big')
            return -1
        for node in out_of_scope:
            for (x, y) in available_grids:
                distance = math.dist(pos[node], (x, y))
                g2.add_edge(node, (x, y), weight=distance)

        nwx.max_weight_matching(g2)
        for node in out_of_scope:
            for ed in g2.edges:
                if node == ed[0]:
                    pos[node] = ed[1]
        print(out_of_scope)
        print(terminate)

        return 1
    fast_matching_snap(nodes,pos,width,height,out_of_scope_upper_interval,available_grids_upper_interval)
    fast_matching_snap(nodes,pos,width,height,out_of_scope_lower_interval,available_grids_lower_interval)





def d3_matching_snap(nodes,pos,width,height):
    (out_of_scope_right_1, out_of_scope_right_2, out_of_scope_right_3,
     out_of_scope_upper_1, out_of_scope_upper_2, out_of_scope_upper_3) = partition(nodes, pos, width, height)
    width_interval_1 = 0,round((1/3)*width)
    width_interval_2 = round((1/3)*width),round((2/3)*width)
    width_interval_3 = round((2/3)*width),width
    height_interval_1 = 0,round((1/3)*height)
    height_interval_2 = round((1/3)*height),round((2/3)*height)
    height_interval_3 = round((2/3)*height),height
    matching_snap(out_of_scope_right_1,pos,width_interval_1,(0,height))
    matching_snap(out_of_scope_right_2,pos,width_interval_2,(0,height))
    matching_snap(out_of_scope_right_3,pos,width_interval_3,(0,height))
    matching_snap(out_of_scope_upper_1,pos,(0,width),height_interval_1)
    matching_snap(out_of_scope_upper_2,pos,(0,width),height_interval_2)
    matching_snap(out_of_scope_upper_3,pos,(0,width),height_interval_3)


def has_overlap(nodes,pos):
    if len(pos) == len(set(tuple(val) for val in pos.values())):
        print("no duplicates-------")
        return False
    else:
        print("have duplicates-------")
        return True


def goto_closest_spot(node,pos,width,height):
    is_valid = lambda a, b, x: x > a and x > b
    for i in range(width*height):
        if pos[node] + (i,0) not in pos.values() and is_valid(width,height,i):
            pos[node] = pos[node] + (i,0)
            return
        if pos[node] + (-i,0) not in pos.values() and is_valid(width,height,i):
            pos[node] = pos[node] + (-i,0)
            return
        if pos[node] + (0,i) not in pos.values() and is_valid(width,height,i):
            pos[node] = pos[node] + (0,i)
            return
        if pos[node] + (0,-i) not in pos.values() and is_valid(width,height,i):
            pos[node] = pos[node] + (0,-i)
            return
        if pos[node] + (i,i) not in pos.values() and is_valid(width,height,i):
            pos[node] = pos[node] + (i,i)
            return
        if pos[node] + (i,-i) not in pos.values() and is_valid(width,height,i):
            pos[node] = pos[node] + (i,-i)
            return
        if pos[node] + (-i,-i) not in pos.values() and is_valid(width,height,i):
            pos[node] = pos[node] + (-i,-i)
            return
        if pos[node] + (-i,i) not in pos.values() and is_valid(width,height,i):
            pos[node] = pos[node] + (-i,i)
            return




