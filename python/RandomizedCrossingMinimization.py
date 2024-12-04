import Helpers
import random
import HeuristicAlgorithm


def random_move(positions: dict, graph, width, height):
    pos_copy = positions.copy()
    new_position = (random.randint(0, width), random.randint(0, height))
    random_node = random.choice(list(graph.nodes))
    # print("positions: " + positions.__str__())
    if new_position not in positions.values():
        print("position: " + new_position.__str__() + " , " + str(random_node))
        pos_copy[random_node] = new_position
    return pos_copy


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
    print("Start point of trivial randomized cycle------")
    old_pos = pos
    for i in range(times):
        old_count = Helpers.check_total(edges, old_pos)
        new_pos = random_move(old_pos, graph, width, height)
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


def simulate_annealing(edges, graph, pos, times, width, height):
    print("Start point of simulate annealing cycle------")
    counter = 0
    new_pos = pos
    origin_crossing_count = Helpers.check_total_silence(edges, pos)
    for i in range(5):
        new_pos = combined_randomized_opt(edges, graph, pos, round(times/3), width, height)
        if Helpers.check_identical(pos, new_pos):
            counter += 1
        if counter > 2:
            if Helpers.check_total_silence(edges, new_pos) < (round(origin_crossing_count+666)):
                HeuristicAlgorithm.heuristic_with_random(edges, graph, pos, round(1), width, height)
            else:
                HeuristicAlgorithm.heuristic_with_random(edges, graph, pos, round(2), width, height)
            counter = 0
    print("-------the final(SA) crossing number is: " + Helpers.check_total(edges, new_pos).__str__() + "-------")
    return new_pos
