""" Day 22 in the AoC house - Map Part B
time taken : days .....

Part B - new plan required

- Build the net as a graph of 2D points as nodes, there will be 14 nodes and 19 edges
- Reduce the above to a cube net 8 nodes and 12 edges:
        . Merge qualifying node pairs, which will lower the node/edge count by 1 each go
        . A qualifying node is one of deg<4 that is adjacent to one of deg=4
        . Do not pair nodes on the same face or ones on adjacent faces
- As we reduce the nodes, we keep track of the original 2D point that created it such that
  all 14 nodes will map to the final 8. We also track the faces that the node is on.

- We then build a directed graph of the faces which are identified by their (top,left) point
  The edges of this graph are labelled with a direction value (0-3). For example from face A
  going in direction d, puts you on face B. Going from B->A will have a different direction value.
  Edges have a value for direction as well as a tuple of the (left,right) nodes relative to the direction of travel.

The implementation of the above I've separated for re-use in a module called cubenet
which uses the networkx package.

We now travel using the face graph to determine the following when it hit the boundary
a) New face
b) New direction
c) Offset from the left (relative to travel)

"""

import math
from time import time

import numpy as np

from tools.common import file_to_string
from tools.cubenet import cubify, face_graph, parse_points, Point

stm = time()

test_mode = 0

if test_mode:
    filename = "day22_map_test.txt"
    moves = file_to_string("day22_moves_test.txt")
else:
    filename = "day22_map.txt"
    moves = file_to_string("day22_moves.txt")

with open(f"input/{filename}") as f:
    map_lines = f.readlines()

map_lines = [line[:-1] for line in map_lines]
map_height = len(map_lines)
map_width = max([len(line) for line in map_lines])
map_lines = [line.ljust(map_width) for line in map_lines]

map_matrix = np.empty((map_height, map_width), dtype=str)
for row, line in enumerate(map_lines):
    for col, ch in enumerate(line):
        map_matrix[row, col] = ch


DIRECTION_CHANGES = {
    "^": "^>v<",
    ">": ">v<^",
    "v": "v<^>",
    "<": "<^>v"
}

DIRECTION_VALUES = {
    "^": 3,
    ">": 0,
    "v": 1,
    "<": 2
}

DIRECTION_CHAR = {v: k for k, v in DIRECTION_VALUES.items()}

face_size = 50
if test_mode:
    face_size = 4

map_matrix = np.pad(map_matrix, ((0, face_size), (0, face_size)), mode='constant', constant_values=" ")
map_height += face_size
map_width += face_size

face_matrices = {}
net_points = set()
for row in range(0, map_height, face_size):
    for col in range(0, map_width, face_size):
        if map_matrix[row, col] != " ":
            net_points.add((row, col))
            net_points.add((row + face_size, col))
            net_points.add((row, col + face_size))
            net_points.add((row + face_size, col + face_size))
            face_matrix = map_matrix[row:row + face_size, col:col + face_size]
            pos = row // face_size, col // face_size
            face_matrices[pos] = face_matrix


vg = parse_points(list(net_points), edge_length=face_size)
# dump_net_data(vg)
vg = cubify(vg)
# draw_net(vg)
fg = face_graph(vg)
# dump_face_graph(fg)

moves_left = moves
move_list = []

# load the moves
while len(moves_left) > 0:
    try:
        right = moves_left.index("R")
    except ValueError:
        right = math.inf
    try:
        left = moves_left.index("L")
    except ValueError:
        left = math.inf
    next_d = min(left, right)

    if next_d == math.inf:
        x = int(moves_left)
        moves_left = ""
        d = None
    else:
        x = int(moves_left[:next_d])
        d = moves_left[next_d]
        moves_left = moves_left[next_d+1:]

    move_list.append(x)
    if d:
        move_list.append(d)

