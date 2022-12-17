"""Slicing by example"""

odds = [x * 2 + 1 for x in range(20)]
print(odds)

print(f"odds[2:4]={odds[2:4]}")
print(f"odds[-4:-2]={odds[-4:-2]}")
print(f"odds[:3]={odds[:3]}")
print(f"odds[:-2]={odds[:-2]}")
print(f"odds[5:]={odds[5:]}")
print(f"odds[-3:]={odds[-3:]}")

print(f"odds[3:1]={odds[3:1]}")
print(f"odds[3:1:-1]={odds[3:1:-1]}")

print(f"odds[::]={odds[::]}")
print(f"odds[::2]={odds[::2]}")
print(f"odds[::-1]={odds[::-1]}")
print(f"odds[::-3]={odds[::-3]}")

print(f"odds[4:8:2]={odds[4:8:2]}")
print(f"odds[4:9:2]={odds[4:9:2]}")

s = slice(3, 12, 2)
print(f"s={s}")
t = s.indices(len(odds))
print(f"tuple of indexes is t={t}")
print([x for x in range(*t)])
print(odds[s])

x = range(4,10)
y = range(9,12)


def range_intersect(r1, r2):
    return range(max(r1.start,r2.start), min(r1.stop,r2.stop)) or None


def range_union(r1, r2):
    if range_intersect(r1, r2):
        return range(min(r1.start,r2.start), max(r1.stop,r2.stop))
    return None



z = range_union(x,y)
print(z)

print(list(range(10,-1,-1)))