import networkx
import networkx as nwx
import numpy as np
import scipy

import AdaptedNXTool
import Helpers
import NewSchema

graph, nodes, edges, attributes, pos, \
    width, height = Helpers.data_process(Helpers.load_file())
pos_old = pos.copy()

nwx.set_edge_attributes(graph, 1, 'weight')
print(edges.__len__())

Helpers.initial_report_smart(edges, pos, graph)


pos = AdaptedNXTool.fruchterman_reingold(graph, nodes, edges, attributes, pos, width, height, False,False)

Helpers.manual_prompt()
pre_made_input = edges, graph, pos, 50, width, height
default_temperature = 10
parameters = {"temp": 2, "step size": 3, "cooling rate" : 0.9,"transition weight": None, }
pos, temperature = NewSchema.ask_for_new_schema_SA(edges, graph, pos, 100, width, height, None,parameters)

Helpers.check_identical(pos_old,pos)
count = 0

# node on node test
for node1 in nodes:
    for node2 in nodes:
        if node2 != node1:
            if pos[node1] == pos[node2]:
                print('overlapped')
                print(f"{node1}, {node2}:{pos[node1]}=={pos[node2]}")
                count += 1
print(count/2)



Helpers.save_file(graph, pos, width, height)
