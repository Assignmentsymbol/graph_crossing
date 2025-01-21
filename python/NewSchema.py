import copy
import math
import time
from collections import deque
from typing import Dict, Any, Set
import Helpers
import networkx
import matplotlib.pyplot as plt
import numpy as np
import random

import SimulateAnnealingTools
# from Main import graph


def check_degree_reusable(nodes, edges, pos, crossed_edges_dict, last_moved_node):
    """Checking and reporting most of the useful information between moves, also make use of the information it reported
     itself to improve the performance in the next call."""
    edges = set(edges)
    backup = None
    node_on_edge_found = False

    if  crossed_edges_dict is None:
        # crossed_edges_dict: a dictionary of edge:{set of other edges that cross the edge} pairs. It's indeed a weird name.
        crossed_edges_dict: dict[Any, set[Any]] = {edge: set() for edge in edges}
        initial_check(edges,pos, crossed_edges_dict)
    elif last_moved_node is None:
        pass
    else:
        edges_of_the_node = {edge for edge in edges if edge[0] == last_moved_node or edge[1] == last_moved_node}
        diff1 = remove_old_crossings(crossed_edges_dict,last_moved_node,edges,edges_of_the_node)
        diff2,node_on_edge_found = refill_new_crossings(crossed_edges_dict,last_moved_node,edges,edges_of_the_node,pos)
        backup = diff1,diff2

    sorted_edges = sorted(crossed_edges_dict.items(),key=lambda item: len(item[1]),reverse=True)
    # !!!sorted_edges:= a 2-tuple of (edge,{set of other edges that crosses this edge}) sorted by how 'bad' they are such
    # as the size of the set, usage:sorted[0][k] to get the k-th 'bad' edge.
    worst_edge = sorted_edges[0][0]
    worst_edge2 = worst_edge

    if sorted_edges[1].__len__() / sorted_edges[0].__len__() == 1:
        worst_edge2 = sorted_edges[1][0]

    worst_cluster = {node3 for wedge in edges if wedge in crossed_edges_dict[worst_edge] or wedge in crossed_edges_dict[worst_edge2] for node3 in wedge}
    # A stupid implementation.

    max_crossing = crossed_edges_dict[worst_edge].__len__()

    total = sum(len(value) for value in crossed_edges_dict.values())/2
    print('One edge with most crossings is: ' + worst_edge.__str__())
    print('The maximum value of crossings in a single edge is: ' + max_crossing.__str__())
    print('The total number of the crossings is: ' + total.__str__())

    return max_crossing,total,worst_cluster,crossed_edges_dict,backup,node_on_edge_found, sorted_edges



def remove_old_crossings(crossed_edges_dict, node, edges, edges_of_the_node):
    """returning the difference:= the nodes that are affected during the process.
    This allows the program to revert the change later."""
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
    """returning the difference:= the nodes that are affected during the process.
        This allows the program to revert the change later."""
    diff2: dict[Any, set[Any]] = {edge: set() for edge in edges}
    node_on_edge_found = False
    for edge_1 in edges_of_the_node:
        for edge_2 in edges:
            if Helpers.is_intersect_adapted(edge_1, edge_2, pos, True) == -1:
                node_on_edge_found = True
            if Helpers.is_intersect_adapted(edge_1, edge_2, pos, True) != 0:
                # assume the last time has no on-line(on-node is easier to avoid) detect on-line here
                # if intersect type == -1 i.e. crossed on-line, announce for cancel or count the punishment and return
                crossed_edges_dict[edge_1].add(edge_2)
                crossed_edges_dict[edge_2].add(edge_1)
                diff2[edge_1].add(edge_2)
                diff2[edge_2].add(edge_1)
    #             return diff2, announcement(now)/punishment
    return diff2, node_on_edge_found


def initial_check(edges, pos, crossed_edges_dict):
    """In case no information is collected."""
    for edge_1 in edges:
        for edge_2 in [x for x in edges if x != edge_1]:
            if Helpers.is_intersect(edge_1, edge_2, pos, True):
                crossed_edges_dict[edge_1].add(edge_2)
                crossed_edges_dict[edge_2].add(edge_1)
    return


