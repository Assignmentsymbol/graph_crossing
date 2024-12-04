import networkx as nwx
import matplotlib.pyplot as plt
import numpy as np
import random
import Helpers
import os
import json

current_directory = os.getcwd()
print("Current Directory:", current_directory)

with open(current_directory + r"\examples\ex1_k6_xr32.json", 'r') as file:
    data = json.load(file)

# print(data)
nodes_data = data["nodes"]
nodes = []
attributes = []
edges = []
pos = {}
for dct in nodes_data:
    nodes.append(dct["id"])
    coordinate = dct['x'], dct['y']
    attributes.append(coordinate)
    pos[dct["id"]] = dct['x'], dct['y']
for dct in data['edges']:
    temp = (dct["source"]), (dct["target"])
    edges.append(temp)
print(nodes)
print(attributes)
print(edges)
print(nodes_data)
G = nwx.Graph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)
print("hey this is the nodes: " + G.nodes.__str__())
graph = nwx.Graph()
graph.add_node("A")
graph.nodes["A"]["x"] = 3
graph.nodes["A"]["y"] = 5
graph.add_node("B")
graph.nodes["B"]["x"] = 3
graph.nodes["B"]["y"] = 4
edge1 = ("A", "B")
graph.add_edge(edge1[0], edge1[1])

print(graph.nodes["A"]["x"] - graph.nodes["B"]["x"])
print(graph.edges)
print(edge1)
print(graph.edges(data=True))
edges_with_data = list(graph.edges(data=True))
print(edges_with_data)
e1, *rest = edges_with_data
print(e1[1])
print(graph.nodes[e1[0]]["x"])

