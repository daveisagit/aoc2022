""" Day 4 in the AoC house and Dave devilishly attempts to thwart James' 100% trajectory
with an early start despite it being Sunday
"""

from collections import namedtuple

Assignment = namedtuple(
    "Assignment", ["lower", "upper"]
)


def get_assignment(ass: str):
    limits = ass.split("-")
    return Assignment(int(limits[0]), int(limits[1]))


def overlaps(ass1: Assignment, ass2: Assignment, cmp: callable):
    return cmp(ass1, ass2) or cmp(ass2, ass1)


def partially(ass1: Assignment, ass2: Assignment):
    return ass2.lower <= ass1.upper <= ass2.upper


def fully(ass1: Assignment, ass2: Assignment):
    return ass2.lower <= ass1.lower and ass1.upper <= ass2.upper


if __name__ == '__main__':
    with open('input/day4.txt') as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]

    pairs = [line.split(",") for line in lines]
    assignments = [(get_assignment(pair[0]), get_assignment(pair[1])) for pair in pairs]

    partials = [overlaps(ass[0], ass[1], partially) for ass in assignments]
    total = [overlap for overlap in partials if overlap]
    print("A: ", len(total))

    fulls = [overlaps(ass[0], ass[1], fully) for ass in assignments]
    total = [overlap for overlap in fulls if overlap]
    print("B: ", len(total))
