import networkx
import networkx as nwx

import AdaptedNXTool
import Helpers
import NewSchema

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
# Helpers.initial_report(edges, pos, graph, width, height)
#graph 11+ are decomposition-able
Helpers.initial_report_smart(edges, pos, graph)
# Helpers.check_total(edges, pos)
# print(pos)
# print(pos.__len__())
#
# # AdaptedNXTool.planar_check(graph, nodes, edges, attributes, pos, width, height,True)
# _, pos = nwx.check_planarity(graph)  # graph: networkx.Graph; pos: dict{node:(x,y)}
# pos = nwx.combinatorial_embedding_to_pos(pos, False)
# print(pos)
# print(pos.__len__())
# pos = AdaptedNXTool.bcc_decomposition(graph,edges,pos,width,height,True)

pos = AdaptedNXTool.fruchterman_reingold(graph, nodes, edges, attributes, pos, width, height, False)
# Helpers.check_total(edges, pos)
# input("press anything to continue")


# temperature = SimulateAnnealingTools.calculate_initial_temperature(width, height, 20, 0.5, 0.2, 0.005, edges, pos, graph)
# print(f"--------Initial temperature is: {temperature}")
Helpers.manual_prompt()
pre_made_input = edges, graph, pos, 50, width, height
default_temperature = 10
parameters = {"temp": default_temperature, "step size": 2, "cooling rate" : None, }
pos, temperature = NewSchema.ask_for_new_schema_SA(edges, graph, pos, 100, width, height, None,parameters)
# pos = AdaptedNXTool.ask_for_operation(graph, nodes, edges, attributes, pos, width, height,False)
pos = NewSchema.ask_for_new_schema(edges, graph, pos, 1000, width, height,None)
Helpers.check_identical(pos_old,pos)
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