import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# Python program to find the orientation
# of the three points

# Function to find the orientation
def orientation(x1, y1, x2, y2, x3, y3):

    # orientation of an (x, y) triplet
    val = ((y2 - y1) * (x3 - x2)) - \
          ((x2 - x1) * (y3 - y2))

    if val == 0:
        print("Collinear")
    elif val > 0:
        print("Clockwise")
    else:
        print("CounterClockwise")


x1, y1, x2, y2, x3, y3 = 0, 0, 2, 0, 4, -1
orientation(x1, y1, x2, y2, x3, y3)
