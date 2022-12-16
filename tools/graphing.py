import math
from itertools import chain, combinations


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


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
