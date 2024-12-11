import time
import networkx as nx

import AdaptedNXTool
import Helpers
import NewSchema

# F:\graphdrawingSW\Graph_Intersaction\python\examples\graph15.json
graph, nodes, edges, attributes, pos, \
    width, height = Helpers.data_process(Helpers.load_file())
pos_old = pos.copy()
# print(nodes)
# print(edges)
# print(pos)
print(edges.__len__())
# Helpers.initial_report_smart(edges, pos, graph)#graph 11+ are decomposition-able

# F:\graphdrawingSW\Graph_Intersaction\python\examples\graph7.json

start_time = time.time()
# pos = nx.kamada_kawai_layout(graph)
# pos = nx.fruchterman_reingold_layout(graph)
pos = nx.spring_layout(graph)
print('-----')
print(nx.average_node_connectivity(graph))
print('-----')
# length = kcp.__len__()
# print(f"length: {length}")
print(nx.make_max_clique_graph(graph))
print(f"ramsey: {nx.ramsey_R2(graph)}")
end_time = time.time()

execution_time = end_time - start_time
print("\n")
print(f"execution time: {execution_time:.5f} s\n\n")

pre_made_input = graph, edges, pos, width, height
Helpers.report_and_draw(*pre_made_input)