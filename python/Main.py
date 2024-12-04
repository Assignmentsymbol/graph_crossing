import networkx as nwx
import matplotlib.pyplot as plt
from networkx.drawing import draw_networkx

import Helpers
import HeuristicAlgorithm
import KawaiiSpringAlgorithm

# g1: 1
# g2: 0
# g3: 1
# g4: 3
# g5: 6
# g6: 7
# g7: 2
# g8: 2304 (not good)
# g9: 1260
# g10: 1779

graph, nodes, edges, attributes, pos, \
    width, height = Helpers.data_process(Helpers.load_file())
nwx.set_edge_attributes(graph, 1, 'weight')
#graph 11+ are decomposition-able
Helpers.initial_report_smart(edges, pos, graph)
print(pos)
bcc = list(nwx.biconnected_components(graph))
print(bcc.__len__())
print('index: '+ bcc.index(max(bcc,key=len)).__str__())
print(max(bcc,key=len).__len__())# bad matching
# sub_graph = nwx.complete_graph(bcc[bcc.index(max(bcc,key=len))])
# sub_edges = sub_graph.edges()
sub_graph = nwx.Graph()
bcc.sort(key=len, reverse = True)
sub_graph_nodes = bcc[0]
sub_graph.add_nodes_from(sub_graph_nodes)
sub_graph_edges = [(x,y) for (x,y) in edges if x in sub_graph_nodes and y in sub_graph_nodes]
sub_pos = {node:(x,y) for node,(x,y) in pos.items() if node in sub_graph_nodes}
print(f'nodes size: {len(sub_graph_nodes)} and edges size: {len(sub_graph_edges)} and pos size: {len(sub_pos)}')
print(sub_graph_nodes)
print(sub_graph_edges)
sub_graph.add_edges_from(sub_graph_edges)
Helpers.report_and_draw(sub_graph,sub_graph_edges,sub_pos)
print()
input()

Helpers.report_and_draw()
# Helpers.initial_report(edges, pos, graph)
Helpers.planarity_check(graph, edges, pos, width, height)  # not yet snapped

# Helpers.ask_for_Kawaii_movement(graph, pos, 3, 1, 0.05,edges,(width,height))
pre_made_input = edges, graph, pos, 50, width, height
pos = Helpers.ask_for_heuristic_with_given_function(edges, graph, pos, 50, width, height, HeuristicAlgorithm.heuristic_jeff_surrounding)
pos = Helpers.ask_for_simulate_annealing(edges, graph, pos, 50, width, height)
pos = Helpers.ask_for_combined_optimization(edges, graph, pos, 50, width, height)
pos = Helpers.ask_for_random_exchange_optimization(edges, graph, pos, 50, width, height)
pos = Helpers.ask_for_trivial_random_optimization(edges, graph, pos, 50, width, height)
# Helpers.ask_for_random_movement(graph, pos, edges)
Helpers.save_file(graph, pos, width, height)


# import GraphProcessor
#
# json_file_path = input("Enter the file path of the json file: ")
# gp = GraphProcessor(json_file_path)
# gp.calculate_crossings()
# preprocessed_positions = gp.preprocess_nodes()
# crossings_table = gp.generate_crossings_table()
#
# gp.plot_graph()
#
# gp.interactive_iteration()