#
# Lets begin the cube walk
#
current_dir = 0
route_matrix = np.copy(map_matrix)
cur_face = min(fg.nodes)
cur_matrix = face_matrices[cur_face]
cur_point = Point(0, min(np.where(cur_matrix[0] == ".")[0]))


def next_point(p: Point, dr, mag=1) -> Point | None:
    next_r = (p.row + (2 - dr) * mag * (dr % 2))
    next_c = (p.col + (1 - dr) * mag * ((dr + 1) % 2))
    if 0 <= next_r < face_size and 0 < next_c < face_size:
        return Point(next_r, next_c)
    else:
        return None


def set_new_journey():
    new_face = [e[1] for e in fg.edges(cur_face, data=True) if e[2]["dir"] == current_dir][0]
    arrive_on_edge_number = [e[2]["dir"] for e in fg.edges(new_face, data=True) if e[1] == cur_face][0]
    new_direction = (arrive_on_edge_number + 2) % 4

    offset_from_left = None
    if current_dir == 0:
        offset_from_left = cur_point.row
    if current_dir == 1:
        offset_from_left = face_size - 1 - cur_point.col
    if current_dir == 2:
        offset_from_left = face_size - 1 - cur_point.row
    if current_dir == 3:
        offset_from_left = cur_point.col

    # leaving_edge = [e[2]["edge"] for e in fg.edges(cur_face, data=True) if e[2]["dir"] == current_dir][0]
    # arriving_edge = [e[2]["edge"] for e in fg.edges(new_face, data=True) if e[2]["dir"] == arrive_on_edge_number][0]

    # print("CHANGE")
    # print("leaving_edge", leaving_edge)
    # print("arriving_edge", arriving_edge)
    # print("cur_point", cur_point)
    # print("current_dir", current_dir)
    # print("arrive_on_edge_number", arrive_on_edge_number)
    # print("offset_from_left", offset_from_left)

    new_point = None
    if arrive_on_edge_number == 0:
        new_point = Point(face_size - 1 - offset_from_left, face_size - 1)
    if arrive_on_edge_number == 1:
        new_point = Point(face_size - 1, offset_from_left)
    if arrive_on_edge_number == 2:
        new_point = Point(offset_from_left, 0)
    if arrive_on_edge_number == 3:
        new_point = Point(0, face_size - 1 - offset_from_left)

    return new_direction, new_face, new_point


for mv in move_list:
    if isinstance(mv, int):
        for i in range(mv):
            # print("cur_face", cur_face)
            # print("cur_point", cur_point)
            # print("current_dir", current_dir)
            nxt_point = next_point(cur_point, current_dir)
            # print("nxt_point", nxt_point)

            if nxt_point is None:
                t = set_new_journey()
                new_dir, new_face, nxt_point = t
                nxt_matrix = face_matrices[new_face]
                next_char = nxt_matrix[nxt_point]
                # print("next_char", next_char)

                if next_char == "#":
                    break
                elif next_char == ".":
                    cur_point = nxt_point
                    current_dir = new_dir
                    cur_matrix = nxt_matrix
                    cur_face = new_face

            else:
                next_char = cur_matrix[nxt_point]
                # print("next_char", next_char)
                if next_char == "#":
                    break
                elif next_char == ".":
                    cur_point = nxt_point

    else:
        if mv == "R":
            current_dir += 1
        else:
            current_dir -= 1
        current_dir %= 4

    # route_matrix[cur_row, cur_col] = current_dir

# print("cur_point", cur_point)
# print("current_dir", current_dir)
# print("cur_face", cur_face)

current_row = cur_face.row * face_size + cur_point.row + 1
current_col = cur_face.col * face_size + cur_point.col + 1
# print("current_row", current_row)
# print("current_col", current_col)
part_b = 1000 * current_row + 4 * current_col + current_dir
print(f"B: {part_b}")
etm = time()
elapsed_time = etm - stm
print(f"Time for part B: {elapsed_time:.3f} s")
