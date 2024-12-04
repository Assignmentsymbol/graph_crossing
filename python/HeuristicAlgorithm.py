import math
import time

import Helpers
import random
import RandomizedCrossingMinimization
import SimulateAnnealingTools


def diameter_induced_function(edges, graph, pos, times, width, height):
    coordinate_xs = []
    coordinate_ys = []
    for coordinate_x, coordinate_y in pos.values():
        coordinate_xs.append(coordinate_x)
        coordinate_ys.append(coordinate_y)
    delta_x = max(coordinate_xs) - min(coordinate_xs)
    delta_y = max(coordinate_ys) - min(coordinate_ys)
    diameter = (delta_x ** 2 + delta_y ** 2) ** (1 / 2)
    max_diameter = (width ** 2 + height ** 2) ** (1 / 2)
    return diameter / max_diameter


def diameter_based_heuristic(edges, graph, pos, times, width, height):
    print("Start point of layout diameter induced heuristic cycle------")
    counter = 0
    new_pos = pos
    origin_crossing_count = Helpers.check_total_silence(edges, pos)
    for i in range(5):
        new_pos = RandomizedCrossingMinimization.combined_randomized_opt(edges, graph, pos, round(times / 3), width,
                                                                         height)
        if Helpers.check_identical(pos, new_pos):
            counter += 1
        if counter > 2:
            if Helpers.check_total_silence(edges, new_pos) < (round(origin_crossing_count + 666)):
                print("here goes heuristic-------------")
                heuristic_with_random(edges, graph, pos, round(1), width, height, diameter_induced_function)
            else:
                print("here goes heuristic-------------")
                heuristic_with_random(edges, graph, pos, round(2), width, height, diameter_induced_function)
            counter = 0
    print("-------the final(diameter) crossing number is: " + Helpers.check_total(edges, new_pos).__str__() + "-------")
    return new_pos


def heuristic_with_random(edges, graph, pos, times, width, height, heuristic):
    old_pos = pos
    for i in range(times):
        old_count = Helpers.check_total(edges, old_pos)
        new_pos = RandomizedCrossingMinimization.random_move(old_pos, graph, edges, width, height)
        new_count = Helpers.check_total(edges, new_pos)
        if new_count < old_count + 2 * heuristic(edges, graph, pos, times, width, height):
            old_pos = new_pos
    print("-------the final crossing number is: " + Helpers.check_total(edges, old_pos).__str__() + "-------")

    return old_pos


def simulate_annealing_exponential(edges, graph, pos:dict, times, width, height, initial_temperature):
    print("Start point of SA cycle------")
    old_pos = pos
    new_pos = pos.copy()
    # old_count = Helpers.check_total(edges, old_pos)
    new_count = math.inf
    decreased_temperature = initial_temperature

    for i in range(times):
        # print(f'log 1 {time.time()}')
        new_pos = RandomizedCrossingMinimization.random_move(new_pos, graph, edges, width, height)
        # new_count = Helpers.check_total(edges, new_pos)
        # print(f'log 2 {time.time()}')
        acceptance_probability = SimulateAnnealingTools.calculate_acceptance_probability_for_total(edges, old_pos,
                                                                                                   new_pos, decreased_temperature)
        # print(f'log 3 {time.time()}')
        # new_count = Helpers.check_total(edges, new_pos)
        random_decider = random.random()
        # if acceptance_probability > random_decider:
        #     print("Updated--------------------------"+acceptance_probability.__str__()+"   "+random_decider.__str__())
        #     new_count = Helpers.check_total(edges, new_pos)
        #     old_pos = new_pos
        #     old_count = new_count
        if Helpers.check_total_silence(edges,new_pos)<Helpers.check_total_silence(edges,old_pos):
            old_pos = new_pos
        # print(f'log 4 {time.time()}')
        # decreased_temperature = SimulateAnnealingTools.get_decreased_temperature(decreased_temperature)
        # print(f'log 5 {time.time()}')
    print(".........SA circle terminated.........")
    Helpers.check_identical(pos, old_pos)
    # print("-------the final(SA) crossing number is: " + Helpers.check_total(edges, old_pos).__str__() + "-------")

    return old_pos, decreased_temperature