# the forced zone
def compute_target_zone(pos, node, worst_edge_local, width, height):
    """This is some other 'mechanism' as lottery draw"""
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
        diffx = 0.001
    if diffy == 0:
        diffy = 0.001
    breakit = False
    rounded_x = round((x1+x2)/2)
    rounded_y = round((y1+y2)/2)
    possible_slots = [(rounded_x + 1, rounded_y + 1), (x1, y2), (x2, y1),(rounded_x-1,rounded_y-1),(rounded_x+1,rounded_y-1)]
    possible_slots.append((rounded_x-1, rounded_y+1))
    random.shuffle(possible_slots)
    for (x,y) in possible_slots:
        if (y0 - y1) / diffy > (x0 - x1) / diffx:
            if (y - y1) / diffy < (x - x1) / diffx:
                disneyland.append((x, y))
        if (y0 - y1) / diffy < (x0 - x1) / diffx:
            if (y - y1) / diffy > (x - x0) / diffx:
                disneyland.append((x, y))
        if [x for x in disneyland if x not in pos.values()].__len__() > 2:
            print('beep---------')
            return disneyland

    # # 6s
    # for x in range(0,width+1):
    #     if breakit:
    #         break
    #     for y in range(0,height+1):
    #         if (y0 - y1) / diffy > (x0 - x1) / diffx:
    #             if (y - y1) / diffy < (x - x1) / diffx:
    #                 disneyland.append((x,y))
    #         if (y0 - y1) / diffy < (x0 - x1) / diffx:
    #             if (y - y1) / diffy > (x - x0) / diffx:
    #                 disneyland.append((x,y))
    #         if [x for x in disneyland if x not in pos.values()].__len__() > 2:
    #             print('beep---------')
    #             breakit = True
    #             break

    if len(disneyland) == 0:
        disneyland.append((x0,y0))
    return disneyland


