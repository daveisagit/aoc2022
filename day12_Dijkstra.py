"""
function Dijkstra(Graph, source):
       dist[source]  := 0                     // Distance from source to source is set to 0
       for each vertex v in Graph:            // Initializations
           if v ≠ source
               dist[v]  := infinity           // Unknown distance function from source to each node set to infinity
           add v to Q                         // All nodes initially in Q

      while Q is not empty:                  // The main loop
          v := vertex in Q with min dist[v]  // In the first run-through, this vertex is the source node
          remove v from Q

          for each neighbor u of v:           // where neighbor u has not yet been removed from Q.
              alt := dist[v] + length(v, u)
              if alt < dist[u]:               // A shorter path to u has been found
                  dist[u]  := alt            // Update distance of u

      return dist[]
  end function

"""
import math

from tools.common import file_to_list

start = 0
end = 0
cols = 0
hills = []
lines = file_to_list("day12.txt")
rows = len(lines)
for line in lines:
    cols = len(line)
    for ch in line:
        h = ord(ch) - 97
        if ch == "S":
            h = -1
            start = len(hills)
        if ch == "E":
            h = 26
            end = len(hills)
        hills.append(h)

print("cols", cols)
print("rows", rows)
print("start", start)
print("end", end)
print(hills)


def neighbours_index(x):
    r = []
    if x % cols != 0:
        r.append(x - 1)
    if x % cols != cols - 1:
        r.append(x + 1)
    if x >= cols:
        r.append(x - cols)
    if x < cols * (rows - 1):
        r.append(x + cols)
    return r


def valid_neighbours_ascent(x):
    for n in neighbours_index(x):
        if hills[n] - hills[x] <= 1:
            yield n


def valid_neighbours_decent(x):
    for n in neighbours_index(x):
        if hills[x] - hills[n] <= 1:
            yield n


ascent_graph = {start: {}}
descent_graph = {end: {}}


def extend_graph(graph, get_adjacent_vertices_function: callable, here=None):
    if here is None:
        here = list(graph.keys())[0]
    new_neighbours = [n for n in get_adjacent_vertices_function(here) if n not in graph]
    for n in new_neighbours:
        graph[here][n] = 1
        graph[n] = {}
    for n in new_neighbours:
        extend_graph(graph, get_adjacent_vertices_function, here=n)


extend_graph(ascent_graph, valid_neighbours_ascent)
print("Ascent", ascent_graph)

extend_graph(descent_graph, valid_neighbours_decent)
print("Descent", descent_graph)


def dijkstra(graph, source_key) -> dict:
    """Given a graph (dict) where the keys are vertex ids
    and the values are dicts of adjacent vertices

    The adjacent vertex dict has values which represent the cost of the edge

    returns a dict of vertex and their path cost from the source
    """

    # initialise things
    remaining_pool = set()
    distances = {v: math.inf for v in graph.keys()}
    distances[source_key] = 0
    for vk in graph.keys():
        # put every vertex key in the pool
        remaining_pool.add(vk)

    # while some in the pool
    while remaining_pool:
        # find one from the pool with the smallest distance
        smallest_distance = math.inf
        vk = None
        for q in remaining_pool:
            if distances[q] < smallest_distance:
                vk = q  # this is it
                smallest_distance = distances[q]

        # remove it from the pool
        remaining_pool.remove(vk)

        # for adjacent vertex in the pool
        v = graph[vk]
        for uk, l in v.items():
            if uk in remaining_pool:

                # get the cost for using this adjacent vertex
                alt = distances[vk] + l

                # if the alternative is better then revise
                if alt < distances[uk]:
                    distances[uk] = alt

    return distances


ds = dijkstra(ascent_graph, start)
print(ds)
print(ds[end])


ds = dijkstra(descent_graph, end)
print(ds)
print(ds[start])
