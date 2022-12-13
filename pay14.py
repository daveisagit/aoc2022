""" Day 14 in the AoC house - Falling sand
time taken : 1hr
leaderboard 1,1

"""
from tools.common import file_to_list

lines = file_to_list("day14.txt")

origin = (500, 0)
rock_walls = []
min_x = 99999
min_y = 99999
max_x = 0
max_y = 0
cave = {}


def parse_rock_points():
    """Get all the points marking out the rock lines as a
    list of
        list of
            point tuples
    Note the min/max x,y values along the way
    """
    global min_x, min_y, max_x, max_y
    for line in lines:
        rock_points = line.split(" -> ")
        points = []
        for rock_point in rock_points:
            rock_point = rock_point.split(",")
            x = int(rock_point[0])
            y = int(rock_point[1])
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)
            points.append((x, y))
        rock_walls.append(points)


def path_gen(a,b):
    """Generate a list of points between 2 points that vertical/horizontally aligned"""
    if a[0] == b[0]:
        d = (a[1] < b[1]) - (a[1] > b[1])
        if d == 0:
            yield a
            return
        for i in range(a[1], b[1]+d, d):
            yield a[0], i
    if a[1] == b[1]:
        d = (a[0] < b[0]) - (a[0] > b[0])
        for i in range(a[0], b[0]+d, d):
            yield i, a[1]


def print_cave():
    """print an ascii representation of the cave state"""
    for y in range(max_y+4):
        r = ""
        for x in range(min_x-2, max_x+3):
            if y == 0 and x == 500:
                e = "+"
            else:
                e = cave.get((x, y), ".")
            r = r + e
        print(r)


def finish_point(c):
    """From a give point can it fall further
    return
        -the new point if it can
        -itself if it can't
        -None if past the point of free fall into the abyss
        """
    if c[1] > max_y+2:
        return None
    n = (c[0], c[1]+1)
    if n not in cave:
        return finish_point(n)
    if n in cave:
        nl = (n[0]) - 1, n[1]
        if nl in cave:
            nr = (n[0]) + 1, n[1]
            if nr in cave:
                return c
            return finish_point(nr)
        return finish_point(nl)


def initialise_cave():
    global cave
    cave = {}
    for rock_wall in rock_walls:
        for idx in range(1, len(rock_wall)):
            for point in path_gen(rock_wall[idx-1], rock_wall[idx]):
                cave[point] = "#"


# parse the input into structured data
parse_rock_points()
initialise_cave()
save_cave = cave.copy()

# Part A
cnt = 0
while True:
    """Fill your boots until the abyss"""
    p = finish_point(origin)
    if p:
        cnt += 1
        cave[p] = "O"
    else:
        break
print("A: ", cnt)

# Part B
# increase the limits and paint in the floor
cave = save_cave.copy()
max_y = max_y + 2
min_x = min_x - max_y + 2
max_x = max_x + max_y + 2
for x in range(min_x - 2, max_x + 3):
    cave[(x, max_y)] = "#"

cnt = 0
while True:
    """Fill your boots until the origin is plugged"""
    p = finish_point(origin)
    if p == origin:
        break
    if p:
        cnt += 1
        cave[p] = "O"
    else:
        break

print("B: ", cnt + 1)
