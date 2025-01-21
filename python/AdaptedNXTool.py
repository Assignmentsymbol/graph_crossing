import networkx
import Helpers
import matplotlib.pyplot as plt
import networkx as nwx



def bcc_decomposition(graph,edges,pos,width,height,draw):
    bcc = list(networkx.biconnected_components(graph))
    print(bcc.__len__())
    print('index: ' + bcc.index(max(bcc, key=len)).__str__())
    print(max(bcc, key=len).__len__())  # bad matching
    # sub_graph = nwx.complete_graph(bcc[bcc.index(max(bcc,key=len))])
    # sub_edges = sub_graph.edges()
    sub_graph = networkx.Graph()
    bcc.sort(key=len, reverse=True)
    sub_graph_nodes = bcc[0]
    sub_graph.add_nodes_from(sub_graph_nodes)
    sub_graph_edges = [(x, y) for (x, y) in edges if x in sub_graph_nodes and y in sub_graph_nodes]
    sub_pos = {node: (x, y) for node, (x, y) in pos.items() if node in sub_graph_nodes}
    print(f'nodes size: {len(sub_graph_nodes)} and edges size: {len(sub_graph_edges)} and pos size: {len(sub_pos)}')
    print(sub_graph_nodes)
    print(sub_graph_edges)
    sub_graph.add_edges_from(sub_graph_edges)
    if draw:
        Helpers.report_and_draw(sub_graph, sub_graph_edges, sub_pos, width, height)
    return pos


def planar_check(graph, nodes, edges, attributes, pos, width, height,draw):
    planarity = nwx.is_planar(graph)
    print(f"The graph is planar? : {planarity}")
    if planarity:
        pos = nwx.planar_layout(graph)
        # Note that snapped layout might not be necessarily planar if there is an un-snapped layout. Consider
        # the complete graph of k(4,4)/{any single e} with 4 square grid(√) and 6 square grid(X)
        print("The planar layout generated by nwx is :")
        # The nwx pos is such: {node_name: NumPy.array}
        print(pos)
        if draw:
            networkx.draw_networkx(graph, pos=pos, with_labels=True, node_color="red", node_size=1,
                                   font_color="white", font_size=10,
                                   font_weight="bold", width=1, edge_color="black")
            plt.margins(0.2)
            plt.show()
    pass

def fruchterman_reingold(graph, nodes, edges, attributes, pos, width, height,draw,silent):
    pos = networkx.fruchterman_reingold_layout(graph,pos=pos,iterations=20,scale=min(width,height)*(1/2),center=(width/2,height/2))
    if not silent:
        print(f'width: {width}, height: {height}, center: {width/2, height/2}')
        print(f'edge size: {len(edges)}')
    pos = Helpers.trivial_snap(graph.nodes,pos,width,height)
    if draw:
        Helpers.report_and_draw(graph,edges,pos,width,height)
    if not silent:
        print((pos.values()))
        print((pos.values()))
    return pos

def ask_for_operation(graph, nodes, edges, attributes, pos, width, height,draw):
    old_copy = pos.copy()
    user_input = input("p/f/d/n: ")
    if user_input == "n":
        return pos
    if user_input=='f':
        pos = fruchterman_reingold(graph,nodes,edges,attributes,pos,width,height,draw)
        Helpers.check_identical(old_copy, pos)
        if draw:
            networkx.draw_networkx(graph, pos=pos, with_labels=True, node_color="red", node_size=1,
                                   font_color="white", font_size=10,
                                   font_weight="bold", width=1, edge_color="black")
            plt.margins(0.2)
            plt.show()
        return ask_for_operation(graph, nodes, edges, attributes, pos, width, height, draw)
    if user_input=='p':
        pass
    return pos
