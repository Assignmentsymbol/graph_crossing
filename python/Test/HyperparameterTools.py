import heapq
import json
import math
import os
import statistics

import AdaptedNXTool
import NewSchema
import networkx as nwx
import Helpers


def unpack_parameters(params):
    pass


def load_filee():
    current_directory = os.getcwd()
    # print("Current Directory:", current_directory)
    with open(current_directory + r"/graph6.json", 'r') as file:
        data = json.load(file)
        return data


def grid_search(edges, graph, pos, times, width, height, crossed_pos_dict):
    crossed_pos_dict = None
    score_record = {}
    best_params_candidates = []
    global_best = math.inf
    # pos = AdaptedNXTool.fruchterman_reingold(graph, nodes, edges, attributes, pos, width, height, False)
    for i in range (10):
        for iniTemp in range(1,10):
            for step_size in range(1, 4):
                _,_,logger = NewSchema.simulate_annealing_exponential(edges, graph, pos, times, width, height,
                                       iniTemp/5,crossed_pos_dict,step_size,None)
                if (iniTemp/5,step_size) not in score_record.keys():
                    score_record[(iniTemp /5, step_size)] = []
                score_record[(iniTemp/5,step_size)].append(logger)

    for key in score_record.keys():
        average = statistics.mean(score_record[key])
        heapq.heappush(best_params_candidates, (round(average,5), key))


    best_count,best_params = heapq.heappop(best_params_candidates)
    print(best_params_candidates)
    print(f'best count: {best_count} ----')
    # fishy+need to be averaged.
    print(f'best_params: {best_params} ----')
    if best_params[0] is None:
        print('Nothing returned...')
    return best_params



graph, nodes, edges, attributes, pos, \
    width, height = Helpers.data_process(load_filee())
pos_old = pos.copy()
# print(nodes)
# print(edges)
# print(pos)
print(edges.__len__())

Helpers.initial_report_smart(edges, pos, graph)


best_params = grid_search(edges, graph, pos, 300, width, height,None)
parameters = {"temp": 20, "step size": 2, "cooling rate": None, }