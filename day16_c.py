""" Day 16 in the AoC house -
time taken :
leaderboard

"""
import math

from anytree import AnyNode, AsciiStyle, RenderTree

from tools.common import file_to_list
from itertools import chain, combinations

lines = file_to_list("day16.txt")


class Valve:

    def __init__(self, name, rate, leads_to):
        # super().__init__()
        self.name = name
        self.rate = int(rate)
        self.leads_to = {l:1 for l in leads_to}
        self.open = False
        self.targets = {}

    def __repr__(self):
        if self.open:
            return f"{self.name} (O)"
        else:
            return f"{self.name}"



def dijkstra(graph, source_key) -> dict:
    """Given a graph (dict) where the keys are vertex ids
    and the values are dicts of adjacent vertices

    The adjacent vertex dict has values which represent the cost of the edge

    returns a dict of vertices and their total path cost from the source
    """

    # initialise things
    remaining_pool = set()
    path_costs = {v: math.inf for v in graph.keys()}
    path_costs[source_key] = 0  # the cost of the start is always zero
    for vk in graph.keys():
        # put every vertex key in the pool
        remaining_pool.add(vk)

    # while there are some in the pool
    while remaining_pool:
        # find one from the pool with the smallest distance
        smallest_distance = math.inf
        vk = None
        for q in remaining_pool:
            if path_costs[q] < smallest_distance:
                vk = q  # this is it
                smallest_distance = path_costs[q]

        if vk is None:
            # then none of the vertices left in the pool are connected to the source
            break

        # remove it from the pool
        remaining_pool.remove(vk)

        v = graph[vk]
        for uk, cost in v.items():  # for adjacent vertices
            if uk in remaining_pool:  # in the pool

                # get the total path cost for using this adjacent vertex
                alt = path_costs[vk] + cost

                # if the alternative is better, then revise the cost
                if alt < path_costs[uk]:
                    path_costs[uk] = alt

    return path_costs


valves = {}
for line in lines:
    v = line[6:8]
    r = line.split("=")
    r = r[1].split(";")[0]
    dst = line.split(",")
    dst[0] = dst[0][-2:]
    dst = [v.strip() for v in dst]
    vc = Valve(v, r, dst)
    valves[v] = vc


nzs = [v for v in valves.values() if v.rate > 0]
nz = [v for v in valves.values() if v.rate > 0]
nzk = [v.name for v in valves.values() if v.rate > 0]
print(len(nz))
print(nz)
nzs.append(valves["AA"])
print(nzs)

v_graph = {}
for vv in valves.values():
    v_graph[vv.name] = vv.leads_to

print(v_graph)

for vv in nzs:
    dists = dijkstra(v_graph, vv.name)
    for k, v in dists.items():
        if k in nzk:
            vv.targets[k] = v

for vv in nzs:
    print(f"{vv} : {vv.targets}")


class VNode(AnyNode):
    @property
    def ren(self):
        return f"{self.v} {self.amt}"


my_subset = [vv.name for vv in nz]


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


psl = list(powerset(my_subset))
print(psl)
print(len(psl))


def add_child(cn: VNode, subset):
    done = [n.v.name for n in cn.ancestors]
    for nvk, tt in cn.v.targets.items():
        if nvk not in done and nvk != cn.v.name and nvk in subset:
            nvo = valves[nvk]
            ntt = cn.tt + tt + 1
            run_for = 26 - ntt
            if run_for > 0:
                amt = nvo.rate * run_for
                nn = VNode(v=nvo, parent=cn, tt=cn.tt + tt + 1, amt=cn.amt+amt)
                add_child(nn, subset)


cnt=0
all_v_set = set(nzk)
res=[]
psl = [s for s in psl if len(s) <= len(all_v_set) // 2]
print(len(psl))


for my_subset in psl:
    cnt +=1
    print(cnt)

    my_subset = set(my_subset)
    e_subset = all_v_set.difference(my_subset)
    # print(my_subset, e_subset)

    my_root = VNode(v=valves["AA"], tt=0, amt=0)
    e_root = VNode(v=valves["AA"], tt=0, amt=0)

    add_child(my_root, my_subset)
    add_child(e_root, e_subset)

    my_max = max([l.amt for l in my_root.leaves])
    e_max = max([l.amt for l in e_root.leaves])
    the_max = my_max + e_max
    res.append(the_max)

print(max(res))






