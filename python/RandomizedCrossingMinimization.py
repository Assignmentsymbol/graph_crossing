import time

import Helpers
import random
import HeuristicAlgorithm


def random_move_at_worst_edge(positions: dict, graph, edges, width, height):
    """returns a copy of pos"""
    pos_copy = positions.copy()
    new_position = (random.randint(0, width), random.randint(0, height))
    random_endpoint = random.choice(Helpers.find_worst(edges, pos_copy))
    # print("positions: " + positions.__str__())
    if new_position not in positions.values():
        print("position: " + new_position.__str__() + " , " + str(random_endpoint))
        pos_copy[random_endpoint] = new_position
    return pos_copy


def random_move_at_worst_cluster(positions: dict, graph, edges, width, height):
    """returns a copy of pos"""
    pos_copy = positions.copy()
    # Store the last worst cluster and get last energy, if energy didn't decent much,
    # use the same cluster without the last moved node
    new_position = (random.randint(0, width), random.randint(0, height))
    worst_cluster = Helpers.find_worst_cluster(edges, pos_copy)
    # worst_cluster = Helpers.find_random_cluster(graph.nodes, pos_copy)
    random_node = random.choice(worst_cluster)
    old_position = pos_copy[random_node]
    # print("positions: " + positions.__str__())
    if new_position not in positions.values():
        print(f"Node {random_node} at old position: {old_position.__str__()} goes to position: {new_position.__str__()} ")
        pos_copy[random_node] = new_position
    return pos_copy


def random_move(positions: dict, graph, edges, width, height):
    """returns a copy of pos
    :param positions:
    :param graph:
    :param height:
    :param width:
    :param edges:
    """
    pos_copy = positions.copy()
    new_position = (random.randint(0, width), random.randint(0, height))
    partition_indexes = get_partition_of_nodes(graph)
    if partition_indexes != -1:
        random_part_choice = random.randint(0, 20)
        random_node = random.choice(
            list(graph.nodes)[partition_indexes[random_part_choice]:partition_indexes[random_part_choice + 1]])
    else:
        random_node = random.choice(list(graph.nodes))
    # print("positions: " + positions.__str__())
    if new_position not in positions.values():
        # print("position: " + new_position.__str__() + " , " + str(random_node))
        pos_copy[random_node] = new_position
    return pos_copy


def get_partition_of_nodes(graph):
    size = graph.number_of_nodes()
    temp = (0,)
    if size <= 30:
        return -1
    for i in range(0, 20):
        temp += (i * round(size / 20),)
    temp += (size,)
    return temp


def random_exchange(positions: dict, graph, width, height):
    pos_copy = positions.copy()
    random_node_1 = random.choice(list(graph.nodes))
    random_node_2 = random.choice(list(graph.nodes))
    temp_coordinate = pos_copy[random_node_1][0], pos_copy[random_node_1][1]
    if random_node_1 == random_node_2:
        print('nodes are the same')
    # print("positions: " + positions.__str__())
    pos_copy[random_node_1] = pos_copy[random_node_2]
    pos_copy[random_node_2] = temp_coordinate
    print("positions (node1, node2) are: " + pos_copy[random_node_1].__str__() + " , " + pos_copy[
        random_node_2].__str__() +
          " and nodes (node1, node2): " + str(random_node_1) + " , " + str(random_node_2))
    # print('pos in random exchange: ' + str(pos_copy))
    return pos_copy


def random_optimization_trivial(edges, graph, pos, times, width, height):
    """returns a position that has the same reference as input(different name)"""
    print("Start point of trivial randomized cycle------")
    old_pos = pos
    for i in range(times):
        old_count = Helpers.check_total(edges, old_pos)
        # new_pos = random_move(old_pos, graph, edges, width, height)
        new_pos = random_move_at_worst_cluster(old_pos, graph, edges, width, height)
        new_count = Helpers.check_total(edges, new_pos)
        if new_count < old_count:
            old_pos = new_pos
    print("-------the final(trivial) crossing number is: " + str(Helpers.check_total_silence(edges, old_pos)) + "-------")

    return old_pos


def random_test(edges, graph, pos, times, width, height):
    """returns a position that has the same reference as input(different name)"""
    print("Start point of trivial randomized cycle------")
    for i in range(times):
        print('leftttttt-----------'+str(i)+'-------rightttttt--------------')
        time_before = time.time()
        print("log111  "+time_before.__str__())
        old_count = Helpers.check_total_quick(edges, pos)
        # old_count = Helpers.check_total(edges, pos)
        time_after = time.time()
        time_diff = time_after - time_before
        print("log222  "+time_after.__str__())
        print("log diff  "+time_diff.__str__())
        # new_pos = random_move_at_worst_cluster(pos, graph, edges, width, height)
        # new_count = Helpers.check_total(edges, new_pos)
    # print("-------the final(trivial) crossing number is: " + str(Helpers.check_total_silence(edges, old_pos)) + "-------")

    return pos


