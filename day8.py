""" Day 8 in the AoC house and Nick smashes another early 1st

For me so much miscomprehended here initially
I thought on part a) they wanted the sum of heights ( oh dear too much beer, not enough sleep Zzzz )
I thought on part b) that say given 521111111153333 the first 5 looking right would not see any of the 1's being hidden
by the 2 (BUT that is not what was defined!), 5 would see all of them but nothing after the next 5

Good to learn a bit more about numpy arrays
"""
from collections import namedtuple

import numpy as np
from tools.common import file_to_list

lines = file_to_list("day8.txt")

woods = []
for line in lines:
    e = [int(height) for height in line]
    woods.append(e)
woods = np.array(woods)

# a tuple of slices of what the subject tree would see looking out to the edge in each direction
CrossHair = namedtuple(
    "CrossHair", ["down", "up", "left", "right"]
)


def get_cross_hair(a_2d, row, col):
    """Given a 2D array and row,col indexes return the 4 slices that span out to the edge of the matrix
    as a list of slices"""

    return CrossHair(
        down=a_2d[row+1:, col],
        up=a_2d[:row, col][::-1],
        right=a_2d[row, col+1:],
        left=a_2d[row, :col][::-1]
    )


can_be_seen = np.full_like(woods, 0)
for idx, val in np.ndenumerate(woods):
    r = idx[0]
    c = idx[1]
    views = get_cross_hair(woods, r, c)
    max_heights = []
    for view in views:
        max_height = -1
        if len(view) > 0:
            max_height = np.max(view)
        max_heights.append(max_height)

    clear_views = [1 if max_height < val else 0 for max_height in max_heights]
    seen = max(clear_views)
    can_be_seen[r][c] = seen

print("A: Count of trees that can be seen", np.sum(can_be_seen))

scenic_score = np.full_like(woods, 0)
for idx, val in np.ndenumerate(woods):
    r = idx[0]
    c = idx[1]
    views = get_cross_hair(woods, r, c)
    score = 1
    for view in views:
        sc = 0
        for t in view:
            sc += 1
            if t >= val:
                break
        score *= sc
    scenic_score[r][c] = score

print("B: Best scenic score", np.max(scenic_score))


