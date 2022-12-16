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
from tools.common import file_to_list
from tools.graphing import dijkstra

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


ascent_graph = {}
for i, h in enumerate(hills):
    ascent_graph[i] = {n: 1 for n in valid_neighbours_ascent(i)}

descent_graph = {}
for i, h in enumerate(hills):
    descent_graph[i] = {n: 1 for n in valid_neighbours_decent(i)}


costs = dijkstra(ascent_graph, start)
print("A: ", costs[end])  # the path cost at the end


costs = dijkstra(descent_graph, end)
print(
    "B: ",
    min([
            d for v, d in costs.items()
            if hills[v] == 0  # only consider "a"'s
        ])  # the smallest path cost from the end to any "a"
)
