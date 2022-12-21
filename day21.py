""" Day 21 in the AoC house - Monkey Maths
time taken : 2hrs
leaderboard 1,1

Interesting double binary problem
only 1 human means a linear factor we can narrow in on

"""
from time import time

from anytree import AnyNode

from tools.common import file_to_list

stm = time()


class Monkey:

    def __init__(self, name):
        self.name = name
        self.is_expr = False
        self.value = None
        self.a = ""
        self.op = ""
        self.b = ""

    def __str__(self):
        if self.is_expr:
            return f"{self.name} {self.a} {self.op} {self.b}"
        else:
            return f"{self.name} {self.value}"


lines = file_to_list("day21.txt")
monkies = {}
for line in lines:
    data = line.split(":")
    m_id = data[0]
    m_say = data[1].strip()
    monkey = Monkey(m_id)
    if m_say.isnumeric():
        monkey.value = int(m_say)
    else:
        monkey.is_expr = True
        monkey.a = m_say[:4]
        monkey.op = m_say[5]
        monkey.b = m_say[7:]

    monkies[m_id] = monkey


def add_monkey_business(node):
    mky: Monkey = node.m
    if not mky.is_expr:
        return
    a = AnyNode(m=monkies[mky.a], parent=node)
    add_monkey_business(a)
    b = AnyNode(m=monkies[mky.b], parent=node)
    add_monkey_business(b)


root = AnyNode(m=monkies["root"])
add_monkey_business(root)


def evaluate_node(node: AnyNode):
    if node.m.is_expr:
        node_a = node.children[0]
        node_b = node.children[1]
        val_a = evaluate_node(node_a)
        val_b = evaluate_node(node_b)
        expr = f"{val_a} {node.m.op} {val_b}"
        return eval(expr)
    else:
        return node.m.value


part_a = int(evaluate_node(root))
print(f"A: {part_a}")

etm = time()
elapsed_time = etm - stm
print(f"Time for part A: {elapsed_time:.3f} s")


root.m.op = "-"
human = [m for m in monkies.values() if m.name == "humn"][0]


def examine_range(start, end=None):
    if not end:
        end = start + 1

    min_val = None
    max_val = None

    for x in range(start, end):
        human.value = x
        root_val = evaluate_node(root)
        if min_val:
            min_val = min(root_val, min_val)
        else:
            min_val = root_val

        if max_val:
            max_val = max(root_val, min_val)
        else:
            max_val = root_val

    return min_val, max_val


def try_value(x):
    human.value = x
    return evaluate_node(root)


def signs_differ(a, b):
    return a < 0 < b or a > 0 > b


def find_seed_values():
    e = 1
    res = None
    while True:
        last_res = res
        res = try_value(e)
        if last_res and signs_differ(res, last_res):
            return e // 2, e
        e *= 2


def find_human_value(a, b):
    while True:

        m = (a + b) // 2

        res_a = try_value(a)
        res_m = try_value(m)
        res_b = try_value(b)

        if res_a == 0:
            return a
        if res_m == 0:
            return m
        if res_b == 0:
            return b

        if signs_differ(res_a, res_m):
            return find_human_value(a, m)
        else:
            return find_human_value(m, b)


seed_min, seed_max = find_seed_values()
print(f"Between {seed_min} {seed_max}")
part_b = find_human_value(seed_min, seed_max)
print(f"B: {part_b}")

etm = time()
elapsed_time = etm - stm
print(f"Time for part B: {elapsed_time:.3f} s")
