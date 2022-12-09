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


def cmp(a, b):
    return (a > b) - (a < b)


# create a ufunc to run over a matrix
np_cmp = np.frompyfunc(cmp, 2, 1)


def tail_adj(head, tail):
    """Given a head and tail position return the adjustment for the tail"""
    # get the biggest difference in any direction
    diff = np.max(np.abs(np.subtract(head, tail)))
    if diff <= 1:
        # if within 1 all round then no adjustment needed
        return np.array([0, 0])

    # return a sort of unit vector adjustment for t
    return np_cmp(head, tail)


lines = file_to_list("day9.txt")

moves = [Move(*line.split(" ")) for line in lines]
moves = [Move(direction=v_map[m.direction], amount=int(m.amount)) for m in moves]


def get_trace_count(number_of_knots):
    origin = np.array([0, 0])
    knots = [origin] * number_of_knots
    tail_trace = set()
    for m in moves:
        for i in range(m.amount):
            knots[0] = np.add(knots[0], m.direction)
            for j in range(1, number_of_knots):
                ka = tail_adj(knots[j-1], knots[j])
                kp = knots[j]
                kp = np.add(kp, ka)
                knots[j] = kp
            tail_trace.add(tuple(o for o in kp))
    return len(tail_trace)


print("A) 2 knots ", get_trace_count(2))
print("B) 10 knots", get_trace_count(10))

