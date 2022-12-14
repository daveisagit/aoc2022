""" Day 14 in the AoC house - Falling sand
time taken : 1hr
leaderboard 1,1

"""
from tools.common import file_to_list
from tools.grid import limits_of_point_set, Point, point_add, point_sub, str_to_point, \
    straight_path_of_points_between

lines = file_to_list("day14.txt")

origin = Point(500, 0)
rock_walls = []
cave = {}


def parse_rock_points():
    """Get all the points marking out the rock lines as a
    list of
        list of
            point tuples
    """
    for line in lines:
        rock_points = line.split(" -> ")
        points = []
        for rock_point in rock_points:
            rock_point = str_to_point(rock_point)
            points.append(rock_point)
        rock_walls.append(points)


def print_cave(w_min: Point, w_max: Point):
    """print an ascii representation of the cave state"""
    print()
    for y in range(w_max.y + 2):
        r = ""
        for x in range(w_min.x - 2, w_max.x + 2):
            p = Point(x, y)
            if y == 0 and x == 500:
                e = "+"
            else:
                e = cave.get(p, ".")
            r = r + e
        print(r)


def finish_point(c):
    """From a give point can it fall further
    return
        -the new point if it can
        -itself if it can't
        -None if past the point of free fall into the abyss
        """
    if c.y > g_max.y+2:
        return None
    n = Point(c.x, c.y+1)
    if n not in cave:
        return finish_point(n)
    if n in cave:
        nl = Point(n.x - 1, n.y)
        if nl in cave:
            nr = Point(n.x + 1, n.y)
            if nr in cave:
                return c
            return finish_point(nr)
        return finish_point(nl)


def initialise_cave():
    global cave
    cave = {}
    for rock_wall in rock_walls:
        for idx in range(1, len(rock_wall)):
            for point in straight_path_of_points_between(rock_wall[idx-1], rock_wall[idx]):
                cave[point] = "#"


# parse the input into structured data
parse_rock_points()
all_points = [p for w in rock_walls for p in w]
g_min, g_max = limits_of_point_set(all_points)
initialise_cave()
save_cave = cave.copy()


# Part A
cnt = 0
while True:
    """Fill your boots until the abyss"""
    p = finish_point(origin)
    if p:
        cnt += 1
        cave[p] = "o"
    else:
        break
print("A: ", cnt)
# print_cave(g_min, g_max)

# Part B

# restore empty cave from save
cave = save_cave.copy()

# increase the limits and paint in the floor
g_max = point_add(g_max, Point(0, 2))
g_min = point_sub(g_min, Point(g_max.y, 0))
g_max = point_add(g_max, Point(g_max.y, 0))
for x in range(g_min.x - 1, g_max.x + 1):
    cave[(x, g_max.y)] = "#"
# print_cave(g_min, g_max)

cnt = 0
while True:
    """Fill your boots until the origin is plugged"""
    p = finish_point(origin)
    if p == origin:
        break
    if p:
        cnt += 1
        cave[p] = "o"
    else:
        break

# print_cave(g_min, g_max)
print("B: ", cnt + 1)
