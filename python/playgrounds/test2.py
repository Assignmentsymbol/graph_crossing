# import networkx as nwx
# import matplotlib.pyplot as plt
# import numpy as np
# from Helpers import show_grid as sg
#
#
#
# p1 = 5
# p2 = 6
# p3 = 5
# p4 = 5
#
# if len((p1, p3, p2, p4)) != len(set((p1, p3, p2, p4))):
#     print("false")
# else:
#     print("true")

import json
import random
import os
import networkx as nx
import matplotlib.pyplot as plt

# Assume Point and doIntersect are provided from the IntersectAlgorithm
from IntersectAlgorithm import Point, doIntersect


class GraphHeuristicOptimizer:
    def __init__(self, file_path=None):
        self.graph = nx.Graph()
        self.positions = {}
        self.edges = []
        self.width = 0
        self.height = 0
        if file_path:
            self.load_file(file_path)

    def load_file(self, file_path):
        """Loads graph data from a JSON file and initializes graph attributes."""
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
            self._process_data(data)
        except Exception as e:
            print("Error loading file:", e)
            self.load_default_file()

    def load_default_file(self):
        """Loads a default file if the specified file path fails."""
        current_directory = os.getcwd()
        default_path = os.path.join(current_directory, "examples/ex1_k6_xr32.json")
        self.load_file(default_path)

    def _process_data(self, data):
        """Processes loaded data into graph structure, positions, and edges."""
        self.width = data["width"]
        self.height = data["height"]

        # Parse nodes
        for node_data in data["nodes"]:
            node_id = node_data["id"]
            self.graph.add_node(node_id)
            self.positions[node_id] = (node_data["x"], node_data["y"])

        # Parse edges
        for edge_data in data["edges"]:
            source = edge_data["source"]
            target = edge_data["target"]
            self.edges.append((source, target))
            self.graph.add_edge(source, target)

    def perform_heuristic(self, iterations=10):
        """Applies a heuristic to reduce edge crossings by adjusting node positions."""
        for _ in range(iterations):
            self._perform_single_adjustment()
            crossings = self._check_total_crossings()
            print(f"Iteration complete. Total crossings: {crossings}")

    def _perform_single_adjustment(self):
        """Performs a single heuristic adjustment by moving a random node."""
        node = random.choice(list(self.graph.nodes))
        new_position = (random.randint(0, self.width), random.randint(0, self.height))
        self.positions[node] = new_position

    def _is_intersect(self, edge1, edge2):
        """Checks if two edges intersect using their position coordinates."""
        p1, p2 = Point(*self.positions[edge1[0]]), Point(*self.positions[edge1[1]])
        p3, p4 = Point(*self.positions[edge2[0]]), Point(*self.positions[edge2[1]])
        return doIntersect(p1, p2, p3, p4)

    def _check_total_crossings(self):
        """Calculates the total number of edge crossings in the graph."""
        total_crossings = 0
        for i, edge1 in enumerate(self.edges):
            for edge2 in self.edges[i + 1:]:  # Avoid double counting
                if self._is_intersect(edge1, edge2):
                    total_crossings += 1
        return total_crossings

    def draw_graph(self):
        """Displays the graph with the current positions."""
        nx.draw_networkx(self.graph, pos=self.positions, with_labels=True, node_color="red",
                         node_size=100, font_color="white", font_size=10,
                         edge_color="black", width=1)
        plt.grid(True)
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.show()