def simulate_annealing_exponential(edges, graph, pos:dict, times, width, height,
                                   initial_temperature,crossed_pos_dict,step_size=1,logger=None,cooling_rate=0.95):
    # Remark the name crossed_pos_dict: a dictionary of edges, values are a set of edges that intersect some edge.
    print("Start point of SA cycle------")
    old_pos = pos
    new_count = math.inf
    new_total = math.inf # new
    decreased_temperature = initial_temperature
    gradient_observer = []
    for i in range(times):
        # default settings
        acceptance_probability = None
        backup_stack = deque()
        worst_cluster = None
        total = math.inf
        weight_rdm = 0.5
        weight2_rdwc = 0.9
        weight_release_string = 0.1
        gradient = math.inf
        stuck = False
        new_pos = None
        if i > 0:
            gradient_observer.append(oldest_count)
            if gradient_observer.__len__() == 10:
                gradient = gradient_observer[-1] - gradient_observer[0]
                print(f'gradient: {gradient} = {gradient_observer[-1]} - {gradient_observer[0]} --------------')
                gradient_observer.clear()
            if gradient_observer.__len__() > 200:
                print('no improvement for long...')
                return old_pos, decreased_temperature, None

        if gradient == 0:
            stuck = True

        go_chaotic = False
        if i < times* 0.1 or decreased_temperature < initial_temperature * 0.05:
            step_size = step_size
            go_chaotic = True
            node_on_edge_found = False
        #   Whenever this is True, we always revert the most current change.
        for j in range(step_size):
            move_decider = random.random()
            pick_rd = move_decider < weight_rdm
            pick_rdwc = weight_rdm < move_decider < weight2_rdwc
            pick_release = move_decider > 0.9
            old_count, old_total, worst_cluster, crossed_pos_dict, _,node_on_edge_found ,sorted_edges = check_degree_reusable(graph.nodes, edges, old_pos,
                                                                                             crossed_pos_dict, None)
            # can be refactored
            if j > 0 and oldest_count < 80:
                step_size = 5
            if stuck:
                stuck_level = 1
                if gradient_observer.__len__() > 1:
                    stuck_level = math,round(math.log(gradient_observer.__len__()))
                if stuck_level >= sorted_edges.__len__():
                    stuck_level = sorted_edges.__len__()
                worst_cluster = expand_worst_cluster(sorted_edges,worst_cluster,stuck_level)
            if stuck and move_decider > math.inf:
                if new_pos is not None:
                    old_pos = new_pos
                new_pos, random_node = random_release(old_pos, graph, worst_cluster, width, height, edges, crossed_pos_dict)
                # if step_size < 2:
                #     step_size = 2
                # new_pos, random_node = random_move_on_cluster(old_pos, worst_cluster, width, height)
            else:
                # new_pos, random_node = random_move(old_pos, graph, width, height)
                if new_pos is None:
                    new_pos, random_node = random_move_on_cluster(old_pos, worst_cluster, width, height)
                else:
                    new_pos, random_node = random_move_on_cluster(new_pos, worst_cluster, width, height)
                #     ⬆ Could be written in some more elegant way, but this works.


            new_count, new_total, worst_cluster, crossed_edges_dict_new, backup, node_on_edge_found ,sorted_edges = check_degree_reusable(graph.nodes, edges,
                                                                                                        new_pos,
                                                                                                        crossed_pos_dict,
                                                                                                        random_node)
            if j == 0:
                oldest_count = old_count
                oldest_total = old_total

            acceptance_probability = (SimulateAnnealingTools.
                                      calculate_acceptance_probability_for_crossing(oldest_count,
                                                                                    new_count,decreased_temperature))
            backup_stack.append(backup)
            if (oldest_count > new_count) or node_on_edge_found:
                break


        random_decider = random.random()

        if not node_on_edge_found and (acceptance_probability > random_decider or new_count < oldest_count or (new_count == oldest_count and new_total <= oldest_total)):
            print("Updated--------------------------"+acceptance_probability.__str__()+"   "+random_decider.__str__())
            print(f"new count {new_count} with "
                  f" acc {acceptance_probability}! lucky enough? {acceptance_probability > random_decider}! better "
                  f"than {oldest_count} and total better? {oldest_total>new_total}! -------iteration {i} terminated--------")
            if (not acceptance_probability > random_decider) and new_count == oldest_count and oldest_total < new_total:
                breakpoint()
            old_pos = new_pos
            crossed_pos_dict = crossed_edges_dict_new
        else:
            print(f"old count better-------iteration {i} terminated--------")
            while backup_stack.__len__() > 0:
                backup = backup_stack.pop()
                for key in backup[1].keys():
                    if len(backup[1][key]) != 0:
                        for edge in backup[1][key]:
                            crossed_pos_dict[key].remove(edge)
                for key in backup[0].keys():
                    if len(backup[0][key]) != 0:
                        for edge in backup[0][key]:
                            crossed_pos_dict[key].add(edge)
        decreased_temperature = SimulateAnnealingTools.get_decreased_temperature(decreased_temperature,cooling_rate)
        total = min(old_total, new_total)
    print(f"worst cluster is : {worst_cluster}")
    logger,_,_,_,_,_ ,sorted_edges = check_degree_reusable(graph.nodes, edges, old_pos, crossed_pos_dict, None)
    Helpers.check_identical(pos, old_pos)
    return old_pos, decreased_temperature, logger


def expand_worst_cluster(sorted_edges,worst_cluster,stuck_level):
    for i in range(stuck_level):
        worst_cluster.add(sorted_edges[stuck_level][0])
    return worst_cluster



def random_move(positions: dict, graph, width, height):
    """If used correctly it won't cause overlap"""
    pos_copy = positions.copy()
    new_position = (random.randint(0, width), random.randint(0, height))
    random_node = random.choice(list(graph.nodes))
    if new_position not in positions.values():
        print("position: " + new_position.__str__() + " , " + str(random_node))
        pos_copy[random_node] = new_position
    return pos_copy, random_node


def random_move_on_cluster(positions: dict, worst_cluster, width, height):
    """If used correctly it won't cause overlap"""
    pos_copy = positions.copy()
    new_position = (random.randint(0, width), random.randint(0, height))
    while new_position in positions.values():
        new_position = (random.randint(0, width), random.randint(0, height))

    if worst_cluster is None:
        print('no worst cluster--------------------')
    if new_position in positions.values():
        breakpoint()
    random_node = random.choice(list(worst_cluster))
    print(f'worst cluster 0: {list(worst_cluster)}')
    if new_position not in positions.values():
        print("position: " + new_position.__str__() + " , " + str(random_node))
        pos_copy[random_node] = new_position
    return pos_copy, random_node


