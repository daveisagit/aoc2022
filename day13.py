""" Day 13 in the AoC house -
time taken : 2hr
leaderboard 2,2

"""
from functools import cmp_to_key
from tools.common import file_to_list
from anytree import AnyNode, RenderTree, AsciiStyle


class Packet:

    def __init__(self, raw):
        super().__init__()
        self.raw = raw
        self.tree = AnyNode()
        self.parse()

    def __repr__(self):
        return self.raw

    def parse(self):
        """Build a tree structure of the packet"""
        cv = ""
        cp = self.tree
        for ch in self.raw:

            if ch == "[":
                cp = AnyNode(parent=cp, list_container=True)

            elif ch in [
                ",",
                "]"
            ]:
                if cv:
                    cv = int(cv)
                    AnyNode(parent=cp, number=cv)

                cv = ""
                if ch == "]":
                    cp = cp.parent

            else:
                cv += ch


def get_child_at_index_or_none(a_list, idx):
    try:
        return a_list[idx]
    except IndexError:
        return None


def compare_integers(a, b):
    return (a.number > b.number) - (a.number < b.number)


def compare_packets(a, b):
    return compare_trees(a.tree, b.tree)


def compare_trees(a, b):

    if a is None and b is None:
        return 0

    if a is not None and b is None:
        return 1

    if a is None and b is not None:
        return -1

    if hasattr(a, "number") and hasattr(b, "number"):
        return compare_integers(a, b)

    if hasattr(a, "number"):
        b = get_child_at_index_or_none(b.children, 0)
        return compare_trees(a, b)

    if hasattr(b, "number"):
        a = get_child_at_index_or_none(a.children, 0)
        return compare_trees(a, b)

    if not hasattr(a, "number") and not hasattr(b, "number"):
        max_c = max(len(a.children), len(b.children))
        for idx in range(max_c):
            ac = get_child_at_index_or_none(a.children, idx)
            bc = get_child_at_index_or_none(b.children, idx)
            res = compare_trees(ac, bc)
            if res != 0:
                return res
        return 0


lines = file_to_list("day13.txt")

# Pat A
pairs = []
for i, line in enumerate(lines):
    if i % 3 == 0:
        pair = [Packet(line)]
    if i % 3 == 1:
        pair.append(Packet(line))
        pairs.append(pair)

results = [compare_packets(pair[0], pair[1]) for pair in pairs]
results = [1 if res == -1 else 0 for res in results]
ans_a = sum([(idx + 1) * res for idx, res in enumerate(results)])
print("A:", ans_a)


# Part B
packets = []
for idx, line in enumerate(lines):
    if line:
        packets.append(Packet(line))
packets.append(Packet("[[2]]"))
packets.append(Packet("[[6]]"))

sorted_list = sorted(packets, key=cmp_to_key(compare_packets))
raw_list = [r.raw for r in sorted_list]
idx_a = raw_list.index("[[2]]") + 1
idx_b = raw_list.index("[[6]]") + 1
print("B:", idx_a * idx_b)

# pkt = sorted_list[-1]
# print(pkt)
# print(RenderTree(pkt.tree, style=AsciiStyle()))

