# import networkx as nwx
# import matplotlib.pyplot as plt
# import Helpers
# import KawaiiSpringAlgorithm
#
# # g1: 1
# # g2: 0
# # g3: 1
# # g4: 3
# # g5: 6
# # g6: 7
# # g7: 2
# # g8: 2304 (not good)
# # g9: 1260
# # g10: 1779
#
# graph, nodes, edges, attributes, pos, \
#     width, height = Helpers.data_process(Helpers.load_file())
# nwx.set_edge_attributes(graph, 1, 'weight')
# Helpers.initial_report(edges, pos, graph)
# print(pos)
#
# # Helpers.initial_report(edges, pos, graph)
# Helpers.planarity_check(graph, edges, pos, width, height)  # not yet snapped
#
# # Helpers.ask_for_Kawaii_movement(graph, pos, 3, 1, 0.05,edges,(width,height))
# pre_made_input = edges, graph, pos, 50, width, height
# pos = Helpers.ask_for_heuristic_with_given_function(edges, graph, pos, 50, width, height)
# pos = Helpers.ask_for_simulate_annealing(edges, graph, pos, 50, width, height)
# pos = Helpers.ask_for_heuristic_with_given_function(edges, graph, pos, 50, width, height)
# pos = Helpers.ask_for_combined_optimization(edges, graph, pos, 50, width, height)
# pos = Helpers.ask_for_random_exchange_optimization(edges, graph, pos, 50, width, height)
# pos = Helpers.ask_for_trivial_random_optimization(edges, graph, pos, 50, width, height)
# # Helpers.ask_for_random_movement(graph, pos, edges)
# Helpers.save_file(graph, pos, width, height)
#

import GraphProcessor

json_file_path = input("Enter the file path of the json file: ")
gp = GraphProcessor(json_file_path)
gp.calculate_crossings()
preprocessed_positions = gp.preprocess_nodes()
crossings_table = gp.generate_crossings_table()

gp.plot_graph()

gp.interactive_iteration()


