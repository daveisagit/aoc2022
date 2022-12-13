""" Just use eval doh """
from functools import cmp_to_key
from tools.common import file_to_list


def get_child_at_index_or_none(a_list, idx):
    try:
        return a_list[idx]
    except IndexError:
        return None


def compare_packets(a, b):
    if a is None and b is None:
        return 0

    if a is not None and b is None:
        return 1

    if a is None and b is not None:
        return -1

    if isinstance(a, int) and isinstance(b, int):
        return (a > b) - (a < b)

    ca = a
    cb = b
    if isinstance(a, int):
        ca = [a]
    if isinstance(b, int):
        cb = [b]

    max_c = max(len(ca), len(cb))
    for idx in range(max_c):
        ac = get_child_at_index_or_none(ca, idx)
        bc = get_child_at_index_or_none(cb, idx)
        res = compare_packets(ac, bc)
        if res != 0:
            return res
    return 0


lines = file_to_list("day13.txt")

# Part A
pairs = []
for i, line in enumerate(lines):
    if i % 3 == 0:
        pair = [eval(line)]
    if i % 3 == 1:
        pair.append(eval(line))
        pairs.append(pair)

results = [compare_packets(pair[0], pair[1]) for pair in pairs]
results = [1 if res == -1 else 0 for res in results]
ans_a = sum([(idx + 1) * res for idx, res in enumerate(results)])
print("A:", ans_a)


# Part B
packets = []
for idx, line in enumerate(lines):
    if line:
        packets.append(line)
packets.append("[[2]]")
packets.append("[[6]]")
packets = [eval(packet) for packet in packets]

sorted_list = sorted(packets, key=cmp_to_key(compare_packets))
idx_a = sorted_list.index([[2]]) + 1
idx_b = sorted_list.index([[6]]) + 1
print("B:", idx_a * idx_b)
