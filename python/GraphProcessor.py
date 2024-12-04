import json
import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Tuple, Union


class GraphProcessor:
    def __init__(self, json_file: str):

        self.graph = nx.Graph()
        self.node_crossings = {}
        self.read_json(json_file)

    def read_json(self, json_file: str):

        with open(json_file, 'r') as f:
            data = json.load(f)

        # Adding nodes with positions
        for node in data["nodes"]:
            self.graph.add_node(node["id"], pos=(node["x"], node["y"]))

        # Adding edges
        for edge in data["edges"]:
            self.graph.add_edge(edge["source"], edge["target"])

        # Initialize the crossings table for each node
        self.node_crossings = {node: [] for node in self.graph.nodes()}

    def calculate_crossings(self):

        edges = list(self.graph.edges())

        # Compare each pair of edges to check for crossings
        for i, edge1 in enumerate(edges):
            for j, edge2 in enumerate(edges):
                if i < j:  # Avoid duplicate comparisons and self-comparisons
                    if self.edges_cross(edge1, edge2):
                        # Update crossings table
                        self.node_crossings[edge1[0]].append(edge2)
                        self.node_crossings[edge1[1]].append(edge2)
                        self.node_crossings[edge2[0]].append(edge1)
                        self.node_crossings[edge2[1]].append(edge1)

    def edges_cross(self, edge1: Tuple[int, int], edge2: Tuple[int, int]) -> bool:

        def ccw(A, B, C):
            return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

        pos = nx.get_node_attributes(self.graph, 'pos')
        A, B = pos[edge1[0]], pos[edge1[1]]
        C, D = pos[edge2[0]], pos[edge2[1]]

        return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)

    def generate_crossings_table(self, max_columns: int = 5) -> List[List[Union[Tuple[int, int], None]]]:

        table = []
        for node, crossings in self.node_crossings.items():
            row = crossings[:max_columns] + [None] * (max_columns - len(crossings))
            table.append(row)
        return table

    def plot_graph(self):

        pos = nx.get_node_attributes(self.graph, 'pos')  # Use node positions from the JSON file
        nx.draw(self.graph, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10)
        nx.draw_networkx_edge_labels(
            self.graph,
            pos,
            edge_labels={(u, v): f"{u}-{v}" for u, v in self.graph.edges()},
            font_color='red'
        )
        plt.show()

    def preprocess_nodes(self):
        node_degrees = {}
        for node in self.graph.nodes():
            connections = len(list(self.graph.neighbors(node)))
            crossings = len(self.node_crossings[node])
            node_degrees[node] = connections + crossings

        sorted_nodes = sorted(node_degrees.keys(), key=lambda x: node_degrees[x], reverse=True)

        node_positions = {}
        center = (0, 0)
        offsets = [
            (-1, -1), (0, -1), (1, -1),  # Top row
            (-1, 0),  (0, 0),  (1, 0),   # Middle row
            (-1, 1),  (0, 1),  (1, 1),   # Bottom row
        ]

        for i, node in enumerate(sorted_nodes):
            if i < len(offsets):
                node_positions[node] = (center[0] + offsets[i][0], center[1] + offsets[i][1])
            else:
                layer = (i - len(offsets)) // 8 + 1
                direction = (i - len(offsets)) % 8
                directions = [
                    (layer, -layer),  # Top-right
                    (-layer, layer),  # Bottom-left
                    (-layer, -layer),  # Top-left
                    (layer, layer),   # Bottom-right
                    (layer, layer + 1),   # Top-right further out
                    (layer + 1, layer),   # Bottom-right further out
                    (-layer - 1, -layer), # Top-left further out
                    (-layer, -layer - 1), # Bottom-left further out
                ]
                node_positions[node] = directions[direction]

        nx.set_node_attributes(self.graph, node_positions, 'pos')
        return node_positions

    def move_node(self, node: int, edge: Tuple[int, int]):
        pos = nx.get_node_attributes(self.graph, 'pos')
        source, target = edge
        source_pos = pos[source]
        target_pos = pos[target]

        midpoint = (int((source_pos[0] + target_pos[0]) / 2), int((source_pos[1] + target_pos[1]) / 2))

        node_pos = pos[node]
        direction = (midpoint[0] - node_pos[0], midpoint[1] - node_pos[1])

        magnitude = (direction[0] ** 2 + direction[1] ** 2) ** 0.5
        if magnitude == 0:
            return

        unit_vector = (direction[0] / magnitude, direction[1] / magnitude)
        new_position = (
            round(midpoint[0] + unit_vector[0]),
            round(midpoint[1] + unit_vector[1])
        )

        self.graph.nodes[node]['pos'] = new_position

    def iterate(self):
        for node, crossings in self.node_crossings.items():
            if crossings:
                crossing_counts = {}
                for edge in crossings:
                    crossing_counts[edge] = crossing_counts.get(edge, 0) + 1

                max_crossing_edge = max(crossing_counts, key=crossing_counts.get)
                self.move_node(node, max_crossing_edge)

    def interactive_iteration(self):
        while True:
            self.iterate()
            self.plot_graph()  # Show the updated graph
            proceed = input("Do you want to iterate again? (n to stop): ").strip().lower()
            if proceed == 'n':
                break

