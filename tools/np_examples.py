import numpy as np


a = np.arange(1, 31)
print(a)

# 10 rows of 3
g = np.reshape(a, (10, 3))
print(g)

# 5 rows of 6
g = np.reshape(a, (5, 6))
print(g)


def my_func(x):
    return x * 2


t = np.apply_along_axis(my_func, axis=1, arr=g)

print(g)
print(g[4, :])  # 5th row
print(g[:, 1])  # 2nd column
print(g[1:3, 0:3])  # rows 2-3,  columns 1-3


def to_edge(a, row, col):
    return [(a[row+1:, col]), (a[:row, col]), (a[row, col+1:]), (a[row, :col])]

print("to edge")
print(g)
to_edge(g,2,1)


def get_index(x):
    return x*3

u_get_index = np.frompyfunc(get_index, 1, 1)
g3 = u_get_index(g)
print(g3)

h = np.full_like(g, 0)
for idx, val in np.ndenumerate(g):
    r = idx[0]
    c = idx[1]


print(h)




