"""
https://oeis.org/A000105
"""

import numpy as np

from tools import cubenet
from tools.cubenet import cubify, parse_points

DIRECTIONS = [
    (0, 1), (1, 0), (0, -1), (-1, 0)
]

CORNERS = [
    (0, 0), (1, 0), (0, 1), (1, 1)
]


def add_tuples(a, b):
    return tuple([sum(x) for x in zip(a, b)])


def sub_tuples(a, b):
    return tuple([x[0]-x[1] for x in zip(a, b)])


def top_left_tile(net):
    x, y = zip(*net)
    return min(x), min(y)


def surrounds(tile):
    for d in DIRECTIONS:
        yield add_tuples(tile, d)


def corners(tile):
    for d in CORNERS:
        yield add_tuples(tile, d)


def normalise(net):
    top_left = top_left_tile(net)
    return tuple(sorted(tuple(sub_tuples(tile, top_left) for tile in net)))


def matrix_to_net(m):
    net = tuple()
    for r, row in enumerate(m):
        for c, v in enumerate(row):
            if v == "X":
                net += ((r, c), )
    return normalise(net)


def required_shape(net):
    x, y = zip(*net)
    return max(x) + 1, max(y) + 1


def net_to_matrix(net):
    shape = required_shape(net)
    net_matrix = np.full(shape, " ", dtype=str)
    for tile in net:
        net_matrix[tile] = "X"
    return net_matrix


def dihedral_nets(net):
    net_matrix = net_to_matrix(net)
    for i in range(2):
        for j in range(4):
            rotated = np.rot90(net_matrix, j)
            yield normalise(matrix_to_net(rotated))
        net_matrix = np.fliplr(net_matrix)


def next_set(nets=None):
    if not nets:
        return ((0, 0),),

    new_nets = tuple()
    sym_nets = tuple()
    for this_net in nets:
        for tile in this_net:
            for next_tile in surrounds(tile):
                if next_tile not in this_net:
                    new_net = this_net + (next_tile, )
                    new_net = normalise(new_net)
                    if new_net not in sym_nets:
                        for sym_net in dihedral_nets(new_net):
                            sym_nets += (sym_net,)
                        new_nets = new_nets + (new_net, )

    return new_nets


def net_points(net):
    set_of_points = set()
    for tile in net:
        for point in corners(tile):
            set_of_points.add(point)
    return tuple(sorted(tuple(set_of_points)))


def draw_net(net):
    m = net_to_matrix(net)
    for row in m:
        print("".join(row))


def nets_of_size(sz, print_working=False):
    nets = None
    for i in range(sz):
        nets = next_set(nets)
        if print_working:
            print(f"Nominoe size={i+1} : nets={len(nets)}")
    return nets


def draw_nets(nets, inc_cube_net=False, inc_dihedral=False):
    for idx, net in enumerate(nets):
        print()
        print("==========================================")
        print(f"Net #: {idx+1}")
        print("==========================================")
        di_nets = [net]
        if inc_dihedral:
            di_nets = list(dihedral_nets(net))

        for x, net in enumerate(di_nets):
            if inc_dihedral:
                print(f"{idx+1}.({chr(ord('a') + x)})")
                print()
            draw_net(net)
            if inc_cube_net:
                cb = cube_net(net)
                if cb:
                    cubenet.draw_net(cb)


def cube_net(net):
    points = net_points(net)
    vg = parse_points(points)
    return cubify(vg)


def cube_nets(nets, progress=False):
    cub_nets = []
    for i, net in enumerate(nets):
        if progress:
            print(f"{i+1} of {len(nets)}")
        cub = cube_net(net)
        if cub:
            cub_nets.append(net)
    return tuple(cub_nets)


# all_nets = nets_of_size(10, print_working=True)
# all_nets = cube_nets(all_nets, progress=True)
# draw_nets(all_nets, inc_cube_net=True, inc_dihedral=True)
# print(f"Number of cube nets: {len(all_nets)}")
