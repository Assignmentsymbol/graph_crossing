import networkx as nwx
import matplotlib.pyplot as plt
import numpy as np
import Helpers
from Helpers import show_grid as sg

G = nwx.Graph()
G.add_node("A")
G.add_node("B")
G.add_node("C")
G.add_node("D")

G.add_edge("A", "C")
G.add_edge("B", "C")
G.add_edge("B", "D")
G.add_edge("C", "D")

edge1 = ("C", "D")
edge2 = ("B", "D")


pos={
    "A":(1,5),
    "B":(4,7),
    "C":(6,2),
    "D":(5,0),
    "E":(8,4)
}

print(G.nodes)
print(G.edges)
Helpers.is_intersect(edge1,edge2,pos,False)
# plt.figure(figsize=(1, 1))
# plt.figure()
# plt.axes().set_axis_on()
nwx.draw_networkx(G,pos=pos,with_labels=True,node_color="red",node_size=1000,
                  font_color="white",font_size=20,font_family="Times New Roman", font_weight="bold",width=3,edge_color="black")

plt.margins(0.2)

sg()
plt.show()



