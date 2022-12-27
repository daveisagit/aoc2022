""" Day 23 in the AoC house - Game of Lefl
time taken :
leaderboard

"""
import math
from collections import Counter, namedtuple
from time import time

import numpy as np

from tools.common import file_to_string

priority = (
    ((-1, -1), (-1, 0), (-1, 1)),
    ((1, -1), (1, 0), (1, 1)),
    ((-1, -1), (0, -1), (1, -1)),
    ((-1, 1), (0, 1), (1, 1)),
)

surround = (
    (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1),
)


def add_tuples(a, b):
    return tuple([sum(x) for x in zip(a, b)])


def sub_tuples(a, b):
    return tuple([x[0]-x[1] for x in zip(a, b)])


def limit_nw(locations):
    x, y = zip(*locations)
    return min(x), min(y)


def limit_se(locations):
    x, y = zip(*locations)
    return max(x), max(y)


def crop(locations):
    top_left = limit_nw(locations)
    return [sub_tuples(loc, top_left) for loc in locations]


def to_matrix(locations):
    # base = ord("A")
    shape = limit_se(locations)
    shape = add_tuples(shape, (1, 1))
    loc_matrix = np.full(shape, ".", dtype=str)
    for idx, elf in enumerate(locations):
        # loc_matrix[elf] = chr(base + idx)
        loc_matrix[elf] = "#"
    return loc_matrix


def draw_locations(locations):
    # cropped = crop(locations)
    m = to_matrix(locations)
    for row in m:
        print("".join(row))
    print()


stm = time()

test_mode = 0

if test_mode:
    filename = "day23_test.txt"
else:
    filename = "day23.txt"

with open(f"input/{filename}") as f:
    lines = f.readlines()

start_locations = []
for r, row in enumerate(lines):
    for c, ch in enumerate(row):
        if ch == "#":
            start_locations.append((r, c))


def do_round(current_locations, move_count=0):
    proposed = []
    no_movement = True
    for idx, loc in enumerate(current_locations):

        remain = True
        for direction in surround:
            nxt = add_tuples(loc, direction)
            if nxt in current_locations:
                remain = False
                break

        if remain:
            proposed.append(loc)
            continue

        nxt = loc
        for x in range(4):
            i = x + move_count
            i %= 4
            direction = priority[i]
            clear = True
            for w in range(3):
                chk = add_tuples(loc, direction[w])
                if chk in current_locations:
                    clear = False
                    break
            if clear:
                nxt = add_tuples(loc, direction[1])
                break

        proposed.append(nxt)
        if nxt != loc:
            no_movement = False

    cnt = Counter(proposed)
    actual = [loc if cnt[loc] == 1 else current_locations[idx] for idx, loc in enumerate(proposed)]
    return actual, no_movement


def solve_a(rounds=10):
    cur_locations = start_locations.copy()
    for move_count in range(rounds):
        cur_locations = do_round(cur_locations, move_count=move_count)

    cur_locations = crop(cur_locations)
    draw_locations(cur_locations)
    shape = limit_se(cur_locations)
    shape = add_tuples(shape, (1, 1))
    area = shape[0] * shape[1]
    space = area - len(cur_locations)
    print(space)


def solve_b():
    cur_locations = start_locations.copy()
    cnt = 0
    moving = True
    while moving:
        print(cnt)
        new_locations, no_movement = do_round(cur_locations, move_count=cnt)
        cnt += 1
        if no_movement:
            print(cnt)
            break
        cur_locations = new_locations


solve_a()

solve_b()