def random_optimization_trivial_fast(edges, graph, pos, times, width, height):
    """returns a position that has the same reference as input(different name)"""
    print("Start point of trivial randomized cycle------")
    old_pos = pos
    for i in range(times):
        old_count = Helpers.check_total_quick(edges, old_pos)
        new_pos = random_move(old_pos, graph, edges, width, height)
        new_count = Helpers.check_total_quick(edges, new_pos)
        if new_count < old_count:
            old_pos = new_pos
    print("-------the final(trivial) crossing number is: " + str(Helpers.check_total_quick(edges, old_pos)) + "-------")

    return old_pos


def random_optimization_trivial_greedy(edges, graph, pos, times, width, height):
    """returns a position that has the same reference as input(different name)"""
    print("Start point of trivial randomized cycle------")
    old_pos = pos
    smallest_crossing = 99999
    smallest_degree_pos = pos
    for i in range(times):
        old_count = Helpers.check_total(edges, old_pos)
        new_pos = random_move(old_pos, graph, edges, width, height)
        if smallest_crossing > Helpers.check_max_degree_silence(edges, new_pos):
            smallest_crossing = Helpers.check_max_degree_silence(edges, new_pos)
            smallest_degree_pos = new_pos.copy()
        new_count = Helpers.check_total(edges, new_pos)
        if new_count < old_count:
            old_pos = new_pos
    if Helpers.check_max_degree_silence(edges, new_pos) > smallest_crossing:
        print("Replacing heuristic result.......")
        old_pos = smallest_degree_pos
    print("-------the final(trivial) crossing number is: "
          + Helpers.check_total(edges, old_pos).__str__() +
          " and the smallest crossing met is " + smallest_crossing.__str__() + "--------")

    return old_pos


def random_with_lucky_jump(edges, graph, pos, times, width, height):
    """returns a position that has the same reference as input(different name)"""
    print("Start point of trivial randomized cycle------")
    old_pos = pos
    p = random.random
    k = 1 / 20
    allow_jump = p * k > 1 / 2
    for i in range(times):
        old_count = Helpers.check_total(edges, old_pos)
        new_pos = random_move(old_pos, graph, edges, width, height)
        new_count = Helpers.check_total(edges, new_pos)
        if new_count < old_count or allow_jump:
            old_pos = new_pos
    print("-------the final(trivial) crossing number is: " + Helpers.check_total(edges, old_pos).__str__() + "-------")

    return old_pos


def random_optimization_at_worst_cluster(edges, graph, pos, times, width, height):
    """returns a position that has the same reference as input(different name)"""
    print("Start point of trivial randomized cycle------")
    old_pos = pos
    for i in range(times):
        old_count = Helpers.check_total(edges, old_pos)
        new_pos = random_move_at_worst_cluster(old_pos, graph, edges, width, height)
        new_count = Helpers.check_total(edges, new_pos)
        if new_count < old_count:
            old_pos = new_pos
    print("-------the final(trivial) crossing number is: " + Helpers.check_total(edges, old_pos).__str__() + "-------")

    return old_pos


def random_optimization_exchange(edges, graph, pos, times, width, height):
    print("Start point of exchange based cycle------")
    old_pos = pos
    for i in range(times):
        old_count = Helpers.check_total(edges, old_pos)
        new_pos = random_exchange(old_pos, graph, width, height)
        # print("log1800----------")
        # print(new_pos)
        new_count = Helpers.check_total(edges, new_pos)
        if new_count < old_count:
            old_pos = new_pos
    print("-------the final(exchange) crossing number is: " + Helpers.check_total(edges, old_pos).__str__() + "-------")

    return old_pos


def combined_randomized_opt(edges, graph, pos, times, width, height):
    print("Start point of combined randomized cycle------")
    old_pos = pos
    new_pos = random_optimization_exchange(edges, graph, old_pos, times, width, height)
    for i in range(1):
        old_count = Helpers.check_total_silence(edges, old_pos)
        break_counter = 0
        while break_counter < 1:
            old_pos_cp = old_pos.copy()
            new_pos = random_optimization_exchange(edges, graph, old_pos, times, width, height)
            if Helpers.check_identical(old_pos_cp, new_pos):
                break_counter += 1
            old_pos = new_pos
        break_counter = 0
        while break_counter < 2:
            old_pos_cp = old_pos.copy()
            new_pos = random_optimization_trivial(edges, graph, old_pos, times, width, height)
            if Helpers.check_identical(old_pos_cp, new_pos):
                break_counter += 1
            old_pos = new_pos
        new_count = Helpers.check_total_silence(edges, new_pos)
        if new_count < old_count:
            old_pos = new_pos
    print("-------the final(combine) crossing number is: " + Helpers.check_total(edges, old_pos).__str__() + "-------")

    return old_pos
