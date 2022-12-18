""" Day 18 in the AoC house - Obsidian Blob of Cubes
time taken : 2hr
leaderboard 1,1

"""

import operator
from time import time

import networkx as nx

from tools.common import file_to_list

stm = time()


def parse_int(file_name):
    lines = file_to_list(file_name)
    data = []
    for line in lines:
        ords = line.split(",")
        cube = tuple([int(n) for n in ords])
        data.append(cube)
    return data


def are_adjacent_cubes(cube_a, cube_b) -> bool:
    """Return True if two cubes are adjacent"""
    diff = tuple(map(operator.sub, cube_a, cube_b))
    diff_size = sum([abs(n) for n in diff])
    return diff_size == 1


def add_edges(gph, cube_list):
    """Given a graph of cube nodes and list of cubes add the edges to the graph
    to represent an adjacent cube"""
    for idx_a, cube_a in enumerate(cube_list):
        for idx_b, cube_b in enumerate(cube_list[idx_a + 1:]):
            if are_adjacent_cubes(cube_a, cube_b):
                gph.add_edge(cube_a, cube_b)


test_mode = 0
if test_mode:
    cubes = parse_int("day18_test.txt")
else:
    cubes = parse_int("day18.txt")

# Part A
G = nx.Graph()
G.add_nodes_from(cubes)
add_edges(G, cubes)
faces_a = len(G.nodes) * 6 - (len(G.edges) * 2)

etm = time()
elapsed_time = etm - stm
print(f"Time for part A: {elapsed_time:.3f} s")


print(f"A: {faces_a}")
an_exterior = None

# Part B
# Get all the air spaces
# Create an adjacency graph like above of them
# Determine the interior = those not connected to the exterior (using shortest_path)
# Calc interior faces and take that off Part A


def possible_directions():
    for i in range(3):
        d1 = [0] * 3
        d2 = [0] * 3
        d1[i] = -1
        d2[i] = 1
        yield tuple(d1)
        yield tuple(d2)


def gen_test_cubes():
    limits_for_range = [(min(list(z)), max(list(z)) + 1) for z in zip(*cubes)]
    print(f"Limits {limits_for_range}")
    for x in range(*limits_for_range[0]):
        for y in range(*limits_for_range[1]):
            for z in range(*limits_for_range[2]):
                cube = (x, y, z)
                if cube in cubes:
                    continue
                yield cube


def gen_air_gaps():
    global an_exterior
    limits_for_range = [(min(list(z)), max(list(z)) + 1) for z in zip(*cubes)]
    for x in range(*limits_for_range[0]):
        for y in range(*limits_for_range[1]):
            for z in range(*limits_for_range[2]):
                cube = (x, y, z)
                if cube in cubes:
                    continue
                if not an_exterior:
                    an_exterior = cube
                yield cube


# Get all the air spaces
air_gaps = list(gen_air_gaps())

# Create an adjacency graph like above of them
air_graph = nx.Graph()
air_graph.add_nodes_from(air_gaps)
add_edges(air_graph, air_gaps)
print(air_graph)

# Determine the interior = those not connected to the exterior (using shortest_path)
connected_to_exterior = nx.shortest_path(air_graph, source=an_exterior)
interior = [air_gap for air_gap in air_gaps if air_gap not in connected_to_exterior]

# Calc interior faces using same idea from part A
interior_graph = nx.Graph()
interior_graph.add_nodes_from(interior)
add_edges(interior_graph, interior)
interior_faces = len(interior_graph.nodes) * 6 - (len(interior_graph.edges) * 2)
print(f"less the interior faces: {interior_faces}")

# Take that off Part A
faces_b = faces_a - interior_faces
print(f"B: ext faces: {faces_b}")

etm = time()
elapsed_time = etm - stm
print(f"time taken: {elapsed_time:.3f} s")
