""" Day 20 in the AoC house - Encryption Wheel
time taken : 1 hr
leaderboard 1,1

Use a Wheel like a linked list connecting the tail back to the head

"""
from time import time

from tools.common import file_to_list


class Node:
    def __init__(self, data):
        self.data = data
        self.next = self
        self.prev = self
        self.og_next = None
        self.og_prev = None

    def __str__(self):
        return str(self.data)


class Wheel:
    def __init__(self):
        self.length = 0
        self.start = None
        self.current = None
        self.zero_node = None

    def __str__(self):
        return str(self.as_list_from())

    def as_list_from(self, node=None):
        if not node:
            node = self.zero_node
        if not node:
            raise ValueError("from where?")
        r = []
        for i in range(self.length):
            r.append(node.data)
            node = node.next
        return r

    def add(self, val, after=None, enc_key=1):
        if isinstance(val, Node):
            n = val
        else:
            val = val * enc_key
            n = Node(val)
            if n.data == 0:
                self.zero_node = n
        if self.length == 0:
            self.current = n
            self.start = n
            after = n

        if not after:
            after = self.current

        before = after.next

        after.next = n
        n.prev = after

        before.prev = n
        n.next = before

        self.current = n
        self.length += 1
        return n

    def remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev
        self.length -= 1

    def save_to_og(self):
        node: Node = self.start
        for i in range(self.length):
            node.og_next = node.next
            node.og_prev = node.prev
            node = node.next

    def mixing(self, start: Node = None, amt=None):
        if not amt:
            amt = self.length
        if start is None:
            start = self.start
        node: Node = start
        for i in range(amt):

            val = node.data
            self.remove(node)
            val = val % self.length
            after_node = node.prev

            for j in range(val):
                after_node = after_node.next

            self.add(node, after_node)
            node = node.og_next


stm = time()

input_seq = []
lines = file_to_list("day20.txt")
for line in lines:
    input_seq.append(int(line))


print(f"Size: {len(input_seq)}")
print(f"Limits: {min(input_seq)}, {max(input_seq)}")
print(f"Unique: {len(set(input_seq))}")
print(f"Zeros {len([i for i in input_seq if i == 0])}")


def get_at(lst, x):
    x = x % len(lst)
    return lst[x]


input_list = Wheel()
for data in input_seq:
    input_list.add(data)

# remember our original list order
input_list.save_to_og()

# mix them up
input_list.mixing(amt=input_list.length)

shuffled = input_list.as_list_from()
total = 0
for i in range(1000, 3001, 1000):
    v = get_at(shuffled, i)
    total += v
print(f"A: {total}")

etm = time()
elapsed_time = etm - stm
print(f"Time for part A: {elapsed_time:.3f} s")

#
# Part B
#

enc_key = 811589153
input_list = Wheel()
for data in input_seq:
    input_list.add(data, enc_key=enc_key)
input_list.save_to_og()

# shuffle 10 times
for i in range(10):
    input_list.mixing(amt=input_list.length)

shuffled = input_list.as_list_from()

total = 0
for i in range(1000, 3001, 1000):
    v = get_at(shuffled,i)
    total += v
print(f"B: {total}")

etm = time()
elapsed_time = etm - stm
print(f"Time for part B: {elapsed_time:.3f} s")