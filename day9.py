""" Day 9 in the AoC house
time taken 1:15
leaderboard 1,1

Another 2D simulation, might be possible to not model the grid and just keep track of
knot positions, recording the trace in a dict

Slightly fiddly rule on the adjustment of the tail

"""
from collections import namedtuple
import numpy as np
from tools.common import file_to_list

Move = namedtuple(
    "Move", ["direction", "amount", ]
)

v_map = {
    "U": np.array([0, 1]),
    "D": np.array([0, -1]),
    "R": np.array([1, 0]),
    "L": np.array([-1, 0]),
}

lines = file_to_list("day9.txt")

moves = [Move(*line.split(" ")) for line in lines]
moves = [Move(direction=v_map[m.direction], amount=int(m.amount)) for m in moves]
print(moves)

p = np.zeros((2,), int)
min_p = np.zeros((2,), int)
max_p = np.zeros((2,), int)
for m in moves:
    p = np.add(p, m.direction*m.amount)
    max_p = np.maximum(max_p, p)
    min_p = np.minimum(max_p, p)

print("limits", min_p, max_p)

req = np.subtract(max_p, min_p)
req = tuple(r+1 for r in req)
print("shape required", req)

origin = np.subtract(req, max_p)
origin = np.subtract(origin, np.array([1, 1]))
print("origin offset", origin)

tg = np.zeros(req, int)


def scalar_adj(a: int, b: int) -> int:
    if a > b:
        return 1
    elif b > a:
        return -1
    else:
        return 0


# create a ufunc to run over a matrix
np_scalar_adj = np.frompyfunc(scalar_adj, 2, 1)


def tail_adj(head, tail):
    """Given a head and tail position return the adjustment for the tail"""
    # get the biggest difference in any direction
    diff = np.max(np.abs(np.subtract(head, tail)))
    if diff <= 1:
        # if within 1 all round then no adjustment needed
        return np.array([0, 0])

    # return a sort of unit vector adjustment for t
    return np_scalar_adj(head, tail)


hp = origin
tp = origin
# this is how to set the value of a cell using a vector
# to give location
tg.itemset(*tp, 1)
for m in moves:
    for i in range(m.amount):
        hp = np.add(hp, m.direction)
        ta = tail_adj(hp, tp)
        tp = np.add(tp, ta)
        tg.itemset(*tp, 1)

print("A) Tail positions", np.sum(tg))


# keep track of the 10 knot positions
# 0 is the head, 9 is the tail
tg = np.zeros(req, int)
tg.itemset(*origin, 1)
knot_pos = [origin] * 10

for m in moves:
    for i in range(m.amount):
        for j in range(10):

            kp = knot_pos[j]

            if j == 0:
                # move the head
                kp = np.add(kp, m.direction)
            else:
                # adjust each subsequent knot
                kp_prv = knot_pos[j-1]
                ka = tail_adj(kp_prv, kp)
                kp = np.add(kp, ka)

            # set new knot position
            knot_pos[j] = kp

        # note where the tail has been
        tg.itemset(*knot_pos[9], 1)

print("B) Tail positions", np.sum(tg))



