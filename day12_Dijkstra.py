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


import numpy as np

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
print(hills)


def neighbours(x):
    r = []
    if x % cols != 0:
        r.append(x - 1)
    if x % cols != cols-1:
        r.append(x + 1)
    if x >= cols:
        r.append(x - cols)
    if x < cols * (rows - 1):
        r.append(x + cols)
    return r

