from collections import namedtuple

import networkx as nx
import numpy as np

Point = namedtuple(
    "P", ["row", "col", ]
)


def limit_nw(points):
    x, y = zip(*points)
    return min(x), min(y)


def limit_se(points):
    x, y = zip(*points)
    return max(x), max(y)


def map_point_to_node(vg, p: Point):
    possible = [n for n, d in vg.nodes().items() if p in d["points"]]
    if len(possible) > 1:
        raise ValueError(f"More than 1 node for {p} : {possible}")
    elif len(possible) == 1:
        return possible[0]
    else:
        return None


def parse_points(points, edge_length=1):
    points = [Point(p[0] // edge_length, p[1] // edge_length) for p in points]
    vg = nx.Graph()
    faces = []

    for idx, p in enumerate(sorted(points)):
        p = Point(*p)

        vg.add_node(idx, points={p}, faces=set())
        v = map_point_to_node(vg, p)

        p_n = Point(p.row - 1, p.col)
        p_w = Point(p.row, p.col - 1)
        p_nw = Point(p.row - 1, p.col - 1)

        v_n = map_point_to_node(vg, p_n)
        if v_n is not None:
            vg.add_edge(v_n, v)

        v_w = map_point_to_node(vg, p_w)
        if v_w is not None:
            vg.add_edge(v_w, v)

        v_nw = map_point_to_node(vg, p_nw)
        if v_n is not None and v_w is not None and v_nw is not None:
            faces.append(p_nw)

    faces_update = {}
    for f in faces:
        f: Point
        f_s = Point(f.row + 1, f.col)
        f_e = Point(f.row, f.col + 1)
        f_se = Point(f.row + 1, f.col + 1)

        v = map_point_to_node(vg, f)
        faces_for_node = faces_update.get(v, set())
        faces_for_node.add(f)
        faces_update[v] = faces_for_node

        v_s = map_point_to_node(vg, f_s)
        faces_for_node = faces_update.get(v_s, set())
        faces_for_node.add(f)
        faces_update[v_s] = faces_for_node

        v_e = map_point_to_node(vg, f_e)
        faces_for_node = faces_update.get(v_e, set())
        faces_for_node.add(f)
        faces_update[v_e] = faces_for_node

        v_se = map_point_to_node(vg, f_se)
        faces_for_node = faces_update.get(v_se, set())
        faces_for_node.add(f)
        faces_update[v_se] = faces_for_node

    nx.set_node_attributes(vg, faces_update, "faces")

    return vg


def dump_net_data(vg):
    print(vg)
    for n in vg.nodes(data=True):
        print(n)


def draw_net(vg, scale=4, labels=None):
    print()
    points = sorted([p for n in vg.nodes(data=True) for p in list(n[1]["points"])])
    sz = Point(*limit_se(points))
    sz = (scale * (sz.row + 1), scale * (sz.col + 1))
    net_layout = np.full(sz, dtype=str, fill_value=" ")
    label = {}
    for i, v in enumerate(sorted(vg.nodes)):
        if labels:
            label[v] = labels[i]
        else:
            label[v] = chr(ord("A") + i)

    for e in vg.edges():
        for p1 in list(vg.nodes[e[0]]["points"]):
            for p2 in list(vg.nodes[e[1]]["points"]):
                if p1.row == p2.row:
                    for x in range(min(p1.col, p2.col) * scale, max(p1.col, p2.col) * scale):
                        net_layout[p1.row * scale, x] = "-"
                if p1.col == p2.col:
                    for x in range(min(p1.row, p2.row) * scale, max(p1.row, p2.row) * scale):
                        net_layout[x, p1.col * scale] = "|"

    for p in points:
        p = Point(*p)
        net_layout[p.row * scale, p.col * scale] = label[map_point_to_node(vg, p)]

    for row in net_layout:
        print("".join(row))


def nodes_of_face(vg, f):
    return [n for n, d in vg.nodes().items() if f in d["faces"]]


def nodes_are_on_same_face(vg, u, v) -> bool:
    fu: set = vg.nodes[u]["faces"]
    fv: set = vg.nodes[v]["faces"]
    return not fu.isdisjoint(fv)


def nodes_are_on_adjacent_faces(vg, u, v) -> bool:
    """Returns True if the nodes are on adjacent faces"""
    for fu in vg.nodes[u]["faces"]:
        for fv in vg.nodes[v]["faces"]:
            su = set(nodes_of_face(vg, fu))
            sv = set(nodes_of_face(vg, fv))
            if len(su.intersection(sv)) == 2:
                return True
    return False


def merge_two_nodes(cur_vg, leaver, remainer):
    """Give all leavers data to the remainer. Re-map the edges that were linked to leaver
    to now link to the remainer and remove the leaver node"""
    vg = cur_vg.copy()
    vl = vg.nodes[leaver]
    vr = vg.nodes[remainer]
    vl_p: set = vl["points"]
    vr_p: set = vr["points"]
    vl_f: set = vl["faces"]
    vr_f: set = vr["faces"]

    new_position_set = vl_p.union(vr_p)
    new_face_set = vl_f.union(vr_f)
    nx.set_node_attributes(vg, {remainer: new_position_set}, "points")
    nx.set_node_attributes(vg, {remainer: new_face_set}, "faces")

    # get all neighbours of leaver and attach them to remainer
    for nl in nx.neighbors(vg, leaver):
        vg.add_edge(remainer, nl)

    # remove leaver
    vg.remove_node(leaver)

    return vg


# def is_solved(vg) -> bool:
#     deg_3 = [v for v in vg.nodes if len(vg.edges(v)) == 3]
#     if len(vg.nodes) == 8 and len(vg.edges) == 12 and len(deg_3) == 8:
#         return True
#     return False

def is_solved(vg) -> bool:
    """Once the final fold as happened the Euler char being 2 will mean
    all faces are accounted for and there no extra external region"""
    deg_3 = [v for v in vg.nodes if len(vg.edges(v)) == 3]
    # if len(vg.edges) - len(vg.nodes) == 4 and len(deg_3) == len(vg.nodes):
    if len(vg.edges) - len(vg.nodes) == 4:
        return True
    return False


def is_still_valid(vg) -> bool:
    """No point going any further if we go below certain limits"""
    if len(vg.nodes) >= 8 and len(vg.edges) >= 12:
        return True
    return False


def cubify(vg):
    """Recursively merge candidate nodes until we reach the cube"""

    if is_solved(vg):
        return vg

    if not is_still_valid(vg):
        return None

    deg_4 = [v for v in vg.nodes if len(vg.edges(v)) == 4]
    for v4 in deg_4:

        candidates = [v for v in vg.neighbors(v4) if len(vg.edges(v)) < 4]
        for i, u in enumerate(candidates):
            for v in candidates[i+1:]:
                # for each pair of candidate nodes

                if nodes_are_on_same_face(vg, u, v):
                    continue

                if nodes_are_on_adjacent_faces(vg, u, v):
                    continue

                new_vg = merge_two_nodes(vg, u, v)

                result = cubify(new_vg)
                if result:
                    return result

    return None


def faces_of(vg):
    """All the faces on the vertex graph"""
    return set([p for n in vg.nodes(data=True) for p in list(n[1]["faces"])])


def edge_from_points(vg, left_point, right_point):
    left_node = map_point_to_node(vg, left_point)
    right_node = map_point_to_node(vg, right_point)
    e = (left_node, right_node)
    return e


def edges_of_face(vg, f):
    """Generate all the directions, edges for a face"""
    left_point = Point(f.row, f.col + 1)
    right_point = Point(f.row + 1, f.col + 1)
    e = edge_from_points(vg, left_point, right_point)
    yield 0, e

    left_point = Point(f.row + 1, f.col + 1)
    right_point = Point(f.row + 1, f.col)
    e = edge_from_points(vg, left_point, right_point)
    yield 1, e

    left_point = Point(f.row + 1, f.col)
    right_point = Point(f.row, f.col)
    e = edge_from_points(vg, left_point, right_point)
    yield 2, e

    left_point = Point(f.row, f.col)
    right_point = Point(f.row, f.col + 1)
    e = edge_from_points(vg, left_point, right_point)
    yield 3, e


def face_graph(vg):
    """Create a directed graph of the faces"""
    fg = nx.DiGraph()
    for f in faces_of(vg):
        fg.add_node(f)

    for f in fg.nodes:
        for d, e in edges_of_face(vg, f):
            for f2 in fg.nodes:
                if f2 != f:
                    n_f2 = nodes_of_face(vg, f2)
                    if e[0] in n_f2 and e[1] in n_f2:
                        fg.add_edge(f, f2, dir=d, edge=e)

    return fg


def dump_face_graph(fg):
    print(fg)
    for f in fg.nodes:
        print(f"Face {f}")
        for f2 in fg.edges(f, data=True):
            print(f2)
