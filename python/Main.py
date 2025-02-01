import math

import networkx
import networkx as nwx
import numpy as np
import scipy
from networkx.classes import Graph

import AdaptedNXTool
import Helpers
import NewSchema
from Helpers import report_and_draw

# F:\graphdrawingSW\Graph_Intersaction\python\examples\graph15.json
# https://jacoblmiller.github.io/tum-gd-contest/tool.html
graph, nodes, edges, attributes, pos, \
    width, height = Helpers.data_process(Helpers.load_file())
pos_old = pos.copy()
# print(nodes)
# print(edges)
# print(pos)
nwx.set_edge_attributes(graph, 1, 'weight')
print(edges.__len__())
#graph 11+ are decomposition-worth
Helpers.initial_report_smart(edges, pos, graph)
# Helpers.check_total(edges, pos)
# print(pos)
# print(pos.__len__())
#
# # AdaptedNXTool.planar_check(graph, nodes, edges, attributes, pos, width, height,True)
# _, pos1 = nwx.check_planarity(graph)  # graph: networkx.Graph; pos: dict{node:(x,y)}
# pos = nwx.combinatorial_embedding_to_pos(pos, False)
# print(pos)
# print(pos.__len__())
# pos = AdaptedNXTool.bcc_decomposition(graph,edges,pos,width,height,True)

# pos = AdaptedNXTool.fruchterman_reingold(graph, nodes, edges, attributes, pos, width, height, False)

# Helpers.report_and_draw(graph, edges,pos, width, height)
# Helpers.check_total(edges, pos)

# print('beeep------------')
# is_planar, embedding = nwx.check_planarity(graph)
# print(is_planar)
# if is_planar:
#     pos = nwx.combinatorial_embedding_to_pos(embedding, False)
# print(pos)
# input('++')


# pos[1] = (9999,9999)
# Helpers.fast_matching_snap(nodes,pos,width,height,None,None)
# input('cut')
# Helpers.save_file(graph, pos, width, height)
# input('saved')


# temperature = SimulateAnnealingTools.calculate_initial_temperature(width, height, 20, 0.5, 0.2, 0.005, edges, pos, graph)
# print(f"--------Initial temperature is: {temperature}")
Helpers.manual_prompt()
pre_made_input = edges, graph, pos, 50, width, height
default_temperature = 10
# 0.6 or 1.8, on g6
parameters = {"temp": 2, "step size": 3, "cooling rate" : 0.9,"transition weight": None, }
pos, temperature = NewSchema.ask_for_new_schema_SA(edges, graph, pos, 500, width, height, None,parameters)
# pos = AdaptedNXTool.ask_for_operation(graph, nodes, edges, attributes, pos, width, height,False)
# pos = NewSchema.ask_for_new_schema(edges, graph, pos, 1000, width, height,None)
Helpers.check_identical(pos_old,pos)
count = 0

for node1 in nodes:
    for node2 in nodes:
        if node2 != node1:
            if pos[node1] == pos[node2]:
                print('overlapped')
                print(f"{node1}, {node2}:{pos[node1]}=={pos[node2]}")
                count += 1
print(count)

# Helpers.check_total(edges,pos)


Helpers.save_file(graph, pos, width, height)












# Helpers.ask_for_testing_method(edges, graph, pos, 50, width, height)
# pos = Helpers.ask_for_trivial_random_optimization(edges, graph, pos, 50, width, height)
# pos, initial_temperature = Helpers.ask_for_trivial_simulate_annealing(edges, graph, pos, width,
#                                                                       height, 50, default_temperature)
# # pos = Helpers.ask_for_trivial_random_optimization(edges, graph, pos, 50, width, height)
# pos = Helpers.ask_for_diameter_based_heuristic(edges, graph, pos, 50, width, height)
# pos = Helpers.ask_for_heuristic_with_func1(edges, graph, pos, 50, width, height)
# pos = Helpers.ask_for_combined_optimization(edges, graph, pos, 50, width, height)
# pos = Helpers.ask_for_random_exchange_optimization(edges, graph, pos, 50, width, height)
# Helpers.ask_for_random_movement(graph, pos, edges)