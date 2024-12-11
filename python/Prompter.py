import Helpers
import RandomizedCrossingMinimization


def ask_for_choosing_algorithm_type():
    input_string = input("Type 1 perform trivial randomized optimization;"
                         "Type 2 perform exchange based optimization;"
                         "Type 3 perform spring optimization;"
                         "Type 4 perform a single randomized move.")
    pass


def ask_for_wcluster_based_random_optimization(edges, graph, pos, times, width, height):
    old_copy = pos.copy()
    input_string = input("Do you want to perform a worst cluster based random optimization?[y/n]")
    new_pos = pos
    if input_string == "y":
        new_pos = RandomizedCrossingMinimization.random_optimization_at_worst_cluster(edges, graph, pos, times, width,
                                                                                      height)
        print(".........optimization circle terminated.........")
        Helpers.report_and_draw(graph, edges, new_pos, width, height)
        Helpers.check_identical(old_copy, new_pos)
        new_pos = ask_for_wcluster_based_random_optimization(edges, graph, new_pos, times, width, height)
    elif input_string == 'e' or input_string == '4':
        new_pos = Helpers.ask_for_random_exchange_optimization(edges, graph, pos, times, width, height)
    elif input_string == 'c' or input_string == '2':
        new_pos = Helpers.ask_for_combined_optimization(edges, graph, pos, times, width, height)
    elif input_string == 'h' or input_string == '3':
        new_pos = Helpers.ask_for_heuristic_with_func1(edges, graph, pos, times, width, height)
    return new_pos
