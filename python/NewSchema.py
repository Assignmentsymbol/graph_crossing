import copy
import math
from typing import Dict, Any, Set

import Helpers
import RandomizedCrossingMinimization
import networkx
import matplotlib.pyplot as plt
import numpy as np
import random

import SimulateAnnealingTools


def check_degree_reusable(nodes, edges, pos, crossed_edges_dict, last_moved_node):
    # 5t spent
    edges = set(edges)
    backup = None
    # print(edges)
    if  crossed_edges_dict is None:
        crossed_edges_dict: dict[Any, set[Any]] = {edge: set() for edge in edges}
        # edge:{edge,edge,edge}
        initial_check(edges,pos, crossed_edges_dict)
        #backup
    elif last_moved_node is None:
        pass
    else:
        # crossed_edges_dict_copy = copy.deepcopy(crossed_edges_dict)
        # crossed_edges_dict = crossed_edges_dict_copy
        # looking for work around
        edges_of_the_node = {edge for edge in edges if edge[0] == last_moved_node or edge[1] == last_moved_node}
        diff1 = remove_old_crossings(crossed_edges_dict,last_moved_node,edges,edges_of_the_node)
        diff2 = refill_new_crossings(crossed_edges_dict,last_moved_node,edges,edges_of_the_node,pos)
        backup = diff1,diff2
    worst_edge = sorted(crossed_edges_dict.items(),key=lambda item: len(item[1]),reverse=True)[0][0]
    # this line needs doc
    # print(type(crossed_edges_dict[worst_edge]))
    # print(type(edges))
    worst_cluster = {node3 for node3 in edges if node3 in crossed_edges_dict[worst_edge]}
    max_crossing = crossed_edges_dict[worst_edge].__len__()
    print(f'Crossed edges of the worst edge: {crossed_edges_dict[worst_edge]}')
    total = sum(len(value) for value in crossed_edges_dict.values())/2
    print('One edge with most crossings is: ' + worst_edge.__str__())
    print('The maximum value of crossings in a single edge is: ' + max_crossing.__str__())
    print('The total number of the crossings is: ' + total.__str__())

    return max_crossing,total,worst_cluster,crossed_edges_dict,backup



def remove_old_crossings(crossed_edges_dict, node, edges, edges_of_the_node):
    # edges_of_the_node = {edge for edge in edges if edge[0] == node or edge[1] == node}
    #back up here
    diff1: dict[Any, set[Any]] = {edge: set() for edge in edges}
    for edge_1 in edges_of_the_node:
        diff1[edge_1] = {edge for edge in crossed_edges_dict[edge_1]}
        for edge_2 in crossed_edges_dict[edge_1].copy():
            diff1[edge_2].add(edge_1)
            crossed_edges_dict[edge_2].remove(edge_1)
        crossed_edges_dict[edge_1] = set()
    return diff1


def refill_new_crossings(crossed_edges_dict, node, edges, edges_of_the_node, pos):
    diff2: dict[Any, set[Any]] = {edge: set() for edge in edges}
    for edge_1 in edges_of_the_node:
        for edge_2 in edges:
            if Helpers.is_intersect(edge_1, edge_2, pos, True):
                crossed_edges_dict[edge_1].add(edge_2)
                crossed_edges_dict[edge_2].add(edge_1)
                diff2[edge_1].add(edge_2)
                diff2[edge_2].add(edge_1)
    return diff2


def initial_check(edges, pos, crossed_edges_dict):
    for edge_1 in edges:
        for edge_2 in [x for x in edges if x != edge_1]:
            if Helpers.is_intersect(edge_1, edge_2, pos, True):
                crossed_edges_dict[edge_1].add(edge_2)
                crossed_edges_dict[edge_2].add(edge_1)
    return


def quasi_spring_movement():
    return -1


# the forced zone
def compute_target_zone(pos, node, worst_edge_local, width, height):
    disneyland = []
    x1 = pos[worst_edge_local[0]][0]
    y1 = pos[worst_edge_local[0]][1]
    x2 = pos[worst_edge_local[1]][0]
    y2 = pos[worst_edge_local[1]][1]
    x0 = pos[node][0]
    y0 = pos[node][1]
    diffx = x2-x1
    diffy = y2-y1
    if diffx == 0:
        diffx = 0.01
    if diffy == 0:
        diffy = 0.01
    for x in range(0,width+1):
        for y in range(0,height+1):
            if (y0 - y1) / diffy > (x0 - x1) / diffx:
                if (y - y1) / diffy < (x - x1) / diffx:
                    disneyland.append((x,y))
            if (y0 - y1) / diffy < (x0 - x1) / diffx:
                if (y - y1) / diffy > (x - x0) / diffx:
                    disneyland.append((x,y))
    if len(disneyland) == 0:
        disneyland.append((x0,y0))
    return disneyland


def get_trivial_energy():
    pass


def get_non_trivial_energy():
    pass

def get_diameter():
    pass


