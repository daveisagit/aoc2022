""" Day 15 in the AoC house - Sensors and Beacons
time taken : 2hr
leaderboard 2

shapely was a life saver

"""
from tools.common import file_to_list
from tools.grid import manhattan_distance, orthogonal_points, Point as pnt
from shapely import box, difference, Polygon

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
    beacons.append(pnt(btx, bty))
    sensors.append(pnt(stx, sty))


gs = 4000000
# gs = 20
land = Polygon(box(0, 0, gs, gs))

mds = [manhattan_distance(sensors[i], p) for i, p in enumerate(beacons)]
for i, s in enumerate(sensors):
    md = mds[i]
    shp = Polygon(orthogonal_points(s, dist=md))
    land = difference(land, shp)


def output_result(g):
    print()
    print(g)
    min_x, min_y, max_x, max_y = g.bounds
    x = int(min_x + max_x) // 2
    y = int(min_y + max_y) // 2
    ans = x * 4000000 + y
    print(f"x={x} y={y}")
    print(f"B: {x} x 4000000 + {y} = {ans}")


if land.geom_type == "MultiPolygon":
    # test data gives rise to two polygons ??
    for g in land.geoms:
        output_result(g)
else:
    output_result(land)


# not used but might useful another time
def extract_poly_coords(geom):
    if geom.geom_type == 'Polygon':
        exterior_coords = geom.exterior.coords[:]
        interior_coords = []
        for interior in geom.interiors:
            interior_coords += interior.coords[:]
    elif geom.geom_type == 'MultiPolygon':
        exterior_coords = []
        interior_coords = []
        for part in geom:
            epc = extract_poly_coords(part)  # Recursive call
            exterior_coords += epc['exterior_coords']
            interior_coords += epc['interior_coords']
    else:
        raise ValueError('Unhandled geometry type: ' + repr(geom.type))
    return {'exterior_coords': exterior_coords,
            'interior_coords': interior_coords}