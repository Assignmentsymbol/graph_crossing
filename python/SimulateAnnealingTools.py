import math
import random

import HeuristicAlgorithm
import NewSchema
import RandomizedCrossingMinimization
import Helpers


def get_fitness(edges, pos):
    total = Helpers.check_total_silence(edges, pos)
    if total != 0:
        return 1 / (float(total))
    else:
        return 3


def get_energy_as_total(edges, pos):
    return Helpers.check_total_silence(edges, pos)


def get_energy_as_crossing(nodes, edges, pos, crossed_edges_dict, last_moved_node):
    max_crossing,_,_,_ = NewSchema.check_degree_reusable(nodes, edges, pos, crossed_edges_dict, last_moved_node)
    return max_crossing


def calculate_acceptance_probability_fitness(edges, old_pos, new_pos, temperature):
    old_fitness = get_fitness(edges, old_pos)
    new_fitness = get_fitness(edges, new_pos)
    improvement = new_fitness - old_fitness
    if improvement >= 0:
        return 1
    else:
        accp_p = math.e ** (improvement / temperature)
        print(f"acceptance p is: {accp_p}")
        return accp_p


def calculate_acceptance_probability_for_total(edges, old_pos, new_pos, temperature):
    old_energy = get_energy_as_total(edges, old_pos)
    new_energy = get_energy_as_total(edges, new_pos)
    energy_diff = new_energy - old_energy
    if energy_diff <= 0:
        return 1
    else:
        # accp_p = math.e ** ((-1) * energy_diff / temperature)
        accp_p = -1
        # print(f"acceptance p is: {accp_p}")
        return accp_p

def calculate_acceptance_probability_for_crossing(nodes, edges, old_pos,new_pos, crossed_edges_dict, last_moved_node):
    old_energy = get_energy_as_crossing(nodes, edges, old_pos, crossed_edges_dict, last_moved_node)
    new_energy = get_energy_as_crossing(nodes, edges, new_pos, crossed_edges_dict, last_moved_node)
    energy_diff = new_energy - old_energy
    if energy_diff <= 0:
        return 1
    else:
        # accp_p = math.e ** ((-1) * energy_diff / temperature)
        accp_p = -1
        # print(f"acceptance p is: {accp_p}")
        return accp_p


def get_decreased_temperature(temperature):
    print("current temperature is: " + temperature.__str__())
    if temperature < 0.05:
        pass
        # print(f"Degenerated to random mountain climb with p = {temperature}")
        # return 0.01
    return 0.9 * temperature


def wander(edges, graph, pos, width, height):
    return RandomizedCrossingMinimization.random_move(pos, graph, edges, width, height)


def wander_worst_cluster_based(edges, graph, pos, width, height):
    return RandomizedCrossingMinimization.random_move_at_worst_cluster(pos, graph, edges, width, height)


def wander_worst_edge_based(edges, graph, pos, width, height):
    return RandomizedCrossingMinimization.random_move_at_worst_edge(pos, graph, edges, width, height)


def wander_heuristic_diameter(edges, graph, pos, times, height, width):
    return HeuristicAlgorithm.heuristic_with_random(edges, graph, pos, times,
                                                    height, width, HeuristicAlgorithm.diameter_induced_function)


def generate_transitions_energy(width, height, transition_amount, pos, edges, graph):
    transition_energy = []
    fixed_copy = pos.copy()
    for i in range(0, transition_amount*2):
        state_1 = RandomizedCrossingMinimization.random_move(fixed_copy, graph, edges, width, height)
        state_2 = RandomizedCrossingMinimization.random_move(fixed_copy, graph, edges, width, height)
        energy_1 = get_energy_as_total(edges, state_1)
        energy_2 = get_energy_as_total(edges, state_2)
        if energy_1 > energy_2:
            max_state = state_1
            min_state = state_2
            max_energy = energy_1
            min_energy = energy_2
        else:
            max_energy = energy_2
            min_energy = energy_1
            transition_energy.append((max_energy, min_energy))
    # print(transition_energy.__str__())
    return transition_energy


def calculate_initial_temperature(width, height, transition_amount, T_0, X_0, acceptable_diff, edges, pos, graph):
    T = T_0
    print("Calculating temperature, now is: "+T.__str__())
    n = 1
    transition_energy = generate_transitions_energy(width, height, transition_amount, pos, edges, graph)
    current_estimation = compute_estimation_x(T_0, transition_energy)
    current_diff = abs(current_estimation - X_0)
    print(f"estimation is: {current_estimation}")
    if current_diff < acceptable_diff:
        return T
    else:
        T = process_t(T, X_0, current_estimation, 3)
        n += 1
        return calculate_initial_temperature(width, height, transition_amount, T, X_0,
                                             acceptable_diff, edges, pos, graph)


def compute_estimation_x(T, transitions):
    numerator = 0
    denominator = 0
    for s in transitions:
        # print("log compute esti: " + s[0].__str__() +"  " + s[1].__str__())
        # print("log exponent: "+ (-1 * s[0] / T).__str__())
        numerator += math.exp(-1 * s[0] / T)
        denominator += math.exp(-1 * s[1] / T)
    return numerator / denominator


def process_t(Tn, X_0, estimation, p):
    # print(f"estimation is: {estimation}")
    temp = Tn * ((math.log(estimation) / math.log(X_0)) ** (1 / p))
    # print(f"temp is: {temp}")
    return temp
