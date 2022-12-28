""" Day 24 in the AoC house - Blizzards
time taken :
leaderboard

"""
import math
from collections import Counter, deque, namedtuple
from time import time

import numpy as np

from tools.common import file_to_string

OPTIONS = (
    (0, 1), (1, 0), (0, -1), (-1, 0), (0, 0)
)

DIRECTIONS = ">v<^"


def add_tuples(a, b):
    return tuple([sum(x) for x in zip(a, b)])


def load_blizzards():
    global valley_w, valley_h
    valley_w = len(lines[0]) - 3
    valley_h = len(lines) - 2
    for r, line in enumerate(lines[1:-1]):
        for c, ch in enumerate(line[1:-2]):
            if ch in DIRECTIONS:
                d = DIRECTIONS.index(ch)
                blizzard = blizzards[d]
                blizzard.append((r, c))


def draw_valley():
    flat = [loc for blizzard in blizzards for loc in blizzard]
    cnt = Counter(flat)
    print(cnt)
    print("#" * (valley_w+2))
    for r in range(valley_h):
        line = "#"
        for c in range(valley_w):
            if (r, c) in flat:
                if cnt[(r, c)] > 1:
                    line += str(cnt[(r, c)])
                else:
                    for d, arrow in enumerate(DIRECTIONS):
                        if (r, c) in blizzards[d]:
                            line += arrow
                            break
            else:
                line += "."
        line += "#"
        print(line)

    print("#" * (valley_w + 2))


def move_blizzards():
    new_blizzards = []
    for d, blizzard in enumerate(blizzards):
        new_blizzard = []
        for loc in blizzard:
            new_loc = add_tuples(loc, OPTIONS[d])
            new_loc = (new_loc[0] % valley_h, new_loc[1] % valley_w)
            new_blizzard.append(new_loc)
        new_blizzards.append(new_blizzard)
    return new_blizzards


def quickest_time(start, end):
    global blizzards
    blizzards = move_blizzards()
    queue = deque([(0, start)])
    last_minute = 0
    already_done = set()
    while queue:

        state = queue.popleft()

        if state in already_done:
            continue

        already_done.add(state)
        # print(state)
        minute, cur_pos = state

        if cur_pos == end:
            return minute + 1

        if minute > last_minute:
            # print(f"Min: {minute} {cur_pos} {len(queue)}")
            blizzards = move_blizzards()
            last_minute = minute

        all_blizzards = [loc for blizzard in blizzards for loc in blizzard]
        for opt in OPTIONS:
            new_pos = add_tuples(cur_pos, opt)
            if new_pos == start or (0 <= new_pos[0] < valley_h and 0 <= new_pos[1] < valley_w):
                if new_pos not in all_blizzards:
                    new_state = minute + 1, new_pos
                    queue.append(new_state)


stm = time()

test_mode = 1

if test_mode:
    filename = "day24_test.txt"
else:
    filename = "day24.txt"

with open(f"input/{filename}") as f:
    lines = f.readlines()

blizzards = [list() for x in range(4)]
valley_w = 0
valley_h = 0


load_blizzards()
out_at = quickest_time((-1, 0), (valley_h-1, valley_w-1))
etm = time()
elapsed_time = etm - stm
print(f"Time for part A: {elapsed_time:.3f} s")
print(f"Part A: {out_at}")
print()

back_in = quickest_time((valley_h, valley_w-1), (0, 0))
etm = time()
elapsed_time = etm - stm
print(f"Part B - return: {back_in}")
print(f"Time for return: {elapsed_time:.3f} s")


out_again = quickest_time((-1, 0), (valley_h-1, valley_w-1))
etm = time()
elapsed_time = etm - stm
print(f"Part B - out again: {out_again}")
print(f"Time for out_again: {elapsed_time:.3f} s")
print()
print(f"Part B - Total: {out_at + back_in + out_again}")
