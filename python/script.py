import json
import math
import os
import time

import networkx
import networkx as nwx
import scipy
import AdaptedNXTool
import Helpers
import NewSchema

def save_file_direct(graph: networkx.Graph, pos, width, height, filename, config):
    # current_directory = os.getcwd()
    # data_testing = {"node": {"id": 1, "di": 2}}
    storage_directory = config['output']
    data_out = {}
    nodes = []
    edges = []
    for node in graph.nodes:
        nodes.append({"id": node, "x": pos[node][0], "y": pos[node][1]})
    for edge in graph.edges:
        edges.append({"source": edge[0], "target": edge[1]})
    data_out["nodes"] = nodes
    data_out["edges"] = edges
    data_out["width"] = 0
    data_out["height"] = 0
    data_out["width"] = width
    data_out["height"] = height

    with open(os.path.join(storage_directory, f"{filename}.json"), 'w', encoding='utf-8') as file:
        json.dump(data_out, file, indent=4, ensure_ascii=False)
        # print("total: " + check_total(graph.edges, pos).__str__())
        print("File saved")


def load_directory(config):
    input_directory = config['input']
    data_set = []
    # current_directory = os.getcwd()
    target_directory = input_directory


    for filename in os.listdir(target_directory):
        if filename.endswith('.json'):
            file_path = os.path.join(target_directory, filename)
            data_set.append(load_file(file_path))
    print(data_set)
    return data_set


def load_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def ask_for_new_schema_SA2(edges, graph, pos, times, width, height, crossed_dict, param):
    old_copy = pos.copy()
    new_pos = pos
    temperature = param["temp"]
    step_size = param["step size"]
    cooling_rate = param['cooling rate']
    decreased_temperature = temperature
    if crossed_dict is None:
        crossed_dict = NewSchema.initialize_crossed_dict(graph, edges, pos)
    # new_pos = pos

    pos, decreased_temperature, _ = NewSchema.simulate_annealing_exponential(edges, graph, pos, times,
                                                                             width, height,
                                                                             decreased_temperature,
                                                                             crossed_dict, step_size, None)
    print(".........optimization circle terminated.........")
    Helpers.check_identical(old_copy, pos)
    NewSchema.check_degree_reusable(graph.nodes, edges, pos, crossed_dict, None)
    param['temp'] = decreased_temperature

    return pos,param

def execute_process(data,counter,config):
    # F:\graphdrawingSW\Graph_Intersaction\python\examples\graph15.json
    # https://jacoblmiller.github.io/tum-gd-contest/tool.html

    start_time = time.time()

    graph, nodes, edges, attributes, pos, \
        width, height = Helpers.data_process(data)
    pos_old = pos.copy()
    initial_crossing_count = Helpers.check_total_silence(edges, pos)

    nwx.set_edge_attributes(graph, 1, 'weight')
    print(edges.__len__())

    pos = AdaptedNXTool.fruchterman_reingold(graph, nodes, edges, attributes, pos, width, height, False)
    pre_made_input = edges, graph, pos, 50, width, height
    default_temperature = 10
    temp = int(config['iteration'])
    parameters = {"temp": 1, "step size": 2, "cooling rate" : 0.9,"iteration times":temp,"transition weight": None, }
    iteration_times = parameters["iteration times"]
    pos, temperature = ask_for_new_schema_SA2(edges, graph, pos, iteration_times, width, height, None,parameters)

    processed_count = Helpers.check_total_silence(edges, pos)

    file_name = f'output{counter}'
    save_file_direct(graph, pos, width, height,file_name,config)


    end_time = time.time()
    delta = end_time - start_time
    delta_trunc= float('{:.4f}'.format(delta))
    print(f"runtime for the graph: {delta_trunc} s")
    return delta_trunc,initial_crossing_count,processed_count



config = {}
with open("config.txt", "r", encoding="utf-8") as file:
    for line in file:
        line = line.strip()
        if line and "=" in line:
            key, value = line.split("=", 1)
            config[key.strip()] = value.strip()
print(config)
print(config['input'])
print(config['iteration'])
iteration = int(config['iteration'])
print(type(iteration))

data_set = load_directory(config)
counter = 0

report = {}
for data in data_set:
    counter += 1
    time_used,initial_count,after_process_count = execute_process(data,counter,config)
    graph_name = "Output_" + str(counter)
    report[graph_name] = {}
    report[graph_name]['initial crossing count'] = initial_count
    report[graph_name]['after process crossing count'] = after_process_count
    report[graph_name]['improvement'] = initial_count-after_process_count
    report[graph_name]['time used'] = time_used


with open(os.path.join(config['output'], "report.json"), 'w', encoding='utf-8') as file:
    json.dump(report, file, indent=4, ensure_ascii=False)
    print("Report saved")


