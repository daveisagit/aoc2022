""" Day 22 in the AoC house - Map
time taken :
leaderboard

Plan
Determine for every point and direction the
- maximum walking distance
- distance to edge
- modulus wrap around

store this in a matrix of tuples known as limits

Read through the moves and use the "limits" matrix to adjust the row,col
as required

"""
import math
from collections import namedtuple
from time import time

import numpy as np

from tools.common import file_to_string

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

print("Size", map_height, map_width)

map_matrix = np.empty((map_height, map_width), dtype=str)
for row, line in enumerate(map_lines):
    for col, ch in enumerate(line):
        map_matrix[row, col] = ch

limit_matrix = np.empty_like(map_matrix, dtype=dict)

Limit = namedtuple(
    "L", ["max_walk", "off_at", "walk_mod"]
)

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


def get_cross_hair(r, c):
    return {
        "v": map_matrix[r + 1:, c],
        "^": map_matrix[:r, c][::-1],
        ">": map_matrix[r, c + 1:],
        "<": map_matrix[r, :c][::-1]
    }


def get_limits_for_position(r, c):
    cross_hair = get_cross_hair(r, c)
    paths_to_walls = {
        d: "".join(p).strip() for d, p in cross_hair.items()
    }
    limits = {}
    for d, p in paths_to_walls.items():
        opposite_direction = DIRECTION_CHANGES[d][2]
        opposite_path = paths_to_walls[opposite_direction]
        full_path: str = p + opposite_path[::-1]
        max_walk = 0
        if "#" in full_path:
            idx = full_path.index("#")
            max_walk = idx
        off_at = len(p)
        walk_mod = len(p) + len(opposite_path)
        limits[d] = Limit(max_walk, off_at, walk_mod)

    return limits


for row, line in enumerate(map_matrix):
    for col, ch in enumerate(line):
        if ch == ".":
            limit_matrix[row, col] = get_limits_for_position(row, col)


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

current_dir = ">"
route_matrix = np.copy(map_matrix)
cur_row = 0
cur_col = min(np.where(map_matrix[0] == ".")[0])

for mv in move_list:
    if isinstance(mv, int):
        limit: Limit = limit_matrix[cur_row, cur_col][current_dir]
        walk = min(mv, limit.max_walk)
        route_matrix[cur_row, cur_col] = current_dir

        if current_dir == ">":
            for i in range(walk):
                if i == limit.off_at:
                    cur_col -= limit.walk_mod
                else:
                    cur_col += 1
                    if cur_col >= map_width:
                        cur_col = 0
                route_matrix[cur_row, cur_col] = ">"

        if current_dir == "<":
            for i in range(walk):
                if i == limit.off_at:
                    cur_col += limit.walk_mod
                else:
                    cur_col -= 1
                    if cur_col < 0:
                        cur_col = map_width - 1
                route_matrix[cur_row, cur_col] = "<"

        if current_dir == "^":
            for i in range(walk):
                if i == limit.off_at:
                    cur_row += limit.walk_mod
                else:
                    cur_row -= 1
                    if cur_row < 0:
                        cur_row = map_height - 1
                route_matrix[cur_row, cur_col] = "^"

        if current_dir == "v":
            for i in range(walk):
                if i == limit.off_at:
                    cur_row -= limit.walk_mod
                else:
                    cur_row += 1
                    if cur_row >= map_height:
                        cur_row = 0
                route_matrix[cur_row, cur_col] = "v"

    else:
        if mv == "R":
            chg = 1
        else:
            chg = 3
        current_dir = DIRECTION_CHANGES[current_dir][chg]


part_a = 1000 * (cur_row+1) + 4 * (cur_col+1) + DIRECTION_VALUES[current_dir]
print(f"A: {part_a}")
etm = time()
elapsed_time = etm - stm
print(f"Time for part A: {elapsed_time:.3f} s")