def new_process_testing(graph, edges, pos, width, height, times, crossed_pos_dict):
    old_pos = pos.copy()
    for i in range(times):
        new_pos,random_node = random_move(old_pos,graph,width,height)
        old_count,old_total,worst_cluster,crossed_pos_dict,_ = check_degree_reusable(graph.nodes,edges,old_pos, crossed_pos_dict ,None)
        new_count,new_total,worst_cluster,crossed_edges_dict_new,backup = check_degree_reusable(graph.nodes, edges, new_pos,crossed_pos_dict,random_node)
        print("------new_count is: " + str(new_count) + "-----------")
        print("------old_count is: " + str(old_count)+ "-----------")
        if  new_count <= old_count:
            print(f"new count better-------iteration {i} terminated--------")
            old_pos = new_pos
            crossed_pos_dict = crossed_edges_dict_new
        else:
            print(f"old count better-------iteration {i} terminated--------")
            for key in backup[1].keys():
                if len(backup[1][key]) != 0:
                    for edge in backup[1][key]:
                        crossed_pos_dict[key].remove(edge)

            for key in backup[0].keys():
                if len(backup[0][key]) != 0:
                    for edge in backup[0][key]:
                        crossed_pos_dict[key].add(edge)

        # if  new_total < old_total:
        #     print(f"------------new count better-------iteration {i} terminated--------")
        #     old_pos = new_pos
        # print(f"------------old count better-------iteration {i} terminated--------")
    return old_pos,random_node


def simulate_annealing_exponential(edges, graph, pos:dict, times, width, height,
                                   initial_temperature,crossed_edges_dict):
    print("Start point of SA cycle------")
    old_pos = pos
    new_pos = pos.copy()
    # old_count = Helpers.check_total(edges, old_pos)
    new_count = math.inf
    decreased_temperature = initial_temperature

    for i in range(times):
        new_pos,random_node = random_move(new_pos, graph, width, height)
        new_count = Helpers.check_total(edges, new_pos)
        # acceptance_probability = SimulateAnnealingTools.calculate_acceptance_probability_for_total(edges, old_pos,
        #                                                                                            new_pos, decreased_temperature)
        acceptance_probability = (SimulateAnnealingTools.
                                  calculate_acceptance_probability_for_crossing(graph.nodes, edges, old_pos,new_pos,
                                                                                crossed_edges_dict, random_node))
        new_count = Helpers.check_total(edges, new_pos)
        random_decider = random.random()
        if acceptance_probability > random_decider:
            print("Updated--------------------------"+acceptance_probability.__str__()+"   "+random_decider.__str__())
            new_count = Helpers.check_total(edges, new_pos)
            old_pos = new_pos
            old_count = new_count
        if Helpers.check_total_silence(edges,new_pos)<Helpers.check_total_silence(edges,old_pos):
            old_pos = new_pos
        decreased_temperature = SimulateAnnealingTools.get_decreased_temperature(decreased_temperature)
    print(".........SA circle terminated.........")
    Helpers.check_identical(pos, old_pos)
    # print("-------the final(SA) crossing number is: " + Helpers.check_total(edges, old_pos).__str__() + "-------")
    return old_pos, decreased_temperature


def random_move(positions: dict, graph, width, height):
    pos_copy = positions.copy()
    new_position = (random.randint(0, width), random.randint(0, height))
    random_node = random.choice(list(graph.nodes))
    # print("positions: " + positions.__str__())
    if new_position not in positions.values():
        print("position: " + new_position.__str__() + " , " + str(random_node))
        pos_copy[random_node] = new_position
    return pos_copy, random_node


def ask_for_new_schema(edges, graph, pos, times, width, height, crossed_dict):
    old_copy = pos.copy()
    new_pos = pos
    input_string = input("Do you want to perform a new schema?[y/n]")
    if input_string == "n":
        return pos
    if crossed_dict is None:
        crossed_dict = initialize_crossed_dict(graph,edges, pos)
    # new_pos = pos
    if input_string == "y":
        pos,random_node = new_process_testing(graph, edges, pos, width, height, times, crossed_dict)
        print(".........optimization circle terminated.........")
        draw(graph, edges, pos, width, height)
        Helpers.check_identical(old_copy, pos)
        check_degree_reusable(graph.nodes,edges,pos, crossed_dict,None)
        pos = ask_for_new_schema(edges, graph, pos, times, width, height,crossed_dict)
    elif input_string == "rp":
        Helpers.report_and_draw(graph, edges, pos, width, height)
    return pos


def ask_for_new_schema_SA(edges, graph, pos, times, width, height, crossed_dict,temperature):
    old_copy = pos.copy()
    new_pos = pos
    decreased_temperature = temperature
    input_string = input("Do you want to perform a new schema of SA?[y/n]")
    if crossed_dict is None:
        crossed_dict = initialize_crossed_dict(graph,edges, pos)
    # new_pos = pos
    if input_string == "y":
        pos,decreased_temperature = simulate_annealing_exponential(edges,graph,pos ,times,
                                                                   width, height, temperature,crossed_dict)
        print(".........optimization circle terminated.........")
        draw(graph, edges, pos, width, height)
        Helpers.check_identical(old_copy, pos)
        check_degree_reusable(graph.nodes,edges,pos, crossed_dict,None)
        pos = ask_for_new_schema_SA(edges, graph, pos, times, width, height,crossed_dict,decreased_temperature)
    elif input_string == "rp":
        Helpers.report_and_draw(graph, edges, pos, width, height)
    return pos,decreased_temperature


def initialize_crossed_dict(graph, edges, pos):
    edges = set(edges)
    crossed_edges_dict: dict[Any, set[Any]] = {edge: set() for edge in edges}
    initial_check(edges, pos, crossed_edges_dict)
    return crossed_edges_dict


def draw(graph, edges, new_pos, width, height):
    diameter = (width**2+height**2)**(1/2)
    fig = plt.figure()
    networkx.draw_networkx(graph, pos=new_pos, with_labels=True, node_color="red", node_size=1,
                      font_color="white", font_size=10, font_family="Times New Roman",
                      font_weight="bold", width=1, edge_color="black")
    plt.margins(0.2)
    plt.show()
    # plt.pause(5)
    # plt.close(fig)
    # plt.draw()
    # plt.show()