def random_switch(positions: dict, graph, width, height, switching_node, slot):
    """Transition API: Shouldn't edit the input pos; returns a tuple of pos, node. Warning: this
    method need some more control variant to avoid trigger the first half of the exchange when loop
    counter = 0 (the following 2nd half thus have no time)."""
    pos_copy = positions.copy()

    if switching_node is None:
        random_node_1 = random.choice(list(graph.nodes))
        random_node_2 = random.choice(list(graph.nodes))
        origin_slot = pos_copy[random_node_1][0], pos_copy[random_node_1][1]
        print(origin_slot is not None)
        return pos_copy, random_node_1, random_node_2, origin_slot
        # has to be always true
    else:
        pos_copy[switching_node] = slot
        return pos_copy, switching_node, None, None


# too far
def random_release(positions: dict, graph, worst_cluster, width, height, edges, crossed_pos_dict):
    """Transition API: Shouldn't edit the input pos; returns a tuple of pos, node (at least)"""
    pos_copy = positions.copy()
    # flat_worst_cluster = {x for edge in worst_cluster for x in edge}
    random_node = random.choice(list(worst_cluster))
    adjacency = [n for n in graph.neighbors(random_node)]
    temp = random.choice(adjacency)
    random_edge = temp,random_node
    if random_edge not in edges:
        random_edge = random_node, temp
    if crossed_pos_dict[random_edge].__len__() == 0:
        return pos_copy, random_node

    edge1 = random.choice(list(crossed_pos_dict[random_edge]))
    edge2 = random.choice(list(crossed_pos_dict[random_edge]))
    # can be improved
    count_e1 = 0
    count_e2 = 0
    # should be neighbors

    for adj_node in adjacency:
        edge = random_node,adj_node
        rever_edge = adj_node,random_node
        # too big
        if Helpers.is_intersect(edge,edge1,pos_copy,True) or Helpers.is_intersect(rever_edge,edge1,pos_copy,True):
            count_e1 += 1
        if Helpers.is_intersect(edge,edge2,pos_copy,True) or Helpers.is_intersect(rever_edge,edge1,pos_copy,True):
            count_e2 += 1

    go_e1 = count_e1 > count_e2
    if go_e1:
        e1_side = compute_target_zone(pos_copy, random_node, edge1, width, height)
        # prioritize here
        slot = e1_side[0]
        if slot not in positions.values():
            pos_copy[random_node] = slot
    else:
        e2_side = compute_target_zone(pos_copy, random_node, edge2, width, height)
        slot = e2_side[0]
        if slot not in positions.values():
            pos_copy[random_node] = slot
    return pos_copy, random_node


def ask_for_new_schema_SA(edges, graph, pos, times, width, height, crossed_dict, param):
    old_copy = pos.copy()
    new_pos = pos
    temperature = param["temp"]
    step_size = param["step size"]
    cooling_rate = param['cooling rate']
    decreased_temperature = temperature
    input_string = input("Do you want to perform simulated annealing?[y/n]")
    if input_string == "n":
        return pos,decreased_temperature
    if crossed_dict is None:
        crossed_dict = initialize_crossed_dict(graph,edges, pos)
    # new_pos = pos
    if input_string == "y":
        pos,decreased_temperature,_ = simulate_annealing_exponential(edges, graph, pos, times,
                                                                   width, height,
                                                                   decreased_temperature,
                                                                   crossed_dict, step_size,None)
        print(".........optimization circle terminated.........")
        draw(graph, edges, pos, width, height)
        Helpers.check_identical(old_copy, pos)
        check_degree_reusable(graph.nodes,edges,pos, crossed_dict,None)
        param['temp'] = decreased_temperature
        pos,decreased_temperature = ask_for_new_schema_SA(edges, graph, pos, times, width, height, crossed_dict, param)
    elif input_string == "rp":
        Helpers.report_and_draw(graph, edges, pos, width, height)
    return pos,param


def initialize_crossed_dict(graph, edges, pos):
    edges = set(edges)
    crossed_edges_dict: dict[Any, set[Any]] = {edge: set() for edge in edges}
    initial_check(edges, pos, crossed_edges_dict)
    return crossed_edges_dict


def draw(graph, edges, new_pos, width, height):
    diameter = (width**2+height**2)**(1/2)
    fig = plt.figure()
    networkx.draw_networkx(graph, pos=new_pos, with_labels=True, node_color="red", node_size=(0/diameter),
                      font_color="blue", font_size=10,
                      font_weight="bold", width=1, edge_color="black")
    plt.margins(0.2)
    plt.show()