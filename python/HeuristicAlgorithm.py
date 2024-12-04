import Helpers
import random
import RandomizedCrossingMinimization


def diameter_induced_function(edges, graph, pos, times, width, height):
    coordinate_xs = []
    coordinate_ys = []
    for coordinate_x, coordinate_y in pos.values():
        coordinate_xs.append(coordinate_x)
        coordinate_ys.append(coordinate_y)
    delta_x = max(coordinate_xs)-min(coordinate_xs)
    delta_y = max(coordinate_ys)-min(coordinate_ys)
    diameter = (delta_x**2+delta_y**2)**(1/2)
    max_diameter = (width**2+height**2)**(1/2)
    return diameter/max_diameter


def heuristic_with_random(edges, graph, pos, times, width, height, heuristic):
    old_pos = pos
    for i in range(times):
        old_count = Helpers.check_total(edges, old_pos)
        new_pos = RandomizedCrossingMinimization.random_move(old_pos, graph, width, height)
        new_count = Helpers.check_total(edges, new_pos)
        if new_count < old_count + 2 * heuristic(edges, graph, pos, times, width, height):
            old_pos = new_pos
    print("-------the final crossing number is: " + Helpers.check_total(edges, old_pos).__str__() + "-------")

    return old_pos


def heuristic_jeff_surrounding(edges, graph, pos, times, width, height):
    degrees = {node: len(list(graph.neighbors(node))) for node in graph.nodes}
    sorted_nodes = sorted(degrees, key=degrees.get, reverse=True)

    center = (int(width // 2), int(height // 2))  # Place the highest degree node in the middle of the plot
    pos[sorted_nodes[0]] = center


    directions = [
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0),
        (-1, 1),
    ]

    # Place the first 8 nodes in a surrounding pattern
    for i in range(1, min(9, len(sorted_nodes))):
        dx, dy = directions[(i - 1) % len(directions)]
        pos[sorted_nodes[i]] = (center[0] + dx, center[1] + dy)


    ring_distance = 2
    index = 9  # Start from the 9th node

    while index < len(sorted_nodes):
        for dx, dy in directions:

            for _ in range(ring_distance):
                if index >= len(sorted_nodes):
                    break
                pos[sorted_nodes[index]] = (center[0] + dx * ring_distance, center[1] + dy * ring_distance)
                index += 1
        ring_distance += 1

    occupied_positions = set(pos.values())
    for node in sorted_nodes:
        x, y = pos[node]
        while any(other_node != node and (other_x == x or other_y == y)
                  for other_node, (other_x, other_y) in pos.items()):
            x += 1
            y += 1
            pos[node] = (x, y)
            occupied_positions.add((x, y))

    return pos
