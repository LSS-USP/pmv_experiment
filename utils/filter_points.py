#!/bin/python3

from xml.dom import minidom
from scipy.spatial import distance
import numpy as np
import pandas as pd


def load_nodes():
    map_path = "../city_scale/inputs/map.xml"
    # map_path = "../validation/inputs/hex_map.xml"
    dom = minidom.parse(map_path)\
            .getElementsByTagName('node')
    mylist = []
    for u in dom:
        mylist.append([
            int(u.getAttribute('id')),
            float(u.getAttribute('x')),
            float(u.getAttribute('y'))
        ])
    return mylist

def load_edges():
    map_path = "../city_scale/inputs/map.xml"
    # map_path = "../validation/inputs/hex_map.xml"
    dom = minidom.parse(map_path)\
            .getElementsByTagName('link')
    results = {}
    for u in dom:
        results[int(u.getAttribute('id'))] = [
            int(u.getAttribute('from')),
            int(u.getAttribute('to'))
        ]

    return results

print("Loading map edges...")
edges = load_edges()
print("Map edges loaded...")
print(len(edges))

print("Loading map nodes...")
nodes = {}
for u in load_nodes():
    nodes[u[0]] = [u[1], u[2]]
print("Map nodes loaded...")

ref_node_id = 1492963064

x1, y1 = nodes[ref_node_id]
start = nodes[ref_node_id]

affected_edges = []
total = 0
for k, v in edges.items():
    origin, destination = v
    if (origin != ref_node_id):
        dst = distance.euclidean(start, nodes[origin])
        if (dst <= 1000):
            total += 1
            affected_edges.append(k)

    if (destination != ref_node_id):
        dst = distance.euclidean(start, nodes[destination])
        if (dst <= 1000):
            total += 1
            affected_edges.append(k)

affected_edges = np.unique(affected_edges)
print("Arestas afetadas => ", len(affected_edges))
print("Qtd de arestas => ", len(edges))
df = pd.DataFrame(data=affected_edges)
df.to_csv("affected_edges.csv", header=False,index=False)
