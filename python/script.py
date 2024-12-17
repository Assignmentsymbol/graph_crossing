import json
import os

import networkx
import networkx as nwx
import scipy
import AdaptedNXTool
import Helpers
import NewSchema

def save_file_direct(graph: networkx.Graph, pos, width, height, filename):
    current_directory = os.getcwd()
    # data_testing = {"node": {"id": 1, "di": 2}}
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

    with open(os.path.join(current_directory, f"{filename}.json"), 'w', encoding='utf-8') as file:
        json.dump(data_out, file, indent=4, ensure_ascii=False)
        # print("total: " + check_total(graph.edges, pos).__str__())
        print("File saved")


def pass_config():
    current_directory = os.getcwd()
    return


def load_directory():
    data_set = []
    current_directory = os.getcwd()
    target_directory = os.path.join(current_directory, 'benchmarks')

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
    NewSchema.draw(graph, edges, pos, width, height)
    Helpers.check_identical(old_copy, pos)
    NewSchema.check_degree_reusable(graph.nodes, edges, pos, crossed_dict, None)
    param['temp'] = decreased_temperature

    return pos,param

def execute_process(data,counter):
    # F:\graphdrawingSW\Graph_Intersaction\python\examples\graph15.json
    # https://jacoblmiller.github.io/tum-gd-contest/tool.html

    graph, nodes, edges, attributes, pos, \
        width, height = Helpers.data_process(data)
    pos_old = pos.copy()

    nwx.set_edge_attributes(graph, 1, 'weight')
    print(edges.__len__())

    Helpers.initial_report_smart(edges, pos, graph)
    pos = AdaptedNXTool.fruchterman_reingold(graph, nodes, edges, attributes, pos, width, height, False)
    Helpers.manual_prompt()
    pre_made_input = edges, graph, pos, 50, width, height
    default_temperature = 10
    parameters = {"temp": 1, "step size": 2, "cooling rate" : 0.9,"transition weight": None, }
    pos, temperature = ask_for_new_schema_SA2(edges, graph, pos, 100, width, height, None,parameters)
    Helpers.check_identical(pos_old,pos)

    file_name = f'output{counter}'
    save_file_direct(graph, pos, width, height,file_name)


data_set = load_directory()
counter = 0
for data in data_set:
    counter += 1
    execute_process(data,counter)


