""" Day 12 in the AoC house - Hill walk
time taken : 3hrs
leaderboard 2,3

Work away from the end noting the shortest distance from the last
Refine the distance recursively only revisiting spots where the distance has been lowered
"""

import numpy as np

from tools.common import file_to_list


class GridCursor2d:
    directions = [
        np.array([0, 1]),
        np.array([0, -1]),
        np.array([1, 0]),
        np.array([-1, 0]),
    ]

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.border_min = np.array([0, 0])
        self.border_max = np.array([rows, cols])

    def adjacent_positions(self, current_position: np.array):
        """Generator of possible adjacent positions for a given position"""
        for direction in self.directions:
            next_position = np.add(direction, current_position)
            if (self.border_min <= next_position).all() and (next_position < self.border_max).all():
                yield next_position


def find_element(a, e):
    """Returns a list of coordinates where this element is found"""
    findings = np.where(a == e)
    coordinates = list(zip(findings[0], findings[1]))
    return np.array(coordinates)


def parse_input():
    rows = []
    lines = file_to_list("day12.txt")
    for line in lines:
        e = [ord(height)-97 for height in line]
        rows.append(e)
    rows = np.array(rows)
    return rows


hills = parse_input()
grid_cursor = GridCursor2d(*hills.shape)
print(hills)

start = find_element(hills, -14)[0]
end = find_element(hills, -28)[0]

distance = np.full_like(hills, -1, dtype=int)
hills.itemset(*end, 26)
distance.itemset(*end, 0)


def refine_distance(cp, dist):
    h = hills.item(*cp)
    moves = []
    for adj_pos in grid_cursor.adjacent_positions(cp):
        adj_pos_height = hills.item(*adj_pos)
        adj_pos_distance = distance.item(*adj_pos)
        if adj_pos_height >= h-1 and (adj_pos_distance == -1 or adj_pos_distance > dist+1):
            moves.append(adj_pos)
            distance.itemset(*adj_pos, dist + 1)
    for m in moves:
        refine_distance(m, dist+1)


refine_distance(end, 0)
print(distance)


all_distances = [distance.item(*adj_pos) for adj_pos in grid_cursor.adjacent_positions(start)]
shortest = sorted(all_distances)[0]+1
print("A", shortest)


def best_dist(p):
    """Given a possible starting point what is the best path if any"""
    # only consider start points next to a viable path that starts with a "b"
    p_distances = [
        distance.item(*adj_pos) for adj_pos in grid_cursor.adjacent_positions(p)
        if distance.item(*adj_pos) > 0 and hills.item(*adj_pos) == 1
    ]
    if p_distances:
        return sorted(p_distances)[0] + 1
    else:
        return None


# get all the possible starting points (the "a"s)
pos_starts = find_element(hills, 0)
best_paths = [best_dist(p) for p in pos_starts if best_dist(p)]
best_of_the_best = sorted(best_paths)[0]
print("B", best_of_the_best)
