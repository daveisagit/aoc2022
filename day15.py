""" Day 15 in the AoC house - Sensors and Beacons
time taken : 1hr
leaderboard 1

"""
from tools.common import file_to_list
from tools.grid import limits_of_point_set, manhattan_distance, orthogonal_points, Point


def initialise_space():
    global space
    space = {}
    for beacon in beacons:
        space[beacon] = "B"
    for sensor in sensors:
        space[sensor] = "S"


def draw_space():
    """print an ascii representation of space"""
    for y in range(min_g.y, max_g.y+1):
        r = f"{y:12} "
        for x in range(min_g.x, max_g.x+1):
            p = Point(x,y)
            e = space.get((x, y), ".")
            if manhattan_distance(p, sensors[6]) <= mds[6] and e == ".":
                e = "#"
            r = r + e
        print(r)


lines = file_to_list("day15.txt")

beacons = []
sensors = []
for line in lines:
    line = line.split(":")
    st = line[0].split(",")
    bt = line[1].split(",")
    stx = st[0]
    sty = st[1]
    btx = bt[0]
    bty = bt[1]
    stx = int(stx.split("=")[1])
    sty = int(sty.split("=")[1])
    btx = int(btx.split("=")[1])
    bty = int(bty.split("=")[1])
    beacons.append(Point(btx, bty))
    sensors.append(Point(stx, sty))

all_points = beacons + sensors
mds = [manhattan_distance(sensors[i], p) for i, p in enumerate(beacons)]
for i, s in enumerate(sensors):
    for limit in orthogonal_points(s, dist=mds[i]):
        all_points.append(limit)

min_g, max_g = limits_of_point_set(all_points)
print("Limits", min_g, max_g)

# useful in test mode
# space = {}
# initialise_space()
# draw_space()

no_beacon = set()
# no_beacon_y = 10  # test value
no_beacon_y = 2000000
for i,s in enumerate(sensors):
    md = mds[i]

    # will the scope of the sensor reach it
    y_diff = abs(no_beacon_y - s.y)
    if y_diff <= md:
        # if so then which part of the row will be covered
        x_range = md - y_diff
        x_from = s.x - x_range
        x_to = s.x + x_range
        for x in range(x_from, x_to+1):
            b_chk = (x, no_beacon_y)
            if b_chk not in beacons:  # don't add existing beacons to the set
                no_beacon.add(x)

print("A:", len(no_beacon))

# Part B in separate module, and requires a very different approach
